# 21 — Busca Full-Text e Armazenamento de Arquivos (Storage + Metadados)

> Parte do [SDD v2](00-README.md). Validação de upload em [15](15-validacoes.md), seção 4.3. Eventos de indexação em [14](14-integracao-modulos.md). Isolamento de tenant em [03](03-dominio-tenancy.md). Criptografia em [05](05-seguranca.md). Retenção e expurgo em [07](07-privacidade-lgpd.md). Modelo de dados da v1 em `spec_object_storage_digital_assets.md`, seção 13.
> **Status:** D-13, D-14 e D-15 decididas pelo autor em 02/11/2026 (seção 9). OCR entra nesta versão. Os valores numéricos são padrões iniciais para medir, não garantias.
> **Atualização de 03/11/2026:** o armazenamento atende três contextos de documento, cada um com prefixo e prazo próprios. Ver [54](54-gestao-de-documentos-tres-contextos.md), seções 1 e 5.

---

## 1. Escopo

Este documento cobre duas capacidades compartilhadas por todos os módulos:

1. **Armazenamento de arquivos:** upload, validação, guarda, versionamento, download, retenção e expurgo de documentos, anexos, comprovantes, imagens e exportações.
2. **Busca:** localizar registros e documentos por nome, código e texto, respeitando permissão, tenant e unidade.

Fora de escopo: edição colaborativa de documento e assinatura digital com ICP-Brasil (ficam em Documentos, [12](12-catalogo-modulos.md)).

## 2. Princípios

1. **Módulos não acessam o armazenamento físico.** Acessam um bucket lógico por API. Ver a v1, seção 7.
2. **O nome do arquivo nunca é a chave de armazenamento.** A chave é gerada no servidor a partir de UUID.
3. **Arquivo é imutável por versão.** Nova versão gera nova chave. Nada é sobrescrito.
4. **Nada é baixável antes de validado.** Arquivo em `pendente_verificacao` ou `quarentena` não tem URL de download.
5. **Permissão é checada no momento do download e da busca,** não só no momento do upload.
6. **Exclusão é lógica, com expurgo controlado e com bloqueio por retenção legal.**

---

## 3. Arquitetura de armazenamento

### 3.1 Componentes

| Componente | Função |
|---|---|
| Armazenamento de objetos compatível com S3 | Guarda bytes. Bucket privado, sem acesso público. |
| Serviço de arquivos (backend) | Autoriza, valida metadados, emite URLs assinadas, registra eventos. |
| Metadados (banco relacional) | Bucket, arquivo, versão, estado, permissão e auditoria. Ver seção 4. |
| Verificador (worker) | Confere tipo real, tamanho, checksum e antivírus. Atualiza estado. |
| Gerador de derivados (worker) | Miniaturas, texto extraído por OCR (seção 3.10) e versão sem metadados. Roda em processo isolado. |
| Serviço de retenção (job) | Aplica política, expurgo e bloqueio legal. |

### 3.2 Layout no provedor

**[Decidida D-14]** Um bucket privado por ambiente, com prefixo por unidade (`unidade_uuid`, a unidade dona do banco de metadados, ver [03](03-dominio-tenancy.md), seção 1.1):

```
{unidade_uuid}/{bucket_code}/{file_uuid}/v{version}/original
{unidade_uuid}/{bucket_code}/{file_uuid}/v{version}/derivado-{tipo}
```

Alternativa: um bucket por tenant. Mais isolamento, mais custo e mais limites de provedor. Condição de falha da proposta: um erro de política no bucket único afeta todos os tenants. Mitigação: política de bucket com negação explícita por prefixo e revisão de política em CI.

### 3.3 Upload

1. Cliente pede `POST /api/v1/storage/buckets/{code}/uploads` com nome, tamanho declarado, checksum SHA-256 e tipo declarado. Serviço valida permissão, cota e tipo declarado contra a lista do bucket ([15](15-validacoes.md), seção 4.3).
2. Serviço cria registro com estado `pendente_upload` e devolve URL assinada de PUT, com validade de 15 min, `content-length` fixo e checksum esperado no cabeçalho.
3. Cliente envia direto ao provedor. Arquivos acima de 5 MB vão direto; arquivos menores podem passar pelo backend, com a mesma validação.
4. Provedor confirma o checksum. Se não bater, recusa o envio.
5. Evento `storage.file.uploaded` vai para a fila ([14](14-integracao-modulos.md), seção 5).
6. Verificador confere magic bytes, tipo real, tamanho e antivírus. Estado vai para `disponivel` ou `quarentena`.
7. Derivados são gerados só depois de `disponivel`.

Regras:

- Executável, script, macro ativa em Office e PDF com JavaScript são recusados e vão para quarentena.
- Nome original é guardado como metadado, sanitizado (sem caminho, sem caractere de controle, máximo 255).
- Limite de cota por bucket, reservado no início do upload e liberado se falhar.

### 3.4 Download

1. Usuário pede `GET /api/v1/storage/files/{uuid}/url`.
2. Serviço valida tenant, unidade, permissão do arquivo e estado `disponivel`.
3. Serviço emite URL assinada de GET com validade de 60 a 900 s (padrão 300 s), com `Content-Disposition: attachment` quando não for imagem de exibição.
4. Evento `storage.file.accessed` é gravado.

Documento confidencial (contracheque, laudo, contrato) recebe **marca d'água dinâmica** no derivado de visualização, com nome e CPF mascarado de quem visualiza ([05](05-seguranca.md), seção 2).

### 3.5 Versões

- Nova versão cria novo `version_number` e nova chave.
- Versão anterior fica acessível por permissão de histórico.
- Restaurar versão antiga cria nova versão cujo conteúdo é a versão restaurada. Não reaponta a chave antiga.

### 3.6 Exclusão, retenção e bloqueio legal

| Etapa | Ação | Reversível |
|---|---|---|
| Exclusão pelo usuário | Estado `lixeira` com `purge_at` | Sim, até `purge_at` |
| Expurgo | Job remove versões e derivados do provedor, mantém metadado mínimo (uuid, data, motivo) | Não |
| Bloqueio legal | Impede expurgo independente da política | Sim, por ato registrado |
| Backup | Retenção de backup seguida pela política; expurgo se propaga em até 35 dias **[Pendente: prazo de backup]** | Não |

Regras:

- Expurgo depende de política de retenção do bucket ([07](07-privacidade-lgpd.md), seção 5).
- Bloqueio legal exige permissão `storage.bloqueio.aplicar` e motivo.
- Titular pode pedir eliminação; arquivo sob obrigação legal permanece até o prazo legal, e o registro informa a exceção.

### 3.7 Criptografia

| Camada | Controle |
|---|---|
| Trânsito | TLS 1.2 mínimo, certificado validado. |
| Repouso (provedor) | Criptografia do lado do servidor, habilitada por padrão. |
| Repouso (aplicação) | Para buckets sensíveis (RH, SMT, Financeiro, Documentos restritos): envelope com chave de dados do tenant, protegida pela chave-mestra da biblioteca de cofre (ADR-05 em [02](02-arquitetura.md)). |
| Chave | Rotação anual da chave de dados, com reencriptação em lote e registro. |

### 3.8 Cota e custo

- Uso por bucket mantido em contador atualizado na mesma transação do metadado, com trava na linha do bucket.
- Alerta a 80% e bloqueio de novo upload a 100%.
- Arquivo expurgado libera a cota após confirmação do provedor.

### 3.9 Limites padrão

| Item | Valor inicial |
|---|---|
| Tamanho máximo por arquivo | 50 MB (documento), 10 MB (imagem), ajustável por bucket |
| Arquivos por lote de upload | 20 |
| Validade da URL de upload | 15 min |
| Validade da URL de download | 300 s padrão, 900 s máximo |
| Tempo máximo de estado `pendente_upload` | 24 h, depois descartado |

---

### 3.10 OCR de documentos digitalizados (D-15, decidida)

**Quando roda:** após `disponivel`, para imagem e para PDF sem camada de texto em alguma página. Arquivo em `quarentena` nunca passa por OCR.

**Execução:**

- Worker isolado: sem rede de saída, sem credenciais de produção, sem acesso ao banco. Só lê o original por URL interna de leitura de curta validade e grava o derivado.
- Motor de OCR de código aberto com versão fixada, em ADR próprio ([02](02-arquitetura.md), seção 6). Idiomas: português, inglês e espanhol.
- Limites: 120 s por página, 200 páginas por arquivo, 3 tentativas. Esgotado, o estado vai para `ocr_falhou` e gera alerta à equipe do bucket.
- Imagem é reprocessada antes do OCR para remover metadados (ver seção 3.3).

**Saída:**

- Derivado `derivado-ocr` com texto por página e confiança por página, em JSON. Gravado em `storage_derivatives` (seção 4.3.1).
- Página com confiança abaixo de 60% é marcada `baixa_confianca`. A busca mostra o aviso no resultado, sem ocultar o texto.
- Derivado registra a versão do motor e a data. Mudança de versão não sobrescreve: um job reprocessa por tenant e cria novo derivado.

**Dado pessoal no texto extraído:**

- Em bucket de sensibilidade `pessoal` ou `sensivel` (RH, SMT, Financeiro, Documentos restritos), o texto OCR **não entra no índice de busca**. A busca encontra o arquivo pelo nome e pelos metadados, e o texto é lido só na visualização autorizada.
- Em bucket `comum`, o texto entra no índice com as mesmas regras de escopo da seção 6.3.
- Padrões de CPF, RG e número de cartão são removidos do texto antes da indexação, mesmo em bucket comum. Cartão reconhecido gera alerta ([20](20-pagamentos-seguranca.md), seção 3).

**Expurgo:** ao expurgar o arquivo, o derivado de OCR é removido do provedor e do índice, no mesmo prazo da seção 6.4.

**Testes específicos:**

- PDF digitalizado com CPF em bucket de RH: CPF ausente do índice.
- Imagem com cartão de crédito legível: número removido do texto e alerta gerado.
- Página acima de 120 s: `ocr_falhou` após 3 tentativas, sem derrubar a fila.
- Worker sem rede: tentativa de conexão externa falha, e o teste verifica esse bloqueio.

## 4. Banco de metadados

### 4.1 Correções ao modelo da v1

A v1 (`spec_object_storage_digital_assets.md`, seção 13) define seis tabelas. Problemas:

| ID | Problema | Correção |
|---|---|---|
| S-01 | Nenhuma tabela tem `tenant_id`. Só `entity_id` e `unit_id` em buckets. | `tenant_id CHAR(36) NOT NULL` em todas ([03](03-dominio-tenancy.md), seção 3). |
| S-02 | `DEFAULT (UUID())` gera UUIDv1, que não atende a regra de UUIDv4 ([03](03-dominio-tenancy.md), seção 2). | UUID gerado pela aplicação com `random_bytes(16)`. |
| S-03 | `checksum_sha256 NOT NULL` impede registrar upload pendente. | Nulo até a confirmação do provedor. |
| S-04 | `visibility ENUM('public','private')`. Público em bucket de dado pessoal é risco. | Só `private`. Visibilidade pública fica em bucket separado, aprovado por política. |
| S-05 | `antivirus_status` e `status` não modelam a quarentena e o pendente de upload em conjunto. | Estado único com estados da seção 4.2. |
| S-06 | `storage_access_logs` sem `tenant_id`, com `user_agent TEXT` completo. | `tenant_id` e `user_agent` truncado em 200. Retenção de 180 dias. |
| S-07 | `uploaded_by BIGINT` e `origin_entity_uuid` misturam chaves. | Usar `uuid` do usuário e do agregado de origem. |
| S-08 | `storage_key VARCHAR(500)` sem unicidade. | `UNIQUE (tenant_id, storage_key)`. |
| S-09 | `current_version` sem garantia de coerência com a tabela de versões. | Restrição por transação; `current_version` é a última linha de versão. |
| S-10 | Sem índice para deduplicação nem para busca por origem. | Índice `(tenant_id, checksum_sha256)` e `(tenant_id, origin_entity_type, origin_entity_uuid)`. |

### 4.2 Estados do arquivo

| Estado | Significado | Download |
|---|---|---|
| `pendente_upload` | URL emitida; bytes não confirmados | Não |
| `verificando` | Bytes recebidos; checagens em andamento | Não |
| `disponivel` | Validado | Sim, com permissão |
| `quarentena` | Falhou em validação ou antivírus | Não. Só equipe de segurança. |
| `lixeira` | Excluído logicamente | Não |
| `expurgado` | Bytes removidos; metadado mínimo mantido | Não |

Transições fora da tabela são `409`.

### 4.3 DDL proposto

```sql
CREATE TABLE storage_buckets (
  id                 BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid               CHAR(36)     NOT NULL,
  tenant_id          CHAR(36)     NOT NULL,
  entity_id          CHAR(36)     NOT NULL,
  unit_id            CHAR(36)     NULL,
  code               VARCHAR(60)  NOT NULL,
  source_module      VARCHAR(60)  NOT NULL,
  sensitivity        ENUM('comum','pessoal','sensivel') NOT NULL DEFAULT 'pessoal',
  quota_bytes        BIGINT UNSIGNED NOT NULL,
  used_bytes         BIGINT UNSIGNED NOT NULL DEFAULT 0,
  max_file_bytes     BIGINT UNSIGNED NOT NULL,
  allowed_mime       JSON         NOT NULL,
  retention_policy_id BIGINT UNSIGNED NULL,
  requires_scan      TINYINT(1)   NOT NULL DEFAULT 1,
  requires_envelope  TINYINT(1)   NOT NULL DEFAULT 0,
  status             ENUM('ativo','suspenso') NOT NULL DEFAULT 'ativo',
  created_at         DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  UNIQUE KEY uk_bucket_uuid (uuid),
  UNIQUE KEY uk_bucket_code (tenant_id, code),
  CHECK (used_bytes <= quota_bytes)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE storage_files (
  id                 BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid               CHAR(36)     NOT NULL,
  tenant_id          CHAR(36)     NOT NULL,
  bucket_id          BIGINT UNSIGNED NOT NULL,
  display_name       VARCHAR(255) NOT NULL,
  declared_mime      VARCHAR(100) NOT NULL,
  detected_mime      VARCHAR(100) NULL,
  size_bytes         BIGINT UNSIGNED NOT NULL,
  checksum_sha256    CHAR(64)     NULL,
  current_version    INT UNSIGNED NOT NULL DEFAULT 1,
  origin_type        VARCHAR(60)  NULL,
  origin_uuid        CHAR(36)     NULL,
  status             ENUM('pendente_upload','verificando','disponivel','quarentena','lixeira','expurgado') NOT NULL,
  scan_status        ENUM('pendente','limpo','infectado','ignorado') NOT NULL DEFAULT 'pendente',
  legal_hold         TINYINT(1)   NOT NULL DEFAULT 0,
  uploaded_by        CHAR(36)     NOT NULL,
  trashed_at         DATETIME(6)  NULL,
  purge_at           DATETIME(6)  NULL,
  created_at         DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  UNIQUE KEY uk_file_uuid (uuid),
  INDEX idx_tenant_bucket (tenant_id, bucket_id, status),
  INDEX idx_tenant_origin (tenant_id, origin_type, origin_uuid),
  INDEX idx_tenant_checksum (tenant_id, checksum_sha256),
  INDEX idx_purge (status, purge_at),
  FOREIGN KEY (bucket_id) REFERENCES storage_buckets(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE storage_object_versions (
  id                 BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tenant_id          CHAR(36)     NOT NULL,
  file_id            BIGINT UNSIGNED NOT NULL,
  version_number     INT UNSIGNED NOT NULL,
  storage_key        VARCHAR(500) NOT NULL,
  size_bytes         BIGINT UNSIGNED NOT NULL,
  checksum_sha256    CHAR(64)     NOT NULL,
  created_by         CHAR(36)     NOT NULL,
  created_at         DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  UNIQUE KEY uk_version (file_id, version_number),
  UNIQUE KEY uk_storage_key (tenant_id, storage_key),
  FOREIGN KEY (file_id) REFERENCES storage_files(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE storage_scan_results (
  id                 BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tenant_id          CHAR(36)     NOT NULL,
  file_id            BIGINT UNSIGNED NOT NULL,
  version_number     INT UNSIGNED NOT NULL,
  engine             VARCHAR(60)  NOT NULL,
  engine_version     VARCHAR(40)  NOT NULL,
  result             ENUM('limpo','infectado','erro') NOT NULL,
  detail             VARCHAR(255) NULL,
  scanned_at         DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  INDEX idx_file (tenant_id, file_id),
  FOREIGN KEY (file_id) REFERENCES storage_files(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE storage_access_events (
  id                 BIGINT UNSIGNED AUTO_INCREMENT,
  tenant_id          CHAR(36)     NOT NULL,
  file_id            BIGINT UNSIGNED NOT NULL,
  actor_uuid         CHAR(36)     NULL,
  action             ENUM('visualizar','baixar','enviar','excluir','restaurar','expurgar','versionar') NOT NULL,
  ip_address         VARCHAR(45)  NULL,
  user_agent         VARCHAR(200) NULL,
  occurred_at        DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id, occurred_at),
  INDEX idx_tenant_file (tenant_id, file_id, occurred_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
PARTITION BY RANGE COLUMNS(occurred_at) (
  PARTITION p_init VALUES LESS THAN ('2027-01-01')
);

CREATE TABLE storage_retention_policies (
  id                 BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid               CHAR(36)     NOT NULL,
  tenant_id          CHAR(36)     NOT NULL,
  name               VARCHAR(120) NOT NULL,
  retention_days     INT UNSIGNED NOT NULL,
  action_on_expiry   ENUM('expurgar','anonimizar','arquivar') NOT NULL,
  legal_basis        VARCHAR(255) NULL,
  UNIQUE KEY uk_policy_uuid (uuid),
  UNIQUE KEY uk_policy_name (tenant_id, name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Notas:

- `storage_access_events` é particionada por data. Partições antigas são removidas conforme a retenção de 180 dias. Partição nova é criada por job mensal.
- `storage_files.checksum_sha256` é nulo até a confirmação. Restrição de unicidade por checksum não é imposta, porque o mesmo arquivo pode existir em dois tenants ou dois registros legítimos.
- `CHECK` em `used_bytes` é verificado pelo banco em versões que suportam; a aplicação mantém a mesma regra.
- Os campos `origin_type` e `origin_uuid` ligam o arquivo ao agregado de origem ([14](14-integracao-modulos.md)), sem chave estrangeira entre módulos.

### 4.3.1 Derivados

```sql
CREATE TABLE storage_derivatives (
  id                 BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid               CHAR(36)     NOT NULL,
  tenant_id          CHAR(36)     NOT NULL,
  file_id            BIGINT UNSIGNED NOT NULL,
  version_number     INT UNSIGNED NOT NULL,
  kind               ENUM('miniatura','ocr','visualizacao') NOT NULL,
  engine             VARCHAR(60)  NULL,
  engine_version     VARCHAR(40)  NULL,
  storage_key        VARCHAR(500) NOT NULL,
  status             ENUM('gerado','ocr_falhou','baixa_confianca','expurgado') NOT NULL,
  created_at         DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  UNIQUE KEY uk_derivative_uuid (uuid),
  UNIQUE KEY uk_derivative_key (tenant_id, storage_key),
  INDEX idx_file_kind (tenant_id, file_id, kind),
  FOREIGN KEY (file_id) REFERENCES storage_files(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 4.4 Eventos de armazenamento

| Evento | Quando |
|---|---|
| `storage.file.uploaded` | Bytes confirmados |
| `storage.file.scanned` | Verificação concluída (limpo ou quarentena) |
| `storage.file.accessed` | Download ou visualização |
| `storage.file.trashed` | Exclusão lógica |
| `storage.file.purged` | Expurgo concluído |
| `storage.legal-hold.applied` | Bloqueio legal aplicado |

Consumidores: busca (seção 6), auditoria ([18](18-regras-modulos-2.md), seção 4.2), cota e notificações.

---

## 5. Métricas e alertas de armazenamento

| Alerta | Condição |
|---|---|
| Quarentena | Qualquer arquivo de dado sensível em quarentena |
| Verificação lenta | Arquivo em `verificando` por mais de 15 min |
| Cota | Uso acima de 80% |
| Upload órfão | `pendente_upload` acima de 24 h |
| Expurgo falho | Falha de remoção no provedor, com tentativa seguinte |
| Acesso anômalo | Volume de download de um usuário acima do padrão do tenant |

---

## 6. Busca full-text

### 6.1 O que é indexado

| Fonte | Campos | Permissão de leitura da fonte |
|---|---|---|
| Registros dos módulos | Nome, código, título, descrição | Herda a permissão do registro |
| Arquivos | Nome de exibição, tipo e texto extraído por OCR (seção 3.10), exceto em bucket sensível | Herda a permissão do arquivo |
| Documentos e anexos | Texto de PDF com camada de texto ou, na falta dela, texto de OCR | Herda a permissão do documento |

Não são indexados: CPF, RG, dado de saúde, valor salarial, número de cartão, token, senha, segredo. CPF é pesquisável só pelo fluxo controlado da seção 6.8, com configuração LGPD, permissão específica e auditoria. Os demais dados desta lista não aparecem em busca. Texto livre nunca é pesquisado por CPF.

### 6.2 Motor

**[Decidida D-13]** MySQL FULLTEXT inicialmente, com interface isolada para migrar depois.

| Opção | Mecanismo | Vantagem | Condição de falha |
|---|---|---|---|
| (a) Índice FULLTEXT no MySQL (**proposta inicial**) | Índice por tabela de busca, com stemming limitado | Sem novo componente. Tenant e permissão filtram na mesma consulta. | Relevância pobre para português com acentuação e flexão. Escala limitada para texto extraído de muitos documentos. |
| (b) Motor de busca dedicado (OpenSearch ou equivalente) | Índice por tenant ou com filtro obrigatório de tenant | Relevância, sinônimos, stemming de português, realce | Mais um componente para operar, backup e atualizar. Vazamento de índice expõe texto. |

Proposta: começar com (a) para nomes e códigos, e migrar para (b) quando o volume de texto extraído passar do limite que a medição indicar. A camada de busca é isolada atrás de uma interface, para que a troca não altere os módulos.

### 6.3 Isolamento e permissão

- **Índice por tenant** se o motor for (b). Quando o índice é compartilhado, filtro por `tenant_id` é obrigatório e verificado em teste de regressão.
- Cada documento indexado guarda `acl_scope`: módulo, unidade e papel mínimo que pode ler. A consulta filtra por esse escopo.
- O resultado é checado de novo na leitura do registro. Se a permissão mudou depois da indexação, o item não é exibido.
- Contagem de resultados por escopo não revela existência de registro sem permissão. Resultado vazio e resultado negado têm a mesma resposta.

### 6.4 Pipeline de indexação

1. Evento de mudança chega pela fila ([14](14-integracao-modulos.md), seção 5), com `event_id` usado como chave de idempotência.
2. Indexador atualiza o documento de busca. Versão do registro evita sobrescrever mudança mais nova.
3. Arquivo só é indexado depois de `disponivel`. Quarentena e infectado nunca são indexados.
4. Exclusão ou expurgo remove o documento do índice em até 24 h. Expurgo por obrigação legal remove o texto e mantém só o identificador.
5. Reindexação completa por tenant é possível e registrada, sem derrubar a busca.

### 6.5 Consulta

| Regra | Valor |
|---|---|
| Tamanho máximo do termo | 200 caracteres |
| Caracteres | Termo é escapado. Sintaxe de operador do motor é desativada para usuário comum. |
| Resultados por página | 20; máximo 100 |
| Realce | Trecho escapado antes de ser exibido. Nenhum HTML do documento é renderizado. |
| Autocompletar | Só sobre nomes e códigos já autorizados. Limite de 10 sugestões. |
| Limite de taxa | 30 buscas por minuto por usuário; 300 por tenant. |
| Acentos | Busca ignora acentos e maiúsculas. |

### 6.6 Privacidade e logs de busca

- O termo buscado pode conter dado pessoal. O log guarda `tenant_id`, `user_uuid`, hash do termo, quantidade de resultados e tempo. O termo em texto não é gravado.
- Retenção do log de busca: 30 dias.
- Quando um titular pede eliminação ([07](07-privacidade-lgpd.md)), o documento sai do índice no mesmo prazo da seção 6.4.

### 6.7 Desempenho

| Medida | Meta inicial |
|---|---|
| Busca por nome e código, p95 | até 300 ms |
| Busca em texto extraído, p95 | até 800 ms |
| Atraso de indexação, p95 | até 60 s |
| Reindexação de 100 mil documentos | medida e registrada em homologação |

---

### 6.8 Busca por CPF: LGPD e auditoria

**Status: aprovada pelo autor em 02/11/2026.** Retenção da auditoria: 24 horas (conflito com o relatório ao titular, a confirmar). Base legal por finalidade: matriz em [07](07-privacidade-lgpd.md), seção 3, pendente de parecer jurídico.

A busca por CPF é um recurso de alto risco: permite localizar uma pessoa a partir de um dado pessoal. Por isso, só existe com configuração explícita, controle de finalidade, permissão própria e registro de cada consulta.

**Ativação por tenant (desligada por padrão):**

| Requisito | Detalhe |
|---|---|
| Finalidade | Cada tenant escolhe, em lista fechada, a finalidade da busca: atendimento, matrícula, cobrança, RH ou segurança do trabalho. Sem finalidade, o recurso não liga. |
| Base legal | Registrada por finalidade ([07](07-privacidade-lgpd.md), seção 3). **(jurídico)** confirmar a base por finalidade. |
| Relatório de impacto | Obrigatório antes de ativar. Aprovação do encarregado (DPO) registrada. |
| Módulos habilitados | Cada módulo que usa a busca deve estar na lista. Por padrão, nenhum. |
| Aceite do administrador | Registrado com nome, data e versão do texto de finalidade. |

**Permissão e MFA:**

- Permissão `busca.cpf.consultar`, separada de `busca.geral`.
- MFA recente (até 5 min) antes da primeira consulta de CPF em cada sessão. Canais de mensagem (seção 5 de [06](06-identidade-acesso.md)) não bastam para ativar a permissão.
- Revogar a permissão encerra as consultas em andamento daquele usuário.

**Como a consulta funciona:**

- Entrada: CPF completo com 11 dígitos e dígito verificador válido ([15](15-validacoes.md), seção 2). Busca parcial, por prefixo ou por sufixo é recusada. Autocompletar não existe para CPF.
- Comparação feita por hash HMAC com pepper, sobre o CPF normalizado. Nenhum texto de CPF é gravado no índice.
- Resposta mínima: nome, unidade, situação e CPF mascarado (`***.456.789-**`). Não retorna dado de saúde, salário, endereço ou documento.
- CPF completo só aparece em tela de detalhe autorizada, com motivo registrado, e não aparece em lista, exportação, notificação ou log.
- Resultado vazio e CPF inexistente têm a mesma resposta, sem diferença de tempo perceptível, para não revelar cadastro.

**Limites contra enumeração:**

| Controle | Valor inicial |
|---|---|
| Consultas de CPF por usuário | 20 por hora |
| CPFs distintos por usuário | 50 por dia; acima disso, bloqueio temporário e alerta |
| Consultas de CPF por tenant | 500 por hora; acima disso, alerta ao DPO |
| Consultas sem resultado seguidas | 10 seguidas: bloqueio temporário e alerta |

**Auditoria obrigatória de cada consulta:**

| Campo | Conteúdo |
|---|---|
| Ator | UUID do usuário, papel e unidade |
| Quando | Data e hora em UTC |
| Finalidade | Finalidade declarada no momento da consulta |
| Módulo | Módulo de origem |
| CPF | Apenas o hash HMAC, nunca o CPF em texto |
| Resultado | Quantidade de resultados: 0 ou 1 |
| Motivo | Texto obrigatório quando a consulta leva ao detalhe completo |
| Origem | IP, user-agent truncado, identificador de sessão |

Regras da auditoria:

- O registro é gravado antes da resposta. Falha na gravação recusa a consulta.
- A auditoria é imutável ([18](18-regras-modulos-2.md), seção 4.2).
- O titular pode solicitar relatório de quem consultou o CPF dele. O relatório lista ator, finalidade, data e módulo. Não lista motivo livre nem dado de outro titular.
- Prazo de retenção da auditoria de consulta por CPF: **24 horas**, decisão do autor em 02/11/2026. Após o prazo, o registro é expurgado por job, com registro do próprio expurgo.
- **Conflito a confirmar pelo autor:** com 24 horas, o relatório ao titular (acima) cobre só consultas recentes, e a investigação de incidente também fica limitada a esse prazo. O jurídico deve confirmar se o prazo atende às obrigações de registro de tratamento (LGPD, art. 37) e de resposta ao titular. Se não atender, o prazo precisa ser ampliado para o mínimo exigido.

**Alertas:**

- Consulta fora do horário de trabalho do usuário, conforme padrão do tenant.
- Consulta de CPF por usuário sem vínculo com o módulo de origem.
- Padrão de varredura (muitos CPFs distintos em pouco tempo).
- Consulta de CPF de pessoa com cadastro sensível (menor de idade, ou dado de saúde ocupacional) fora da finalidade.

**Testes específicos:**

- Tenant sem finalidade declarada: a busca de CPF não aparece e a rota responde como inexistente.
- Usuário sem `busca.cpf.consultar`: recusado, sem vazar a existência do CPF.
- Consulta com CPF parcial: recusada.
- Consulta sem MFA recente: recusada.
- Vigésima primeira consulta em uma hora: bloqueada.
- Log de busca e log de aplicação não contêm CPF em texto (varredura).
- Falha na gravação de auditoria: consulta recusada.
- Relatório ao titular não inclui motivo livre de outro registro.

## 7. Segurança específica

| Ameaça | Controle |
|---|---|
| Upload de arquivo malicioso | Verificação de tipo real, antivírus, quarentena, nenhuma execução de conteúdo. |
| Download não autorizado por URL vazada | URL de curta validade, amarrada ao usuário, sem acesso público. |
| Enumeração de arquivos por ID | UUID aleatório; permissão checada em toda leitura. |
| Path traversal no nome | Nome é só metadado; chave é gerada no servidor. |
| XSS via texto indexado | Realce escapado; resposta JSON sem HTML. |
| Injeção na busca | Termo escapado; operadores desativados. |
| Vazamento de texto por índice | Acesso ao índice só pelo serviço de busca; dado sensível excluído (seção 6.1). |
| Documento indexado após exclusão | Remoção do índice pelo evento de expurgo, com verificação em job diário. |

---

## 8. Testes obrigatórios

- Upload com extensão `.pdf` e conteúdo `.exe`: quarentena, sem URL de download.
- Upload com checksum divergente: recusado pelo provedor.
- URL de download emitida para um tenant e usada com token de outro: recusada.
- Arquivo de tenant A não aparece na busca de tenant B, com termo exato do arquivo.
- Permissão retirada depois da indexação: item não é exibido.
- Termo com `*`, `"`, `OR`, `<script>`: tratado como texto, sem erro nem execução.
- Expurgo remove o arquivo do provedor e do índice dentro do prazo.
- Bloqueio legal impede expurgo na data prevista.
- CPF não aparece no índice de texto livre.
- Versão antiga restaurada cria nova versão, sem reapontar a chave antiga.

---

## 9. Decisões pendentes

| # | Decisão | Proposta | Alternativa e condição de falha |
|---|---|---|---|
| D-13 | Motor de busca | **Decidida:** MySQL FULLTEXT inicialmente, interface isolada para migrar depois | — |
| D-14 | Layout de buckets | **Decidida:** um bucket por ambiente, com prefixo por unidade | — |
| D-15 | OCR de documentos digitalizados | **Decidida:** OCR entra nesta versão, com as regras da seção 3.10 | — |

---

## 10. Critérios de aceite

- [ ] Todas as tabelas de metadados têm `tenant_id NOT NULL` e UUID gerado pela aplicação.
- [ ] Nenhum arquivo em `quarentena` ou `pendente_upload` é baixável.
- [ ] Nenhum arquivo sensível é indexado por texto sem permissão de escopo.
- [ ] Expurgo e bloqueio legal testados.
- [ ] Testes da seção 8 passando em CI.
- [ ] D-13 a D-15 decididas e registradas.
