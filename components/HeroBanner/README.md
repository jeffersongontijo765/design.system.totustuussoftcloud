# HeroBanner

Faixa de destaque da página com título, status, um índice de saúde em anel e uma linha de quatro KPIs. Substitui o cabeçalho simples quando a visão geral precisa de leitura rápida.

## Quando usar

- Visão geral de um portal (secretaria, financeiro, direção) em que o número mais importante deve aparecer antes dos gráficos.
- Quando há um índice composto (saúde, desempenho, ocupação) além de métricas isoladas.
- Para a faixa executiva completa (ticker, frentes, tiles com delta, limites e watchlist), use [ExecutiveStrip](../ExecutiveStrip/README.md); o HeroBanner cobre o hero sozinho.
- Não use em telas de formulário ou listagem: o hero ocupa muito espaço vertical.

## Anatomia

```
┌───────────────────────────────────────────────┬──────────┐
│ EYEBROW · período                             │  (anel)  │
│ Título                                        │   94     │
│ Subtítulo                                     │ Saúde    │
│ [chip] [chip] [chip]                          │          │
├───────────────────────────────────────────────┴──────────┤
│ [KPI]      [KPI]      [KPI]      [KPI]                  │
└──────────────────────────────────────────────────────────┘
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Contêiner | `section.ttsc-hero` | sim |
| Texto | `.ttsc-hero-eyebrow`, `.ttsc-hero-title`, `.ttsc-hero-sub` | título sim |
| Chips de status | `.ttsc-hero-chip` (`-chip-live` para atualização) | não |
| Índice em anel | `.ttsc-hero-score` com `--p` (0–100) | não |
| KPIs | `dl.ttsc-hero-kpis > div` com `dt`, `dd`, e variação `.up` / `.down` / `.flat` | não |

## Variantes / Estados

- **Com índice:** três colunas (texto, anel, KPIs embaixo).
- **Sem índice:** remova `.ttsc-hero-score`; a grade vira uma coluna.
- **Variação:** `.up` (verde) quando melhorou, `.down` (vermelho) quando piorou, `.flat` quando neutro.

## API

| Atributo | Tipo | Efeito |
|---|---|---|
| `--p` (inline no `circle.val`) | número 0–100 | preenchimento do anel |
| `role="img"` + `aria-label` no `.ttsc-hero-score` | texto | descreve o índice para leitores de tela |
| `aria-labelledby` na `section` | id do título | nomeia a região |

## Acessibilidade

- O anel tem `role="img"` e `aria-label` com o valor completo ("94 de 100"), porque o SVG sozinho não é lido.
- A variação usa texto além da cor (`↑`, `↓`), para não depender só de verde e vermelho.
- Use `dl`/`dt`/`dd` para que cada KPI seja lido como par rótulo-valor.

## Modelos

### HTML

```html
<section class="ttsc-hero" aria-labelledby="hero-t">
  <div>
    <p class="ttsc-hero-eyebrow">Gestão acadêmica · 2026.2</p>
    <h2 id="hero-t" class="ttsc-hero-title">Visão geral da instituição</h2>
    <p class="ttsc-hero-sub">Matrículas, frequência e inadimplência do período.</p>
    <div class="ttsc-hero-chips"><span class="ttsc-hero-chip ttsc-hero-chip-live">Atualizado há 3 min</span></div>
  </div>
  <div class="ttsc-hero-score" role="img" aria-label="Índice de saúde acadêmica: 94 de 100">
    <svg class="ttsc-hero-ring" viewBox="0 0 120 120" aria-hidden="true">
      <circle class="trk" cx="60" cy="60" r="52"/>
      <circle class="val" cx="60" cy="60" r="52" style="--p:94"/>
    </svg>
    <span class="ttsc-hero-score-num">94<small>/100</small></span>
    <span class="ttsc-hero-score-label">Saúde acadêmica</span>
  </div>
  <dl class="ttsc-hero-kpis">
    <div><dt>Matrículas ativas</dt><dd>1.284</dd><span class="up">↑ 4,2%</span></div>
    <div><dt>Inadimplência</dt><dd>6,1%</dd><span class="down">↑ 1,2 pt</span></div>
  </dl>
</section>
```

### CSS

Classes: `.ttsc-hero`, `.ttsc-hero-*`. Cores vêm de `--ttsc-accent-soft`, `--ttsc-surface`, `--ttsc-border`, `--ttsc-accent`, `--ttsc-success`, `--ttsc-danger-text`. No tema escuro os tokens trocam sozinhos.

Quebra para uma coluna abaixo de 640 px e os KPIs passam a 2 colunas.

### JS

Sem JavaScript. Para atualizar o índice, altere `--p` e o texto de `.ttsc-hero-score-num`:

```js
function setHealth(el, value) {
  el.querySelector('.val').style.setProperty('--p', value);
  el.querySelector('.ttsc-hero-score-num').firstChild.nodeValue = value;
  el.setAttribute('aria-label', 'Índice de saúde acadêmica: ' + value + ' de 100');
}
```

### SQL

Índice de frequência e matrículas ativas do período (`:periodo` é o `uuid` de `academic_periods`):

```sql
SELECT COUNT(*) AS matriculas_ativas
FROM enrollments
WHERE deleted_at IS NULL AND status = 'active' AND period_uuid = ?;

SELECT ROUND(100 * SUM(status = 'present') / NULLIF(COUNT(*), 0), 1) AS frequencia_media
FROM attendance
WHERE lesson_date >= ? AND lesson_date < ?;
```

## Faça / Não faça

- Faça: um único título por página, com o período no eyebrow.
- Faça: limite a quatro KPIs; os demais vão para a página detalhada.
- Não faça: colocar botões de ação dentro do hero; use o cabeçalho da página.
- Não faça: usar o anel para valores que não são de 0 a 100.
