# EmptyState

Estado vazio do chassi (`.ttsc-empty-state`): caixa tracejada com ícone em tile verde, título, descrição e no máximo uma ação, nas variantes sem dados, sem resultado de busca e erro de carregamento.

## Quando usar

- Uma visão do chassi (tabela, cards, Kanban, gráfico, painel de dashboard) não tem o que mostrar e o usuário precisa saber **por quê** e **o que fazer**.
- **Sem dados** (`is-no-data`): a entidade ainda não tem registros → ação "Novo" (só se a fonte é gravável).
- **Sem resultado** (`is-no-results`): há registros, mas a busca/filtro não encontrou nada → "Limpar filtros", nunca "Novo".
- **Erro** (`is-error`): a leitura falhou → explique e ofereça "Tentar novamente"; não mostre zero como se fosse dado.
- **Sem permissão** (`is-permission-denied`, previsto no átomo): explique o acesso necessário, sem ação.
- Não use para avisos dentro de formulários ([Alert](../Alert/README.md)) nem para carregamento ([Skeleton](../Skeleton/README.md) / spinner).

## Anatomia

```
┌ - - - - - - - - - - - - - - - - - - - - ┐  .ttsc-empty-state.is-<variante>[role=status]
╎              [ ícone ]                   ╎  .ttsc-empty-state-icon (tile 52px, verde)
╎     Nenhuma matrícula cadastrada         ╎  .ttsc-empty-state-title (h3/strong 16px 700)
╎  As matrículas do ano letivo 2026 …      ╎  .ttsc-empty-state-desc (13px, máx. 28rem)
╎          [ + Nova matrícula ]            ╎  .ttsc-empty-state-action (opcional)
└ - - - - - - - - - - - - - - - - - - - - ┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Caixa | `div.ttsc-empty-state` + `is-no-data` / `is-no-results` / `is-error` / `is-permission-denied`; `role="status"` (erro: `role="alert"`) | sim |
| Ícone | `span/div.ttsc-empty-state-icon > i.fa-light.<ícone>[aria-hidden]` | sim |
| Título | `.ttsc-empty-state-title` (`h3` ou `strong`) | sim |
| Descrição | `p.ttsc-empty-state-desc` | sim |
| Ação | `button/a.ttsc-empty-state-action` (ou `ttsc-btn ttsc-btn-primary` no átomo) | não |
| Célula de tabela | `td.ttsc-empty-state-cell[colspan]` envolvendo a caixa | em tabelas |
| Compacto | `.is-compact` (min-height 9rem, máx. 28rem) / dentro de `.portal-dashboard` | não |

## Variantes

| Variante | Ícone típico | Ação | Origem no repo |
|---|---|---|---|
| Sem dados | ícone da entidade / `fa-inbox` | "Novo …" (`data-action="open-create-drawer"`) se gravável | `chassis/table.php`, `components/empty_state.php`, `TTSCModelKit.blocks.empty` |
| Sem resultado | `fa-magnifying-glass` | "Limpar filtros" (texto verde) | `#<id>-empty` da tabela/cards; o átomo suprime CTA em `no-results` |
| Erro | `fa-triangle-exclamation` | "Tentar novamente" | `ttsc.analytics-panels.js` (`.ttsc-analytics-empty`) e status do developer; a classe `is-error` não tem CSS próprio no runtime — use a extensão abaixo |
| Não se aplica | `fa-bars-progress` | atalho para a aba Tabela | `.ttsc-chassis-empty-card` ("Kanban não se aplica", `domain_page.php`) |
| Ficha pendente | `fa-file-pen` | — | `TTSCModelKit.render(t, null)` |

Tokens/cores: borda `var(--ttsc-border)` 2px tracejada, fundo `var(--ttsc-surface-subtle)`, ícone `rgba(16,185,129,.08)` + `var(--ttsc-accent-strong)`, título `var(--ttsc-text)`, descrição `var(--ttsc-text-muted)`.

## API

**PHP — partials reais**

| Partial | Parâmetros |
|---|---|
| `app::components/atoms/empty-state` (`$this->fetch`) | `variant` (`no-data\|no-results\|permission-denied\|error`), `title`, `description`, `icon` (classe completa, padrão `fa-light fa-folder-open`), `ctaLabel`, `ctaUrl`, `ctaAction` (nome de função JS), `class` |
| `resources/views/app/partials/components/empty_state.php` (`include`) | `$variant` (padrão `no-data`), `$icon` (sem prefixo `fa-`), `$title` (padrão "Nenhum registro encontrado"), `$description`, `$actionText` + `$actionUrl` (omitidos em `no-results`), `$class`, `$attrs`, `$slot` |
| `chassis/table.php` | `$table['emptyTitle']`, `['emptyDescription']`, `$chassis['create']['label']` → ação "Novo" com `data-action="open-create-drawer"` |

**JS**

| API | Efeito |
|---|---|
| `TTSCModelKit.blocks.empty(icon, title, desc, ctaHtml)` | HTML de `.ttsc-empty-state.is-no-data[role=status]` |
| `data-action="open-create-drawer"` | `domain_page.php` abre `CFG.drawers.create` |
| `#<id>-reset` / "Limpar filtros" | zera busca e `window.__modelFilters` e redesenha (kit); `behaviors.php` no chassi |
| `TTSCAnalytics` `model.empty` / `emptyDetail` | estado vazio dentro do painel de gráfico |

**Quando cada variante aparece (endpoints)**

| Resposta de `GET /api/v1/domain/records{rota}` | Variante |
|---|---|
| `200` com `totalRecords = 0` e sem `search`/`status` | sem dados |
| `200` com `totalRecords = 0` e com `search` ou `status` | sem resultado |
| `403` (permissão/rail), `409` (tenant) | sem permissão |
| `422`, `429`, `5xx`, falha de rede | erro (manter dados anteriores) |

## Acessibilidade

- `role="status"` para vazio e sem resultado (anuncia sem roubar o foco); `role="alert"` para erro.
- Ícone sempre `aria-hidden="true"`; o título diz o estado em palavras.
- Uma única ação, com verbo: "Nova matrícula", "Limpar filtros", "Tentar novamente".
- O runtime pinta a ação com texto branco sobre `--ttsc-accent` (≈ 2:1). Use `--ttsc-accent-on` (9,6:1), como no preview.
- Descrição em `--ttsc-text-muted` (≥ 4,5:1 nos dois temas).

## Modelos

### HTML

1) PHP real:

```php
<?php // resources/views/app/partials/chassis/table.php — tabela sem linhas ?>
<?php if (empty($tblRows)): ?>
<tr>
  <td colspan="<?= $tblColspan ?>" class="ttsc-empty-state-cell">
    <div class="ttsc-empty-state is-no-data" role="status">
      <span class="ttsc-empty-state-icon"><i class="fa-light fa-inbox" aria-hidden="true"></i></span>
      <strong class="ttsc-empty-state-title"><?= $e($tblEmptyTitle) ?></strong>
      <p class="ttsc-empty-state-desc"><?= $e($tblEmptyDescription) ?></p>
      <?php if (!empty($chassis['create']['label'])): ?>
      <button type="button" class="ttsc-empty-state-action" data-action="open-create-drawer">
        <i class="fa-light fa-plus" aria-hidden="true"></i><?= $e($chassis['create']['label']) ?>
      </button>
      <?php endif; ?>
    </div>
  </td>
</tr>
<?php endif; ?>

<?php // Átomo, como em partials/portal/data_explorer.php ?>
<?= $this->fetch('app::components/atoms/empty-state', [
    'variant'     => $search !== '' ? 'no-results' : 'no-data',
    'title'       => $search !== '' ? 'Nenhuma matrícula para “' . $search . '”' : 'Nenhuma matrícula cadastrada',
    'description' => 'As matrículas do ano letivo 2026 aparecem aqui assim que a primeira for registrada.',
    'icon'        => 'fa-light fa-user-graduate',
    'ctaLabel'    => $canWrite ? 'Nova matrícula' : '',
    'ctaAction'   => 'openCreateEnrollment',
]) ?>
```

2) HTML gerado (preview):

```html
<div class="ttsc-empty-state is-no-data" role="status">
  <div class="ttsc-empty-state-icon"><i class="fa-light fa-user-graduate" aria-hidden="true"></i></div>
  <h3 class="ttsc-empty-state-title">Nenhuma matrícula cadastrada</h3>
  <p class="ttsc-empty-state-desc">As matrículas do ano letivo 2026 aparecem aqui assim que a primeira for registrada.</p>
  <button type="button" class="ttsc-empty-state-action" data-action="open-create-drawer"><i class="fa-light fa-plus" aria-hidden="true"></i>Nova matrícula</button>
</div>

<div class="ttsc-empty-state is-no-results" role="status" aria-live="polite">
  <span class="ttsc-empty-state-icon"><i class="fa-light fa-magnifying-glass" aria-hidden="true"></i></span>
  <h3 class="ttsc-empty-state-title">Nenhuma matrícula para “Ana Beatriz”</h3>
  <p class="ttsc-empty-state-desc">Nenhum registro corresponde à busca e ao filtro Status: Em análise. Ajuste a busca ou limpe os filtros para ver as 48 matrículas.</p>
  <button type="button" id="es-reset" class="whitespace-nowrap rounded-lg px-2.5 py-2 text-xs font-semibold text-emerald-700 hover:bg-emerald-50 focus:outline-none focus:ring-2 focus:ring-emerald-500/40">Limpar filtros</button>
</div>

<div class="ttsc-empty-state is-error" role="alert">
  <span class="ttsc-empty-state-icon"><i class="fa-light fa-triangle-exclamation" aria-hidden="true"></i></span>
  <h3 class="ttsc-empty-state-title">Não foi possível carregar as matrículas</h3>
  <p class="ttsc-empty-state-desc">O servidor respondeu HTTP 503 em <code>GET /api/v1/domain/records/academic/enrollment/re-enrollment</code>. Os dados anteriores foram mantidos.</p>
  <button type="button" class="ttsc-empty-state-action"><i class="fa-light fa-arrows-rotate" aria-hidden="true"></i>Tentar novamente</button>
</div>
```

### CSS

`assets/css/ttsc.css` ("Shared empty-data state used by every portal"): `.ttsc-empty-state` (flex coluna, min-height 12rem, borda 2px tracejada, raio 1.25rem, padding 3rem/3.5rem), `.is-compact`, `.portal-dashboard .ttsc-empty-state`, `-icon`, `-title`, `-desc`, `-action` (+ `:hover`, `:focus-visible`), `.ttsc-empty-state-cell`, e o escuro: `html.dark .ttsc-empty-state { border-color:#334155; background:rgba(30,41,59,.45) }`, ícone `#34d399` sobre verde 12%, título `#f8fafc`, descrição `#94a3b8`. `assets/css/ttsc.commercial.css` garante que `.hidden`/`[hidden]`/`display:none` escondam a caixa e define `.ttsc-chassis-empty-card`.

```css
/* Extensões por tokens (as mesmas do preview) */
.ttsc-empty-state-action { color: var(--ttsc-accent-on); }               /* 9,6:1 em vez de branco */
.ttsc-empty-state.is-error { border-color: color-mix(in srgb, var(--ttsc-danger) 45%, var(--ttsc-border)); }
.ttsc-empty-state.is-error .ttsc-empty-state-icon,
html.dark .ttsc-empty-state.is-error .ttsc-empty-state-icon {
  color: var(--ttsc-danger-text);
  background: color-mix(in srgb, var(--ttsc-danger) 10%, transparent);
  border-color: color-mix(in srgb, var(--ttsc-danger) 30%, transparent);
  box-shadow: none;
}
```

### JS

```js
// Decide a variante pela resposta do endpoint real e renderiza com o bloco do kit
const API = '/api/v1/domain/records/academic/enrollment/re-enrollment';
const host = document.getElementById('domain-table-empty-host');

function emptyFor(kind, search) {
  if (kind === 'no-data') {
    return TTSCModelKit.blocks.empty('fa-user-plus', 'Nenhuma solicitação de rematrícula',
      'As solicitações aparecem aqui quando o período de rematrícula abrir.');
  }
  if (kind === 'no-results') {
    return TTSCModelKit.blocks.empty('fa-magnifying-glass', `Nenhuma solicitação para “${search}”`,
      'Ajuste a busca ou limpe os filtros.',
      '<button type="button" data-empty-reset class="rounded-lg px-2.5 py-2 text-xs font-semibold text-emerald-700 hover:bg-emerald-50">Limpar filtros</button>')
      .replace('is-no-data', 'is-no-results');
  }
  return TTSCModelKit.blocks.empty('fa-triangle-exclamation', 'Não foi possível carregar as solicitações',
    'Tente novamente em instantes. Os dados anteriores foram mantidos.',
    '<button type="button" data-empty-retry class="ttsc-empty-state-action"><i class="fa-light fa-arrows-rotate" aria-hidden="true"></i>Tentar novamente</button>')
    .replace('is-no-data', 'is-error').replace('role="status"', 'role="alert"');
}

async function load(search = '') {
  try {
    const res = await fetch(`${API}?per_page=25&search=${encodeURIComponent(search)}`, { credentials: 'same-origin' });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const { totalRecords } = await res.json();
    host.innerHTML = totalRecords ? '' : emptyFor(search ? 'no-results' : 'no-data', search);
  } catch (e) {
    host.innerHTML = emptyFor('error');
  }
}
host.addEventListener('click', (ev) => {
  if (ev.target.closest('[data-empty-reset]')) load('');
  if (ev.target.closest('[data-empty-retry]')) load(document.getElementById('domain-table-search')?.value || '');
});
load();
```

### SQL

O estado vazio é decidido por duas contagens — total da fonte e total com o filtro:

```sql
-- Sem dados? (total da fonte da página, sem filtros)
SELECT COUNT(*) AS total
  FROM inst_secretariat_reenrollment;

-- Sem resultado? (mesmo filtro que a tabela aplica)
SELECT COUNT(*) AS filtrado
  FROM inst_secretariat_reenrollment
 WHERE (student_name LIKE :q ESCAPE '\\' OR course_name LIKE :q ESCAPE '\\' OR class_name LIKE :q ESCAPE '\\')
   AND (:status = '' OR status = :status);

-- Sem permissão? (catálogo RBAC do master, mesma cadeia do AuthorizationGuard)
SELECT COUNT(*) > 0 AS pode_ler
  FROM permissions p
  JOIN role_permission rp ON rp.permission_id = p.uuid
  JOIN user_role ur       ON ur.role_id = rp.role_id
 WHERE ur.user_id = :user_uuid
   AND p.slug = 'admin.academic.enrollments';
```

`total = 0` → `is-no-data`; `total > 0` e `filtrado = 0` → `is-no-results`; exceção/HTTP ≥ 500 → `is-error`. `pode_ler = 0` → `is-permission-denied` (o servidor já responde 403).

## Faça / Não faça

- **Faça:** dizer o motivo e o próximo passo; usar o ícone da entidade em "sem dados".
- **Faça:** separar "sem dados" de "sem resultado" — a ação muda (Novo × Limpar filtros).
- **Não faça:** mostrar "Novo" em fonte somente leitura ou em "sem resultado".
- **Não faça:** transformar erro em zero ou em estado vazio silencioso.
