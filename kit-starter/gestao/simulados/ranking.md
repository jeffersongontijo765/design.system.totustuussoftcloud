# Ranking

- Portal: Gestão (`gestao.`)
- Área: Simulados
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [47](../../../docs/v2/47-simulados-por-portal.md), seção 8; [47](../../../docs/v2/47-simulados-por-portal.md), seção 7
- Fonte da v1: absorvida integralmente em [banco-de-questoes.md](banco-de-questoes.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Relatórios e ranking de desempenho por turma, unidade e habilidade.

## 3. Telas

- **Ranking** (dashboard com filtros).
- **Relatório por habilidade** (gráficos).

## 4. Permissões por portal (extraídas do SDD)

Do [47](../../../docs/v2/47-simulados-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Criar perfil custom, ver relatórios agregados, ver kanban da unidade, exportar com auditoria | Ver redação individual sem papel de correção. Alterar nota confirmada sem motivo | E |
| **Coordenação pedagógica** | Ver relatório consolidado, confirmar nota em revisão, aprovar reprocessamento | Editar questão de simulado já publicado | E |

## 5. Papéis

- `unit.coordinator` e `unit.manager`: unidade.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Ranking é recurso do plano PRO ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.6); relatórios por portal ([47](../../../docs/v2/47-simulados-por-portal.md), seção 8).

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

### 13.1 [47](../../../docs/v2/47-simulados-por-portal.md), seção 8

#### 8. Relatórios e ranking

- Relatório por competência, por turma e por unidade, com média e distribuição. Abaixo do mínimo de respostas da [41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 3, o grupo não aparece.
- Ranking é do plano PRO (MOD-05). Mostra posição com nome só se a unidade permitir. O padrão é não expor nome de colega.
- Exportação de notas gera evento de auditoria ([29](../../../docs/v2/29-auditoria.md)).

### 13.2 [47](../../../docs/v2/47-simulados-por-portal.md), seção 7

#### 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar perfis-modelo, sem dado de aluno | Ver redação ou nota de qualquer entidade | P |
| **Gestão** | Criar perfil custom, ver relatórios agregados, ver kanban da unidade, exportar com auditoria | Ver redação individual sem papel de correção. Alterar nota confirmada sem motivo | E |
| **Professor** | Montar simulado para a própria turma, publicar, revisar sugestão da IA, confirmar ou devolver nota, ver relatório da turma | Ver simulado ou redação de outra turma. Confirmar a própria redação, se for aluno | E |
| **Coordenação pedagógica** | Ver relatório consolidado, confirmar nota em revisão, aprovar reprocessamento | Editar questão de simulado já publicado | E |
| **Aluno** | Enviar redação dentro do prazo, ver a nota e o feedback depois de confirmados. Ver o próprio ranking, se a unidade publicar | Ver nota da IA antes da confirmação. Ver redação de colega. Ver ranking nominal de colegas sem opção da unidade | E |
| **Responsáveis** | Ver a nota confirmada do dependente e o relatório do simulado | Ver redação do dependente com dado de terceiro. Ver outro aluno | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada, por padrão | Ver simulado, redação ou nota | E, [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md) |

**Aluno e nota da IA:** a regra de MOD-06 vale para qualquer nota. A IA nunca aparece ao aluno como nota.
