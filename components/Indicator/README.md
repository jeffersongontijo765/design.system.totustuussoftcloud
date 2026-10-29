# Indicator

Indicador de carregamento (`data-indicator="on|off"`) que troca o rótulo de um botão por texto + spinner, mais spinners avulsos e barra de progresso indeterminada para página/bloco.

## Quando usar

- Botão que dispara requisição demorada (salvar matrícula, gerar boletim, exportar): o botão mostra “Salvando…” e fica bloqueado até a resposta.
- Carregamento de uma região (lista de turmas, gráfico) com spinner + texto.
- Topo de página/card enquanto um filtro recarrega dados (barra `ttsc-page-indicator`).
- **Não use** para cobrir e bloquear um bloco inteiro — use [Overlay](../Overlay/README.md) (`ttsc-overlay-loading`).
- **Não use** para progresso com porcentagem conhecida (upload, importação) — use `ttsc-progress`.
- Carregamento inicial de tabela: prefira skeleton do [DataTable](../DataTable/README.md).

## Anatomia

```
[ ícone  Salvar matrícula ]  data-indicator="off"  → .ttsc-indicator-label visível
[ Salvando…  ◠ ]             data-indicator="on"   → .ttsc-indicator-progress visível
━━━━━━━░░░░░░░░░░░░          .ttsc-page-indicator (barra indeterminada)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container | qualquer elemento com `data-indicator="off"` (normalmente `.ttsc-btn`) | sim |
| Rótulo normal | `span.ttsc-indicator-label` | sim |
| Rótulo de progresso | `span.ttsc-indicator-progress` + `role="status"` | sim |
| Spinner FA | `<i class="fa-light fa-spinner-third fa-spin">` | um dos dois |
| Spinner CSS | `span.ttsc-spinner` (`-sm` 12px · 16px · `-lg` 28px) | um dos dois |
| Barra de página | `div.ttsc-page-indicator[data-indicator]` + `role="progressbar"` | não |

## Estados

| Estado | Marcação | Efeito |
|---|---|---|
| Parado | `data-indicator="off"` | mostra `.ttsc-indicator-label` |
| Carregando | `data-indicator="on"` + `disabled` + `aria-busy="true"` | mostra `.ttsc-indicator-progress`, bloqueia cliques, mantém opacidade 100% |
| Barra oculta | `.ttsc-page-indicator[data-indicator="off"]` | `visibility: hidden` (não muda a altura) |

## API

Implementação TTSC (`assets/js/core/ttsc.indicator.js`), equivalente ao `data-kt-indicator` do Metronic.

| Método | Efeito |
|---|---|
| `TTSC.indicator.on(el)` | `data-indicator="on"`, `disabled`, `aria-busy="true"` |
| `TTSC.indicator.off(el)` | volta para `off` e reabilita |
| `TTSC.indicator.wrap(el, promise)` | liga, aguarda a promise, desliga (inclusive em erro); retorna a promise |

| Evento (no elemento) | Quando |
|---|---|
| `ttsc.indicator.on` | após ligar |
| `ttsc.indicator.off` | após desligar |

## Acessibilidade

- `aria-busy="true"` no botão e `role="status"` no texto de progresso: o leitor anuncia “Salvando…”.
- Sempre texto junto do spinner (“Gerando…”) — spinner sozinho não comunica nada.
- `disabled` evita duplo envio; o CSS mantém `opacity: 1` para o texto de progresso não cair abaixo de 4,5:1.
- `prefers-reduced-motion`: as animações desaceleram (2,4 s) em vez de girar rápido.
- Spinner em botão primary usa `ttsc-accent-on`; em superfícies, `ttsc-accent` sobre `ttsc-border-strong`.

## Modelos

### HTML

```html
<form method="post" action="/secretaria/matriculas" data-ttsc-crud>
  <input type="hidden" name="_token" value="<?= $this->e($csrf) ?>">
  <!-- … campos … -->
  <button type="submit" class="ttsc-btn ttsc-btn-primary" data-indicator="off">
    <span class="ttsc-indicator-label"><i class="fa-light fa-floppy-disk"></i> Salvar matrícula</span>
    <span class="ttsc-indicator-progress" role="status">Salvando… <i class="fa-light fa-spinner-third fa-spin"></i></span>
  </button>
</form>

<!-- Botão de relatório com spinner CSS -->
<button type="button" class="ttsc-btn ttsc-btn-outline" data-indicator="off" id="btn-attendance-report">
  <span class="ttsc-indicator-label"><i class="fa-light fa-file-pdf"></i> Relatório de frequência</span>
  <span class="ttsc-indicator-progress" role="status"><span class="ttsc-spinner ttsc-spinner-sm"></span> Gerando…</span>
</button>

<!-- Barra no topo do card -->
<div class="ttsc-page-indicator" data-indicator="off" role="progressbar" aria-label="Carregando turmas"></div>
```

### CSS

```css
[data-indicator] .ttsc-indicator-progress { display: none; }
[data-indicator="on"] .ttsc-indicator-label { display: none; }
[data-indicator="on"] .ttsc-indicator-progress { display: inline-flex; align-items: center; gap: var(--ttsc-space-2); }
[data-indicator="on"] { pointer-events: none; }
.ttsc-btn[data-indicator="on"]:disabled { opacity: 1; }

.ttsc-spinner { display: inline-block; width: 16px; height: 16px; flex-shrink: 0; border-radius: var(--ttsc-radius-pill);
  border: 2px solid var(--ttsc-border-strong); border-top-color: var(--ttsc-accent); animation: ttsc-spin .7s linear infinite; }
.ttsc-spinner-sm { width: 12px; height: 12px; border-width: 1.5px; }
.ttsc-spinner-lg { width: 28px; height: 28px; border-width: 3px; }
.ttsc-btn-primary .ttsc-spinner { border-color: color-mix(in oklab, var(--ttsc-accent-on) 25%, transparent); border-top-color: var(--ttsc-accent-on); }
@keyframes ttsc-spin { to { transform: rotate(360deg); } }

.ttsc-page-indicator { position: relative; height: 3px; overflow: hidden; background: var(--ttsc-accent-soft); border-radius: var(--ttsc-radius-pill); }
.ttsc-page-indicator::before { content: ""; position: absolute; inset: 0 auto 0 0; width: 35%; background: var(--ttsc-accent);
  border-radius: inherit; animation: ttsc-indeterminate 1.2s ease-in-out infinite; }
.ttsc-page-indicator[data-indicator="off"] { visibility: hidden; }
@keyframes ttsc-indeterminate { from { transform: translateX(-100%); } to { transform: translateX(300%); } }
@media (prefers-reduced-motion: reduce) { .ttsc-spinner, .fa-spin, .ttsc-page-indicator::before { animation-duration: 2.4s; } }
```

### JS

```js
// assets/js/core/ttsc.indicator.js — implementação TTSC
(function (w) {
  const emit = (el, name) => el.dispatchEvent(new CustomEvent(name, { bubbles: true }));
  const indicator = {
    on(el) {
      el.setAttribute('data-indicator', 'on');
      el.setAttribute('aria-busy', 'true');
      if ('disabled' in el) el.disabled = true;
      emit(el, 'ttsc.indicator.on');
    },
    off(el) {
      el.setAttribute('data-indicator', 'off');
      el.removeAttribute('aria-busy');
      if ('disabled' in el) el.disabled = false;
      emit(el, 'ttsc.indicator.off');
    },
    async wrap(el, promise) {
      indicator.on(el);
      try { return await promise; } finally { indicator.off(el); }
    },
  };
  w.TTSC = w.TTSC || {};
  w.TTSC.indicator = indicator;
})(window);

// Uso: relatório de frequência
document.getElementById('btn-attendance-report')?.addEventListener('click', (event) => {
  const button = event.currentTarget;
  const bar = document.querySelector('.ttsc-page-indicator');
  bar?.setAttribute('data-indicator', 'on');
  TTSC.indicator.wrap(button, fetch('/api/v1/reports/attendance?from=2026-08-01&to=2026-10-21')
    .then((r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.blob(); })
    .then((blob) => window.open(URL.createObjectURL(blob))))
    .finally(() => bar?.setAttribute('data-indicator', 'off'));
});

// Formulários CRUD: liga o indicador do submit
document.querySelectorAll('form[data-ttsc-crud]').forEach((form) => {
  form.addEventListener('submit', () => {
    const submit = form.querySelector('[type="submit"][data-indicator]');
    if (submit) TTSC.indicator.on(submit);
  });
});
```

### SQL

O indicador cobre consultas lentas. Exemplo — o relatório de frequência por turma que o botão acima gera:

```sql
SELECT c.uuid, c.code, c.name,
       COUNT(a.id) AS records,
       ROUND(100 * SUM(a.status IN ('present', 'late')) / NULLIF(COUNT(a.id), 0), 1) AS attendance_pct
  FROM classes c
  LEFT JOIN attendance a
         ON a.class_uuid = c.uuid
        AND a.lesson_date BETWEEN :date_from AND :date_to
 WHERE c.deleted_at IS NULL
   AND c.unit_uuid = :unit_uuid
 GROUP BY c.uuid, c.code, c.name
 ORDER BY c.name;
```

O endpoint executa a consulta, gera o PDF e responde; enquanto isso o botão fica em `data-indicator="on"` e a barra do card em `on`.

## Faça / Não faça

- **Faça:** verbo no gerúndio no progresso (“Salvando…”, “Gerando…”), mesmo verbo do rótulo.
- **Faça:** sempre desligar no `finally` (erro também).
- **Não faça:** spinner sem texto ou trocar a largura do botão drasticamente (rótulos de tamanho parecido).
- **Não faça:** deixar o botão clicável durante o carregamento.
