# Avaliação de desempenho

- Portal: Gestão (`gestao.`)
- Área: Pessoas e RH
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 4; [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 4
- Fonte da v1: absorvida integralmente em [recursos-humanos.md](../../desenvolvedor/pessoas-da-plataforma/recursos-humanos.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Ciclos de avaliação, metas e PDI dos colaboradores.

## 3. Telas

- **Ciclos** (lista).
- **Avaliações** (formulários e consolidação).
- **PDI** (planejamento de desenvolvimento, [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 4).

## 4. Permissões por portal (extraídas do SDD)

Do [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md):

| Portal | Departamento pessoal | Recursos humanos | Medicina e SST |
|---|---|---|---|
| Gestão | Completo, por permissão ([17](../../../docs/v2/17-regras-modulos.md), seção 3) | Completo, por permissão | Apto, inapto, restrição, EPI, NR, CAT, afastamento. **Sem CID nem prontuário** |

Do [37](../../../docs/v2/37-planejamento-e-empenho.md):

| Portal | Planejamento acadêmico | Planejamento institucional | Desenvolvimento de pessoas | Empenho |
|---|---|---|---|---|
| Gestão | Completo, por permissão | Completo, por permissão | Completo, por permissão | Completo, para entidade pública, por permissão |

## 5. Papéis

- `unit.hr`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Recursos humanos ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 4).

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

### 13.1 [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 4

#### 4. Recursos humanos

| Submódulo | Estado na v2 | Proposta mínima |
|---|---|---|
| Recrutamento | Ausente | Vaga → candidato → entrevista → aprovação → oferta. Estados por etapa. Candidato sem consentimento para guarda de currículo é descartado ao fim do prazo ([07](../../../docs/v2/07-privacidade-lgpd.md)) |
| Onboarding | Ausente | Checklist de admissão por cargo, com responsável por item. Convite de acesso ao sistema com validade de 72 h ([06](../../../docs/v2/06-identidade-acesso.md)) |
| Desempenho | Ausente | Ciclo, metas e avaliação. Avaliação não altera a nota de desempenho do aluno, nem a folha |
| Clima | Ausente | Pesquisa anônima. Resultado só com mínimo de respostas por grupo, para não identificar pessoa ([19](../../../docs/v2/19-regras-modulos-3.md), seção 11) |
| Treinamento e desenvolvimento | Parcial | Ver [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 4 |
| Movimentação interna | Ausente | Transferência de unidade e de cargo, com histórico. Não apaga o histórico anterior |

### 13.2 [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 4

#### 4. Planejamento de desenvolvimento de pessoas

##### 4.1 Entidades

| Entidade | Função |
|---|---|
| Plano de desenvolvimento | Por colaborador, com período e metas de formação e carreira |
| Ação de formação | Curso, treinamento ou certificação, com carga horária |
| Trilha | Conjunto de ações para um cargo |
| Avaliação de competência | Resultado por competência, vinculado ao ciclo de avaliação de desempenho |

##### 4.2 Estados

Plano: `rascunho` → `pactuado` → `em_execucao` → `concluido`. Pactuado exige assinatura do colaborador e do gestor. Ação de formação: `prevista` → `realizada` → `comprovada`.

##### 4.3 Regras

- Plano sem assinatura do colaborador não entra em execução.
- Ação `realizada` sem comprovante não vira `comprovada`.
- Carga horária comprovada alimenta o registro de formação do colaborador ([18](../../../docs/v2/18-regras-modulos-2.md), seção 3).
- Avaliação de competência não altera nota de desempenho. Os dois são registros separados.
- Dado de saúde ou de afastamento não entra no plano ([07](../../../docs/v2/07-privacidade-lgpd.md), seção 2).
