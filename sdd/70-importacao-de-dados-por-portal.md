# 70 — Importação de Dados e Carga Inicial, por Portal

> Parte do [SDD v2](00-README.md). Décima terceira e última lacuna da ordem de [55](55-academico-verificacao-e-lacunas.md), seção 3. Regra geral de importação (simulação, erro por linha, limite e idempotência) em [15](15-validacoes.md), seção 5. Carga de sistema legado por arquivo, sem acesso direto ao banco de terceiros, em [16](16-integracoes-externas.md). Cada tipo de dado segue o módulo de origem: estrutura ([59](59-estrutura-academica-por-portal.md)), turmas ([60](60-turmas-e-grade-de-horarios-por-portal.md)), matrícula ([46](46-matricula-e-rematricula-por-portal.md)), diário e boletim ([61](61-diario-escolar-por-portal.md), [62](62-boletim-e-conselho-de-classe-por-portal.md)), prontuário ([66](66-prontuario-e-portfolio-do-aluno-por-portal.md)), biblioteca ([68](68-biblioteca-por-portal.md)) e financeiro ([18](18-regras-modulos-2.md)). Notificação em massa em [57](57-notificacoes-por-portal.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 13 do acadêmico. A v1 tem importação em lote por CSV com validação e relatório de erros (`spec_gestao_academica_completo.md`, seção 15). Esta versão define a ordem, as regras de domínio e o que a importação não pode fazer.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Importação tem regra? | **Parcial.** A regra geral de [15](15-validacoes.md) existe. Falta ordem por tipo, regra de domínio e tratamento do histórico |
| Carga de sistema anterior? | **Parcial.** [16](16-integracoes-externas.md) proíbe acesso direto ao banco de terceiro. Falta o processo |
| Importação pode contornar regra? | **Não, por regra desta especificação.** Ver seção 3 |

---

## 2. Tipos e ordem

A ordem segue a dependência. Nenhum tipo entra antes do que ele referencia.

| Ordem | Tipo | Depende de | Módulo |
|---|---|---|---|
| 1 | Pessoas: alunos, responsáveis, professores, servidores | Nada | [14](14-integracao-modulos.md), seção 3 e [46](46-matricula-e-rematricula-por-portal.md) |
| 2 | Estrutura: tipos de curso, cursos, disciplinas, grades, sistema avaliativo, períodos | 1 | [59](59-estrutura-academica-por-portal.md) |
| 3 | Calendário e salas | 2 | [58](58-calendario-e-eventos-por-portal.md), [44](44-agendamento-ambientes-equipamentos.md) |
| 4 | Turmas e enturmação | 2 e 3 | [60](60-turmas-e-grade-de-horarios-por-portal.md) |
| 5 | Matrículas ativas | 1, 2 e 4 | [46](46-matricula-e-rematricula-por-portal.md) |
| 6 | Histórico: notas, faltas, situação final de períodos fechados | 4 e 5 | [61](61-diario-escolar-por-portal.md), [62](62-boletim-e-conselho-de-classe-por-portal.md) |
| 7 | Documentos e prontuário | 1 | [54](54-gestao-de-documentos-tres-contextos.md), [66](66-prontuario-e-portfolio-do-aluno-por-portal.md) |
| 8 | Acervo da biblioteca | 2 | [68](68-biblioteca-por-portal.md) |
| 9 | Saldos e parcelas em aberto | 5 | [18](18-regras-modulos-2.md) |

---

## 3. O que a importação não faz

A importação entra pelos mesmos caminhos de regra que a tela. Por isso:

- **Nota fora da escala** é recusada, como na tela ([59](59-estrutura-academica-por-portal.md), seção 4).
- **Matrícula acima da capacidade** vai para a lista de espera ou é recusada com motivo ([60](60-turmas-e-grade-de-horarios-por-portal.md), seção 2.4).
- **Aluno sem vínculo válido** de responsável não é importado como ativo ([07](07-privacidade-lgpd.md)).
- **Histórico não recalcula regra de período fechado.** A situação final vem do arquivo, com a versão do sistema avaliativo que o arquivo declara. Se a versão não existe no sistema, a linha é rejeitada.
- **Não gera cobrança retroativa.** Parcela já paga na origem entra como paga. Parcela em aberto entra com a data da origem, sem nova multa.
- **Não dispara aviso em massa.** Carga histórica entra com flag de histórico, e nenhuma notificação é enviada por ela ([57](57-notificacoes-por-portal.md)).

---

## 4. Processo

1. **Modelo.** A plataforma publica um modelo de arquivo por tipo, com cabeçalho, tipos de campo e chave externa de origem. Ver seção 4.1.
2. **Envio.** O arquivo é enviado com tamanho e tipo validados ([15](15-validacoes.md), seção 5).
3. **Simulação.** O sistema valida tudo e mostra o relatório, sem gravar. Mostra quantas linhas entram, quantas são rejeitadas e por quê.
4. **Confirmação.** A pessoa que importa confirma o lote. A confirmação fica em auditoria.
5. **Gravação.** O lote grava em transação por lote. Linha rejeitada não bloqueia as outras, mas o lote fica marcado como parcial.
6. **Desfazer.** O lote pode ser desfeito enquanto não houver registro posterior dependente dele. Depois disso, só correção por novo lote.
7. **Rejeitados.** Relatório de rejeitados, com linha e motivo, para correção e novo envio.
8. **Descarte do arquivo.** O arquivo de origem é apagado após a gravação, e fica só o hash e o relatório. Prazo em IMP-04.

**Idempotência:** a chave externa de origem evita duplicar o mesmo registro em reenvio. Reenvio do mesmo lote não cria registro novo.

### 4.1 Modelos de arquivo (IMP-05)

**Formato comum a todos os modelos:**

| Item | Regra |
|---|---|
| Arquivos | Planilha (`.xlsx`, uma aba por modelo) e CSV. Os dois têm as mesmas colunas, na mesma ordem |
| CSV | UTF-8, separador ponto e vírgula, primeira linha com o nome das colunas |
| Data | `AAAA-MM-DD`. Data em outro formato é recusada, para não confundir dia e mês |
| Número | Vírgula como separador decimal, sem separador de milhar |
| Valor em dinheiro | Reais com duas casas. O sistema converte para centavos ([71](71-financeiro-completo-por-portal.md)) |
| CPF | Só dígitos, com dígito verificador conferido ([15](15-validacoes.md)) |
| Chave externa | Coluna `chave_origem` obrigatória em todo modelo. É o identificador no sistema anterior e garante a idempotência |
| Versão | Cada modelo tem versão no nome do arquivo e numa linha de comentário da planilha. Arquivo de versão que já saiu do prazo de aceitação (ver Publicação, abaixo) é recusado com aviso da versão atual |
| Coluna a mais | Recusada, para não esconder dado que não tem destino. Campo personalizado entra pela coluna com a chave do campo ([72](72-campos-personalizados-por-portal.md)) |

**Colunas obrigatórias por modelo**, na ordem da seção 2:

| Modelo | Colunas obrigatórias | Observação |
|---|---|---|
| 1. Pessoas | `chave_origem`, `tipo_pessoa`, `nome`, `cpf` ou `documento_estrangeiro`, `nascimento`, `email` ou `telefone` | Responsável tem `chave_origem_dependente` e `tipo_vinculo`. Aluno menor sem responsável não fica ativo (seção 3) |
| 2. Estrutura | `chave_origem`, `tipo_registro` (curso, disciplina, grade, período), `codigo`, `nome`, `carga_horaria` | Sistema avaliativo é configurado na tela, não importado |
| 3. Calendário e salas | `chave_origem`, `tipo_registro` (dia, período, sala), `data_ou_codigo`, `descricao` | Sala tem `capacidade` |
| 4. Turmas e enturmação | `chave_origem`, `codigo_turma`, `curso`, `periodo`, `turno`, `capacidade`, `chave_origem_aluno` | Enturmação usa uma linha por aluno |
| 5. Matrículas | `chave_origem`, `chave_origem_aluno`, `codigo_turma`, `data_matricula`, `situacao` | Só matrícula ativa. Capacidade segue a seção 3 |
| 6. Histórico | `chave_origem`, `chave_origem_aluno`, `periodo`, `disciplina`, `nota_final`, `faltas`, `situacao_final`, `versao_sistema_avaliativo` | Só período fechado. Aprovação da coordenação (seção 6) |
| 7. Documentos | `chave_origem`, `chave_origem_pessoa`, `tipo_documento`, `nome_arquivo` | O arquivo vai num pacote compactado junto, com o mesmo nome. Dado de saúde segue IMP-03 |
| 8. Acervo | `chave_origem`, `titulo`, `autor`, `isbn` ou `codigo_interno`, `exemplares` | Item sem ISBN usa código interno |
| 9. Saldos e parcelas | `chave_origem`, `chave_origem_matricula`, `vencimento`, `valor`, `situacao` (paga, em aberto), `data_pagamento` | Sem multa nova (seção 3). Aprovação do financeiro |

**Publicação:** o portal do desenvolvedor publica os modelos, sem dado. A empresa aprova cada versão antes da publicação. Mudança de coluna gera nova versão, e a anterior continua aceita por 90 dias.

---

## 5. Dado sensível e dado de terceiros

- Laudos, diagnósticos e dados de saúde só são importados se a regra de [66](66-prontuario-e-portfolio-do-aluno-por-portal.md), seção 2.3, permitir. Ver IMP-03.
- Arquivo de origem tem dado pessoal. Fica em armazenamento restrito, cifrado, pelo tempo do processo.
- Nenhum acesso direto ao banco do sistema anterior ([16](16-integracoes-externas.md)).

---

## 6. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos de arquivo, sem dado. Orientar a importação | Importar ou ver dado de entidade, nem o conteúdo de lote | P |
| **Gestão** | Autorizar a importação inicial. Ver o relatório de lote | Importar sem a secretaria. Ver dado sensível do arquivo | E |
| **Secretaria** | Importar pessoas, estrutura, turmas, matrículas, documentos e acervo. Desfazer lote | Importar histórico sem a coordenação. Importar saldo sem o financeiro | E |
| **Coordenação** | Importar histórico de período fechado, com aprovação | Importar pessoa ou matrícula | E |
| **Financeiro** (perfil da unidade) | Importar saldos e parcelas em aberto | Importar notas ou documentos | E |
| **Professor** | Nada | Qualquer item de importação | E |
| **Aluno** | Nada | Qualquer item de importação | E |
| **Responsáveis** | Nada | Qualquer item de importação | E |
| **Terceiros** | Nada | Qualquer item de importação | E |

---

## 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| IMP-01 | Quem executa a importação inicial (seção 6) | **Decidido** em 03/11/2026: a entidade, pela secretaria. A equipe da empresa só orienta |
| IMP-02 | Histórico importado gera notificação (seção 3) | **Decidido** em 03/11/2026: não |
| IMP-03 | Laudos e dados de saúde na importação: aceitar, ou bloquear e tratar na seção de saúde | (jurídico) |
| IMP-04 | Prazo de retenção do arquivo de origem depois da gravação (seção 4, passo 8) | (jurídico) |
| IMP-05 | Modelos de arquivo por tipo: publicar em planilha e em CSV | **Escrito** na seção 4.1. Revisão do owner pendente: a empresa aprova cada versão |
| IMP-06 | DDL: lote, linha, erro, chave externa, mapeamento de campo e histórico de desfazer | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.15. Revisão do owner pendente (DDL-01) |

---

## 8. Critérios de aceite

- [ ] Simulação não grava nenhuma linha (teste).
- [ ] Reenvio do mesmo lote não duplica registro (teste de idempotência).
- [ ] Nota fora da escala é rejeitada na importação (teste de integração com [59](59-estrutura-academica-por-portal.md)).
- [ ] Matrícula acima da capacidade não entra como ativa (teste).
- [ ] Histórico com versão de sistema avaliativo inexistente é rejeitado (teste).
- [ ] Importação de histórico não dispara notificação (teste de integração com [57](57-notificacoes-por-portal.md)).
- [ ] Arquivo de origem é apagado depois da gravação e fica só o hash (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
