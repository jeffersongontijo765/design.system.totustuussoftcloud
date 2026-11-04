# Protocolo de atendimento

- Portal: Gestão (`gestao.`)
- Área: Secretaria
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.2; [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 5; [17](../../../docs/v2/17-regras-modulos.md), seção 4
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Registrar e acompanhar requerimentos e solicitações (secretaria, pedagógico, financeiro, LGPD) com número de protocolo, prazo, responsável e consulta pública por número e CPF.

## 3. Telas

- **Protocolos** (DataTable e kanban por estado): número, tipo, solicitante, prazo, responsável.
- **Novo protocolo — balcão** (formulário por tipo de requerimento).
- **Protocolo — detalhe** (página): linha do tempo, anexos, despacho, resposta, documento emitido.
- **Tipos de requerimento** (configuração): prazo, setor, documentos exigidos, taxa.
- **Consulta pública** (página sem login): número e CPF, com limite de tentativas.

## 4. Permissões por portal (extraídas do SDD)

Do [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md):

| Portal | Contexto A (recebidos) | Contexto B (administrativos) | Contexto C (emitidos) |
|---|---|---|---|
| **Gestão** | Consulta o que foi aprovado, sem a imagem, salvo papel de validação | Cria, tramita, aprova e arquiva | Acompanha emissão e relatório |
| **Secretaria** | Valida, aprova ou recusa; vincula ao processo | Não tramita (salvo se for setor da própria secretaria) | Emite, assina e revoga com motivo |

## 5. Papéis

- `unit.secretary`: abrir, despachar e responder.
- `unit.coordinator` e `unit.finance`: despachar os do próprio setor.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Protocolo é serviço comum, separado do CRM comercial e do atendimento (helpdesk) ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.2).
- Consulta pública por número e CPF, sem login, com limite de tentativas ([17](../../../docs/v2/17-regras-modulos.md), seção 4.2).

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

### 13.1 [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.2

##### 3.2 Protocolo × CRM comercial × Atendimento

Não encontrei na v1 um módulo chamado "CRM protocolo". O protocolo aparece em:

- Secretaria (número e senha, consulta pública por número e CPF) — [`spec_gestao_academica_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_academica_completo.md), seção 6.2;
- Gestão de documentos e validações;
- Serviços do portal do aluno, do professor e dos responsáveis;
- Direitos do titular (solicitação LGPD com protocolo — [07](../../../docs/v2/07-privacidade-lgpd.md));
- Segurança e medicina do trabalho (protocolo de CAT ou INSS).

**Decisão proposta:** o **protocolo é um serviço transversal**, dono em Atendimento. Ele gera número único, status, prazo e trilha. Ele **não pertence ao CRM**:

| | CRM comercial (plataforma e tenant) | Protocolo |
|---|---|---|
| Objeto | Lead, oportunidade, proposta, matrícula em andamento | Pedido ou solicitação com número |
| Quem abre | Vendedor, admissões, canal de captação | Pessoa que pede algo (aluno, responsável, professor, titular, fornecedor) |
| Consulta pública | Não | Sim, por número e CPF, com limite de tentativas ([17](../../../docs/v2/17-regras-modulos.md), seção 3) |

**Regra de separação:** nenhum protocolo guarda dado comercial, e nenhum lead recebe número de protocolo. Quando um lead vira matrícula, o protocolo de matrícula é um pedido separado, vinculado ao lead.

### 13.2 [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 5

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

### 13.3 [17](../../../docs/v2/17-regras-modulos.md), seção 4

#### 4. Acadêmico

##### 4.1 Entidades

Matrícula, aluno, turma, disciplina, diário, avaliação, plano de aula, plano de ensino, conselho de classe, estágio, documentos da secretaria, presença (22 tabelas na v1).

##### 4.2 Campos e regras (v1, seções 4 a 9)

| Campo | Regra |
|---|---|
| CPF do aluno ou candidato | Único por tenant. Busca antes de cadastrar; alerta de matrícula duplicada (v1, seção 4.2). |
| Documentos pessoais | Versionados, com data de upload, validade, responsável e hash de integridade (v1, seção 5). |
| Matrícula | Um vínculo ativo por aluno e turma. Vaga disponível com bloqueio de concorrência ([15](../../../docs/v2/15-validacoes.md), seção 7). |
| Trancamento | Prazo máximo conforme regimento **[Pendente: valor do regimento, por curso]**. |
| Nota | Dentro da faixa do método de avaliação; período de lançamento aberto. |
| Presença por QR Code | Válido por 5 minutos por padrão, configurável pela escola. Decidido pelo autor em 03/11/2026. Geolocalização só com consentimento, conforme [07](../../../docs/v2/07-privacidade-lgpd.md). |
| Horas de atividade complementar | Status `pendente_validacao`, `validado`, `recusado`. Total validado nunca ultrapassa o limite do curso. |
| Estágio | CNPJ válido da empresa concedente. Apólice de seguro com validade. |
| Protocolo de atendimento | Consulta pública por número e CPF, sem login, com limite de tentativas. |

##### 4.3 Estados

| Entidade | Estados |
|---|---|
| Matrícula | `pre_matricula`, `ativa`, `trancada`, `concluida`, `cancelada`, `transferida` |
| Diário | `aberto`, `fechado`, `reaberto` (com justificativa) |
| Estágio | `solicitado`, `ativo`, `concluido`, `cancelado` |

##### 4.4 Segurança específica

- Dados de aluno menor de idade: acesso do responsável legal, com vínculo verificado ([07](../../../docs/v2/07-privacidade-lgpd.md), seção 1).
- Diário e notas: professor vê só as turmas em que está vinculado.
