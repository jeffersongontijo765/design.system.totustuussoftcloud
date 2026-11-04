# Inventário de telas por portal

Gerado por `inventario/gera_inventario.py` a partir de `docs/v2/31-matriz-portais-modulos.md`, seção 2.
Nível: portal → área → módulo. As telas de cada módulo são detalhadas antes de implementar.
Total de módulos listados: 190. Status inicial: nenhum implementado.


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

Escopo: D-23. Chamado de "builder de portais" na v1. **Não é o editor de modelos do Gerador de documentos** (ver seção 3.4)

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

Escopo: **Decidido** em 03/11/2026: mantido para a gestão da própria empresa desenvolvedora

- [ ] Contas a pagar e a receber **da própria empresa**

### Contábil da plataforma

Escopo: Mesma decisão do financeiro. Tributos da empresa: seção 3.3, confirmado pelo autor em 04/11/2026

- [ ] Plano de contas
- [ ] razão
- [ ] fechamento da empresa
- [ ] tributos e obrigações fiscais da empresa

### Operações internas

Escopo: **Decidido** em 03/11/2026: mantidos, como instâncias separadas dos módulos das entidades

- [ ] Patrimônio
- [ ] frotas
- [ ] suprimentos da empresa

### Pessoas da plataforma

Escopo: Mesma decisão. O HCM das entidades não é o da plataforma. Três módulos separados, conforme HCM-01 e HCM-10 do [39](../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 11

- [ ] Departamento pessoal
- [ ] recursos humanos
- [ ] medicina e segurança do trabalho da empresa

### Suporte

Escopo: Seção 3.2

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

Escopo: [17](../docs/v2/17-regras-modulos.md)

- [ ] Administração escolar
- [ ] pedagógico
- [ ] calendário
- [ ] séries e turmas
- [ ] regras de aprovação
- [ ] relatórios acadêmicos

### Secretaria

Escopo: Sub-área do acadêmico. Ver seções 3.2 e 3.5

- [ ] Matrículas
- [ ] rematrículas
- [ ] transferências
- [ ] enturmação
- [ ] ficha cadastral
- [ ] protocolo de atendimento
- [ ] emissão de documentos

### Gestão de documentos

Escopo: [54](../docs/v2/54-gestao-de-documentos-tres-contextos.md). Ver também seções 3.1 e 3.4

- [ ] Três contextos: documentos recebidos (validação)
- [ ] documentos administrativos (tramitação) e documentos emitidos (modelos e emissão). Serviços comuns de assinatura
- [ ] protocolo e armazenamento

### Simulados

Escopo: Ver seção 3.6

- [ ] Banco de questões
- [ ] geração de provas
- [ ] correção
- [ ] gabarito
- [ ] ranking

### Biblioteca

Escopo: Ver seção 3.1

- [ ] Acervo
- [ ] empréstimos
- [ ] reservas
- [ ] multas
- [ ] biblioteca digital

### Financeiro da entidade

Escopo: [17](../docs/v2/17-regras-modulos.md), [18](../docs/v2/18-regras-modulos-2.md), [20](../docs/v2/20-pagamentos-seguranca.md)

- [ ] Mensalidades
- [ ] títulos
- [ ] cobrança
- [ ] régua
- [ ] conciliação
- [ ] centros de custo

### Contábil e fiscal da entidade

Escopo: Ver seção 3.3

- [ ] Plano de contas da entidade
- [ ] tributos
- [ ] retenções
- [ ] obrigações
- [ ] NFSe

### Comercial e admissões

Escopo: [22](../docs/v2/22-crm-canais-e-papeis.md), seção 6.2

- [ ] CRM do tenant (captação
- [ ] pré-cadastro
- [ ] inscrição)

### Pessoas e RH

Escopo: [18](../docs/v2/18-regras-modulos-2.md), seção 3

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

Escopo: [17](../docs/v2/17-regras-modulos.md)

- [ ] Contratos de fornecedor
- [ ] de aluno e de pessoal

### Atendimento

Escopo: Seção 3.7

- [ ] SAC
- [ ] helpdesk
- [ ] chat
- [ ] tickets

### Arquivos

Escopo: [21](../docs/v2/21-busca-e-armazenamento.md)

- [ ] Armazenamento de arquivos

### Relatórios e gráficos

Escopo: Seção 3.8

- [ ] Painéis
- [ ] gráficos salvos

### Configuração e acesso

Escopo: [06](../docs/v2/06-identidade-acesso.md)

- [ ] Unidades
- [ ] usuários
- [ ] vínculos
- [ ] privacidade da entidade

### Planejamento acadêmico, institucional e de desenvolvimento

Escopo: Ver seção 3.9

- [ ] **[Sem especificação]**

### Empenho

Escopo: Ver seção 3.9

- [ ] **[Sem especificação]**

## 2.3 Portal do Professor (`portal-do-professor.`)

### Classe

Escopo: Só turmas vinculadas

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

Escopo: Questão passa por revisão antes de publicar (seção 3.6)

- [ ] Elaboração de questões
- [ ] agendamento
- [ ] resultados da turma

### Biblioteca

Escopo: Somente leitura

- [ ] Consulta de acervo
- [ ] indicação de leitura

### Protocolos e pedidos

Escopo: Usa o serviço de protocolo (seção 3.2)

- [ ] Solicitação de material
- [ ] reserva de laboratório
- [ ] justificativa

### Documentos e pessoal

Escopo: Só dados do próprio docente

- [ ] Declarações
- [ ] contrato de trabalho
- [ ] holerite
- [ ] ponto

### Relatórios

Escopo: Só turmas vinculadas

- [ ] Rendimento da turma
- [ ] ficha individual

## 2.4 Portal do Aluno (`portal-do-aluno.`)

### Classe e diário

Escopo: Só o próprio aluno

- [ ] Disciplinas
- [ ] materiais
- [ ] entregas
- [ ] boletim
- [ ] presença

### Simulados

Escopo: Só simulados do próprio aluno

- [ ] Simulados agendados
- [ ] realização de prova
- [ ] gabarito e comentários

### Biblioteca

Escopo: Só os próprios empréstimos

- [ ] Empréstimos
- [ ] prazos
- [ ] renovação
- [ ] pesquisa de acervo

### Protocolos online

Escopo: Usa o serviço de protocolo

- [ ] Requerimento de segunda chamada
- [ ] declaração de matrícula

### Documentos

Escopo: Emissão pelo aluno conforme regra de [21](../docs/v2/21-busca-e-armazenamento.md) e seção 3.5

- [ ] Boletim oficial
- [ ] histórico
- [ ] declarações

### Matrícula

Escopo: Seção 3.5

- [ ] Confirmação para o ano seguinte
- [ ] eletivas
- [ ] rematrícula

### Financeiro

Escopo: Só títulos do próprio aluno

- [ ] Mensalidades
- [ ] boleto
- [ ] PIX
- [ ] comprovantes

### Privacidade

Escopo: [07](../docs/v2/07-privacidade-lgpd.md)

- [ ] Dados cadastrais
- [ ] solicitações LGPD

## 2.5 Portal dos Pais e Responsáveis (`portal-dos-responsaveis.`)

### Acompanhamento

Escopo: Só dependentes com vínculo ativo de responsabilidade

- [ ] Notas
- [ ] faltas
- [ ] ocorrências
- [ ] comunicados
- [ ] entradas e saídas da portaria

### Biblioteca e simulados

Escopo: Somente leitura

- [ ] Empréstimos e desempenho dos filhos

### Protocolos da família

Escopo: Usa o serviço de protocolo

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

## 2.6 Portal de Terceiros (`portal-de-terceiros.`)

### Faturamento de serviços

Escopo: Só o próprio fornecedor

- [ ] Emissão e envio de NF-e de serviço
- [ ] acompanhamento de pagamento
- [ ] extrato

### Pedidos e contratos

Escopo: Só o próprio fornecedor

- [ ] Pedidos de compra pendentes
- [ ] contratos em vigor

### Documentos da empresa

Escopo: Só o próprio fornecedor. Validade com alerta

- [ ] Certidões
- [ ] contrato social
- [ ] alvarás
- [ ] seguro

### Prestação de serviço

Escopo: Só ordens do próprio fornecedor

- [ ] Ordens de serviço
- [ ] relatórios de execução
- [ ] cronograma

### Chamados

Escopo: Usa o módulo de atendimento (seção 3.7)

- [ ] Abertura de chamado de manutenção
- [ ] solicitação de acesso à unidade

### Configurações e integrações

Escopo: Dados bancários exigem confirmação por MFA

- [ ] Dados da empresa
- [ ] responsáveis técnicos
- [ ] dados bancários
- [ ] integrações via API

