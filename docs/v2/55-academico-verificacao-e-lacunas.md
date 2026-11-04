# 55 — Verificação do Acadêmico: Cobertura, Lacunas e Ordem de Fechamento

> Parte do [SDD v2](00-README.md). Referência de comparação: menu do sistema iScholar, colado pelo autor em 03/11/2026, e o mapa de páginas acadêmico da v1 ([`spec_gestao_academica_completo.md`](anexo-v1/spec_gestao_academica_completo.md), seção 2). Regras já existentes em [17](17-regras-modulos.md), seção 4. Matrícula em [46](46-matricula-e-rematricula-por-portal.md). Agendamento em [44](44-agendamento-ambientes-equipamentos.md). Sala online em [40](40-aulas-online-por-portal.md). Documentos em [48](48-gerador-de-documentos-por-portal.md) e [54](54-gestao-de-documentos-tres-contextos.md). Simulados em [47](47-simulados-por-portal.md). Preceptoria em [42](42-preceptoria-por-portal.md).
> **Veredito:** o acadêmico **não está completo**. A parte de matrícula, documentos e salas está especificada. A estrutura acadêmica, a grade de horários, notas, frequência, diário, conselho de classe e planos pedagógicos estão só citados.

---

## 1. Resposta direta

Atualizado em 04/11/2026: os itens que esta verificação marcava como lacuna foram especificados nos documentos 58 a 70. A tabela abaixo aponta onde cada um está.

| Pergunta | Veredito |
|---|---|
| Matrícula e rematrícula estão completas? | **Sim**, em [46](46-matricula-e-rematricula-por-portal.md), com estados, janelas, condicional e trancamento |
| Estrutura acadêmica (cursos, grades, disciplinas, períodos, calendário) está especificada? | **Sim**, em [59](59-estrutura-academica-por-portal.md) e [58](58-calendario-e-eventos-por-portal.md) |
| Notas, boletim e aprovação? | **Sim**, em [61](61-diario-escolar-por-portal.md), seção 5, e [62](62-boletim-e-conselho-de-classe-por-portal.md) |
| Frequência, faltas e justificativas? | **Sim**, em [61](61-diario-escolar-por-portal.md), seções 3 e 4 |
| Diário, planos de aula e de ensino? | **Sim**, em [61](61-diario-escolar-por-portal.md) e [64](64-planos-de-aula-e-de-ensino-por-portal.md) |
| Ocorrências disciplinares? | **Sim**, em [63](63-ocorrencias-disciplinares-por-portal.md) |
| Conselho de classe, recuperação paralela, portfólio? | **Sim**, em [62](62-boletim-e-conselho-de-classe-por-portal.md) (conselho e recuperação) e [66](66-prontuario-e-portfolio-do-aluno-por-portal.md) (portfólio) |
| Estágio, TCC? | **Sim**, em [65](65-estagio-e-tcc-por-portal.md) |
| Livros digitais (registro e atas)? | **Sim**, em [67](67-livros-digitais-e-arquivo-morto-por-portal.md) |
| Relatórios acadêmicos e censo? | **Sim**, em [69](69-relatorios-e-censo-por-portal.md) |

---

## 2. Mapa: menu iScholar × SDD

Itens do menu de referência, na ordem em que aparecem.

### 2.1 Coordenação

| Item do iScholar | Cobertura no SDD | Situação |
|---|---|---|
| Empresas | Empresa e unidades: [03](03-dominio-tenancy.md) | Coberto no modelo de tenant |
| Unidades escolares | [03](03-dominio-tenancy.md), [44](44-agendamento-ambientes-equipamentos.md) | Coberto |
| Salas de aula | [44](44-agendamento-ambientes-equipamentos.md) | Coberto |
| Cursos | [59](59-estrutura-academica-por-portal.md), seção 3.1 | Coberto |
| Grupos de horários | [60](60-turmas-e-grade-de-horarios-por-portal.md), seção 3 | Coberto |
| Disciplinas | [59](59-estrutura-academica-por-portal.md), seção 3.2 | Coberto |
| Grades curriculares | [59](59-estrutura-academica-por-portal.md), seções 3.3 e 3.5 (equivalência) | Coberto |
| Períodos letivos | [59](59-estrutura-academica-por-portal.md), seção 3.6 | Coberto |
| Funcionários | [39](39-departamento-pessoal-rh-medicina-por-portal.md) | Coberto como RH |
| Documentos (pendentes) | [54](54-gestao-de-documentos-tres-contextos.md), contexto A | Coberto |
| Sistemas avaliativos | [59](59-estrutura-academica-por-portal.md), seção 4 | Coberto |
| Calendários escolares | [58](58-calendario-e-eventos-por-portal.md) | Coberto |
| Planos de pagamento | [18](18-regras-modulos-2.md) e [26](26-sdd-juridico-regulatorio.md) | Coberto no financeiro |

### 2.2 Secretaria

| Item do iScholar | Cobertura no SDD | Situação |
|---|---|---|
| Turmas | [60](60-turmas-e-grade-de-horarios-por-portal.md), seção 2; enturmação em [46](46-matricula-e-rematricula-por-portal.md), M-07 | Coberto |
| Responsáveis | [46](46-matricula-e-rematricula-por-portal.md), [07](07-privacidade-lgpd.md) | Coberto no vínculo |
| Alunos | [17](17-regras-modulos.md), seção 4.2; prontuário em [66](66-prontuario-e-portfolio-do-aluno-por-portal.md) | Coberto |
| Matrículas | [46](46-matricula-e-rematricula-por-portal.md) | Coberto |
| Alunos potenciais | [22](22-crm-canais-e-papeis.md), leads | Coberto no CRM |
| Modelos de documentos | [48](48-gerador-de-documentos-por-portal.md) | Coberto |
| Ocorrências | [63](63-ocorrencias-disciplinares-por-portal.md) | Coberto |
| Solicitações | [32](32-atendimento-privacidade-por-portal.md) e [46](46-matricula-e-rematricula-por-portal.md) | Coberto pelo protocolo |
| Agenda de eventos | [58](58-calendario-e-eventos-por-portal.md), seção 5 | Coberto |
| Processos seletivos | [46](46-matricula-e-rematricula-por-portal.md), seção 4 | Coberto |
| Gabaritos | [47](47-simulados-por-portal.md) e [31](31-matriz-portais-modulos.md), seção 3.6 (leitor próprio ou de terceiro) | Coberto |
| Secretaria digital (portal externo) | [46](46-matricula-e-rematricula-por-portal.md), [48](48-gerador-de-documentos-por-portal.md) | Coberto |
| Relatórios | [69](69-relatorios-e-censo-por-portal.md) e [56](56-configuracoes-e-relatorios-lacunas.md), seção 4 | Coberto |

### 2.3 Diário escolar

| Item do iScholar | Cobertura no SDD | Situação |
|---|---|---|
| Notas | [61](61-diario-escolar-por-portal.md), seção 5; boletim e aprovação em [62](62-boletim-e-conselho-de-classe-por-portal.md) | Coberto |
| Aulas (conteúdo) | [61](61-diario-escolar-por-portal.md), seção 2; planos em [64](64-planos-de-aula-e-de-ensino-por-portal.md) | Coberto |
| Faltas | [61](61-diario-escolar-por-portal.md), seções 3 e 4 | Coberto |
| Relatórios | [69](69-relatorios-e-censo-por-portal.md) e [56](56-configuracoes-e-relatorios-lacunas.md), seção 5 | Coberto |

### 2.4 Outros módulos do menu

| Item | Cobertura | Situação |
|---|---|---|
| Financeiro (parcelas, cobrança, conciliação, NF, cheques, cartões, estoque) | [18](18-regras-modulos-2.md), [20](20-pagamentos-seguranca.md), [34](34-pagamentos-fiscal-bancos-por-portal.md) | Coberto no financeiro. Cheques e estoque de cantina não têm especificação |
| Centros de custo | [71](71-financeiro-completo-por-portal.md), seções 3 e 4 (rateio por centro de custo em lançamento e despesa) | Coberto como atributo; sem cadastro próprio especificado |
| Controle patrimonial | [19](19-regras-modulos-3.md), seção 8 | Coberto |
| Catraca | [35](35-acesso-e-seguranca-fisica-por-portal.md) | Coberto |
| Biblioteca (bibliografias, empréstimos e reservas) | [68](68-biblioteca-por-portal.md) | Coberto |
| Administração (usuários, grupos, integrações, importação, notificações) | [06](06-identidade-acesso.md), [16](16-integracoes-externas.md), [19](19-regras-modulos-3.md), seção 13; importação em [70](70-importacao-de-dados-por-portal.md) | Coberto |
| Ischolar Intelligence | [27](27-inteligencia-artificial-e-portais.md) e [28](28-cobertura-ia-todos-os-modulos.md) | Coberto |

---

## 3. Lacunas do acadêmico, em ordem de dependência

As lacunas abaixo se apoiam umas nas outras. Por isso a ordem importa.

| Ordem | Módulo a especificar | Depende de | Itens do menu que cobre | Situação em 04/11/2026 |
|---|---|---|---|---|
| 1 | **Estrutura acadêmica**: cursos, disciplinas, grades curriculares, períodos letivos, calendário e tipos de curso | Nada | Cursos, disciplinas, grades, períodos, calendários | Especificado em [59](59-estrutura-academica-por-portal.md) e [58](58-calendario-e-eventos-por-portal.md) |
| 2 | **Sistemas avaliativos**: escalas, método de média, recuperação, conceitos, regra de aprovação | 1 | Sistemas avaliativos | Especificado em [59](59-estrutura-academica-por-portal.md), seção 4 |
| 3 | **Turmas e grade de horários**: criação de turma, grupos de horários, enturmação, quadro de aulas | 1 | Turmas, grupos de horários | Especificado em [60](60-turmas-e-grade-de-horarios-por-portal.md) |
| 4 | **Diário**: chamada, faltas, justificativa, notas por período, conteúdo da aula, fechamento | 2 e 3 | Notas, aulas, faltas, relatórios do diário | Especificado em [61](61-diario-escolar-por-portal.md) |
| 5 | **Boletim e conselho de classe**: boletim, aprovação final, recuperação paralela, ata de conselho | 4 | Boletim, conselho de classe, recuperação paralela | Especificado em [62](62-boletim-e-conselho-de-classe-por-portal.md) |
| 6 | **Ocorrências disciplinares**: registro, fluxo, notificação ao responsável, sigilo | Nada | Ocorrências | Especificado em [63](63-ocorrencias-disciplinares-por-portal.md) |
| 7 | **Planos de aula e de ensino**: planos por disciplina, revisão pela coordenação | 1 e 3 | Plano de aula, plano de ensino | Especificado em [64](64-planos-de-aula-e-de-ensino-por-portal.md) |
| 8 | **Estágio e TCC** | 1 | Estágio, TCC | Especificado em [65](65-estagio-e-tcc-por-portal.md) |
| 9 | **Prontuário e portfólio do aluno** | 4 e 5 | Perfil e prontuário do aluno, portfólio | Especificado em [66](66-prontuario-e-portfolio-do-aluno-por-portal.md) |
| 10 | **Livros digitais e arquivo morto**: livro de registro, arquivo digitalizado | 54 | Livro de registro, arquivo morto | Especificado em [67](67-livros-digitais-e-arquivo-morto-por-portal.md) |
| 11 | **Biblioteca**: acervo, empréstimo e reserva | Nada | Bibliografias, empréstimos | Especificado em [68](68-biblioteca-por-portal.md) |
| 12 | **Relatórios e censo** | 1 a 10 | Relatórios de cada módulo | Especificado em [69](69-relatorios-e-censo-por-portal.md) |
| 13 | **Importação de dados** de sistema anterior | 1 a 4 | Importação | Especificado em [70](70-importacao-de-dados-por-portal.md) |

---

## 4. Decisões necessárias

Estas são de produto. Não as tomo sozinho.

| # | Decisão | Opções |
|---|---|---|
| ACA-01 | Escopo: o SDD cobre ensino básico, técnico, superior, ou os três? | **Decidido** em 03/11/2026: os três níveis. Inclui TCC e CPA/SINAES, a confirmar em ACA-02 |
| ACA-02 | TCC e CPA/SINAES entram nesta versão? | **Decidido** em 03/11/2026: sim, entram. TCC em [65](65-estagio-e-tcc-por-portal.md) e CPA em [69](69-relatorios-e-censo-por-portal.md) |
| ACA-03 | Estágio: obrigatório para o curso ou só opcional? | **Decidido** em 03/11/2026: obrigatório quando o curso exigir |
| ACA-04 | Ordem de fechamento da seção 3 | **Decidido** em 03/11/2026: confirmada |

---

## 5. Critérios para dizer que o acadêmico está completo

- [ ] Cada item do menu de referência (seção 2) tem um documento de origem.
- [ ] Cada módulo da seção 3 tem estados, regra de portal, DDL e critérios de aceite.
- [ ] Notas, frequência e boletim têm regra de cálculo testada com caso real.
- [ ] Importação tem validação de origem e relatório de rejeitados.
- [ ] Pareceres de jurídico e norma sobre histórico, guarda de registro e prazos estão respondidos.
