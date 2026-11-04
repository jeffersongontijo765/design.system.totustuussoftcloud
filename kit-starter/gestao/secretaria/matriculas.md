# Matrículas

- Portal: Gestão (`gestao.`)
- Área: Secretaria
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) (integral); [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.5; [17](../../../docs/v2/17-regras-modulos.md), seção 4
- Fonte da v1: absorvida integralmente em [administracao-escolar-estrutura-academica.md](../academico/administracao-escolar-estrutura-academica.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Conduzir a matrícula do ingresso à efetivação: pedido (wizard ou balcão), análise de documentos e pagamento, matrícula condicional com prazo, contrato assinado e efetivação, com vaga reservada e bloqueio de concorrência.

## 3. Telas

- **Matrículas** (DataTable e kanban por estado): `lista_espera`, `solicitada`, `em_analise`, `condicional`, `ativa`, `trancada`, `transferida`, `concluida`, `cancelada`, `nao_rematriculada`.
- **Nova matrícula — balcão** (wizard em etapas, igual ao do portal, M-02): aluno e responsável (busca por CPF antes de cadastrar, alerta de duplicidade), turma e eletivas, documentos, plano financeiro, contrato e aceite de LGPD, primeira parcela.
- **Análise** (página): checklist de documentos por tipo (M-08), situação financeira, decisão `ativa`, `condicional` (com prazo) ou `cancelada` com motivo.
- **Condicionais a vencer** (lista com prazo e aviso).
- **Trancamento** (fluxo com motivo, aprovação por níveis e protocolo, M-06).
- **Painel de matrículas** (dashboard): vagas por turma, ocupação, condicionais, lista de espera.

## 4. Permissões por portal (extraídas do SDD)

Do [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Abrir e fechar janela de rematrícula, ver kanban, aprovar trancamento acima do prazo, emitir declaração, cancelar matrícula com motivo | Alterar matrícula ativa sem registro de motivo. Ver documento de saúde sem o papel do módulo | E |
| **Secretaria** | Analisar, condicionar, efetivar, transferir, enturmar, emitir protocolo | Efetivar sem contrato e sem documento do responsável, quando exigidos | E |
| **Coordenação pedagógica** | Aprovar trancamento até o prazo do regimento, aprovar reopção e aproveitamento | Aprovar trancamento acima do prazo sem a secretaria | E |

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Teste de isolamento | Teste de permissão | Teste de fluxo principal | Teste de acessibilidade |
|---|---|---|---|---|
| Gestão | Cross-tenant e cross-unidade | Papel sem permissão não vê o módulo | Matrícula, cobrança, emissão de documento | Telas principais |

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Autenticação | Sessão | Dados e restrições especiais |
|---|---|---|---|
| Gestão | Senha e MFA conforme política da entidade ([06](../../../docs/v2/06-identidade-acesso.md), seção 5) | Padrão | Consulta por CPF com finalidade ([21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6.8) |

## 5. Papéis

- `unit.secretary`: matrícula, análise, trancamento (até a alçada), enturmação.
- `unit.coordinator`: aprova trancamento até o prazo do regimento; transferência de turma.
- `unit.manager`: trancamento acima do prazo (com a secretaria), liberar vaga de não rematriculado.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Um vínculo ativo por aluno e turma; vaga reservada na transação de confirmação; empate na última vaga gera uma matrícula e uma `lista_espera` ([15](../../../docs/v2/15-validacoes.md), seção 7).
- Condicional vencida vira `cancelada` por job com aviso e registro; a vaga volta à lista de espera (M-04).
- Sem contrato e termo de LGPD assinados, não passa de `em_analise` (M-08).
- Inadimplente de outro período mantém acesso à rematrícula e documentação ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 3).

## 7. Dados

- Tabelas e campos conforme a seção 13 e o DDL do [51](../../../docs/v2/51-ddl-modulos-novos.md), quando o módulo estiver lá. Toda tabela tem `entidade_id`, `unidade_id`, `created_at`, `updated_at`, `created_by` e exclusão lógica com `deleted_at` e `deleted_by` ([03](../../../docs/v2/03-dominio-tenancy.md), seção 6; [15](../../../docs/v2/15-validacoes.md); [19](../../../docs/v2/19-regras-modulos-3.md), seção 14).

## 8. Integrações

- Contrato e assinatura ([33](../../../docs/v2/33-contratos-por-portal.md), seção 5); gateway da unidade ([34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md)); enturmação ([60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), seção 2.4); CRM do tenant para candidatos ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 4.2); notificações ([57](../../../docs/v2/57-notificacoes-por-portal.md)).

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

### 13.1 [46 — Matrícula e Rematrícula, por Portal (Acadêmico)](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Matriz em [31](../../../docs/v2/31-matriz-portais-modulos.md). Regras de validação de matrícula em [15](../../../docs/v2/15-validacoes.md), seção 7, e em [17](../../../docs/v2/17-regras-modulos.md), seção 4. Bloqueio parcial por inadimplência em [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 3. Contrato de matrícula em [33](../../../docs/v2/33-contratos-por-portal.md). Pagamento da matrícula em [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md). Protocolo de atendimento em [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md). Documentos exigidos e LGPD em [07](../../../docs/v2/07-privacidade-lgpd.md). Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026 a partir de [`spec_gestao_academica_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_academica_completo.md) (seções 4.1 a 4.9 e 4.3 do portal online). Fecha M-01 a M-09 da [31](../../../docs/v2/31-matriz-portais-modulos.md). Itens **(jurídico)** e **[Decisão do autor]** dependem de resposta.

---

#### 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| A matrícula está completa na v1? | **Em parte.** Tem telas (lista, wizard de 6 etapas, portal online, processo seletivo, lista de espera, trancamento, reopção, aproveitamento e atividades complementares). Não tem estados, regra de transição nem DDL completo |
| Está organizada por portal? | **Parcialmente.** O portal online existe. A v1 não diz o que o responsável vê antes e depois da matrícula, nem o que a secretaria pode alterar depois de ativa |
| Há conflito de regra? | **Sim.** "CPF único por tenant" (v1) está errado: a regra é por entidade, com banco por unidade ([03](../../../docs/v2/03-dominio-tenancy.md)). Trancamento "conforme regimento" não tem valor |
| Rematrícula está especificada? | **Não.** A v1 só cita "Rematrícula Online" na navegação e um aviso de 30 dias. M-01 a M-05 não têm regra |

---

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

---

#### 3. Regras por item da matriz

##### M-01 Janela de rematrícula por série e unidade

- A unidade define a janela por série e por curso: abertura, fechamento e prazo de confirmação.
- Fora da janela, a rematrícula não aceita confirmação. A tela informa a data de abertura.
- Kanban de rematrícula na gestão: `não iniciada`, `em preenchimento`, `confirmada`, `em pendência`, `não rematriculada`.

##### M-02 Wizard do responsável ou aluno

Etapas do portal, em ordem: dados do aluno e do responsável; escolha de turma e eletivas; documentos; plano financeiro; contrato e aceite de LGPD; pagamento da primeira parcela. Cada etapa salva e pode ser retomada.

- Aluno maior de idade faz o próprio wizard. Menor é feito pelo responsável com vínculo ativo.
- Eletiva só aparece se a grade do curso tiver vaga e pré-requisito cumprido.

##### M-03 Vaga com reserva e bloqueio de concorrência

Já definido em [15](../../../docs/v2/15-validacoes.md), seção 7. A vaga é reservada na transação de confirmação. Duas confirmações simultâneas para a última vaga resultam em uma matrícula e uma `lista_espera`.

##### M-04 Matrícula condicional com prazo e expiração

- Condicional é aceita com pendência financeira ou documental, e recebe prazo de regularização configurável por unidade.
- Ao vencer o prazo, a matrícula vai para `cancelada` por job, com aviso ao responsável e registro. A vaga volta para a lista de espera.
- Condicional não dá acesso ao contrato de turma até a regularização. Dá acesso à documentação pendente e ao pagamento.

##### M-05 Não rematriculado após 30 dias

- Aluno ativo que não confirmou rematrícula até o fim da janela, mais 30 dias, vai para `nao_rematriculada`.
- Aviso ao responsável em até 2 dias úteis após o fim da janela, e novo aviso aos 30 dias.
- Não é cancelamento. A vaga só é liberada com decisão da secretaria.

##### M-06 Trancamento com motivo, aprovação por níveis e protocolo

- Motivo escolhido na lista (pessoal, financeiro, saúde, militar, outro), com texto complementar quando for "outro".
- Aprovação por níveis: coordenação pedagógica para trancamento até o prazo do regimento, e secretaria mais direção acima desse prazo.
- Gera protocolo. O prazo máximo do trancamento vem do regimento de cada curso (pendência abaixo).
- Trancamento com dado de saúde segue o acesso restrito de [43](../../../docs/v2/43-pastoral-por-portal.md), seção 2.2, e não aparece no portal de terceiros.

##### M-07 Transferência e enturmação

- Transferência de turma dentro da mesma unidade: aprovada pela coordenação, com verificação de vaga e de pré-requisito.
- Transferência entre unidades da mesma entidade: exige matrícula nova na unidade de destino, com histórico transferido por registro, não por cópia.
- Enturmação: lista de alunos por turma, gerada pela secretaria, com vagas e bloqueio pela regra de M-03.

##### M-08 Documento obrigatório pendente

Proposta, por tipo de documento:

| Tipo | Efeito de pendência |
|---|---|
| Documento de identidade do aluno e do responsável | Matrícula fica `condicional`, com prazo |
| Histórico escolar anterior (para série final ou transferência) | Matrícula fica `condicional`, com prazo |
| Comprovante de vacinação, quando exigido pela norma da unidade | Matrícula fica `condicional`, com prazo |
| Termo de LGPD e contrato | Sem assinatura, a matrícula não passa de `em_analise` |

**(jurídico):** lista de documentos obrigatórios por nível de ensino e se algum pode bloquear, e não apenas condicionar.

##### M-09 Assinatura do contrato e pagamento da primeira parcela

- Contrato de matrícula é gerado no wizard e assinado pelo responsável (menor) ou pelo aluno (maior), com o provedor de assinatura da [33](../../../docs/v2/33-contratos-por-portal.md), seção 4.
- Primeira parcela é cobrada pelo gateway da unidade ([34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md)). Sem pagamento, a matrícula fica `condicional`, com o prazo da M-04.
- Inadimplente de outro período continua com acesso à rematrícula, à documentação e à comunicação com a família, pelo bloqueio parcial de [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 3.

---

#### 4. Processo seletivo e lista de espera

Mantidos da v1 (4.4 e 4.5), com estas regras:

- Candidato em lista de espera recebe aviso quando abrir vaga, com prazo de resposta configurável (48 horas na v1).
- Sem resposta no prazo, o candidato vai para `cancelada` e a vaga passa ao próximo, em ordem de prioridade.
- Ordem de prioridade: data de inscrição, nota, cota ou critério manual, configurável por processo.
- Cota de vaga é campo do processo, com regra de comprovação documental ([17](../../../docs/v2/17-regras-modulos.md), seção 4).

---

#### 5. Reopção, aproveitamento e atividades complementares

Mantidos da v1 (4.7 a 4.9). Regras de estado:

- **Reopção de curso:** nova matrícula vinculada à anterior. A anterior vai para `transferida`.
- **Aproveitamento de estudos:** cada disciplina tem estado `aproveitada`, `não aproveitada` ou `pendente`. O parecer é emitido pelo coordenador e vira documento da secretaria ([17](../../../docs/v2/17-regras-modulos.md)).
- **Atividade complementar:** `pendente_validacao`, `validada` ou `recusada`. Só horas validadas contam para a conclusão.

---

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

---

#### 7. Modelo de dados proposto

Não é o DDL final. Tabelas no banco da unidade, horários em UTC.

| Tabela | Campos principais |
|---|---|
| `matriculas` | `uuid`, `aluno_uuid`, `turma_uuid`, `periodo_letivo`, `tipo` (regular, especial, transferencia, condicional, ead), `estado`, `solicitada_em`, `prazo_regularizacao_em`, `motivo_estado`, `created_by`. Unicidade de vínculo ativo por aluno e período |
| `matricula_pendencias` | `matricula_uuid`, `tipo` (financeira, documental), `documento_tipo`, `prazo_em`, `resolvida_em` |
| `janelas_rematricula` | `unidade_uuid`, `serie`, `curso_uuid`, `abre_em`, `fecha_em`, `prazo_confirmacao_dias` |
| `trancamentos` | `matricula_uuid`, `motivo`, `descricao`, `solicitado_em`, `retorno_previsto_em`, `estado`, `protocolo_uuid` |
| `transferencias` | `matricula_origem_uuid`, `matricula_destino_uuid`, `tipo` (turma, curso, unidade), `aprovado_por`, `aprovado_em` |
| `vagas_reserva` | `turma_uuid`, `matricula_uuid`, `reservada_em`, `expira_em`. Índice único em (`turma_uuid`, `matricula_uuid`) |
| `lista_espera` | `processo_uuid`, `candidato_uuid`, `prioridade`, `estado`, `notificado_em`, `expira_em` |

Regra: `vagas_reserva` é o que impede concorrência. A confirmação de matrícula consome a vaga dentro de transação com bloqueio da turma.

---

#### 8. Pendências

| # | Pendência | Tipo |
|---|---|---|
| MAT-01 | Lista de documentos obrigatórios por nível e se algum pode bloquear, não só condicionar (M-08) | (jurídico) |
| MAT-02 | Prazo máximo de trancamento (M-06) | **Decidido** em 03/11/2026: um ano letivo, configurável por curso |
| MAT-03 | Prazo de regularização de matrícula condicional (M-04) | **Decidido** em 03/11/2026: 15 dias, ajustável por unidade |
| MAT-04 | Aviso de não rematrícula: 2 dias úteis após a janela e 30 dias depois (M-05) | **Decidido** em 03/11/2026 |
| MAT-05 | "CPF único por tenant" da v1 passa a ser "CPF único por entidade", com verificação entre unidades ([03](../../../docs/v2/03-dominio-tenancy.md)) | **Decidido** em 03/11/2026 |
| MAT-06 | Níveis de aprovação de trancamento: coordenação até o regimento, secretaria e direção acima (M-06) | **Decidido** em 03/11/2026 |
| MAT-07 | DDL das tabelas da seção 7, com teste de concorrência em vagas | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 10. Revisão do owner pendente (DDL-01) |

---

#### 9. Critérios de aceite

- [ ] Duas confirmações simultâneas para a última vaga geram uma matrícula e uma `lista_espera` (teste de concorrência).
- [ ] Matrícula condicional vencida vai para `cancelada` e libera a vaga (teste).
- [ ] Rematrícula fora da janela é recusada com a data de abertura (teste).
- [ ] Aluno sem vínculo ativo não vê matrícula de outro aluno (teste de isolamento).
- [ ] Responsável vê só dependentes com vínculo ativo (teste de isolamento).
- [ ] Inadimplente de outro período mantém rematrícula, documentação e comunicação (teste, conforme [26](../../../docs/v2/26-sdd-juridico-regulatorio.md)).
- [ ] Trancamento gera protocolo e registro de aprovação por nível (teste).
- [ ] Itens **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).

### 13.2 [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.5

##### 3.5 Matrícula e rematrícula

A v2 tem só os estados da matrícula em [17](../../../docs/v2/17-regras-modulos.md) (`pre_matricula`, `ativa`, `trancada`, `concluida`, `cancelada`, `transferida`). A v1 ([`spec_gestao_academica_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_academica_completo.md)) tem mais: kanban de rematrícula, wizard, prazo de 7 dias, lembrete, "não rematriculado" após 30 dias, matrícula condicional com prazo e trancamento com motivo e protocolo.

**Lacunas do fluxo, a incluir na v2:**

| # | Passo ou regra | Origem na v1 | Estado na v2 |
|---|---|---|---|
| M-01 | Janela de rematrícula por série e unidade, com abertura e fechamento | Acadêmico, kanban | Não definido |
| M-02 | Wizard do responsável ou aluno: dados, documentos, escolha de turma e eletivas, contrato, pagamento | Portal dos responsáveis e do aluno | Não definido |
| M-03 | Vaga com reserva e bloqueio de concorrência | [15](../../../docs/v2/15-validacoes.md), seção 7 | Definido |
| M-04 | Matrícula condicional com prazo e expiração | Ações automáticas, v1 linha 1181 | Não definido |
| M-05 | Não rematriculado após 30 dias: estado e aviso | Ações automáticas, v1 linha 1175 | Não definido |
| M-06 | Trancamento com motivo, aprovação por níveis e protocolo | Requerimentos, v1 seção 15 | Não definido |
| M-07 | Transferência e enturmação | Secretaria digital | Não definido |
| M-08 | Documento obrigatório pendente bloqueia a matrícula? Regra por tipo | v1 linha 1176 | Não definido. Ver [26](../../../docs/v2/26-sdd-juridico-regulatorio.md) |
| M-09 | Assinatura do contrato de matrícula e pagamento da primeira parcela | Portal dos responsáveis | Parcial em [20](../../../docs/v2/20-pagamentos-seguranca.md) |

### 13.3 [17](../../../docs/v2/17-regras-modulos.md), seção 4

#### 4. Acadêmico

##### 4.1 Entidades

Matrícula, aluno, turma, disciplina, diário, avaliação, plano de aula, plano de ensino, conselho de classe, estágio, documentos da secretaria, presença (22 tabelas na v1).

##### 4.2 Campos e regras (v1, seções 4 a 9)

| Campo | Regra |
|---|---|
| CPF do aluno ou candidato | Único por tenant. Busca antes de cadastrar; alerta de matrícula duplicada (v1, seção 4.2). |
| Documentos pessoais | Versionados, com data de upload, validade, responsável e hash de integridade (v1, seção 5). |
| Matrícula | Um vínculo ativo por aluno e turma. Vaga disponível com bloqueio de concorrência ([15](../../../docs/v2/15-validacoes.md), seção 7). |
| Trancamento | Prazo máximo de um ano letivo, configurável por curso. Decidido pelo autor em 03/11/2026 ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), MAT-02). |
| Nota | Dentro da faixa do método de avaliação; período de lançamento aberto. |
| Presença por QR Code | Válido por 5 minutos por padrão, configurável pela escola. Decidido pelo autor em 03/11/2026. Geolocalização só com consentimento, conforme [07](../../../docs/v2/07-privacidade-lgpd.md). |
| Horas de atividade complementar | Status `pendente_validacao`, `validado`, `recusado`. Total validado nunca ultrapassa o limite do curso. |
| Estágio | CNPJ válido da empresa concedente. Apólice de seguro com validade. |
| Protocolo de atendimento | Consulta pública por número e CPF, sem login, com limite de tentativas. |

##### 4.3 Estados

| Entidade | Estados |
|---|---|
| Matrícula | `pre_matricula`, `ativa`, `trancada`, `concluida`, `cancelada`, `transferida` |
| Diário | `aberto`, `fechado`, `reaberto` (com justificativa) |
| Estágio | `solicitado`, `ativo`, `concluido`, `cancelado` |

##### 4.4 Segurança específica

- Dados de aluno menor de idade: acesso do responsável legal, com vínculo verificado ([07](../../../docs/v2/07-privacidade-lgpd.md), seção 1).
- Diário e notas: professor vê só as turmas em que está vinculado.
