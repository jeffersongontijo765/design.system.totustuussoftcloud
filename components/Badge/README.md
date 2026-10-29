# Badge

Etiqueta curta (`.ttsc-badge`) para status de registro, contagem ou código, com variantes sólida, light, outline, ghost e ponto, em quatro tamanhos.

> Também listado em: **Base › Badges**.

## Quando usar

- Status de um registro em tabela, card ou cabeçalho de drawer: matrícula Ativa, Trancada, Cancelada; mensalidade Paga, Vencida.
- Contadores ao lado de rótulos: abas (“Pendências 12”), filtros, itens de menu.
- Códigos e formatos: `MAT-2026-0381`, `PDF`, `EAD`.
- Para uma ação clicável use [Button](../Button/README.md) (`ttsc-btn-sm`); badge não é botão — exceto o “x” de remover (`ttsc-badge-btn`) em filtros aplicados.
- Para mensagem com frase completa use alerta (`.ttsc-alert`), não badge.
- Para presença de pessoa use o ponto do [Avatar](../Avatar/README.md).

## Anatomia

```
[ ● ][ rótulo ][ x ]      .ttsc-badge + cor + estilo + tamanho
  │                └ .ttsc-badge-btn (opcional, remover)
  └ .ttsc-badge-dot (opcional, herda currentColor)
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Container | `span.ttsc-badge` | sim |
| Cor | `ttsc-badge-primary` · `-secondary` · `-success` · `-warning` · `-info` · `-destructive` · `-mono` | sim |
| Estilo | (sólido) · `ttsc-badge-light` · `ttsc-badge-outline` · `ttsc-badge-ghost` · `ttsc-badge-stroke` | não |
| Tamanho | `ttsc-badge-xs` (16px) · `-sm` (20px) · padrão (24px) · `-lg` (28px) | não |
| Ponto | `span.ttsc-badge-dot` antes do rótulo | não |
| Remover | `button.ttsc-badge-btn` com `<i class="fa-light fa-xmark">` + `aria-label` | não |
| Desabilitado | `ttsc-badge-disabled` | não |

## Variantes

Status de matrícula do esquema (`enrollments.status`) → variante recomendada:

| Status | Rótulo | Classe | Tokens (com a ponte TTSC) |
|---|---|---|---|
| `active` | Ativa | `ttsc-badge-success ttsc-badge-light` | fundo `ttsc-accent-soft`, texto `ttsc-accent-text` (5,7:1 claro / 6,5:1 escuro) |
| `conditional_pending` | Condicional | `ttsc-badge-warning ttsc-badge-light` | fundo `ttsc-warning` 10%, texto `ttsc-warning-text` (4,7:1 / 8,4:1) |
| `locked` | Trancada | `ttsc-badge-secondary ttsc-badge-light` | fundo `ttsc-surface-2`, texto `ttsc-text` |
| `transferred` | Transferida | `ttsc-badge-info ttsc-badge-light` | fundo `ttsc-info` 10%, texto `ttsc-info-text` (7,7:1 / 6:1) |
| `cancelled` | Cancelada | `ttsc-badge-destructive ttsc-badge-light` | fundo `ttsc-danger` 10%, texto `ttsc-danger-text` escurecido (5,5:1 / 6,9:1) |
| `completed` | Concluída | `ttsc-badge-primary` (sólido) | fundo `ttsc-accent`, texto `ttsc-accent-on` (9,6:1) |

Estilos:

| Estilo | Classe | Uso | Observação |
|---|---|---|---|
| Sólido | só a cor | contadores, “Novo”, destaque único na tela | `success`/`warning`/`info` sólidos do runtime têm texto branco (1,7–3,7:1): a ponte troca para `ttsc-accent-on` |
| Light | `ttsc-badge-light` | **padrão para status** em tabelas | tons suaves; no runtime puro primary = azul — a ponte mapeia para o verde da marca |
| Outline | `ttsc-badge-outline` | status em cards sobre `ttsc-canvas-2` | borda tonal + fundo tonal |
| Stroke | `ttsc-badge-stroke` | códigos (`MAT-2026-0381`), formatos | borda `ttsc-border`, fundo `ttsc-surface` |
| Ghost | `ttsc-badge-ghost` | texto colorido sem fundo, em linhas densas | sem padding horizontal |
| Ponto | `ttsc-badge-dot` dentro de light/outline | status em listas longas | 6px, `currentColor` |
| Mono | `ttsc-badge-mono` | contagem neutra de alto contraste | fundo `ttsc-text`, texto `ttsc-surface` |

## API

Componente só de CSS (sem módulo JS no ttscui). O botão de remover usa [Dismiss](../Dismiss/README.md):

| Atributo | Efeito |
|---|---|
| `data-ttsc-dismiss="#filtro-curso"` no `ttsc-badge-btn` | remove o badge do filtro aplicado (mode `remove`) |

## Acessibilidade

- Cor nunca é o único sinal: o rótulo (“Cancelada”) carrega o significado; o ponto é reforço.
- Contadores ganham contexto para leitor de tela: `<span class="ttsc-badge …" aria-label="12 pendências">12</span>`.
- `ttsc-badge-btn` é `<button type="button">` com `aria-label="Remover filtro Curso: Pedagogia"`.
- Contraste conferido com os tokens (tabela acima). Não use `ttsc-badge-ghost` com `success`/`warning` (verde/amarelo 500 sobre branco ≈ 2:1): prefira `ttsc-badge-light`.
- Rótulos curtos (1–2 palavras), substantivo/adjetivo no feminino quando se refere a “matrícula”: Ativa, Trancada.

## Modelos

### HTML

```html
<!-- Status na listagem de matrículas (mapa status → classe no PHP) -->
<?php
$badge = [
  'active'              => ['success',     'Ativa'],
  'conditional_pending' => ['warning',     'Condicional'],
  'locked'              => ['secondary',   'Trancada'],
  'transferred'         => ['info',        'Transferida'],
  'cancelled'           => ['destructive', 'Cancelada'],
][$row['status']] ?? ['secondary', $row['status_label']];
?>
<span class="ttsc-badge ttsc-badge-sm ttsc-badge-light ttsc-badge-<?= $badge[0] ?>">
  <span class="ttsc-badge-dot"></span><?= $this->e($badge[1]) ?>
</span>

<!-- Contador em aba -->
<button type="button" class="ttsc-tab-toggle active">
  Pendências <span class="ttsc-badge ttsc-badge-xs ttsc-badge-destructive" aria-label="12 pendências">12</span>
</button>

<!-- Código e formato -->
<span class="ttsc-badge ttsc-badge-stroke ttsc-badge-sm">MAT-2026-0381</span>

<!-- Filtro aplicado com remover -->
<span class="ttsc-badge ttsc-badge-outline ttsc-badge-secondary" id="filtro-curso">
  Curso: Pedagogia
  <button type="button" class="ttsc-badge-btn" data-ttsc-dismiss="#filtro-curso" aria-label="Remover filtro Curso: Pedagogia">
    <i class="fa-light fa-xmark"></i>
  </button>
</span>
```

### CSS

```css
/* Ponte (bundle.css): o badge sólido primary já lê --primary (ttsc-accent) e --primary-foreground (ttsc-accent-on) */
:root { --primary: var(--ttsc-accent); --primary-foreground: var(--ttsc-accent-on); }

/* Ponte de contraste TTSC — mesmo papel do ttsc.supabase.css do app: status tonais com tokens */
.ttsc-badge-success:not(.ttsc-badge-light):not(.ttsc-badge-outline):not(.ttsc-badge-ghost) { background: var(--ttsc-success); color: var(--ttsc-accent-on); }
.ttsc-badge-warning:not(.ttsc-badge-light):not(.ttsc-badge-outline):not(.ttsc-badge-ghost) { background: var(--ttsc-warning); color: var(--ttsc-accent-on); }
.ttsc-badge-info:not(.ttsc-badge-light):not(.ttsc-badge-outline):not(.ttsc-badge-ghost)    { background: var(--ttsc-info);    color: var(--ttsc-accent-on); }

.ttsc-badge.ttsc-badge-light.ttsc-badge-primary,
.ttsc-badge.ttsc-badge-light.ttsc-badge-success   { background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text); }
.ttsc-badge.ttsc-badge-light.ttsc-badge-warning   { background: color-mix(in oklab, var(--ttsc-warning) 10%, var(--ttsc-surface)); color: var(--ttsc-warning-text); }
.ttsc-badge.ttsc-badge-light.ttsc-badge-info      { background: color-mix(in oklab, var(--ttsc-info) 10%, var(--ttsc-surface)); color: var(--ttsc-info-text); }
.ttsc-badge.ttsc-badge-light.ttsc-badge-destructive { background: color-mix(in oklab, var(--ttsc-danger) 10%, var(--ttsc-surface)); color: color-mix(in oklab, var(--ttsc-danger-text) 80%, var(--ttsc-text)); }
.ttsc-badge.ttsc-badge-light.ttsc-badge-secondary { background: var(--ttsc-surface-2); color: var(--ttsc-text); }

.ttsc-badge.ttsc-badge-outline.ttsc-badge-primary,
.ttsc-badge.ttsc-badge-outline.ttsc-badge-success { background: var(--ttsc-accent-soft); border-color: var(--ttsc-accent-border); color: var(--ttsc-accent-text); }
.ttsc-badge.ttsc-badge-outline.ttsc-badge-warning { background: var(--ttsc-surface); border-color: color-mix(in oklab, var(--ttsc-warning) 40%, transparent); color: var(--ttsc-warning-text); }
.ttsc-badge.ttsc-badge-outline.ttsc-badge-info    { background: var(--ttsc-surface); border-color: color-mix(in oklab, var(--ttsc-info) 40%, transparent); color: var(--ttsc-info-text); }
.ttsc-badge.ttsc-badge-outline.ttsc-badge-destructive { background: var(--ttsc-surface); border-color: color-mix(in oklab, var(--ttsc-danger) 40%, transparent); color: var(--ttsc-danger-text); }

.ttsc-badge.ttsc-badge-ghost.ttsc-badge-success { color: var(--ttsc-accent-text); }
.ttsc-badge.ttsc-badge-ghost.ttsc-badge-warning { color: var(--ttsc-warning-text); }
.ttsc-badge.ttsc-badge-ghost.ttsc-badge-info    { color: var(--ttsc-info-text); }
.ttsc-badge.ttsc-badge-ghost.ttsc-badge-primary { color: var(--ttsc-accent-text); }
.ttsc-badge.ttsc-badge-ghost.ttsc-badge-destructive { color: var(--ttsc-danger-text); }

/* Extensão: badge numérico redondo para contadores */
.ttsc-badge-count { border-radius: var(--ttsc-radius-pill); font-variant-numeric: tabular-nums; }
```

### JS

```js
// assets/js/core/ttsc.badge.js — cria/atualiza badges de status e contadores vindos da API
const STATUS = {
  active: ['success', 'Ativa'],
  conditional_pending: ['warning', 'Condicional'],
  locked: ['secondary', 'Trancada'],
  transferred: ['info', 'Transferida'],
  cancelled: ['destructive', 'Cancelada'],
};

export function statusBadge(status, label) {
  const [color, text] = STATUS[status] || ['secondary', label || status];
  const el = document.createElement('span');
  el.className = `ttsc-badge ttsc-badge-sm ttsc-badge-light ttsc-badge-${color}`;
  el.innerHTML = '<span class="ttsc-badge-dot"></span>';
  el.append(document.createTextNode(label || text));
  return el;
}

export function setCount(badge, value, noun) {
  badge.textContent = value > 99 ? '99+' : String(value);
  badge.setAttribute('aria-label', `${value} ${noun}`);
  badge.hidden = value === 0;
}

// Contador de pendências da aba (atualiza a cada 2 min)
const counter = document.querySelector('[data-badge-count="pendencias"]');
if (counter) {
  const refresh = async () => {
    const res = await fetch('/api/v1/academic/enrollments/status-counts', { headers: { Accept: 'application/json' } });
    if (!res.ok) return;
    const { data } = await res.json(); // [{ status, label, total }]
    const pend = data.filter((r) => r.status === 'conditional_pending').reduce((s, r) => s + Number(r.total), 0);
    setCount(counter, pend, 'pendências');
  };
  refresh();
  setInterval(refresh, 120000);
}
```

### SQL

```sql
-- Contagem de matrículas por status na unidade, com o rótulo traduzido do enum (MariaDB 10.11 / MySQL 8)
SELECT e.status,
       COALESCE(r.label, e.status) AS label,
       COUNT(*)                    AS total
  FROM enrollments e
  LEFT JOIN ref_enum_enrollments_status_2c4b21edf701 r
         ON r.value = e.status AND r.deleted_at IS NULL
 WHERE e.unit_uuid = :unit_uuid
   AND e.deleted_at IS NULL
 GROUP BY e.status, r.label, r.sort_order
 ORDER BY COALESCE(r.sort_order, 999), total DESC;
```

O controller devolve as linhas como `[{status, label, total}]`; a view usa o mapa `status → classe` do modelo HTML para escolher a cor e mostra `label` com o `total` num `ttsc-badge-xs` (ex.: filtros “Ativa 412 · Trancada 18”). Na listagem, cada linha usa `enrollments.status` com o mesmo mapa.

## Faça / Não faça

- **Faça:** `ttsc-badge-light` para status em tabelas; sólido só para contagens e destaques pontuais.
- **Faça:** mesmo status = mesma cor em todo o produto (use o mapa único do JS/PHP).
- **Faça:** `ttsc-badge-sm` dentro de linhas de tabela (`--ttsc-row-normal`).
- **Não faça:** badge sólido verde/amarelo com texto branco (o runtime puro fica em 1,7–2,3:1).
- **Não faça:** frase inteira dentro de badge; mais de um badge de status por linha.
