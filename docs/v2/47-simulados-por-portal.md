# 47 — Simulados e Correção de Redação, por Portal

> Parte do [SDD v2](00-README.md). Matriz em [31](31-matriz-portais-modulos.md), seção 2, e pendências MOD-05, MOD-06 e MOD-08. Gateway de IA e regras de nota por IA em [27](27-inteligencia-artificial-e-portais.md). Formulários de pesquisa em [41](41-formularios-e-pesquisas.md). Agendamento de sala de prova em [44](44-agendamento-ambientes-equipamentos.md). Dado de aluno e de menor em [07](07-privacidade-lgpd.md). Armazenamento de redação e imagem em [21](21-busca-e-armazenamento.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026 a partir de [`spec_gestao_simulados_ia.md`](anexo-v1/spec_gestao_simulados_ia.md) (v1, seções de escopo, perfis, fluxo, correção, OCR e automações). Fecha MOD-08 da [31](31-matriz-portais-modulos.md). Itens **[Decisão do autor]** e **(jurídico)** dependem de resposta.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| O simulado está completo? | **Em parte.** A v1 tem escopo, perfis (ENEM, MEC, Harvard, custom), fluxo, OCR, correção por IA, rubricas, kanban e relatórios. Não tem estados, DDL, nem regra de quem publica e de quem confirma a nota |
| Há conflito com regra da v2? | **Sim.** A v1 gera "nota final estimada" pela IA. A v2 decide que a IA sugere e o professor confirma (MOD-06) |
| Está organizado por portal? | **Não.** A v1 não diz o que o aluno vê antes e depois da correção |
| Há item excluído? | **Sim.** Proctoring com biometria e reconhecimento facial estão fora do escopo, conforme a v1 e a regra de [35](35-acesso-e-seguranca-fisica-por-portal.md) |

---

## 2. Decisões já tomadas que se aplicam aqui

- **MOD-05 (decidido):** o plano PRO libera correção por IA e ranking. O plano básico tem simulado e gabarito.
- **MOD-06 (decidido):** a IA sugere nota e feedback. O professor e a coordenação pedagógica confirmam. Nada chega ao aluno sem aprovação.
- **MOD-04 (decidido):** gabarito óptico pode ser próprio ou de terceiro, por configuração da entidade.

---

## 3. Perfis de prova

| Perfil | Uso | Regra |
|---|---|---|
| ENEM | Preparação com estrutura do exame, redação dissertativo-argumentativa e competências | Rubrica e competências do perfil, versionadas. Tema central obrigatório |
| MEC | Correção rápida, com envio por foto ou PDF | Mesma estrutura de envio, rubrica simplificada |
| Harvard | Redação analítica longa | Rubrica própria, com peso maior para profundidade crítica |
| Custom | Vestibular, concurso, curso interno | Entidade cria a rubrica. Sem nome de exame oficial sem direito de uso |

Perfil publicado não muda. Mudança gera nova versão, como em [41](41-formularios-e-pesquisas.md), seção 2.3.

---

## 4. Estados

**Simulado:** `rascunho` → `publicado` → `em_aplicacao` → `encerrado` → `arquivado`.

**Redação:** `enviada` → `ocr_em_andamento` → `ocr_concluido` ou `revisao_ocr` → `em_correcao_ia` → `sugerida_pela_ia` → `em_revisao_professor` → `confirmada` ou `devolvida`.

- `revisao_ocr`: confiança baixa ou página ilegível. Pede novo envio ou leitura manual.
- `devolvida`: o professor pede reprocessamento ou nova entrega. Registrada com motivo.
- Prazo vencido é calculado, não gravado ([18](18-regras-modulos-2.md), T-04).

---

## 5. Entrada: envio, OCR e fallback

| Etapa | Regra |
|---|---|
| Upload | Imagem, PDF digitalizado, PDF com texto selecionável, ou texto digitado. Tamanho e tipo são validados na entrada ([21](21-busca-e-armazenamento.md)) |
| Conversão | PDF é separado em páginas. Cada página guarda a ordem |
| OCR | Motor de código aberto com versão fixada, em ADR próprio, como na [21](21-busca-e-armazenamento.md), seção 3.10 |
| Confiança | Abaixo do limite configurável, a redação vai para `revisao_ocr`. Limite padrão a definir (SIM-03) |
| Falha em várias páginas | Abre ticket de análise no atendimento ([32](32-atendimento-privacidade-por-portal.md)) |

**Dado do aluno na imagem:** a foto da redação pode conter nome e documento do aluno. O sistema recorta o cabeçalho e guarda o nome só como vínculo, não no texto enviado à IA.

---

## 6. Correção por IA

### Entrada enviada ao gateway

- Texto transcrito, sem nome e sem identificador do aluno.
- Rubrica ativa e perfil de prova.
- Tema.

Histórico do aluno não é enviado. A comparação com o histórico é feita pelo sistema, depois da resposta.

### Saída guardada

- Nota por competência e nota total **sugerida**. A v1 chama de "nota final estimada". Na v2 o nome é **nota sugerida**.
- Feedback textual por competência.
- Alerta de fuga do tema e de incoerência.
- Versão do modelo e do prompt, e o hash da entrada.

### Regras

- A IA não grava nota final. Só o professor ou a coordenação confirma ([27](27-inteligencia-artificial-e-portais.md)).
- Reprocessamento com prompt revisado cria nova versão, sem apagar a anterior.
- Toda chamada passa pelo gateway de IA, com registro ([27](27-inteligencia-artificial-e-portais.md), seção 3).

---

## 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar perfis-modelo, sem dado de aluno | Ver redação ou nota de qualquer entidade | P |
| **Gestão** | Criar perfil custom, ver relatórios agregados, ver kanban da unidade, exportar com auditoria | Ver redação individual sem papel de correção. Alterar nota confirmada sem motivo | E |
| **Professor** | Montar simulado para a própria turma, publicar, revisar sugestão da IA, confirmar ou devolver nota, ver relatório da turma | Ver simulado ou redação de outra turma. Confirmar a própria redação, se for aluno | E |
| **Coordenação pedagógica** | Ver relatório consolidado, confirmar nota em revisão, aprovar reprocessamento | Editar questão de simulado já publicado | E |
| **Aluno** | Enviar redação dentro do prazo, ver a nota e o feedback depois de confirmados. Ver o próprio ranking, se a unidade publicar | Ver nota da IA antes da confirmação. Ver redação de colega. Ver ranking nominal de colegas sem opção da unidade | E |
| **Responsáveis** | Ver a nota confirmada do dependente e o relatório do simulado | Ver redação do dependente com dado de terceiro. Ver outro aluno | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada, por padrão | Ver simulado, redação ou nota | E, [38](38-portal-de-terceiros-prestadores.md) |

**Aluno e nota da IA:** a regra de MOD-06 vale para qualquer nota. A IA nunca aparece ao aluno como nota.

---

## 8. Relatórios e ranking

- Relatório por competência, por turma e por unidade, com média e distribuição. Abaixo do mínimo de respostas da [41](41-formularios-e-pesquisas.md), seção 3, o grupo não aparece.
- Ranking é do plano PRO (MOD-05). Mostra posição com nome só se a unidade permitir. O padrão é não expor nome de colega.
- Exportação de notas gera evento de auditoria ([29](29-auditoria.md)).

---

## 9. Automações

- Publicar simulado: aviso à turma, com data de abertura e fechamento.
- Receber redação: OCR automático.
- Concluir OCR com confiança suficiente: correção por IA.
- Confiança baixa: `revisao_ocr` e aviso ao professor.
- Confirmar nota: aviso ao aluno.
- Nota abaixo da meta da rubrica: trilha de reforço, com sugestão de atividade para o professor aprovar.
- Encerrar simulado: relatório consolidado.

---

## 10. Retenção e segurança

- Redação original (imagem e PDF) segue o prazo de guarda de documentos escolares, a definir **(jurídico)**.
- Texto transcrito segue o mesmo prazo.
- Sem proctoring biométrico e sem reconhecimento facial, como na v1.
- Gravação de vídeo de prova é fora do escopo.

---

## 11. Pendências

| # | Pendência | Tipo |
|---|---|---|
| SIM-01 | Prazo de guarda de redação original e de transcrição (seção 10) | (jurídico) |
| SIM-02 | Uso de nome de exame oficial (ENEM e outros) no perfil, e a permissão de uso | (jurídico) |
| SIM-03 | Limite padrão de confiança do OCR, abaixo do qual vai para revisão | **Decidido** em 03/11/2026: 80% |
| SIM-04 | Ranking (seção 8) | **Decidido** em 03/11/2026: vários tipos de ranking e de análise, escolhidos pela unidade. Nome do aluno aparece só no ranking da própria turma |
| SIM-05 | Quem aprova a trilha de reforço após nota baixa | **Decidido** em 03/11/2026: a escola configura. Pode ser o professor, a coordenação ou os dois. Prazo padrão de 15 dias para refazer a atividade, ajustável pela escola |
| SIM-06 | Nomenclatura da nota da IA | **Decidido** em 03/11/2026: "nota sugerida", para professor e aluno |
| SIM-07 | DDL de simulado, perfil, questão, redação, OCR, correção e rubrica | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.19. Revisão do owner pendente (DDL-01) |

---

## 12. Critérios de aceite

- [ ] Aluno não vê nota sugerida pela IA antes da confirmação (teste).
- [ ] Nota confirmada não muda sem motivo e sem evento de auditoria (teste).
- [ ] Texto enviado ao gateway não contém nome nem identificador do aluno (varredura).
- [ ] Redação de uma turma não aparece para professor de outra turma (teste de isolamento).
- [ ] OCR com confiança abaixo do limite vai para `revisao_ocr` (teste).
- [ ] Ranking não mostra nome de colega sem a opção da unidade (teste).
- [ ] Itens **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
