# START HERE — montar uma tela com o design system

Tempo de leitura: 3 minutos. Se você é um agente, este é o caminho obrigatório.

## 1. Identifique o arquétipo

Toda tela é **uma** destas sete coisas. Escolher errado é a causa nº 1 de tela
genérica.

| Arquétipo | Quando é | Variantes permitidas |
|---|---|---|
| `dashboard` | Responder "como está?" com números e tendência | `dense-kpi`, `executive-strip`, `ops-monitor` |
| `records` | Listar/gerenciar muitos registros iguais | `dense-table`, `card-grid`, `master-list` |
| `detail` | Aprofundar **um** registro | `split-pane`, `stacked-tabs`, `document-view` |
| `settings` | Configurar preferências e políticas | `sectioned-form`, `wizard` |
| `calendar` | Tempo, agenda, alocação | `month-grid`, `agenda-list` |
| `auth` | Entrar, recuperar acesso, aceitar convite | `centered-card`, `split-hero` |
| `catalog` | Documentação/galeria de páginas (não é tela de produto) | `gallery` |

> `catalog` existe para páginas de documentação e é isenta da regra de estados
> (R14). Nunca use `catalog` para uma tela de produto.

Uma tela de "boletim" é `detail` se mostra um aluno; é `records` se lista a turma
inteira. Não misture os dois na mesma página.

## 2. Declare a page-spec

O primeiro elemento do `<body>` (ou comentário antes de `<main>`) declara intenção.
Isso alimenta o validador e impede repetição.

```html
<!-- page-spec {"id":"aluno-boletim","archetype":"detail","variant":"split-pane","density":"comfortable","intent":"consultar notas e situação do aluno no bimestre","components":["ttsc-page-header","ttsc-card","ttsc-table","ttsc-badge"]} -->
```

## 3. Consulte o catálogo por necessidade

```bash
# o que existe para "tabela"?
node -e "const c=require('./docs/ai/catalog.json');for(const x of c.components.filter(x=>/tabela|table/i.test(x.purpose+' '+x.title)))console.log(x.id,'—',x.purpose)"
```

Escolha pelo `purpose` e leia o README do componente antes de usar. O README diz
variantes, estados, acessibilidade e o que **não** fazer.

## 4. Componha com os primitivos

```html
<main class="ttsc-container ttsc-stack">
  <header class="ttsc-page-header">…</header>
  <section class="ttsc-grid ttsc-grid--kpi">…</section>
  <div class="ttsc-split">
    <section class="ttsc-card">…</section>
    <aside class="ttsc-card">…</aside>
  </div>
</main>
```

- `ttsc-container` — largura máxima e padding responsivo.
- `ttsc-stack` — coluna com gap tokenizado.
- `ttsc-grid` — grade auto-ajustável (sem media query manual).
- `ttsc-split` — mestre/detalhe que colapsa em uma coluna abaixo de 1024 px.
- `ttsc-toolbar` — busca + filtros + ações que quebram linha no mobile.
- `ttsc-table-wrapper` — tabela com rolagem própria (a página nunca rola).

## 5. Diferencie a tela

Antes de escrever, responda: **o que esta tela tem que nenhuma outra tem?**
Escolha a variante e a densidade por isso, não por hábito.

- Dashboard de diretoria → 4 KPIs + 1 gráfico largo + 1 lista curta (`executive-strip`).
- Dashboard operacional → 8 KPIs densos + split com feed (`ops-monitor`).
- Lista de 10 mil registros → tabela compacta + filtros em linha (`dense-table`).
- Lista de 12 registros com foto → cards (`card-grid`).

Se a resposta for "igual à anterior", você está prestes a criar mais uma página
clonada.

## 6. Valide antes de entregar

```bash
node scripts/ds-check.mjs paginas/referencia/*.html
```

O validador reprova cor literal, utilitário cru, largura fixa, tabela sem wrapper,
page-spec ausente/duplicada, página acima de 80 KB e — nas regras novas — qualquer
renderizador genérico (`data-model*`), `<script>` inline ou controller acima de
8 KB. Corrija o que ele apontar — não desative a regra.

```bash
node scripts/ds-check.mjs paginas/referencia   # conjunto de referência: exit 0
node scripts/ds-check.mjs --all --report       # dívida histórica: só relatório
```

Antes de escrever JavaScript, leia `docs/ai/js-architecture.md`: componente é
comportamento reutilizável, página é template próprio + controller pequeno.

## Lacuna de componente

Se o catálogo não cobre a necessidade:

1. Registre em `docs/ai/gaps.md`: nome, uso, componente mais próximo.
2. Use o mais próximo **sem** recriar estilo.
3. Proponha a entrada (README + preview) numa mudança separada.
