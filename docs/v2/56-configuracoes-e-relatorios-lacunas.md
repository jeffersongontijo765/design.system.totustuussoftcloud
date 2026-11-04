# 56 — Configurações e Relatórios: Cobertura e Lacunas

> Parte do [SDD v2](00-README.md). Referência: menus de Configurações, Relatórios da Secretaria, Relatórios do Diário escolar, Relatórios do Financeiro e Relatórios da Biblioteca, colados pelo autor em 03/11/2026 a partir do sistema iScholar. Acadêmico em [55](55-academico-verificacao-e-lacunas.md). Auditoria em [29](29-auditoria.md). Minimização de dado em [07](07-privacidade-lgpd.md).
> **Veredito:** o SDD **não tem especificação de relatórios**. Muitos itens dependem de módulos que ainda estão em lacuna ([55](55-academico-verificacao-e-lacunas.md)). Nenhum relatório do menu está especificado como relatório.

---

## 1. Resposta direta

Atualizado em 04/11/2026: feriados ([58](58-calendario-e-eventos-por-portal.md)), campos personalizados ([72](72-campos-personalizados-por-portal.md)) e tipos de justificativa de falta ([61](61-diario-escolar-por-portal.md)) passaram a coberto. A regra geral de relatórios e o catálogo por módulo estão no [69](69-relatorios-e-censo-por-portal.md), seções 2 e 3. As contagens abaixo são as da verificação original e ficam como histórico.

| Área | Itens no menu | Cobertos | Parciais | Lacunas | Fora do escopo |
|---|---|---|---|---|---|
| Configurações | 19 | 5 | 6 | 6 | 2 (rejeitado, incluindo "Outras") |
| Relatórios da Secretaria | 35 linhas (com repetições) | 6 | 8 | 19 | 2 (senhas) |
| Relatórios do Diário escolar | 33 | 0 | 3 | 30 | 0 |
| Relatórios do Financeiro | 27 | 0 | parcial em 5 grupos | lacuna em 3 grupos | 0 |
| Relatórios da Biblioteca | 4 | 0 | 0 | 4 | 0 |

Contagem feita a partir das tabelas das seções 2 a 7. Financeiro é contado por grupo, porque alguns grupos misturam itens cobertos e lacunas. "Coberto" significa que o documento de origem define regra, estado e portal. "Parcial" significa que o item aparece, mas falta regra. "Lacuna" significa que não aparece.

---

## 2. Configurações

| Item | Situação | Onde |
|---|---|---|
| Painel do aluno e do professor | Parcial | [31](31-matriz-portais-modulos.md), seção 2. Sem tela de configuração |
| Agenda iScholar | Lacuna | Não está claro o que é. **Definir** |
| Número de matrícula | Lacuna | Regra de numeração não especificada. Ver [46](46-matricula-e-rematricula-por-portal.md) |
| Financeiro (configurações gerais) | Parcial | [18](18-regras-modulos-2.md), [34](34-pagamentos-fiscal-bancos-por-portal.md) |
| Mensagens de carnê | Lacuna | Modelo de carnê não especificado. Ver [53](53-pacote-documentos-e-contratos.md), DC-25 |
| Mensagens de NFS-e | Parcial | [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 5 |
| Gerenciar feriados | Coberto | [58](58-calendario-e-eventos-por-portal.md), seções 3 e 4: dia não letivo (feriado, recesso, ponto facultativo) no calendário da unidade |
| Campos personalizados | Coberto | [72](72-campos-personalizados-por-portal.md) (CFG-06) |
| Matrícula online | Coberto | [46](46-matricula-e-rematricula-por-portal.md), seção 3 |
| Gerenciar tokens | Coberto | [06](06-identidade-acesso.md) e [04](04-api.md) |
| Fuso horário | Parcial | Horários em UTC, com exibição no fuso da unidade ([44](44-agendamento-ambientes-equipamentos.md)). Configuração por unidade não especificada |
| Webhooks | Coberto | [16](16-integracoes-externas.md), [04](04-api.md) |
| Gerenciar IES | Parcial | [03](03-dominio-tenancy.md) cobre entidade e unidade. Cadastro de IES (credenciamento) não especificado |
| Preferências de comunicação | Parcial | Consentimento por finalidade em [32](32-atendimento-privacidade-por-portal.md), seção 3.2. Sem tela de canal preferido |
| Tipos de descontos | Parcial | [18](18-regras-modulos-2.md), seção 2.6 (acumulação decidida). Tipos não listados |
| Catraca | Coberto | [35](35-acesso-e-seguranca-fisica-por-portal.md) |
| Tipos de justificativa de falta | Coberto | [61](61-diario-escolar-por-portal.md), seção 4.2 |
| Integração de parceiros | Coberto | [16](16-integracoes-externas.md) |
| Outras configurações | Não aplicável | Genérico |

---

## 3. Relatórios: regra geral que falta

Atualizado em 04/11/2026: a regra geral foi escrita no [69](69-relatorios-e-censo-por-portal.md), seção 2 (tipos, ciclo, formatos e regras), com o catálogo por módulo na seção 3. O texto abaixo é a análise original.

Nenhum documento define como um relatório é gerado. Proposta, para ser validada:

1. **Relatório pertence ao módulo que tem o dado.** Não existe "relatório central". Cada módulo expõe os seus relatórios, com a mesma regra de acesso.
2. **Três tipos:** operacional (lista do dia), gerencial (totais e indicadores) e regulatório (formato exigido por órgão, como o censo e a ficha SEE).
3. **Permissão por escopo.** O relatório respeita o mesmo filtro de portal, unidade e turma que a tela. Relatório não é atalho para dado que a tela não mostra.
4. **Minimização.** Relatório com dado pessoal sai só com os campos necessários. Aniversariantes usa mês e dia, não a data completa de nascimento.
5. **Exportação é evento de auditoria** ([29](29-auditoria.md)), com o campo `portal` e o filtro usado.
6. **Agregado com mínimo de grupo**, como em [41](41-formularios-e-pesquisas.md), seção 3, quando o relatório for sobre grupo pequeno.
7. **Senha e segredo nunca aparecem em relatório.** Exceção decidida pelo autor em 03/11/2026: a secretaria gera relatório com os dados de acesso do responsável (usuário e link de acesso). O relatório só pode ser enviado ao próprio responsável, nunca a aluno nem a terceiro, e segue a LGPD. **Decidido pelo autor em 03/11/2026:** a senha não aparece em texto. O relatório traz o usuário e um link de primeiro acesso, de uso único e com validade curta. O responsável cria a própria senha ao acessar.
8. **Foto em relatório** (carômetro) só com consentimento específico ([35](35-acesso-e-seguranca-fisica-por-portal.md), seção 6).

---

## 4. Relatórios da Secretaria

| Item | Situação | Dependência |
|---|---|---|
| Alunos com mais de uma matrícula | Lacuna | Regra de vínculo ativo, [46](46-matricula-e-rematricula-por-portal.md) |
| Alunos por transporte escolar | Parcial | [38](38-portal-de-terceiros-prestadores.md). Dado de localização, não entra no relatório |
| Aniversariantes | Lacuna | Minimização, regra 4 da seção 3 |
| Assinatura eletrônica | Parcial | [33](33-contratos-por-portal.md), [54](54-gestao-de-documentos-tres-contextos.md) |
| Calendário por turma | Lacuna | Calendário escolar ([55](55-academico-verificacao-e-lacunas.md), item 1) |
| Capa de pasta por turma | Lacuna | Turma ([55](55-academico-verificacao-e-lacunas.md), item 3) |
| Carômetro | Lacuna | Foto, regra 8 da seção 3 |
| Compara matrículas entre períodos letivos | Lacuna | Período letivo |
| Declaração de transferência | Parcial | [48](48-gerador-de-documentos-por-portal.md) (tipo a incluir) |
| Declarações | Coberto | [48](48-gerador-de-documentos-por-portal.md), [53](53-pacote-documentos-e-contratos.md) |
| Documentos pendentes (Bilhete) | Parcial | [46](46-matricula-e-rematricula-por-portal.md), M-08; [54](54-gestao-de-documentos-tres-contextos.md) |
| Ficha de matrícula SEE | Lacuna | Formato da Secretaria de Educação **a confirmar** |
| Ficha de recadastramento | Lacuna | Não especificado |
| Grade curricular | Lacuna | [55](55-academico-verificacao-e-lacunas.md), item 1 |
| Histórico escolar e alunos | Parcial | [48](48-gerador-de-documentos-por-portal.md), DOC-03 |
| Horário do professor por período | Lacuna | Grade de horários ([55](55-academico-verificacao-e-lacunas.md), item 3) |
| Horários da semana | Lacuna | Grade de horários |
| Horários da turma e dos professores | Lacuna | Grade de horários |
| Irmãos | Lacuna | Vínculo de família, [07](07-privacidade-lgpd.md) |
| Lista de presença por disciplina e por turma | Lacuna | Diário ([55](55-academico-verificacao-e-lacunas.md), item 4) |
| Lista de professores | Parcial | [37](37-planejamento-e-empenho.md), carga docente |
| Lista geral de alunos | Parcial | [17](17-regras-modulos.md), seção 4.2 |
| Matrículas | Coberto | [46](46-matricula-e-rematricula-por-portal.md) |
| Matrículas ativas | Coberto | [46](46-matricula-e-rematricula-por-portal.md), seção 2 |
| Matrículas e rematrículas | Coberto | [46](46-matricula-e-rematricula-por-portal.md) |
| Ocorrências | Lacuna | [55](55-academico-verificacao-e-lacunas.md), item 6 |
| Ocupação de sala | Coberto | [44](44-agendamento-ambientes-equipamentos.md) |
| Reunião de pais | Parcial | [40](40-aulas-online-por-portal.md), seção 4.1 (reunião 1:1). Reunião coletiva não especificada |
| Responsável por dois ou mais alunos | Lacuna | Vínculo de família |
| Senhas de acesso ao Painel | Parcial | Decidido: relatório de dados de acesso do responsável, só para o próprio responsável. Senha em texto não deve aparecer (regra 7 da seção 3) |
| Senhas do Painel do Professor | Parcial | Mesma regra do painel do responsável, para o professor, sem envio a aluno ou terceiro |
| Sistema avaliativo, detalhamento por disciplina | Lacuna | [55](55-academico-verificacao-e-lacunas.md), item 2 |
| Telefones por tipo | Lacuna | Contato do titular, minimização |
| Total de alunos por turma e por unidade | Lacuna | Turma |
| Atividades complementares e de extensão | Coberto | [46](46-matricula-e-rematricula-por-portal.md), seção 5 |
| Ficha de matrícula e outros formatos oficiais | Lacuna | Formato oficial **a confirmar** |

Observação: a contagem por linha dá mais itens do que a tabela da seção 1, porque alguns itens do menu se repetem em grupos diferentes. A seção 1 usa a contagem do menu colado.

---

## 5. Relatórios do Diário escolar

| Grupo | Itens | Situação | Dependência |
|---|---|---|---|
| Diário eletrônico, capa e composição da turma | 3 | Lacuna | Diário, turma ([55](55-academico-verificacao-e-lacunas.md), itens 3 e 4) |
| Conteúdos curriculares não lançados e registro de conteúdos | 2 | Lacuna | Plano de aula ([55](55-academico-verificacao-e-lacunas.md), item 7) |
| Apuração de frequência, faltas consecutivas, fora do período, justificadas, por divisão, sintético | 7 | Lacuna | Frequência e justificativa ([55](55-academico-verificacao-e-lacunas.md), item 4) |
| Notas: abaixo da média, reprovados, ata de resultados finais, boletim | 4 | Lacuna | Boletim e aprovação ([55](55-academico-verificacao-e-lacunas.md), item 5) |
| Notas: recuperação, consulta por turma e professor, controle de lançamento, detalhamento, ficha individual, notas médias, notas por divisão, notas finais por curso | 11 | Lacuna | Sistema avaliativo ([55](55-academico-verificacao-e-lacunas.md), item 2) |
| Gráficos de desempenho, ranking, gráfico entre turmas | 3 | Parcial | Ranking tem regra em [47](47-simulados-por-portal.md), seção 8, só para simulado |
| Planejamento de aulas: total planejado e ministrado, total de dias | 3 | Lacuna | Planos de aula ([55](55-academico-verificacao-e-lacunas.md), item 7) |

---

## 6. Relatórios do Financeiro

> **Decidido em 03/11/2026: escopo financeiro completo** (CFG-04). Cheques, caixa, DRE e fluxo de caixa precisam de especificação própria, que ainda não existe. Abaixo, o estado atual.

| Grupo | Itens | Situação | Dependência |
|---|---|---|---|
| Recebimentos: alunos com e sem parcelas válidas, boletos, cheques recebidos, contas a receber, expectativa, ficha por turma, boletos por turma, montante negociado, valor mensal por aluno, visão por competência | 10 | Parcial para boletos e contas a receber ([18](18-regras-modulos-2.md), [34](34-pagamentos-fiscal-bancos-por-portal.md)). Demais, lacuna | Cheques e caixa não têm especificação |
| Pagamentos: cheques emitidos, contas a pagar, custos e despesas | 3 | Lacuna | [17](17-regras-modulos.md), seção 2 (financeiro sem detalhe) |
| Fluxo de caixa: demonstrativo, DRE, fluxo diário | 3 | Lacuna | DRE citado em [15](15-validacoes.md) e [21](21-busca-e-armazenamento.md), sem especificação |
| Inadimplência: carta de cobrança, cobrança e inadimplentes, histórico de cobrança, inadimplência | 4 | Parcial | [18](18-regras-modulos-2.md), [26](26-sdd-juridico-regulatorio.md). Carta de cobrança depende de DC-13 |
| Conciliação bancária e caixas: extrato por usuário, extrato de conta, fechamento de caixa | 4 | Parcial | Conciliação em [17](17-regras-modulos.md), seção 2.5. Caixa não especificado |
| Outras: comprovante de IRPF, histórico de movimentações, parcelas de serviços financeiros | 3 | Lacuna | Comprovante de IRPF depende de regra fiscal **a confirmar** |

---

## 7. Relatórios da Biblioteca

| Item | Situação | Dependência |
|---|---|---|
| Busca geral de bibliografia e exemplares | Lacuna | Biblioteca sem especificação ([55](55-academico-verificacao-e-lacunas.md), item 11) |
| Código de barras | Lacuna | Idem |
| Empréstimos de exemplares | Lacuna | Idem |
| Etiquetas | Lacuna | Idem |

---

## 8. Decisões necessárias

| # | Decisão | Opções |
|---|---|---|
| CFG-01 | "Agenda iScholar" | **Decidido** em 03/11/2026: não entra. Eventos ficam no calendário e no módulo de eventos, especificados em [58](58-calendario-e-eventos-por-portal.md) |
| CFG-02 | Carômetro e ficha com foto | **Decidido** em 03/11/2026: entram, só com consentimento específico por aluno |
| CFG-03 | Relatório de dados de acesso do responsável | **Decidido** em 03/11/2026: a secretaria gera, só para o responsável, com LGPD. Senha não aparece: vai link de primeiro acesso de uso único, com validade curta |
| CFG-04 | Financeiro: escopo | **Decidido** em 03/11/2026: escopo financeiro completo, com cheques, caixa, DRE e fluxo de caixa. Especificado em [71](71-financeiro-completo-por-portal.md) |
| CFG-05 | Relatórios regulatórios: quais formatos oficiais | **Decidido** em 03/11/2026: censo, ficha SEE e SINAES. Ficha de recadastramento fica para configuração da unidade. Ver [69](69-relatorios-e-censo-por-portal.md), seção 5 |
| CFG-06 | Campos personalizados: entram no escopo? | **Decidido** em 03/11/2026: sim, definidos por entidade ou por unidade, com valores no banco da unidade. Ver [72](72-campos-personalizados-por-portal.md) |

---

## 9. Ordem de fechamento

Os relatórios dependem dos módulos. Por isso, a ordem é a mesma de [55](55-academico-verificacao-e-lacunas.md), seção 3, e depois os relatórios de cada módulo. Os relatórios de financeiro e de biblioteca dependem de especificações ainda não escritas.

---

## 10. Critérios de aceite

- [ ] Cada item do menu de referência tem um documento de origem, ou uma decisão de "fora do escopo".
- [ ] Nenhum relatório mostra senha, token ou segredo (varredura).
- [ ] Relatório com dado pessoal exporta só os campos necessários (teste de minimização).
- [ ] Exportação gera evento de auditoria com o filtro usado (teste).
- [ ] Relatório respeita o mesmo escopo da tela de origem (teste de isolamento).
