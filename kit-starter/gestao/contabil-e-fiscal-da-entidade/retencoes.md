# Retenções

- Portal: Gestão (`gestao.`)
- Área: Contábil e fiscal da entidade
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.9; [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 11
- Fonte da v1: absorvida integralmente em [plano-de-contas-da-entidade.md](plano-de-contas-da-entidade.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Calcular e registrar retenções tributárias em pagamentos a fornecedores e prestadores.

## 3. Telas

- **Retenções** (DataTable por documento e tributo).

## 4. Permissões por portal (extraídas do SDD)

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Teste de isolamento | Teste de permissão | Teste de fluxo principal | Teste de acessibilidade |
|---|---|---|---|---|
| Gestão | Cross-tenant e cross-unidade | Papel sem permissão não vê o módulo | Matrícula, cobrança, emissão de documento | Telas principais |

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Autenticação | Sessão | Dados e restrições especiais |
|---|---|---|---|
| Gestão | Senha e MFA conforme política da entidade ([06](../../../docs/v2/06-identidade-acesso.md), seção 5) | Padrão | Consulta por CPF com finalidade ([21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6.8) |

## 5. Papéis

- `unit.fiscal`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Retenção não é módulo próprio; fica em contábil e fiscal ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.9). Parâmetros obrigatórios (critério 3 do [80](../../../docs/v2/80-decisoes-por-padrao.md)).

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

### 13.1 [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.9

##### 3.9 Módulos sem especificação

| Nome | Onde aparece | Situação |
|---|---|---|
| Planejamento acadêmico | Pedido do autor | Não há especificação na v1 nem na v2. **Decidido** em 03/11/2026: analisado e implementado em [37](../../../docs/v2/37-planejamento-e-empenho.md). |
| Planejamento institucional | Pedido do autor | Idem |
| Planejamento de desenvolvimento | Pedido do autor. A v1 cita "Plano de Desenvolvimento Individual" no PRO de preceptoria | Idem. Se o termo for o PDI, ele fica em preceptoria ([19](../../../docs/v2/19-regras-modulos-3.md), seção 11) |
| Empenho | Pedido do autor. A v1 não traz o termo como módulo | Empenho é fase da despesa pública (empenho, liquidação, pagamento). Só se aplica se a entidade for órgão público. **Decidido** em 03/11/2026: só para entidade pública. |
| Secretaria como módulo | v1 tem "Secretaria Digital" e "Secretaria Acadêmica" | Não é módulo próprio. É sub-área do acadêmico (seção 2.2) |
| Tributos como módulo | v1 tem "Retenção Tributária" e "Retenções e Tributos" | Não é módulo próprio. Fica em contábil e fiscal |

### 13.2 [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 11

#### 11. Fiscal

- Nota fiscal de serviço segue o ISS do município (LC 116/2003) [A]. Cada município tem integração própria ([16](../../../docs/v2/16-integracoes-externas.md), seção 3).
- Guarda de documentos fiscais: 5 anos (CTN, art. 195) [V].
- Cancelamento de nota segue as regras do município e registra o motivo.
