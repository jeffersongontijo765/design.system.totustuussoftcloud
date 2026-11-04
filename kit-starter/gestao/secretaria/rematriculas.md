# Rematrículas

- Portal: Gestão (`gestao.`)
- Área: Secretaria
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 2; [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-01; [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-02; [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-05; [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 6
- Fonte da v1: absorvida integralmente em [administracao-escolar-estrutura-academica.md](../academico/administracao-escolar-estrutura-academica.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Abrir a janela de rematrícula por série e curso, acompanhar a confirmação das famílias pelo kanban e tratar os não rematriculados.

## 3. Telas

- **Janelas de rematrícula** (lista e formulário por série e curso): abertura, fechamento, prazo de confirmação.
- **Kanban de rematrícula** (M-01): `não iniciada`, `em preenchimento`, `confirmada`, `em pendência`, `não rematriculada`; filtros por série e turma; ação em lote de lembrete.
- **Não rematriculados** (lista, M-05): avisos enviados, decisão de liberar vaga.

## 4. Permissões por portal (extraídas do SDD)

Do [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Abrir e fechar janela de rematrícula, ver kanban, aprovar trancamento acima do prazo, emitir declaração, cancelar matrícula com motivo | Alterar matrícula ativa sem registro de motivo. Ver documento de saúde sem o papel do módulo | E |
| **Secretaria** | Analisar, condicionar, efetivar, transferir, enturmar, emitir protocolo | Efetivar sem contrato e sem documento do responsável, quando exigidos | E |
| **Coordenação pedagógica** | Aprovar trancamento até o prazo do regimento, aprovar reopção e aproveitamento | Aprovar trancamento acima do prazo sem a secretaria | E |

## 5. Papéis

- `unit.secretary`: configurar janela e acompanhar.
- `unit.manager`: liberar vaga de não rematriculado.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Fora da janela, a confirmação é recusada e a tela mostra a data de abertura (M-01).
- Não rematriculado após o fim da janela mais 30 dias; aviso em até 2 dias úteis e aos 30 dias; não é cancelamento (M-05).

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

### 13.2 [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-01

##### M-01 Janela de rematrícula por série e unidade

- A unidade define a janela por série e por curso: abertura, fechamento e prazo de confirmação.
- Fora da janela, a rematrícula não aceita confirmação. A tela informa a data de abertura.
- Kanban de rematrícula na gestão: `não iniciada`, `em preenchimento`, `confirmada`, `em pendência`, `não rematriculada`.

### 13.3 [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-02

##### M-02 Wizard do responsável ou aluno

Etapas do portal, em ordem: dados do aluno e do responsável; escolha de turma e eletivas; documentos; plano financeiro; contrato e aceite de LGPD; pagamento da primeira parcela. Cada etapa salva e pode ser retomada.

- Aluno maior de idade faz o próprio wizard. Menor é feito pelo responsável com vínculo ativo.
- Eletiva só aparece se a grade do curso tiver vaga e pré-requisito cumprido.

### 13.4 [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção M-05

##### M-05 Não rematriculado após 30 dias

- Aluno ativo que não confirmou rematrícula até o fim da janela, mais 30 dias, vai para `nao_rematriculada`.
- Aviso ao responsável em até 2 dias úteis após o fim da janela, e novo aviso aos 30 dias.
- Não é cancelamento. A vaga só é liberada com decisão da secretaria.

### 13.5 [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 6

#### 6. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Nada sobre matrícula de entidade | Ver matrícula, aluno ou responsável | P |
| **Gestão** | Abrir e fechar janela de rematrícula, ver kanban, aprovar trancamento acima do prazo, emitir declaração, cancelar matrícula com motivo | Alterar matrícula ativa sem registro de motivo. Ver documento de saúde sem o papel do módulo | E |
| **Secretaria** | Analisar, condicionar, efetivar, transferir, enturmar, emitir protocolo | Efetivar sem contrato e sem documento do responsável, quando exigidos | E |
| **Coordenação pedagógica** | Aprovar trancamento até o prazo do regimento, aprovar reopção e aproveitamento | Aprovar trancamento acima do prazo sem a secretaria | E |
| **Professor** | Ver a lista da própria turma, após enturmação | Matricular, trancar ou ver documento de matrícula | E |
| **Aluno maior** | Fazer o próprio wizard, rematrícula e eletivas. Ver a própria situação | Ver matrícula de outro aluno. Alterar matrícula ativa | E |
| **Responsável** | Fazer o wizard de dependente, rematrícula, pagamento da primeira parcela e assinatura. Ver a situação de cada dependente | Ver matrícula de outro aluno. Confirmar rematrícula sem vínculo ativo | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada, por padrão | Ver matrícula, aluno ou responsável | E |
