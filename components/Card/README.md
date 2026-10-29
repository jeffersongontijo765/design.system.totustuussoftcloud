# Card

Superfície agrupadora do ttscui (`.ttsc-card`) com cabeçalho, toolbar, conteúdo, tabela e rodapé — a base de painéis de dashboard, KPIs e blocos de formulário.

> Também listado em: **Base › Cards**.

## Quando usar

- Agrupar um bloco com título próprio: “Matrículas recentes”, “Frequência da turma”, “Dados do responsável”.
- KPI de dashboard (número + variação + meta) — padrão detalhado em [KpiCard](../KpiCard/README.md).
- Tabela curta (até ~10 linhas) dentro de um painel com `.ttsc-card-table`; listagem completa com busca e paginação vai no [DataTable](../DataTable/README.md).
- Não aninhe card dentro de card; dentro de um card use `.ttsc-card-group` (seções separadas por borda).
- Conteúdo de um único registro aberto a partir de uma lista vai no [Drawer](../Drawer/README.md), não num card expandido.

## Anatomia

```
┌ .ttsc-card ─────────────────────────────────────────────┐
│ .ttsc-card-header                                        │
│   .ttsc-card-heading (.ttsc-card-title + -description)   │
│                                   .ttsc-card-toolbar [⋯] │
├──────────────────────────────────────────────────────────┤
│ .ttsc-card-content   ou   .ttsc-card-table > table       │
│   (.ttsc-card-group … .ttsc-card-group)                  │
├──────────────────────────────────────────────────────────┤
│ .ttsc-card-footer                         [Ver todas →]  │
└──────────────────────────────────────────────────────────┘
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Container | `.ttsc-card` (borda `--border`, raio `--radius + 4px`, sombra xs) | sim |
| Cabeçalho | `.ttsc-card-header` (mín. 56px, `flex-wrap`, borda inferior) | não |
| Título | `.ttsc-card-heading > h3.ttsc-card-title` + `p.ttsc-card-description` | com cabeçalho |
| Toolbar | `.ttsc-card-toolbar` (botões `ttsc-btn-sm`, toggle group, dropdown) | não |
| Conteúdo | `.ttsc-card-content` (padding 20px) | um dos dois |
| Tabela | `.ttsc-card-table > .ttsc-table-wrapper > table.ttsc-table` (alinha 1ª/última coluna ao padding do card) | um dos dois |
| Seções | `.ttsc-card-group` (várias, separadas por borda) | não |
| Rodapé | `.ttsc-card-footer` (borda superior, padding 16/20px) | não |

## Variantes

| Variante | Classe | Uso | Tokens |
|---|---|---|---|
| Padrão | `.ttsc-card` | painéis | fundo `--card` (= `ttsc-surface`), borda `ttsc-border`, texto `ttsc-text` |
| Accent | `.ttsc-card.ttsc-card-accent` | card “emoldurado”: fundo externo `--muted` (= `ttsc-canvas-2`) com conteúdo em `surface` | `ttsc-canvas-2` + `ttsc-surface` |
| Grid | `.ttsc-card.ttsc-card-grid` | tabela sem padding lateral no conteúdo | — |
| KPI (extensão) | `.ttsc-card` + `.ttsc-card-kpi` | número grande, variação e meta | valor `ttsc-text`, variação positiva `ttsc-accent-text`, negativa `ttsc-danger-text`, barra `ttsc-accent` |
| Interativo (extensão) | `a.ttsc-card.ttsc-card-link` | card clicável (atalho de módulo) | hover borda `ttsc-border-strong` |

## Estados

| Estado | Como aplicar |
|---|---|
| Carregando | `.ttsc-skeleton` dentro de `.ttsc-card-content` (mesma altura do conteúdo final) |
| Vazio | `.ttsc-card-content` com o [EmptyState](../EmptyState/README.md) compacto |
| Hover (card-link) | borda `ttsc-border-strong` (extensão CSS) |
| Erro de carga | `.ttsc-alert.ttsc-alert-destructive` no topo do conteúdo + botão “Tentar novamente” |

## API

Componente de layout sem JavaScript. Os elementos internos usam seus próprios componentes: toolbar com [Dropdown](../Dropdown/README.md) (`data-ttsc-dropdown`), corpo recolhível com [Collapse](../Collapse/README.md), remoção do card com [Dismiss](../Dismiss/README.md) (`data-ttsc-dismiss="#card-id"`).

| Atributo (extensão `ttsc.card.js`) | Efeito |
|---|---|
| `data-ttsc-card-src="/api/v1/…"` | carrega o conteúdo via `fetch` e substitui o skeleton |
| `data-ttsc-card-refresh="60"` | recarrega a cada N segundos |

## Acessibilidade

- O título é um heading real (`h2`/`h3` conforme a hierarquia da página); o card inteiro pode ser `<section aria-labelledby="id-do-título">`.
- Card clicável: o elemento é `<a>` (um único link), nunca `div` com `onclick`; botões internos não ficam dentro de um card-link.
- Valores de KPI têm rótulo textual (“Matrículas ativas”) e a variação inclui o sentido em texto (“+4,2% vs. mês anterior”), não só seta/cor.
- Contraste: título `ttsc-text` (16:1), descrição `--muted-foreground` = `ttsc-text-muted` (≥4,5:1), variação positiva em `ttsc-accent-text` (nunca `ttsc-accent`).

## Modelos

### HTML

```html
<!-- KPI -->
<section class="ttsc-card ttsc-card-kpi" aria-labelledby="kpi-ativas">
  <div class="ttsc-card-content">
    <div class="flex items-center justify-between">
      <span class="ttsc-kpi-label" id="kpi-ativas">Matrículas ativas</span>
      <span class="ttsc-kpi-icon"><i class="fa-light fa-user-graduate"></i></span>
    </div>
    <div class="ttsc-kpi-value"><?= number_format($kpi['active_total'], 0, ',', '.') ?></div>
    <div class="ttsc-kpi-delta is-up"><i class="fa-light fa-arrow-trend-up"></i> +<?= $kpi['delta_pct'] ?>% vs. mês anterior</div>
    <div class="ttsc-progress ttsc-progress-primary" role="progressbar" aria-valuenow="<?= $kpi['occupancy'] ?>" aria-valuemin="0" aria-valuemax="100" aria-label="Ocupação das turmas">
      <div class="ttsc-progress-indicator" style="width: <?= $kpi['occupancy'] ?>%"></div>
    </div>
  </div>
</section>

<!-- Card com toolbar, tabela e rodapé -->
<section class="ttsc-card" aria-labelledby="card-recentes">
  <div class="ttsc-card-header">
    <div class="ttsc-card-heading">
      <h3 class="ttsc-card-title" id="card-recentes">Matrículas recentes</h3>
      <p class="ttsc-card-description">Últimas 5 matrículas da unidade</p>
    </div>
    <div class="ttsc-card-toolbar">
      <button type="button" class="ttsc-btn ttsc-btn-sm ttsc-btn-outline"><i class="fa-light fa-arrow-down-to-line"></i> Exportar</button>
    </div>
  </div>
  <div class="ttsc-card-table">
    <div class="ttsc-table-wrapper">
      <table class="ttsc-table">
        <thead><tr><th>Aluno</th><th>Curso</th><th>Status</th><th class="text-end">Data</th></tr></thead>
        <tbody>
        <?php foreach ($recent as $r): ?>
          <tr>
            <td><?= $this->e($r['student_name']) ?></td>
            <td><?= $this->e($r['course_name']) ?></td>
            <td><span class="ttsc-badge ttsc-badge-sm ttsc-badge-light ttsc-badge-success">Ativa</span></td>
            <td class="text-end"><?= date('d/m/Y', strtotime($r['enrollment_date'])) ?></td>
          </tr>
        <?php endforeach; ?>
        </tbody>
      </table>
    </div>
  </div>
  <div class="ttsc-card-footer justify-end">
    <a class="ttsc-link ttsc-link-sm" href="/academic/enrollments">Ver todas <i class="fa-light fa-arrow-right"></i></a>
  </div>
</section>
```

### CSS

```css
/* Ponte (bundle.css) */
:root { --card: var(--ttsc-surface); --card-foreground: var(--ttsc-text); --muted: var(--ttsc-canvas-2); --border: var(--ttsc-border); }

/* Ajustes do chassi: título 14px, sombra do token */
.ttsc-card { box-shadow: var(--ttsc-shadow-xs); }
.ttsc-card-title { font-size: 14px; color: var(--ttsc-text); }
.ttsc-card-description { font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-card-table .ttsc-table thead th { font-size: 12px; color: var(--ttsc-text-muted); background: var(--ttsc-canvas-2); height: var(--ttsc-row-compact); }
.ttsc-card-table .ttsc-table tbody td { color: var(--ttsc-text-2); }

/* Extensão: KPI */
.ttsc-card-kpi .ttsc-card-content { display: flex; flex-direction: column; gap: var(--ttsc-space-2); padding: var(--ttsc-space-4); }
.ttsc-kpi-label { font-size: 12px; font-weight: 500; color: var(--ttsc-text-muted); }
.ttsc-kpi-icon { display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: var(--ttsc-radius-sm); background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text); }
.ttsc-kpi-value { font-size: 28px; line-height: 1.1; font-weight: 600; color: var(--ttsc-text); font-variant-numeric: tabular-nums; }
.ttsc-kpi-delta { font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-kpi-delta.is-up { color: var(--ttsc-accent-text); }
.ttsc-kpi-delta.is-down { color: var(--ttsc-danger-text); }

/* Extensão: card clicável */
a.ttsc-card-link { text-decoration: none; transition: border-color .15s ease; }
a.ttsc-card-link:hover { border-color: var(--ttsc-border-strong); }
```

### JS

```js
// assets/js/core/ttsc.card.js — cards com conteúdo remoto (dashboards)
async function loadCard(card) {
  const body = card.querySelector('.ttsc-card-content, .ttsc-card-table');
  card.setAttribute('aria-busy', 'true');
  try {
    const res = await fetch(card.dataset.ttscCardSrc, { headers: { Accept: 'text/html' } });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    body.innerHTML = await res.text();      // o endpoint devolve o parcial Plates já renderizado
    TTSC.init();                            // reativa dropdowns/tooltips do conteúdo novo
  } catch (error) {
    body.innerHTML = `<div class="ttsc-alert ttsc-alert-destructive"><div class="ttsc-alert-title">Não foi possível carregar.</div>
      <button type="button" class="ttsc-btn ttsc-btn-sm ttsc-btn-outline" data-card-retry>Tentar novamente</button></div>`;
  } finally {
    card.removeAttribute('aria-busy');
  }
}

document.querySelectorAll('.ttsc-card[data-ttsc-card-src]').forEach((card) => {
  loadCard(card);
  card.addEventListener('click', (e) => { if (e.target.closest('[data-card-retry]')) loadCard(card); });
  const every = Number(card.dataset.ttscCardRefresh || 0);
  if (every > 0) setInterval(() => document.visibilityState === 'visible' && loadCard(card), every * 1000);
});
```

### SQL

```sql
-- KPI "Matrículas ativas" + novas no mês e no mês anterior + capacidade das turmas (MariaDB 10.11 / MySQL 8)
SELECT COUNT(*) AS active_total,
       COALESCE(SUM(e.enrollment_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')), 0) AS new_this_month,
       COALESCE(SUM(e.enrollment_date >= DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y-%m-01')
                AND e.enrollment_date <  DATE_FORMAT(CURDATE(), '%Y-%m-01')), 0) AS new_last_month,
       (SELECT COALESCE(SUM(c.max_students), 0)
          FROM classes c
         WHERE c.unit_uuid = :unit_uuid AND c.is_active = 1 AND c.deleted_at IS NULL) AS capacity
  FROM enrollments e
 WHERE e.unit_uuid = :unit_uuid
   AND e.status = 'active'
   AND e.deleted_at IS NULL;

-- Tabela do card "Matrículas recentes"
SELECT e.uuid, e.code, s.name AS student_name, c.name AS course_name, e.status, e.enrollment_date
  FROM enrollments e
  JOIN users s   ON s.uuid = e.student_uuid AND s.deleted_at IS NULL
  JOIN courses c ON c.uuid = e.course_uuid  AND c.deleted_at IS NULL
 WHERE e.unit_uuid = :unit_uuid
   AND e.deleted_at IS NULL
 ORDER BY e.enrollment_date DESC, e.id DESC
 LIMIT 5;
```

O controller calcula `delta_pct = (new_this_month - new_last_month) / max(new_last_month, 1) * 100` e `occupancy = active_total / max(capacity, 1) * 100` em PHP e passa `$kpi` e `$recent` para a view.

## Faça / Não faça

- **Faça:** um card por assunto; título curto em substantivo (“Frequência da turma”).
- **Faça:** toolbar com no máximo 2 ações visíveis + menu “⋯”.
- **Faça:** `.ttsc-card-table` para tabelas (alinha as colunas ao padding do card).
- **Não faça:** card dentro de card; sombra maior que `ttsc-shadow-xs` em cards estáticos.
- **Não faça:** variação de KPI só com cor ou seta; escreva o percentual e o período.
