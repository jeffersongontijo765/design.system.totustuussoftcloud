# Utilities

Catálogo das classes utilitárias Tailwind v4 **realmente compiladas** no `bundle.css` (subconjunto do `tailwind-runtime.css` do app) e dos helpers `ds-*` de documentação.

## Quando usar

- Ajustes de layout local numa view Plates: alinhar itens (`flex items-center gap-2`), grade de 2/3 colunas, truncar texto, esconder (`hidden`).
- Cores **só** pelas utilitárias ligadas a tokens (`text-foreground`, `text-muted-foreground`, `bg-muted`, `border-border`) — trocam sozinhas no tema escuro.
- Se a classe não existe no bundle (ex.: `p-6`, `space-y-3`, `h-10`, `max-w-sm`, `sr-only`, `font-bold`), **não invente**: use um componente `ttsc-*`, um helper `ds-*` (só documentação) ou CSS local com `var(--ttsc-*)`.
- Visual de componente (botão, badge, card) → classes `ttsc-*` ([Button](../Button/README.md), [Badge](../Badge/README.md)); não recrie com utilitárias.

## Anatomia

```
bundle.css = ponte de tokens (--primary → --ttsc-accent …) + tailwind-runtime.css (utilitários usados pelo app + .ttsc-*)
           + Font Awesome 7 + helpers ds-*
Conferência:  grep -c '\.p-6[{:,. ]' components/bundle.css   → 0 = não existe
```

| Categoria | Classes presentes (conferidas por grep) |
|---|---|
| Display | `block` `inline` `inline-block` `flex` `inline-flex` `grid` `contents` `table` `hidden` |
| Posição | `relative` `absolute` `fixed` `static` · `top-0` `top-2` `top-1/2` `end-0` `start-0` `right-0` `bottom-0` `z-1` `z-5` `z-10` `z-20` `z-50` |
| Flex | `flex-row` `flex-col` `flex-col-reverse` `flex-wrap` `flex-nowrap` `flex-1` `grow` `grow-0` `shrink-0` `basis-1/2` `basis-1/4` `order-1` `order-2` |
| Alinhamento | `items-start` `items-center` `items-end` `items-stretch` `justify-start` `justify-center` `justify-end` `justify-between` `place-items-center` `self-*` não (use `justify-self-end`) |
| Grid | `grid-cols-1` `grid-cols-2` `grid-cols-3` `col-span-1` `col-span-2` · responsivo `lg:grid-cols-2` `lg:grid-cols-5` `xl:grid-cols-3` |
| Gap | `gap-0` `gap-0.5` `gap-1` `gap-1.5` `gap-2` `gap-2.5` `gap-3` `gap-3.5` `gap-4` `gap-5` `gap-6` `gap-7.5` `gap-10` `gap-px` `gap-x-4` `gap-x-6` |
| Padding | `p-0` `p-0.5` `p-1.5` `p-2` `p-2.5` `p-3` `p-3.5` `p-4` `p-5` `p-7` `p-7.5` · `px-0…px-10` (0, .5, 1.5, 2, 2.5, 3, 3.5, 4, 5, 7) · `py-1…py-10` · `pt-*` `pb-*` `ps-*` `pe-*` parciais |
| Margem | `m-2.5` `m-5` `mx-auto` `my-auto` `ms-auto` `mt-0…mt-5` `mb-0…mb-7.5` `me-*` `ms-*` parciais |
| Tamanho | `w-full` `w-px` `w-4…w-80` (4, 5, 7, 8, 9, 16, 20, 24, 28, 36, 40, 48, 56, 72, 80) `w-[220px]`… · `h-full` `h-auto` `h-4…h-12` (4, 5, 6, 7, 8, 8.5, 9, 11, 12) · `size-1…size-16` · `min-w-0` `max-w-full` `max-w-none` `max-w-5xl` |
| Tipografia | `text-2xs` `text-xs` `text-2sm` `text-sm` `text-base` `text-lg` `text-xl` `text-2xl` `text-3xl` · `font-normal` `font-medium` `font-semibold` · `leading-none` `leading-4` `leading-5` `leading-6` · `uppercase` `italic` `tracking-tight` · `text-start` `text-center` `text-end` · `truncate` `whitespace-nowrap` `text-nowrap` |
| Cor de texto (tokens) | `text-foreground` (`ttsc-text`) · `text-secondary-foreground` (`ttsc-text`) · `text-muted-foreground` (`ttsc-text-muted`) · `text-accent-foreground` · `text-mono` · `text-destructive` (`ttsc-danger`) · `text-primary` (**`ttsc-accent`, 2:1 — não use para texto**) · `text-primary-foreground` |
| Fundo (tokens) | `bg-background` (`ttsc-surface`) · `bg-muted` `bg-muted/25…/70` (`ttsc-canvas-2`) · `bg-accent` `bg-accent/60` (hover neutro) · `bg-primary` `bg-primary/10` · `bg-destructive` · `bg-border` · `bg-transparent` |
| Borda (tokens) | `border` `border-0` `border-2` `border-t` `border-b` `border-s` `border-e` `border-x` `border-y` `border-dashed` · `border-border` (`ttsc-border`) `border-input` (`ttsc-border-strong`) `border-primary` `border-transparent` |
| Raio | `rounded-sm` `rounded-md` `rounded-lg` `rounded-xl` `rounded-2xl` `rounded-full` `rounded-t-xl` `rounded-b-xl` |
| Efeitos | `shadow-xs` `shadow-md` `shadow-none` · `opacity-0` `opacity-80` `opacity-90` `opacity-100` · `transition` `transition-all` `transition-opacity` `duration-200` `duration-300` · `cursor-pointer` `select-none` `overflow-hidden` `overflow-auto` `overflow-x-auto` `overflow-y-auto` |
| Responsivo | só os prefixos usados pelo app: `md:flex-row` `md:hidden` `md:block` `lg:flex` `lg:hidden` `lg:gap-*` `lg:p-*`… (confira cada um) |
| Tema | `dark:hidden` `dark:block` `light:hidden` (mostrar/ocultar por tema) |

Classes com cor crua também existem porque o app as usa (`text-gray-500`, `bg-white`, `bg-emerald-500`, `text-green-500`…). **Não use em telas novas**: não trocam no tema escuro.

### Helpers `ds-*` (somente páginas de documentação)

| Classe | Efeito |
|---|---|
| `ds-pad` | `padding: 16px` |
| `ds-row` | flex, wrap, centro, gap 8px |
| `ds-stack` | coluna, gap 12px |
| `ds-grid` | grid auto-fill `minmax(220px, 1fr)`, gap 12px |
| `ds-label` | 11px, 500, caixa alta, `ttsc-text-muted` |
| `ds-note` | 12px, `ttsc-text-muted` |

## Variantes

| Necessidade | Utilitária | Alternativa quando falta |
|---|---|---|
| Espaço vertical entre filhos | `flex flex-col gap-3` | (`space-y-*` não existe) |
| Padding 24px | — (`p-6` não existe) | `p-5`/`p-7` ou `padding: var(--ttsc-space-6)` |
| Texto só para leitor de tela | — (`sr-only` está no `assets/css/tailwind.css` do app, não no bundle) | CSS local `.ttsc-sr-only` (ver Helpers) |
| Negrito forte | `font-semibold` | (`font-bold` não existe) |
| Texto verde | — | `color: var(--ttsc-accent-text)` |

## API

Sem JavaScript. Para classes vindas do banco, mapeie **valor → classe** no SQL ou no PHP (lista fechada), nunca interpole texto livre do usuário em `class=""`.

## Acessibilidade

- Contraste vem do token: `text-muted-foreground` (≥ 4,5:1) é o mínimo para texto; `ttsc-meta` é decorativo.
- `hidden` remove também do leitor de tela; para esconder só visualmente use o helper sr-only.
- `truncate` corta o texto: forneça o texto completo em `title` ou no detalhe do registro.

## Modelos

### HTML

```html
<!-- Linha de lista: avatar + nome truncado + badge de status à direita -->
<div class="flex items-center gap-3 p-3 border-b border-border">
  <span class="size-8 rounded-full bg-muted flex items-center justify-center text-xs font-medium text-secondary-foreground shrink-0">AS</span>
  <div class="flex flex-col min-w-0 flex-1">
    <span class="text-sm font-medium text-foreground truncate" title="Ana Beatriz Souza">Ana Beatriz Souza</span>
    <span class="text-xs text-muted-foreground truncate">MAT-2026-00412 · 1º ano A · Manhã</span>
  </div>
  <span class="<?= $this->e($row['status_class']) ?>"><?= $this->e($row['status_label']) ?></span>
</div>

<!-- Grade responsiva de cards -->
<div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">…</div>
```

### CSS

```css
/* Ponte (bundle.css): as utilitárias "semânticas" leem estas variáveis */
:root {
  --foreground: var(--ttsc-text);
  --muted-foreground: var(--ttsc-text-muted);
  --muted: var(--ttsc-canvas-2);
  --background: var(--ttsc-surface);
  --border: var(--ttsc-border);
  --input: var(--ttsc-border-strong);
}

/* Utilitárias que faltam no bundle: crie no CSS do domínio, sempre com tokens */
.ttsc-text-accent { color: var(--ttsc-accent-text); }
.ttsc-stack-3 > * + * { margin-top: var(--ttsc-space-3); }
.ttsc-p-6 { padding: var(--ttsc-space-6); }
```

### JS

```js
// Verifica no navegador se uma utilitária existe antes de usá-la em markup gerado por JS
export function hasUtility(className) {
  const selector = `.${CSS.escape(className)}`;
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch { continue; } // folha de outra origem
    for (const rule of rules) {
      if (rule.selectorText && rule.selectorText.split(',').some((s) => s.trim() === selector)) return true;
    }
  }
  return false;
}

// Mapa fechado status → classe (espelha o CASE do SQL)
export const STATUS_CLASS = {
  active: 'ttsc-badge ttsc-badge-success',
  pending: 'ttsc-badge ttsc-badge-warning',
  locked: 'ttsc-badge ttsc-badge-info',
  cancelled: 'ttsc-badge ttsc-badge-destructive',
};
export const statusClass = (status) => STATUS_CLASS[status] || 'ttsc-badge ttsc-badge-secondary';
```

### SQL

Utilitárias não guardam dados — **não aplicável** como persistência. O ponto de contato com o banco é a classe condicional derivada do status: mapeie numa lista fechada (CASE) e escape na view.

```sql
SELECT e.uuid, e.code, e.status,
       CASE e.status
         WHEN 'active'    THEN 'ttsc-badge ttsc-badge-success'
         WHEN 'pending'   THEN 'ttsc-badge ttsc-badge-warning'
         WHEN 'locked'    THEN 'ttsc-badge ttsc-badge-info'
         WHEN 'cancelled' THEN 'ttsc-badge ttsc-badge-destructive'
         ELSE 'ttsc-badge ttsc-badge-secondary'
       END AS status_class
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
 ORDER BY e.enrollment_date DESC
 LIMIT 50;
```

O rótulo (`status_label`) vem da tradução `__('enrollment_status_' . $status)` no PHP; a classe sai do `CASE` (ou do mapa JS acima) e é escrita com `$this->e()`.

## Faça / Não faça

- **Faça:** `grep` no `bundle.css` antes de usar qualquer utilitária; cores pelas utilitárias de token.
- **Faça:** `gap-*` em flex/grid em vez de margens entre irmãos.
- **Não faça:** `text-primary` para texto (verde 2:1); `bg-white`/`text-gray-*` em telas novas; classes montadas com texto do usuário (`class="badge-<?= $status ?>"`).
