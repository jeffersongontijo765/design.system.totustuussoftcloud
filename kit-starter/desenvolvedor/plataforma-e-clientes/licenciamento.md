# Licenciamento

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Plataforma e clientes
- Domínio: plataforma (banco master)
- Escopo: Módulos e recursos contratados por cliente (habilitação de módulos por entidade)
- Status: detalhado

## 1. Identificação
- Especificações: `docs/v2/23` (§1, mapa de portais); `docs/v2/33-contratos-por-portal.md` (relação com contrato)

## 2. Objetivo e escopo
Definir quais módulos e recursos cada entidade pode usar. Serve de base para a exibição dos módulos no portal (SDD 23 §1: cada portal mostra os módulos permitidos pelo vínculo).

## 3. Telas
- **Licenças por entidade** (datatable): módulo, status, data de início e fim, limite contratado.
- **Catálogo de módulos licenciáveis** (datatable).
- Sem telas adicionais detalhadas.

## 4. Dados
- Relação entre entidade, licença e módulo. Modelo exato: **[Sem detalhamento]**.
- Relação com contrato comercial (SDD 33): **[Sem detalhamento]** do vínculo.

## 5. Campos e validações
- Campos da licença: **[Sem detalhamento]**.

## 6. Indicadores e gráficos
- Quantidade de licenças ativas por módulo: **[Sem detalhamento]**.

## 7. Ações e confirmações
- Ativar e desativar módulo para a entidade: regra de efeito na navegação **[Sem detalhamento]**.

## 8. Permissões e papéis
- Papel de plataforma: **[Sem detalhamento]**.

## 9. Exportação e auditoria
- Mudanças de licença auditadas (SDD 29): **[Sem detalhamento]** do evento.

## 10. Estados de interface
- Padrão de estados de tela (SDD 08).

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
Todo o módulo: sem especificação própria na v1 ou na v2. Definir antes de implementar.
