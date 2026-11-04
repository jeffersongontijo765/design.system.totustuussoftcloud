# Serviços comuns (assinatura, protocolo e armazenamento)

- Portal: Gestão (`gestao.`)
- Área: Gestão de documentos
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md) (integral)
- Fonte da v1: [spec_gestao_documentos_completo.md](../../../docs/v2/anexo-v1/spec_gestao_documentos_completo.md) (546 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Serviços usados pelos três contextos: assinatura eletrônica, protocolo, armazenamento com versão e hash, temporalidade e eliminação.

## 3. Telas

- **Assinaturas** (painel de pendências por documento e signatário).
- **Temporalidade** (configuração de prazos de guarda por tipo).
- **Armazenamento documental** (visão por contexto; integra Arquivos, [21](../../../docs/v2/21-busca-e-armazenamento.md)).

## 4. Permissões por portal (extraídas do SDD)

Do [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md):

| Portal | Contexto A (recebidos) | Contexto B (administrativos) | Contexto C (emitidos) |
|---|---|---|---|
| **Gestão** | Consulta o que foi aprovado, sem a imagem, salvo papel de validação | Cria, tramita, aprova e arquiva | Acompanha emissão e relatório |
| **Secretaria** | Valida, aprova ou recusa; vincula ao processo | Não tramita (salvo se for setor da própria secretaria) | Emite, assina e revoga com motivo |

## 5. Papéis

- `unit.manager`: temporalidade e eliminação.
- `unit.legal`: bloqueio legal.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Serviços comuns e DDL dos contextos ([54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seções 5 e 10); o que muda nos documentos existentes (seção 8).

## 7. Dados

- Tabelas e campos conforme a seção 13 e o DDL do [51](../../../docs/v2/51-ddl-modulos-novos.md), quando o módulo estiver lá. Toda tabela tem `entidade_id`, `unidade_id`, `created_at`, `updated_at`, `created_by` e exclusão lógica com `deleted_at` e `deleted_by` ([03](../../../docs/v2/03-dominio-tenancy.md), seção 6; [15](../../../docs/v2/15-validacoes.md); [19](../../../docs/v2/19-regras-modulos-3.md), seção 14).

## 8. Integrações

- Ver a seção de integrações do documento de origem, na seção 13.

## 9. Exportação, auditoria e privacidade

- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Toda criação, alteração, aprovação, exclusão lógica, exportação e leitura de dado sensível gera evento de auditoria no banco da unidade ([29](../../../docs/v2/29-auditoria.md)).
- Dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md): mínimo necessário, mascaramento em listas, base legal registrada.

## 10. Estados de interface

- Carregando (skeleton), vazio com chamada para ação, sem resultado de filtro, erro com nova tentativa, acesso negado, registro bloqueado, fechado ou baixado (somente leitura), conflito de edição (versão).

## 11. Requisitos de frontend

- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`): página de lista com DataTable, KPIs, drawer de detalhe, formulário em página ou modal, kanban quando houver fluxo de estados.
- Seletor de unidade no topo quando o usuário tiver mais de uma; a troca reemite o token com o novo contexto ([06](../../../docs/v2/06-identidade-acesso.md), seção 12).

## 12. Critérios de aceite e pendências

- Critérios de aceite: os do documento de origem (seção 13) e os de [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 6.
- Testes de isolamento: usuário de outra unidade ou entidade recebe 404 em toda rota do módulo ([03](../../../docs/v2/03-dominio-tenancy.md)).
- As pendências do documento de origem estão na seção 13 e consolidadas no [45](../../../docs/v2/45-pendencias-consolidadas.md).

## 13. Regras da v2 (texto integral das fontes, sem corte)

### 13.1 [54 — Gestão de Documentos: Três Contextos e Serviços Comuns](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Substitui a visão de "gestão de documentos" como bloco único que aparecia em [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.1. Emissão de documentos pela secretaria, detalhada em [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md). Armazenamento e retenção em [21](../../../docs/v2/21-busca-e-armazenamento.md). Protocolo e atendimento em [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md). Assinatura de contratos em [33](../../../docs/v2/33-contratos-por-portal.md), seção 5. Auditoria em [29](../../../docs/v2/29-auditoria.md). Pacotes jurídicos em [50](../../../docs/v2/50-pacote-juridico-e-norma.md) e [53](../../../docs/v2/53-pacote-documentos-e-contratos.md).
> **Status:** decisão de arquitetura, criada em 03/11/2026. Não centralizar: cada contexto tem dono, regras e portal próprios. O que é comum fica em serviços, sem compartilhar tabelas de negócio.

---

#### 1. Os três contextos

| Contexto | O que é | Quem origina | Quem cuida | Exemplos |
|---|---|---|---|---|
| **A. Documentos recebidos** | Arquivos enviados a instituição para análise e validação | Responsáveis, alunos, candidatos, fornecedores | Secretaria, RH, compras | Certidão de nascimento, RG do responsável, histórico de escola anterior, alvará do fornecedor |
| **B. Documentos administrativos** | Documentos internos de gestão, com tramitação e aprovação | Equipe da instituição | Gestão e administração | Ata de reunião de diretoria, ofício, circular, processo administrativo, política interna |
| **C. Documentos emitidos** | Documentos gerados pela instituição a partir de modelo, para uma pessoa ou uma organização | Secretaria | Secretaria | Declaração, histórico, boletim, certidão, contrato, termo |

Os três contextos não se misturam. Um documento pertence a um contexto, e o contexto define regras, estados, portal de acesso e prazo de guarda.

---

#### 2. Contexto A: documentos recebidos

##### 2.1 O que o contexto faz

- Recebe arquivo enviado pelo portal (responsável, aluno, candidato ou fornecedor).
- Confere o arquivo: formato, tamanho, legibilidade e tipo declarado.
- Valida o conteúdo por pessoa habilitada. A validação registra quem validou, quando e o resultado.
- Vincula o arquivo a um cadastro ou a um processo: matrícula, cadastro de fornecedor, candidatura.
- Controla vencimento, quando o documento tem validade (ex.: alvará, seguro, certidão).

##### 2.2 Estados

`enviado` → `em_analise` → `aprovado` ou `recusado` ou `pendente_correcao`.

- `recusado` exige motivo. O remetente recebe o motivo e pode reenviar.
- `pendente_correcao` tem prazo. Vencido o prazo, o processo vinculado é tratado conforme a regra do processo (ex.: matrícula condicional, em [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md)).
- `vencido` é calculado por data ([18](../../../docs/v2/18-regras-modulos-2.md), T-04), não gravado.

##### 2.3 Regras

- Documento de menor é enviado pelo responsável com vínculo ativo.
- Imagem de documento de identidade é guardada cifrada, com acesso restrito à validação. Número completo aparece mascarado nas telas ([07](../../../docs/v2/07-privacidade-lgpd.md)).
- Documento recebido não é emitido. Nunca gera código de validação pública.
- Validação não é automática por padrão. Automação de leitura (OCR) só sugere, e a pessoa confirma ([21](../../../docs/v2/21-busca-e-armazenamento.md), seção 3.10).

##### 2.4 Retenção

Prazo por tipo de documento, vinculado ao processo que originou o envio. Documento de matrícula segue o prazo de guarda escolar **(jurídico, [50](../../../docs/v2/50-pacote-juridico-e-norma.md), J-05 e N-10)**. Documento de fornecedor segue o prazo do contrato.

---

#### 3. Contexto B: documentos administrativos

##### 3.1 O que o contexto faz

- Cria documento interno com modelo ou em formato livre.
- Tramita: envia para análise, aprovação e assinatura de quem deve aprovar.
- Mantém versões. Versão aprovada não muda.
- Arquiva ao fim da tramitação, com prazo de guarda.

##### 3.2 Estados

`rascunho` → `em_tramitacao` → `aprovado` → `arquivado`, com `reprovado` como saída de `em_tramitacao`.

- Quem cria não aprova o próprio documento. Regra verificada no banco, como em [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), seção 12.
- Documento aprovado pode ser assinado. A assinatura usa o serviço comum da seção 5.

##### 3.3 Regras

- Documento administrativo não é visível a alunos e responsáveis, salvo quando a gestão publica um comunicado, que é contexto C ou um comunicado específico ([53](../../../docs/v2/53-pacote-documentos-e-contratos.md), DC-26).
- Ata de conselho ou de diretoria com dado sensível tem acesso restrito aos participantes ([53](../../../docs/v2/53-pacote-documentos-e-contratos.md), DC-27).
- Documento de processo administrativo público segue a lei de processo do ente. Conferido em 03/11/2026 na Lei 9.784/1999 (planalto.gov.br), que vale para a administração federal (art. 1º). Ente estadual e municipal segue lei própria, configurada pela entidade **(verificar)** por ente. Regras da lei federal que o sistema aplica quando a entidade escolher esse regime:
  - **Forma:** ato escrito, em português, com data, local e assinatura da autoridade (art. 22, § 1º). Páginas numeradas em sequência e rubricadas (art. 22, § 4º): no processo digital, o sistema numera cada peça e guarda o hash.
  - **Prazos:** 5 dias quando não houver prazo próprio, prorrogável até o dobro com justificativa (art. 24). Decisão em até 30 dias após a instrução, prorrogável uma vez com motivo (art. 49). Recurso em 10 dias da ciência (art. 59), com reconsideração em 5 dias e no máximo três instâncias (arts. 56 e 57). Contagem exclui o dia do começo e inclui o do vencimento, que passa ao dia útil seguinte sem expediente (art. 66). O sistema calcula e mostra o vencimento.
  - **Intimação:** com antecedência mínima de 3 dias úteis e o conteúdo do art. 26, § 1º. Registro da ciência no processo.
  - **Motivação:** obrigatória quando o ato nega ou limita direito, impõe sanção, decide recurso ou anula ato (art. 50). O sistema exige o campo de motivação nesses tipos de decisão.

---

#### 4. Contexto C: documentos emitidos

Detalhado em [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md). Resumo do que o contexto tem e não tem:

- Tem: modelo versionado, elegibilidade, emissão individual e em lote, código de validação pública, revogação, cancelamento.
- Não tem: recebimento de arquivo do usuário. O único arquivo que entra é o anexo de assinatura, dentro do fluxo de assinatura.
- Documento emitido é imutável. Correção gera novo documento.

---

#### 5. Serviços comuns

Estes serviços são usados pelos três contextos. Não guardam regra de negócio de nenhum contexto.

| Serviço | Função | Quem usa | Onde é especificado |
|---|---|---|---|
| **Armazenamento** | Guarda arquivos cifrados, com checksum e prazo de retenção. Cada contexto tem seu prefixo e sua política | A, B, C | [21](../../../docs/v2/21-busca-e-armazenamento.md) |
| **Assinatura** | Coleta assinaturas de uma ou mais partes, na ordem definida, e guarda a evidência. Aceita provedores de terceiros e a assinatura própria, conforme CTR-06 | B e C, e contratos | [33](../../../docs/v2/33-contratos-por-portal.md), seção 5 |
| **Protocolo** | Gera o número de protocolo de qualquer pedido ou documento. Número único por unidade | A (envio), B (tramitação), C (emissão) | [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md) |
| **Auditoria** | Registra cada ação com o contexto e o portal | A, B e C | [29](../../../docs/v2/29-auditoria.md) |
| **Validação pública** | Confirma autenticidade por código. Só para documento emitido ou assinado | C e B (assinados) | [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), seção 6 |

**Regra de uso dos serviços:** o contexto chama o serviço e recebe o resultado. Não lê tabela de outro contexto.

---

#### 6. Por portal

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

#### 7. Como os contextos se encontram

Exemplo de fluxo completo, em matrícula:

1. **A:** responsável envia certidão de nascimento. A secretaria valida e aprova.
2. **Matrícula:** a aprovação libera o passo de documentos do wizard ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), M-08).
3. **C:** a secretaria emite o contrato de matrícula pelo modelo publicado.
4. **Assinatura:** o contrato passa pelo serviço comum de assinatura, com o responsável como signatário.
5. **Protocolo:** cada etapa recebe número de protocolo pelo serviço comum.
6. **Auditoria:** cada etapa grava o contexto e o portal.

Ata de conselho de classe (B) pode gerar declaração de encaminhamento (C), mas o vínculo é de referência: a ata não é copiada para dentro do documento emitido.

---

#### 8. O que muda nos documentos existentes

| Documento | Mudança |
|---|---|
| [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.1 | "Gestão de documentos" vira três contextos. Ver seção 1 deste documento |
| [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md) | Escopo restrito ao contexto C. Não recebe arquivo do usuário |
| [21](../../../docs/v2/21-busca-e-armazenamento.md) | Prefixo e prazo de retenção por contexto |
| [33](../../../docs/v2/33-contratos-por-portal.md), seção 5 | Assinatura passa a ser serviço comum |
| [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md) | Protocolo passa a ser serviço comum |

---

#### 9. Pendências

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

#### 10. DDL dos contextos e serviços comuns (GD-07)

Convenções de [51](../../../docs/v2/51-ddl-modulos-novos.md): MySQL 8 ou MariaDB 10.6, `utf8mb4`, horários em UTC, `unidade_uuid` em toda tabela de unidade. Cada contexto tem prefixo próprio, para que as tabelas fiquem separadas.

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
- O documento emitido (contexto C) está em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 12, e não é repetido aqui.

---

#### 11. Critérios de aceite

- [ ] Documento recebido (A) nunca gera código de validação pública (teste).
- [ ] Quem criou um documento administrativo não aprova o próprio (teste de constraint).
- [ ] Documento emitido (C) não aceita upload de arquivo do usuário (teste).
- [ ] Documento administrativo não aparece para aluno ou responsável (teste de isolamento).
- [ ] Cada etapa do fluxo da seção 7 gera protocolo e evento de auditoria com o contexto (teste de integração).
- [ ] Contexto não lê tabela de outro contexto (verificação de código).

## 14. Conteúdo integral da v1 (absorvido)

### Spec — Gestão de Documentos

- Language Standard: Global English
#### 1. Objetivo do módulo

O módulo de **Gestão de Documentos** deve centralizar cadastro, organização, tramitação, aprovação, assinatura digital, arquivamento e auditoria de documentos físicos e digitais, com suporte completo a fluxo operacional, segurança e conformidade.

#### 2. Escopo funcional

##### 2.1 Tipos de documento
- Documentos internos.
- Documentos externos.
- Contratos.
- Ofícios.
- Procurações.
- Políticas e procedimentos.
- Requisições.
- Relatórios.
- Documentos com assinatura digital.
- Documentos sem assinatura digital.

##### 2.2 Ciclo de vida
- Rascunho.
- Em revisão.
- Aguardando aprovação.
- Aguardando assinatura.
- Assinado.
- Publicado.
- Arquivado.
- Expirado.
- Cancelado.
- Rejeitado.

##### 2.3 Capacidades centrais
- Upload, indexação e versionamento.
- Busca avançada e filtros combinados.
- Fluxo de aprovação e assinatura.
- Controle de acesso por perfil, unidade e entidade.
- Histórico, trilha de auditoria e logs.
- Automação de tarefas e alertas.
- Gestão por Kanban e lista.
- Indicadores e dashboards.

#### 3. Páginas do módulo

##### 3.1 Dashboard principal
**Objetivo:** visão executiva e operacional do ambiente documental.

**Widgets:**
- Total de documentos.
- Documentos pendentes por status.
- Documentos aguardando assinatura.
- Documentos vencendo em X dias.
- Documentos com SLA estourado.
- Documentos arquivados por período.
- Volume de upload por dia.
- Taxa de aprovação.
- Taxa de rejeição.
- Assinaturas pendentes por aprovador.

**Charts:**
- Linha: volume de documentos por tempo.
- Barras: documentos por status.
- Pizza: distribuição por tipo.
- Donut: documentos com e sem assinatura digital.
- Área: evolução de assinaturas concluídas.
- Heatmap: atividade por dia da semana e hora.

**Controles:**
- Filtros por entidade, unidade, tipo, status, período, responsável e prioridade.
- Atalho para novo documento.
- Atalho para iniciar fluxo.
- Atalho para documentos vencidos.
- Exportação CSV/PDF.
- Atualização automática.

##### 3.2 Lista de documentos
**Objetivo:** visualização tabular robusta para operação diária.

**Datatable com colunas:**
- Checkbox de seleção.
- Código.
- Título.
- Tipo.
- Categoria.
- Status.
- Assinatura digital.
- Versão.
- Responsável.
- Unidade.
- Entidade.
- Criado em.
- Atualizado em.
- Validade.
- Prioridade.
- SLA.
- Ações.

**Recursos do datatable:**
- Ordenação por qualquer coluna.
- Paginação.
- Busca global.
- Busca por colunas.
- Filtros salvos.
- Agrupamento por status, tipo ou unidade.
- Colunas configuráveis.
- Multi-select.
- Ações em massa.
- Exportar CSV, XLSX e PDF.
- Pin de colunas.
- Lazy loading.

**Ações por linha:**
- Visualizar.
- Editar.
- Duplicar.
- Enviar para revisão.
- Solicitar assinatura.
- Aprovar.
- Rejeitar.
- Arquivar.
- Reabrir.
- Cancelar.
- Ver histórico.
- Baixar arquivo.
- Gerenciar permissões.

##### 3.3 Cadastro de documento
**Objetivo:** criar e editar documentos com controle de metadados e anexos.

**Campos principais:**
- Título.
- Código interno.
- Tipo.
- Categoria.
- Subcategoria.
- Descrição.
- Tags.
- Unidade.
- Entidade.
- Responsável.
- Solicitante.
- Data de emissão.
- Data de validade.
- Confidencialidade.
- Nível de acesso.
- Requer assinatura digital.
- Requer aprovação.
- Observações.

**Campos de arquivo:**
- Upload principal.
- Anexos complementares.
- Versão inicial.
- Formato aceito.
- Preview.

**Campos de fluxo:**
- Roteiro de aprovação.
- Roteiro de assinatura.
- Prazo por etapa.
- Prioridade.
- SLA.

##### 3.4 Drawer de CRUD
**Objetivo:** criação e edição rápida sem sair da lista.

**Seções do drawer:**
- Dados básicos.
- Classificação.
- Arquivos.
- Fluxo.
- Assinatura.
- Permissões.
- Auditoria resumida.

**Comportamentos:**
- Salvar rascunho.
- Salvar e continuar editando.
- Salvar e iniciar fluxo.
- Salvar e anexar outro arquivo.
- Validação inline.
- Autosave opcional.
- Histórico de mudanças no próprio drawer.

##### 3.5 Visualização detalhada
**Objetivo:** página completa do documento.

**Blocos da página:**
- Cabeçalho com título, status e ações.
- Resumo do documento.
- Preview do arquivo.
- Timeline de eventos.
- Histórico de versões.
- Aprovações.
- Assinaturas.
- Comentários.
- Anexos.
- Permissões.
- Auditoria.

**Ações no cabeçalho:**
- Editar.
- Baixar.
- Compartilhar.
- Solicitar revisão.
- Solicitar assinatura.
- Aprovar.
- Rejeitar.
- Arquivar.
- Cancelar.
- Criar nova versão.

##### 3.6 Kanban
**Objetivo:** acompanhar o fluxo documental por estágio.

**Colunas sugeridas:**
- Rascunho.
- Em revisão.
- Aguardando aprovação.
- Aguardando assinatura.
- Em assinatura.
- Concluído.
- Arquivado.
- Rejeitado.

**Cards com:**
- Título.
- Tipo.
- Responsável.
- Prazo.
- Alertas.
- Ícone de assinatura.
- Indicador de prioridade.
- Última atualização.

**Interações:**
- Drag and drop.
- Filtro por responsável.
- Filtro por unidade.
- Filtro por tipo.
- Atalhos de ação no card.
- Expansão rápida do card.

##### 3.7 Assinatura digital
**Objetivo:** controlar documentos que exigem assinatura eletrônica/digital.

**Funcionalidades:**
- Marcar documento como assinável.
- Definir signatários em ordem ou paralelos.
- Exibir status de cada assinatura.
- Capturar evidências da assinatura.
- Validar certificado.
- Registrar IP, data, hora e trilha.
- Bloquear edição após assinatura, conforme política.
- Reenvio de solicitação.
- Expiração de pedido de assinatura.

**Estados de assinatura:**
- Não iniciado.
- Enviado.
- Visualizado.
- Em andamento.
- Assinado.
- Recusado.
- Expirado.
- Revogado.

##### 3.8 Automações
**Objetivo:** reduzir trabalho manual com regras de negócio.

**Automations examples:**
- Ao subir documento, classificar automaticamente por tipo via regra.
- Ao atingir status “Aguardando assinatura”, notificar signatários.
- Ao vencer prazo, gerar alerta e escalar.
- Ao aprovar, mover para próximo estágio.
- Ao rejeitar, devolver ao solicitante com motivo.
- Ao expirar validade, arquivar automaticamente.
- Ao criar nova versão, invalidar versão anterior.
- Ao anexar documento sensível, aplicar nível de acesso restrito.

**Tipos de automação:**
- Baseada em evento.
- Baseada em tempo.
- Baseada em condição.
- Baseada em regra de classificação.
- Baseada em SLA.

##### 3.9 Controles
**Objetivo:** governança e segurança do módulo.

**Controles obrigatórios:**
- Permissões por papel.
- Permissões por entidade.
- Permissões por unidade.
- Controle de leitura, edição, exclusão, aprovação, assinatura e exportação.
- Máscara de campos sensíveis.
- Bloqueio de download em documentos restritos.
- Watermark no preview e exportação.
- Expiração de links compartilhados.
- Auditoria de acesso.
- Versionamento imutável.
- Retenção por política.
- Lock de documento em workflow.
- Dupla validação para ações críticas.

##### 3.10 Gerenciamentos
**Objetivo:** administrar a estrutura documental.

**Subáreas:**
- Tipos de documento.
- Categorias e subcategorias.
- Modelos e templates.
- Tags.
- Status e transições.
- Regras de SLA.
- Níveis de confidencialidade.
- Papéis e permissões.
- Assinantes.
- Integrações externas.
- Políticas de retenção.
- Logs e auditoria.

#### 4. Estrutura de páginas

##### 4.1 Navegação
- Dashboard.
- Documentos.
- Kanban.
- Assinaturas.
- Aprovações.
- Categorias.
- Templates.
- Automações.
- Auditoria.
- Configurações.

##### 4.2 Rotas sugeridas
- `/documentos`
- `/documentos/novo`
- `/documentos/:id`
- `/documentos/:id/editar`
- `/documentos/:id/versoes`
- `/documentos/:id/auditoria`
- `/documentos/kanban`
- `/documentos/assinaturas`
- `/documentos/aprovacoes`
- `/documentos/automacoes`
- `/documentos/configuracoes`

#### 5. Widgets essenciais

- Total de documentos ativos.
- Pendências por usuário.
- Assinaturas atrasadas.
- Fluxos em andamento.
- Documentos por vencimento.
- Documentos por unidade.
- Documentos por categoria.
- Últimas movimentações.
- Alertas críticos.
- Documentos sensíveis.
- Aprovações recentes.
- Uploads recentes.

#### 6. Charts recomendados

- Linha: criação de documentos ao longo do tempo.
- Barras verticais: documentos por status.
- Barras horizontais: documentos por unidade.
- Pizza: distribuição por tipo.
- Donut: com assinatura vs sem assinatura.
- Radar: desempenho por área.
- Funil: etapa de aprovação.
- Heatmap: atividade por horário.
- Área empilhada: crescimento por categoria.

#### 7. Regras de negócio

- Documento com assinatura digital não pode ser editado após assinatura final, exceto nova versão autorizada.
- Documentos confidenciais exigem permissão explícita para leitura e download.
- Toda ação crítica deve ser registrada em auditoria.
- Toda mudança de status deve respeitar transições válidas.
- Documento vencido deve gerar alerta e política de tratamento.
- Documentos arquivados ficam somente leitura.
- Rejeição deve exigir motivo obrigatório.
- A exclusão física deve ser substituída por exclusão lógica, salvo política especial.
- Deve existir rastreabilidade completa de versões.

#### 8. Permissões sugeridas

- `document.view`
- `document.create`
- `document.edit`
- `document.delete`
- `document.export`
- `document.archive`
- `document.approve`
- `document.reject`
- `document.sign`
- `document.manage_permissions`
- `document.manage_workflow`
- `document.manage_templates`
- `document.manage_automations`
- `document.view_audit`

#### 9. Estados e feedbacks

##### Estados de interface
- Loading.
- Empty state.
- Error state.
- Permission denied.
- Draft saved.
- Action success.
- Action failed.
- Syncing signature.
- File uploading.
- Processing preview.

##### Feedbacks obrigatórios
- Toasts.
- Confirm dialog para ações destrutivas.
- Banner para pendências críticas.
- Badge por status.
- Alertas por SLA.

#### 10. Validações

- Título obrigatório.
- Tipo obrigatório.
- Arquivo obrigatório para documentos publicados.
- Assinante obrigatório quando assinatura digital estiver ativa.
- Fluxo obrigatório quando aprovação for requerida.
- Data de validade não pode ser anterior à emissão.
- Campos sensíveis precisam de justificativa quando exigido.
- Regras de transição devem ser respeitadas.
- Upload deve validar extensão, tamanho e integridade.

#### 11. Auditoria e rastreabilidade

Registrar:
- Criação.
- Edição.
- Troca de status.
- Upload e remoção de anexos.
- Visualização de documento sensível.
- Download.
- Exportação.
- Aprovação.
- Rejeição.
- Assinatura.
- Reabertura.
- Arquivamento.
- Cancelamento.
- Mudança de permissão.
- Alteração de automação.

Cada evento deve guardar:
- Usuário.
- Data/hora.
- IP.
- Unidade.
- Entidade.
- Ação.
- Dados antes/depois.
- Correlation ID.

#### 12. Componentes front-end

- DataTable avançada.
- Drawer CRUD.
- Modal de confirmação.
- Modal de assinatura.
- Modal de compartilhamento.
- Preview de documento.
- Timeline.
- Kanban board.
- Badge de status.
- KPI cards.
- Chart cards.
- Tabs de detalhes.
- Comment thread.
- Permission matrix.
- Version list.
- Audit log table.
- Workflow stepper.

#### 13. Integrações

- Serviço de assinatura digital.
- Storage de arquivos.
- OCR/indexação.
- Notificações por e-mail.
- Notificações in-app.
- Webhooks.
- API para integrações externas.
- SSO/IdP, se aplicável.
- Logs centralizados.
- Antivírus/scan de upload.

#### 14. MVP e evolução

##### MVP
- Cadastro de documentos.
- Lista com datatable.
- Preview.
- Upload.
- Versionamento.
- Aprovação simples.
- Assinatura digital básica.
- Kanban.
- Dashboard.
- Auditoria.

##### Evolução
- OCR.
- Busca full-text.
- Classificação automática.
- Regras avançadas de automação.
- SLA por perfil.
- Compartilhamento externo seguro.
- Templates dinâmicos.
- Assinatura múltipla em fluxo paralelo.
- Expiração e retenção automatizada.

#### 15. Critérios de aceite

- O usuário consegue criar, editar, visualizar e arquivar documentos com segurança.
- O sistema suporta documentos com e sem assinatura digital.
- A lista suporta filtros, busca, exportação e ações em massa.
- O Kanban reflete o fluxo real do documento.
- As automações disparam corretamente por evento e tempo.
- As permissões impedem acesso indevido.
- Toda ação crítica é auditável.
- Os dashboards exibem indicadores confiáveis e atualizados.

#### 16. Observação de implementação

Para sua stack, esse módulo pode ser implementado com:
- Backend com API REST bem versionada.
- Banco com tabelas para documentos, versões, assinaturas, aprovações, auditoria, automações e permissões.
- Frontend com páginas modulares, drawers, tabs e componentes reutilizáveis.
- Storage separado para binários.
- Índice de busca para metadados e texto extraído.
- Camada de workflow para transições e automações.
