# SAC

- Portal: Gestão (`gestao.`)
- Área: Atendimento
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.5; [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.6; [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.8
- Fonte da v1: absorvida integralmente em [chamados-dos-clientes.md](../../desenvolvedor/suporte/chamados-dos-clientes.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Atendimento ao público externo (famílias e candidatos) no modelo único de ticket.

## 3. Telas

- **SAC** (fila de tickets externos).

## 4. Permissões por portal (extraídas do SDD)

Do [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md):

| Portal | Quem abre | Onde é atendido | Visibilidade |
|---|---|---|---|
| Gestão | Equipe da entidade e atendentes | Fila da categoria e da unidade | Conforme permissão da fila |

Do [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md):

| Portal | Recurso de privacidade | Escopo |
|---|---|---|
| Gestão | DPO da entidade, ROPA da entidade, pedidos de titular, consentimentos, termos de imagem, proteção de menores | Entidade e unidades conforme permissão |

## 5. Papéis

- `unit.support`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seções 2.5 e 2.6.

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

### 13.1 [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.5

##### 2.5 Canais

Conforme [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 2, com estas regras de atendimento:

- Opção "Abrir ticket" sem IA em todo ponto de atendimento (D-18).
- Texto do solicitante é guardado literal, nunca interpretado como instrução ([05](../../../docs/v2/05-seguranca.md)).
- Campos obrigatórios variam por tipo, conforme a v1 ([`SPEC-HELPDESK.md`](../../../docs/v2/anexo-v1/SPEC-HELPDESK.md), seção 7). Lista de campos padrão é fixa para todo tipo.

### 13.2 [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.6

##### 2.6 Portal do cliente (solicitante)

- Abertura, acompanhamento, anexos, respostas públicas por padrão (v1, seção 12), consulta da base de conhecimento e avaliação do atendimento.
- Resposta interna (nota do atendente) nunca aparece no portal.
- Consulta pública por número e CPF, sem login, com limite de tentativas ([17](../../../docs/v2/17-regras-modulos.md), seção 3).

### 13.3 [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.8

##### 2.8 Atendimento por portal

| Portal | Quem abre | Onde é atendido | Visibilidade |
|---|---|---|---|
| Desenvolvedor | Entidades (clientes da plataforma) | Suporte da plataforma | Tickets de clientes; sem dado de aluno sem chamado vinculado ([29](../../../docs/v2/29-auditoria.md), seção 8) |
| Gestão | Equipe da entidade e atendentes | Fila da categoria e da unidade | Conforme permissão da fila |
| Professor | Docente, para materiais, reservas, justificativas | Secretaria ou coordenação | Só o próprio ticket |
| Aluno | Aluno, para segunda chamada, declaração, dúvidas | Secretaria, biblioteca, financeiro | Só o próprio ticket |
| Responsáveis | Responsável legal, pelos dependentes | Secretaria, financeiro, coordenação | Só dependentes com vínculo ativo |
| Terceiros | Fornecedor, para manutenção e acesso | Operacional e compras | Só o próprio ticket |
