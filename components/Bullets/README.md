# Bullets

Marcadores decorativos (`.ttsc-bullet`) — ponto, linha e barra vertical — para listas, legendas de status e agendas, com cores de status por token.

## Quando usar

- Lista curta de itens sem numeração (documentos exigidos, requisitos da turma).
- Legenda de status ao lado do rótulo (“Ativa”, “Pendente”, “Cancelada”) em cards de resumo e gráficos.
- Submenu ou lista de navegação secundária (bullet **linha**; o item ativo ganha cor).
- Agenda/linha do tempo compacta: a **barra vertical** acompanha a altura do item (aulas do dia, eventos).
- **Não use** como único indicador de status em tabelas — use [Badge](../Badge/README.md) (texto + cor).
- **Não use** para status “ao vivo”/em andamento animado — use [Pulse](../Pulse/README.md).
- **Não use** para passos ordenados — use lista numerada ou Stepper.

## Anatomia

```
•  Texto do item          ponto      .ttsc-bullet
—  Texto do item          linha      .ttsc-bullet.ttsc-bullet-line
▌  Título do evento       vertical   .ttsc-bullet.ttsc-bullet-vertical (estica com o item)
▌  08:00–09:40 · Sala
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Lista | `ul.ttsc-bullet-list` (`.is-timeline` para barras verticais) | não |
| Marcador | `span.ttsc-bullet` + `aria-hidden="true"` | sim |
| Forma | (ponto) · `ttsc-bullet-line` · `ttsc-bullet-vertical` · `ttsc-bullet-ring` (vazado) | não |
| Tamanho | `ttsc-bullet-sm` 4px · (6px) · `ttsc-bullet-lg` 8px | não |
| Cor | `ttsc-bullet-accent` · `-success` · `-warning` · `-danger` · `-info` (padrão `ttsc-meta`) | não |
| Texto | irmão do marcador, dentro do `li` | sim |

## Variantes

| Variante | Classe | Uso | Token |
|---|---|---|---|
| Neutro | `ttsc-bullet` | listas de conteúdo | `ttsc-meta` (decorativo) |
| Accent | `ttsc-bullet-accent` | item ativo, “em andamento” | `ttsc-accent` |
| Success | `ttsc-bullet-success` | ativa, aprovado, pago | `ttsc-success` |
| Warning | `ttsc-bullet-warning` | pendente, prova, a vencer | `ttsc-warning` |
| Danger | `ttsc-bullet-danger` | cancelada, reprovado, feriado | `ttsc-danger` |
| Info | `ttsc-bullet-info` | trancada, reunião, informativo | `ttsc-info` |
| Ring | `ttsc-bullet-ring` | rascunho / não iniciado | contorno com a cor da variante |

## API

Somente CSS (implementação TTSC em `assets/css/ttsc.css`). A cor fica em `--ttsc-bullet-color`, usada pelo `ring`; sobrescreva via variável para cores de categoria.

| Variável CSS | Padrão | Efeito |
|---|---|---|
| `--ttsc-bullet-color` | cor da variante | cor do contorno no `ttsc-bullet-ring` |

## Acessibilidade

- Marcador sempre `aria-hidden="true"`: o significado vem do texto (“Pendente”), nunca só da cor.
- Use `<ul>/<li>` para manter a semântica de lista mesmo com `list-style: none`.
- Cores de bullet são **não textuais** (exigem 3:1 contra o fundo); `ttsc-meta` é decorativo e não deve carregar informação.
- No submenu, o item ativo também recebe `aria-current="page"` e texto `ttsc-text` (não só a linha verde).

## Modelos

### HTML

```html
<!-- Legenda de status (card de resumo de matrículas) -->
<ul class="ttsc-bullet-list">
  <?php foreach ($statusCounts as $row): ?>
    <li>
      <span class="ttsc-bullet ttsc-bullet-lg ttsc-bullet-<?= $this->e($statusVariant[$row['status']] ?? 'info') ?>" aria-hidden="true"></span>
      <?= $this->e($statusLabel[$row['status']] ?? $row['status']) ?>
      <span class="text-muted-foreground">· <?= (int) $row['total'] ?></span>
    </li>
  <?php endforeach ?>
</ul>

<!-- Agenda do dia com barra vertical -->
<ul class="ttsc-bullet-list is-timeline">
  <?php foreach ($events as $ev): ?>
    <li>
      <span class="ttsc-bullet ttsc-bullet-vertical ttsc-bullet-<?= $this->e($ev['bullet_variant']) ?>" aria-hidden="true"></span>
      <div>
        <div class="font-medium"><?= $this->e($ev['title']) ?></div>
        <div class="text-xs text-muted-foreground"><?= $this->e(substr($ev['start_time'] ?? '', 0, 5)) ?>–<?= $this->e(substr($ev['end_time'] ?? '', 0, 5)) ?> · <?= $this->e($ev['location']) ?></div>
      </div>
    </li>
  <?php endforeach ?>
</ul>

<!-- Submenu com linha -->
<ul class="ttsc-bullet-list">
  <li><span class="ttsc-bullet ttsc-bullet-line ttsc-bullet-accent" aria-hidden="true"></span><a href="/secretaria/matriculas" aria-current="page">Matrículas</a></li>
  <li><span class="ttsc-bullet ttsc-bullet-line" aria-hidden="true"></span><a href="/secretaria/rematricula">Rematrícula</a></li>
</ul>
```

### CSS

```css
/* assets/css/ttsc.css — Bullets (implementação TTSC, só tokens) */
.ttsc-bullet { display: inline-block; flex-shrink: 0; width: 6px; height: 6px; border-radius: var(--ttsc-radius-pill); background: var(--ttsc-meta); }
.ttsc-bullet-sm { width: 4px; height: 4px; }
.ttsc-bullet-lg { width: 8px; height: 8px; }
.ttsc-bullet-line { width: 12px; height: 2px; }
.ttsc-bullet-vertical { width: 4px; height: auto; min-height: 28px; align-self: stretch; }
.ttsc-bullet-ring { background: transparent; box-shadow: inset 0 0 0 1.5px var(--ttsc-bullet-color, var(--ttsc-meta)); }
.ttsc-bullet-accent  { background: var(--ttsc-accent);  --ttsc-bullet-color: var(--ttsc-accent); }
.ttsc-bullet-success { background: var(--ttsc-success); --ttsc-bullet-color: var(--ttsc-success); }
.ttsc-bullet-warning { background: var(--ttsc-warning); --ttsc-bullet-color: var(--ttsc-warning); }
.ttsc-bullet-danger  { background: var(--ttsc-danger);  --ttsc-bullet-color: var(--ttsc-danger); }
.ttsc-bullet-info    { background: var(--ttsc-info);    --ttsc-bullet-color: var(--ttsc-info); }
.ttsc-bullet-ring[class*="ttsc-bullet-"] { background: transparent; }
.ttsc-bullet-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: var(--ttsc-space-2); }
.ttsc-bullet-list > li { display: flex; align-items: center; gap: 10px; color: var(--ttsc-text-2); }
.ttsc-bullet-list.is-timeline > li { align-items: stretch; gap: var(--ttsc-space-3); }
```

### JS

```js
// Sem JS obrigatório. Helper para listas montadas no cliente (ex.: legenda de gráfico ApexCharts)
const STATUS_VARIANT = { active: 'success', pending: 'warning', locked: 'info', cancelled: 'danger', draft: 'ring' };

export function renderStatusLegend(ul, rows, labels) {
  ul.classList.add('ttsc-bullet-list');
  ul.replaceChildren(...rows.map(({ status, total }) => {
    const li = document.createElement('li');
    const dot = document.createElement('span');
    dot.className = `ttsc-bullet ttsc-bullet-lg ttsc-bullet-${STATUS_VARIANT[status] || 'info'}`;
    dot.setAttribute('aria-hidden', 'true');
    li.append(dot, `${labels[status] || status} · ${total}`);
    return li;
  }));
}
```

### SQL

```sql
-- Agenda do dia (barra vertical): eventos da unidade que cobrem :day
SELECT e.uuid, e.title, e.start_time, e.end_time, e.location,
       CASE e.type WHEN 'exam' THEN 'warning' WHEN 'meeting' THEN 'info'
                   WHEN 'holiday' THEN 'danger' ELSE 'accent' END AS bullet_variant
  FROM events e
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
   AND e.status <> 'cancelled'
   AND :day BETWEEN e.start_date AND COALESCE(e.end_date, e.start_date)
 ORDER BY e.start_time IS NULL, e.start_time;

-- Legenda de status (ponto)
SELECT en.status, COUNT(*) AS total
  FROM enrollments en
 WHERE en.deleted_at IS NULL AND en.unit_uuid = :unit_uuid
 GROUP BY en.status
 ORDER BY total DESC;
```

O controller entrega `$events` e `$statusCounts`; o rótulo traduzido de cada `status` vem da tabela `ref_enum_enrollments_status_*` e o mapa status → variante fica num array PHP da view.

## Faça / Não faça

- **Faça:** marcador + texto sempre; cor só reforça.
- **Faça:** barra vertical para itens com 2 linhas (título + horário); ponto para itens de 1 linha.
- **Não faça:** misturar formas na mesma lista nem usar `ttsc-meta` para status.
- **Não faça:** usar `•` digitado no texto — use o `span.ttsc-bullet` (alinhamento e cor consistentes).
