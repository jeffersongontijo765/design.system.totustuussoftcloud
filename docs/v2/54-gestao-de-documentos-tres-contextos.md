# 54 — Gestão de Documentos: Três Contextos e Serviços Comuns

> Parte do [SDD v2](00-README.md). Substitui a visão de "gestão de documentos" como bloco único que aparecia em [31](31-matriz-portais-modulos.md), seção 3.1. Emissão de documentos pela secretaria, detalhada em [48](48-gerador-de-documentos-por-portal.md). Armazenamento e retenção em [21](21-busca-e-armazenamento.md). Protocolo e atendimento em [32](32-atendimento-privacidade-por-portal.md). Assinatura de contratos em [33](33-contratos-por-portal.md), seção 5. Auditoria em [29](29-auditoria.md). Pacotes jurídicos em [50](50-pacote-juridico-e-norma.md) e [53](53-pacote-documentos-e-contratos.md).
> **Status:** decisão de arquitetura, criada em 03/11/2026. Não centralizar: cada contexto tem dono, regras e portal próprios. O que é comum fica em serviços, sem compartilhar tabelas de negócio.

---

## 1. Os três contextos

| Contexto | O que é | Quem origina | Quem cuida | Exemplos |
|---|---|---|---|---|
| **A. Documentos recebidos** | Arquivos enviados a instituição para análise e validação | Responsáveis, alunos, candidatos, fornecedores | Secretaria, RH, compras | Certidão de nascimento, RG do responsável, histórico de escola anterior, alvará do fornecedor |
| **B. Documentos administrativos** | Documentos internos de gestão, com tramitação e aprovação | Equipe da instituição | Gestão e administração | Ata de reunião de diretoria, ofício, circular, processo administrativo, política interna |
| **C. Documentos emitidos** | Documentos gerados pela instituição a partir de modelo, para uma pessoa ou uma organização | Secretaria | Secretaria | Declaração, histórico, boletim, certidão, contrato, termo |

Os três contextos não se misturam. Um documento pertence a um contexto, e o contexto define regras, estados, portal de acesso e prazo de guarda.

---

## 2. Contexto A: documentos recebidos

### 2.1 O que o contexto faz

- Recebe arquivo enviado pelo portal (responsável, aluno, candidato ou fornecedor).
- Confere o arquivo: formato, tamanho, legibilidade e tipo declarado.
- Valida o conteúdo por pessoa habilitada. A validação registra quem validou, quando e o resultado.
- Vincula o arquivo a um cadastro ou a um processo: matrícula, cadastro de fornecedor, candidatura.
- Controla vencimento, quando o documento tem validade (ex.: alvará, seguro, certidão).

### 2.2 Estados

`enviado` → `em_analise` → `aprovado` ou `recusado` ou `pendente_correcao`.

- `recusado` exige motivo. O remetente recebe o motivo e pode reenviar.
- `pendente_correcao` tem prazo. Vencido o prazo, o processo vinculado é tratado conforme a regra do processo (ex.: matrícula condicional, em [46](46-matricula-e-rematricula-por-portal.md)).
- `vencido` é calculado por data ([18](18-regras-modulos-2.md), T-04), não gravado.

### 2.3 Regras

- Documento de menor é enviado pelo responsável com vínculo ativo.
- Imagem de documento de identidade é guardada cifrada, com acesso restrito à validação. Número completo aparece mascarado nas telas ([07](07-privacidade-lgpd.md)).
- Documento recebido não é emitido. Nunca gera código de validação pública.
- Validação não é automática por padrão. Automação de leitura (OCR) só sugere, e a pessoa confirma ([21](21-busca-e-armazenamento.md), seção 3.10).

### 2.4 Retenção

Prazo por tipo de documento, vinculado ao processo que originou o envio. Documento de matrícula segue o prazo de guarda escolar **(jurídico, [50](50-pacote-juridico-e-norma.md), J-05 e N-10)**. Documento de fornecedor segue o prazo do contrato.

---

## 3. Contexto B: documentos administrativos

### 3.1 O que o contexto faz

- Cria documento interno com modelo ou em formato livre.
- Tramita: envia para análise, aprovação e assinatura de quem deve aprovar.
- Mantém versões. Versão aprovada não muda.
- Arquiva ao fim da tramitação, com prazo de guarda.

### 3.2 Estados

`rascunho` → `em_tramitacao` → `aprovado` → `arquivado`, com `reprovado` como saída de `em_tramitacao`.

- Quem cria não aprova o próprio documento. Regra verificada no banco, como em [48](48-gerador-de-documentos-por-portal.md), seção 12.
- Documento aprovado pode ser assinado. A assinatura usa o serviço comum da seção 5.

### 3.3 Regras

- Documento administrativo não é visível a alunos e responsáveis, salvo quando a gestão publica um comunicado, que é contexto C ou um comunicado específico ([53](53-pacote-documentos-e-contratos.md), DC-26).
- Ata de conselho ou de diretoria com dado sensível tem acesso restrito aos participantes ([53](53-pacote-documentos-e-contratos.md), DC-27).
- Documento de processo administrativo público segue a lei de processo do ente. Conferido em 03/11/2026 na Lei 9.784/1999 (planalto.gov.br), que vale para a administração federal (art. 1º). Ente estadual e municipal segue lei própria, configurada pela entidade **(verificar)** por ente. Regras da lei federal que o sistema aplica quando a entidade escolher esse regime:
  - **Forma:** ato escrito, em português, com data, local e assinatura da autoridade (art. 22, § 1º). Páginas numeradas em sequência e rubricadas (art. 22, § 4º): no processo digital, o sistema numera cada peça e guarda o hash.
  - **Prazos:** 5 dias quando não houver prazo próprio, prorrogável até o dobro com justificativa (art. 24). Decisão em até 30 dias após a instrução, prorrogável uma vez com motivo (art. 49). Recurso em 10 dias da ciência (art. 59), com reconsideração em 5 dias e no máximo três instâncias (arts. 56 e 57). Contagem exclui o dia do começo e inclui o do vencimento, que passa ao dia útil seguinte sem expediente (art. 66). O sistema calcula e mostra o vencimento.
  - **Intimação:** com antecedência mínima de 3 dias úteis e o conteúdo do art. 26, § 1º. Registro da ciência no processo.
  - **Motivação:** obrigatória quando o ato nega ou limita direito, impõe sanção, decide recurso ou anula ato (art. 50). O sistema exige o campo de motivação nesses tipos de decisão.

---

## 4. Contexto C: documentos emitidos

Detalhado em [48](48-gerador-de-documentos-por-portal.md). Resumo do que o contexto tem e não tem:

- Tem: modelo versionado, elegibilidade, emissão individual e em lote, código de validação pública, revogação, cancelamento.
- Não tem: recebimento de arquivo do usuário. O único arquivo que entra é o anexo de assinatura, dentro do fluxo de assinatura.
- Documento emitido é imutável. Correção gera novo documento.

---

## 5. Serviços comuns

Estes serviços são usados pelos três contextos. Não guardam regra de negócio de nenhum contexto.

| Serviço | Função | Quem usa | Onde é especificado |
|---|---|---|---|
| **Armazenamento** | Guarda arquivos cifrados, com checksum e prazo de retenção. Cada contexto tem seu prefixo e sua política | A, B, C | [21](21-busca-e-armazenamento.md) |
| **Assinatura** | Coleta assinaturas de uma ou mais partes, na ordem definida, e guarda a evidência. Aceita provedores de terceiros e a assinatura própria, conforme CTR-06 | B e C, e contratos | [33](33-contratos-por-portal.md), seção 5 |
| **Protocolo** | Gera o número de protocolo de qualquer pedido ou documento. Número único por unidade | A (envio), B (tramitação), C (emissão) | [32](32-atendimento-privacidade-por-portal.md) |
| **Auditoria** | Registra cada ação com o contexto e o portal | A, B e C | [29](29-auditoria.md) |
| **Validação pública** | Confirma autenticidade por código. Só para documento emitido ou assinado | C e B (assinados) | [48](48-gerador-de-documentos-por-portal.md), seção 6 |

**Regra de uso dos serviços:** o contexto chama o serviço e recebe o resultado. Não lê tabela de outro contexto.

---

## 6. Por portal

| Portal | Contexto A (recebidos) | Contexto B (administrativos) | Contexto C (emitidos) |
|---|---|---|---|
| **Desenvolvedor** | Nada | Nada, salvo documentos da própria empresa | Publica modelos-padrão, sem dado |
| **Gestão** | Consulta o que foi aprovado, sem a imagem, salvo papel de validação | Cria, tramita, aprova e arquiva | Acompanha emissão e relatório |
| **Secretaria** | Valida, aprova ou recusa; vincula ao processo | Não tramita (salvo se for setor da própria secretaria) | Emite, assina e revoga com motivo |
| **Professor** | Nada | Lê documento de tramitação em que é parte | Solicita documento de sua turma |
| **Aluno maior e responsável** | Envia e acompanha o próprio documento e o de dependente com vínculo ativo | Nada | Solicita e baixa o próprio documento |
| **Fornecedor (terceiros)** | Envia documentos da empresa, com validade e alerta | Nada | Recebe documento emitido para ele, quando o contrato prevê |
| **Público** | Nada | Nada | Valida código, sem dado pessoal |

---

## 7. Como os contextos se encontram

Exemplo de fluxo completo, em matrícula:

1. **A:** responsável envia certidão de nascimento. A secretaria valida e aprova.
2. **Matrícula:** a aprovação libera o passo de documentos do wizard ([46](46-matricula-e-rematricula-por-portal.md), M-08).
3. **C:** a secretaria emite o contrato de matrícula pelo modelo publicado.
4. **Assinatura:** o contrato passa pelo serviço comum de assinatura, com o responsável como signatário.
5. **Protocolo:** cada etapa recebe número de protocolo pelo serviço comum.
6. **Auditoria:** cada etapa grava o contexto e o portal.

Ata de conselho de classe (B) pode gerar declaração de encaminhamento (C), mas o vínculo é de referência: a ata não é copiada para dentro do documento emitido.

---

## 8. O que muda nos documentos existentes

| Documento | Mudança |
|---|---|
| [31](31-matriz-portais-modulos.md), seção 3.1 | "Gestão de documentos" vira três contextos. Ver seção 1 deste documento |
| [48](48-gerador-de-documentos-por-portal.md) | Escopo restrito ao contexto C. Não recebe arquivo do usuário |
| [21](21-busca-e-armazenamento.md) | Prefixo e prazo de retenção por contexto |
| [33](33-contratos-por-portal.md), seção 5 | Assinatura passa a ser serviço comum |
| [32](32-atendimento-privacidade-por-portal.md) | Protocolo passa a ser serviço comum |

---

## 9. Pendências

| # | Pendência | Tipo |
|---|---|---|
| GD-01 | Validação de documento recebido | **Decidido** em 03/11/2026: secretaria valida, com dupla conferência para documento de identidade |
| GD-02 | Prazo de guarda de documento recebido, por tipo (matrícula, fornecedor, candidato) | (jurídico) |
| GD-03 | Tramitação de documento administrativo | **Decidido** em 03/11/2026: o sistema deve permitir criar o fluxo de aprovação por tipo de documento, com níveis configuráveis |
| GD-04 | Formato e tamanho máximo de arquivo recebido, por contexto | Operação, em homologação |
| GD-05 | Leitura automática (OCR) de documento recebido | **Decidido** em 03/11/2026: só sugere, e a pessoa confirma |
| GD-06 | Documento administrativo de entidade pública: regra de processo administrativo | **Conferido** em parte em 03/11/2026: Lei 9.784/1999 para o federal (seção 3.3). Falta a lei de cada estado e município **(verificar)** |
| GD-07 | DDL dos contextos A e B e das tabelas compartilhadas de protocolo e assinatura | **Feito** em 03/11/2026: seção 10 |
| GD-08 | Revisão do DDL pelo owner de cada contexto e teste de migração | Owner e operação |

---

## 10. DDL dos contextos e serviços comuns (GD-07)

Convenções de [51](51-ddl-modulos-novos.md): MySQL 8 ou MariaDB 10.6, `utf8mb4`, horários em UTC, `unidade_uuid` em toda tabela de unidade. Cada contexto tem prefixo próprio, para que as tabelas fiquem separadas.

```sql
-- Contexto A: documentos recebidos
CREATE TABLE recebidos_envios (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  origem          ENUM('responsavel','aluno','candidato','fornecedor') NOT NULL,
  remetente_uuid  CHAR(36) NOT NULL,
  pessoa_uuid     CHAR(36) NULL,
  tipo_documento  VARCHAR(60) NOT NULL,
  processo_tipo   ENUM('matricula','cadastro_fornecedor','candidatura','outro') NOT NULL,
  processo_uuid   CHAR(36) NULL,
  arquivo_uuid    CHAR(36) NOT NULL,
  arquivo_sha256  CHAR(64) NOT NULL,
  validade_em     DATE NULL,
  estado          ENUM('enviado','em_analise','aprovado','recusado','pendente_correcao','substituido') NOT NULL,
  motivo_estado   VARCHAR(500) NULL,
  protocolo_uuid  CHAR(36) NOT NULL,
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at      DATETIME(3) NULL,
  INDEX ix_envio_processo (unidade_uuid, processo_tipo, processo_uuid),
  INDEX ix_envio_validade (unidade_uuid, validade_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE recebidos_validacoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  envio_id        BIGINT UNSIGNED NOT NULL,
  validador_uuid  CHAR(36) NOT NULL,
  etapa           TINYINT UNSIGNED NOT NULL,
  resultado       ENUM('aprovado','recusado') NOT NULL,
  motivo          VARCHAR(500) NULL,
  validado_em     DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY ux_validacao_etapa (envio_id, etapa),
  CONSTRAINT fk_validacao_envio FOREIGN KEY (envio_id) REFERENCES recebidos_envios (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Contexto B: documentos administrativos
CREATE TABLE admin_documentos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tipo            VARCHAR(60) NOT NULL,
  titulo          VARCHAR(200) NOT NULL,
  estado          ENUM('rascunho','em_tramitacao','reprovado','aprovado','arquivado') NOT NULL,
  versao_aprovada INT UNSIGNED NULL,
  criado_por_uuid CHAR(36) NOT NULL,
  arquivo_uuid    CHAR(36) NULL,
  protocolo_uuid  CHAR(36) NULL,
  guarda_ate      DATE NULL,
  deleted_at      DATETIME(3) NULL,
  INDEX ix_admin_estado (unidade_uuid, estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE admin_fluxos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  unidade_uuid    CHAR(36) NOT NULL,
  tipo            VARCHAR(60) NOT NULL,
  nivel           TINYINT UNSIGNED NOT NULL,
  papel_aprovador VARCHAR(60) NOT NULL,
  UNIQUE KEY ux_fluxo_nivel (unidade_uuid, tipo, nivel)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE admin_tramitacoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  documento_id    BIGINT UNSIGNED NOT NULL,
  nivel           TINYINT UNSIGNED NOT NULL,
  aprovador_uuid  CHAR(36) NOT NULL,
  resultado       ENUM('pendente','aprovado','reprovado') NOT NULL,
  decidido_em     DATETIME(3) NULL,
  motivo          VARCHAR(500) NULL,
  CONSTRAINT fk_tramitacao_documento FOREIGN KEY (documento_id) REFERENCES admin_documentos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Serviços comuns
CREATE TABLE protocolos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  numero          VARCHAR(30) NOT NULL,
  contexto        ENUM('atendimento','recebido','administrativo','emitido') NOT NULL,
  referencia_uuid CHAR(36) NOT NULL,
  criado_em       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY ux_protocolo_numero (unidade_uuid, numero),
  INDEX ix_protocolo_referencia (referencia_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE assinaturas_pedidos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  contexto        ENUM('administrativo','emitido','contrato') NOT NULL,
  documento_uuid  CHAR(36) NOT NULL,
  arquivo_sha256  CHAR(64) NOT NULL,
  estado          ENUM('pendente','concluido','cancelado','expirado') NOT NULL,
  expira_em       DATETIME(3) NULL,
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  INDEX ix_assinatura_documento (documento_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE assinaturas_signatarios (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  pedido_id       BIGINT UNSIGNED NOT NULL,
  ordem           TINYINT UNSIGNED NOT NULL,
  pessoa_uuid     CHAR(36) NULL,
  papel           VARCHAR(40) NOT NULL,
  provedor        VARCHAR(40) NOT NULL,
  tipo            ENUM('simples','avancada','qualificada_icp_brasil') NOT NULL,
  estado          ENUM('pendente','assinado','recusado','expirado') NOT NULL,
  evidencia_hash  CHAR(64) NULL,
  assinado_em     DATETIME(3) NULL,
  UNIQUE KEY ux_signatario_ordem (pedido_id, ordem),
  CONSTRAINT fk_signatario_pedido FOREIGN KEY (pedido_id) REFERENCES assinaturas_pedidos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Regras do DDL:**

- `recebidos_validacoes` tem uma linha por etapa. A constraint `ux_validacao_etapa` impede repetir a mesma etapa. A regra de dupla conferência, que exige pessoa diferente na segunda etapa, é de aplicação.
- `protocolos` guarda os quatro contextos. É o único lugar onde o número é gerado, e a referência aponta para o objeto de origem, sem copiar dado.
- `assinaturas_pedidos` é usado por documentos administrativos, emitidos e contratos. A ordem de assinatura é a constraint `ux_signatario_ordem`.
- O documento emitido (contexto C) está em [51](51-ddl-modulos-novos.md), seção 12, e não é repetido aqui.

---

## 11. Critérios de aceite

- [ ] Documento recebido (A) nunca gera código de validação pública (teste).
- [ ] Quem criou um documento administrativo não aprova o próprio (teste de constraint).
- [ ] Documento emitido (C) não aceita upload de arquivo do usuário (teste).
- [ ] Documento administrativo não aparece para aluno ou responsável (teste de isolamento).
- [ ] Cada etapa do fluxo da seção 7 gera protocolo e evento de auditoria com o contexto (teste de integração).
- [ ] Contexto não lê tabela de outro contexto (verificação de código).
