# Scrolltop

Botão flutuante “Voltar ao topo” que aparece depois de N px de rolagem e sobe a página (ou um contêiner) com rolagem suave — implementação TTSC em JS puro (`TTSC.Scrolltop`, `data-ttsc-scrolltop`).

## Quando usar

- Páginas longas sem paginação: diário de classe com muitos alunos, relatório impresso em tela, histórico de lançamentos, base de conhecimento.
- Contêineres roláveis altos (drawer com formulário extenso, lista dentro de card com `overflow: auto`).
- **Não use** em listagens paginadas curtas (o rodapé de [Pagination](../Pagination/README.md) já está perto) nem em telas que cabem em 2 alturas de viewport.
- **Não use** para pular para uma seção específica: [SmoothScroll](../SmoothScroll/README.md) / [Scrollto](../Scrollto/README.md) com âncora.
- Não empilhe com outros flutuantes no mesmo canto (chat widget): desloque com `bottom` ou esconda um deles.

## Anatomia

```
                                        ┌────┐
   conteúdo rolado > offset  ─────────► │ ↑  │  button.ttsc-scrolltop.is-visible
                                        └────┘  fixed, right/bottom --ttsc-space-6, z --ttsc-z-floating
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Botão | `button.ttsc-scrolltop` + `aria-label="Voltar ao topo"` | sim |
| Ativação | `data-ttsc-scrolltop` (`"true"` = janela, ou seletor do contêiner) | sim |
| Limite | `data-ttsc-scrolltop-offset="200"` (px) | não (200) |
| Ícone | `<i class="fa-light fa-arrow-up">` | sim |
| Visível | `.is-visible` (aplicado pelo JS) | — |
| Alvo de foco | `main h1` ou `[data-ttsc-scrolltop-focus]` | recomendado |

## Variantes

| Variante | Como | Tokens |
|---|---|---|
| Janela | `data-ttsc-scrolltop="true"`, `position: fixed` | fundo `ttsc-surface`, borda `ttsc-border`, `ttsc-shadow-md`, z `ttsc-z-floating`, raio `ttsc-radius-pill` |
| Contêiner | `data-ttsc-scrolltop="#lista"`; botão `position: absolute` dentro do wrapper `position: relative` | idem |
| Destaque | `.ttsc-scrolltop-accent` | fundo `ttsc-accent`, ícone `ttsc-accent-on` |

## Estados

| Estado | Marca |
|---|---|
| Oculto (rolagem ≤ offset) | sem `.is-visible`, `opacity: 0`, `pointer-events: none`, `aria-hidden="true"`, `tabindex="-1"` |
| Visível | `.is-visible`, focável |
| Hover / foco | `ttsc-canvas-2` / contorno 2px `ttsc-accent` |

## API

| Atributo / opção | Padrão | Descrição |
|---|---|---|
| `data-ttsc-scrolltop` | `"true"` | alvo da rolagem: janela ou seletor |
| `data-ttsc-scrolltop-offset` / `{ offset }` | `200` | px rolados para aparecer |

| Método | Descrição |
|---|---|
| `TTSC.Scrolltop.init(root?)` | inicializa todos os `[data-ttsc-scrolltop]` (idempotente) |
| `new TTSC.Scrolltop(button, options)` | instância manual |
| `instance.update()` | recalcula visibilidade (após trocar conteúdo) |
| `instance.go()` | rola ao topo e move o foco |
| `instance.position()` | posição atual em px |

| Evento (bubbles, no botão) | Quando |
|---|---|
| `ttsc:scrolltop:show` | passou do offset |
| `ttsc:scrolltop:hide` | voltou abaixo do offset |

## Acessibilidade

- `<button>` real com `aria-label="Voltar ao topo"`; oculto fica `aria-hidden` e fora da ordem de Tab.
- Após rolar, o foco vai para o título da página (`main h1`, com `tabindex="-1"`) ou para o contêiner — quem usa teclado não fica “perdido” no fim da página.
- `prefers-reduced-motion`: rolagem instantânea e sem transição.
- Ícone `ttsc-text` sobre `ttsc-surface` (≥ 12:1); a área clicável tem 40×40 px.

## Modelos

### HTML

```html
<!-- No layout (resources/views/app/layouts/…): um por página -->
<button type="button" class="ttsc-scrolltop" data-ttsc-scrolltop="true" data-ttsc-scrolltop-offset="300"
        aria-label="Voltar ao topo">
  <i class="fa-light fa-arrow-up"></i>
</button>

<!-- Dentro de um card com rolagem própria -->
<div class="ttsc-card" style="position: relative">
  <div id="diario-lista" style="max-height: 480px; overflow-y: auto" tabindex="0" aria-label="Lista de alunos">…</div>
  <button type="button" class="ttsc-scrolltop" style="position: absolute"
          data-ttsc-scrolltop="#diario-lista" data-ttsc-scrolltop-offset="120" aria-label="Voltar ao topo">
    <i class="fa-light fa-arrow-up"></i>
  </button>
</div>
```

### CSS

```css
/* assets/css/ttsc.scrolltop.css */
.ttsc-scrolltop {
  position: fixed; right: var(--ttsc-space-6); bottom: var(--ttsc-space-6); z-index: var(--ttsc-z-floating);
  width: 40px; height: 40px; border-radius: var(--ttsc-radius-pill);
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--ttsc-surface); color: var(--ttsc-text);
  border: 1px solid var(--ttsc-border); box-shadow: var(--ttsc-shadow-md); cursor: pointer;
  opacity: 0; transform: translateY(8px); pointer-events: none;
  transition: opacity .2s ease, transform .2s ease, background .15s ease;
}
.ttsc-scrolltop.is-visible { opacity: 1; transform: none; pointer-events: auto; }
.ttsc-scrolltop:hover { background: var(--ttsc-canvas-2); }
.ttsc-scrolltop:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-scrolltop-accent { background: var(--ttsc-accent); color: var(--ttsc-accent-on); border-color: transparent; }
/* acima do rodapé fixo do chassi */
.ttsc-has-footer .ttsc-scrolltop { bottom: calc(var(--ttsc-footer-h) + var(--ttsc-space-4)); }
@media (prefers-reduced-motion: reduce) { .ttsc-scrolltop { transition: none; } }
```

### JS

```js
// assets/js/core/ttsc.scrolltop.js — implementação TTSC
(function (w) {
  function Scrolltop(btn, options) {
    this.btn = btn;
    const sel = btn.getAttribute('data-ttsc-scrolltop');
    this.target = sel && sel !== 'true' ? document.querySelector(sel) : w;
    this.options = Object.assign({ offset: parseInt(btn.getAttribute('data-ttsc-scrolltop-offset') || '200', 10) }, options || {});
    let ticking = false;
    this.target.addEventListener('scroll', () => {
      if (ticking) return;
      ticking = true;
      w.requestAnimationFrame(() => { ticking = false; this.update(); });
    }, { passive: true });
    btn.addEventListener('click', () => this.go());
    this.update();
  }
  Scrolltop.prototype.position = function () {
    return this.target === w ? w.scrollY : this.target.scrollTop;
  };
  Scrolltop.prototype.update = function () {
    const show = this.position() > this.options.offset;
    if (show === this.btn.classList.contains('is-visible')) return;
    this.btn.classList.toggle('is-visible', show);
    this.btn.setAttribute('aria-hidden', String(!show));
    this.btn.tabIndex = show ? 0 : -1;
    this.btn.dispatchEvent(new CustomEvent(show ? 'ttsc:scrolltop:show' : 'ttsc:scrolltop:hide', { bubbles: true }));
  };
  Scrolltop.prototype.go = function () {
    const reduce = w.matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.target.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    const focusEl = this.target === w ? document.querySelector('main h1, [data-ttsc-scrolltop-focus]') : this.target;
    if (focusEl) {
      if (!focusEl.hasAttribute('tabindex')) focusEl.setAttribute('tabindex', '-1');
      focusEl.focus({ preventScroll: true });
    }
  };
  Scrolltop.init = function (root) {
    (root || document).querySelectorAll('[data-ttsc-scrolltop]').forEach((b) => {
      if (!b._ttscScrolltop) b._ttscScrolltop = new Scrolltop(b);
    });
  };
  w.TTSC = w.TTSC || {};
  w.TTSC.Scrolltop = Scrolltop;
  document.addEventListener('DOMContentLoaded', () => Scrolltop.init());
})(window);
```

### SQL

Componente puramente de interface — não lê nem grava dados. O que decide se ele aparece é o tamanho da lista que a página renderiza; por exemplo, o diário de classe com a frequência de cada aluno da turma:

```sql
SELECT s.name AS student_name, e.code,
       ROUND(100 * SUM(a.status = 'present') / NULLIF(COUNT(a.id), 0), 1) AS attendance_rate
  FROM enrollments e
  JOIN users s           ON s.uuid = e.student_uuid AND s.deleted_at IS NULL
  LEFT JOIN attendance a ON a.enrollment_uuid = e.uuid
 WHERE e.class_uuid = :class_uuid
   AND e.status = 'active'
   AND e.deleted_at IS NULL
 GROUP BY e.uuid, s.name, e.code
 ORDER BY s.name;
```

A view inclui o botão no layout uma única vez; com menos de ~20 linhas ele simplesmente nunca passa do offset.

## Faça / Não faça

- **Faça:** um único botão por página (ou por contêiner rolável), no canto inferior direito.
- **Faça:** offset de 1–1,5 altura de viewport para a janela; ~120 px em contêineres.
- **Faça:** mover o foco para o topo após a rolagem.
- **Não faça:** ouvir `scroll` sem `requestAnimationFrame`/`passive` (trava a rolagem).
- **Não faça:** esconder conteúdo (paginação, botões do rodapé) atrás do botão — deixe margem ou suba o `bottom`.
- **Não faça:** usar z-index cru (`9999`): use `--ttsc-z-floating`, abaixo de drawers e modais.
