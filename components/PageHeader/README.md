# PageHeader

Cabeçalho de toda página do chassi: tile de ícone 44×44, título `h1`, breadcrumb e o botão verde "Atualizar".

## Quando usar

- Em **toda** página de módulo montada pelo chassi (`chassis/chassis.php` ou `chassis/domain_page.php`) — é o bloco "model 3.1" de `developer/dashboard.php`.
- Uma única vez por página, sempre como primeiro filho de `#main-viewport`.
- Contexto adicional (ano letivo, contagem, alerta) vai no [ContextBanner](../ContextBanner/README.md), logo abaixo; ações da página (Filtrar, Exportar, Novo) vão nas [SegmentedTabs](../SegmentedTabs/README.md), nunca no cabeçalho.
- Não use dentro de drawers, cards ou modais: lá o título é `h3` do próprio painel ([RecordDrawers](../RecordDrawers/README.md)).

## Anatomia

```
[tile 44px: fa-light <ícone>]  Matrículas                                   [⟳ Atualizar]
                               ⌂ / Administração / Acadêmico / Matrículas
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Linha | `div.flex.flex-col.md:flex-row.md:items-center.justify-between.gap-4` | sim |
| Tile de ícone | `div.w-11.h-11.rounded-2xl.bg-emerald-50.border-emerald-200` + `i.fa-light.<ícone>.text-emerald-600.text-lg` | sim |
| Título | `h1.text-xl.font-bold.text-slate-900.tracking-tight` | sim |
| Breadcrumb | `div.text-xs.text-slate-400` com `i.fa-house`, separadores `<span>/</span>`; último item `span.text-slate-600.font-medium` | sim |
| Atualizar | `button.bg-emerald-500 … rounded-xl` com `fa-arrows-rotate` (no chassi: `onclick="location.reload()"`; no kit: `data-model-refresh`) | sim |

## Variantes

| Variante | Como | Tokens / classes |
|---|---|---|
| Tom do módulo | `$chassis['tone']` troca `emerald` por `blue`, `purple`, `amber`, `rose` no tile | `bg-<tone>-50`, `border-<tone>-200`, `text-<tone>-600` |
| Crumb com link | item com `url` vira `<a class="hover:text-slate-600">` | — |
| Sem dados de página | `TTSCModelKit.render(t, null)` desenha só o cabeçalho + estado vazio "Page sheet pending" | [EmptyState](../EmptyState/README.md) |

## API

**PHP (`resources/views/app/partials/chassis/chassis.php`)** — variáveis lidas do escopo da página:

| Variável | Tipo | Efeito |
|---|---|---|
| `$title` (ou `$chassis['title']`) | string | texto do `h1` |
| `$icon` (ou `$chassis['icon']`) | string | classe Font Awesome do tile (padrão `fa-cubes`) |
| `$breadcrumb` | `[['label'=>..,'url'=>..], …]` | migalhas; o último item é a página atual |
| `$chassis['tone']` | `emerald\|blue\|purple\|amber\|rose` | cor do tile (padrão `emerald`) |

Em `domain_page.php`, `$title`/`$icon`/`$breadcrumb` vêm do shim gerado (`resources/views/app/pages/**`), e o título cai para `PagesManifest::find($pageRoute)['title']` quando vazio.

**Ficha (`specs/<portal>/<módulo>.json`)** — campos usados:

| Campo | Uso |
|---|---|
| `title` | `h1` (fallback: `t.page.label`) |
| `icon` | ícone do tile (fallback `fa-file-lines`) |

**JS (`TTSCModelKit`, fim de `vendor/app/app.js`)**

| Chamada | Retorno / efeito |
|---|---|
| `TTSCModelKit.blocks.header(t, page)` | string HTML do cabeçalho; `t = {portal:{label}, module:{label}, page:{label, route}}` |
| `TTSCModelKit.render(t, page, {header:false})` | omite o cabeçalho |
| clique em `[data-model-refresh]` | re-renderiza a página com os últimos argumentos de `render()` |

## Acessibilidade

- Um único `h1` por página; drawers e painéis usam `h3`.
- O ícone do tile é decorativo; o título carrega o sentido. O breadcrumb é texto (no chassi real os itens intermediários com URL são `<a>`); envolva em `<nav aria-label="Trilha">` ao usar fora do chassi.
- "Atualizar" é `<button type="button">` com rótulo visível. Branco sobre `emerald-500` fica abaixo de 4,5:1 para texto pequeno — o contraste é herdado do produto; ao criar variações use `--ttsc-accent` com `--ttsc-accent-on` (9,6:1).

## Modelos

### HTML

1) Como a página real produz o bloco — shim gerado + `chassis/domain_page.php` (que repete o cabeçalho do `chassis.php`):

```php
<?php
// resources/views/app/pages/client/academic/enrollment/re-enrollment.php (gerado por scripts/generate-domain-pages.php)
$pageRoute  = '/academic/enrollment/re-enrollment';
$pageRail   = 'client';
$pageModule = 'Secretariat';
$title      = 'Espaço de Trabalho — Rematrícula';
$description = 'Gerencie Rematrícula em Secretaria (Portal do Cliente).';
$icon       = 'fa-light fa-user-plus';
$breadcrumb = [
    ['label' => 'Portal da Instituição', 'url' => url('/dashboard')],
    ['label' => 'Rematrícula', 'url' => url('/academic/enrollment/re-enrollment')]
];
$this->layout('app::layouts/main', [
    'title' => $title, 'description' => $description, 'icon' => $icon, 'breadcrumb' => $breadcrumb,
    'pageHasHeader' => true, 'railKey' => 'client', 'subSidebarModule' => 'academic_secretariat',
]);
include base_path('resources/views/app/partials/chassis/domain_page.php');
```

2) HTML gerado (capturado do preview):

```html
<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
  <div class="flex items-start space-x-3.5">
    <div class="w-11 h-11 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center shrink-0">
      <i class="fa-light fa-user-graduate text-emerald-600 text-lg"></i>
    </div>
    <div>
      <h1 class="text-xl font-bold text-slate-900 tracking-tight">Matrículas</h1>
      <div class="flex items-center space-x-2 text-xs text-slate-400 mt-0.5">
        <i class="fa-light fa-house text-[10px]"></i>
        <span>/</span><span>Administração</span><span>/</span><span>Acadêmico</span><span>/</span>
        <span class="text-slate-600 font-medium">Matrículas</span>
      </div>
    </div>
  </div>
  <button type="button" data-model-refresh=""
    class="inline-flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-medium text-xs shadow-sm transition active:scale-95 self-start md:self-auto cursor-pointer">
    <i class="fa-light fa-arrows-rotate text-xs"></i><span>Atualizar</span>
  </button>
</div>
```

### CSS

Utilitários Tailwind do runtime; o tema escuro vem de `assets/css/ttsc.commercial.model.css` e `ttsc.luxury-commercial.css`, que remapeiam `html.dark .bg-white`, `.text-slate-900`, `.bg-emerald-50` etc. para superfícies escuras — o cabeçalho não tem CSS próprio.

```css
/* Extensão por tokens: tile no tom de acento do design system (light e dark) */
#model-page > div:first-child .w-11.h-11 {
  background: var(--ttsc-accent-soft);
  border-color: var(--ttsc-accent-border);
}
#model-page > div:first-child .w-11.h-11 i { color: var(--ttsc-accent-text); }
#model-page h1 { color: var(--ttsc-text); letter-spacing: -0.01em; }
```

### JS

```js
// Montar só o cabeçalho de uma página do chassi a partir da ficha real
fetch('/docs/model/app/specs/admin/academico.json')
  .then((r) => r.json())
  .then((sheet) => {
    const route = '/academico/matriculas';
    const crumbs = { portal: { label: 'Administração' }, module: { label: 'Acadêmico' }, page: { label: 'Matrículas', route } };
    TTSCModelKit.render(crumbs, sheet.pages[route], { banner: false, tabs: false });
  });

// Na página real o "Atualizar" recarrega; para recarregar só os dados do endpoint:
document.querySelector('[data-model-refresh]')?.addEventListener('click', async (ev) => {
  ev.stopPropagation();
  const res = await fetch('/api/v1/domain/records/academic/enrollment?page=1&per_page=25', { credentials: 'same-origin' });
  const body = await res.json();          // { success, route, table, totalRecords, page, per_page, records }
  document.dispatchEvent(new CustomEvent('ttsc:records-loaded', { detail: body }));
});
```

### SQL

O cabeçalho não lê o banco; o título vem do manifesto e a visibilidade da página da permissão do contrato (`page-domain-sources.php` → `'permission' => 'admin.academic.view'`). Para montar o breadcrumb a partir da unidade e do período corrente:

```sql
-- Período letivo corrente da unidade (texto do breadcrumb/subtítulo)
SELECT ap.name, ap.year, ap.start_date, ap.end_date
  FROM academic_periods ap
 WHERE ap.is_current = 1
   AND ap.deleted_at IS NULL
   AND (ap.unit_uuid = :unit_uuid OR ap.unit_uuid IS NULL)
 ORDER BY ap.unit_uuid IS NULL, ap.start_date DESC
 LIMIT 1;
```

O controlador passa `name` para `$breadcrumb` ou para o [ContextBanner](../ContextBanner/README.md).

## Faça / Não faça

- **Faça:** um cabeçalho por página, ícone `fa-light` coerente com o item da sidebar (`sidebar-nav.php`).
- **Faça:** breadcrumb curto: portal › módulo › página.
- **Não faça:** colocar Exportar/Novo no cabeçalho — isso é da barra de abas.
- **Não faça:** trocar o `h1` por `h2` ou repetir o título dentro do banner.
