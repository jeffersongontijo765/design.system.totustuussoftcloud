# 31 — Matriz de Portais, Fronteiras entre Módulos, Logs, Testes, Segurança e Auditoria

> Parte do [SDD v2](00-README.md). Portais em [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 1. Catálogo em [12](12-catalogo-modulos.md). Auditoria em [29](29-auditoria.md). Testes em [24](24-operacao-continuidade-qualidade.md), seção 5. Logs em [10](10-implantacao-operacao.md), seção 7. Fonte dos módulos por portal: a navegação da v1 ([12-portals-navigation-sidebar-pages-spec.md](anexo-v1/12-portals-navigation-sidebar-pages-spec.md), seção 4), agora reclassificada pelos seis portais da v2.
> **Status:** aprovada pelo autor em 03/11/2026, com as propostas adotadas. Itens sem valor definido continuam pendentes, criada em 03/11/2026 a partir de auditoria das especificações da v1. Itens marcados **[Decisão do autor]** dependem de resposta. Itens **[Sem especificação]** não têm fonte na v1 ou na v2.

---

## 1. Regras de organização

1. **Módulo tem um dono de dado.** Cada módulo pertence a um único domínio (plataforma ou entidade) e a um único banco ([03](03-dominio-tenancy.md), seção 1.1).
2. **Portal é tela, não dono.** Um portal mostra os módulos que o vínculo da pessoa permite. Nenhum portal guarda dado próprio além de preferências.
3. **Dois contextos não se misturam.** Operação da plataforma (portal do desenvolvedor) e operação de cada entidade (portal de gestão, professor, aluno, responsáveis, terceiros) usam bancos, papéis e módulos diferentes, mesmo quando o nome é igual (ex.: Financeiro, Contábil).
4. **Um nome, uma especificação.** Dois documentos que descrevem o mesmo módulo viram um só. O que sobra vai para o arquivo histórico.

---

## 2. Matriz por portal

Legenda de origem: **P** = plataforma (banco master); **E** = entidade/unidade (banco da unidade).

### 2.1 Portal do Desenvolvedor (`desenvolvedor.`) — equipe da plataforma

| Área | Módulos | Contexto | Observação |
|---|---|---|---|
| Plataforma e clientes | Clientes (tenants), licenciamento, assinaturas, faturamento de clientes, limites e consumo, domínios, provisionamento | P | Ciclo de vida da seção 5 de [23](23-dominios-provisionamento-ciclo-de-vida.md) |
| Editor de portais | Páginas, rotas, layouts, blocos, publicação e rollback | P | D-23. Chamado de "builder de portais" na v1. **Não é o editor de modelos do Gerador de documentos** (ver seção 3.4) Especificação: [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 3 (D-23) |
| Comercial da plataforma | CRM da plataforma, leads, propostas, comissões | P | [22](22-crm-canais-e-papeis.md), seção 6.1. Não se mistura com o protocolo de atendimento (seção 3.2) |
| Financeiro da plataforma | Contas a pagar e a receber **da própria empresa** | P | **Decidido** em 03/11/2026: mantido para a gestão da própria empresa desenvolvedora. Especificação: [31](31-matriz-portais-modulos.md), seção 3.3; [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 3 (taxas de split) |
| Contábil da plataforma | Plano de contas, razão, fechamento da empresa, tributos e obrigações fiscais da empresa | P | Mesma decisão do financeiro. Tributos da empresa: seção 3.3, confirmado pelo autor em 04/11/2026. Especificação: [31](31-matriz-portais-modulos.md), seção 3.3; [22](22-crm-canais-e-papeis.md), seção 5 (papéis contábil e fiscal) |
| Operações internas | Patrimônio, frotas, suprimentos da empresa | P | **Decidido** em 03/11/2026: mantidos, como instâncias separadas dos módulos das entidades. Especificação: [19](19-regras-modulos-3.md), seções 8 e 9; [80](80-decisoes-por-padrao.md), DP-01 a DP-03 |
| Pessoas da plataforma | Departamento pessoal, recursos humanos, medicina e segurança do trabalho da empresa | P | Mesma decisão. O HCM das entidades não é o da plataforma. Três módulos separados, conforme HCM-01 e HCM-10 do [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 11 |
| Suporte | Chamados dos clientes, base de conhecimento, SLA | P | Seção 3.2. Especificação: [32](32-atendimento-privacidade-por-portal.md), seção 2 |
| Segurança e operação | Acesso, MFA, auditoria, privacidade (DPO), TI, configurações do sistema, integrações globais, painel de bancos de dados | P | [05](05-seguranca.md), [07](07-privacidade-lgpd.md), [10](10-implantacao-operacao.md). Painel de bancos de dados: substitui o módulo Bancos (PAG-03, [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 4) |

### 2.2 Portal de Gestão (`gestao.`) — equipe administrativa da entidade

| Área | Módulos | Contexto | Observação |
|---|---|---|---|
| Acadêmico | Administração escolar (estrutura acadêmica), pedagógico (coordenação e diário), calendário e eventos, séries e turmas (grade de horários), regras de aprovação (sistemas avaliativos, boletim e conselho de classe), ocorrências disciplinares, planos de aula e de ensino, estágio e TCC, prontuário e portfólio do aluno, livros digitais e arquivo morto, preceptoria, gestão pastoral, aulas online, agendamento de ambientes e equipamentos, formulários e pesquisas, relatórios acadêmicos e censo | E | [17](17-regras-modulos.md), seção 4; [55](55-academico-verificacao-e-lacunas.md); [58](58-calendario-e-eventos-por-portal.md) a [69](69-relatorios-e-censo-por-portal.md); [40](40-aulas-online-por-portal.md) a [44](44-agendamento-ambientes-equipamentos.md). Itens explicitados em 04/11/2026 a partir da seção 7 e dos documentos por portal |
| Secretaria | Matrículas, rematrículas, transferências, enturmação, ficha cadastral, protocolo de atendimento, emissão de documentos, processo seletivo e lista de espera | E | Sub-área do acadêmico. Ver seções 3.2 e 3.5; [46](46-matricula-e-rematricula-por-portal.md), [48](48-gerador-de-documentos-por-portal.md) |
| Gestão de documentos | Documentos recebidos (validação), documentos administrativos (tramitação), documentos emitidos (modelos e emissão), serviços comuns (assinatura, protocolo e armazenamento) | E | [54](54-gestao-de-documentos-tres-contextos.md). Ver também seções 3.1 e 3.4 |
| Simulados | Banco de questões, geração de provas, correção, gabarito, ranking | E | Ver seção 3.6. Especificação: [47](47-simulados-por-portal.md) |
| Biblioteca | Acervo, empréstimos, reservas, multas, biblioteca digital | E | Ver seção 3.1. Especificação: [68](68-biblioteca-por-portal.md) |
| Financeiro da entidade | Mensalidades, títulos, cobrança, régua, conciliação, centros de custo, contas a pagar, cheques, caixa físico, fluxo de caixa e DRE, gateways e split | E | [17](17-regras-modulos.md), [18](18-regras-modulos-2.md), [20](20-pagamentos-seguranca.md), [34](34-pagamentos-fiscal-bancos-por-portal.md), [71](71-financeiro-completo-por-portal.md) |
| Contábil e fiscal da entidade | Plano de contas da entidade, tributos, retenções, obrigações, NFSe | E | Ver seção 3.3. Especificação: [31](31-matriz-portais-modulos.md), seção 3.3; [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 5; [26](26-sdd-juridico-regulatorio.md), seção 11 |
| Comercial e admissões | CRM do tenant (captação, pré-cadastro, inscrição) | E | [22](22-crm-canais-e-papeis.md), seção 6.2 |
| Pessoas e RH | HCM, folha, ponto, férias, avaliação de desempenho, SST | E | [18](18-regras-modulos-2.md), seção 3; [39](39-departamento-pessoal-rh-medicina-por-portal.md); [52](52-medicina-do-trabalho-especificacao.md) |
| Suprimentos e compras | Requisição, cotação, pedido, almoxarifado, merenda | E | [19](19-regras-modulos-3.md), seção 2 |
| Patrimônio e frotas | Bens, depreciação, veículos, manutenção, rotas | E | [19](19-regras-modulos-3.md), seções 8 e 9 |
| Contratos | Contratos de fornecedor, contratos de aluno, contratos de pessoal | E | [17](17-regras-modulos.md), seção 7; [33](33-contratos-por-portal.md); [53](53-pacote-documentos-e-contratos.md) |
| Atendimento | SAC, helpdesk, chat, tickets | E | Seção 3.7; [32](32-atendimento-privacidade-por-portal.md), seção 2 |
| Arquivos | Armazenamento de arquivos | E | [21](21-busca-e-armazenamento.md) |
| Relatórios e gráficos | Painéis, gráficos salvos | E | Seção 3.8; [56](56-configuracoes-e-relatorios-lacunas.md), seção 3; [69](69-relatorios-e-censo-por-portal.md) |
| Configuração e acesso | Unidades, usuários, vínculos, privacidade da entidade, configurações da entidade, campos personalizados, notificações, integrações educacionais oficiais, importação de dados, acesso físico e portaria, TI da entidade | E | [06](06-identidade-acesso.md); [32](32-atendimento-privacidade-por-portal.md), seção 3; [35](35-acesso-e-seguranca-fisica-por-portal.md); [36](36-tecnologia-da-informacao-por-portal.md), seção 4; [56](56-configuracoes-e-relatorios-lacunas.md), seção 2; [57](57-notificacoes-por-portal.md); [70](70-importacao-de-dados-por-portal.md); [72](72-campos-personalizados-por-portal.md); [74](74-integracoes-educacionais-oficiais.md). Unidade só é criada por `platform.developer` (L-02); a gestão edita a unidade existente |
| Planejamento acadêmico, institucional e de desenvolvimento | Planejamento acadêmico, planejamento institucional, planejamento de desenvolvimento de pessoas | E | [37](37-planejamento-e-empenho.md), seções 2 a 4 (especificado em 03/11/2026, seção 3.9) |
| Empenho | Empenho, liquidação e pagamento (só entidade pública) | E | [37](37-planejamento-e-empenho.md), seção 5 (especificado em 03/11/2026, seção 3.9) |

### 2.3 Portal do Professor (`portal-do-professor.`)

| Área | Módulos | Escopo |
|---|---|---|
| Classe | Turmas e disciplinas do próprio docente, mural, materiais, tarefas | Só turmas vinculadas. Especificação: [80](80-decisoes-por-padrao.md), DP-06 (mural, materiais e tarefas) |
| Diário | Frequência, conteúdo, notas, plano de aula | Só turmas vinculadas. Nota só pelo professor da turma ([22](22-crm-canais-e-papeis.md), seção 5) |
| Simulados | Elaboração de questões, agendamento, resultados da turma | Questão passa por revisão antes de publicar (seção 3.6) Especificação: [47](47-simulados-por-portal.md), seção 7 |
| Biblioteca | Consulta de acervo, indicação de leitura | Somente leitura. Especificação: [68](68-biblioteca-por-portal.md), seção 11 |
| Protocolos e pedidos | Solicitação de material, reserva de laboratório, justificativa | Usa o serviço de protocolo (seção 3.2) Especificação: [31](31-matriz-portais-modulos.md), seção 3.2; [44](44-agendamento-ambientes-equipamentos.md) |
| Documentos e pessoal | Declarações, contrato de trabalho, holerite, ponto | Só dados do próprio docente. Especificação: [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 6; [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 8 |
| Relatórios | Rendimento da turma, ficha individual | Só turmas vinculadas. Especificação: [69](69-relatorios-e-censo-por-portal.md), seção 6 |
| Agenda e comunicação | Horário e calendário das turmas, aulas online, notificações, meu perfil | Só turmas vinculadas. [58](58-calendario-e-eventos-por-portal.md), [60](60-turmas-e-grade-de-horarios-por-portal.md), [40](40-aulas-online-por-portal.md), [57](57-notificacoes-por-portal.md), [76](76-meu-perfil-por-portal.md) (explicitado em 04/11/2026) |
| Acompanhamento pedagógico | Ocorrências da turma, orientação de estágio e TCC, preceptoria, portfólio dos alunos, formulários e pesquisas, pastoral | Só turmas e orientandos vinculados. [63](63-ocorrencias-disciplinares-por-portal.md), [65](65-estagio-e-tcc-por-portal.md), [42](42-preceptoria-por-portal.md), [66](66-prontuario-e-portfolio-do-aluno-por-portal.md), [41](41-formularios-e-pesquisas.md), [43](43-pastoral-por-portal.md) (explicitado em 04/11/2026) |

### 2.4 Portal do Aluno (`portal-do-aluno.`)

| Área | Módulos | Escopo |
|---|---|---|
| Classe e diário | Disciplinas, materiais, entregas, boletim, presença | Só o próprio aluno. Especificação: [61](61-diario-escolar-por-portal.md), seção 7; [62](62-boletim-e-conselho-de-classe-por-portal.md), seção 7; [80](80-decisoes-por-padrao.md), DP-06 |
| Simulados | Simulados agendados, realização de prova, gabarito e comentários | Só simulados do próprio aluno. Especificação: [47](47-simulados-por-portal.md), seção 7 |
| Biblioteca | Empréstimos, prazos, renovação, pesquisa de acervo | Só os próprios empréstimos. Especificação: [68](68-biblioteca-por-portal.md), seção 11 |
| Protocolos online | Requerimento de segunda chamada, declaração de matrícula | Usa o serviço de protocolo. Especificação: [31](31-matriz-portais-modulos.md), seção 3.2 |
| Documentos | Boletim oficial, histórico, declarações | Emissão pelo aluno conforme regra de [21](21-busca-e-armazenamento.md) e seção 3.5 |
| Matrícula | Confirmação para o ano seguinte, eletivas, rematrícula | Seção 3.5. Especificação: [46](46-matricula-e-rematricula-por-portal.md), seção 6 |
| Financeiro | Mensalidades, boleto, PIX, comprovantes | Só títulos do próprio aluno. Especificação: [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 8; [20](20-pagamentos-seguranca.md) |
| Privacidade | Dados cadastrais, solicitações LGPD | [07](07-privacidade-lgpd.md) |
| Agenda e comunicação | Horário da turma, calendário e eventos, aulas online, notificações, meu perfil | Só o próprio aluno. [58](58-calendario-e-eventos-por-portal.md), [60](60-turmas-e-grade-de-horarios-por-portal.md), [40](40-aulas-online-por-portal.md), [57](57-notificacoes-por-portal.md), [76](76-meu-perfil-por-portal.md) (explicitado em 04/11/2026) |
| Vida acadêmica | Ocorrências próprias, estágio e TCC, portfólio, preceptoria, formulários e pesquisas, pastoral | Só o próprio aluno. [63](63-ocorrencias-disciplinares-por-portal.md), [65](65-estagio-e-tcc-por-portal.md), [66](66-prontuario-e-portfolio-do-aluno-por-portal.md), [42](42-preceptoria-por-portal.md), [41](41-formularios-e-pesquisas.md), [43](43-pastoral-por-portal.md) (explicitado em 04/11/2026) |

### 2.5 Portal dos Pais e Responsáveis (`portal-dos-responsaveis.`)

| Área | Módulos | Escopo |
|---|---|---|
| Acompanhamento | Notas, faltas, ocorrências, comunicados, entradas e saídas da portaria | Só dependentes com vínculo ativo de responsabilidade. Especificação: [61](61-diario-escolar-por-portal.md), [62](62-boletim-e-conselho-de-classe-por-portal.md), [63](63-ocorrencias-disciplinares-por-portal.md), [35](35-acesso-e-seguranca-fisica-por-portal.md), seção 4, [57](57-notificacoes-por-portal.md) |
| Biblioteca e simulados | Empréstimos e desempenho dos filhos | Somente leitura. Especificação: [68](68-biblioteca-por-portal.md), seção 11; [47](47-simulados-por-portal.md), seção 7 |
| Protocolos da família | Mudança de turno, saída antecipada, documentos | Usa o serviço de protocolo. Especificação: [31](31-matriz-portais-modulos.md), seção 3.2 |
| Financeiro e matrícula | Faturas dos filhos, PIX, rematrícula online, assinatura do contrato | Seção 3.5. Bloqueio parcial por inadimplência ([26](26-sdd-juridico-regulatorio.md), seção 3) |
| Privacidade e menores | Consentimento de imagem, dados dos filhos | Regra de menor de idade em [07](07-privacidade-lgpd.md) |
| Agenda e comunicação | Horário e calendário dos dependentes, eventos e autorizações, notificações, meu perfil | Só dependentes com vínculo ativo. [58](58-calendario-e-eventos-por-portal.md), [60](60-turmas-e-grade-de-horarios-por-portal.md), [43](43-pastoral-por-portal.md), [57](57-notificacoes-por-portal.md), [76](76-meu-perfil-por-portal.md) (explicitado em 04/11/2026) |

### 2.6 Portal de Terceiros (`portal-de-terceiros.`)

| Área | Módulos | Escopo |
|---|---|---|
| Faturamento de serviços | Emissão e envio de NF-e de serviço, acompanhamento de pagamento, extrato | Só o próprio fornecedor. Especificação: [38](38-portal-de-terceiros-prestadores.md); [34](34-pagamentos-fiscal-bancos-por-portal.md), seções 5 e 8 |
| Pedidos e contratos | Pedidos de compra pendentes, contratos em vigor | Só o próprio fornecedor. Especificação: [38](38-portal-de-terceiros-prestadores.md), seção 4; [33](33-contratos-por-portal.md), seção 9 |
| Documentos da empresa | Certidões, contrato social, alvarás, seguro | Só o próprio fornecedor. Validade com alerta. Especificação: [38](38-portal-de-terceiros-prestadores.md), seção 5 |
| Prestação de serviço | Ordens de serviço, relatórios de execução, cronograma | Só ordens do próprio fornecedor. Especificação: [38](38-portal-de-terceiros-prestadores.md), seção 3 |
| Chamados | Abertura de chamado de manutenção, solicitação de acesso à unidade | Usa o módulo de atendimento (seção 3.7) Especificação: [32](32-atendimento-privacidade-por-portal.md), seção 2.8; [35](35-acesso-e-seguranca-fisica-por-portal.md), seção 4 |
| Configurações e integrações | Dados da empresa, responsáveis técnicos, dados bancários, integrações via API | Dados bancários exigem confirmação por MFA. Especificação: [38](38-portal-de-terceiros-prestadores.md), seção 6; [06](06-identidade-acesso.md), seção 8 |
| Habilitação e acesso | Cadastro e habilitação do prestador, pessoas e papéis do prestador, tipo de prestador, meu perfil | [38](38-portal-de-terceiros-prestadores.md), seções 2 a 6; [76](76-meu-perfil-por-portal.md) (explicitado em 04/11/2026) |

**Regra:** o portal de terceiros nunca mostra financeiro interno, contábil, folha ou dado de aluno.

---

## 3. Fronteiras entre módulos

### 3.1 Biblioteca × Gestão de Documentos

**Problema encontrado:** a especificação [`spec_gestao_biblioteca_completo.md`](anexo-v1/spec_gestao_biblioteca_completo.md) (UI enterprise) inclui páginas de gestão de usuários, perfis, auditoria, integrações e **"Gestão de Documentos e Anexos"** (página 14). Isso mistura o acervo da biblioteca com o cofre de documentos da entidade.

**Decisão proposta:**

| Módulo | Dono | Guarda | Não guarda |
|---|---|---|---|
| Biblioteca | Acervo, exemplar, empréstimo, reserva, multa | Metadados do acervo; arquivo digital do acervo via [21](21-busca-e-armazenamento.md) | Documento oficial de aluno ou de funcionário |
| Gestão de documentos | Documento oficial, versão, assinatura, validação, modelo | Declarações, históricos, certidões, contratos assinados | Exemplar físico, empréstimo |

A página 14 da UI de biblioteca sai dela. A "Interface de biblioteca (UI)" do catálogo deixa de ser módulo e passa a ser componentes de [08](08-frontend-design-system.md). As páginas 6 a 13 da UI são padrões de tela, não módulos.

### 3.2 Protocolo × CRM comercial × Atendimento

Não encontrei na v1 um módulo chamado "CRM protocolo". O protocolo aparece em:

- Secretaria (número e senha, consulta pública por número e CPF) — [`spec_gestao_academica_completo.md`](anexo-v1/spec_gestao_academica_completo.md), seção 6.2;
- Gestão de documentos e validações;
- Serviços do portal do aluno, do professor e dos responsáveis;
- Direitos do titular (solicitação LGPD com protocolo — [07](07-privacidade-lgpd.md));
- Segurança e medicina do trabalho (protocolo de CAT ou INSS).

**Decisão proposta:** o **protocolo é um serviço transversal**, dono em Atendimento. Ele gera número único, status, prazo e trilha. Ele **não pertence ao CRM**:

| | CRM comercial (plataforma e tenant) | Protocolo |
|---|---|---|
| Objeto | Lead, oportunidade, proposta, matrícula em andamento | Pedido ou solicitação com número |
| Quem abre | Vendedor, admissões, canal de captação | Pessoa que pede algo (aluno, responsável, professor, titular, fornecedor) |
| Consulta pública | Não | Sim, por número e CPF, com limite de tentativas ([17](17-regras-modulos.md), seção 3) |

**Regra de separação:** nenhum protocolo guarda dado comercial, e nenhum lead recebe número de protocolo. Quando um lead vira matrícula, o protocolo de matrícula é um pedido separado, vinculado ao lead.

### 3.3 Financeiro e contábil: plataforma × entidade

| Assunto | Plataforma (portal do desenvolvedor) | Entidade (portal de gestão) |
|---|---|---|
| Receita | Assinaturas dos clientes ([20](20-pagamentos-seguranca.md)) | Mensalidades e serviços de alunos |
| Despesa | Da própria empresa | Da entidade (fornecedor, folha) |
| Contábil | Plano de contas da empresa | Plano de contas da entidade, com centro de custo por unidade |
| Tributos | Da empresa | Retenções e apurações da entidade ([19](19-regras-modulos-3.md) e v1 [`spec_gestao_contabil_fiscal_completo.md`](anexo-v1/spec_gestao_contabil_fiscal_completo.md), seção 6.5) |

**Proposta:** o módulo Financeiro e o Contábil são o mesmo código com dois donos de dado (banco master e banco de cada unidade). **Decidido** em 03/11/2026: a plataforma precisa dos módulos contábil e financeiro para a própria empresa.

### 3.4 Builder: três significados

O termo "builder" aparece em três lugares e pode confundir:

| Nome | Dono | Função | Documento |
|---|---|---|---|
| Builder de portais | Plataforma | Páginas e layouts declarativos | [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 3 |
| Builder de documentos | Entidade (Gestão de documentos) | Modelos de documento com variáveis e emissão em PDF | [`spec-builder-documentos-academicos.md`](anexo-v1/spec-builder-documentos-academicos.md) (26 seções) |
| Builder de automações | Entidade (Automações) | Regras de disparo | [`spec_gestao_biblioteca_completo.md`](anexo-v1/spec_gestao_biblioteca_completo.md), página 7 |

**Ação (feita em 03/11/2026, MOD-12):** na v2 os nomes são "Editor de portais" ([23](23-dominios-provisionamento-ciclo-de-vida.md)), "Gerador de documentos", com o "editor de modelos" ([48](48-gerador-de-documentos-por-portal.md)), e "Automações". O termo "builder" fica só nos nomes de arquivo da v1 e no código do papel `platform.builder`.

**Gerador de documentos:** especificado em [48](48-gerador-de-documentos-por-portal.md) (MOD-07), a partir da v1, que cobre tipos documentais, tamanhos de papel, cabeçalho e rodapé, variáveis, condicionais, fluxo de emissão, auditoria e LGPD. Os itens abaixo eram a lista do que faltava e estão cobertos lá:

- Lista de tipos documentais com retenção de cada um (ligada a [07](07-privacidade-lgpd.md), seção 5).
- Emissão só de modelo aprovado. Versão emitida é imutável.
- Número de protocolo da emissão (seção 3.2).
- Assinatura: [26](26-sdd-juridico-regulatorio.md), seção 6.

### 3.5 Matrícula e rematrícula

A v2 tem só os estados da matrícula em [17](17-regras-modulos.md) (`pre_matricula`, `ativa`, `trancada`, `concluida`, `cancelada`, `transferida`). A v1 ([`spec_gestao_academica_completo.md`](anexo-v1/spec_gestao_academica_completo.md)) tem mais: kanban de rematrícula, wizard, prazo de 7 dias, lembrete, "não rematriculado" após 30 dias, matrícula condicional com prazo e trancamento com motivo e protocolo.

**Lacunas do fluxo, a incluir na v2:**

| # | Passo ou regra | Origem na v1 | Estado na v2 |
|---|---|---|---|
| M-01 | Janela de rematrícula por série e unidade, com abertura e fechamento | Acadêmico, kanban | Não definido |
| M-02 | Wizard do responsável ou aluno: dados, documentos, escolha de turma e eletivas, contrato, pagamento | Portal dos responsáveis e do aluno | Não definido |
| M-03 | Vaga com reserva e bloqueio de concorrência | [15](15-validacoes.md), seção 7 | Definido |
| M-04 | Matrícula condicional com prazo e expiração | Ações automáticas, v1 linha 1181 | Não definido |
| M-05 | Não rematriculado após 30 dias: estado e aviso | Ações automáticas, v1 linha 1175 | Não definido |
| M-06 | Trancamento com motivo, aprovação por níveis e protocolo | Requerimentos, v1 seção 15 | Não definido |
| M-07 | Transferência e enturmação | Secretaria digital | Não definido |
| M-08 | Documento obrigatório pendente bloqueia a matrícula? Regra por tipo | v1 linha 1176 | Não definido. Ver [26](26-sdd-juridico-regulatorio.md) |
| M-09 | Assinatura do contrato de matrícula e pagamento da primeira parcela | Portal dos responsáveis | Parcial em [20](20-pagamentos-seguranca.md) |

### 3.6 Simulados

A v2 tem só a regra de IA em [19](19-regras-modulos-3.md), seção 12, e a linha da tabela em [28](28-cobertura-ia-todos-os-modulos.md). Faltam:

- **Banco de questões**, com origem, autoria, revisão e situação (`rascunho`, `revisada`, `publicada`, `arquivada`).
- **Geração de prova** por perfil (ENEM, vestibular, interna) e gabarito.
- **Gabarito óptico**: a v1 cita, mas não há especificação do leitor. **Decidido** em 03/11/2026: as duas opções, próprio e de terceiro, por configuração da entidade.
- **Correção por IA**. **Conflito:** a v1 ([`spec_gestao_simulados_ia.md`](anexo-v1/spec_gestao_simulados_ia.md), seção "Correção automática por IA") tem como saída "nota final estimada". A v2 proíbe nota final dada só pela IA ([27](27-inteligencia-artificial-e-portais.md), princípio 2 e seção 5.11). Ação: a v2 fica com a regra da [27](27-inteligencia-artificial-e-portais.md). A nota da IA é sugestão; o professor confirma.
- **Anonimização** do aluno enviado ao provedor de IA ([19](19-regras-modulos-3.md), seção 12).
- **Relatórios por portal**: professor vê a turma; aluno vê as próprias provas; responsável vê os filhos; gestor vê a unidade.
- **Plano**: a v1 marca o simulado como "PRO" no portal de gestão. **Decidido** em 03/11/2026: o PRO libera correção por IA e ranking.

### 3.7 Atendimento: SAC, helpdesk, chat e bots

Há três especificações separadas, todas em "Revisar" no catálogo:

- [`spec_chat_rapido_sac.md`](anexo-v1/spec_chat_rapido_sac.md): chat rápido e abertura de ticket no SAC.
- [`SPEC-HELPDESK.md`](anexo-v1/SPEC-HELPDESK.md): helpdesk com SLA, base de conhecimento e portal do cliente.
- [`spec_gestao_sac_base_conhecimento.md`](anexo-v1/spec_gestao_sac_base_conhecimento.md).

**Decisão proposta (já adotada na v1 do catálogo):** um módulo único de atendimento, com helpdesk como base ([19](19-regras-modulos-3.md), seção 2). Os canais (chat do site, WhatsApp, Telegram, Instagram, Messenger, telefone e presencial) são entradas desse módulo, com as regras de [22](22-crm-canais-e-papeis.md), seção 2.

**Bots.** Há dois tipos e não podem ser confundidos:

| Bot | Dono | Regra |
|---|---|---|
| Bot de captação (CRM) | CRM da plataforma ou do tenant | [22](22-crm-canais-e-papeis.md), seção 3 |
| Bot de atendimento (SAC) | Atendimento | Mesma regra de IA: fonte cadastrada, humano para o resto, opção "Abrir ticket" sem IA (D-18) |

A reunião global ([`global_meeting_spec_v2_complete.md`](anexo-v1/global_meeting_spec_v2_complete.md)) menciona proteção contra bot em entrada pública, sem módulo de bot. Não é um terceiro tipo.

Pendente: a v2 ainda não tem DDL do atendimento consolidado (T-02 em [19](19-regras-modulos-3.md)).

### 3.8 Gráficos e painéis

[`chart-builder-spec-complete.md`](anexo-v1/chart-builder-spec-complete.md) (16 seções: consulta, renderização, painéis, API, segurança, exportação, tempo real) está marcado como "Especificado" no catálogo, mas a v2 não tem regra para ele.

**Proposta:**

- O construtor de gráfico é **componente compartilhado** ([08](08-frontend-design-system.md)), não módulo de domínio.
- Cada gráfico salvo pertence a um portal e a um contexto (plataforma, entidade ou unidade). Nenhum gráfico mostra dado fora do escopo de quem o abriu.
- Consulta passa pela mesma camada de permissão das telas. A consulta não tem acesso direto ao banco.
- Gráfico de dado sensível (CPF, saúde, salário) não é exportável sem motivo e sem auditoria ([29](29-auditoria.md)).
- Painel com dado pessoal entra no cache só com a regra de [30](30-cache.md), seção 4.

### 3.9 Módulos sem especificação

| Nome | Onde aparece | Situação |
|---|---|---|
| Planejamento acadêmico | Pedido do autor | Não há especificação na v1 nem na v2. **Decidido** em 03/11/2026: analisado e implementado em [37](37-planejamento-e-empenho.md). |
| Planejamento institucional | Pedido do autor | Idem |
| Planejamento de desenvolvimento | Pedido do autor. A v1 cita "Plano de Desenvolvimento Individual" no PRO de preceptoria | Idem. Se o termo for o PDI, ele fica em preceptoria ([19](19-regras-modulos-3.md), seção 11) |
| Empenho | Pedido do autor. A v1 não traz o termo como módulo | Empenho é fase da despesa pública (empenho, liquidação, pagamento). Só se aplica se a entidade for órgão público. **Decidido** em 03/11/2026: só para entidade pública. |
| Secretaria como módulo | v1 tem "Secretaria Digital" e "Secretaria Acadêmica" | Não é módulo próprio. É sub-área do acadêmico (seção 2.2) |
| Tributos como módulo | v1 tem "Retenção Tributária" e "Retenções e Tributos" | Não é módulo próprio. Fica em contábil e fiscal |

---

## 4. Logs, testes, segurança e auditoria por portal

### 4.1 Logs

**Estado na v2:** [10](10-implantacao-operacao.md), seção 7 define log estruturado em JSON com `request_id`, `tenant_id` e nível, sem PII. [29](29-auditoria.md) define a auditoria. Não há especificação de logs por portal.

| Canal de log | Conteúdo | Portais | Retenção | Estado |
|---|---|---|---|---|
| Aplicação | Erros, desempenho, requisição | Todos | 90 dias ([10](10-implantacao-operacao.md)) | Definido |
| Segurança | Login, falha, bloqueio, MFA, acesso negado | Todos | Conforme [29](29-auditoria.md), seção 7 | Definido |
| Auditoria de negócio | Alteração de dado, leitura sensível, exportação | Todos | Conforme [29](29-auditoria.md) | Definido. Campo `portal` incluído em [29](29-auditoria.md), seção 2 (AUD-04) |
| Integração | Chamada a provedor, webhook, falha de conector | Gestão, desenvolvedor | 90 dias (LOG-03) | **Especificado** em [49](49-logs-testes-por-portal.md), seção 2 |
| Job e fila | Processamento, reprocessamento, expurgo | Plataforma e entidade | 90 dias (LOG-03) | **Especificado** em [49](49-logs-testes-por-portal.md), seção 3 |
| Logger técnico (módulo `spec_gestao_logger_completo`) | — | — | — | Revisar: retirar dados de log da especificação, conforme o catálogo |

**Lacunas:** LOG-01 a LOG-03 (seção 5).

### 4.2 Testes

[24](24-operacao-continuidade-qualidade.md), seção 5 define a estratégia geral. Falta a matriz por portal. Cada portal precisa de um conjunto mínimo:

| Portal | Teste de isolamento | Teste de permissão | Teste de fluxo principal | Teste de acessibilidade |
|---|---|---|---|---|
| Desenvolvedor | O Editor de portais publica só para o escopo escolhido | Publicação não é aprovada pelo próprio editor (D-23) | Criar entidade e unidade (provisionamento, seção 4 de [23](23-dominios-provisionamento-ciclo-de-vida.md)) | Telas de leitura |
| Gestão | Cross-tenant e cross-unidade | Papel sem permissão não vê o módulo | Matrícula, cobrança, emissão de documento | Telas principais |
| Professor | Só turmas vinculadas | Nota só pelo professor da turma | Lançar nota e frequência | Diário |
| Aluno | Só os próprios dados | Não vê nota de outro aluno | Realizar simulado, rematrícula | Telas principais |
| Responsáveis | Só dependentes com vínculo ativo | Vínculo revogado perde acesso em até 30 s ([30](30-cache.md), seção 4) | Pagar fatura e rematricular | Telas principais |
| Terceiros | Só o próprio fornecedor | Sem acesso a financeiro interno | Emitir NF-e de serviço | Telas principais |

Itens de teste comuns: fluxo ponta a ponta por portal a cada release, varredura de log sem PII, e varredura de auditoria sem segredo ([29](29-auditoria.md), seção 9).

**Lacunas:** TST-01 a TST-03 (seção 5).

### 4.3 Segurança por portal

[05](05-seguranca.md) é genérico. Falta o que muda entre portais:

| Portal | Autenticação | Sessão | Dados e restrições especiais |
|---|---|---|---|
| Desenvolvedor | Senha e passkey obrigatória ([06](06-identidade-acesso.md), seção 10) | Curta; reautenticação antes de publicar | Acesso ao Editor de portais é registrado; sem acesso a dado de cliente sem chamado ([29](29-auditoria.md), seção 8) |
| Gestão | Senha e MFA conforme política da entidade ([06](06-identidade-acesso.md), seção 5) | Padrão | Consulta por CPF com finalidade ([21](21-busca-e-armazenamento.md), seção 6.8) |
| Professor | Senha e MFA conforme política | Padrão | Dado de aluno só das turmas |
| Aluno | Senha e MFA opcional por política | Padrão | Dado de menor de idade: regra de [07](07-privacidade-lgpd.md) e [26](26-sdd-juridico-regulatorio.md) |
| Responsáveis | Senha e MFA obrigatório para pagamento ([20](20-pagamentos-seguranca.md), seção 19.2) | Padrão | Vínculo de responsabilidade verificado; dado do filho é de acesso restrito |
| Terceiros | Senha e MFA obrigatório | Curta | Escopo contratual; sem financeiro interno; dados bancários exigem MFA |

**Lacuna de segurança:** o portal dos responsáveis não tem regra de verificação do vínculo de responsabilidade legal. Ver SEG-01 (seção 5).

### 4.4 Auditoria por portal

[29](29-auditoria.md), seção 2 tem o esquema do evento, mas **não tem o campo `portal`**. A v1 exige o campo (`spec` de navegação, seção 6 — `audit_logs` com `portal`). Sem ele não é possível separar a auditoria do portal do desenvolvedor da auditoria do portal de gestão.

**Correção proposta:** incluir `portal` (enum: `desenvolvedor`, `gestao`, `professor`, `aluno`, `responsaveis`, `terceiros`, `sistema`) na tabela de campos de [29](29-auditoria.md), seção 2.

---

## 5. Lacunas e decisões pendentes

| # | Assunto | Tipo | Dono |
|---|---|---|---|
| MOD-01 | Módulos Financeiro, Contábil, Patrimônio, Frotas, Suprimentos e Pessoas da plataforma: manter ou remover | **Decidido** em 03/11/2026: mantidos, para a gestão da própria empresa desenvolvedora | Autor |
| MOD-02 | Planejamento acadêmico, institucional e de desenvolvimento: definir ou remover | **Decidido** em 03/11/2026: analisado e implementado ([37](37-planejamento-e-empenho.md)) | Autor |
| MOD-03 | Empenho: aplicável ou não | **Decidido** em 03/11/2026: só para entidade pública ([37](37-planejamento-e-empenho.md)) | Autor, jurídico |
| MOD-04 | Gabarito óptico: próprio ou terceiro | **Decidido** em 03/11/2026: as duas opções, próprio e de terceiro, por configuração da entidade | Autor |
| MOD-05 | Plano que muda o simulado (PRO) | **Decidido** em 03/11/2026: o PRO libera correção por IA e ranking | Comercial |
| MOD-06 | Nota de IA em simulado | **Decidido** em 03/11/2026: a IA sugere, e o professor e a coordenação pedagógica confirmam. Nada chega ao aluno sem aprovação | Autor |
| MOD-07 | Especificação de Gerador de documentos na v2 | **Escrito** em [48](48-gerador-de-documentos-por-portal.md). Revisão do owner pendente | Owner de Gestão de documentos |
| MOD-08 | Especificação de Simulados na v2 (banco, prova, correção, relatórios) | **Escrito** em [47](47-simulados-por-portal.md). Revisão do owner pendente | Owner de Simulados |
| MOD-09 | Especificação de Matrícula e rematrícula (M-01 a M-09) | **Escrito** em [46](46-matricula-e-rematricula-por-portal.md). Revisão do owner pendente | Owner de Acadêmico |
| MOD-10 | Remover a página de gestão de documentos da UI da biblioteca | **Escrito** em [68](68-biblioteca-por-portal.md), seção 1: a página sai da UI da biblioteca | Owner de Biblioteca |
| MOD-11 | Unificar Atendimento (SAC, helpdesk, chat) com DDL | **Escrito** em [32](32-atendimento-privacidade-por-portal.md), com DDL em [51](51-ddl-modulos-novos.md), seção 1 | Owner de Atendimento |
| MOD-12 | Renomear os três "builders" (seção 3.4) | **Feito** em 03/11/2026: Editor de portais em [23](23-dominios-provisionamento-ciclo-de-vida.md), editor de modelos em [48](48-gerador-de-documentos-por-portal.md) | Autor |
| LOG-01 | Especificação de logs de integração | **Escrito** em [49](49-logs-testes-por-portal.md), seção 2 | Integrações |
| LOG-02 | Especificação de logs de job e fila | **Escrito** em [49](49-logs-testes-por-portal.md), seção 3 | Operação |
| LOG-03 | Retenção de logs de integração e de job | **Decidido** em 03/11/2026: 90 dias | Autor |
| TST-01 | Conjunto de testes por portal (seção 4.2) em CI | **Escrito** em [49](49-logs-testes-por-portal.md), seção 4 | QA |
| TST-02 | Teste de isolamento para cada par portal e módulo | **Escrito** em [49](49-logs-testes-por-portal.md), seção 5 | QA |
| TST-03 | Teste de acessibilidade por portal | **Escrito** em [49](49-logs-testes-por-portal.md), seção 6 | Frontend |
| SEG-01 | Regra de verificação do vínculo de responsabilidade legal | **Decidido** em 03/11/2026: documento e vínculo cadastrado pela escola. Parecer do jurídico pendente | Autor, jurídico |
| AUD-04 | Adicionar campo `portal` ao evento de auditoria | **Feito** em [29](29-auditoria.md), seção 2, campo `portal` | Segurança |

---

## 6. Critérios de aceite

- [ ] Cada módulo tem um dono de dado e um portal de entrada documentados.
- [ ] Nenhum documento de módulo descreve o mesmo domínio que outro.
- [ ] Protocolo, CRM e Atendimento têm fronteiras escritas e testadas.
- [ ] Financeiro e contábil da plataforma e da entidade não compartilham banco.
- [ ] Matrícula, rematrícula e simulados têm regra de validação completa (MOD-08, MOD-09).
- [ ] Logs, testes, segurança e auditoria têm regra por portal (seção 4).
- [ ] Campo `portal` presente em toda auditoria.
- [ ] Itens **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).

---

## 7. Módulos adicionados em 03/11/2026

Estes módulos ganharam especificação própria. Cada um tem seu portal e seu dono de dado na matriz da seção 2:

| Módulo | Documento | Dono de dado | Portal principal |
|---|---|---|---|
| Aulas online e reuniões ao vivo | [40](40-aulas-online-por-portal.md) | Entidade (unidade) | Professor e aluno |
| Formulários e pesquisas | [41](41-formularios-e-pesquisas.md) | Módulo que criou o formulário | Gestão |
| Preceptoria | [42](42-preceptoria-por-portal.md) | Entidade (unidade) | Preceptor e residente |
| Gestão pastoral | [43](43-pastoral-por-portal.md) | Entidade (unidade) | Equipe pastoral |
| Agendamento de ambientes e equipamentos | [44](44-agendamento-ambientes-equipamentos.md) | Entidade (unidade) | Professor e responsável |
| Matrícula e rematrícula | [46](46-matricula-e-rematricula-por-portal.md) | Entidade (unidade) | Secretaria e responsável |
| Simulados e correção por IA | [47](47-simulados-por-portal.md) | Entidade (unidade) | Professor e aluno |
| Gerador de documentos | [48](48-gerador-de-documentos-por-portal.md) | Entidade (unidade) | Secretaria |
| Logs, testes e acessibilidade | [49](49-logs-testes-por-portal.md) | Plataforma | Desenvolvedor |
| Medicina do trabalho | [52](52-medicina-do-trabalho-especificacao.md) | Entidade (unidade) | Médico e SESMT |

Os DDL de todos esses módulos estão em [51](51-ddl-modulos-novos.md).
