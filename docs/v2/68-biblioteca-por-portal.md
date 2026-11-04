# 68 — Biblioteca (Acervo, Empréstimos, Reservas, Multas e Salas de Leitura), por Portal

> Parte do [SDD v2](00-README.md). Décima primeira lacuna da ordem de [55](55-academico-verificacao-e-lacunas.md), seção 3. Fronteira com Gestão de Documentos em [31](31-matriz-portais-modulos.md), seção 3.1: biblioteca e documentos são módulos separados. Multas viram cobrança em [18](18-regras-modulos-2.md). Aquisição em [17](17-regras-modulos.md), suprimentos. Patrimônio e baixa em [19](19-regras-modulos-3.md), seção 8. Salas de leitura usam o cadastro de recursos de [44](44-agendamento-ambientes-equipamentos.md) e [60](60-turmas-e-grade-de-horarios-por-portal.md), seção 2.2. Avisos de prazo em [57](57-notificacoes-por-portal.md). Busca no acervo em [21](21-busca-e-armazenamento.md), seção 6. Bibliografia do plano em [64](64-planos-de-aula-e-de-ensino-por-portal.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 11 do acadêmico. A referência de domínio é [`spec_gestao_biblioteca_academica.md`](anexo-v1/spec_gestao_biblioteca_academica.md) (v1, Draft). O [`spec_gestao_biblioteca_completo.md`](anexo-v1/spec_gestao_biblioteca_completo.md) é design de interface e não é usado aqui, conforme [31](31-matriz-portais-modulos.md), seção 3.1.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Biblioteca tem especificação na v2? | **Não.** Só citada como módulo em [31](31-matriz-portais-modulos.md) e como lacuna em [56](56-configuracoes-e-relatorios-lacunas.md) |
| Domínio na v1? | **Sim, em rascunho.** Acervo, exemplar, empréstimo, reserva, multa, inventário, salas e biblioteca digital. Tem modelo de dados e API |
| Separada de documentos? | **Sim**, em [31](31-matriz-portais-modulos.md). A página de gestão de documentos sai da UI da biblioteca |
| Problemas da v1 a corrigir? | **Sim:** tabelas sem `tenant_id` (T-01), seção 3 numerada duas vezes, salas de leitura duplicadas do agendamento, aquisição duplicada de suprimentos |

---

## 2. Escopo

Entra: catálogo (livros, periódicos, mídias, e-books e TCCs), exemplares com código de barras, empréstimo e devolução, renovação, reserva com fila, multas, inventário, baixa e descarte, biblioteca digital e indicadores.

Não entra:

- **Documento oficial** de aluno ou funcionário. É [54](54-gestao-de-documentos-tres-contextos.md).
- **Arquivo morto** de documentos escolares. É [67](67-livros-digitais-e-arquivo-morto-por-portal.md).
- **Pedido de compra** do acervo. Fica em suprimentos (BIB-03).
- **Cobrança de multa.** Gera fatura no financeiro, como em [18](18-regras-modulos-2.md).
- **Sala de reunião e de aula.** Usa o cadastro de recursos de [44](44-agendamento-ambientes-equipamentos.md).

---

## 3. Acervo e exemplares

- **Item** é a obra: título, autores, ISBN ou ISSN, editora, edição, ano, idioma, categoria e sinopse.
- **Exemplar** é a cópia física: código de barras único, localização (estante e prateleira), estado de conservação e situação.
- **Situação do exemplar:** `disponivel`, `emprestado`, `reservado`, `em_manutencao`, `baixado`.
- **Item digital** tem arquivo, licença e número de licenças simultâneas (seção 8).
- **Tombamento:** código de tombamento é único na unidade. O acervo fica só no módulo de biblioteca, com valor de aquisição. Não entra no patrimônio (BIB-02).

---

## 4. Perfis e prazos

| Perfil | Empréstimos simultâneos | Prazo | Renovação |
|---|---|---|---|
| Aluno | 3 itens | 7 dias | Até 2 vezes, se não houver reserva de outro usuário |
| Professor | 5 itens | 30 dias | Mesma regra do aluno |
| Servidor | 5 itens | 30 dias | Mesma regra do aluno |

**Regra:** os valores da tabela são o ponto de partida de toda unidade nova. A escola altera por perfil e por categoria de item. **Decidido** em 03/11/2026 (BIB-04).

---

## 5. Empréstimo, devolução e reserva

### 5.1 Empréstimo

- Só com usuário com vínculo ativo: matrícula ativa para aluno, vínculo ativo para professor e servidor ([46](46-matricula-e-rematricula-por-portal.md) e [39](39-departamento-pessoal-rh-medicina-por-portal.md)).
- Bloqueado com multa em aberto ou item atrasado.
- Retirada com busca por código de barras ou título. Confirmação de retirada pode ser assinada, se a escola exigir.

### 5.2 Renovação

- Bloqueada se o item tiver reserva pendente de outro usuário.
- As renovações são contadas no empréstimo. Depois do limite, só devolução.

### 5.3 Reserva

- Fila por item indisponível. Quando o exemplar volta, o próximo da fila é avisado ([57](57-notificacoes-por-portal.md)).
- Reserva tem prazo de retirada. Expirado, passa ao próximo da fila.

### 5.4 Devolução

- Devolução dentro da tolerância baixa a multa automaticamente.
- Exemplar devolvido em estado danificado vira `em_manutencao` até a avaliação do bibliotecário.

---

## 6. Multas

- Valor por dia de atraso e teto por item são configurados pela escola, por categoria.
- Multa confirmada gera fatura no financeiro ([18](18-regras-modulos-2.md)). A baixa da fatura volta para a biblioteca.
- Isenção exige justificativa e aprovação do bibliotecário ou da coordenação (BIB-06). Quem isenta não isenta a própria multa.
- O responsável financeiro vê só valor e situação da multa, sem título do livro. Regra de [31](31-matriz-portais-modulos.md) e da v1.

---

## 7. Inventário e baixa

- Inventário por estante, setor ou geral. Contagem com leitor de código de barras ou QR.
- Divergências (não encontrado, fora do lugar) geram relatório.
- Baixa por extravio exige aprovação do bibliotecário. Como o acervo não é patrimônio (BIB-02), a baixa não passa pelo patrimônio.
- Doação e descarte seguem regra própria: lista, termo e aprovação da gestão. Descarte de obra rara exige justificativa.

---

## 8. Biblioteca digital

- E-books e PDFs com licença de uso. Quando a licença tem limite, o número de empréstimos simultâneos é controlado e expira sozinho.
- Leitura embutida, sem download quando a licença exigir.
- Marca d'água com identificação do leitor é dado pessoal. Só com base legal confirmada (BIB-05).
- Histórico de leitura é dado do aluno. Não aparece para professor nem responsável.

---

## 9. Salas de leitura

- Salas e cabines são recursos de [44](44-agendamento-ambientes-equipamentos.md), com capacidade e regra de reserva. Não há cadastro de sala próprio na biblioteca.
- Reserva por aluno ou professor, com horário e duração máxima.
- Check-in obrigatório para validar a reserva.

---

## 10. Empréstimo entre unidades

- Unidades têm banco próprio ([03](03-dominio-tenancy.md)). Empréstimo entre unidades exige transferência de registro, não consulta direta ao banco da outra unidade.
- **Decidido** em 03/11/2026 (BIB-01): o empréstimo é pedido pela unidade de destino e aprovado pela unidade de origem. Só o registro do exemplar e do usuário é transferido.

---

## 11. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Ver métricas agregadas de uso, sem dado de acervo ou empréstimo | Ver acervo, empréstimo, multa ou histórico de leitura | P |
| **Gestão** | Ver indicadores e relatórios de circulação. Aprovar baixa e descarte | Emprestar, isentar multa ou editar acervo sem perfil de biblioteca | E |
| **Bibliotecário** (perfil da unidade) | Gerir acervo, empréstimo, multa, inventário, salas e biblioteca digital | Aprovar a própria isenção de multa | E |
| **Auxiliar de biblioteca** (perfil da unidade) | Emprestar e devolver. Lançar reserva | Gerir acervo. Isentar multa | E |
| **Coordenação** | Ver relatórios de uso por curso e disciplina | Editar acervo ou empréstimo | E |
| **Professor** | Consultar catálogo. Emprestar com prazo próprio. Reservar sala. Ver os próprios empréstimos | Ver empréstimo ou multa de outro usuário | E |
| **Aluno** | Consultar catálogo. Emprestar, reservar e renovar. Ver as próprias multas. Biblioteca digital | Ver empréstimo ou histórico de leitura de colega | E |
| **Responsáveis** | Ver empréstimos e multas do dependente, só leitura | Pagar, isentar ou ver título e histórico de leitura | E, só dependentes com vínculo ativo |
| **Responsável financeiro** (função dentro de responsáveis) | Ver valor e situação da multa do aluno sob sua responsabilidade, com link para quitar no financeiro | Ver título, categoria ou histórico | E |
| **Terceiros** | Nada por padrão. Acesso só por permissão explícita da entidade | Qualquer item sem permissão | E |

---

## 12. Integrações

| Módulo | Relação |
|---|---|
| Acadêmico ([46](46-matricula-e-rematricula-por-portal.md), [60](60-turmas-e-grade-de-horarios-por-portal.md)) | Validação de matrícula ativa. Turma e disciplina para relatórios |
| Pessoas ([39](39-departamento-pessoal-rh-medicina-por-portal.md)) | Vínculo ativo de professor e servidor |
| Financeiro ([18](18-regras-modulos-2.md)) | Fatura de multa e baixa |
| Suprimentos ([17](17-regras-modulos.md)) | Aquisição: pedido de compra e nota fiscal |
| Patrimônio ([19](19-regras-modulos-3.md), seção 8) | Baixa de item patrimonial |
| Recursos ([44](44-agendamento-ambientes-equipamentos.md)) | Salas e cabines |
| Plano de ensino ([64](64-planos-de-aula-e-de-ensino-por-portal.md)) | Bibliografia referencia o acervo quando o item existe |
| Busca ([21](21-busca-e-armazenamento.md)) | Busca no acervo, com o escopo de permissão |
| Notificações ([57](57-notificacoes-por-portal.md)) | Vencimento, atraso, reserva liberada |
| Relatórios ([56](56-configuracoes-e-relatorios-lacunas.md), seção 7) | Circulação e busca geral de bibliografia |

---

## 13. Pendências

| # | Pendência | Tipo |
|---|---|---|
| BIB-01 | Empréstimo entre unidades (seção 10) | **Decidido** em 03/11/2026: sim, com pedido e aprovação da origem |
| BIB-02 | O acervo é patrimônio ou fica só na biblioteca (seções 3 e 7) | **Decidido** em 03/11/2026: só na biblioteca. Confirmar com (contábil) a classificação do acervo |
| BIB-03 | Aquisição do acervo (seção 2) | **Decidido** em 03/11/2026: pelo suprimentos, com pedido de compra e nota fiscal |
| BIB-04 | Limites, prazos e renovações por perfil (seção 4) | **Decidido** em 03/11/2026: valor inicial da plataforma, que a escola ajusta |
| BIB-05 | Marca d'água de leitura digital com identificação do leitor: base legal e licença do editor (seção 8) | (jurídico) |
| BIB-06 | Quem pode isentar multa (seção 6) | **Decidido** em 03/11/2026: bibliotecário ou coordenação, sem isentar a própria multa |
| BIB-07 | Guarda de histórico de leitura e de empréstimo, e prazo de eliminação | (jurídico) |
| BIB-08 | DDL: reescrever com `unidade_uuid`, chave interna e `uuid` do padrão de [51](51-ddl-modulos-novos.md). Corrige T-01 | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.13. Revisão do owner pendente (DDL-01). Corrige T-01 |

---

## 14. Critérios de aceite

- [ ] Empréstimo com multa em aberto é recusado (teste).
- [ ] Reserva é liberada ao próximo da fila na devolução (teste).
- [ ] Renovação com reserva de outro usuário é recusada (teste).
- [ ] Usuário sem vínculo ativo não empresta (teste de integração com [46](46-matricula-e-rematricula-por-portal.md)).
- [ ] Responsável não vê título nem histórico de leitura (teste de isolamento).
- [ ] Responsável financeiro não vê título nem categoria (varredura da API de multa).
- [ ] Bibliotecário não isenta a própria multa (teste).
- [ ] Empréstimo entre unidades não consulta o banco da outra unidade (teste de isolamento).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
