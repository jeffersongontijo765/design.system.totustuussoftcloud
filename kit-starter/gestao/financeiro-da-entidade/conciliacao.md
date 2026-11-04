# Conciliação

- Portal: Gestão (`gestao.`)
- Área: Financeiro da entidade
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [17](../../../docs/v2/17-regras-modulos.md), seção 2.5; [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 12; [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 9
- Fonte da v1: absorvida integralmente em [titulos.md](titulos.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Conciliar extratos bancários e do gateway com títulos e pagamentos.

## 3. Telas

- **Conciliação** (página lado a lado: extrato × lançamentos, sugestão automática, confirmação).
- **Divergências** (fila).

## 4. Permissões por portal (extraídas do SDD)

Do [71](../../../docs/v2/71-financeiro-completo-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver tudo: DRE, fluxo, inadimplência, caixa. Aprovar despesa e fechamento de caixa | Operar caixa. Lançar pagamento sem aprovação | E |
| **Coordenação** | Ver o financeiro da unidade, em leitura | Lançar ou aprovar lançamento | E |
| **Secretaria** | Receber pagamento de aluno na unidade, em caixa de atendimento. Emitir boleto e segunda via | Pagar despesa. Ver DRE | E |

## 5. Papéis

- `unit.finance`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Regras de conciliação ([17](../../../docs/v2/17-regras-modulos.md), seção 2.5; [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 12; [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 9).

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

### 13.1 [17](../../../docs/v2/17-regras-modulos.md), seção 2.5

##### 2.5 Conciliação bancária

A v1 define matching automático (seção 7.5):

| Regra | Classificação |
|---|---|
| Valor exato e data ± 1 dia | Match automático, confiança alta |
| Valor exato e data ± 3 dias | Match sugerido, confiança média |
| Valor ± R$ 0,01 e data ± 1 dia | Match sugerido |
| Sem match | Pendente manual |

**[Pendente]** A regra de R$ 0,01 é tolerância de arredondamento. Ela deve ser parâmetro do tenant, e não constante. Um lançamento só pode ser conciliado uma vez: `financial_transactions.status = matched` impede novo vínculo.

### 13.2 [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 12

#### 12. Conciliação

- Diária, por conta de gateway: extrato do provedor contra o ledger.
- Diferença de valor, de quantidade ou de status gera item na fila de conciliação, com alerta ao financeiro.
- Conciliação não corrige sozinha. Ajuste é lançamento com motivo e aprovação.
- Relatório de conciliação fica disponível para auditoria e não contém dado de cartão.

### 13.3 [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 9

#### 9. Conciliação

Regras já definidas em [17](../../../docs/v2/17-regras-modulos.md), seção 2.5, e [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 12. Reforço:

- Tolerância de arredondamento é parâmetro da entidade, não constante ([17](../../../docs/v2/17-regras-modulos.md), LAC-06).
- Conciliação não ajusta sozinha. Diferença vira item de conciliação e o ajuste é lançamento com motivo e aprovação.
- Extrato OFX é importado com hash por linha, para não duplicar.
