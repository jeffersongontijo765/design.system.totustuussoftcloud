# SDD TotusTuus SoftCloud — documento único (v1 + v2), por partes

Gerado em 2026-11-04 por `inventario/gera_sdd_unificado.py`. Não editar à mão: a fonte são os documentos da v2, as especificações da v1 e a estrutura em `inventario/sdd_partes.py`.

## Como ler

- O SDD está dividido em 20 partes, por assunto; a última é o plano de implementação. Cada parte começa com uma visão geral: resumo, diagramas dos fluxos e estados e regras principais.
- Depois da visão geral vem o texto integral de cada documento da v2 da parte e, logo abaixo de cada um, o texto integral das especificações da v1 que ele absorveu.
- No fim de cada parte estão as especificações da v1 que viraram fichas do kit-starter.
- Quando a v1 e a v2 divergem, vale a v2. Nenhum link aponta para fora deste arquivo.

## Glossário

| Termo | Significado |
|---|---|
| Plataforma | A empresa que opera o SaaS. Tenant reservado, com contas de plataforma ([03](parte-02-arquitetura-e-tenancy.md#doc-03), seção 1) |
| Mantenedora | Cliente que contrata o SaaS; agrupa entidades |
| Entidade | Instituição (razão social). Tem um banco de identidade com o cadastro civil |
| Unidade | Campus, filial ou polo da entidade. Tem um banco próprio com os dados operacionais |
| Tenant | Nível de isolamento de dados: entidade e unidade. Toda consulta filtra pelo tenant do contexto |
| Banco master | Banco da plataforma: catálogo de entidades e unidades, contas de plataforma, CRM da plataforma, índice de pessoas |
| Conta global | Conta única da pessoa, por e-mail verificado, válida em todas as entidades ([06](parte-03-identidade-acesso-e-permissoes.md#doc-06), seção 12) |
| Vínculo | Ligação da conta com uma entidade e uma unidade, com um papel (aluno, responsável, professor, colaborador, terceiro) |
| Contexto | Entidade e unidade ativas na sessão; o token leva só o contexto ativo |
| Papel | Conjunto de permissões com nível de 0 a 7 ([78](parte-03-identidade-acesso-e-permissoes.md#doc-78)) |
| Permissão | Ação autorizada no formato `modulo.recurso.acao`; sem permissão explícita, a ação é negada (default-deny) |
| Step-up | Nova autenticação recente exigida antes de uma ação sensível |
| Break-glass | Credencial de emergência guardada offline em dois cofres ([06](parte-03-identidade-acesso-e-permissoes.md#doc-06), seção 10) |
| Separação de funções | Quem cria um objeto financeiro, de compra ou de consentimento não o aprova ([78](parte-03-identidade-acesso-e-permissoes.md#doc-78), seção 2.2) |
| Portal | Superfície do produto para um público: desenvolvedor, gestão, professor, aluno, responsáveis, terceiros |
| Área e módulo | Área agrupa módulos dentro de um portal ([31](parte-05-portais-navegacao-e-interface.md#doc-31), seção 2) |
| Protocolo | Número de acompanhamento de requerimento ou solicitação, consultável por número e CPF |
| Matrícula condicional | Matrícula aceita com pendência e prazo; vencido o prazo, é cancelada por job ([46](parte-09-secretaria-matricula-e-documentos.md#doc-46), M-04) |
| Diário | Registro de aula, chamada, conteúdo e notas da turma ([61](parte-08-academico.md#doc-61)) |
| Sistema avaliativo | Escala, média, recuperação e regra de aprovação de uma turma ([59](parte-08-academico.md#doc-59), seção 4) |
| Ledger | Registro financeiro em partidas dobradas de todo movimento ([20](parte-10-financeiro-pagamentos-e-fiscal.md#doc-20), seção 5) |
| Split | Divisão do pagamento entre recebedores no gateway ([34](parte-10-financeiro-pagamentos-e-fiscal.md#doc-34), seção 3) |
| NFS-e | Nota fiscal de serviço eletrônica ([34](parte-10-financeiro-pagamentos-e-fiscal.md#doc-34), seção 5) |
| DPO (encarregado) | Pessoa indicada para responder pela proteção de dados; a plataforma e cada entidade têm o seu |
| ROPA | Registro das operações de tratamento de dados pessoais |
| ANPD | Autoridade Nacional de Proteção de Dados |
| SLA | Prazo de atendimento com contagem pausada nos estados de espera ([32](parte-04-seguranca-privacidade-e-auditoria.md#doc-32), seção 2.3) |
| DDL | Definição das tabelas do banco ([51](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#doc-51)) |
| ADR | Registro de decisão de arquitetura ([02](parte-02-arquitetura-e-tenancy.md#doc-02), seção 6) |
| SBOM e SLSA | Lista de componentes do build e procedência verificável do artefato ([05](parte-04-seguranca-privacidade-e-auditoria.md#doc-05), [10](parte-17-operacao-qualidade-testes-e-ti.md#doc-10)) |
| D-xx, L-xx, DP-xx | Decisão do autor, regra de licenciamento ou permissão aprovada, e decisão tomada por padrão ([80](parte-19-pendencias-decisoes-e-rastreabilidade.md#doc-80)) |
| [Declarado] e [Planejado] | Afirmação da v1 ainda não reproduzida; item ainda não implementado, com dono e critério de aceite ([00](parte-01-visao-e-escopo.md#doc-00)) |
| [A], [V] e [P] | Norma consolidada; norma a verificar; ponto que depende de parecer ([26](parte-18-juridico-e-regulatorio.md#doc-26)) |

## Mapa por portal e módulo

Para cada portal: as áreas, os módulos e os documentos deste SDD que os especificam (da matriz do documento 31).

### Portal do Desenvolvedor (`desenvolvedor.`) — equipe da plataforma

| Área | Módulos | Onde está especificado |
|---|---|---|
| Plataforma e clientes | Clientes (tenants), licenciamento, assinaturas, faturamento de clientes, limites e consumo, domínios, provisionamento | [23](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md#doc-23) |
| Editor de portais | Páginas, rotas, layouts, blocos, publicação e rollback | [23](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md#doc-23), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Comercial da plataforma | CRM da plataforma, leads, propostas, comissões | [22](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md#doc-22), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Financeiro da plataforma | Contas a pagar e a receber da própria empresa | [31](parte-05-portais-navegacao-e-interface.md#doc-31), [34](parte-10-financeiro-pagamentos-e-fiscal.md#doc-34) |
| Contábil da plataforma | Plano de contas, razão, fechamento da empresa, tributos e obrigações fiscais da empresa | [31](parte-05-portais-navegacao-e-interface.md#doc-31), [22](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md#doc-22) |
| Operações internas | Patrimônio, frotas, suprimentos da empresa | [19](parte-07-regras-gerais-dos-modulos-de-gestao.md#doc-19), [80](parte-19-pendencias-decisoes-e-rastreabilidade.md#doc-80) |
| Pessoas da plataforma | Departamento pessoal, recursos humanos, medicina e segurança do trabalho da empresa | [39](parte-11-pessoas-departamento-pessoal-e-sst.md#doc-39) |
| Suporte | Chamados dos clientes, base de conhecimento, SLA | [32](parte-04-seguranca-privacidade-e-auditoria.md#doc-32), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Segurança e operação | Acesso, MFA, auditoria, privacidade (DPO), TI, configurações do sistema, integrações globais, painel de bancos de dados | [05](parte-04-seguranca-privacidade-e-auditoria.md#doc-05), [07](parte-04-seguranca-privacidade-e-auditoria.md#doc-07), [10](parte-17-operacao-qualidade-testes-e-ti.md#doc-10), [34](parte-10-financeiro-pagamentos-e-fiscal.md#doc-34) |

### Portal de Gestão (`gestao.`) — equipe administrativa da entidade

| Área | Módulos | Onde está especificado |
|---|---|---|
| Acadêmico | Administração escolar (estrutura acadêmica), pedagógico (coordenação e diário), calendário e eventos, séries e turmas (grade de horários), regras de aprovação (sistemas avaliativos, boletim e conselho de classe), ocorrências disciplinares, planos de aula e de ensino, estágio e TCC, prontuário e portfólio do aluno, livros digitais e arquivo morto, preceptoria, gestão pastoral, aulas online, agendamento de ambientes e equipamentos, formulários e pesquisas, relatórios acadêmicos e censo | [17](parte-07-regras-gerais-dos-modulos-de-gestao.md#doc-17), [55](parte-08-academico.md#doc-55), [58](parte-08-academico.md#doc-58), [69](parte-08-academico.md#doc-69), [40](parte-08-academico.md#doc-40), [44](parte-08-academico.md#doc-44) |
| Secretaria | Matrículas, rematrículas, transferências, enturmação, ficha cadastral, protocolo de atendimento, emissão de documentos, processo seletivo e lista de espera | [46](parte-09-secretaria-matricula-e-documentos.md#doc-46), [48](parte-09-secretaria-matricula-e-documentos.md#doc-48) |
| Gestão de documentos | Documentos recebidos (validação), documentos administrativos (tramitação), documentos emitidos (modelos e emissão), serviços comuns (assinatura, protocolo e armazenamento) | [54](parte-09-secretaria-matricula-e-documentos.md#doc-54) |
| Simulados | Banco de questões, geração de provas, correção, gabarito, ranking | [47](parte-08-academico.md#doc-47), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Biblioteca | Acervo, empréstimos, reservas, multas, biblioteca digital | [68](parte-08-academico.md#doc-68), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Financeiro da entidade | Mensalidades, títulos, cobrança, régua, conciliação, centros de custo, contas a pagar, cheques, caixa físico, fluxo de caixa e DRE, gateways e split | [17](parte-07-regras-gerais-dos-modulos-de-gestao.md#doc-17), [18](parte-07-regras-gerais-dos-modulos-de-gestao.md#doc-18), [20](parte-10-financeiro-pagamentos-e-fiscal.md#doc-20), [34](parte-10-financeiro-pagamentos-e-fiscal.md#doc-34), [71](parte-10-financeiro-pagamentos-e-fiscal.md#doc-71) |
| Contábil e fiscal da entidade | Plano de contas da entidade, tributos, retenções, obrigações, NFSe | [31](parte-05-portais-navegacao-e-interface.md#doc-31), [34](parte-10-financeiro-pagamentos-e-fiscal.md#doc-34), [26](parte-18-juridico-e-regulatorio.md#doc-26) |
| Comercial e admissões | CRM do tenant (captação, pré-cadastro, inscrição) | [22](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md#doc-22) |
| Pessoas e RH | HCM, folha, ponto, férias, avaliação de desempenho, SST | [18](parte-07-regras-gerais-dos-modulos-de-gestao.md#doc-18), [39](parte-11-pessoas-departamento-pessoal-e-sst.md#doc-39), [52](parte-11-pessoas-departamento-pessoal-e-sst.md#doc-52) |
| Suprimentos e compras | Requisição, cotação, pedido, almoxarifado, merenda | [19](parte-07-regras-gerais-dos-modulos-de-gestao.md#doc-19) |
| Patrimônio e frotas | Bens, depreciação, veículos, manutenção, rotas | [19](parte-07-regras-gerais-dos-modulos-de-gestao.md#doc-19) |
| Contratos | Contratos de fornecedor, contratos de aluno, contratos de pessoal | [17](parte-07-regras-gerais-dos-modulos-de-gestao.md#doc-17), [33](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-33), [53](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-53) |
| Atendimento | SAC, helpdesk, chat, tickets | [32](parte-04-seguranca-privacidade-e-auditoria.md#doc-32), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Arquivos | Armazenamento de arquivos | [21](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#doc-21) |
| Relatórios e gráficos | Painéis, gráficos salvos | [56](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#doc-56), [69](parte-08-academico.md#doc-69), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Configuração e acesso | Unidades, usuários, vínculos, privacidade da entidade, configurações da entidade, campos personalizados, notificações, integrações educacionais oficiais, importação de dados, acesso físico e portaria, TI da entidade | [06](parte-03-identidade-acesso-e-permissoes.md#doc-06), [32](parte-04-seguranca-privacidade-e-auditoria.md#doc-32), [35](parte-03-identidade-acesso-e-permissoes.md#doc-35), [36](parte-17-operacao-qualidade-testes-e-ti.md#doc-36), [56](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#doc-56), [57](parte-13-atendimento-e-notificacoes.md#doc-57), [70](parte-14-integracoes-e-importacao.md#doc-70), [72](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#doc-72), [74](parte-14-integracoes-e-importacao.md#doc-74) |
| Planejamento acadêmico, institucional e de desenvolvimento | Planejamento acadêmico, planejamento institucional, planejamento de desenvolvimento de pessoas | [37](parte-08-academico.md#doc-37), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Empenho | Empenho, liquidação e pagamento (só entidade pública) | [37](parte-08-academico.md#doc-37), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |

### Portal do Professor (`portal-do-professor.`)

| Área | Módulos | Onde está especificado |
|---|---|---|
| Classe | Turmas e disciplinas do próprio docente, mural, materiais, tarefas | [81](parte-08-academico.md#doc-81), [80](parte-19-pendencias-decisoes-e-rastreabilidade.md#doc-80) |
| Diário | Frequência, conteúdo, notas, plano de aula | [22](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md#doc-22) |
| Simulados | Elaboração de questões, agendamento, resultados da turma | [47](parte-08-academico.md#doc-47), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Biblioteca | Consulta de acervo, indicação de leitura | [68](parte-08-academico.md#doc-68) |
| Protocolos e pedidos | Solicitação de material, reserva de laboratório, justificativa | [31](parte-05-portais-navegacao-e-interface.md#doc-31), [44](parte-08-academico.md#doc-44) |
| Documentos e pessoal | Declarações, contrato de trabalho, holerite, ponto | [39](parte-11-pessoas-departamento-pessoal-e-sst.md#doc-39), [34](parte-10-financeiro-pagamentos-e-fiscal.md#doc-34) |
| Relatórios | Rendimento da turma, ficha individual | [69](parte-08-academico.md#doc-69) |
| Agenda e comunicação | Horário e calendário das turmas, aulas online, notificações, meu perfil | [58](parte-08-academico.md#doc-58), [60](parte-08-academico.md#doc-60), [40](parte-08-academico.md#doc-40), [57](parte-13-atendimento-e-notificacoes.md#doc-57), [76](parte-05-portais-navegacao-e-interface.md#doc-76) |
| Acompanhamento pedagógico | Ocorrências da turma, orientação de estágio e TCC, preceptoria, portfólio dos alunos, formulários e pesquisas, pastoral | [63](parte-08-academico.md#doc-63), [65](parte-08-academico.md#doc-65), [42](parte-08-academico.md#doc-42), [66](parte-08-academico.md#doc-66), [41](parte-08-academico.md#doc-41), [43](parte-08-academico.md#doc-43) |

### Portal do Aluno (`portal-do-aluno.`)

| Área | Módulos | Onde está especificado |
|---|---|---|
| Classe e diário | Disciplinas, materiais, entregas, boletim, presença | [61](parte-08-academico.md#doc-61), [62](parte-08-academico.md#doc-62), [81](parte-08-academico.md#doc-81) |
| Simulados | Simulados agendados, realização de prova, gabarito e comentários | [47](parte-08-academico.md#doc-47) |
| Biblioteca | Empréstimos, prazos, renovação, pesquisa de acervo | [68](parte-08-academico.md#doc-68) |
| Protocolos online | Requerimento de segunda chamada, declaração de matrícula | [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Documentos | Boletim oficial, histórico, declarações | [21](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#doc-21), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Matrícula | Confirmação para o ano seguinte, eletivas, rematrícula | [46](parte-09-secretaria-matricula-e-documentos.md#doc-46), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Financeiro | Mensalidades, boleto, PIX, comprovantes | [34](parte-10-financeiro-pagamentos-e-fiscal.md#doc-34), [20](parte-10-financeiro-pagamentos-e-fiscal.md#doc-20) |
| Privacidade | Dados cadastrais, solicitações LGPD | [07](parte-04-seguranca-privacidade-e-auditoria.md#doc-07) |
| Agenda e comunicação | Horário da turma, calendário e eventos, aulas online, notificações, meu perfil | [58](parte-08-academico.md#doc-58), [60](parte-08-academico.md#doc-60), [40](parte-08-academico.md#doc-40), [57](parte-13-atendimento-e-notificacoes.md#doc-57), [76](parte-05-portais-navegacao-e-interface.md#doc-76) |
| Vida acadêmica | Ocorrências próprias, estágio e TCC, portfólio, preceptoria, formulários e pesquisas, pastoral | [63](parte-08-academico.md#doc-63), [65](parte-08-academico.md#doc-65), [66](parte-08-academico.md#doc-66), [42](parte-08-academico.md#doc-42), [41](parte-08-academico.md#doc-41), [43](parte-08-academico.md#doc-43) |

### Portal dos Pais e Responsáveis (`portal-dos-responsaveis.`)

| Área | Módulos | Onde está especificado |
|---|---|---|
| Acompanhamento | Notas, faltas, ocorrências, comunicados, entradas e saídas da portaria | [61](parte-08-academico.md#doc-61), [62](parte-08-academico.md#doc-62), [63](parte-08-academico.md#doc-63), [35](parte-03-identidade-acesso-e-permissoes.md#doc-35), [57](parte-13-atendimento-e-notificacoes.md#doc-57) |
| Biblioteca e simulados | Empréstimos e desempenho dos filhos | [68](parte-08-academico.md#doc-68), [47](parte-08-academico.md#doc-47) |
| Protocolos da família | Mudança de turno, saída antecipada, documentos | [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Financeiro e matrícula | Faturas dos filhos, PIX, rematrícula online, assinatura do contrato | [26](parte-18-juridico-e-regulatorio.md#doc-26), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Privacidade e menores | Consentimento de imagem, dados dos filhos | [07](parte-04-seguranca-privacidade-e-auditoria.md#doc-07) |
| Agenda e comunicação | Horário e calendário dos dependentes, eventos e autorizações, notificações, meu perfil | [58](parte-08-academico.md#doc-58), [60](parte-08-academico.md#doc-60), [43](parte-08-academico.md#doc-43), [57](parte-13-atendimento-e-notificacoes.md#doc-57), [76](parte-05-portais-navegacao-e-interface.md#doc-76) |

### Portal de Terceiros (`portal-de-terceiros.`)

| Área | Módulos | Onde está especificado |
|---|---|---|
| Faturamento de serviços | Emissão e envio de NF-e de serviço, acompanhamento de pagamento, extrato | [38](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-38), [34](parte-10-financeiro-pagamentos-e-fiscal.md#doc-34) |
| Pedidos e contratos | Pedidos de compra pendentes, contratos em vigor | [38](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-38), [33](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-33) |
| Documentos da empresa | Certidões, contrato social, alvarás, seguro | [38](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-38) |
| Prestação de serviço | Ordens de serviço, relatórios de execução, cronograma | [38](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-38) |
| Chamados | Abertura de chamado de manutenção, solicitação de acesso à unidade | [32](parte-04-seguranca-privacidade-e-auditoria.md#doc-32), [35](parte-03-identidade-acesso-e-permissoes.md#doc-35), [31](parte-05-portais-navegacao-e-interface.md#doc-31) |
| Configurações e integrações | Dados da empresa, responsáveis técnicos, dados bancários, integrações via API | [38](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-38), [06](parte-03-identidade-acesso-e-permissoes.md#doc-06) |
| Habilitação e acesso | Cadastro e habilitação do prestador, pessoas e papéis do prestador, tipo de prestador, meu perfil | [38](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-38), [76](parte-05-portais-navegacao-e-interface.md#doc-76) |

## Índice

- [Parte 1 — Visão e escopo](parte-01-visao-e-escopo.md)
  - [00 — SDD v2 — TotusTuus SoftCloud](parte-01-visao-e-escopo.md#doc-00)
    - [v1 `sdd-mestre-php8-mvc-saas.md`](parte-01-visao-e-escopo.md#v1-sdd-mestre-php8-mvc-saas-md)
  - [01 — Visão e Escopo](parte-01-visao-e-escopo.md#doc-01)
    - [v1 `01-vision-scope.md`](parte-01-visao-e-escopo.md#v1-01-vision-scope-md)
  - [12 — Catálogo de Módulos](parte-01-visao-e-escopo.md#doc-12)
  - [13 — Achados da v1](parte-01-visao-e-escopo.md#doc-13)
- [Parte 2 — Arquitetura e tenancy](parte-02-arquitetura-e-tenancy.md)
  - [02 — Arquitetura de Solução](parte-02-arquitetura-e-tenancy.md#doc-02)
    - [v1 `02-solution-architecture.md`](parte-02-arquitetura-e-tenancy.md#v1-02-solution-architecture-md)
  - [03 — Domínio e Multi-Tenancy](parte-02-arquitetura-e-tenancy.md#doc-03)
    - [v1 `03-domain-model.md`](parte-02-arquitetura-e-tenancy.md#v1-03-domain-model-md)
    - [v1 `06-tenancy.md`](parte-02-arquitetura-e-tenancy.md#v1-06-tenancy-md)
  - [04 — API REST](parte-02-arquitetura-e-tenancy.md#doc-04)
    - [v1 `04-api-standards.md`](parte-02-arquitetura-e-tenancy.md#v1-04-api-standards-md)
  - [14 — Integração entre Módulos](parte-02-arquitetura-e-tenancy.md#doc-14)
  - [30 — Cache: Camadas, Chaves, Validade e Invalidação](parte-02-arquitetura-e-tenancy.md#doc-30)
  - [v1 `spec_education_saas_architecture.md`](parte-02-arquitetura-e-tenancy.md#v1-spec-education-saas-architecture-md)
- [Parte 3 — Identidade, acesso e permissões](parte-03-identidade-acesso-e-permissoes.md)
  - [06 — Identidade, Autenticação e Autorização](parte-03-identidade-acesso-e-permissoes.md#doc-06)
    - [v1 `07-identity-auth.md`](parte-03-identidade-acesso-e-permissoes.md#v1-07-identity-auth-md)
  - [78 — Permissões, papéis e níveis de acesso por portal](parte-03-identidade-acesso-e-permissoes.md#doc-78)
  - [35 — Acesso Físico e Segurança: Portaria, Catracas, Câmeras, Portas e Biometria, por Portal](parte-03-identidade-acesso-e-permissoes.md#doc-35)
  - [v1 `client-migration-module-spec-completo.md`](parte-03-identidade-acesso-e-permissoes.md#v1-client-migration-module-spec-completo-md)
  - [v1 `spec_gestao_autenticacao_completo.md`](parte-03-identidade-acesso-e-permissoes.md#v1-spec-gestao-autenticacao-completo-md)
  - [v1 `spec_gestao_cookies_sessions.md`](parte-03-identidade-acesso-e-permissoes.md#v1-spec-gestao-cookies-sessions-md)
  - [v1 `spec_gestao_notificacoes.md`](parte-03-identidade-acesso-e-permissoes.md#v1-spec-gestao-notificacoes-md)
  - [v1 `spec_gestao_notificacoes_revisada.md`](parte-03-identidade-acesso-e-permissoes.md#v1-spec-gestao-notificacoes-revisada-md)
- [Parte 4 — Segurança, privacidade e auditoria](parte-04-seguranca-privacidade-e-auditoria.md)
  - [05 — Segurança](parte-04-seguranca-privacidade-e-auditoria.md#doc-05)
    - [v1 `05-security-architecture.md`](parte-04-seguranca-privacidade-e-auditoria.md#v1-05-security-architecture-md)
  - [07 — Privacidade e LGPD](parte-04-seguranca-privacidade-e-auditoria.md#doc-07)
    - [v1 `08-privacy-lgpd.md`](parte-04-seguranca-privacidade-e-auditoria.md#v1-08-privacy-lgpd-md)
  - [29 — Auditoria: Registro, Integridade, Acesso e Retenção](parte-04-seguranca-privacidade-e-auditoria.md#doc-29)
  - [32 — Atendimento (Help Desk, SAC), Privacidade, LGPD e Encarregado, por Portal](parte-04-seguranca-privacidade-e-auditoria.md#doc-32)
  - [v1 `spec-sub-sidebar-privacidade-lgpd.md`](parte-04-seguranca-privacidade-e-auditoria.md#v1-spec-sub-sidebar-privacidade-lgpd-md)
  - [v1 `spec_gestao_auditoria_completo.md`](parte-04-seguranca-privacidade-e-auditoria.md#v1-spec-gestao-auditoria-completo-md)
  - [v1 `spec_gestao_logger_completo.md`](parte-04-seguranca-privacidade-e-auditoria.md#v1-spec-gestao-logger-completo-md)
  - [v1 `spec_gestao_privacy_global_completo.md`](parte-04-seguranca-privacidade-e-auditoria.md#v1-spec-gestao-privacy-global-completo-md)
- [Parte 5 — Portais, navegação e interface](parte-05-portais-navegacao-e-interface.md)
  - [31 — Matriz de Portais, Fronteiras entre Módulos, Logs, Testes, Segurança e Auditoria](parte-05-portais-navegacao-e-interface.md#doc-31)
  - [08 — Frontend e Design System](parte-05-portais-navegacao-e-interface.md#doc-08)
    - [v1 `11-frontend-design-system-master-model.md`](parte-05-portais-navegacao-e-interface.md#v1-11-frontend-design-system-master-model-md)
  - [09 — Internacionalização e Localização](parte-05-portais-navegacao-e-interface.md#doc-09)
  - [75 — Análise por Escopo: Busca, Notificações, Perfil e Integrações](parte-05-portais-navegacao-e-interface.md#doc-75)
  - [76 — Meu Perfil, por Portal](parte-05-portais-navegacao-e-interface.md#doc-76)
  - [v1 `12-portals-navigation-sidebar-pages-spec.md`](parte-05-portais-navegacao-e-interface.md#v1-12-portals-navigation-sidebar-pages-spec-md)
- [Parte 6 — Plataforma SaaS: clientes, domínios, licenças e CRM](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md)
  - [23 — Domínios, Editor de portais, Autenticação, Provisionamento e Ciclo de Vida](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md#doc-23)
  - [77 — Licenciamento, planos, assinaturas e limites](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md#doc-77)
  - [22 — CRM: Dois Contextos, Canais de Captação e Papéis](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md#doc-22)
  - [v1 `spec_crm_funil_comercial.md`](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md#v1-spec-crm-funil-comercial-md)
  - [v1 `spec_gestao_marketing_redes_sociais.md`](parte-06-plataforma-saas-clientes-dominios-licencas-e-crm.md#v1-spec-gestao-marketing-redes-sociais-md)
- [Parte 7 — Regras gerais dos módulos de gestão](parte-07-regras-gerais-dos-modulos-de-gestao.md)
  - [17 — Regras de Validação dos Módulos Prioritários](parte-07-regras-gerais-dos-modulos-de-gestao.md#doc-17)
  - [18 — Regras de Validação: Cobrança, Notificações, Auditoria, RH e Contábil/Fiscal](parte-07-regras-gerais-dos-modulos-de-gestao.md#doc-18)
  - [19 — Regras de Validação: Demais Módulos do Catálogo](parte-07-regras-gerais-dos-modulos-de-gestao.md#doc-19)
- [Parte 8 — Acadêmico](parte-08-academico.md)
  - [55 — Verificação do Acadêmico: Cobertura, Lacunas e Ordem de Fechamento](parte-08-academico.md#doc-55)
  - [59 — Estrutura Acadêmica, por Portal: Cursos, Disciplinas, Grades, Períodos e Sistemas Avaliativos](parte-08-academico.md#doc-59)
  - [58 — Calendário Escolar e Eventos, por Portal](parte-08-academico.md#doc-58)
  - [60 — Turmas, Enturmação e Grade de Horários, por Portal](parte-08-academico.md#doc-60)
  - [61 — Diário Escolar, por Portal: Chamada, Faltas, Justificativas, Notas e Conteúdo](parte-08-academico.md#doc-61)
  - [81 — Classe: Mural, Materiais e Tarefas, por Portal](parte-08-academico.md#doc-81)
  - [62 — Boletim, Aprovação, Recuperação e Conselho de Classe, por Portal](parte-08-academico.md#doc-62)
  - [63 — Ocorrências Disciplinares e de Convivência, por Portal](parte-08-academico.md#doc-63)
  - [64 — Planos de Ensino e de Aula, por Portal](parte-08-academico.md#doc-64)
  - [65 — Estágio e TCC, por Portal](parte-08-academico.md#doc-65)
  - [66 — Prontuário e Portfólio do Aluno, por Portal](parte-08-academico.md#doc-66)
  - [67 — Livros Digitais e Arquivo Morto, por Portal](parte-08-academico.md#doc-67)
  - [68 — Biblioteca (Acervo, Empréstimos, Reservas, Multas e Salas de Leitura), por Portal](parte-08-academico.md#doc-68)
  - [69 — Relatórios, Exportações Regulatórias e Censo, por Portal](parte-08-academico.md#doc-69)
  - [40 — Aulas Online e Reuniões ao Vivo, por Portal](parte-08-academico.md#doc-40)
  - [41 — Formulários e Pesquisas (motor compartilhado, estilo Google Forms e Microsoft Forms)](parte-08-academico.md#doc-41)
  - [42 — Preceptoria e Autoavaliação, por Portal](parte-08-academico.md#doc-42)
  - [43 — Gestão Pastoral, por Portal (eventos, missas e celebrações, ações sociais)](parte-08-academico.md#doc-43)
  - [44 — Agendamento de Ambientes e Equipamentos, por Portal (Acadêmico)](parte-08-academico.md#doc-44)
  - [47 — Simulados e Correção de Redação, por Portal](parte-08-academico.md#doc-47)
  - [37 — Planejamento (Acadêmico, Institucional, de Desenvolvimento) e Empenho](parte-08-academico.md#doc-37)
  - [v1 `global_meeting_spec_v2_complete.md`](parte-08-academico.md#v1-global-meeting-spec-v2-complete-md)
  - [v1 `spec-gestao-preceptoria-autoavaliacao.md`](parte-08-academico.md#v1-spec-gestao-preceptoria-autoavaliacao-md)
  - [v1 `spec_gestao_academica_completo.md`](parte-08-academico.md#v1-spec-gestao-academica-completo-md)
  - [v1 `spec_gestao_biblioteca_academica.md`](parte-08-academico.md#v1-spec-gestao-biblioteca-academica-md)
  - [v1 `spec_gestao_biblioteca_completo.md`](parte-08-academico.md#v1-spec-gestao-biblioteca-completo-md)
  - [v1 `spec_gestao_simulados_ia.md`](parte-08-academico.md#v1-spec-gestao-simulados-ia-md)
- [Parte 9 — Secretaria, matrícula e documentos](parte-09-secretaria-matricula-e-documentos.md)
  - [46 — Matrícula e Rematrícula, por Portal (Acadêmico)](parte-09-secretaria-matricula-e-documentos.md#doc-46)
  - [48 — Gerador de Documentos, por Portal](parte-09-secretaria-matricula-e-documentos.md#doc-48)
  - [54 — Gestão de Documentos: Três Contextos e Serviços Comuns](parte-09-secretaria-matricula-e-documentos.md#doc-54)
  - [v1 `spec-builder-documentos-academicos.md`](parte-09-secretaria-matricula-e-documentos.md#v1-spec-builder-documentos-academicos-md)
  - [v1 `spec_gestao_documentos_completo.md`](parte-09-secretaria-matricula-e-documentos.md#v1-spec-gestao-documentos-completo-md)
- [Parte 10 — Financeiro, pagamentos e fiscal](parte-10-financeiro-pagamentos-e-fiscal.md)
  - [20 — Pagamentos e Recebimentos: Segurança, Validação e Conformidade](parte-10-financeiro-pagamentos-e-fiscal.md#doc-20)
  - [34 — Pagamentos, Gateways, Split, Notas Fiscais, Bancos e Carteiras, por Portal](parte-10-financeiro-pagamentos-e-fiscal.md#doc-34)
  - [71 — Financeiro Completo, por Portal: Pagamentos, Cheques, Caixa, Fluxo, DRE e Conciliação](parte-10-financeiro-pagamentos-e-fiscal.md#doc-71)
  - [v1 `spec_gestao_billing_cobranca_mensalidades.md`](parte-10-financeiro-pagamentos-e-fiscal.md#v1-spec-gestao-billing-cobranca-mensalidades-md)
  - [v1 `spec_gestao_contabil_fiscal_completo.md`](parte-10-financeiro-pagamentos-e-fiscal.md#v1-spec-gestao-contabil-fiscal-completo-md)
  - [v1 `spec_gestao_financeiro_completo.md`](parte-10-financeiro-pagamentos-e-fiscal.md#v1-spec-gestao-financeiro-completo-md)
- [Parte 11 — Pessoas, departamento pessoal e SST](parte-11-pessoas-departamento-pessoal-e-sst.md)
  - [39 — Departamento Pessoal, Recursos Humanos e Medicina do Trabalho, por Portal](parte-11-pessoas-departamento-pessoal-e-sst.md#doc-39)
  - [52 — Medicina e Segurança do Trabalho: PCMSO, PGR, LTCAT, CIPA e Ergonomia](parte-11-pessoas-departamento-pessoal-e-sst.md#doc-52)
  - [v1 `spec_gestao_pessoas_completo.md`](parte-11-pessoas-departamento-pessoal-e-sst.md#v1-spec-gestao-pessoas-completo-md)
  - [v1 `spec_gestao_rh_completo.md`](parte-11-pessoas-departamento-pessoal-e-sst.md#v1-spec-gestao-rh-completo-md)
  - [v1 `spec_gestao_seguranca_medicina_trabalho_completo.md`](parte-11-pessoas-departamento-pessoal-e-sst.md#v1-spec-gestao-seguranca-medicina-trabalho-completo-md)
- [Parte 12 — Suprimentos, patrimônio, frotas, contratos e terceiros](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md)
  - [33 — Gestão de Contratos, por Portal](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-33)
  - [53 — Pacote para Parecer Jurídico: Contratos, Declarações, Boletins e Demais Documentos](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-53)
  - [38 — Portal de Terceiros: Prestadores de Serviço, por Tipo, com Acesso Restrito ao Próprio Escopo](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#doc-38)
  - [v1 `spec_gestao_armazenamento_completo.md`](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#v1-spec-gestao-armazenamento-completo-md)
  - [v1 `spec_gestao_contratos_completo.md`](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#v1-spec-gestao-contratos-completo-md)
  - [v1 `spec_gestao_frotas_completo.md`](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#v1-spec-gestao-frotas-completo-md)
  - [v1 `spec_gestao_suprimentos_v3_consolidado.md`](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#v1-spec-gestao-suprimentos-v3-consolidado-md)
  - [v1 `spec_patrimonio_completo.md`](parte-12-suprimentos-patrimonio-frotas-contratos-e-terceiros.md#v1-spec-patrimonio-completo-md)
- [Parte 13 — Atendimento e notificações](parte-13-atendimento-e-notificacoes.md)
  - [57 — Notificações, por Portal](parte-13-atendimento-e-notificacoes.md#doc-57)
  - [v1 `SPEC-HELPDESK.md`](parte-13-atendimento-e-notificacoes.md#v1-spec-helpdesk-md)
  - [v1 `SPEC-LAYOUT-TICKET.md`](parte-13-atendimento-e-notificacoes.md#v1-spec-layout-ticket-md)
  - [v1 `spec_chat_rapido_sac.md`](parte-13-atendimento-e-notificacoes.md#v1-spec-chat-rapido-sac-md)
  - [v1 `spec_gestao_sac_base_conhecimento.md`](parte-13-atendimento-e-notificacoes.md#v1-spec-gestao-sac-base-conhecimento-md)
- [Parte 14 — Integrações e importação](parte-14-integracoes-e-importacao.md)
  - [16 — Integrações Externas: Plataforma (master) e Tenant](parte-14-integracoes-e-importacao.md#doc-16)
  - [74 — Integrações Educacionais Oficiais, por Portal](parte-14-integracoes-e-importacao.md#doc-74)
  - [70 — Importação de Dados e Carga Inicial, por Portal](parte-14-integracoes-e-importacao.md#doc-70)
  - [v1 `spec_complementar_integracoes_governanca.md`](parte-14-integracoes-e-importacao.md#v1-spec-complementar-integracoes-governanca-md)
- [Parte 15 — Inteligência artificial](parte-15-inteligencia-artificial.md)
  - [27 — Inteligência Artificial por Módulo e por Portal](parte-15-inteligencia-artificial.md#doc-27)
  - [28 — Cobertura de IA em Todos os Módulos](parte-15-inteligencia-artificial.md#doc-28)
- [Parte 16 — Dados, validações, configurações e armazenamento](parte-16-dados-validacoes-configuracoes-e-armazenamento.md)
  - [51 — DDL dos Módulos Novos e Pendentes](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#doc-51)
  - [15 — Validações de Dados, Transações e Integrações](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#doc-15)
  - [56 — Configurações e Relatórios: Cobertura e Lacunas](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#doc-56)
  - [72 — Campos Personalizados, por Portal](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#doc-72)
  - [21 — Busca Full-Text e Armazenamento de Arquivos (Storage + Metadados)](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#doc-21)
  - [v1 `06-i18n-l10n.md`](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#v1-06-i18n-l10n-md)
  - [v1 `chart-builder-spec-complete.md`](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#v1-chart-builder-spec-complete-md)
  - [v1 `language_locale_selector_spec.md`](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#v1-language-locale-selector-spec-md)
  - [v1 `spec-soft-delete-totustuus.md`](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#v1-spec-soft-delete-totustuus-md)
  - [v1 `spec_object_storage_digital_assets.md`](parte-16-dados-validacoes-configuracoes-e-armazenamento.md#v1-spec-object-storage-digital-assets-md)
- [Parte 17 — Operação, qualidade, testes e TI](parte-17-operacao-qualidade-testes-e-ti.md)
  - [10 — Implantação e Operação](parte-17-operacao-qualidade-testes-e-ti.md#doc-10)
    - [v1 `09-deployment-ops.md`](parte-17-operacao-qualidade-testes-e-ti.md#v1-09-deployment-ops-md)
  - [11 — Governança, Qualidade e Processo de Entrega](parte-17-operacao-qualidade-testes-e-ti.md#doc-11)
    - [v1 `10-governance-delivery.md`](parte-17-operacao-qualidade-testes-e-ti.md#v1-10-governance-delivery-md)
  - [24 — Operação, Continuidade, Qualidade e Lacunas do Projeto](parte-17-operacao-qualidade-testes-e-ti.md#doc-24)
  - [49 — Logs de Integração, de Job e de Fila, e Testes por Portal](parte-17-operacao-qualidade-testes-e-ti.md#doc-49)
  - [36 — Tecnologia da Informação (TI), por Portal](parte-17-operacao-qualidade-testes-e-ti.md#doc-36)
    - [v1 `sub_sidebar_itsm.php`](parte-17-operacao-qualidade-testes-e-ti.md#v1-sub-sidebar-itsm-php)
  - [v1 `penetration-test-spec-v2.md`](parte-17-operacao-qualidade-testes-e-ti.md#v1-penetration-test-spec-v2-md)
  - [v1 `slsa-build-spec.md`](parte-17-operacao-qualidade-testes-e-ti.md#v1-slsa-build-spec-md)
  - [v1 `spec_gestao_ti_completa.md`](parte-17-operacao-qualidade-testes-e-ti.md#v1-spec-gestao-ti-completa-md)
  - [v1 `TASKS_SPECS.md`](parte-17-operacao-qualidade-testes-e-ti.md#v1-tasks-specs-md)
- [Parte 18 — Jurídico e regulatório](parte-18-juridico-e-regulatorio.md)
  - [25 — Dossiê Jurídico e Análise das Lacunas](parte-18-juridico-e-regulatorio.md#doc-25)
  - [26 — SDD Jurídico-Regulatório](parte-18-juridico-e-regulatorio.md#doc-26)
  - [50 — Pacote para Parecer Jurídico e Conferência de Norma](parte-18-juridico-e-regulatorio.md#doc-50)
  - [73 — Resumo para o Jurídico: Perguntas dos Módulos Acadêmicos e Administrativos (docs 55 a 72)](parte-18-juridico-e-regulatorio.md#doc-73)
- [Parte 19 — Pendências, decisões e rastreabilidade](parte-19-pendencias-decisoes-e-rastreabilidade.md)
  - [45 — Pendências Consolidadas, por Responsável](parte-19-pendencias-decisoes-e-rastreabilidade.md#doc-45)
  - [80 — Decisões tomadas por padrão (delegadas pelo autor)](parte-19-pendencias-decisoes-e-rastreabilidade.md#doc-80)
  - [79 — Rastreabilidade v1 → v2](parte-19-pendencias-decisoes-e-rastreabilidade.md#doc-79)
  - [v1 `spec_gestao_bancos.md`](parte-19-pendencias-decisoes-e-rastreabilidade.md#v1-spec-gestao-bancos-md)
  - [v1 `spec_gestao_bancos_completo.md`](parte-19-pendencias-decisoes-e-rastreabilidade.md#v1-spec-gestao-bancos-completo-md)
  - [v1 `teste`](parte-19-pendencias-decisoes-e-rastreabilidade.md#v1-teste)
- [Parte 20 — Plano de implementação](parte-20-plano-de-implementacao.md)

---



O mesmo conteúdo, num arquivo só, está em `docs/SDD-UNIFICADO.md` (grande demais para o GitHub exibir na tela; abre pelo botão "Raw" ou num editor).
