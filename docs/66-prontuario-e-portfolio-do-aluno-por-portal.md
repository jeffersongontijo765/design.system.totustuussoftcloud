# 66 — Prontuário e Portfólio do Aluno, por Portal

> Parte do [SDD v2](00-README.md). Nona lacuna da ordem de [55](55-academico-verificacao-e-lacunas.md), seção 3. Depende do diário ([61](61-diario-escolar-por-portal.md)) e do boletim ([62](62-boletim-e-conselho-de-classe-por-portal.md)). Documentos recebidos e emitidos ficam em [54](54-gestao-de-documentos-tres-contextos.md), contextos A e C. O prontuário é uma visão sobre eles, sem cópia. Armazenamento, hash e OCR em [21](21-busca-e-armazenamento.md). Ocorrências em [63](63-ocorrencias-disciplinares-por-portal.md). Acesso a dado sensível e campos bloqueados em [18](18-regras-modulos-2.md), seção 3.3, e [38](38-portal-de-terceiros-prestadores.md). Dados de menor e imagem em [40](40-aulas-online-por-portal.md) e [07](07-privacidade-lgpd.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 9 do acadêmico. A v1 tem `student_records` e `student_portfolios` (`spec_gestao_academica_completo.md`, seções 5.3, 7.5 e 16). Pontos que dependem de norma ou de decisão do autor estão marcados.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Prontuário tem regra? | **Parcial.** Documentos com versão, validade, responsável e hash em [17](17-regras-modulos.md) e [54](54-gestao-de-documentos-tres-contextos.md). Falta a visão do prontuário e as seções de dado de saúde |
| Acesso ao prontuário? | **Não.** A v1 dá leitura à coordenação sem limitar seção. Pela regra de dado sensível, isso não basta |
| Portfólio tem regra? | **Não.** A v1 tem campos e tipos de evidência, sem regra de compartilhamento nem de exportação |
| Dado de saúde e necessidade específica? | **Não.** A v1 não tem seção. Acessibilidade aparece em [60](60-turmas-e-grade-de-horarios-por-portal.md), seção 2.2 |

---

## 2. Prontuário

### 2.1 Princípio: visão, não cópia

O prontuário é a página do aluno que reúne, por seção, o que já existe em outro lugar. Cada documento tem um único armazenamento e uma única origem. O prontuário mostra e linka.

| Seção | Origem | Como aparece |
|---|---|---|
| Documentos pessoais | Contexto A, recebidos ([54](54-gestao-de-documentos-tres-contextos.md)) | Lista de documentos com validade, status e versão |
| Documentos acadêmicos | Contexto C, emitidos, e histórico externo recebido | Histórico interno, diplomas anteriores e histórico externo |
| Histórico acadêmico | Diário e boletim ([61](61-diario-escolar-por-portal.md), [62](62-boletim-e-conselho-de-classe-por-portal.md)) | Só leitura. Não é editado no prontuário |
| Contratos e termos | Contratos ([33](33-contratos-por-portal.md)) e termos de [65](65-estagio-e-tcc-por-portal.md) | Contrato pedagógico, aditivos, termo de estágio, termo LGPD |
| Requerimentos e protocolos | Atendimento ([32](32-atendimento-privacidade-por-portal.md)) e matrícula ([46](46-matricula-e-rematricula-por-portal.md)) | Todos os requerimentos e respostas |
| Comunicações | Notificações ([57](57-notificacoes-por-portal.md)) | Correspondência oficial enviada e recebida |
| Ocorrências | [63](63-ocorrencias-disciplinares-por-portal.md) | Só comunicação e medida, conforme OCO-05 |
| Saúde e apoio | Seção própria (seção 2.3) | Restrita |

### 2.2 Regras gerais

- Cada documento do prontuário tem data de envio, validade, responsável, versão e hash de integridade ([54](54-gestao-de-documentos-tres-contextos.md)). Nova versão não apaga a anterior.
- Documento vencido aparece com aviso. Não é removido sem prazo de guarda ([26](26-sdd-juridico-regulatorio.md), N-10).
- O prontuário não tem campo de edição livre para dado que já é de outro módulo.

### 2.3 Saúde e apoio educacional

Esta seção é restrita. Inclui:

- Laudo ou relatório de necessidade educacional específica, quando houver.
- Plano de apoio ou de acessibilidade, com o recurso que a escola disponibilizou.
- Restrição alimentar ou medicamento de uso escolar.
- Registro de atendimento de enfermaria.

**Regras:**

- Diagnóstico e CID ficam visíveis para coordenação, secretaria, enfermagem e médico da escola. Decidido em 03/11/2026 (PRT-01). Os demais portais não veem.
- Medicamento de uso escolar tem validade e autorização do responsável, com documento no contexto A.
- Acesso à seção gera evento de auditoria com motivo ([29](29-auditoria.md)).
- A seção não é enviada para terceiros. Empresa de transporte e de alimentação recebem só o que a regra de contrato permite ([38](38-portal-de-terceiros-prestadores.md), seção 5).

### 2.4 Histórico após saída

- Aluno transferido, trancado ou desligado mantém o prontuário com acesso restrito à secretaria e à coordenação.
- Prazo de guarda segue o acervo escolar ([26](26-sdd-juridico-regulatorio.md), seção 3, N-10). **(jurídico)**

---

## 3. Portfólio

### 3.1 Evidências

| Campo | Regra |
|---|---|
| Aluno e disciplina | Um portfólio por aluno e disciplina, com período letivo |
| Evidência | Texto, imagem, arquivo, link ou vídeo |
| Quem publica | O aluno, pelo portal. Ou o professor, por material de aula |
| Imagem ou vídeo com outra pessoa | Só com autorização do responsável, quando o aluno é menor. Mesma regra de [40](40-aulas-online-por-portal.md) |
| Dado pessoal de terceiro | Evidência com dado de outra pessoa é recusada ou anonimizada antes de publicar, como em [42](42-preceptoria-por-portal.md), seção 6 |

### 3.2 Avaliação

- O professor avalia o portfólio com comentário e nota qualitativa. Nota qualitativa não entra no cálculo da média sem regra do sistema avaliativo ([59](59-estrutura-academica-por-portal.md), seção 4).
- O aluno vê a avaliação depois de publicada. Antes, o portfólio fica em rascunho.

### 3.3 Compartilhamento e exportação

- Para aluno maior de idade, o aluno decide compartilhar com o responsável.
- Para aluno menor de idade, o responsável vê o portfólio sempre, sem depender do aluno. Decidido em 03/11/2026 (PRT-02).
- Exportação em PDF é feita pelo próprio aluno, com a data e a identificação do aluno. A escola não exporta portfólio para terceiros sem pedido por escrito do aluno ou do responsável.
- Exportação registra evento de auditoria.

---

## 4. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelo de prontuário e de portfólio, sem dado | Ver prontuário, saúde ou portfólio de entidade | P |
| **Gestão** | Ver indicador: prontuários completos, documentos vencidos, portfólios publicados | Ver seção de saúde. Ver documento pessoal | E |
| **Coordenação** | Ver o prontuário, inclusive a seção de saúde com CID e diagnóstico. Ver portfólio da unidade | Editar histórico | E |
| **Secretaria** | Gerir documentos pessoais e acadêmicos, requerimentos e comunicações. Ver a seção de saúde, inclusive CID | Editar avaliação do portfólio | E |
| **Enfermagem e médico da escola** | Ver e registrar a seção de saúde e apoio | Ver histórico de notas ou ocorrência, sem necessidade | E |
| **Professor** | Ver o portfólio da própria disciplina. Avaliar. Publicar material de aula | Ver prontuário. Ver portfólio de outra disciplina | E |
| **Aluno** | Ver o próprio prontuário, exceto saúde restrita. Publicar e exportar o próprio portfólio. Ver a avaliação | Ver portfólio ou prontuário de colega | E |
| **Responsáveis** | Ver documentos e comunicações do dependente. Ver o portfólio do dependente menor sempre, e do maior se ele compartilhar | Ver CID ou diagnóstico. Ver portfólio de outro aluno | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item do prontuário ou do portfólio | E |

---

## 5. Integrações

| Módulo | Relação |
|---|---|
| Documentos ([54](54-gestao-de-documentos-tres-contextos.md)) | Origem de documentos pessoais, acadêmicos e de termo |
| Armazenamento ([21](21-busca-e-armazenamento.md)) | Arquivo, hash, OCR de digitalização |
| Diário e boletim ([61](61-diario-escolar-por-portal.md), [62](62-boletim-e-conselho-de-classe-por-portal.md)) | Histórico acadêmico só para leitura |
| Acessibilidade ([60](60-turmas-e-grade-de-horarios-por-portal.md), seção 2.2) | Sala com recurso de acessibilidade |
| Ocorrências ([63](63-ocorrencias-disciplinares-por-portal.md)) | Comunicação e medida |
| Atendimento ([32](32-atendimento-privacidade-por-portal.md)) e matrícula ([46](46-matricula-e-rematricula-por-portal.md)) | Requerimentos e protocolos |
| Notificações ([57](57-notificacoes-por-portal.md)) | Aviso de documento vencido, de portfólio avaliado e de comunicação |

---

## 6. Pendências

| # | Pendência | Tipo |
|---|---|---|
| PRT-01 | CID e diagnóstico: quem vê (seção 2.3) | **Decidido** em 03/11/2026: coordenação, secretaria, enfermagem e médico da escola. **Atenção:** a regra de mínimo de dado usada em [18](18-regras-modulos-2.md), seção 3.3, e em [52](52-medicina-do-trabalho-especificacao.md) restringe CID a quem trata o paciente. Vale rever com o (jurídico) (PRT-07) |
| PRT-02 | Portfólio de menor: responsável vê sem o aluno compartilhar (seção 3.3) | **Decidido** em 03/11/2026: sim, sempre para menor |
| PRT-07 | Revisão jurídica do acesso da secretaria e da coordenação ao CID (PRT-01), à luz da minimização de dado | (jurídico) |
| PRT-03 | Guarda do prontuário após saída do aluno (seção 2.4). Mesmo ponto de N-10 | (jurídico) |
| PRT-04 | Imagem de menor em portfólio: autorização e prazo (seção 3.1). Mesmo ponto de LIV-13 de [40](40-aulas-online-por-portal.md) | (jurídico) |
| PRT-05 | Restrição alimentar e medicamento de uso escolar: documento e validade exigidos (seção 2.3) | (verificar) |
| PRT-06 | DDL das tabelas: seção de prontuário, vínculo com documento, portfólio, evidência, avaliação e compartilhamento | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.11. Revisão do owner pendente (DDL-01) |

---

## 7. Critérios de aceite

- [ ] Prontuário não guarda cópia de documento de outro contexto (teste de integridade: um documento, uma origem).
- [ ] Professor e responsável não veem CID nem diagnóstico (teste de isolamento e varredura de resposta).
- [ ] Documento vencido aparece com aviso, sem ser removido (teste).
- [ ] Aluno transferido mantém prontuário com acesso restrito (teste).
- [ ] Portfólio em rascunho não aparece para o responsável (teste).
- [ ] Evidência com dado de terceiro é recusada ou anonimizada antes de publicar (teste).
- [ ] Exportação de portfólio gera evento de auditoria (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
