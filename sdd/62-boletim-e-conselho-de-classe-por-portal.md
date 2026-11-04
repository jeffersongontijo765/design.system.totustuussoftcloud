# 62 — Boletim, Aprovação, Recuperação e Conselho de Classe, por Portal

> Parte do [SDD v2](00-README.md). Quinta lacuna da ordem de [55](55-academico-verificacao-e-lacunas.md), seção 3. Depende do diário ([61](61-diario-escolar-por-portal.md)), da turma ([60](60-turmas-e-grade-de-horarios-por-portal.md)) e do sistema avaliativo ([59](59-estrutura-academica-por-portal.md), seção 4). Atas e boletim como documento em [53](53-pacote-documentos-e-contratos.md), DC-17 a DC-18, e em [48](48-gerador-de-documentos-por-portal.md). Validação pública em [48](48-gerador-de-documentos-por-portal.md), seção 6. Ocorrências, item 6 de [55](55-academico-verificacao-e-lacunas.md), alimentam a pauta do conselho, mas ainda não têm especificação. Aviso de resultado em [57](57-notificacoes-por-portal.md). Regras de matrícula por resultado em [46](46-matricula-e-rematricula-por-portal.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 5 do acadêmico. Pontos que dependem de norma ou de decisão do autor estão marcados.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Boletim tem regra? | **Não.** Aparece só como documento do portal do aluno em [31](31-matriz-portais-modulos.md), seção 3 |
| Aprovação final tem regra? | **Parcial.** Nota dentro da faixa em [15](15-validacoes.md). Regra de aprovação por nota e frequência não está especificada |
| Recuperação paralela? | **Não.** Só citada como tipo de avaliação em [59](59-estrutura-academica-por-portal.md), seção 4 |
| Conselho de classe? | **Não.** Só citado como entidade em [17](17-regras-modulos.md), seção 4.1, e como ata em [53](53-pacote-documentos-e-contratos.md), DC-18 |
| Ata e assinatura? | **Parcial.** Quem assina a ata de conselho está em DC-18. Ata de resultados finais em DC-17 |

---

## 2. Boletim

### 2.1 Conteúdo

O boletim reúne, por aluno e por período:

- Identificação do aluno, da turma, do curso, da versão da grade e do período letivo.
- Por disciplina: avaliações com nota, peso e data, média do período, total de aulas, faltas e percentual de frequência.
- Situação da disciplina: `aprovado`, `recuperacao`, `reprovado_nota`, `reprovado_frequencia`, `aprovado_conselho`, `em_andamento`.
- Versão do sistema avaliativo aplicada. Mudança posterior do sistema não altera o boletim já emitido.
- Resultado final do período, quando o período estiver fechado.

### 2.2 Tipos de emissão

| Tipo | Quando | Valor |
|---|---|---|
| Parcial | Durante o período, a qualquer momento | Informativo. Traz a marca "parcial, sem valor oficial". Não é documento de [48](48-gerador-de-documentos-por-portal.md) |
| Oficial | Depois do fechamento do período e da ata do conselho, se houver | Documento oficial, com código de validação e QR. Vai para o contexto C de [54](54-gestao-de-documentos-tres-contextos.md) |
| Segunda via | A pedido, depois da emissão oficial | Indica que é reemissão e mantém a data de origem, como em DC-14 ([53](53-pacote-documentos-e-contratos.md)) |

**Regras:**

- Boletim oficial só é emitido com período `fechado` ([59](59-estrutura-academica-por-portal.md), seção 3.6).
- Boletim oficial traz código de validação pública. Pela regra DC-13, a validação mostra tipo, data, situação e entidade. Não mostra nota.
- Alteração de nota depois do boletim oficial gera nova versão do boletim, com aviso ao aluno e ao responsável ([57](57-notificacoes-por-portal.md)). A versão anterior fica no histórico.

---

## 3. Aprovação final

### 3.1 Regra

Para cada disciplina, a situação final segue esta ordem:

1. **Frequência** abaixo do mínimo do sistema avaliativo: `reprovado_frequencia`. Valor mínimo por nível de ensino em [59](59-estrutura-academica-por-portal.md), EST-01: 75% na educação básica (LDB, art. 24, VI).
2. **Média** igual ou acima da nota mínima de aprovação: `aprovado`.
3. **Média** abaixo da nota mínima, mas acima do piso de recuperação do sistema: `recuperacao`. A recuperação é feita conforme a seção 4.
4. **Média** abaixo do piso de recuperação: `reprovado_nota`.
5. **Caso fora da regra** (por exemplo, média abaixo do mínimo em disciplina com regra especial): vai ao conselho, seção 5. Pode resultar em `aprovado_conselho` ou `reprovado_nota`, com justificativa registrada.

O resultado do período combina as disciplinas conforme a regra do sistema avaliativo. Se a regra exigir aprovação em todas as disciplinas, uma disciplina reprovada reprova o período. O sistema não decide a combinação sozinho, porque ela muda por escola e por norma **(verificar)**.

### 3.2 Regras

- A situação é calculada pela regra da versão do sistema vigente no período, e gravada com o número da versão.
- Situação gravada só muda por conselho ou por reabertura autorizada. Recálculo sem reabertura gera aviso à coordenação, não mudança silenciosa.
- Aluno transferido ou trancado no período não recebe situação final. Fica com a situação parcial e com o motivo.

---

## 4. Recuperação paralela

- Aluno com situação `recuperacao` faz avaliação de recuperação durante o período letivo, dentro do calendário da unidade ([58](58-calendario-e-eventos-por-portal.md)).
- A nota de recuperação é lançada como avaliação do tipo recuperação, com peso definido no sistema avaliativo.
- A nota resultante segue a regra do sistema: **substitui** a média ou **compõe** com ela ([59](59-estrutura-academica-por-portal.md), seção 4). **Decidido** em 03/11/2026: as duas opções existem, e a instituição escolhe no sistema avaliativo.
- Recuperação só é lançada com período aberto, pelo professor da disciplina, como as demais notas ([61](61-diario-escolar-por-portal.md), seção 5).
- Aluno que não fez a recuperação fica com a situação do início da recuperação, sem nova média.

---

## 5. Conselho de classe

### 5.1 Convocação e pauta

- O conselho é convocado pela coordenação pedagógica, por turma e por período. Pode haver conselho intermediário, sem decisão de resultado.
- A pauta é gerada pelo sistema com os alunos em situação de atenção:
  - média abaixo da nota mínima;
  - frequência a menos de 5 pontos percentuais do mínimo. **Decidido** em 03/11/2026;
  - alunos com recuperação pendente;
  - ocorrências do período ([55](55-academico-verificacao-e-lacunas.md), item 6), quando a especificação de ocorrências estiver pronta.
- A coordenação pode incluir ou retirar alunos da pauta, com justificativa.

### 5.2 Participantes

| Papel | Participa | Vota ou decide |
|---|---|---|
| Coordenação pedagógica | Sim | Preside |
| Professores da turma | Sim | Opinam. A decisão do caso é da reunião |
| Secretaria | Sim | Registra. Não vota |
| Gestão | A convite | Não decide resultado de aluno |
| Responsáveis e aluno | Não participam da reunião | Podem enviar parecer por escrito antes da reunião. **Decidido** em 03/11/2026 |

### 5.3 Decisão

- A decisão é registrada por aluno e por disciplina, com a situação, a justificativa e o nome de quem decidiu.
- Aprovação fora da regra (seção 3.1, item 5) exige justificativa escrita.
- Decisão de conselho não pode ser tomada sem quórum mínimo de maioria dos membros. **Decidido** em 03/11/2026.
- Parecer de professor sobre aluno com dado de saúde, pastoral ou atendimento sensível não entra na ata. Fica em registro restrito aos participantes e à direção ([53](53-pacote-documentos-e-contratos.md), DC-27).

### 5.4 Ata

- A ata é gerada do registro do conselho: data, turma, pauta, presentes, decisões por aluno e justificativas.
- Assinada pelo presidente e pelo secretário, conforme DC-18 ([53](53-pacote-documentos-e-contratos.md)). Não exige assinatura de todos os presentes.
- Ata assinada entra no acervo da secretaria ([54](54-gestao-de-documentos-tres-contextos.md), contexto B ou C, conforme o tipo).
- Ata sem assinatura fica como rascunho. Não gera resultado final.

---

## 6. Fechamento e reabertura do resultado

- O fechamento do período (diário, [61](61-diario-escolar-por-portal.md), seção 6) gera o resultado final por aluno, segundo a seção 3.
- Fechamento com conselho pendente: o período fecha, e a falta de ata assinada fica como pendência para a coordenação. **Decidido** em 03/11/2026.
- Reabertura do resultado exige justificativa e autorização da coordenação. A secretaria executa. Nova versão do resultado é gravada, com o anterior no histórico ([61](61-diario-escolar-por-portal.md), seção 6).
- Resultado final alimenta a matrícula do período seguinte: aprovado avança, reprovado segue a regra de rematrícula de [46](46-matricula-e-rematricula-por-portal.md).
- Mudança de resultado depois da rematrícula gera aviso à secretaria, que decide sobre o vínculo.

---

## 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelo de ata e de boletim, sem dado | Ver boletim, resultado ou ata de entidade | P |
| **Gestão** | Ver indicadores de aprovação e reprovação, ver atas da unidade | Alterar resultado. Decidir conselho de aluno | E |
| **Coordenação** | Convocar conselho, montar pauta, presidir, decidir resultado fora da regra, autorizar reabertura | Lançar nota pelo professor | E |
| **Secretaria** | Emitir boletim oficial, registrar ata, executar reabertura autorizada, emitir segunda via | Decidir resultado de aluno | E |
| **Professor** | Ver boletim parcial das próprias turmas. Opinar no conselho. Lançar recuperação | Decidir resultado. Ver boletim de turma de que não é professor | E |
| **Aluno** | Ver o próprio boletim, parcial e oficial, e a situação. Baixar boletim oficial | Ver ata. Ver boletim de colega | E |
| **Responsáveis** | Ver boletim do dependente, parcial e oficial. Ver a situação | Ver ata ou parecer. Ver boletim de outro aluno | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item do boletim ou do conselho | E |

---

## 8. Integrações

| Módulo | Relação |
|---|---|
| Diário ([61](61-diario-escolar-por-portal.md)) | Notas, faltas e fechamento alimentam o boletim |
| Estrutura ([59](59-estrutura-academica-por-portal.md)) | Sistema avaliativo define média, mínimo, recuperação e frequência |
| Calendário ([58](58-calendario-e-eventos-por-portal.md)) | Período de recuperação e de conselho |
| Ocorrências ([55](55-academico-verificacao-e-lacunas.md), item 6) | Entram na pauta do conselho |
| Documentos ([48](48-gerador-de-documentos-por-portal.md), [54](54-gestao-de-documentos-tres-contextos.md)) | Boletim oficial, ata e segunda via |
| Matrícula ([46](46-matricula-e-rematricula-por-portal.md)) | Resultado final define avanço ou rematrícula |
| Notificações ([57](57-notificacoes-por-portal.md)) | Aviso de resultado, de conselho e de boletim disponível |

---

## 9. Pendências

| # | Pendência | Tipo |
|---|---|---|
| BOL-01 | Frequência mínima para aprovação, por nível de ensino (seção 3.1, item 1) | **Conferido** em 03/11/2026 com EST-01 de [59](59-estrutura-academica-por-portal.md): 75% na educação básica. Superior segue EST-01 |
| BOL-02 | Regra de combinação do resultado do período (seção 3.1, último parágrafo) | (verificar) |
| BOL-03 | Recuperação: substitui ou compõe a média (seção 4) | **Decidido** em 03/11/2026: a instituição escolhe no sistema avaliativo |
| BOL-04 | Pareceres por escrito de responsáveis e alunos antes do conselho (seção 5.2) | **Decidido** em 03/11/2026: sim, por escrito |
| BOL-05 | Quórum mínimo do conselho (seção 5.3) | **Decidido** em 03/11/2026: maioria dos membros |
| BOL-06 | Fechamento com conselho pendente: bloqueia ou marca pendência (seção 6) | **Decidido** em 03/11/2026: marca pendência |
| BOL-07 | Frequência para alerta no conselho (seção 5.1) | **Decidido** em 03/11/2026: 5 pontos acima do mínimo |
| BOL-08 | Prazo de guarda de boletim e de ata | (jurídico). Mesmo ponto de DC-17 em [53](53-pacote-documentos-e-contratos.md) |
| BOL-09 | Piso de recuperação: nota mínima para entrar em recuperação (seção 3.1, item 3). O sistema avaliativo de [59](59-estrutura-academica-por-portal.md) ainda não define esse valor | **Decidido** em 03/11/2026: a escola define o valor no sistema avaliativo, sem padrão da plataforma |
| BOL-10 | DDL das tabelas: boletim, resultado por disciplina, recuperação, pauta, reunião, decisão e ata | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.6. Revisão do owner pendente (DDL-01) |

---

## 10. Critérios de aceite

- [ ] Resultado calculado com a versão do sistema avaliativo vigente no período, e a versão fica gravada (teste).
- [ ] Mudança de sistema avaliativo não altera boletim já emitido (teste).
- [ ] Boletim parcial não é aceito como documento oficial (teste).
- [ ] Validação pública do boletim não mostra nota (teste de DC-13).
- [ ] Aprovação fora da regra sem justificativa escrita é recusada (teste).
- [ ] Ata sem assinatura não gera resultado final (teste).
- [ ] Parecer com dado de saúde ou pastoral não aparece na ata (varredura).
- [ ] Aluno ou responsável não vê boletim de outro aluno (teste de isolamento).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
