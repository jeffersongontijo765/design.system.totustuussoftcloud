# 10 — Implantação e Operação

> Parte do [SDD v2](00-README.md). Segurança de cadeia de suprimentos em [05](05-seguranca.md).

---

## 1. Requisitos de runtime

| Componente | Requisito |
|---|---|
| PHP | 8.2 ou superior, com suporte a sodium, PDO MySQL, mbstring, openssl, fileinfo, intl, json, curl |
| Banco | MySQL 8.0 ou MariaDB 10.6 ou superior, InnoDB, `utf8mb4` |
| Cache e sessão | Redis recomendado; banco como alternativa |
| Armazenamento | Objeto compatível com S3 ou volume dedicado fora do diretório público |
| Processos | Workers via supervisor ou equivalente; `pcntl` para jobs |
| Web | Apache ou Nginx com HTTPS obrigatório |

## 2. Ambientes

| Ambiente | `APP_ENV` | Dados | Acesso |
|---|---|---|---|
| Local | `local` | Sintéticos | Desenvolvedor |
| Homologação | `staging` | Sintéticos ou anonimizados | Equipe; dados reais proibidos |
| Produção | `production` | Reais | Operação, com registro |

- `APP_DEBUG=false` e `display_errors=0` em homologação e produção.
- `APP_URL` canônico, sem valor padrão de `localhost` em produção (a aplicação recusa iniciar se a URL for local).
- HSTS habilitado somente em ambientes com HTTPS validado.
- CORS com lista explícita de origens por ambiente.

## 3. Segredos

- Produção: biblioteca própria `TotusTuus\Vault` (ADR-05, D-02), com chave-mestra fora do host da aplicação. `FileVault` proibido em produção.
- Segredos carregados na inicialização; nunca gravados em log, em erro ou em cache de página.
- `.env` nunca versionado. `.env.example` sem valores reais.
- Rotação documentada por segredo: chave de cifragem, pepper, chave de assinatura JWT, segredo de webhook, credencial de banco.
- Remover variáveis não usadas (por exemplo `JWT_SECRET` se o caminho HS256 for removido).
- Revisão semestral do inventário de segredos.

## 4. Pipeline

Ordem obrigatória:

1. **Verificação de segredos** (`gitleaks`) — bloqueia.
2. **Lint** de PHP (`php -l` em todos os arquivos) e análise estática (PHPStan ou Psalm no nível acordado).
3. **Dependências** (`composer audit`, `npm audit`) — bloqueia em alto ou crítico.
4. **Testes** unitários e de integração, incluindo isolamento de tenant e autorização.
5. **Build** de artefato com lockfiles e geração de SBOM (CycloneDX).
6. **Verificação do artefato:** nenhum diretório da lista de exclusão (`scratch/`, `workspace/`, `uploads/`, `node_modules/`, `storage/`, `.env*`, `*.rar`) presente.
7. **Migrações** versionadas, aplicadas antes do deploy, com plano de reversão ou migração compatível com a versão anterior.
8. **Deploy** em homologação, testes de fumaça, depois produção.
9. **Testes de fumaça pós-deploy:** `/health` (sem dados sensíveis), login de conta de teste em homologação, leitura de tela principal.

Ferramentas de deploy são fixadas por versão. Comandos `npx`, `bunx` ou instaladores remotos não aparecem no pipeline.

## 5. Migrações de banco por tenant

- Estrutura (D-16): banco master (`totustuus.matriz.bd`, com plataforma e registro de bancos) + um banco por unidade (entidade + unidade). Ver [03](03-dominio-tenancy.md), seção 1.1.
- Migração roda em ordem por banco de unidade, com registro de versão por banco (`schema_version` no registro do master) e retomada após falha. O banco fica em `migrando` durante a execução.
- Migração que afeta todas as unidades é aplicada em lote, com janela, e reporta falhas por banco. Falha em um banco não impede os demais.
- Migração que apaga coluna ou tabela segue duas etapas: primeiro deixa de usar, depois remove na versão seguinte.

## 6. Backup e recuperação

| Política | Valor de referência (v1) | Observação |
|---|---|---|
| Backup completo | Diário, 7 dias | Ajustar à política contratual |
| Semanal | 4 semanas | |
| Mensal | 12 meses | Dados pessoais: retenção limitada (ver [07](07-privacidade-lgpd.md)) |
| Teste de restauração | Mensal, com registro | Obrigatório antes do go-live |
| RPO / RTO | Definir por contrato | Sem valor fixado neste SDD |

Backup criptografado. Chave de backup separada da chave de dados e guardada no cofre.

## 7. Observabilidade

- Logs estruturados em JSON com `request_id`, `tenant_id` (quando houver), nível e canal. Sem PII.
- Métricas: latência por rota (p50, p95, p99), taxa de erro 5xx, filas, uso de conexões de banco.
- Alertas: erro 5xx acima de 1% em 5 min; fila parada 10 min; certificado TLS com menos de 14 dias; eventos de segurança (força bruta, escalonamento, exportação em massa).
- Painel de auditoria é consulta. Não é fonte de métrica.
- Retenção de logs de aplicação: 90 dias. Logs de auditoria: prazo a definir pelo DPO e pelo jurídico (a v2 não fixa valor; ver [07](07-privacidade-lgpd.md)). Até a definição, nenhum expurgo de auditoria é executado.

## 8. Operação de filas

- Jobs idempotentes com chave de evento.
- Tentativas com atraso exponencial e limite; falha definitiva vai para fila de mortos com alerta.
- Worker não executa código de tenant sem contexto de tenant definido.

## 9. Checklist de go-live

- [ ] `APP_DEBUG=false`, `display_errors=0`.
- [ ] HTTPS com certificado válido e HSTS.
- [ ] Cofre de segredos de produção ativo (D-02); `FileVault` desligado.
- [ ] Limites de taxa configurados por ambiente.
- [ ] Restauração de backup testada e registrada.
- [ ] SBOM gerado.
- [ ] Testes de fumaça pós-deploy verdes.
- [ ] `gitleaks` limpo.
- [ ] DAST em homologação sem achado médio ou superior não tratado.
- [ ] Nenhum arquivo de desenvolvimento no artefato (ver seção 4, passo 6).
- [ ] Runbook de incidente publicado e contatos atualizados.

---

## 10. Operação de mídia (aulas online e reuniões)

Decidido em 03/11/2026: mídia própria, com as melhores tecnologias disponíveis ([40](40-aulas-online-por-portal.md), seção 8). Esta seção define a operação. A escolha de cada componente open source é feita em homologação, com critério de maturidade, segurança e desempenho, e registrada nesta seção.

### 10.1 Componentes

| Componente | Função | Escala |
|---|---|---|
| Sinalização | Entrada na sala, controle de participantes, eventos de sessão. Conexão segura | Horizontal, sem estado |
| SFU (unidade de encaminhamento de mídia) | Recebe o fluxo de cada participante e entrega a quem assiste. Não guarda nada | Por região e por faixa de salas |
| Gravador | Consome o fluxo do SFU e grava em fragmentos (seção 10.2) | Um processo por sessão gravada, com trava de posse |
| Armazenamento de fragmentos | Objetos cifrados no armazenamento da seção 21, com o prefixo de unidade da [21](21-busca-e-armazenamento.md), seção 3.2 | Conforme volume |
| Índice de fragmentos | Tabelas da seção 10.3. Liga sessão, trilha, sequência e objeto | Banco da unidade |
| Verificador de fragmento | Confere checksum e tamanho após o fechamento de cada fragmento | Worker da fila |
| Serviço de retenção | Expurgo e bloqueio legal, na mesma regra de [21](21-busca-e-armazenamento.md), seção 3.6 | Job diário |

### 10.2 Fragmentação da gravação

- Cada trilha (áudio, vídeo e tela) é gravada em **fragmentos de tamanho fixo por tempo**. Padrão proposto: **60 segundos**, configurável. O valor final é medido em homologação (LIV-13).
- Cada fragmento tem número de sequência único por sessão e trilha. Nunca é sobrescrito. Se o gravador reiniciar, ele abre o próximo número.
- Cada fragmento é cifrado com AES-256-GCM, com nonce único, e a chave da sessão fica no cofre ([05](05-seguranca.md)). O índice guarda só a referência da chave, nunca o valor.
- Ao fechar o fragmento, o gravador calcula SHA-256 e tamanho. O verificador confere e muda o estado para `verificado`.
- Fragmento sem fechamento correto vira `corrompido` e não entra na reprodução. O sistema registra o intervalo perdido, sem preencher com silêncio.

Chave do objeto no armazenamento:

```
{unidade_uuid}/midia/{sessao_uuid}/{trilha}/{sequencia:08d}.seg
```

### 10.3 Mapeamento e reprodução

DDL proposto (MySQL 8 ou MariaDB 10.6, `utf8mb4`, horários em UTC):

```sql
CREATE TABLE sessao_midia (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  sessao_uuid     CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  estado          ENUM('gravando','pausada','encerrada','verificada','expurgada') NOT NULL,
  chave_ref       VARCHAR(120) NOT NULL,
  iniciada_em     DATETIME(3) NOT NULL,
  encerrada_em    DATETIME(3) NULL,
  created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX ix_midia_unidade (unidade_uuid, estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sessao_fragmento (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  midia_id        BIGINT UNSIGNED NOT NULL,
  trilha          ENUM('audio','video','tela') NOT NULL,
  sequencia       INT UNSIGNED NOT NULL,
  inicio_utc      DATETIME(3) NOT NULL,
  duracao_ms      INT UNSIGNED NOT NULL,
  chave_objeto    VARCHAR(500) NOT NULL,
  tamanho_bytes   BIGINT UNSIGNED NOT NULL,
  sha256          CHAR(64) NOT NULL,
  estado          ENUM('gravando','fechado','verificado','corrompido','expurgado') NOT NULL,
  UNIQUE KEY ux_fragmento_sequencia (midia_id, trilha, sequencia),
  CONSTRAINT fk_fragmento_midia FOREIGN KEY (midia_id) REFERENCES sessao_midia (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Reprodução:** o sistema monta um manifesto ordenado por trilha e sequência, somente com fragmentos `verificado`. O manifesto é emitido por URL assinada, com validade curta, e vinculada ao usuário e à sessão. Lacuna de tempo entre dois fragmentos aparece como intervalo marcado, nunca emendada.

**Consolidação:** um job opcional junta os fragmentos em um arquivo único para download, depois de verificados. O arquivo consolidado não substitui os fragmentos. O expurgo atinge os dois.

### 10.4 Falhas

| Falha | Comportamento |
|---|---|
| SFU indisponível | Sala não abre. Alerta imediato. Aula reagendável pela gestão |
| Gravador cai no meio | Fragmento aberto vira `corrompido`. Nova sequência abre ao retomar. Sessão segue |
| Armazenamento indisponível | Gravador guarda o fragmento em buffer local cifrado, por tempo limitado. Se o buffer estourar, a gravação é marcada como interrompida. A sala segue sem gravação |
| Verificador acusa checksum errado | Fragmento vai para `corrompido`. Alerta para operação |
| Chave não encontrada no cofre | Fragmento não é reproduzido. Alerta de segurança. Não há fallback de chave |

### 10.5 Capacidade

Fórmulas de planejamento, com valores a medir em homologação (LIV-13):

- Banda de saída do SFU ≈ número de participantes que recebem × bitrate médio por participante.
- Armazenamento por hora de gravação ≈ bitrate gravado × 3600 ÷ 8, em bytes, por trilha.
- Número de salas simultâneas por nó é medido em teste de carga antes do go-live, não estimado.

### 10.6 Monitoramento

| Métrica | Alerta |
|---|---|
| Salas ativas e participantes por nó | Acima de 80% da capacidade medida |
| Perda de pacote, jitter e latência por sala | Perda acima de limite a definir em homologação, por 2 min |
| Fila de fragmentos aguardando verificação | Fila parada por 10 min |
| Fragmentos `corrompido` por dia | Qualquer ocorrência |
| Espaço livre do armazenamento de mídia | Abaixo de 20% |
| Chaves não encontradas | Qualquer ocorrência, com alerta de segurança |

Logs de mídia não contêm conteúdo, nomes de participantes nem trecho de áudio ou texto. Identificadores de sessão e de nó são suficientes.

### 10.7 Isolamento e segurança

- Token de entrada na sala é assinado e tem o `sessao_uuid` e a unidade. O SFU recusa token de outra sessão ou de outra unidade.
- Gravação e fragmento nunca saem da região definida para a unidade. A localização dos dados precisa de parecer **(jurídico)**.
- Acesso operacional ao conteúdo de sessão é proibido. O suporte vê estado e métricas, não mídia. Exceção só com ordem formal e registro em auditoria ([29](29-auditoria.md)).

### 10.8 Retenção

- O expurgo de fragmento segue o prazo de gravação de [40](40-aulas-online-por-portal.md), seção 5 (padrão proposto de 30 dias, a confirmar **(jurídico)**).
- Ao expurgar, o sistema remove os objetos, marca os fragmentos `expurgado` e mantém só o registro mínimo: sessão, trilha, sequência, data, motivo.
- Bloqueio legal impede o expurgo, nos termos de [21](21-busca-e-armazenamento.md), seção 3.6.

### 10.9 Critérios de aceite

- [ ] Fragmento nunca é sobrescrito (teste de concorrência em reinício do gravador).
- [ ] Fragmento com checksum errado não aparece no manifesto (teste).
- [ ] Lacuna de tempo aparece como intervalo, sem silêncio emendado (teste).
- [ ] Token de uma sessão não abre o manifesto de outra (teste de isolamento).
- [ ] Expurgo remove objetos e fragmentos, e mantém só o registro mínimo (teste).
- [ ] Valores de LIV-13 medidos em homologação e registrados aqui.
