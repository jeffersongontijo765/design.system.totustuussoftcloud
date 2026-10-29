# ContextBanner

Faixa verde de contexto abaixo do cabeçalho: ícone, título do recorte, descrição curta e uma pill de contagem cujo ponto fica âmbar quando há itens que exigem atenção.

## Quando usar

- Logo abaixo do [PageHeader](../PageHeader/README.md), para dizer **o que** a página mostra (ano letivo, escopo, modo de gravação) e quantos registros existem.
- Quando há um sinal de atenção que vale ver antes das abas (ex.: matrículas indeferidas, rematrículas em análise).
- Não use para avisos transitórios ou erros de ação: use [Toast](../Toast/README.md) ou [Alert](../Alert/README.md).
- Não use como segundo título: se não agrega informação, omita (`banner` ausente na ficha) — regra do `docs/model/app/README.md`.

## Anatomia

```
┌ bg-emerald-50/70 ─────────────────────────────────────────────────────────────┐
│ [tile 40px]  Matrículas 2026  [[cadeado] Somente leitura]          ( ● 48 matrículas ) │
│              Pré-matrículas, documentação pendente, análise…                    │
└───────────────────────────────────────────────────────────────────────────────┘
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Container | `div.bg-emerald-50/70.border.border-emerald-200/80.rounded-2xl.p-4` | sim |
| Tile | `div.w-10.h-10.rounded-xl.bg-white.border-emerald-200.text-emerald-600` + `i.fa-light` | sim |
| Título | `h2.text-base.font-bold.text-slate-800` (> `span`) | sim |
| Modo de gravação | `span.rounded-full.text-[10px].bg-white.border-slate-200` com `fa-pen-to-square` ou `fa-lock` (só em `domain_page.php`) | não |
| Descrição | `p.text-xs.text-slate-500` | sim |
| Pill | `div.rounded-full.bg-white.border-emerald-300.text-emerald-700` + ponto `span.w-2.h-2.rounded-full.animate-pulse` | não |

## Estados

| Estado | Como | Classe do ponto |
|---|---|---|
| Normal | sem itens em atenção | `bg-emerald-500` |
| Atenção | `banner.attention` da ficha > 0 (kit) ou colunas `pending/review/rejected/expired/overdue/failed…` com contagem > 0 (`domain_page.php`) | `bg-amber-500` |
| Cadastro completo / Consulta / Somente leitura | `$canWrite` / `$canCrud` de `DrawerRegistry::forRoute()` | ícone `fa-pen-to-square` ou `fa-lock` |

## API

**Ficha** — objeto `banner`:

| Campo | Tipo | Uso |
|---|---|---|
| `banner.icon` | string | ícone do tile (padrão `fa-circle-info`) |
| `banner.title` | string | `h2` |
| `banner.desc` | string | parágrafo |
| `banner.pill` | string | texto da pill; `{count}` é trocado pelo total de registros |
| `banner.attention` | `{agg, where}` | agregação (mesma sintaxe de `kpis[].value`); > 0 deixa o ponto âmbar |

**PHP** — `chassis/chassis.php`: `$chassis['banner'] = ['icon','title','desc','status']` (`status` = texto da pill; `$chassis['tone']` troca o verde). `chassis/domain_page.php` monta o banner sozinho: título = `$title` sem "Workspace", descrição por escopo (`scope` = `platform` ou tenant), pill = `Banco ativo (N registros)` com `title="<tabela>"`.

**JS**

| Chamada | Efeito |
|---|---|
| `TTSCModelKit.blocks.banner(banner, attention)` | HTML do banner; `attention` booleano liga o ponto âmbar |
| `TTSCModelKit.render(t, page, {banner:false})` | omite o banner |

## Acessibilidade

- O `h2` fica abaixo do `h1` do cabeçalho; não pule níveis.
- A cor do ponto não pode ser a única pista: escreva o motivo no texto da pill ou na descrição ("3 em análise").
- `animate-pulse` respeita `prefers-reduced-motion` só se o tema desligar animações; para quem é sensível, prefira o ponto estático em páginas de leitura longa.
- `text-emerald-700` sobre branco = 5,5:1; `text-slate-500` sobre `emerald-50` ≈ 4,6:1.

## Modelos

### HTML

1) Na página real (`resources/views/app/partials/chassis/domain_page.php`, linhas do "Status banner"):

```php
<?php
$bannerTitle = trim((string) preg_replace('/\s+Workspace$/i', '', $title));
$bannerAttention = 0;
foreach ($kanbanColumns as $col) {
    if (in_array($col['id'], ['pending', 'review', 'pending_review', 'rejected', 'expired', 'overdue', 'failed'], true)) {
        $bannerAttention += (int) $col['count'];
    }
}
$bannerMode = $canWrite ? 'Cadastro completo' : ($canCrud ? 'Consulta — gravado pelo fluxo do sistema' : 'Somente leitura');
?>
<div class="bg-emerald-50/70 border border-emerald-200/80 rounded-2xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
  …
  <span class="w-2 h-2 rounded-full <?= $bannerAttention > 0 ? 'bg-amber-500' : 'bg-emerald-500' ?> animate-pulse"></span>
  <span>Banco ativo (<?= $e(number_format($totalRecords, 0, ',', '.')) ?> registros)</span>
</div>
```

Ou, em páginas montadas com `chassis.php`:

```php
<?php $chassis['banner'] = ['icon' => 'fa-user-graduate', 'title' => 'Matrículas 2026',
    'desc' => 'Pré-matrículas, documentação pendente, análise e alunos matriculados por curso.',
    'status' => $totalRecords . ' matrículas']; ?>
```

2) HTML gerado (preview, com atenção ativa):

```html
<div class="bg-emerald-50/70 border border-emerald-200/80 rounded-2xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
  <div class="flex items-center space-x-3.5">
    <div class="w-10 h-10 rounded-xl bg-white border border-emerald-200 flex items-center justify-center text-emerald-600 shrink-0">
      <i class="fa-light fa-user-graduate text-base"></i>
    </div>
    <div>
      <h2 class="text-base font-bold text-slate-800 flex items-center space-x-1.5"><span>Matrículas 2026</span></h2>
      <p class="text-xs text-slate-500 mt-0.5">Pré-matrículas, documentação pendente, análise e alunos matriculados por curso.</p>
    </div>
  </div>
  <div class="inline-flex items-center space-x-2 px-3 py-1 bg-white border border-emerald-300 rounded-full text-xs font-semibold text-emerald-700 self-start md:self-auto shadow-sm">
    <span class="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
    <span>48 matrículas</span>
  </div>
</div>
```

### CSS

Sem classe própria: utilitários do runtime. No escuro, `assets/css/ttsc.commercial.model.css` tem regras específicas para o banner — `html.dark .bg-emerald-50\/70` (fundo verde translúcido escuro), `html.dark .bg-emerald-50\/70 .bg-white` (tile/pill em superfície escura) e `html.dark .bg-emerald-50\/70 .text-emerald-700` (texto verde claro).

```css
/* Extensão por tokens: variante de alerta (banner âmbar) para períodos encerrados */
.ttsc-banner-warning.bg-emerald-50\/70 {
  background: color-mix(in srgb, var(--ttsc-warning) 10%, var(--ttsc-surface));
  border-color: color-mix(in srgb, var(--ttsc-warning) 35%, transparent);
}
.ttsc-banner-warning .text-emerald-600,
.ttsc-banner-warning .text-emerald-700 { color: var(--ttsc-warning-text); }
```

### JS

```js
// Atualiza a pill com o total do endpoint real e liga o alerta pelos status em análise
async function refreshBanner(route) {
  const base = '/api/v1/domain/records' + route;
  const [all, review] = await Promise.all([
    fetch(base + '?per_page=10', { credentials: 'same-origin' }).then((r) => r.json()),
    fetch(base + '?status=pending_review&per_page=10', { credentials: 'same-origin' }).then((r) => r.json()),
  ]);
  const html = TTSCModelKit.blocks.banner(
    { icon: 'fa-user-plus', title: 'Rematrícula 2027', desc: 'Solicitações de rematrícula por curso e turma.',
      pill: all.totalRecords + ' solicitações' },
    review.totalRecords > 0
  );
  const current = document.querySelector('#model-page > .bg-emerald-50\\/70');
  if (current) current.outerHTML = html;
}
refreshBanner('/academic/enrollment/re-enrollment');
```

### SQL

Contagem da pill + contagem de atenção numa só leitura (ficha: `pill: "{count} matrículas"`, `attention: {agg:"count", where:{status:"rejected"}}`):

```sql
SELECT COUNT(*)                                        AS total,
       SUM(er.status IN ('pending_review', 'rejected')) AS attention
  FROM enrollment_requests er
 WHERE er.deleted_at IS NULL
   AND er.period_uuid = :period_uuid;
```

`total` vira o texto da pill; `attention > 0` liga `bg-amber-500`. Na página real, `PortalDomainDataService::getDataForRoute()` devolve `totalRecords` e as colunas do Kanban com `count`, e o PHP soma as colunas de atenção.

## Faça / Não faça

- **Faça:** descrição de uma linha que diga o recorte (ano, unidade, escopo).
- **Faça:** escrever na pill a unidade ("48 matrículas"), não só o número.
- **Não faça:** mais de um banner por página ou banner dentro de abas.
- **Não faça:** usar o ponto âmbar sem um motivo legível em outro lugar da página (KPI ou lista de atenção).
