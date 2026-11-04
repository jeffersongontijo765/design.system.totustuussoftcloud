# 61 — Diário Escolar, por Portal: Chamada, Faltas, Justificativas, Notas e Conteúdo

> Parte do [SDD v2](00-README.md). Quarta lacuna da ordem de [55](55-academico-verificacao-e-lacunas.md), seção 3. Turma, aula e grade em [60](60-turmas-e-grade-de-horarios-por-portal.md). Sistema avaliativo e frequência mínima em [59](59-estrutura-academica-por-portal.md), seção 4. Chamada por QR Code e sala online em [17](17-regras-modulos.md), seção 4, e [40](40-aulas-online-por-portal.md). Períodos em [59](59-estrutura-academica-por-portal.md), seção 3.6. Aviso ao responsável em [57](57-notificacoes-por-portal.md). Relatórios do diário em [56](56-configuracoes-e-relatorios-lacunas.md), seção 5. Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna do diário. Pontos que dependem de norma ou de decisão do autor estão marcados.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Chamada tem regra? | **Parcial.** QR Code e manual em [17](17-regras-modulos.md). Falta regra de registro por aula |
| Faltas e justificativas? | **Não.** Só o nome "faltas" e "justificadas" no menu de referência |
| Lançamento de nota? | **Parcial.** Regra de faixa e de período aberto em [17](17-regras-modulos.md) |
| Conteúdo da aula? | **Não.** Só citado como plano de aula em [55](55-academico-verificacao-e-lacunas.md) |
| Fechamento e reabertura? | **Parcial.** Estados `aberto`, `fechado`, `reaberto` em [17](17-regras-modulos.md) |

---

## 2. Aula

Cada aula da grade ([60](60-turmas-e-grade-de-horarios-por-portal.md), seção 4) gera uma **aula realizada** no diário. A aula tem:

- Turma, disciplina, professor, data e bloco.
- Conteúdo ministrado, com texto livre e referência ao plano de aula.
- Estado: `planejada`, `realizada`, `cancelada`, `reposicao`.

**Regras:**

- Só o professor da disciplina na turma registra a aula.
- Aula cancelada não conta na frequência. Exige motivo.
- Aula de reposição é aula nova, com data própria. Não substitui a original.
- Conteúdo não lançado até o fim do período aparece no relatório de pendências ([56](56-configuracoes-e-relatorios-lacunas.md), seção 5).

---

## 3. Chamada

### 3.1 Formas de registro

| Forma | Quando | Regra |
|---|---|---|
| Manual | Padrão | Presente, falta, ou justificada, por aluno |
| QR Code | Presencial | Código válido pelo tempo configurado (5 minutos por padrão, decidido em 03/11/2026). Presença sem QR vira pendência |
| Sala online | Aula online | Presença pelo tempo conectado e confirmação, conforme [40](40-aulas-online-por-portal.md), seção 6 |

**Regra geral:** a chamada é lançada na aula, com correção até o fim do dia útil seguinte. **Decidido** em 03/11/2026 (DIA-05). Lançamento fora do prazo exige justificativa da coordenação.

### 3.2 Presença pendente

Aluno sem registro, em aula que usou QR ou sala online, fica como **pendência de chamada**. Não vira falta sem revisão do professor.

---

## 4. Faltas e justificativas

### 4.1 Falta

- Falta é registrada por aluno, por aula. Não por dia.
- Falta é contada por disciplina, e por período no total de frequência.

### 4.2 Justificativa

| Regra | Detalhe |
|---|---|
| Tipos | Lista padrão da plataforma, ajustável pela escola. Decidido em 03/11/2026 |
| Prazo | 5 dias úteis após a falta, ajustável pela escola. Decidido em 03/11/2026 |
| Documento | Anexo quando o tipo exigir. Armazenado como documento recebido ([54](54-gestao-de-documentos-tres-contextos.md), contexto A) |
| Quem aprova | Coordenação. Professor não aprova justificativa de própria aula |
| Efeito | A LDB não prevê abono geral de falta: a falta justificada continua contando para o mínimo de 75% (art. 24, VI). A exceção da LDB é a falta por motivo religioso com atividade alternativa, que regulariza a frequência (art. 7º-A, § 2º). Regimes especiais de lei própria, como exercícios domiciliares, entram como exceção configurada **(verificar)** |
| Negativa | Sempre com motivo. Aluno ou responsável recebe o aviso ([57](57-notificacoes-por-portal.md)) |

### 4.3 Aviso de falta

- Falta acima do limite de alerta da escola gera aviso ao responsável ([57](57-notificacoes-por-portal.md)).
- O aviso informa a disciplina e a quantidade de faltas. Não informa motivo clínico.
- Falta de saúde justificada por atestado não aparece com diagnóstico no aviso ([57](57-notificacoes-por-portal.md), seção 3.5).
- **Conselho Tutelar:** a escola notifica ao Conselho Tutelar do município a relação dos alunos com faltas acima de 30% do percentual permitido em lei (LDB, art. 12, VIII). O sistema gera a lista por período para a secretaria enviar. A forma de cálculo e a periodicidade ficam em DIA-09 **(verificar)**.

---

## 5. Notas

### 5.1 Lançamento

- Nota é lançada por avaliação, na escala e com o peso do sistema avaliativo ([59](59-estrutura-academica-por-portal.md), seção 4).
- Só o professor da disciplina na turma lança nota.
- Nota fora da escala é recusada.
- Nota lançada é `lançada`. Correção gera nova versão com motivo, e a anterior fica no histórico.

### 5.2 Média e recuperação

- Média por disciplina e por período, pelo método do sistema avaliativo.
- Aluno abaixo da média entra em recuperação conforme a regra do sistema. A nota de recuperação aplica-se conforme o sistema.
- Recuperação paralela e conselho de classe seguem [55](55-academico-verificacao-e-lacunas.md), item 5.

### 5.3 Período

Lançamento de nota e de chamada só com período `aberto` ([59](59-estrutura-academica-por-portal.md), seção 3.6). Reabertura exige justificativa e autorização da coordenação pedagógica (DIA-04).

---

## 6. Fechamento do diário

- Diário fecha por turma e disciplina, ao fim do período.
- Diário fechado não aceita chamada, nota ou conteúdo.
- Reabertura exige justificativa e autorização da coordenação pedagógica. Fica em auditoria ([29](29-auditoria.md)).
- Fechamento sem todas as notas gera pendência, não bloqueio. **Decidido** em 03/11/2026 (DIA-07).

---

## 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Nada sobre diário de entidade | Ver diário, nota, falta ou conteúdo | P |
| **Gestão** | Ver relatórios do diário e indicadores de frequência | Lançar nota ou chamada. Autorizar reabertura, que é da coordenação | E |
| **Coordenação** | Aprovar justificativa. Autorizar lançamento fora do prazo e reabertura. Ver diário de todas as turmas da unidade | Lançar nota pelo professor | E |
| **Secretaria** | Consultar diário. Emitir relatórios. Cadastrar tipos de justificativa | Lançar nota ou aprovar justificativa | E |
| **Professor** | Fazer chamada, lançar nota e conteúdo das próprias turmas. Ver o diário das próprias turmas | Lançar em turma em que não leciona. Aprovar justificativa da própria aula | E |
| **Aluno** | Ver as próprias notas, faltas e justificativas. Enviar justificativa com anexo | Ver nota ou falta de colega | E |
| **Responsáveis** | Ver as notas e faltas do dependente. Enviar justificativa | Ver diário de outra turma | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item do diário | E |

---

## 8. Pendências

| # | Pendência | Tipo |
|---|---|---|
| DIA-01 | Tipos de justificativa de falta | **Decidido** em 03/11/2026: lista padrão da plataforma (atestado médico, motivo familiar, luto, convocação oficial, atividade escolar, outro), que a escola ajusta |
| DIA-02 | Prazo para apresentar justificativa | **Decidido** em 03/11/2026: 5 dias úteis, ajustável pela escola |
| DIA-03 | Falta justificada conta ou não na frequência, por nível de ensino (seção 4.2) | **Conferido** em parte em 03/11/2026: a LDB não prevê abono geral (art. 24, VI). A exceção é o art. 7º-A. Regimes especiais de lei própria **(verificar)** |
| DIA-04 | Quem autoriza reabertura de diário e lançamento fora do prazo | **Decidido** em 03/11/2026: coordenação pedagógica, com justificativa e registro. A secretaria executa |
| DIA-05 | Prazo de correção da chamada após a aula (seção 3.1) | **Decidido** em 03/11/2026: até o fim do dia útil seguinte |
| DIA-06 | Limite de falta que gera aviso ao responsável (seção 4.3) | **Decidido** em 03/11/2026: a cada 5 faltas na disciplina |
| DIA-07 | Fechamento sem todas as notas: pendência ou bloqueio (seção 6) | **Decidido** em 03/11/2026: pendência, sem bloqueio |
| DIA-08 | DDL: aula, chamada, falta, justificativa, lançamento de nota e conteúdo | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.5. Revisão do owner pendente (DDL-01) |
| DIA-09 | Lista de alunos para o Conselho Tutelar (LDB, art. 12, VIII): base do cálculo de "30% do percentual permitido" e periodicidade do envio (seção 4.3) | (verificar) |

---

## 9. Critérios de aceite

- [ ] Professor de outra turma não lança chamada nem nota (teste de isolamento).
- [ ] Presença pendente de QR não vira falta sem revisão (teste).
- [ ] Nota fora da escala é recusada (teste).
- [ ] Correção de nota gera nova versão com motivo (teste).
- [ ] Diário fechado não aceita lançamento, e reabertura fica em auditoria (teste).
- [ ] Aviso de falta não traz diagnóstico (varredura).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
