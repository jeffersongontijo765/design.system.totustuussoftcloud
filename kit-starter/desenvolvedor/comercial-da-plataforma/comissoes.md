# Comissões

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Comercial da plataforma
- Domínio: plataforma (banco master, D-16)
- Escopo: Metas e comissionamento da equipe comercial da plataforma
- Status: detalhado (v1, com regras da v2)

## 1. Identificação
- Especificações: SDD 22 (CRM em dois contextos), v1 `spec_crm_funil_comercial.md`, SDD 78 (permissões).
- Regra de fonte: onde a v1 e a v2 divergem, vale a v2 ([22](../../../docs/v2/22-crm-canais-e-papeis.md)). A v1 ([spec_crm_funil_comercial.md](../../../docs/v2/anexo-v1/spec_crm_funil_comercial.md)) vale onde a v2 não trata do assunto.

## 2. Objetivo e escopo
Definir metas por vendedor e acompanhar o realizado, calculando a comissão a pagar da equipe comercial da plataforma.

- **Separação dos CRMs (D-16):** nenhum lead de tenant aparece aqui, e nenhum lead da plataforma aparece em tenant. A ligação entre os dois é só o contrato comercial (SDD 22, seção 1).

## 3. Telas
- **Metas** (`/crm/goals`, datatable): vendedor, período (mês ou trimestre), meta, realizado, percentual.
- **Acompanhamento** (gráfico de progresso por vendedor, realizado contra meta) (v1, seção 10).
- **Regras de comissão** (configuração): percentual fixo, escalonado ou por plano (v1, seção 10).
- **Relatório de comissão a pagar** por período.

## 4. Dados
- `crm_goals` (v1, seção 14): responsável, período `AAAA-MM`, meta, realizado, regra de comissão (JSON), com `tenant_id` e `context`.
- Comissão a pagar vai para o Financeiro da plataforma e para o RH da plataforma (v1, seção 13), nunca para os módulos de uma entidade.

## 5. Campos e validações
- Meta: valor positivo; período no formato `AAAA-MM`.
- Realizado vem das oportunidades ganhas no período, não é digitado.

## 6. Indicadores e gráficos
- Realizado contra meta por vendedor; alerta quando a meta estiver em risco (abaixo de 70% aos 20 dias do período, v1 seção 12).

## 7. Ações e confirmações
- Criar e ajustar metas; configurar regra de comissão; fechar o período e gerar o relatório de comissão.

## 8. Permissões e papéis
Papéis do CRM da plataforma (SDD 22, seção 4.1; códigos em SDD 78, seção 4.1):

| Papel | Pode | Não pode |
|---|---|---|
| Pré-vendas (SDR) | Qualificar, agendar demonstração, registrar interação | Fechar proposta, alterar preço, ver contrato |
| Vendedor (AE) | Criar proposta, avançar o funil até negociação (só os próprios) | Aprovar desconto acima da alçada, alterar contrato assinado |
| Gerente comercial | Atribuir leads, aprovar desconto dentro da alçada, ver funil da equipe | Aprovar a própria proposta |
| Operador de chatbot | Atender, transferir e registrar conversas da fila | Acessar carteira fora da fila |
| Sucesso do cliente | Acompanhar implantação e uso dos clientes ativos | Alterar cobrança |
- Metas e regras de comissão: gerente comercial. Fechamento do período: separado de quem recebe a comissão (SDD 78, seção 2.2).

## 9. Exportação e auditoria
- Auditoria de alteração de meta e de regra de comissão, e do fechamento do período.

## 10. Estados de interface
- Carregando, vazio, sem resultado, erro, acesso negado. Lead `sem_consentimento` mostrado com aviso de que não recebe marketing.

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
- Regra de comissão padrão e periodicidade de pagamento: **[Sem detalhamento]**.
