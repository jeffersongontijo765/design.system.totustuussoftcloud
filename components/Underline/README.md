# Underline

Sublinhado decorativo para títulos (`.ttsc-underline`: barra curta ou cheia, marca-texto suave) e links com sublinhado animado (`.ttsc-underline-link`), com cor por token.

## Quando usar

- Título de seção em páginas públicas ou de destaque (portal do aluno, processo seletivo, landing de curso) — barra curta abaixo do H1/H2.
- Realçar uma expressão dentro do título (“Prazo final: 30/11”) com marca-texto suave.
- Links em texto corrido que precisam de destaque discreto no hover.
- **Não use** em títulos de telas administrativas densas (PageHeader já tem hierarquia) nem em todo H2 da página.
- **Não use** sublinhado em texto que não é link sem ser claramente decorativo (barra afastada, não colada ao texto).
- Para links padrão do sistema use [Link](../Link/README.md) (`.ttsc-link`).

## Anatomia

```
Processo seletivo 2027
━━━                         .ttsc-underline.ttsc-underline-short (barra ::after)

▒▒Prazo final: 30/11▒▒      .ttsc-underline-soft (marca-texto atrás do texto)

regulamento de matrícula    .ttsc-underline-link (linha cresce da esquerda no hover)
───────────────
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Título/trecho | `.ttsc-underline` em `h1–h3` ou `span` | sim |
| Largura | (100% do texto) · `ttsc-underline-short` (32px) | não |
| Espessura | `ttsc-underline-thin` 2px · (3px) · `ttsc-underline-thick` 6px | não |
| Estilo | (barra) · `ttsc-underline-soft` (marca-texto) | não |
| Cor | (accent) · `ttsc-underline-info` · `-warning` · `-danger` · `-mono` | não |
| Link | `a.ttsc-underline-link` (+ `.is-dotted` para termo com definição) | — |

## Variantes

| Variante | Classe | Token |
|---|---|---|
| Accent | `ttsc-underline` | `ttsc-accent` (barra; texto segue `ttsc-text`) |
| Info | `ttsc-underline-info` | `ttsc-info` |
| Warning | `ttsc-underline-warning` | `ttsc-warning` |
| Danger | `ttsc-underline-danger` | `ttsc-danger` |
| Mono | `ttsc-underline-mono` | `ttsc-text` |
| Soft | `ttsc-underline-soft` | cor da variante a 35% atrás do texto |
| Link | `ttsc-underline-link` | linha 2px `ttsc-accent`, texto `ttsc-text` |
| Pontilhado | `ttsc-underline-link.is-dotted` | `text-decoration: underline dotted` em `ttsc-text-muted` |

## API

Somente CSS (implementação TTSC). Variáveis:

| Variável | Padrão | Efeito |
|---|---|---|
| `--ttsc-underline-color` | `var(--ttsc-accent)` | cor da barra |
| `--ttsc-underline-size` | `3px` | espessura |
| `--ttsc-underline-width` | `100%` | largura (`32px` no `-short`) |

## Acessibilidade

- A barra é decorativa (pseudo-elemento); não carrega significado — o título continua sendo `<h1>/<h2>`.
- A cor do **texto** nunca muda para verde: barra `ttsc-accent` é permitida como não-texto; o texto fica `ttsc-text` (≥ 15:1).
- `ttsc-underline-link` em texto corrido: além da linha no hover/foco, o link precisa ser distinguível em repouso — use dentro de parágrafos com peso 500 ou prefira `.ttsc-link` quando houver muitos links.
- Foco visível: `:focus-visible` também estende a linha; mantém o contorno de foco global.
- `prefers-reduced-motion`: a linha aparece sem animar.

## Modelos

### HTML

```html
<header class="ds-stack">
  <h1 class="ttsc-underline ttsc-underline-short">Processo seletivo 2027</h1>
  <?php if ($deadline): ?>
    <h2>
      <span class="ttsc-underline ttsc-underline-soft ttsc-underline-thick ttsc-underline-warning">
        Prazo final: <?= $this->e(date('d/m', strtotime($deadline['end_date'] ?? $deadline['start_date']))) ?>
      </span>
      para envio de documentos
    </h2>
  <?php endif ?>
</header>

<p>Consulte o <a href="/documentos/regulamento-matricula.pdf" class="ttsc-underline-link">regulamento de matrícula</a> antes de enviar.</p>
<p>Total de <abbr title="Horas exigidas para aprovação por frequência" class="ttsc-underline-link is-dotted">carga horária</abbr> por período.</p>
```

### CSS

```css
.ttsc-underline { --ttsc-underline-color: var(--ttsc-accent); --ttsc-underline-size: 3px; --ttsc-underline-width: 100%;
  position: relative; display: inline-block; padding-bottom: calc(var(--ttsc-underline-size) + 4px); }
.ttsc-underline::after { content: ""; position: absolute; left: 0; bottom: 0; width: var(--ttsc-underline-width);
  height: var(--ttsc-underline-size); border-radius: var(--ttsc-radius-pill); background: var(--ttsc-underline-color); }
.ttsc-underline-short { --ttsc-underline-width: 32px; }
.ttsc-underline-thin  { --ttsc-underline-size: 2px; }
.ttsc-underline-thick { --ttsc-underline-size: 6px; }
.ttsc-underline-soft { isolation: isolate; padding-bottom: 2px; }
.ttsc-underline-soft::after { opacity: .35; bottom: 4px; height: calc(var(--ttsc-underline-size) * 2.5); z-index: -1; }
.ttsc-underline-info    { --ttsc-underline-color: var(--ttsc-info); }
.ttsc-underline-warning { --ttsc-underline-color: var(--ttsc-warning); }
.ttsc-underline-danger  { --ttsc-underline-color: var(--ttsc-danger); }
.ttsc-underline-mono    { --ttsc-underline-color: var(--ttsc-text); }

.ttsc-underline-link { color: var(--ttsc-text); text-decoration: none; padding-bottom: 2px;
  background: linear-gradient(var(--ttsc-accent), var(--ttsc-accent)) left bottom / 0 2px no-repeat; transition: background-size .25s ease; }
.ttsc-underline-link:hover, .ttsc-underline-link:focus-visible, .ttsc-underline-link.is-hover { background-size: 100% 2px; }
.ttsc-underline-link.is-dotted { text-decoration: underline dotted var(--ttsc-text-muted); text-underline-offset: 3px; background: none; }
@media (prefers-reduced-motion: reduce) { .ttsc-underline-link { transition: none; } }
.ttsc-underline[data-underline-animate]::after { transition: width .4s ease; }
```

### JS

```js
// Sem JS obrigatório. Opcional: anima a barra de títulos com data-underline-animate ao entrarem na viewport
const io = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    entry.target.style.setProperty('--ttsc-underline-width', entry.target.dataset.underlineWidth || '32px');
    io.unobserve(entry.target);
  });
}, { threshold: 0.6 });

document.querySelectorAll('.ttsc-underline[data-underline-animate]').forEach((title) => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  title.style.setProperty('--ttsc-underline-width', '0px');
  io.observe(title);
});
```

### SQL

```sql
-- Próximo prazo da unidade, destacado com ttsc-underline-soft no título
SELECT e.title, e.start_date, e.end_date
  FROM events e
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
   AND e.type = 'deadline'            -- tipo conforme ref_enum_events_type_*
   AND e.status <> 'cancelled'
   AND COALESCE(e.end_date, e.start_date) >= CURDATE()
 ORDER BY COALESCE(e.end_date, e.start_date)
 LIMIT 1;
```

O controller passa `$deadline` (ou `null`); sem prazo, o H2 com marca-texto não é renderizado.

## Faça / Não faça

- **Faça:** um título sublinhado por seção principal; barra curta alinhada ao início do texto.
- **Faça:** usar a cor do contexto (warning para prazo, accent para institucional).
- **Não faça:** pintar o texto de verde para “combinar” com a barra.
- **Não faça:** sublinhar texto que não é link com a mesma linha dos links.
