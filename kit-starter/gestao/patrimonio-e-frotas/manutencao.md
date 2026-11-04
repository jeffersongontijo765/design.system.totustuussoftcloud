# Manutenção

- Portal: Gestão (`gestao.`)
- Área: Patrimônio e frotas
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [19](../../../docs/v2/19-regras-modulos-3.md), seção 8; [19](../../../docs/v2/19-regras-modulos-3.md), seção 9
- Fonte da v1: absorvida integralmente em [patrimonio.md](../../desenvolvedor/operacoes-internas/patrimonio.md), [frotas.md](../../desenvolvedor/operacoes-internas/frotas.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Ordens de manutenção de bens e veículos.

## 3. Telas

- **Ordens** (kanban).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `unit.assets`, `unit.fleet` e aprovadores.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- [19](../../../docs/v2/19-regras-modulos-3.md), seções 8 e 9.

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

### 13.1 [19](../../../docs/v2/19-regras-modulos-3.md), seção 8

#### 8. Patrimônio

##### 8.1 Entidades com DDL (12 tabelas)

Categorias de ativo, ativos e demais. Valores em `DECIMAL(15,2)` e taxa em `DECIMAL(8,4)`. Os tipos estão adequados.

##### 8.2 Regras

| Campo | Regra |
|---|---|
| `acquisition_value` | Maior que zero. Não altera após a aquisição, salvo correção com motivo. |
| `residual_value` | Não negativo; não maior que `acquisition_value`. |
| `dep_method` | Lista fechada: `linear`, `accelerated`, `degressive`, `unit`. |
| `dep_rate` | Entre 0 e 100%, conforme método. |
| `current_value` | Calculado. Não é campo editável. Ver T-04. |
| Baixa | Ativo baixado não recebe depreciação nem movimento. |

**Pendente:** regra de depreciação por categoria, aprovada pela contabilidade.

### 13.2 [19](../../../docs/v2/19-regras-modulos-3.md), seção 9

#### 9. Frotas

| Regra | Detalhe |
|---|---|
| CNH do motorista | Vencida bloqueia a reserva e exibe alerta (linha 422). |
| Conflito de horário | Bloqueia a reserva do veículo (linha 421). |
| Veículo em manutenção | Bloqueia; sugere veículo alternativo (linha 423). |
| Tacógrafo | Validade obrigatória quando aplicável (linha 240). |
| Consumo | Calculado a partir de litros e quilometragem. Não editável (linha 580). |
| Abastecimento | Litros obrigatório e maior que zero (linha 612). |

**Defeito:** 13 DDL sem `tenant_id` (T-01). Consumo "calculado" aparece como campo de entrada em outra tela (linha 215). Padronizar como calculado.
