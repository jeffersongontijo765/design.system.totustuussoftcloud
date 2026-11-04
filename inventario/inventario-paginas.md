# Inventário de telas por portal

Gerado por `inventario/gera_inventario.py` a partir de `docs/v2/31-matriz-portais-modulos.md`, seção 2.
Nível: portal → área → módulo. As telas de cada módulo são detalhadas antes de implementar.
Total de módulos listados: 245. Status inicial: nenhum implementado.


## 2.1 Portal do Desenvolvedor (`desenvolvedor.`) — equipe da plataforma

### Plataforma e clientes

Escopo: Ciclo de vida da seção 5 de [23](../docs/v2/23-dominios-provisionamento-ciclo-de-vida.md)

- [ ] Clientes (tenants)
- [ ] licenciamento
- [ ] assinaturas
- [ ] faturamento de clientes
- [ ] limites e consumo
- [ ] domínios
- [ ] provisionamento

### Editor de portais

Escopo: D-23. Chamado de "builder de portais" na v1. **Não é o editor de modelos do Gerador de documentos** (ver seção 3.4) Especificação: [23](../docs/v2/23-dominios-provisionamento-ciclo-de-vida.md), seção 3 (D-23)

- [ ] Páginas
- [ ] rotas
- [ ] layouts
- [ ] blocos
- [ ] publicação e rollback

### Comercial da plataforma

Escopo: [22](../docs/v2/22-crm-canais-e-papeis.md), seção 6.1. Não se mistura com o protocolo de atendimento (seção 3.2)

- [ ] CRM da plataforma
- [ ] leads
- [ ] propostas
- [ ] comissões

### Financeiro da plataforma

Escopo: **Decidido** em 03/11/2026: mantido para a gestão da própria empresa desenvolvedora. Especificação: [31](../docs/v2/31-matriz-portais-modulos.md), seção 3.3; [34](../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 3 (taxas de split)

- [ ] Contas a pagar e a receber **da própria empresa**

### Contábil da plataforma

Escopo: Mesma decisão do financeiro. Tributos da empresa: seção 3.3, confirmado pelo autor em 04/11/2026. Especificação: [31](../docs/v2/31-matriz-portais-modulos.md), seção 3.3; [22](../docs/v2/22-crm-canais-e-papeis.md), seção 5 (papéis contábil e fiscal)

- [ ] Plano de contas
- [ ] razão
- [ ] fechamento da empresa
- [ ] tributos e obrigações fiscais da empresa

### Operações internas

Escopo: **Decidido** em 03/11/2026: mantidos, como instâncias separadas dos módulos das entidades. Especificação: [19](../docs/v2/19-regras-modulos-3.md), seções 8 e 9; [80](../docs/v2/80-decisoes-por-padrao.md), DP-01 a DP-03

- [ ] Patrimônio
- [ ] frotas
- [ ] suprimentos da empresa

### Pessoas da plataforma

Escopo: Mesma decisão. O HCM das entidades não é o da plataforma. Três módulos separados, conforme HCM-01 e HCM-10 do [39](../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 11

- [ ] Departamento pessoal
- [ ] recursos humanos
- [ ] medicina e segurança do trabalho da empresa

### Suporte

Escopo: Seção 3.2. Especificação: [32](../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2

- [ ] Chamados dos clientes
- [ ] base de conhecimento
- [ ] SLA

### Segurança e operação

Escopo: [05](../docs/v2/05-seguranca.md), [07](../docs/v2/07-privacidade-lgpd.md), [10](../docs/v2/10-implantacao-operacao.md). Painel de bancos de dados: substitui o módulo Bancos (PAG-03, [34](../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 4)

- [ ] Acesso
- [ ] MFA
- [ ] auditoria
- [ ] privacidade (DPO)
- [ ] TI
- [ ] configurações do sistema
- [ ] integrações globais
- [ ] painel de bancos de dados

## 2.2 Portal de Gestão (`gestao.`) — equipe administrativa da entidade

### Acadêmico

Escopo: [17](../docs/v2/17-regras-modulos.md), seção 4; [55](../docs/v2/55-academico-verificacao-e-lacunas.md); [58](../docs/v2/58-calendario-e-eventos-por-portal.md) a [69](../docs/v2/69-relatorios-e-censo-por-portal.md); [40](../docs/v2/40-aulas-online-por-portal.md) a [44](../docs/v2/44-agendamento-ambientes-equipamentos.md). Itens explicitados em 04/11/2026 a partir da seção 7 e dos documentos por portal

- [ ] Administração escolar (estrutura acadêmica)
- [ ] pedagógico (coordenação e diário)
- [ ] calendário e eventos
- [ ] séries e turmas (grade de horários)
- [ ] regras de aprovação (sistemas avaliativos, boletim e conselho de classe)
- [ ] ocorrências disciplinares
- [ ] planos de aula e de ensino
- [ ] estágio e TCC
- [ ] prontuário e portfólio do aluno
- [ ] livros digitais e arquivo morto
- [ ] preceptoria
- [ ] gestão pastoral
- [ ] aulas online
- [ ] agendamento de ambientes e equipamentos
- [ ] formulários e pesquisas
- [ ] relatórios acadêmicos e censo

### Secretaria

Escopo: Sub-área do acadêmico. Ver seções 3.2 e 3.5; [46](../docs/v2/46-matricula-e-rematricula-por-portal.md), [48](../docs/v2/48-gerador-de-documentos-por-portal.md)

- [ ] Matrículas
- [ ] rematrículas
- [ ] transferências
- [ ] enturmação
- [ ] ficha cadastral
- [ ] protocolo de atendimento
- [ ] emissão de documentos
- [ ] processo seletivo e lista de espera

### Gestão de documentos

Escopo: [54](../docs/v2/54-gestao-de-documentos-tres-contextos.md). Ver também seções 3.1 e 3.4

- [ ] Documentos recebidos (validação)
- [ ] documentos administrativos (tramitação)
- [ ] documentos emitidos (modelos e emissão)
- [ ] serviços comuns (assinatura, protocolo e armazenamento)

### Simulados

Escopo: Ver seção 3.6. Especificação: [47](../docs/v2/47-simulados-por-portal.md)

- [ ] Banco de questões
- [ ] geração de provas
- [ ] correção
- [ ] gabarito
- [ ] ranking

### Biblioteca

Escopo: Ver seção 3.1. Especificação: [68](../docs/v2/68-biblioteca-por-portal.md)

- [ ] Acervo
- [ ] empréstimos
- [ ] reservas
- [ ] multas
- [ ] biblioteca digital

### Financeiro da entidade

Escopo: [17](../docs/v2/17-regras-modulos.md), [18](../docs/v2/18-regras-modulos-2.md), [20](../docs/v2/20-pagamentos-seguranca.md), [34](../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), [71](../docs/v2/71-financeiro-completo-por-portal.md)

- [ ] Mensalidades
- [ ] títulos
- [ ] cobrança
- [ ] régua
- [ ] conciliação
- [ ] centros de custo
- [ ] contas a pagar
- [ ] cheques
- [ ] caixa físico
- [ ] fluxo de caixa e DRE
- [ ] gateways e split

### Contábil e fiscal da entidade

Escopo: Ver seção 3.3. Especificação: [31](../docs/v2/31-matriz-portais-modulos.md), seção 3.3; [34](../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 5; [26](../docs/v2/26-sdd-juridico-regulatorio.md), seção 11

- [ ] Plano de contas da entidade
- [ ] tributos
- [ ] retenções
- [ ] obrigações
- [ ] NFSe

### Comercial e admissões

Escopo: [22](../docs/v2/22-crm-canais-e-papeis.md), seção 6.2

- [ ] CRM do tenant (captação, pré-cadastro, inscrição)

### Pessoas e RH

Escopo: [18](../docs/v2/18-regras-modulos-2.md), seção 3; [39](../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md); [52](../docs/v2/52-medicina-do-trabalho-especificacao.md)

- [ ] HCM
- [ ] folha
- [ ] ponto
- [ ] férias
- [ ] avaliação de desempenho
- [ ] SST

### Suprimentos e compras

Escopo: [19](../docs/v2/19-regras-modulos-3.md), seção 2

- [ ] Requisição
- [ ] cotação
- [ ] pedido
- [ ] almoxarifado
- [ ] merenda

### Patrimônio e frotas

Escopo: [19](../docs/v2/19-regras-modulos-3.md), seções 8 e 9

- [ ] Bens
- [ ] depreciação
- [ ] veículos
- [ ] manutenção
- [ ] rotas

### Contratos

Escopo: [17](../docs/v2/17-regras-modulos.md), seção 7; [33](../docs/v2/33-contratos-por-portal.md); [53](../docs/v2/53-pacote-documentos-e-contratos.md)

- [ ] Contratos de fornecedor
- [ ] contratos de aluno
- [ ] contratos de pessoal

### Atendimento

Escopo: Seção 3.7; [32](../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2

- [ ] SAC
- [ ] helpdesk
- [ ] chat
- [ ] tickets

### Arquivos

Escopo: [21](../docs/v2/21-busca-e-armazenamento.md)

- [ ] Armazenamento de arquivos

### Relatórios e gráficos

Escopo: Seção 3.8; [56](../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 3; [69](../docs/v2/69-relatorios-e-censo-por-portal.md)

- [ ] Painéis
- [ ] gráficos salvos

### Configuração e acesso

Escopo: [06](../docs/v2/06-identidade-acesso.md); [32](../docs/v2/32-atendimento-privacidade-por-portal.md), seção 3; [35](../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md); [36](../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 4; [56](../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 2; [57](../docs/v2/57-notificacoes-por-portal.md); [70](../docs/v2/70-importacao-de-dados-por-portal.md); [72](../docs/v2/72-campos-personalizados-por-portal.md); [74](../docs/v2/74-integracoes-educacionais-oficiais.md). Unidade só é criada por `platform.developer` (L-02); a gestão edita a unidade existente

- [ ] Unidades
- [ ] usuários
- [ ] vínculos
- [ ] privacidade da entidade
- [ ] configurações da entidade
- [ ] campos personalizados
- [ ] notificações
- [ ] integrações educacionais oficiais
- [ ] importação de dados
- [ ] acesso físico e portaria
- [ ] TI da entidade

### Planejamento acadêmico, institucional e de desenvolvimento

Escopo: [37](../docs/v2/37-planejamento-e-empenho.md), seções 2 a 4 (especificado em 03/11/2026, seção 3.9)

- [ ] Planejamento acadêmico
- [ ] planejamento institucional
- [ ] planejamento de desenvolvimento de pessoas

### Empenho

Escopo: [37](../docs/v2/37-planejamento-e-empenho.md), seção 5 (especificado em 03/11/2026, seção 3.9)

- [ ] Empenho
- [ ] liquidação e pagamento (só entidade pública)

## 2.3 Portal do Professor (`portal-do-professor.`)

### Classe

Escopo: Só turmas vinculadas. Especificação: [80](../docs/v2/80-decisoes-por-padrao.md), DP-06 (mural, materiais e tarefas)

- [ ] Turmas e disciplinas do próprio docente
- [ ] mural
- [ ] materiais
- [ ] tarefas

### Diário

Escopo: Só turmas vinculadas. Nota só pelo professor da turma ([22](../docs/v2/22-crm-canais-e-papeis.md), seção 5)

- [ ] Frequência
- [ ] conteúdo
- [ ] notas
- [ ] plano de aula

### Simulados

Escopo: Questão passa por revisão antes de publicar (seção 3.6) Especificação: [47](../docs/v2/47-simulados-por-portal.md), seção 7

- [ ] Elaboração de questões
- [ ] agendamento
- [ ] resultados da turma

### Biblioteca

Escopo: Somente leitura. Especificação: [68](../docs/v2/68-biblioteca-por-portal.md), seção 11

- [ ] Consulta de acervo
- [ ] indicação de leitura

### Protocolos e pedidos

Escopo: Usa o serviço de protocolo (seção 3.2) Especificação: [31](../docs/v2/31-matriz-portais-modulos.md), seção 3.2; [44](../docs/v2/44-agendamento-ambientes-equipamentos.md)

- [ ] Solicitação de material
- [ ] reserva de laboratório
- [ ] justificativa

### Documentos e pessoal

Escopo: Só dados do próprio docente. Especificação: [39](../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 6; [34](../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 8

- [ ] Declarações
- [ ] contrato de trabalho
- [ ] holerite
- [ ] ponto

### Relatórios

Escopo: Só turmas vinculadas. Especificação: [69](../docs/v2/69-relatorios-e-censo-por-portal.md), seção 6

- [ ] Rendimento da turma
- [ ] ficha individual

### Agenda e comunicação

Escopo: Só turmas vinculadas. [58](../docs/v2/58-calendario-e-eventos-por-portal.md), [60](../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), [40](../docs/v2/40-aulas-online-por-portal.md), [57](../docs/v2/57-notificacoes-por-portal.md), [76](../docs/v2/76-meu-perfil-por-portal.md) (explicitado em 04/11/2026)

- [ ] Horário e calendário das turmas
- [ ] aulas online
- [ ] notificações
- [ ] meu perfil

### Acompanhamento pedagógico

Escopo: Só turmas e orientandos vinculados. [63](../docs/v2/63-ocorrencias-disciplinares-por-portal.md), [65](../docs/v2/65-estagio-e-tcc-por-portal.md), [42](../docs/v2/42-preceptoria-por-portal.md), [66](../docs/v2/66-prontuario-e-portfolio-do-aluno-por-portal.md), [41](../docs/v2/41-formularios-e-pesquisas.md), [43](../docs/v2/43-pastoral-por-portal.md) (explicitado em 04/11/2026)

- [ ] Ocorrências da turma
- [ ] orientação de estágio e TCC
- [ ] preceptoria
- [ ] portfólio dos alunos
- [ ] formulários e pesquisas
- [ ] pastoral

## 2.4 Portal do Aluno (`portal-do-aluno.`)

### Classe e diário

Escopo: Só o próprio aluno. Especificação: [61](../docs/v2/61-diario-escolar-por-portal.md), seção 7; [62](../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md), seção 7; [80](../docs/v2/80-decisoes-por-padrao.md), DP-06

- [ ] Disciplinas
- [ ] materiais
- [ ] entregas
- [ ] boletim
- [ ] presença

### Simulados

Escopo: Só simulados do próprio aluno. Especificação: [47](../docs/v2/47-simulados-por-portal.md), seção 7

- [ ] Simulados agendados
- [ ] realização de prova
- [ ] gabarito e comentários

### Biblioteca

Escopo: Só os próprios empréstimos. Especificação: [68](../docs/v2/68-biblioteca-por-portal.md), seção 11

- [ ] Empréstimos
- [ ] prazos
- [ ] renovação
- [ ] pesquisa de acervo

### Protocolos online

Escopo: Usa o serviço de protocolo. Especificação: [31](../docs/v2/31-matriz-portais-modulos.md), seção 3.2

- [ ] Requerimento de segunda chamada
- [ ] declaração de matrícula

### Documentos

Escopo: Emissão pelo aluno conforme regra de [21](../docs/v2/21-busca-e-armazenamento.md) e seção 3.5

- [ ] Boletim oficial
- [ ] histórico
- [ ] declarações

### Matrícula

Escopo: Seção 3.5. Especificação: [46](../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 6

- [ ] Confirmação para o ano seguinte
- [ ] eletivas
- [ ] rematrícula

### Financeiro

Escopo: Só títulos do próprio aluno. Especificação: [34](../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 8; [20](../docs/v2/20-pagamentos-seguranca.md)

- [ ] Mensalidades
- [ ] boleto
- [ ] PIX
- [ ] comprovantes

### Privacidade

Escopo: [07](../docs/v2/07-privacidade-lgpd.md)

- [ ] Dados cadastrais
- [ ] solicitações LGPD

### Agenda e comunicação

Escopo: Só o próprio aluno. [58](../docs/v2/58-calendario-e-eventos-por-portal.md), [60](../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), [40](../docs/v2/40-aulas-online-por-portal.md), [57](../docs/v2/57-notificacoes-por-portal.md), [76](../docs/v2/76-meu-perfil-por-portal.md) (explicitado em 04/11/2026)

- [ ] Horário da turma
- [ ] calendário e eventos
- [ ] aulas online
- [ ] notificações
- [ ] meu perfil

### Vida acadêmica

Escopo: Só o próprio aluno. [63](../docs/v2/63-ocorrencias-disciplinares-por-portal.md), [65](../docs/v2/65-estagio-e-tcc-por-portal.md), [66](../docs/v2/66-prontuario-e-portfolio-do-aluno-por-portal.md), [42](../docs/v2/42-preceptoria-por-portal.md), [41](../docs/v2/41-formularios-e-pesquisas.md), [43](../docs/v2/43-pastoral-por-portal.md) (explicitado em 04/11/2026)

- [ ] Ocorrências próprias
- [ ] estágio e TCC
- [ ] portfólio
- [ ] preceptoria
- [ ] formulários e pesquisas
- [ ] pastoral

## 2.5 Portal dos Pais e Responsáveis (`portal-dos-responsaveis.`)

### Acompanhamento

Escopo: Só dependentes com vínculo ativo de responsabilidade. Especificação: [61](../docs/v2/61-diario-escolar-por-portal.md), [62](../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md), [63](../docs/v2/63-ocorrencias-disciplinares-por-portal.md), [35](../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md), seção 4, [57](../docs/v2/57-notificacoes-por-portal.md)

- [ ] Notas
- [ ] faltas
- [ ] ocorrências
- [ ] comunicados
- [ ] entradas e saídas da portaria

### Biblioteca e simulados

Escopo: Somente leitura. Especificação: [68](../docs/v2/68-biblioteca-por-portal.md), seção 11; [47](../docs/v2/47-simulados-por-portal.md), seção 7

- [ ] Empréstimos e desempenho dos filhos

### Protocolos da família

Escopo: Usa o serviço de protocolo. Especificação: [31](../docs/v2/31-matriz-portais-modulos.md), seção 3.2

- [ ] Mudança de turno
- [ ] saída antecipada
- [ ] documentos

### Financeiro e matrícula

Escopo: Seção 3.5. Bloqueio parcial por inadimplência ([26](../docs/v2/26-sdd-juridico-regulatorio.md), seção 3)

- [ ] Faturas dos filhos
- [ ] PIX
- [ ] rematrícula online
- [ ] assinatura do contrato

### Privacidade e menores

Escopo: Regra de menor de idade em [07](../docs/v2/07-privacidade-lgpd.md)

- [ ] Consentimento de imagem
- [ ] dados dos filhos

### Agenda e comunicação

Escopo: Só dependentes com vínculo ativo. [58](../docs/v2/58-calendario-e-eventos-por-portal.md), [60](../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), [43](../docs/v2/43-pastoral-por-portal.md), [57](../docs/v2/57-notificacoes-por-portal.md), [76](../docs/v2/76-meu-perfil-por-portal.md) (explicitado em 04/11/2026)

- [ ] Horário e calendário dos dependentes
- [ ] eventos e autorizações
- [ ] notificações
- [ ] meu perfil

## 2.6 Portal de Terceiros (`portal-de-terceiros.`)

### Faturamento de serviços

Escopo: Só o próprio fornecedor. Especificação: [38](../docs/v2/38-portal-de-terceiros-prestadores.md); [34](../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seções 5 e 8

- [ ] Emissão e envio de NF-e de serviço
- [ ] acompanhamento de pagamento
- [ ] extrato

### Pedidos e contratos

Escopo: Só o próprio fornecedor. Especificação: [38](../docs/v2/38-portal-de-terceiros-prestadores.md), seção 4; [33](../docs/v2/33-contratos-por-portal.md), seção 9

- [ ] Pedidos de compra pendentes
- [ ] contratos em vigor

### Documentos da empresa

Escopo: Só o próprio fornecedor. Validade com alerta. Especificação: [38](../docs/v2/38-portal-de-terceiros-prestadores.md), seção 5

- [ ] Certidões
- [ ] contrato social
- [ ] alvarás
- [ ] seguro

### Prestação de serviço

Escopo: Só ordens do próprio fornecedor. Especificação: [38](../docs/v2/38-portal-de-terceiros-prestadores.md), seção 3

- [ ] Ordens de serviço
- [ ] relatórios de execução
- [ ] cronograma

### Chamados

Escopo: Usa o módulo de atendimento (seção 3.7) Especificação: [32](../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.8; [35](../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md), seção 4

- [ ] Abertura de chamado de manutenção
- [ ] solicitação de acesso à unidade

### Configurações e integrações

Escopo: Dados bancários exigem confirmação por MFA. Especificação: [38](../docs/v2/38-portal-de-terceiros-prestadores.md), seção 6; [06](../docs/v2/06-identidade-acesso.md), seção 8

- [ ] Dados da empresa
- [ ] responsáveis técnicos
- [ ] dados bancários
- [ ] integrações via API

### Habilitação e acesso

Escopo: [38](../docs/v2/38-portal-de-terceiros-prestadores.md), seções 2 a 6; [76](../docs/v2/76-meu-perfil-por-portal.md) (explicitado em 04/11/2026)

- [ ] Cadastro e habilitação do prestador
- [ ] pessoas e papéis do prestador
- [ ] tipo de prestador
- [ ] meu perfil

