# Gabarito

- Portal: Gestão (`gestao.`)
- Área: Simulados
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [47](../../../docs/v2/47-simulados-por-portal.md), seção 4; [47](../../../docs/v2/47-simulados-por-portal.md), seção 9
- Fonte da v1: absorvida integralmente em [banco-de-questoes.md](banco-de-questoes.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Publicar gabarito e comentários após a prova, com controle de liberação.

## 3. Telas

- **Gabaritos** (lista por prova; liberar para alunos e responsáveis).

## 4. Permissões por portal (extraídas do SDD)

Do [47](../../../docs/v2/47-simulados-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Criar perfil custom, ver relatórios agregados, ver kanban da unidade, exportar com auditoria | Ver redação individual sem papel de correção. Alterar nota confirmada sem motivo | E |
| **Coordenação pedagógica** | Ver relatório consolidado, confirmar nota em revisão, aprovar reprocessamento | Editar questão de simulado já publicado | E |

## 5. Papéis

- `unit.coordinator`: liberar gabarito.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Liberação só depois do fim da aplicação ([47](../../../docs/v2/47-simulados-por-portal.md), seção 9).

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

### 13.1 [47](../../../docs/v2/47-simulados-por-portal.md), seção 4

#### 4. Estados

**Simulado:** `rascunho` → `publicado` → `em_aplicacao` → `encerrado` → `arquivado`.

**Redação:** `enviada` → `ocr_em_andamento` → `ocr_concluido` ou `revisao_ocr` → `em_correcao_ia` → `sugerida_pela_ia` → `em_revisao_professor` → `confirmada` ou `devolvida`.

- `revisao_ocr`: confiança baixa ou página ilegível. Pede novo envio ou leitura manual.
- `devolvida`: o professor pede reprocessamento ou nova entrega. Registrada com motivo.
- Prazo vencido é calculado, não gravado ([18](../../../docs/v2/18-regras-modulos-2.md), T-04).

### 13.2 [47](../../../docs/v2/47-simulados-por-portal.md), seção 9

#### 9. Automações

- Publicar simulado: aviso à turma, com data de abertura e fechamento.
- Receber redação: OCR automático.
- Concluir OCR com confiança suficiente: correção por IA.
- Confiança baixa: `revisao_ocr` e aviso ao professor.
- Confirmar nota: aviso ao aluno.
- Nota abaixo da meta da rubrica: trilha de reforço, com sugestão de atividade para o professor aprovar.
- Encerrar simulado: relatório consolidado.
