# 64 — Planos de Ensino e de Aula, por Portal

> Parte do [SDD v2](00-README.md). Sétima lacuna da ordem de [55](55-academico-verificacao-e-lacunas.md), seção 3. Depende de estrutura acadêmica ([59](59-estrutura-academica-por-portal.md), disciplina e sistema avaliativo) e de turma e grade ([60](60-turmas-e-grade-de-horarios-por-portal.md)). O conteúdo realizado é registrado no diário ([61](61-diario-escolar-por-portal.md), seção 2). Geração de rascunho por IA em [27](27-inteligencia-artificial-e-portais.md), seção 5. Aviso de plano pendente em [57](57-notificacoes-por-portal.md). Acervo de bibliografia em [56](56-configuracoes-e-relatorios-lacunas.md), item de biblioteca. Projeto político-pedagógico e PPC em [59](59-estrutura-academica-por-portal.md), seção 3.4 e [37](37-planejamento-e-empenho.md), PLN-01. Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 7 do acadêmico. A v1 tem `lesson_plans` e `teaching_plans` ([`spec_gestao_academica_completo.md`](anexo-v1/spec_gestao_academica_completo.md), seções 7.1 e 7.2). Esta versão corrige um erro da v1: o projeto político-pedagógico (PPP) não é plano de aula.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Plano de ensino tem regra? | **Não.** A v1 tem campos e DDL, sem regra de vigência, versão nem alinhamento com avaliação |
| Plano de aula tem regra? | **Não.** A v1 tem campos, status e um alerta de envio atrasado, sem regra de revisão |
| Fluxo de aprovação? | **Parcial.** A v1 tem professor → coordenação, mas inclui diretor para PPP, que não é plano de aula |
| Ligação com o diário? | **Não.** Só o diário cita "referência ao plano de aula" ([61](61-diario-escolar-por-portal.md), seção 2) |
| Ligação com a avaliação? | **Não.** A v1 tem "avaliações previstas" no plano de aula, sem vínculo com o sistema avaliativo |

---

## 2. Dois documentos, com relação entre eles

```
Plano de ensino (disciplina + turma + período)
   └── unidades ou módulos de conteúdo
         └── Plano de aula (por aula ou por semana)
               └── Aula realizada no diário (o que foi ministrado)
```

- **Plano de ensino** é o compromisso do professor para a disciplina naquela turma e naquele período. É aprovado pela coordenação.
- **Plano de aula** detalha uma aula ou uma semana dentro do plano de ensino. O professor prepara e a coordenação revisa.
- **Aula realizada** é o que foi ministrado, no diário. Pode diferir do plano. A diferença não é erro, mas é registrada.

**PPP fora deste módulo.** O projeto político-pedagógico da escola é um documento institucional, aprovado pelo colegiado, com o PPC de cada curso em [59](59-estrutura-academica-por-portal.md), seção 3.4. A v1 o põe como tipo de plano de aula, com aprovação de diretor. Essa mistura é removida. Ver PLA-01.

---

## 3. Plano de ensino

### 3.1 Campos

| Campo | Regra |
|---|---|
| Disciplina e turma | Vinculados. Um plano por disciplina, turma e período letivo |
| Professor | Quem leciona a disciplina na turma ([60](60-turmas-e-grade-de-horarios-por-portal.md), seção 2.1) |
| Ementa | Vem do catálogo de disciplina ([59](59-estrutura-academica-por-portal.md), seção 3.2). Não é editada no plano |
| Objetivos gerais e específicos | Texto |
| Conteúdo por unidade ou módulo | Lista ordenada. Cada item tem número, título, carga horária prevista e aulas previstas |
| Metodologia | Texto |
| Critérios de avaliação | Avaliações previstas com tipo, peso e data. A soma dos pesos é a do sistema avaliativo ([59](59-estrutura-academica-por-portal.md), seção 4). Diferença bloqueia o envio |
| Bibliografia básica e complementar | Referências. Quando o item existir no acervo, referencia o acervo (item de biblioteca de [55](55-academico-verificacao-e-lacunas.md)) |
| Versão | Número, incrementado a cada aprovação de alteração |

### 3.2 Estados

`rascunho` → `enviado` → `aprovado`, com `devolvido` a partir de `enviado`. Aprovado não é editado: alteração gera nova versão, que volta a `enviado`.

- **Regra de critério:** alteração de critério de avaliação em período `aberto` exige justificativa e aviso aos alunos da turma ([57](57-notificacoes-por-portal.md)).
- **Regra de conteúdo:** alteração de conteúdo já ministrado não é aceita. Só o conteúdo ainda não ministrado muda.

### 3.3 Prazo

- Plano de ensino é enviado antes do início do período letivo. Prazo definido pelo calendário da unidade ([58](58-calendario-e-eventos-por-portal.md)).
- Plano não aprovado até o início do período não bloqueia aula. Gera pendência para a coordenação.

---

## 4. Plano de aula

### 4.1 Campos

| Campo | Regra |
|---|---|
| Plano de ensino | Obrigatório. Plano de aula sem plano de ensino aprovado não é criado |
| Aula ou semana | Ligada à grade ([60](60-turmas-e-grade-de-horarios-por-portal.md), seção 4). Uma aula ou um intervalo de semana |
| Unidade ou módulo do plano de ensino | Obrigatório. O conteúdo vem da unidade |
| Objetivos específicos da aula | Texto |
| Conteúdo previsto | Texto, com link para o conteúdo da unidade |
| Metodologia e recursos | Texto e arquivos. Arquivos seguem [21](21-busca-e-armazenamento.md) |
| Avaliação prevista | Se houver, vira avaliação prevista do diário. Mesmo tipo e peso do plano de ensino |
| Alinhamento com competências | Na educação básica, o currículo tem base nacional comum obrigatória (LDB, art. 26, e art. 9º, IV). **Decidido** em 03/11/2026 (PLA-04): o plano de ensino indica as competências da BNCC; no plano de aula, a indicação é opcional, porque a lei trata do currículo, não de cada aula |

### 4.2 Estados e prazo

`rascunho` → `enviado` → `aprovado`, com `devolvido`.

- **Prazo de envio:** o plano de aula é enviado 5 dias antes da aula, com alerta ao professor e à coordenação. **Decidido** em 03/11/2026, igual à regra da v1 ([`spec_gestao_academica_completo.md`](anexo-v1/spec_gestao_academica_completo.md), linha 1182).
- **Aula sem plano aprovado:** a aula acontece. O sistema registra pendência de planejamento, sem bloquear o diário.

### 4.3 Conteúdo realizado

- O diário registra o conteúdo ministrado ([61](61-diario-escolar-por-portal.md), seção 2). Ele pode ser diferente do plano.
- Conteúdo previsto e não ministrado aparece como pendente no fechamento do período. O professor decide se reagenda para outra aula. Não há reagendamento automático. **Decidido** em 03/11/2026.
- A diferença entre previsto e realizado aparece no relatório de planejamento ([56](56-configuracoes-e-relatorios-lacunas.md), seção 5).

---

## 5. Revisão

- A coordenação aprova ou devolve o plano, com comentário obrigatório na devolução.
- Plano devolvido volta para `rascunho`. O professor responde no próprio plano, sem criar outro.
- Aprovação é registrada com data e pessoa. Fica em auditoria ([29](29-auditoria.md)).
- A coordenação não edita o conteúdo do professor. Ela pode devolver ou aprovar.

---

## 6. Inteligência artificial

- A IA gera rascunho de plano de ensino e de plano de aula a partir da ementa, do material e da grade ([27](27-inteligencia-artificial-e-portais.md), seção 5).
- Rascunho gerado por IA não é enviado sem revisão do professor. Ele é marcado como gerado por IA até o professor aprovar o texto.
- IA não aprova plano.

---

## 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelo de plano de ensino e de aula, sem dado | Ver plano de entidade | P |
| **Gestão** | Ver indicador: planos aprovados por período e por disciplina. Ver pendência de planejamento | Editar ou aprovar plano | E |
| **Coordenação** | Ver todos os planos da unidade. Aprovar ou devolver. Ver pendência de planejamento | Editar conteúdo do professor | E |
| **Secretaria** | Ver status dos planos da unidade | Criar, editar ou aprovar | E |
| **Professor** | Criar e editar os próprios planos enquanto não aprovados. Ver os planos das próprias turmas | Editar plano aprovado sem nova versão. Ver plano de outra disciplina | E |
| **Aluno** | Ver o plano de ensino publicado da própria turma e os planos de aula aprovados: ementa, critérios, cronograma de conteúdo, bibliografia | Ver plano em rascunho ou devolvido | E |
| **Responsáveis** | Ver o plano de ensino publicado do dependente | Ver plano de aula. Ver plano de outra turma | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item de plano | E |

---

## 8. Integrações

| Módulo | Relação |
|---|---|
| Estrutura ([59](59-estrutura-academica-por-portal.md)) | Ementa vem do catálogo. Critérios seguem o sistema avaliativo |
| Turmas e grade ([60](60-turmas-e-grade-de-horarios-por-portal.md)) | Plano de aula liga a aula da grade |
| Diário ([61](61-diario-escolar-por-portal.md)) | Conteúdo realizado e avaliação prevista |
| Calendário ([58](58-calendario-e-eventos-por-portal.md)) | Prazo de envio e período |
| Notificações ([57](57-notificacoes-por-portal.md)) | Aviso de plano devolvido, de plano pendente e de alteração de critério |
| IA ([27](27-inteligencia-artificial-e-portais.md)) | Rascunho com revisão humana |
| Relatórios ([56](56-configuracoes-e-relatorios-lacunas.md)) | Planejado versus ministrado |

---

## 9. Pendências

| # | Pendência | Tipo |
|---|---|---|
| PLA-01 | PPP sai do plano de aula e vai para documento institucional ([59](59-estrutura-academica-por-portal.md), seção 3.4) | **Decidido** em 03/11/2026: sai do plano de aula |
| PLA-02 | Aluno vê o plano de aula aprovado da própria turma (seção 7) | **Decidido** em 03/11/2026: sim |
| PLA-03 | Prazo de envio do plano de aula antes da aula (seção 4.2) | **Decidido** em 03/11/2026: 5 dias antes |
| PLA-04 | Alinhamento com BNCC e DCN na educação básica, e se é obrigatório (seção 4.1) | **Conferido** em 03/11/2026: base nacional comum obrigatória no currículo (LDB, art. 26 e art. 9º, IV). **Decidido** em 03/11/2026: BNCC obrigatória no plano de ensino e opcional no plano de aula |
| PLA-05 | Quem aprova o plano de ensino (seção 3.2) | **Decidido** em 03/11/2026: coordenação pedagógica |
| PLA-06 | Conteúdo previsto e não ministrado: reagendar automático ou só pendência (seção 4.3) | **Decidido** em 03/11/2026: só pendência |
| PLA-07 | DDL: plano de ensino, unidade, plano de aula, versão, revisão e pendência de planejamento | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.9. Revisão do owner pendente (DDL-01) |

---

## 10. Critérios de aceite

- [ ] Soma dos pesos no plano de ensino diferente do sistema avaliativo bloqueia o envio (teste).
- [ ] Plano aprovado não muda sem nova versão (teste).
- [ ] Alteração de conteúdo já ministrado é recusada (teste).
- [ ] Plano de aula sem plano de ensino aprovado não é criado (teste).
- [ ] Aula sem plano aprovado não é bloqueada, e gera pendência (teste).
- [ ] Rascunho de IA não é enviado sem revisão do professor (teste de [27](27-inteligencia-artificial-e-portais.md), seção 5).
- [ ] Professor não edita plano de outra disciplina (teste de isolamento).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
