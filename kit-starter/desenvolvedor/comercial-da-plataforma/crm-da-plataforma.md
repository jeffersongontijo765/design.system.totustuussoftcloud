# CRM da plataforma

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Comercial da plataforma
- Domínio: plataforma (banco master, D-16)
- Escopo: Vendas do SaaS para instituições: funil, oportunidades, atividades, canais e configurações
- Status: detalhado (SDD 22 e v1)

## 1. Identificação
- Especificações: SDD 22 (CRM em dois contextos), v1 `spec_crm_funil_comercial.md`, SDD 78 (permissões).
- Regra de fonte: onde a v1 e a v2 divergem, vale a v2 ([22](../../../docs/v2/22-crm-canais-e-papeis.md)). A v1 ([spec_crm_funil_comercial.md](../../../docs/v2/anexo-v1/spec_crm_funil_comercial.md)) vale onde a v2 não trata do assunto.

## 2. Objetivo e escopo
Gerir a venda do SaaS para instituições, do primeiro contato até o contrato e a implantação. O lead é a instituição ou empresa que pode contratar o SaaS; o controlador dos dados é a plataforma (SDD 22, seção 1).

- **Separação dos CRMs (D-16):** nenhum lead de tenant aparece aqui, e nenhum lead da plataforma aparece em tenant. A ligação entre os dois é só o contrato comercial (SDD 22, seção 1).

## 3. Telas
- **Painel comercial** (`/crm/dashboard`, arquétipo dashboard): widgets e gráficos da seção 6.
- **Funil de oportunidades** (`/crm/pipeline`, kanban): colunas do funil da plataforma (seção 4). Card com instituição, valor estimado, responsável, próxima atividade, dias na etapa e prioridade (v1, seção 7). Arrastar entre colunas grava a transição.
- **Oportunidades** (`/crm/opportunities`, datatable) e **detalhe da oportunidade** (`/crm/opportunities/:uuid`, página com abas: dados, atividades, propostas, histórico).
- **Atividades** (`/crm/activities`, agenda por vendedor): ligação, e-mail, reunião, WhatsApp, tarefa; resultado (contato feito, não atendeu, reagendado) (v1, seção 8).
- **Conversas dos canais** (fila do chatbot): site, WhatsApp, Telegram, Instagram, Messenger, com handoff para vendedor (SDD 22, seção 2.1).
- **Relatórios** (`/crm/reports`): funil e conversão.
- **Configurações** (`/crm/settings`): funis, motivos de perda, regras de atribuição.
- Leads, propostas e metas: fichas próprias (`leads.md`, `propostas.md`, `comissoes.md`).

## 4. Dados
- Funil da plataforma (SDD 22, seção 6.1): `novo` → `contatado` → `qualificado` → `demonstracao` → `proposta` → `negociacao` → `ganho` ou `perdido`. Após ganho: `implantacao` → `ativo`. Descartes: `desqualificado`, `sem_consentimento`, `duplicado`.
- Tabelas: `crm_leads` e `crm_consents` (SDD 22, seção 8, com `context = 'plataforma'`); `crm_opportunities`, `crm_activities` (v1, seção 14), acrescidas de `tenant_id` e `context` conforme SDD 22, seção 8.
- Ganho gera handoff para **Contratos** (contrato do cliente) e para **provisionamento** da entidade ([provisionamento.md](../plataforma-e-clientes/provisionamento.md)). Nunca gera matrícula: matrícula é do CRM do tenant.

## 5. Campos e validações
- Perda: motivo obrigatório (preço, concorrência, sem orçamento, timing, outro), lista configurável (SDD 22, seção 6; v1, seção 7).
- Atividade: vínculo obrigatório a lead ou oportunidade (v1, seção 8).
- Lead descartado não volta ao funil: novo interesse gera novo lead vinculado ao anterior (regra da seção 6 do SDD 22, aplicada ao contexto da plataforma).

## 6. Indicadores e gráficos
- Widgets (v1, seção 5): leads no período, leads não atribuídos, oportunidades abertas, taxa de conversão (lead → ganho), ticket médio, receita em funil (forecast), atividades atrasadas, tempo médio do ciclo de venda.
- Gráficos (v1, seção 5): funil por etapa; linha de novos leads por semana ou mês; rosca de leads por canal de origem; barras de conversão por vendedor; barras dos motivos de perda.

## 7. Ações e confirmações
- Mover oportunidade de etapa; marcar ganho (dispara handoff); marcar perdido (exige motivo).
- Automações (v1, seção 12): atribuição automática (rodízio, território, disponibilidade); alerta de lead sem contato após o SLA de primeiro atendimento; perda automática após N dias sem atividade; alerta ao gerente quando a meta estiver em risco.
- Mensagens proativas respeitam opt-out (`PARAR`, `SAIR`) e limite por dia (SDD 22, seção 3).

## 8. Permissões e papéis
Papéis do CRM da plataforma (SDD 22, seção 4.1; códigos em SDD 78, seção 4.1):

| Papel | Pode | Não pode |
|---|---|---|
| Pré-vendas (SDR) | Qualificar, agendar demonstração, registrar interação | Fechar proposta, alterar preço, ver contrato |
| Vendedor (AE) | Criar proposta, avançar o funil até negociação (só os próprios) | Aprovar desconto acima da alçada, alterar contrato assinado |
| Gerente comercial | Atribuir leads, aprovar desconto dentro da alçada, ver funil da equipe | Aprovar a própria proposta |
| Operador de chatbot | Atender, transferir e registrar conversas da fila | Acessar carteira fora da fila |
| Sucesso do cliente | Acompanhar implantação e uso dos clientes ativos | Alterar cobrança |
- Separação de funções: quem cria a proposta não a aprova (SDD 78, seção 2.2).

## 9. Exportação e auditoria
- Auditoria (v1, seção 13): mudança de etapa, atribuição, perda e conversão. Exportação: CSV e XLSX, com permissão de exportação e step-up (SDD 15 e 78).

## 10. Estados de interface
- Carregando, vazio, sem resultado, erro, acesso negado. Lead `sem_consentimento` mostrado com aviso de que não recebe marketing.

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
- SLA de primeiro atendimento e N dias para perda automática: **[Sem detalhamento]**.
- Limite de mensagens proativas por canal (lacuna L-22 do SDD 22).
- Retenção de transcrição e gravação de ligação (lacuna L-24 do SDD 22).
- Códigos dos papéis comerciais: pendência D-41 no [78](../../../docs/v2/78-permissoes-e-papeis.md).
