# Páginas de referência

Três páginas-modelo que provam o design system em uso. Cada uma usa um
**arquétipo** e uma **variante** diferente — elas não são o mesmo documento com
dados trocados.

| Página | Arquétipo | Variante | O que demonstra |
|---|---|---|---|
| [index.html](index.html) | `catalog` | `gallery` | galeria, comparação antes/depois |
| [dashboard-operacional.html](dashboard-operacional.html) | `dashboard` | `ops-monitor` | KPIs, gráfico sem biblioteca, alertas, tabela curta |
| [registros-tabela.html](registros-tabela.html) | `records` | `dense-table` | busca, filtro, tabela densa com rolagem própria, paginação |
| [detalhe-registro.html](detalhe-registro.html) | `detail` | `split-pane` | mestre/detalhe que colapsa, meta, progresso, histórico |

## Como usar

1. **Abra `index.html` no navegador** (não precisa de servidor).
2. Reduza a janela para 360 px: a toolbar empilha, as colunas de baixa
   prioridade somem e o `ttsc-split` colapsa em uma coluna.
3. Alterne o tema pelo botão de meio-círculo no cabeçalho das três telas.
4. Valide qualquer alteração: `node ../../scripts/ds-check.mjs .`

## O que copiar

Copie a **composição** (ordem dos blocos, uso de `ttsc-grid` / `ttsc-split` /
`ttsc-toolbar`), não o HTML inteiro. Se a tela nova for igual a uma destas,
mude a variante ou a densidade — repetir a mesma composição é o defeito que
estas páginas existem para impedir.

## Contrato de cada página

| Elemento | Regra |
|---|---|
| `<!-- page-spec {...} -->` | `archetype`, `variant`, `density`, `intent` — validado por R6 |
| CSS | só `components/ttsc.css` + `./assets/referencia.css` |
| JS | `type="module"`, externo, ≤ 8 KB (R18/R19) |
| Dados | escritos no HTML; nenhuma página lê `models/*.json` (R16) |
| Estados | vazio, carregando e erro presentes no DOM (`hidden`) |
| Ícones | SVG inline (sprite no topo do `<body>`) — a fonte Font Awesome Pro não é versionada |
