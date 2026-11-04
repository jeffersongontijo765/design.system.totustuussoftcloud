# 46 — Matrícula e Rematrícula, por Portal (Acadêmico)

> Parte do [SDD v2](00-README.md). Matriz em [31](31-matriz-portais-modulos.md). Regras de validação de matrícula em [15](15-validacoes.md), seção 7, e em [17](17-regras-modulos.md), seção 4. Bloqueio parcial por inadimplência em [26](26-sdd-juridico-regulatorio.md), seção 3. Contrato de matrícula em [33](33-contratos-por-portal.md). Pagamento da matrícula em [34](34-pagamentos-fiscal-bancos-por-portal.md). Protocolo de atendimento em [32](32-atendimento-privacidade-por-portal.md). Documentos exigidos e LGPD em [07](07-privacidade-lgpd.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026 a partir de [`spec_gestao_academica_completo.md`](anexo-v1/spec_gestao_academica_completo.md) (seções 4.1 a 4.9 e 4.3 do portal online). Fecha M-01 a M-09 da [31](31-matriz-portais-modulos.md). Itens **(jurídico)** e **[Decisão do autor]** dependem de resposta.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| A matrícula está completa na v1? | **Em parte.** Tem telas (lista, wizard de 6 etapas, portal online, processo seletivo, lista de espera, trancamento, reopção, aproveitamento e atividades complementares). Não tem estados, regra de transição nem DDL completo |
| Está organizada por portal? | **Parcialmente.** O portal online existe. A v1 não diz o que o responsável vê antes e depois da matrícula, nem o que a secretaria pode alterar depois de ativa |
| Há conflito de regra? | **Sim.** "CPF único por tenant" (v1) está errado: a regra é por entidade, com banco por unidade ([03](03-dominio-tenancy.md)). Trancamento "conforme regimento" não tem valor |
| Rematrícula está especificada? | **Não.** A v1 só cita "Rematrícula Online" na navegação e um aviso de 30 dias. M-01 a M-05 não têm regra |

---

## 2. Estados da matrícula

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

Estado calculado não é gravado. Prazo vencido de condicional é calculado por data e vira `cancelada` por job, com registro ([18](18-regras-modulos-2.md), T-04).

---

## 3. Regras por item da matriz

### M-01 Janela de rematrícula por série e unidade

- A unidade define a janela por série e por curso: abertura, fechamento e prazo de confirmação.
- Fora da janela, a rematrícula não aceita confirmação. A tela informa a data de abertura.
- Kanban de rematrícula na gestão: `não iniciada`, `em preenchimento`, `confirmada`, `em pendência`, `não rematriculada`.

### M-02 Wizard do responsável ou aluno

Etapas do portal, em ordem: dados do aluno e do responsável; escolha de turma e eletivas; documentos; plano financeiro; contrato e aceite de LGPD; pagamento da primeira parcela. Cada etapa salva e pode ser retomada.

- Aluno maior de idade faz o próprio wizard. Menor é feito pelo responsável com vínculo ativo.
- Eletiva só aparece se a grade do curso tiver vaga e pré-requisito cumprido.

### M-03 Vaga com reserva e bloqueio de concorrência

Já definido em [15](15-validacoes.md), seção 7. A vaga é reservada na transação de confirmação. Duas confirmações simultâneas para a última vaga resultam em uma matrícula e uma `lista_espera`.

### M-04 Matrícula condicional com prazo e expiração

- Condicional é aceita com pendência financeira ou documental, e recebe prazo de regularização configurável por unidade.
- Ao vencer o prazo, a matrícula vai para `cancelada` por job, com aviso ao responsável e registro. A vaga volta para a lista de espera.
- Condicional não dá acesso ao contrato de turma até a regularização. Dá acesso à documentação pendente e ao pagamento.

### M-05 Não rematriculado após 30 dias

- Aluno ativo que não confirmou rematrícula até o fim da janela, mais 30 dias, vai para `nao_rematriculada`.
- Aviso ao responsável em até 2 dias úteis após o fim da janela, e novo aviso aos 30 dias.
- Não é cancelamento. A vaga só é liberada com decisão da secretaria.

### M-06 Trancamento com motivo, aprovação por níveis e protocolo

- Motivo escolhido na lista (pessoal, financeiro, saúde, militar, outro), com texto complementar quando for "outro".
- Aprovação por níveis: coordenação pedagógica para trancamento até o prazo do regimento, e secretaria mais direção acima desse prazo.
- Gera protocolo. O prazo máximo do trancamento vem do regimento de cada curso (pendência abaixo).
- Trancamento com dado de saúde segue o acesso restrito de [43](43-pastoral-por-portal.md), seção 2.2, e não aparece no portal de terceiros.

### M-07 Transferência e enturmação

- Transferência de turma dentro da mesma unidade: aprovada pela coordenação, com verificação de vaga e de pré-requisito.
- Transferência entre unidades da mesma entidade: exige matrícula nova na unidade de destino, com histórico transferido por registro, não por cópia.
- Enturmação: lista de alunos por turma, gerada pela secretaria, com vagas e bloqueio pela regra de M-03.

### M-08 Documento obrigatório pendente

Proposta, por tipo de documento:

| Tipo | Efeito de pendência |
|---|---|
| Documento de identidade do aluno e do responsável | Matrícula fica `condicional`, com prazo |
| Histórico escolar anterior (para série final ou transferência) | Matrícula fica `condicional`, com prazo |
| Comprovante de vacinação, quando exigido pela norma da unidade | Matrícula fica `condicional`, com prazo |
| Termo de LGPD e contrato | Sem assinatura, a matrícula não passa de `em_analise` |

**(jurídico):** lista de documentos obrigatórios por nível de ensino e se algum pode bloquear, e não apenas condicionar.

### M-09 Assinatura do contrato e pagamento da primeira parcela

- Contrato de matrícula é gerado no wizard e assinado pelo responsável (menor) ou pelo aluno (maior), com o provedor de assinatura da [33](33-contratos-por-portal.md), seção 4.
- Primeira parcela é cobrada pelo gateway da unidade ([34](34-pagamentos-fiscal-bancos-por-portal.md)). Sem pagamento, a matrícula fica `condicional`, com o prazo da M-04.
- Inadimplente de outro período continua com acesso à rematrícula, à documentação e à comunicação com a família, pelo bloqueio parcial de [26](26-sdd-juridico-regulatorio.md), seção 3.

---

## 4. Processo seletivo e lista de espera

Mantidos da v1 (4.4 e 4.5), com estas regras:

- Candidato em lista de espera recebe aviso quando abrir vaga, com prazo de resposta configurável (48 horas na v1).
- Sem resposta no prazo, o candidato vai para `cancelada` e a vaga passa ao próximo, em ordem de prioridade.
- Ordem de prioridade: data de inscrição, nota, cota ou critério manual, configurável por processo.
- Cota de vaga é campo do processo, com regra de comprovação documental ([17](17-regras-modulos.md), seção 4).

---

## 5. Reopção, aproveitamento e atividades complementares

Mantidos da v1 (4.7 a 4.9). Regras de estado:

- **Reopção de curso:** nova matrícula vinculada à anterior. A anterior vai para `transferida`.
- **Aproveitamento de estudos:** cada disciplina tem estado `aproveitada`, `não aproveitada` ou `pendente`. O parecer é emitido pelo coordenador e vira documento da secretaria ([17](17-regras-modulos.md)).
- **Atividade complementar:** `pendente_validacao`, `validada` ou `recusada`. Só horas validadas contam para a conclusão.

---

## 6. Por portal

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

## 7. Modelo de dados proposto

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

## 8. Pendências

| # | Pendência | Tipo |
|---|---|---|
| MAT-01 | Lista de documentos obrigatórios por nível e se algum pode bloquear, não só condicionar (M-08) | (jurídico) |
| MAT-02 | Prazo máximo de trancamento (M-06) | **Decidido** em 03/11/2026: um ano letivo, configurável por curso |
| MAT-03 | Prazo de regularização de matrícula condicional (M-04) | **Decidido** em 03/11/2026: 15 dias, ajustável por unidade |
| MAT-04 | Aviso de não rematrícula: 2 dias úteis após a janela e 30 dias depois (M-05) | **Decidido** em 03/11/2026 |
| MAT-05 | "CPF único por tenant" da v1 passa a ser "CPF único por entidade", com verificação entre unidades ([03](03-dominio-tenancy.md)) | **Decidido** em 03/11/2026 |
| MAT-06 | Níveis de aprovação de trancamento: coordenação até o regimento, secretaria e direção acima (M-06) | **Decidido** em 03/11/2026 |
| MAT-07 | DDL das tabelas da seção 7, com teste de concorrência em vagas | **Escrito** em [51](51-ddl-modulos-novos.md), seção 10. Revisão do owner pendente (DDL-01) |

---

## 9. Critérios de aceite

- [ ] Duas confirmações simultâneas para a última vaga geram uma matrícula e uma `lista_espera` (teste de concorrência).
- [ ] Matrícula condicional vencida vai para `cancelada` e libera a vaga (teste).
- [ ] Rematrícula fora da janela é recusada com a data de abertura (teste).
- [ ] Aluno sem vínculo ativo não vê matrícula de outro aluno (teste de isolamento).
- [ ] Responsável vê só dependentes com vínculo ativo (teste de isolamento).
- [ ] Inadimplente de outro período mantém rematrícula, documentação e comunicação (teste, conforme [26](26-sdd-juridico-regulatorio.md)).
- [ ] Trancamento gera protocolo e registro de aprovação por nível (teste).
- [ ] Itens **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
