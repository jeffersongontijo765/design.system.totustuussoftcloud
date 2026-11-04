# Limites e consumo

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Plataforma e clientes
- Domínio: plataforma (banco master)
- Escopo: Medição e limites de uso por entidade (usuários, unidades, armazenamento, chamadas de IA)
- Status: detalhado

## 1. Identificação
- Especificações: `docs/v2/14-integracao-modulos.md` (princípio 4); `docs/v2/04-api.md` (limite de taxa, outro assunto)

## 2. Objetivo e escopo
Acompanhar o consumo de cada entidade e aplicar os limites contratados.

## 3. Telas
- **Consumo por entidade** (datatable): recurso, consumido, limite, percentual.
- **Painel de consumo** (KPI e gráfico de série temporal).

## 4. Dados
- Eventos de consumo carregam `tenant_id` e `entity_id` (SDD 14, princípio 4).
- Quais recursos são medidos e como: **[Sem detalhamento]**.

## 5. Campos e validações
- Recursos e unidades de medida: **[Sem detalhamento]**.

## 6. Indicadores e gráficos
- Percentual de uso por recurso; entidades acima de 80%: limiar **[Sem detalhamento]**.

## 7. Ações e confirmações
- Ajustar limite, bloquear ao exceder: **[Sem detalhamento]** da regra.

## 8. Permissões e papéis
- Papel de plataforma: **[Sem detalhamento]**.

## 9. Exportação e auditoria
- Alterações de limite auditadas (SDD 29).

## 10. Estados de interface
- Padrão de estados de tela (SDD 08).

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
Todo o módulo: recursos, limites e comportamento ao exceder **[Sem detalhamento]**. Limites de taxa de API (SDD 04) são outro assunto.
