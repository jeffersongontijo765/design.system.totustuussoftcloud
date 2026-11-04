# Clientes (tenants)

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Plataforma e clientes
- Domínio: plataforma (banco master)
- Escopo: Cadastro e ciclo de vida das entidades clientes da plataforma
- Status: detalhado

## 1. Identificação
- Especificações: `docs/v2/23-dominios-provisionamento-ciclo-de-vida.md` (§1, §4, §5); `docs/v2/03-dominio-tenancy.md`; `docs/v2/06-identidade-acesso.md`

## 2. Objetivo e escopo
Gerir as entidades clientes (instituições) do SaaS: cadastro, status, unidades, bancos de dados e saída. Entidade e unidade são o contexto de dados de cada cliente (D-20).

## 3. Telas
- **Lista de clientes** (datatable): nome, código, status, unidades, plano/licenciamento, data de provisionamento. Filtros por status. Ações em lote: não definidas. Exporta CSV, XLSX.
- **Detalhe do cliente** (página com abas): identificação, unidades, bancos (`tt_NNN`, registro em `tenant_databases`), domínios, histórico de provisionamento, pedidos de saída.
- **Nova entidade** (wizard de 8 etapas, ver `provisionamento-entidade-e-unidade.md`).
- **Saída de cliente** (fluxo de 7 etapas, SDD 23 seção 5): pedido com confirmação MFA recente, suspensão, exportação, retenção legal, encerramento, expurgo e certificado.
- **Painel de clientes** (KPI): clientes ativos, em provisionamento, suspensos, encerrados.

## 4. Dados
- Master (`totustuusdb`): entidade, unidade, código e domínio únicos (SDD 23 §4, etapa 1).
- Cada unidade aponta para o banco próprio (`tt_NNN`) registrado em `tenant_databases`. Dados da operação do cliente não ficam no master.
- Estados citados no SDD 23: `provisionando` (sem acesso de usuário, §4), `suspenso` (somente leitura, §5) e `encerrado` (§5). A lista completa de estados e transições é **[Sem detalhamento]**.

## 5. Campos e validações
- Código da entidade: único. Nome: obrigatório. Domínio: único; validado contra a lista de domínios ativos (SDD 23 §1, regra 5).
- Unidade: pertence a uma entidade; código único dentro da entidade.
- Campos completos de cadastro: **[Sem detalhamento]**.

## 6. Indicadores e gráficos
- Total por status; clientes com provisionamento pendente há mais de N dias: limiar **[Sem detalhamento]**.

## 7. Ações e confirmações
- Criar entidade (wizard), retomar provisionamento, cancelar provisionamento (remove o que foi criado, SDD 23 §4), suspender, iniciar saída.
- Destrutivo: encerrar e expurgar exigem digitar o nome da entidade (SDD 08 §3).

## 8. Permissões e papéis
- Papéis (SDD 78, §3 e §4.1): criar entidade e criar unidade só `platform.developer`; editar dados operacionais da entidade pelo `entity.admin` (nível 4); suspensão e encerramento por `platform.developer`.
- Passkey e sessão curta para papéis de plataforma (SDD 06, seção 10).

## 9. Exportação e auditoria
- Eventos: criação, mudança de status, suspensão, pedido e etapas de saída. Registro de auditoria em cada etapa (SDD 29).

## 10. Estados de interface
- Carregando, vazio ("nenhum cliente cadastrado"), sem resultado, erro, acesso negado, provisionando (bloqueio de acesso de usuário, SDD 23 §4).

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
- Campos completos de cadastro: **[Sem detalhamento]**.
- Limiar do painel de provisionamento pendente: **[Sem detalhamento]**.
