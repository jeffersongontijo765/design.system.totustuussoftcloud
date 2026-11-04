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
- Recurso principal: alunos com matrícula ativa, com limite por plano definido pelo desenvolvedor (L-01, SDD 77, seção 4). Demais recursos: **[Sem detalhamento]**.

## 6. Indicadores e gráficos
- Percentual de uso do limite de alunos; aviso ao atingir 90% (SDD 77, seção 4).

## 7. Ações e confirmações
- Ajustar limite: `platform.developer` (L-01). Ao exceder: bloqueio de novas matrículas ativas, sem alterar dados existentes (D-27, aprovada; SDD 77, seção 4).

## 8. Permissões e papéis
- Limite de alunos definido por `platform.developer`; leitura por `platform.manager` (SDD 78, §4.1).

## 9. Exportação e auditoria
- Alterações de limite auditadas (SDD 29).

## 10. Estados de interface
- Padrão de estados de tela (SDD 08).

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
Todo o módulo: regra de limite de alunos em SDD 77 (L-01 e D-27, aprovadas); demais recursos **[Sem detalhamento]**. Limites de taxa de API (SDD 04) são outro assunto.
