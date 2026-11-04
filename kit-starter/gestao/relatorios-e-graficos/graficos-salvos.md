# Gráficos salvos

- Portal: Gestão (`gestao.`)
- Área: Relatórios e gráficos
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.8; [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 3
- Fonte da v1: [chart-builder-spec-complete.md](../../../docs/v2/anexo-v1/chart-builder-spec-complete.md) (1499 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Construtor de gráficos sobre fontes de dados autorizadas.

## 3. Telas

- **Gráficos** (lista).
- **Construtor** (fonte, métricas, dimensões, filtros, tipo).

## 4. Permissões por portal (extraídas do SDD)

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Teste de isolamento | Teste de permissão | Teste de fluxo principal | Teste de acessibilidade |
|---|---|---|---|---|
| Gestão | Cross-tenant e cross-unidade | Papel sem permissão não vê o módulo | Matrícula, cobrança, emissão de documento | Telas principais |

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Autenticação | Sessão | Dados e restrições especiais |
|---|---|---|---|
| Gestão | Senha e MFA conforme política da entidade ([06](../../../docs/v2/06-identidade-acesso.md), seção 5) | Padrão | Consulta por CPF com finalidade ([21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6.8) |

## 5. Papéis

- Conforme a fonte de dados.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.8.

## 7. Dados

- Tabelas e campos conforme a seção 13 e o DDL do [51](../../../docs/v2/51-ddl-modulos-novos.md), quando o módulo estiver lá. Toda tabela tem `entidade_id`, `unidade_id`, `created_at`, `updated_at`, `created_by` e exclusão lógica com `deleted_at` e `deleted_by` ([03](../../../docs/v2/03-dominio-tenancy.md), seção 6; [15](../../../docs/v2/15-validacoes.md); [19](../../../docs/v2/19-regras-modulos-3.md), seção 14).

## 8. Integrações

- Ver a seção de integrações do documento de origem, na seção 13.

## 9. Exportação, auditoria e privacidade

- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Toda criação, alteração, aprovação, exclusão lógica, exportação e leitura de dado sensível gera evento de auditoria no banco da unidade ([29](../../../docs/v2/29-auditoria.md)).
- Dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md): mínimo necessário, mascaramento em listas, base legal registrada.

## 10. Estados de interface

- Carregando (skeleton), vazio com chamada para ação, sem resultado de filtro, erro com nova tentativa, acesso negado, registro bloqueado, fechado ou baixado (somente leitura), conflito de edição (versão).

## 11. Requisitos de frontend

- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`): página de lista com DataTable, KPIs, drawer de detalhe, formulário em página ou modal, kanban quando houver fluxo de estados.
- Seletor de unidade no topo quando o usuário tiver mais de uma; a troca reemite o token com o novo contexto ([06](../../../docs/v2/06-identidade-acesso.md), seção 12).

## 12. Critérios de aceite e pendências

- Critérios de aceite: os do documento de origem (seção 13) e os de [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 6.
- Testes de isolamento: usuário de outra unidade ou entidade recebe 404 em toda rota do módulo ([03](../../../docs/v2/03-dominio-tenancy.md)).
- As pendências do documento de origem estão na seção 13 e consolidadas no [45](../../../docs/v2/45-pendencias-consolidadas.md).

## 13. Regras da v2 (texto integral das fontes, sem corte)

### 13.1 [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.8

##### 3.8 Gráficos e painéis

[`chart-builder-spec-complete.md`](../../../docs/v2/anexo-v1/chart-builder-spec-complete.md) (16 seções: consulta, renderização, painéis, API, segurança, exportação, tempo real) está marcado como "Especificado" no catálogo, mas a v2 não tem regra para ele.

**Proposta:**

- O construtor de gráfico é **componente compartilhado** ([08](../../../docs/v2/08-frontend-design-system.md)), não módulo de domínio.
- Cada gráfico salvo pertence a um portal e a um contexto (plataforma, entidade ou unidade). Nenhum gráfico mostra dado fora do escopo de quem o abriu.
- Consulta passa pela mesma camada de permissão das telas. A consulta não tem acesso direto ao banco.
- Gráfico de dado sensível (CPF, saúde, salário) não é exportável sem motivo e sem auditoria ([29](../../../docs/v2/29-auditoria.md)).
- Painel com dado pessoal entra no cache só com a regra de [30](../../../docs/v2/30-cache.md), seção 4.

### 13.2 [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 3

#### 3. Relatórios: regra geral que falta

Atualizado em 04/11/2026: a regra geral foi escrita no [69](../../../docs/v2/69-relatorios-e-censo-por-portal.md), seção 2 (tipos, ciclo, formatos e regras), com o catálogo por módulo na seção 3. O texto abaixo é a análise original.

Nenhum documento define como um relatório é gerado. Proposta, para ser validada:

1. **Relatório pertence ao módulo que tem o dado.** Não existe "relatório central". Cada módulo expõe os seus relatórios, com a mesma regra de acesso.
2. **Três tipos:** operacional (lista do dia), gerencial (totais e indicadores) e regulatório (formato exigido por órgão, como o censo e a ficha SEE).
3. **Permissão por escopo.** O relatório respeita o mesmo filtro de portal, unidade e turma que a tela. Relatório não é atalho para dado que a tela não mostra.
4. **Minimização.** Relatório com dado pessoal sai só com os campos necessários. Aniversariantes usa mês e dia, não a data completa de nascimento.
5. **Exportação é evento de auditoria** ([29](../../../docs/v2/29-auditoria.md)), com o campo `portal` e o filtro usado.
6. **Agregado com mínimo de grupo**, como em [41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 3, quando o relatório for sobre grupo pequeno.
7. **Senha e segredo nunca aparecem em relatório.** Exceção decidida pelo autor em 03/11/2026: a secretaria gera relatório com os dados de acesso do responsável (usuário e link de acesso). O relatório só pode ser enviado ao próprio responsável, nunca a aluno nem a terceiro, e segue a LGPD. **Decidido pelo autor em 03/11/2026:** a senha não aparece em texto. O relatório traz o usuário e um link de primeiro acesso, de uso único e com validade curta. O responsável cria a própria senha ao acessar.
8. **Foto em relatório** (carômetro) só com consentimento específico ([35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md), seção 6).

## 14. Conteúdo integral da v1 (absorvido)

### 📊 Chart Builder — Especificação Técnica Completa
#### TotusTuusSoftCloud — Módulo de Visualização de Dados

> **Versão:** 1.0.0  
> **Data:** 2026-07-04  
> **Autor:** Jefferson Augusto  
> **Stack:** PHP 8 / Node.js / MySQL-MariaDB / JavaScript  
> **Status:** Draft para Implementação
- Language Standard: Global English

---

#### 1. Visão Geral

##### 1.1 Objetivo

O **Chart Builder** é um módulo integrado ao TotusTuusSoftCloud que permite criar gráficos complexos e interativos a partir de qualquer tabela do banco de dados, incluindo JOINs entre múltiplas tabelas. O sistema unifica as melhores características do **Power BI** (drill-down, filtros cruzados, tooltips ricos, KPIs), **Google Analytics** (explorações customizadas, segmentos, coortes, geo maps), e das bibliotecas **Chart.js**, **ApexCharts**, **ECharts** e **amCharts 5** (renderização flexível, animações, tipos exóticos de gráfico).

##### 1.2 Princípios de Design

- **Data-Driven:** Toda configuração é serializada em JSON; gráficos são re-renderizados a partir de config, não de código imperativo [web:16][web:19]
- **Multi-Tenant First:** Isolamento obrigatório por `tenant_id` em todas as queries geradas [web:40]
- **Biblioteca-Agnóstica:** Abstração sobre 4 engines de renderização, trocáveis sem reescrever config
- **Segurança por Design:** Query builder com prepared statements, allowlist de tabelas/colunas, nenhum SQL raw do frontend [web:39][web:40]
- **Performance-First:** Cache de resultados, lazy loading, virtualização de datasets grandes, server-side aggregation
- **Extensível:** Plugin architecture para novos tipos de gráfico e fontes de dados externas

##### 1.3 Escopo Funcional

| Capacidade | Descrição |
|---|---|
| Tipos de gráfico | 40+ tipos cobrindo line, bar, column, area, pie, donut, scatter, bubble, radar, heatmap, treemap, sunburst, sankey, funnel, gauge, candlestick, waterfall, boxplot, polar, geo map, timeline, Gantt, wordcloud, chord, force-directed, etc. [web:2][web:37] |
| Fontes de dados | Qualquer tabela do schema do tenant; JOINs INNER/LEFT/RIGHT/FULL entre múltiplas tabelas [web:24] |
| Agregações | SUM, COUNT, AVG, MIN, MAX, COUNT DISTINCT, MEDIAN, STDDEV, PERCENTILE, custom expressions |
| Agrupamento | GROUP BY por 1-N dimensões; drill-down hierárquico |
| Filtros | Dinâmicos (range, lista, busca, data), cross-chart filtering (Power BI style) |
| Dashboards | Composição de múltiplos gráficos em dashboards com layout drag-and-drop |
| Exportação | PNG, JPG, SVG, PDF, CSV, JSON, XLSX [web:37] |
| Tempo real | Atualização via polling ou WebSocket/SSE para dados streaming [web:16][web:29] |
| Multi-idioma | i18n em títulos, legendas, tooltips, formatação numérica/date |

---

#### 2. Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Browser)                           │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐  │
│  │  Chart Builder│  │  Dashboard   │  │  Query Designer Visual    │  │
│  │  Config Editor│  │  Layout Mgr  │  │  (Table/Join/Filter UI)   │  │
│  └──────┬───────┘  └──────┬───────┘  └───────────┬───────────────┘  │
│         │                 │                      │                  │
│  ┌──────▼─────────────────▼──────────────────────▼───────────────┐  │
│  │              Chart Renderer Abstraction Layer                  │  │
│  │  ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌──────────────────┐   │  │
│  │  │ Chart.js│ │ApexCharts│ │ ECharts │ │  amCharts 5      │   │  │
│  │  │ Adapter  │ │ Adapter  │ │ Adapter │ │  Adapter         │   │  │
│  │  └─────────┘ └──────────┘ └─────────┘ └──────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │ REST/GraphQL                         │
└──────────────────────────────┼──────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│                     BACKEND (PHP 8 / Node.js)                        │
│                                                                      │
│  ┌──────────────┐  ┌──────────────────┐  ┌────────────────────────┐ │
│  │ Chart Config │  │  Query Builder    │  │  Data Aggregation      │ │
│  │ Service      │  │  Engine           │  │  Engine                │ │
│  │ (CRUD/Validate│ │  (SQL Generator)  │  │  (Post-DB transforms)  │ │
│  └──────┬───────┘  └────────┬─────────┘  └──────────┬─────────────┘ │
│         │                   │                       │               │
│  ┌──────▼───────────────────▼───────────────────────▼─────────────┐ │
│  │              Tenant Security & Query Guard                       │ │
│  │  (tenant_id injection, allowlist validation, param binding)     │ │
│  └──────────────────────────────┬──────────────────────────────────┘ │
│                                 │                                    │
│  ┌──────────────┐  ┌───────────▼──────────┐  ┌────────────────────┐ │
│  │ Cache Layer  │  │  MySQL / MariaDB      │  │  Audit Log Service │ │
│  │ (Redis/File) │  │  (Multi-tenant schema)│  │  (LGPD compliance)  │ │
│  └──────────────┘  └───────────────────────┘  └────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

---

#### 3. Camada de Dados — Query Builder Engine

##### 3.1 Visão Geral

O Query Builder é o coração do sistema. Ele recebe uma **configuração declarativa** (JSON) do frontend e gera SQL seguro com JOINs, filtros, agregações e agrupamentos — sempre injetando `tenant_id` automaticamente.

##### 3.2 Data Source Configuration Schema

```json
{
  "dataSource": {
    "type": "sql",
    "tenantId": "auto",
    "tables": [
      {
        "id": "t1",
        "name": "vendas",
        "alias": "v",
        "schema": "tenant_123"
      },
      {
        "id": "t2",
        "name": "produtos",
        "alias": "p",
        "schema": "tenant_123"
      },
      {
        "id": "t3",
        "name": "clientes",
        "alias": "c",
        "schema": "tenant_123"
      }
    ],
    "joins": [
      {
        "type": "INNER",
        "left": { "table": "t1", "column": "produto_id" },
        "right": { "table": "t2", "column": "id" }
      },
      {
        "type": "LEFT",
        "left": { "table": "t1", "column": "cliente_id" },
        "right": { "table": "t3", "column": "id" }
      }
    ],
    "dimensions": [
      {
        "id": "d1",
        "table": "t2",
        "column": "categoria",
        "alias": "categoria_produto",
        "dataType": "string"
      },
      {
        "id": "d2",
        "table": "t1",
        "column": "data_venda",
        "alias": "mes_venda",
        "dataType": "date",
        "transform": {
          "type": "dateTrunc",
          "interval": "month"
        }
      }
    ],
    "measures": [
      {
        "id": "m1",
        "table": "t1",
        "column": "valor_total",
        "alias": "receita_total",
        "aggregation": "SUM",
        "dataType": "decimal"
      },
      {
        "id": "m2",
        "table": "t1",
        "column": "id",
        "alias": "qtd_vendas",
        "aggregation": "COUNT",
        "dataType": "integer"
      },
      {
        "id": "m3",
        "expression": "SUM(t1.valor_total) / NULLIF(COUNT(DISTINCT t1.cliente_id), 0)",
        "alias": "ticket_medio",
        "aggregation": null,
        "dataType": "decimal",
        "isCustomExpression": true
      }
    ],
    "filters": [
      {
        "id": "f1",
        "table": "t1",
        "column": "data_venda",
        "operator": "between",
        "value": ["2026-01-01", "2026-12-31"],
        "dataType": "date"
      },
      {
        "id": "f2",
        "table": "t2",
        "column": "categoria",
        "operator": "in",
        "value": ["Eletrônicos", "Móveis"],
        "dataType": "string"
      }
    ],
    "having": [
      {
        "measure": "m1",
        "operator": ">",
        "value": 1000
      }
    ],
    "sortBy": [
      { "field": "d2", "direction": "ASC" },
      { "field": "m1", "direction": "DESC" }
    ],
    "limit": 1000,
    "offset": 0
  }
}
```

##### 3.3 SQL Generation (Pseudo-algoritmo)

```
FUNCTION generateQuery(config, tenantId):

  1. VALIDAR todas as tabelas contra allowlist de schema do tenant
  2. VALIDAR todas as colunas contra INFORMATION_SCHEMA do tenant
  3. INICIAR query com SELECT

  4. PARA cada measure:
       SE isCustomExpression:
         ADICIONAR expression (validada por parser SQL custom)
       SENÃO:
         ADICIONAR {aggregation}({table_alias}.{column}) AS {alias}

  5. PARA cada dimension:
       SE transform existe:
         ADICIONAR DATE_TRUNC('{interval}', {table_alias}.{column}) AS {alias}
       SENÃO:
         ADICIONAR {table_alias}.{column} AS {alias}

  6. ADICIONAR FROM {schema}.{first_table} AS {alias}

  7. PARA cada join:
     ADICIONAR {join_type} JOIN {schema}.{table} AS {alias}
     ON {left_table}.{left_col} = {right_table}.{right_col}

  8. ADICIONAR WHERE {tenant_table}.tenant_id = ? (prepared param)
  9. PARA cada filter:
     ADICIONAR AND {table_alias}.{column} {operator} ? (prepared param)

  10. SE dimensions existem:
      ADICIONAR GROUP BY {dim_columns}

  11. SE having existe:
      ADICIONAR HAVING {measure_expr} {operator} ? (prepared param)

  12. ADICIONAR ORDER BY {sort_fields}

  13. ADICIONAR LIMIT ? OFFSET ? (prepared params)

  14. RETORNAR { sql: string, params: array }
```

##### 3.4 Segurança do Query Builder

| Camada | Mecanismo | Descrição |
|---|---|---|
| **Allowlist de Tabelas** | Metadata Service | Antes de gerar SQL, valida que cada tabela existe no schema do tenant e está marcada como `chartable = true` na metadata |
| **Allowlist de Colunas** | INFORMATION_SCHEMA | Valida que cada coluna referenciada existe fisicamente na tabela |
| **Tenant Isolation** | Auto-injection | `tenant_id = ?` é sempre injetado na cláusula WHERE, nunca confiando no frontend [web:40] |
| **Prepared Statements** | PDO / mysqli | Todos os valores de filtro são bindings parametrizados, nunca concatenação de string [web:39] |
| **Expression Parser** | SQL Parser Library | Expressões customas passam por parser que bloqueia DDL, DML, subqueries não-autorizadas, funções perigosas |
| **Query Timeout** | SET STATEMENT_TIMEOUT | Limite de execução por query (ex: 30s) para prevenir queries pesadas |
| **Audit Log** | Log Service | Toda query gerada é logada com user_id, tenant_id, timestamp, SQL resultante, tempo de execução [web:40] |
| **Row Limit** | Hard Cap | Máximo de rows retornadas por query (configurável por tenant, default 50000) |

##### 3.5 Cache Strategy

```json
{
  "cache": {
    "enabled": true,
    "ttl": 300,
    "strategy": "query_hash",
    "invalidation": {
      "onDataChange": true,
      "onConfigChange": true,
      "onTenantSchemaChange": true
    },
    "layers": {
      "memory": { "maxEntries": 100, "ttl": 60 },
      "redis": { "maxEntries": 10000, "ttl": 300 },
      "disk": { "maxSizeMB": 500, "ttl": 3600 }
    }
  }
}
```

- **Query Hash:** Hash SHA-256 de (tenant_id + SQL + params) usado como chave de cache
- **Invalidação:** Triggers de banco (`data_change_events`) ou TTL expiração
- **Warm Cache:** Agendamento de pré-execução de queries populares em horários de baixa carga

---

#### 4. Engine de Renderização — Abstração Multi-Biblioteca

##### 4.1 Arquitetura de Adapters

Cada biblioteca é encapsulada em um **Adapter** que implementa uma interface comum:

```typescript
interface ChartAdapter {
  name: string;
  supportedTypes: ChartType[];
  render(container: HTMLElement, config: UnifiedChartConfig, data: QueryResult): ChartInstance;
  update(instance: ChartInstance, config: UnifiedChartConfig, data: QueryResult): void;
  destroy(instance: ChartInstance): void;
  exportChart(instance: ChartInstance, format: ExportFormat): Promise<Blob>;
  getCapabilities(): AdapterCapabilities;
}
```

##### 4.2 Unified Chart Configuration

```json
{
  "chart": {
    "id": "uuid",
    "title": "Receita por Categoria — 2026",
    "subtitle": "Comparativo mensal",
    "type": "bar",
    "library": "echarts",
    "description": "Gráfico de barras mostrando receita total por categoria de produto ao longo de 2026"
  },
  "rendering": {
    "theme": "dark",
    "palette": "corporate_blue",
    "width": "100%",
    "height": 400,
    "responsive": true,
    "animations": {
      "enabled": true,
      "duration": 750,
      "easing": "cubicOut"
    },
    "locale": "pt-BR"
  },
  "axes": {
    "xAxis": {
      "dimension": "d1",
      "label": "Categoria",
      "type": "category",
      "rotate": 0,
      "gridLines": true
    },
    "yAxis": {
      "measure": "m1",
      "label": "Receita (R$)",
      "type": "value",
      "format": {
        "type": "currency",
        "currency": "BRL",
        "decimals": 2
      }
    },
    "secondaryAxis": null
  },
  "series": [
    {
      "id": "s1",
      "name": "Receita",
      "measure": "m1",
      "dimension": "d1",
      "type": "bar",
      "color": null,
      "stack": null,
      "visible": true
    },
    {
      "id": "s2",
      "name": "Qtd Vendas",
      "measure": "m2",
      "dimension": "d1",
      "type": "line",
      "color": null,
      "yAxisIndex": 1,
      "visible": true
    }
  ],
  "interaction": {
    "tooltip": {
      "enabled": true,
      "shared": true,
      "trigger": "axis",
      "formatCallback": null
    },
    "legend": {
      "enabled": true,
      "position": "bottom",
      "orientation": "horizontal"
    },
    "zoom": {
      "enabled": true,
      "type": "scroll"
    },
    "drilldown": {
      "enabled": true,
      "levels": ["categoria", "subcategoria", "produto"]
    },
    "crossFilter": {
      "enabled": true,
      "targetCharts": ["chart_uuid_2", "chart_uuid_3"]
    },
    "brush": {
      "enabled": true,
      "type": "rect"
    },
    "export": {
      "enabled": true,
      "formats": ["png", "svg", "csv", "json"]
    },
    "dataLabel": {
      "enabled": false,
      "position": "top",
      "format": "currency"
    },
    "annotations": {
      "enabled": true,
      "items": [
        {
          "type": "line",
          "axis": "y",
          "value": 50000,
          "label": "Meta"
        }
      ]
    }
  },
  "dataSource": { "...": "ver seção 3.2" }
}
```

##### 4.3 Catálogo de Tipos de Gráfico

###### 4.3.1 Tipos Básicos (todas as bibliotecas)

| Tipo | Chart.js | ApexCharts | ECharts | amCharts 5 |
|---|---|---|---|---|
| Line | ✅ | ✅ | ✅ | ✅ |
| Bar (horizontal) | ✅ | ✅ | ✅ | ✅ |
| Column (vertical) | ✅ | ✅ | ✅ | ✅ |
| Area | ✅ | ✅ | ✅ | ✅ |
| Pie | ✅ | ✅ | ✅ | ✅ |
| Donut | ✅ | ✅ | ✅ | ✅ |
| Scatter | ✅ | ✅ | ✅ | ✅ |
| Bubble | ✅ | ✅ | ✅ | ✅ |
| Radar / Polar | ✅ | ✅ | ✅ | ✅ |
| Combo (bar+line) | ✅ | ✅ | ✅ | ✅ |

###### 4.3.2 Tipos Avançados (biblioteca específica)

| Tipo | Biblioteca Recomendada | Descrição |
|---|---|---|
| Heatmap | ECharts | Matriz de intensidade de valores |
| Treemap | ECharts / amCharts | Hierarquia em retângulos aninhados |
| Sunburst | ECharts / amCharts | Hierarquia radial |
| Sankey | ECharts / amCharts | Fluxo de dados entre nós |
| Funnel | ApexCharts / ECharts | Funil de conversão |
| Gauge | ApexCharts / ECharts | Medidor semi-circular |
| Candlestick / OHLC | ECharts / amCharts | Gráfico financeiro de velas |
| Waterfall | ECharts / amCharts | Barras cumulativas com deltas |
| Boxplot | ECharts | Distribuição estatística |
| Chord | ECharts | Relações circulares |
| Force-Directed Graph | ECharts / amCharts | Rede de nós e arestas |
| Geo Map (Choropleth) | ECharts / amCharts | Mapa geográfico com intensidade de cor [web:5] |
| Timeline | amCharts | Linha do tempo de eventos |
| Gantt | amCharts | Cronograma de projeto |
| Word Cloud | amCharts | Nuvem de palavras por frequência |
| Venn Diagram | amCharts | Relações de conjuntos |
| Stream Graph | ECharts | Áreas empilhadas em fluxo |
| Theme River | ECharts | Rio de temas temporais |
| Graph Network | ECharts | Grafo de relacionamentos |
| Pictorial Bar | ECharts | Barras com imagens/ícones |
| Calendar Heatmap | ECharts | Calendário com heatmap |
| Parallel Coordinates | ECharts | Múltiplas dimensões paralelas |
| Candlestick + Volume | ECharts / amCharts | Gráfico financeiro com volume [web:36] |

###### 4.3.3 Recursos Especiais (inspirados em Power BI / GA)

| Recurso | Origem | Descrição |
|---|---|---|
| Drill-down hierárquico | Power BI [web:3] | Navegação por níveis: ano → trimestre → mês → dia |
| Cross-chart filtering | Power BI [web:3] | Seleção em um gráfico filtra os demais do dashboard |
| KPI Cards | Power BI [web:13] | Cards com valor, variação, sparkline e meta |
| Matrix / Pivot Table | Power BI [web:13] | Tabela dinâmica com drill e subtotais |
| Forecasting | Power BI [web:13] | Projeção estatística com intervalo de confiança |
| Play Axis | Power BI [web:13] | Animação temporal para ver evolução de dados |
| Cohort Analysis | Google Analytics [web:5] | Análise de coortes por período de aquisição |
| Geo Map | GA / Power BI [web:5][web:2] | Mapa com intensidade de cor por região |
| Segments / Funnels | GA [web:12] | Filtros sequenciais de jornada |
| Sparklines | Power BI [web:2] | Mini-gráficos inline em tabelas |
| Data Bars | Power BI [web:2] | Barras inline em células de tabela |
| What-If Parameters | Power BI | Sliders que recalculam gráficos dinamicamente |

---

#### 5. Sistema de Dashboards

##### 5.1 Dashboard Configuration

```json
{
  "dashboard": {
    "id": "uuid",
    "name": "Dashboard de Vendas 2026",
    "description": "Visão executiva de vendas, produtos e clientes",
    "tenantId": "auto",
    "layout": {
      "type": "grid",
      "columns": 12,
      "rowHeight": 80,
      "gap": 12,
      "items": [
        {
          "chartId": "chart_uuid_1",
          "x": 0, "y": 0, "w": 6, "h": 5,
          "minW": 3, "minH": 3
        },
        {
          "chartId": "chart_uuid_2",
          "x": 6, "y": 0, "w": 6, "h": 5,
          "minW": 3, "minH": 3
        },
        {
          "chartId": "chart_uuid_3",
          "x": 0, "y": 5, "w": 12, "h": 6,
          "minW": 4, "minH": 4
        }
      ]
    },
    "filters": {
      "globalFilters": [
        {
          "id": "gf1",
          "type": "dateRange",
          "label": "Período",
          "target": {
            "charts": "all",
            "column": "data_venda"
          },
          "defaultValue": {
            "start": "2026-01-01",
            "end": "2026-12-31"
          }
        },
        {
          "id": "gf2",
          "type": "multiSelect",
          "label": "Categoria",
          "target": {
            "charts": ["chart_uuid_1", "chart_uuid_3"],
            "column": "categoria"
          },
          "options": {
            "source": "query",
            "query": "SELECT DISTINCT categoria FROM produtos WHERE tenant_id = ? ORDER BY categoria"
          }
        }
      ]
    },
    "interactions": {
      "crossFiltering": true,
      "crossFilterMode": "highlight"
    },
    "refresh": {
      "autoRefresh": false,
      "interval": 0
    },
    "permissions": {
      "owner": "user_uuid",
      "sharedWith": [],
      "publicReadOnly": false
    }
  }
}
```

##### 5.2 Dashboard Builder UI

- **Drag-and-drop grid** com redimensionamento (estilo Power BI / Grafana)
- **Painel lateral** com lista de gráficos criados para arrastar ao dashboard
- **Filtros globais** configuráveis que afetam múltiplos gráficos simultaneamente
- **Modo preview** para testar interações antes de publicar
- **Auto-refresh** configurável (intervalo em segundos, ou manual)
- **Responsive breakpoints:** desktop (12 col), tablet (8 col), mobile (4 col)

---

#### 6. API Design

##### 6.1 Endpoints REST

```
POST   /api/v1/chart-builder/charts                    # Criar config de gráfico
GET    /api/v1/chart-builder/charts                    # Listar gráficos do tenant
GET    /api/v1/chart-builder/charts/{id}               # Obter config de gráfico
PUT    /api/v1/chart-builder/charts/{id}               # Atualizar config
DELETE /api/v1/chart-builder/charts/{id}               # Deletar gráfico
POST   /api/v1/chart-builder/charts/{id}/clone         # Duplicar gráfico
POST   /api/v1/chart-builder/charts/{id}/data           # Executar query e retornar dados
POST   /api/v1/chart-builder/charts/{id}/render          # Retornar config + dados prontos p/ render
POST   /api/v1/chart-builder/charts/{id}/export         # Exportar (png/svg/pdf/csv/xlsx)
POST   /api/v1/chart-builder/charts/{id}/preview        # Preview com config temporária (sem salvar)

POST   /api/v1/chart-builder/dashboards                # Criar dashboard
GET    /api/v1/chart-builder/dashboards                # Listar dashboards
GET    /api/v1/chart-builder/dashboards/{id}            # Obter dashboard completo
PUT    /api/v1/chart-builder/dashboards/{id}            # Atualizar dashboard
DELETE /api/v1/chart-builder/dashboards/{id}            # Deletar dashboard
POST   /api/v1/chart-builder/dashboards/{id}/share      # Compartilhar (link público/token)

GET    /api/v1/chart-builder/metadata/tables            # Listar tabelas disponíveis (chartable)
GET    /api/v1/chart-builder/metadata/tables/{name}/columns  # Listar colunas + tipos
GET    /api/v1/chart-builder/metadata/relationships       # Listar FKs para sugerir JOINs
GET    /api/v1/chart-builder/metadata/data-types           # Mapeamento de tipos SQL → tipos de gráfico

POST   /api/v1/chart-builder/query/validate              # Validar config de query sem executar
POST   /api/v1/chart-builder/query/explain               # EXPLAIN da query gerada
POST   /api/v1/chart-builder/query/preview                # Executar com LIMIT 10

GET    /api/v1/chart-builder/themes                      # Listar temas/paletas
POST   /api/v1/chart-builder/themes                       # Criar tema customizado
GET    /api/v1/chart-builder/templates                    # Templates de gráficos prontos

POST   /api/v1/chart-builder/realtime/subscribe           # SSE/WS subscription p/ updates
```

##### 6.2 Response Pattern

```json
{
  "success": true,
  "data": { },
  "meta": {
    "requestId": "uuid",
    "tenantId": "tenant_123",
    "executionTime": 245,
    "fromCache": true,
    "rowCount": 1245
  },
  "error": null
}
```

##### 6.3 Query Execution Response

```json
{
  "success": true,
  "data": {
    "columns": [
      { "name": "categoria_produto", "type": "string", "label": "Categoria" },
      { "name": "mes_venda", "type": "date", "label": "Mês" },
      { "name": "receita_total", "type": "decimal", "label": "Receita Total" },
      { "name": "qtd_vendas", "type": "integer", "label": "Qtd Vendas" }
    ],
    "rows": [
      { "categoria_produto": "Eletrônicos", "mes_venda": "2026-01-01", "receita_total": 45000.00, "qtd_vendas": 120 },
      { "categoria_produto": "Eletrônicos", "mes_venda": "2026-02-01", "receita_total": 52000.00, "qtd_vendas": 145 }
    ],
    "totals": {
      "receita_total": 97000.00,
      "qtd_vendas": 265
    },
    "chartConfig": { "...": "config unificada pronta para render" }
  },
  "meta": {
    "requestId": "uuid",
    "executionTime": 189,
    "fromCache": false,
    "rowCount": 2,
    "sqlExecuted": "SELECT p.categoria AS categoria_produto, ...",
    "queryPlan": "rows_estimated: 1200, index_used: idx_tenant_data"
  }
}
```

---

#### 7. Backend — PHP 8 Service Layer

##### 7.1 Estrutura de Classes

```
src/
├── ChartBuilder/
│   ├── Controller/
│   │   ├── ChartController.php
│   │   ├── DashboardController.php
│   │   ├── MetadataController.php
│   │   └── QueryController.php
│   ├── Service/
│   │   ├── ChartConfigService.php       # CRUD + validação de config
│   │   ├── QueryBuilderService.php      # Geração de SQL a partir de config
│   │   ├── QueryExecutorService.php     # Execução com prepared statements
│   │   ├── DataAggregationService.php   # Transformações pós-query
│   │   ├── CacheService.php             # Cache multi-camada
│   │   ├── ExportService.php            # PNG/SVG/PDF/CSV/XLSX
│   │   ├── ThemeService.php             # Gestão de temas/paletas
│   │   ├── MetadataService.php          # Introspecção de schema
│   │   ├── AuditLogService.php          # Logging de queries e ações
│   │   └── RealtimeService.php         # SSE/WebSocket push
│   ├── Security/
│   │   ├── TenantGuard.php              # Injeção de tenant_id
│   │   ├── TableAllowlist.php           # Validação de tabelas
│   │   ├── ColumnAllowlist.php          # Validação de colunas
│   │   ├── ExpressionParser.php         # Parser/validator de expressões SQL
│   │   └── QuerySanitizer.php           # Sanitização final
│   ├── Validator/
│   │   ├── ChartConfigValidator.php     # JSON Schema validation
│   │   ├── DataSourceValidator.php     # Validação de data source config
│   │   └── DashboardConfigValidator.php
│   ├── Repository/
│   │   ├── ChartRepository.php          # Persistência de configs
│   │   ├── DashboardRepository.php
│   │   └── ThemeRepository.php
│   └── DTO/
│       ├── ChartConfigDTO.php
│       ├── DataSourceDTO.php
│       ├── QueryResultDTO.php
│       └── DashboardConfigDTO.php
```

##### 7.2 QueryBuilderService — Exemplo PHP

```php
<?php
declare(strict_types=1);

namespace ChartBuilder\Service;

use ChartBuilder\Security\TenantGuard;
use ChartBuilder\Security\TableAllowlist;
use ChartBuilder\Security\ColumnAllowlist;
use ChartBuilder\Security\ExpressionParser;

class QueryBuilderService
{
    public function __construct(
        private TenantGuard $tenantGuard,
        private TableAllowlist $tableAllowlist,
        private ColumnAllowlist $columnAllowlist,
        private ExpressionParser $expressionParser
    ) {}

    public function buildQuery(array $dataSourceConfig, string $tenantId): array
    {
        $this->validateTables($dataSourceConfig['tables'], $tenantId);
        $this->validateColumns($dataSourceConfig, $tenantId);

        $sql = $this->buildSelectClause($dataSourceConfig);
        $sql .= $this->buildFromClause($dataSourceConfig['tables']);
        $sql .= $this->buildJoinClauses($dataSourceConfig['joins'] ?? []);
        $sql .= $this->buildWhereClause($dataSourceConfig['filters'] ?? [], $tenantId);
        $sql .= $this->buildGroupByClause($dataSourceConfig['dimensions'] ?? []);
        $sql .= $this->buildHavingClause($dataSourceConfig['having'] ?? []);
        $sql .= $this->buildOrderByClause($dataSourceConfig['sortBy'] ?? []);
        $sql .= $this->buildLimitClause(
            $dataSourceConfig['limit'] ?? 1000,
            $dataSourceConfig['offset'] ?? 0
        );

        $params = $this->extractParams($dataSourceConfig, $tenantId);

        return ['sql' => $sql, 'params' => $params];
    }

    private function buildWhereClause(array $filters, string $tenantId): string
    {
        $conditions = ["{$this->tenantTable}.tenant_id = ?"];
        $this->params[] = $tenantId;

        foreach ($filters as $filter) {
            $column = "{$filter['tableAlias']}.{$filter['column']}";
            $conditions[] = $this->buildFilterCondition($column, $filter);
        }

        return ' WHERE ' . implode(' AND ', $conditions);
    }

    private function buildFilterCondition(string $column, array $filter): string
    {
        return match ($filter['operator']) {
            'eq' => "{$column} = ?",
            'neq' => "{$column} != ?",
            'gt' => "{$column} > ?",
            'gte' => "{$column} >= ?",
            'lt' => "{$column} < ?",
            'lte' => "{$column} <= ?",
            'like' => "{$column} LIKE ?",
            'in' => "{$column} IN (" . implode(',', array_fill(0, count($filter['value']), '?')) . ")",
            'not_in' => "{$column} NOT IN (" . implode(',', array_fill(0, count($filter['value']), '?')) . ")",
            'between' => "{$column} BETWEEN ? AND ?",
            'is_null' => "{$column} IS NULL",
            'is_not_null' => "{$column} IS NOT NULL",
            default => throw new \InvalidArgumentException("Unknown operator: {$filter['operator']}")
        };
    }
}
```

##### 7.3 ExpressionParser — Validação de Expressões Custom SQL

```php
<?php
declare(strict_types=1);

namespace ChartBuilder\Security;

class ExpressionParser
{
    private const BLOCKED_KEYWORDS = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE',
        'GRANT', 'REVOKE', 'EXEC', 'EXECUTE', 'INTO OUTFILE', 'INTO DUMPFILE',
        'LOAD_FILE', 'SLEEP', 'BENCHMARK', 'INFORMATION_SCHEMA'
    ];

    private const ALLOWED_FUNCTIONS = [
        'SUM', 'COUNT', 'AVG', 'MIN', 'MAX', 'MEDIAN', 'STDDEV',
        'VARIANCE', 'PERCENTILE_CONT', 'PERCENTILE_DISC',
        'DATE_TRUNC', 'DATE_FORMAT', 'YEAR', 'MONTH', 'DAY', 'WEEK',
        'QUARTER', 'HOUR', 'MINUTE', 'SECOND',
        'COALESCE', 'NULLIF', 'IFNULL', 'GREATEST', 'LEAST',
        'ROUND', 'CEIL', 'FLOOR', 'ABS', 'POWER', 'SQRT',
        'CONCAT', 'SUBSTRING', 'UPPER', 'LOWER', 'TRIM',
        'CAST', 'CONVERT'
    ];

    public function validate(string $expression): bool
    {
        $upper = strtoupper($expression);

        foreach (self::BLOCKED_KEYWORDS as $keyword) {
            if (str_contains($upper, $keyword)) {
                throw new \SecurityException(
                    "Blocked keyword '{$keyword}' found in expression"
                );
            }
        }

        $tokens = $this->tokenize($expression);
        $this->validateFunctionCalls($tokens);

        return true;
    }

    private function validateFunctionCalls(array $tokens): void
    {
        foreach ($tokens as $token) {
            if ($token['type'] === 'function' && !in_array($token['value'], self::ALLOWED_FUNCTIONS)) {
                throw new \SecurityException(
                    "Function '{$token['value']}' is not allowed in custom expressions"
                );
            }
        }
    }
}
```

---

#### 8. Frontend — Arquitetura JavaScript

##### 8.1 Estrutura de Módulos

```
assets/js/chart-builder/
├── core/
│   ├── ChartBuilder.js              # Orquestrador principal
│   ├── ConfigManager.js             # Gerencia estado da config (JSON)
│   ├── EventManager.js              # Pub/sub para interações
│   └── StateStore.js                # Estado global (filters, selections)
├── adapters/
│   ├── ChartJsAdapter.js
│   ├── ApexChartsAdapter.js
│   ├── EChartsAdapter.js
│   └── AmChartsAdapter.js
├── components/
│   ├── QueryDesigner/
│   │   ├── TableSelector.js         # Seleção de tabelas
│   │   ├── JoinBuilder.js           # Construtor visual de JOINs
│   │   ├── DimensionPicker.js       # Seleção de dimensões
│   │   ├── MeasurePicker.js         # Seleção de medidas + agregação
│   │   └── FilterBuilder.js         # Construtor de filtros
│   ├── ChartConfigurator/
│   │   ├── ChartTypeSelector.js     # Grid de tipos de gráfico
│   │   ├── LibrarySelector.js       # Troca de biblioteca
│   │   ├── AxesConfigurator.js      # Configuração de eixos
│   │   ├── SeriesConfigurator.js    # Configuração de séries
│   │   ├── StyleCustomizer.js      # Cores, fontes, temas
│   │   └── InteractionConfigurator.js  # Tooltip, zoom, drilldown
│   ├── DashboardBuilder/
│   │   ├── DashboardGrid.js         # Grid drag-and-drop
│   │   ├── DashboardItem.js         # Wrapper de gráfico no grid
│   │   ├── GlobalFilterBar.js       # Barra de filtros globais
│   │   └── DashboardPreview.js      # Modo preview
│   └── Common/
│       ├── DataPreviewTable.js      # Preview dos dados retornados
│       ├── ExportMenu.js            # Menu de exportação
│       └── ThemePicker.js           # Seletor de temas
├── services/
│   ├── ApiClient.js                 # Wrapper de chamadas REST
│   ├── MetadataService.js           # Cache de metadata do schema
│   └── RealtimeClient.js            # SSE/WebSocket client
└── utils/
    ├── ColorPalette.js              # Geração de paletas
    ├── DataFormatter.js             # Formatação de números/datas/moedas
    └── ChartTypeMapper.js           # Mapeia tipo de dado → tipo de gráfico sugerido
```

##### 8.2 ECharts Adapter — Exemplo

```javascript
class EChartsAdapter {
  constructor() {
    this.name = 'echarts';
    this.supportedTypes = [
      'line', 'bar', 'column', 'area', 'pie', 'donut',
      'scatter', 'bubble', 'radar', 'heatmap', 'treemap',
      'sunburst', 'sankey', 'funnel', 'gauge', 'candlestick',
      'waterfall', 'boxplot', 'chord', 'graph', 'parallel',
      'themeRiver', 'pictorialBar', 'calendar'
    ];
  }

  render(container, config, data) {
    const option = this.translateConfig(config, data);
    const chart = echarts.init(container, config.rendering.theme);
    chart.setOption(option);

    if (config.interaction.zoom?.enabled) {
      chart.setOption({ dataZoom: [{ type: config.interaction.zoom.type }] });
    }

    if (config.interaction.drilldown?.enabled) {
      chart.on('click', (params) => {
        this.handleDrilldown(config, params);
      });
    }

    return chart;
  }

  update(instance, config, data) {
    const option = this.translateConfig(config, data);
    instance.setOption(option, { notMerge: false });
  }

  translateConfig(config, data) {
    return {
      title: {
        text: config.chart.title,
        subtext: config.chart.subtitle
      },
      tooltip: {
        trigger: config.interaction.tooltip.trigger,
        shared: config.interaction.tooltip.shared,
        formatter: this.buildTooltipFormatter(config)
      },
      legend: {
        show: config.interaction.legend.enabled,
        bottom: config.interaction.legend.position === 'bottom' ? 0 : null
      },
      xAxis: this.translateXAxis(config.axes.xAxis, data),
      yAxis: this.translateYAxis(config.axes.yAxis, data),
      series: config.series.map(s => this.translateSeries(s, data))
    };
  }

  translateSeries(series, data) {
    const typeMap = {
      'bar': 'bar',
      'column': 'bar',
      'line': 'line',
      'area': 'line',
      'pie': 'pie',
      'scatter': 'scatter'
    };

    return {
      name: series.name,
      type: typeMap[series.type] || series.type,
      data: this.extractSeriesData(series, data),
      areaStyle: series.type === 'area' ? {} : null,
      yAxisIndex: series.yAxisIndex || 0
    };
  }

  extractSeriesData(series, data) {
    return data.rows.map(row => {
      const dimValue = row[series.dimension];
      const measureValue = row[series.measure];
      return [dimValue, measureValue];
    });
  }

  async exportChart(instance, format) {
    const url = instance.getDataURL({
      type: format === 'jpg' ? 'jpg' : 'png',
      pixelRatio: 2,
      backgroundColor: '#fff'
    });
    return await (await fetch(url)).blob();
  }

  destroy(instance) {
    instance.dispose();
  }

  getCapabilities() {
    return {
      drilldown: true,
      brush: true,
      dataZoom: true,
      export: ['png', 'jpg', 'svg', 'csv'],
      realtime: true,
      animation: true
    };
  }
}
```

---

#### 9. Sistema de Metadados (Schema Introspection)

##### 9.1 MetadataService

Responsável por introspectar o schema do tenant e fornecer dados para o Query Designer visual:

```php
<?php
// Retorna tabelas marcadas como disponíveis para charts
public function getChartableTables(string $tenantSchema): array
{
    // 1. Lista tabelas físicas do schema do tenant
    // 2. Filtra por allowlist configurada (tabelas sensíveis excluídas)
    // 3. Adiciona metadata: label, description, row_count_estimate
    // 4. Identifica colunas: name, type, label, is_nullable, is_foreign_key
    // 5. Identifica relacionamentos (FKs) para sugerir JOINs automáticos
}
```

##### 9.2 Metadata Response Example

```json
{
  "tables": [
    {
      "name": "vendas",
      "label": "Vendas",
      "description": "Registro de todas as vendas realizadas",
      "chartable": true,
      "rowEstimate": 45000,
      "columns": [
        {
          "name": "id",
          "type": "bigint",
          "label": "ID",
          "nullable": false,
          "isPrimaryKey": true
        },
        {
          "name": "data_venda",
          "type": "datetime",
          "label": "Data da Venda",
          "nullable": false,
          "suggestedChartTypes": ["line", "area", "column"],
          "suggestedAggregation": "dateTrunc"
        },
        {
          "name": "valor_total",
          "type": "decimal(12,2)",
          "label": "Valor Total",
          "nullable": false,
          "suggestedChartTypes": ["bar", "line", "area"],
          "suggestedAggregation": "SUM"
        },
        {
          "name": "produto_id",
          "type": "bigint",
          "label": "Produto",
          "nullable": false,
          "isForeignKey": true,
          "references": { "table": "produtos", "column": "id" }
        }
      ],
      "relationships": [
        {
          "targetTable": "produtos",
          "joinType": "INNER",
          "localColumn": "produto_id",
          "foreignColumn": "id",
          "autoSuggest": true
        },
        {
          "targetTable": "clientes",
          "joinType": "LEFT",
          "localColumn": "cliente_id",
          "foreignColumn": "id",
          "autoSuggest": true
        }
      ]
    }
  ]
}
```

##### 9.3 Smart Chart Type Suggestion

O sistema sugere automaticamente tipos de gráfico baseado no tipo de dado:

| Tipo de Coluna (SQL) | Tipo de Gráfico Sugerido |
|---|---|
| DATE / DATETIME / TIMESTAMP | Line, Area, Column (timeline) |
| INT / BIGINT (medida) | Bar, Column, Pie |
| DECIMAL / FLOAT (medida) | Bar, Line, Area |
| VARCHAR / TEXT (dimensão) | Pie, Donut, Bar |
| BOOLEAN | Pie, Donut |
| FK (foreign key) | Bar (COUNT por categoria) |
| Múltiplas dimensões temporais | Heatmap (calendar), Stacked Area |
| 2 medidas + 1 dimensão | Scatter, Bubble |
| Dados geográficos (CEP, estado) | Geo Map (choropleth) [web:5] |

---

#### 10. Segurança e Compliance

##### 10.1 Multi-Tenant Isolation

| Estratégia | Implementação |
|---|---|
| **Schema-level** | Cada tenant tem schema próprio: `tenant_{id}` [web:40] |
| **Tenant Guard** | `tenant_id = ?` injetado em TODA query gerada, sem exceção [web:40] |
| **Allowlist** | Tabelas e colunas validadas contra metadata antes de gerar SQL |
| **RBAC** | Roles: `chart_viewer`, `chart_editor`, `chart_admin`, `dashboard_admin` [web:40] |
| **Audit Log** | Toda execução de query logada: user, tenant, SQL, params, timestamp, duração, rowCount [web:40] |

##### 10.2 SQL Injection Prevention

| Camada | Mecanismo |
|---|---|
| **Zero Raw SQL** | Frontend nunca envia SQL; envia apenas config JSON declarativa [web:39] |
| **Prepared Statements** | PDO com bindings parametrizados para TODOS os valores [web:39] |
| **Allowlist Validation** | Tabelas/colunas validadas contra INFORMATION_SCHEMA antes de inserir na query [web:40] |
| **Expression Sandbox** | Expressões customas validadas por parser (allowlist de funções, blocklist de keywords) |
| **Query Timeout** | `MAX_EXECUTION_TIME` ou `SET SESSION max_execution_time` |
| **Result Cap** | Hard limit de rows por query (configurável por tenant) |

##### 10.3 LGPD Compliance

| Requisito | Implementação |
|---|---|
| **Minimização de dados** | Colunas PII podem ser marcadas como `excluded_from_charts` na metadata |
| **Anonimização** | Opção de aplicar funções de hash/mascaramento em colunas sensíveis |
| **Audit Trail** | Log completo de quem acessou quais dados via charts, quando e como [web:40] |
| **Direito ao esquecimento** | Charts não persistem dados brutos, apenas configs; dados vem do DB em tempo real |
| **Consentimento** | Charts com dados PII podem exigir flag de consentimento no tenant |

---

#### 11. Performance e Escalabilidade

##### 11.1 Estratégias

| Estratégia | Descrição |
|---|---|
| **Server-side aggregation** | Agregação (GROUP BY, SUM, etc.) feita no MySQL, não no frontend |
| **Cache multi-camada** | Memory → Redis → Disk, com TTL e invalidação por eventos [web:16] |
| **Lazy loading** | Gráficos do dashboard carregam sob demanda (viewport visibility) |
| **Query optimization** | EXPLAIN automático; sugestão de índices; alertas de slow query |
| **Data sampling** | Para datasets muito grandes, opção de sampling estatístico |
| **Pagination** | Server-side pagination para tabelas de dados no preview |
| **Debounced filters** | Filtros no UI debounce de 300ms antes de re-executar query |
| **WebSocket push** | Para real-time, apenas delta de dados é enviado, não re-fetch completo [web:16] |
| **Bundle splitting** | Adapters carregados dinamicamente (lazy import) conforme biblioteca selecionada |

##### 11.2 Índices Recomendados

```sql
-- Índice composto para tenant + data (pattern mais comum)
CREATE INDEX idx_{table}_tenant_date ON {table} (tenant_id, data_venda);

-- Índice para tenant + FK (para JOINs)
CREATE INDEX idx_{table}_tenant_fk ON {table} (tenant_id, produto_id);

-- Índice para tenant + dimensão comum
CREATE INDEX idx_{table}_tenant_categoria ON {table} (tenant_id, categoria);
```

---

#### 12. Theming e Customização

##### 12.1 Theme System

```json
{
  "theme": {
    "id": "corporate_dark",
    "name": "Corporate Dark",
    "colors": {
      "background": "#1a1a2e",
      "surface": "#16213e",
      "primary": "#0f3460",
      "accent": "#e94560",
      "text": "#eaeaea",
      "textSecondary": "#a0a0a0",
      "grid": "#2a2a4a",
      "palette": ["#e94560", "#0f3460", "#16c79a", "#f4a261", "#e76f51", "#533483"]
    },
    "typography": {
      "fontFamily": "Inter, sans-serif",
      "fontSize": 12,
      "titleFontSize": 16,
      "fontWeight": 600
    },
    "chartDefaults": {
      "backgroundColor": "transparent",
      "animation": { "duration": 750, "easing": "cubicOut" },
      "borderRadius": 6
    }
  }
}
```

##### 12.2 Paletas Predefinidas

| Nome | Cores | Uso |
|---|---|---|
| Corporate Blue | Azuis e cinzas | Relatórios executivos |
| Vibrant | Cores saturadas diversas | Dashboards de vendas |
| Pastel | Tons suaves | Apresentações educacionais |
| Monochrome | Escalas de cinza | Impressão / acessibilidade |
| Traffic Light | Verde/Amarelo/Vermelho | KPIs e status |
| Heat | Azul → Vermelho | Heatmaps e geo maps |
| Colorblind Safe | Paleta Okabe-Ito | Acessibilidade |

---

#### 13. Exportação e Compartilhamento

##### 13.1 Formatos de Exportação

| Formato | Conteúdo | Biblioteca/Engine |
|---|---|---|
| PNG | Imagem raster do gráfico | Nativo de cada library (getDataURL) |
| JPG | Imagem comprimida | Nativo de cada library |
| SVG | Imagem vetorial escalável | ECharts / amCharts (native SVG export) |
| PDF | Documento com gráfico + metadados | jsPDF + canvas |
| CSV | Dados brutos da query | Backend (PHP) |
| JSON | Config + dados completos | Backend (PHP) |
| XLSX | Planilha com dados + gráfico embutido | PhpSpreadsheet |

##### 13.2 Compartilhamento de Dashboards

- **Link público com token:** Dashboard renderizado em modo read-only via URL com token único
- **Embed iframe:** Widget embedável para portais externos
- **Export dashboard completo:** ZIP com HTML standalone (CSS + JS + dados inline)
- **Agendamento:** Envio de dashboard via e-mail em formato PDF/HTML (cron job)

---

#### 14. Real-Time Updates

##### 14.1 Arquitetura

```
┌──────────────┐         ┌──────────────────┐         ┌──────────────┐
│  MySQL/Maria │───TRIGGER──▶│  Event Bus       │───SSE───▶│  Browser     │
│  (data write)│         │  (Redis Pub/Sub) │         │  (Chart      │
└──────────────┘         └──────────────────┘         │  update)     │
                                                          └──────────────┘
```

##### 14.2 Configuração

```json
{
  "realtime": {
    "enabled": true,
    "transport": "sse",
    "refreshStrategy": "delta",
    "interval": 5000,
    "maxConnections": 50,
    "throttle": {
      "minInterval": 2000,
      "maxBatchSize": 10
    }
  }
}
```

- **Delta strategy:** Apenas dados novos/alterados são enviados ao frontend [web:16]
- **setOption merge:** ECharts faz merge inteligente da nova config com a existente, animando apenas as mudanças [web:19]
- **Throttle:** Evita flood de updates; agrupa mudanças em batches

---

#### 15. Banco de Dados — Schema de Persistência

##### 15.1 Tabelas do Chart Builder

```sql
-- Configs de gráficos
CREATE TABLE cb_charts (
    id              VARCHAR(36) PRIMARY KEY,
    tenant_id       VARCHAR(36) NOT NULL,
    name            VARCHAR(255) NOT NULL,
    description    TEXT,
    chart_type      VARCHAR(50) NOT NULL,
    library         VARCHAR(20) DEFAULT 'echarts',
    config_json     LONGTEXT NOT NULL,
    datasource_json LONGTEXT NOT NULL,
    thumbnail       TEXT,
    is_template     BOOLEAN DEFAULT FALSE,
    created_by      VARCHAR(36) NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at      DATETIME DEFAULT NULL,
    INDEX idx_tenant (tenant_id),
    INDEX idx_tenant_type (tenant_id, chart_type)
);

-- Dashboards
CREATE TABLE cb_dashboards (
    id            VARCHAR(36) PRIMARY KEY,
    tenant_id     VARCHAR(36) NOT NULL,
    name          VARCHAR(255) NOT NULL,
    description   TEXT,
    layout_json   LONGTEXT NOT NULL,
    filters_json  LONGTEXT,
    is_published  BOOLEAN DEFAULT FALSE,
    share_token   VARCHAR(64) UNIQUE,
    created_by    VARCHAR(36) NOT NULL,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at    DATETIME DEFAULT NULL,
    INDEX idx_tenant (tenant_id),
    INDEX idx_share_token (share_token)
);

-- Templates de gráficos
CREATE TABLE cb_chart_templates (
    id           VARCHAR(36) PRIMARY KEY,
    name         VARCHAR(255) NOT NULL,
    category     VARCHAR(50),
    chart_type   VARCHAR(50) NOT NULL,
    library      VARCHAR(20),
    config_json  LONGTEXT NOT NULL,
    icon         VARCHAR(255),
    is_system    BOOLEAN DEFAULT FALSE,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Temas/paletas
CREATE TABLE cb_themes (
    id          VARCHAR(36) PRIMARY KEY,
    tenant_id   VARCHAR(36),
    name        VARCHAR(100) NOT NULL,
    config_json LONGTEXT NOT NULL,
    is_system   BOOLEAN DEFAULT FALSE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tenant (tenant_id)
);

-- Metadata: tabelas disponíveis para charts
CREATE TABLE cb_table_metadata (
    id              VARCHAR(36) PRIMARY KEY,
    tenant_id       VARCHAR(36) NOT NULL,
    table_name      VARCHAR(100) NOT NULL,
    label           VARCHAR(100),
    description     TEXT,
    chartable       BOOLEAN DEFAULT TRUE,
    config_json     LONGTEXT,
    UNIQUE KEY uk_tenant_table (tenant_id, table_name)
);

-- Audit log
CREATE TABLE cb_audit_log (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    tenant_id   VARCHAR(36) NOT NULL,
    user_id     VARCHAR(36) NOT NULL,
    action      VARCHAR(50) NOT NULL,
    entity_type VARCHAR(30) NOT NULL,
    entity_id   VARCHAR(36),
    sql_executed TEXT,
    params_json TEXT,
    execution_ms INT,
    row_count   INT,
    ip_address  VARCHAR(45),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tenant_date (tenant_id, created_at),
    INDEX idx_user (user_id)
);

-- Cache de query results
CREATE TABLE cb_query_cache (
    cache_key   VARCHAR(64) PRIMARY KEY,
    tenant_id   VARCHAR(36) NOT NULL,
    result_json LONGTEXT,
    expires_at  DATETIME NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tenant_expires (tenant_id, expires_at)
);
```

---

#### 16. Roadmap de Implementação

##### Fase 1 — Fundação (Semanas 1-3)

- [ ] Schema de banco (cb_charts, cb_dashboards, cb_audit_log, etc.)
- [ ] MetadataService (introspecção de schema do tenant)
- [ ] QueryBuilderService (geração de SQL com JOINs, filtros, agregações)
- [ ] Security layer (TenantGuard, TableAllowlist, ColumnAllowlist)
- [ ] API REST básica (CRUD de charts + execução de query)
- [ ] ECharts Adapter (primeiro adapter, tipos básicos: line, bar, pie, area)

##### Fase 2 — Builder UI (Semanas 4-6)

- [ ] Query Designer visual (seleção de tabelas, JOINs, dimensões, medidas, filtros)
- [ ] Chart Configurator UI (tipo de gráfico, eixos, séries, estilo)
- [ ] Data Preview Table
- [ ] Theme system (temas predefinidos + custom)
- [ ] Export (PNG, CSV, JSON)

##### Fase 3 — Dashboards (Semanas 7-9)

- [ ] Dashboard Builder (grid drag-and-drop)
- [ ] Global filters
- [ ] Cross-chart filtering (Power BI style)
- [ ] Dashboard sharing (link com token)
- [ ] Dashboard export (PDF, standalone HTML)

##### Fase 4 — Bibliotecas Adicionais (Semanas 10-12)

- [ ] ApexCharts Adapter (gauge, funnel, patterns) [web:25][web:28]
- [ ] Chart.js Adapter (tipos básicos, leveza)
- [ ] amCharts 5 Adapter (geo maps, Gantt, timeline, stock charts) [web:37]
- [ ] Auto-seleção de biblioteca baseada no tipo de gráfico

##### Fase 5 — Avançado (Semanas 13-16)

- [ ] Drill-down hierárquico
- [ ] Real-time updates (SSE/WebSocket) [web:16]
- [ ] Forecasting (regressão linear, médias móveis)
- [ ] KPI Cards e Matrix/Pivot table
- [ ] Templates de gráficos prontos
- [ ] Cache multi-camada (Redis)
- [ ] Audit log completo com dashboard de monitoramento

---

#### 17. Bibliotecas e Dependências

##### 17.1 Frontend

| Biblioteca | Versão | Propósito |
|---|---|---|
| echarts | ^5.5 | Engine principal (mais tipos de gráfico) [web:23] |
| apexcharts | ^4.0 | Gauges, funnels, patterns [web:25] |
| chart.js | ^4.4 | Gráficos leves e rápidos |
| @amcharts/amcharts5 | ^5.9 | Geo maps, Gantt, timeline, stock [web:37] |
| gridstack.js | ^10.0 | Dashboard drag-and-drop grid |
| showdown.js | ^2.1 | Markdown rendering em descrições |

##### 17.2 Backend (PHP)

| Biblioteca | Propósito |
|---|---|
| PHP PDO | Prepared statements e query execution |
| phpoffice/phpspreadsheet | Export XLSX |
| predis/predis | Cache Redis |
| ramsey/uuid | UUID generation |
| vlucas/phpdotenv | Environment config |

---

#### 18. Considerações Finais

Este Chart Builder foi projetado para ser **a ferramenta definitiva de visualização** dentro do TotusTuusSoftCloud, combinando:

- **Flexibilidade do Power BI:** drill-down, cross-filtering, KPIs, dashboards interativos [web:3][web:13]
- **Exploração do Google Analytics:** free-form explorations, segmentos, coortes, geo maps [web:1][web:5][web:12]
- **Poder das 4 bibliotecas:** cobertura de 40+ tipos de gráfico com abstração unificada [web:23][web:25][web:37]
- **Segurança enterprise:** multi-tenant isolation, SQL injection prevention, audit trail LGPD-compliant [web:39][web:40]
- **Multi-tabela nativa:** JOINs visuais entre qualquer combinação de tabelas do schema [web:24]

A arquitetura adapter-based permite que novas bibliotecas sejam adicionadas no futuro sem reescrever configs existentes, e o query builder declarativo garante que usuários nunca precisem escrever SQL — apenas selecionar tabelas, arrastar colunas e configurar visualmente.

---

*Fim da Especificação — v1.0.0*
