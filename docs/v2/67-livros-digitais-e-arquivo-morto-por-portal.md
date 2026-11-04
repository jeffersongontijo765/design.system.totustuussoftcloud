# 67 — Livros Digitais e Arquivo Morto, por Portal

> Parte do [SDD v2](00-README.md). Décima lacuna da ordem de [55](55-academico-verificacao-e-lacunas.md), seção 3. Depende dos documentos de [54](54-gestao-de-documentos-tres-contextos.md) e do registro de matrícula de [46](46-matricula-e-rematricula-por-portal.md). Atas de conselho em [62](62-boletim-e-conselho-de-classe-por-portal.md) e [53](53-pacote-documentos-e-contratos.md), DC-17 e DC-18. Armazenamento, hash e OCR em [21](21-busca-e-armazenamento.md). Cadeia de integridade em [18](18-regras-modulos-2.md), seção 3. Assinatura e ICP-Brasil em [54](54-gestao-de-documentos-tres-contextos.md), seção 5, e [48](48-gerador-de-documentos-por-portal.md). Guarda e eliminação em [26](26-sdd-juridico-regulatorio.md), seção 6, e [07](07-privacidade-lgpd.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 10 do acadêmico. A v1 tem `book-registry`, `meeting-book` e `digital-archive` ([`spec_gestao_academica_completo.md`](anexo-v1/spec_gestao_academica_completo.md), seções 6.4 a 6.6). Esta versão mantém o que a v1 tem e acrescenta as regras de imutabilidade, separação de funções e eliminação.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Livro de registro tem regra? | **Parcial.** A v1 tem campos, numeração e travamento. Faltam regra de correção, de separação de funções e de exportação |
| Livro de atas tem regra? | **Parcial.** A v1 tem estados e numeração. Faltam regras de ata retificadora e de assinatura |
| Arquivo morto tem regra? | **Parcial.** A v1 tem localização física, digitalização e empréstimo. Faltam regra de verificação, de original e de eliminação |
| Guarda e eliminação? | **Não.** Depende do jurídico ([26](26-sdd-juridico-regulatorio.md), J-04) |

---

## 2. Livro de registro

### 2.1 Conteúdo

- Um registro por matrícula efetivada.
- Campos: número de ordem, nome do aluno, curso, série ou módulo, data da matrícula, situação e identificação de quem assinou.
- CPF do aluno no livro: sim, como na v1. **Decidido** em 03/11/2026 (ARQ-01).

### 2.2 Numeração e travamento

- Número de ordem é sequencial por livro e por unidade. Não é reaproveitado, mesmo se a matrícula for cancelada.
- Registro é travado quando o livro é publicado. Alteração depois disso não edita o registro: gera **nota de retificação** com motivo, data e autor. Ver ARQ-05.
- Cada registro guarda hash do conteúdo e do registro anterior, como a cadeia de [18](18-regras-modulos-2.md), seção 3.1.

### 2.3 Geração e envio

- Livro é gerado em PDF, com numeração de páginas e cabeçalho da unidade.
- Exportação para o órgão do sistema de ensino da entidade, no formato que a norma exigir **(verificar)**. A v1 cita envio ao MEC e SIED. A referência do órgão é configurada por unidade ([26](26-sdd-juridico-regulatorio.md), seção 6).

---

## 3. Livro de atas

### 3.1 O que entra

Atas de conselho de classe ([62](62-boletim-e-conselho-de-classe-por-portal.md), seção 5), de reunião e de assembleia. Não entra ata com dado de saúde, pastoral ou de conduta de aluno: esses ficam no registro restrito de cada módulo ([63](63-ocorrencias-disciplinares-por-portal.md), seção 6).

### 3.2 Estados

`rascunho` → `em_assinatura` → `assinado` → `publicado`.

- `rascunho`: pode ser editado pelo autor.
- `em_assinatura`: travado para edição. Todos os participantes assinam individualmente.
- `assinado`: todas as assinaturas registradas. Não tem número final ainda.
- `publicado`: recebe número sequencial e data. Não é alterado. Correção é ata retificadora, que aponta a original.

### 3.3 Regras

- Número e data de criação são imutáveis depois de publicado.
- Ata sem todas as assinaturas exigidas não sai de `em_assinatura`.
- Assinatura segue o tipo de documento: assinatura simples ou ICP-Brasil, conforme a lista do jurídico ([54](54-gestao-de-documentos-tres-contextos.md), seção 5; N-12 de [50](50-pacote-juridico-e-norma.md)).
- Impressão em layout oficial da unidade.

---

## 4. Arquivo morto

### 4.1 O que é

Acervo de documentos de alunos que já saíram ou de documentos sem uso corrente. Inclui papel original e a versão digitalizada. Não é o prontuário de aluno ativo ([66](66-prontuario-e-portfolio-do-aluno-por-portal.md)).

### 4.2 Cadastro físico

| Campo | Regra |
|---|---|
| Localização | Caixa, pasta e prateleira, com código único na unidade |
| Tipo e período | Tipo de documento, aluno ou turma, ano letivo, período |
| Situação | `apenas_fisico`, `digitalizado`, `digitalizado_verificado` |
| Empréstimo | Quem retirou, data, prazo e devolução. Empréstimo em atraso aparece para a secretaria |

### 4.3 Digitalização e verificação

- Digitalização gera PDF ou imagem, com hash e data.
- Quem digitaliza não verifica. A verificação é feita por outra pessoa, com registro de quem verificou. Mesmo padrão de separação de funções de [51](51-ddl-modulos-novos.md).
- Só documento `digitalizado_verificado` pode ser usado como cópia oficial. Ver ARQ-03 para o original.
- Busca no texto digitalizado segue [21](21-busca-e-armazenamento.md). Texto de documento sensível não entra no índice ([21](21-busca-e-armazenamento.md), D-13).

### 4.4 Eliminação

- Nenhum documento físico é descartado pelo sistema. O sistema só registra a eliminação, quando a escola a decide.
- Eliminação só depois do prazo de guarda do tipo de documento ([26](26-sdd-juridico-regulatorio.md), seção 6; N-10) **(jurídico)**.
- Eliminação gera termo com lista do que foi eliminado, data e responsável. O termo não guarda o conteúdo.

---

## 5. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelo de livro de registro e de ata, sem dado | Ver livro, ata ou arquivo de entidade | P |
| **Gestão** | Ver indicadores: livros publicados, documentos digitalizados e verificados, empréstimos em atraso | Publicar livro. Ver conteúdo do arquivo | E |
| **Coordenação** | Assinar atas. Ver atas da unidade. Ver arquivo morto (leitura) | Publicar livro de registro. Eliminar documento | E |
| **Secretaria** | Gerar e publicar livro de registro. Cadastrar, digitalizar e controlar empréstimo do arquivo | Verificar a própria digitalização. Eliminar sem termo autorizado | E |
| **Verificador** (funcionário designado pela secretaria) | Verificar documento digitalizado por outra pessoa | Digitalizar o mesmo documento | E |
| **Professor** | Assinar ata em que participou | Ver livro de registro ou arquivo | E |
| **Aluno** | Pedir cópia de documento do próprio arquivo, por requerimento ([46](46-matricula-e-rematricula-por-portal.md)) | Ver arquivo de colega ou livro | E |
| **Responsáveis** | Pedir cópia de documento do dependente, por requerimento | Ver livro ou ata | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item de livro ou arquivo | E |

---

## 6. Pendências

| # | Pendência | Tipo |
|---|---|---|
| ARQ-01 | CPF do aluno no livro de registro (seção 2.1) | **Decidido** em 03/11/2026: sim, como na v1. A norma que o exige segue em conferência (ARQ-04) |
| ARQ-02 | Prazo de guarda por tipo de documento e de livro (seção 4.4). Mesmo ponto de N-10 e J-04 | (jurídico) |
| ARQ-03 | O original em papel pode ser eliminado depois de digitalizado e verificado (seção 4.3) | (jurídico) |
| ARQ-04 | Formato e órgão de envio do livro de registro por tipo de sistema de ensino (seção 2.3) | (verificar) |
| ARQ-05 | Correção de registro publicado (seção 2.2) | **Decidido** em 03/11/2026: nota de retificação, sem reabrir o livro |
| ARQ-06 | Assinatura de ata: simples ou ICP-Brasil, por tipo de ata. Mesmo ponto de N-12 | (jurídico) |
| ARQ-07 | DDL das tabelas: livro, registro, ata, participante e assinatura, arquivo, localização, empréstimo, digitalização e termo de eliminação | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.12. Revisão do owner pendente (DDL-01) |

---

## 7. Critérios de aceite

- [ ] Número de ordem do livro não é reaproveitado (teste).
- [ ] Registro publicado não é editado; correção gera nota de retificação (teste).
- [ ] Ata em `em_assinatura` não é alterada (teste).
- [ ] Ata publicada mantém número e data (teste).
- [ ] Documento digitalizado não é verificado pela mesma pessoa que o digitalizou (teste).
- [ ] Documento físico não é eliminado pelo sistema sem termo (teste).
- [ ] Aluno não vê arquivo ou livro de colega (teste de isolamento).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
