# Transferências

- Portal: Gestão (`gestao.`)
- Área: Secretaria
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 2; [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-07; [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 5
- Fonte da v1: absorvida integralmente em [administracao-escolar-estrutura-academica.md](../academico/administracao-escolar-estrutura-academica.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Transferir aluno de turma na mesma unidade, entre unidades da mesma entidade e para fora da entidade, com histórico por registro e documentos de transferência.

## 3. Telas

- **Transferências** (DataTable): tipo (turma, unidade, externa), origem, destino, estado.
- **Nova transferência** (formulário): verificação de vaga e pré-requisito, aprovação da coordenação.
- **Transferência entre unidades** (fluxo): nova matrícula no destino com histórico transferido por registro.
- **Transferência externa** (emissão de histórico e declaração pelo [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md)).
- **Reopção e aproveitamento de estudos** (seção 13, 5).

## 4. Permissões por portal (extraídas do SDD)

Do [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Abrir e fechar janela de rematrícula, ver kanban, aprovar trancamento acima do prazo, emitir declaração, cancelar matrícula com motivo | Alterar matrícula ativa sem registro de motivo. Ver documento de saúde sem o papel do módulo | E |
| **Secretaria** | Analisar, condicionar, efetivar, transferir, enturmar, emitir protocolo | Efetivar sem contrato e sem documento do responsável, quando exigidos | E |
| **Coordenação pedagógica** | Aprovar trancamento até o prazo do regimento, aprovar reopção e aproveitamento | Aprovar trancamento acima do prazo sem a secretaria | E |

## 5. Papéis

- `unit.secretary`: registrar e emitir documentos.
- `unit.coordinator`: aprovar transferência de turma.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Transferência entre unidades exige matrícula nova no destino; o histórico é transferido por registro, não por cópia (M-07).
- Estado `transferida` na origem ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 2).

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

### 13.1 [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 2

#### 2. Estados da matrícula

| Estado | Significado | Entra por |
|---|---|---|
| `lista_espera` | Candidato sem vaga, na ordem de prioridade | Pré-matrícula (4.5 da v1) |
| `solicitada` | Pedido feito, aguardando análise | Wizard ou portal online |
| `em_analise` | Documentos ou pagamento em verificação | Secretaria |
| `condicional` | Aceita com pendência financeira ou documental e prazo para regularizar | Análise |
| `ativa` | Matrícula efetivada, com contrato assinado | Análise ou condicional regularizada |
| `trancada` | Suspensa a pedido, com prazo de retorno | Trancamento aprovado |
| `transferida` | Saiu para outra turma ou unidade | Transferência |
| `concluida` | Ciclo encerrado | Conclusão |
| `cancelada` | Desistência ou não regularização | Pedido ou expiração |
| `nao_rematriculada` | Aluno ativo que não confirmou a rematrícula dentro do prazo | Job diário (M-05) |

**Transições:** `solicitada` → `em_analise` → `ativa` ou `condicional` ou `cancelada`. `condicional` → `ativa` ou `cancelada` (ao vencer o prazo). `ativa` → `trancada`, `transferida`, `concluida` ou `cancelada`. `trancada` → `ativa` (retorno) ou `cancelada`.

Estado calculado não é gravado. Prazo vencido de condicional é calculado por data e vira `cancelada` por job, com registro ([18](../../../docs/v2/18-regras-modulos-2.md), T-04).

### 13.2 [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-07

##### M-07 Transferência e enturmação

- Transferência de turma dentro da mesma unidade: aprovada pela coordenação, com verificação de vaga e de pré-requisito.
- Transferência entre unidades da mesma entidade: exige matrícula nova na unidade de destino, com histórico transferido por registro, não por cópia.
- Enturmação: lista de alunos por turma, gerada pela secretaria, com vagas e bloqueio pela regra de M-03.

### 13.3 [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 5

#### 5. Reopção, aproveitamento e atividades complementares

Mantidos da v1 (4.7 a 4.9). Regras de estado:

- **Reopção de curso:** nova matrícula vinculada à anterior. A anterior vai para `transferida`.
- **Aproveitamento de estudos:** cada disciplina tem estado `aproveitada`, `não aproveitada` ou `pendente`. O parecer é emitido pelo coordenador e vira documento da secretaria ([17](../../../docs/v2/17-regras-modulos.md)).
- **Atividade complementar:** `pendente_validacao`, `validada` ou `recusada`. Só horas validadas contam para a conclusão.
