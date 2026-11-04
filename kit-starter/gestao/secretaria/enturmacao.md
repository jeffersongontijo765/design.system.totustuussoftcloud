# Enturmação

- Portal: Gestão (`gestao.`)
- Área: Secretaria
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-03; [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-07; [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), seção 2.4
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Distribuir os alunos matriculados nas turmas, respeitando vagas, pré-requisitos e o bloqueio de concorrência.

## 3. Telas

- **Enturmação** (quadro de turmas com contadores de vaga; arrastar aluno entre turmas com validação).
- **Pendentes de enturmação** (lista).
- **Enturmação em lote** (assistente com pré-visualização e relatório de recusas).

## 4. Permissões por portal (extraídas do SDD)

Do [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Abrir e fechar janela de rematrícula, ver kanban, aprovar trancamento acima do prazo, emitir declaração, cancelar matrícula com motivo | Alterar matrícula ativa sem registro de motivo. Ver documento de saúde sem o papel do módulo | E |
| **Secretaria** | Analisar, condicionar, efetivar, transferir, enturmar, emitir protocolo | Efetivar sem contrato e sem documento do responsável, quando exigidos | E |
| **Coordenação pedagógica** | Aprovar trancamento até o prazo do regimento, aprovar reopção e aproveitamento | Aprovar trancamento acima do prazo sem a secretaria | E |

Do [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Aprovar grade, abrir e encerrar turma, ver ocupação da unidade | Alterar grade publicada sem nova versão | E |
| **Coordenação** | Montar turmas, enturmar, montar e publicar grade, autorizar troca de professor | Publicar grade com conflito | E |
| **Secretaria** | Enturmar com autorização, cadastrar sala de referência, consultar grade | Criar turma ou aula | E |

## 5. Papéis

- `unit.secretary`: enturmar com autorização.
- `unit.coordinator`: montar turmas e autorizar.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Vaga com bloqueio de concorrência (M-03); turma encerrada não recebe aluno ([60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), seção 2.3).

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

### 13.1 [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-03

##### M-03 Vaga com reserva e bloqueio de concorrência

Já definido em [15](../../../docs/v2/15-validacoes.md), seção 7. A vaga é reservada na transação de confirmação. Duas confirmações simultâneas para a última vaga resultam em uma matrícula e uma `lista_espera`.

### 13.2 [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-07

##### M-07 Transferência e enturmação

- Transferência de turma dentro da mesma unidade: aprovada pela coordenação, com verificação de vaga e de pré-requisito.
- Transferência entre unidades da mesma entidade: exige matrícula nova na unidade de destino, com histórico transferido por registro, não por cópia.
- Enturmação: lista de alunos por turma, gerada pela secretaria, com vagas e bloqueio pela regra de M-03.

### 13.3 [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), seção 2.4

##### 2.4 Enturmação

- Aluno matriculado é enturmado em uma turma da própria grade vigente ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 3.3).
- Enturmação passa da capacidade? Recusada. Vai para lista de espera ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 4).
- Transferência de turma segue M-07 de [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), com aprovação da coordenação.
