# 55 — Verificação do Acadêmico: Cobertura, Lacunas e Ordem de Fechamento

> Parte do [SDD v2](00-README.md). Referência de comparação: menu do sistema iScholar, colado pelo autor em 03/11/2026, e o mapa de páginas acadêmico da v1 (`spec_gestao_academica_completo.md`, seção 2). Regras já existentes em [17](17-regras-modulos.md), seção 4. Matrícula em [46](46-matricula-e-rematricula-por-portal.md). Agendamento em [44](44-agendamento-ambientes-equipamentos.md). Sala online em [40](40-aulas-online-por-portal.md). Documentos em [48](48-gerador-de-documentos-por-portal.md) e [54](54-gestao-de-documentos-tres-contextos.md). Simulados em [47](47-simulados-por-portal.md). Preceptoria em [42](42-preceptoria-por-portal.md).
> **Veredito:** o acadêmico **não está completo**. A parte de matrícula, documentos e salas está especificada. A estrutura acadêmica, a grade de horários, notas, frequência, diário, conselho de classe e planos pedagógicos estão só citados.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Matrícula e rematrícula estão completas? | **Sim**, em [46](46-matricula-e-rematricula-por-portal.md), com estados, janelas, condicional e trancamento |
| Estrutura acadêmica (cursos, grades, disciplinas, períodos, calendário) está especificada? | **Não.** Aparece só como nome de entidade em [17](17-regras-modulos.md), seção 4.1 |
| Notas, boletim e aprovação? | **Não.** Só a regra "nota dentro da faixa do método" |
| Frequência, faltas e justificativas? | **Parcial.** QR Code e sala online estão especificados. Faltas, justificativas e cálculo de frequência não |
| Diário, planos de aula e de ensino? | **Não** como especificação. Há estados do diário em [17](17-regras-modulos.md), seção 4.3 |
| Ocorrências disciplinares? | **Não.** Há ocorrências de SST, em outro contexto |
| Conselho de classe, recuperação paralela, portfólio? | **Não** |
| Estágio, TCC? | **Parcial** para estágio (campos em [17](17-regras-modulos.md)). **Não** para TCC |
| Livros digitais (registro e atas)? | **Parcial.** Atas em [53](53-pacote-documentos-e-contratos.md), DC-18. Livro de registro, não |
| Relatórios acadêmicos e censo? | **Não** |

---

## 2. Mapa: menu iScholar × SDD

Itens do menu de referência, na ordem em que aparecem.

### 2.1 Coordenação

| Item do iScholar | Cobertura no SDD | Situação |
|---|---|---|
| Empresas | Empresa e unidades: [03](03-dominio-tenancy.md) | Coberto no modelo de tenant |
| Unidades escolares | [03](03-dominio-tenancy.md), [44](44-agendamento-ambientes-equipamentos.md) | Coberto |
| Salas de aula | [44](44-agendamento-ambientes-equipamentos.md) | Coberto |
| Cursos | Só como entidade em [17](17-regras-modulos.md) | **Lacuna** |
| Grupos de horários | Não especificado | **Lacuna** |
| Disciplinas | Só como entidade em [17](17-regras-modulos.md) | **Lacuna** |
| Grades curriculares | Só como entidade. Mapa de equivalência da v1 não especificado | **Lacuna** |
| Períodos letivos | Não especificado | **Lacuna** |
| Funcionários | [39](39-departamento-pessoal-rh-medicina-por-portal.md) | Coberto como RH |
| Documentos (pendentes) | [54](54-gestao-de-documentos-tres-contextos.md), contexto A | Coberto |
| Sistemas avaliativos | Só "método de avaliação" em [17](17-regras-modulos.md) | **Lacuna** |
| Calendários escolares | Não especificado | **Lacuna** |
| Planos de pagamento | [18](18-regras-modulos-2.md) e [26](26-sdd-juridico-regulatorio.md) | Coberto no financeiro |

### 2.2 Secretaria

| Item do iScholar | Cobertura no SDD | Situação |
|---|---|---|
| Turmas | [46](46-matricula-e-rematricula-por-portal.md), M-07 (enturmação) | Parcial. Sem cadastro de turma |
| Responsáveis | [46](46-matricula-e-rematricula-por-portal.md), [07](07-privacidade-lgpd.md) | Coberto no vínculo |
| Alunos | [17](17-regras-modulos.md), seção 4.2 | Parcial. Sem prontuário detalhado |
| Matrículas | [46](46-matricula-e-rematricula-por-portal.md) | Coberto |
| Alunos potenciais | [22](22-crm-canais-e-papeis.md), leads | Coberto no CRM |
| Modelos de documentos | [48](48-gerador-de-documentos-por-portal.md) | Coberto |
| Ocorrências | Não especificado | **Lacuna** |
| Solicitações | [32](32-atendimento-privacidade-por-portal.md) e [46](46-matricula-e-rematricula-por-portal.md) | Coberto pelo protocolo |
| Agenda de eventos | [40](40-aulas-online-por-portal.md), [43](43-pastoral-por-portal.md), [44](44-agendamento-ambientes-equipamentos.md) | Parcial. Sem agenda escolar geral |
| Processos seletivos | [46](46-matricula-e-rematricula-por-portal.md), seção 4 | Coberto |
| Gabaritos | [47](47-simulados-por-portal.md), MOD-04 | Parcial. Sem especificação do leitor |
| Secretaria digital (portal externo) | [46](46-matricula-e-rematricula-por-portal.md), [48](48-gerador-de-documentos-por-portal.md) | Coberto |
| Relatórios | Não especificado | **Lacuna** |

### 2.3 Diário escolar

| Item do iScholar | Cobertura no SDD | Situação |
|---|---|---|
| Notas | [17](17-regras-modulos.md), seção 4.2 | Parcial. Sem regra de cálculo, de recuperação e de boletim |
| Aulas (conteúdo) | [47](47-simulados-por-portal.md) não; plano de aula só citado | **Lacuna** |
| Faltas | [17](17-regras-modulos.md), presença por QR; [40](40-aulas-online-por-portal.md) | Parcial. Sem justificativa |
| Relatórios | Não especificado | **Lacuna** |

### 2.4 Outros módulos do menu

| Item | Cobertura | Situação |
|---|---|---|
| Financeiro (parcelas, cobrança, conciliação, NF, cheques, cartões, estoque) | [18](18-regras-modulos-2.md), [20](20-pagamentos-seguranca.md), [34](34-pagamentos-fiscal-bancos-por-portal.md) | Coberto no financeiro. Cheques e estoque de cantina não têm especificação |
| Centros de custo | [17](17-regras-modulos.md) e [31](31-matriz-portais-modulos.md) | Citado, sem especificação |
| Controle patrimonial | [19](19-regras-modulos-3.md), seção 8 | Coberto |
| Catraca | [35](35-acesso-e-seguranca-fisica-por-portal.md) | Coberto |
| Biblioteca (bibliografias, empréstimos e reservas) | [31](31-matriz-portais-modulos.md), seção 3.1 | Citado. **Sem especificação própria** |
| Administração (usuários, grupos, integrações, importação, notificações) | [06](06-identidade-acesso.md), [16](16-integracoes-externas.md), [19](19-regras-modulos-3.md), seção 13 | Coberto, exceto importação de dados, que é lacuna |
| Ischolar Intelligence | [27](27-inteligencia-artificial-e-portais.md) e [28](28-cobertura-ia-todos-os-modulos.md) | Coberto |

---

## 3. Lacunas do acadêmico, em ordem de dependência

As lacunas abaixo se apoiam umas nas outras. Por isso a ordem importa.

| Ordem | Módulo a especificar | Depende de | Itens do menu que cobre |
|---|---|---|---|
| 1 | **Estrutura acadêmica**: cursos, disciplinas, grades curriculares, períodos letivos, calendário e tipos de curso | Nada | Cursos, disciplinas, grades, períodos, calendários |
| 2 | **Sistemas avaliativos**: escalas, método de média, recuperação, conceitos, regra de aprovação | 1 | Sistemas avaliativos |
| 3 | **Turmas e grade de horários**: criação de turma, grupos de horários, enturmação, quadro de aulas | 1 | Turmas, grupos de horários |
| 4 | **Diário**: chamada, faltas, justificativa, notas por período, conteúdo da aula, fechamento | 2 e 3 | Notas, aulas, faltas, relatórios do diário |
| 5 | **Boletim e conselho de classe**: boletim, aprovação final, recuperação paralela, ata de conselho | 4 | Boletim, conselho de classe, recuperação paralela |
| 6 | **Ocorrências disciplinares**: registro, fluxo, notificação ao responsável, sigilo | Nada | Ocorrências |
| 7 | **Planos de aula e de ensino**: planos por disciplina, revisão pela coordenação | 1 e 3 | Plano de aula, plano de ensino |
| 8 | **Estágio e TCC** | 1 | Estágio, TCC |
| 9 | **Prontuário e portfólio do aluno** | 4 e 5 | Perfil e prontuário do aluno, portfólio |
| 10 | **Livros digitais e arquivo morto**: livro de registro, arquivo digitalizado | 54 | Livro de registro, arquivo morto |
| 11 | **Biblioteca**: acervo, empréstimo e reserva | Nada | Bibliografias, empréstimos |
| 12 | **Relatórios e censo** | 1 a 10 | Relatórios de cada módulo |
| 13 | **Importação de dados** de sistema anterior | 1 a 4 | Importação |

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
