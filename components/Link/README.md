# Link

Texto navegável do chassi (`.ttsc-link`) em verde de texto `ttsc-accent-text`, com variantes de sublinhado (hover, fixo, tracejado), mono, inversa, tamanhos e desabilitado.

## Quando usar

- Navegar para outra página ou registro: nome do aluno numa tabela → ficha do aluno; “Ver todas as matrículas” no rodapé de um card.
- Links dentro de texto corrido (ajuda, termos, e-mails da secretaria).
- Abrir documento/arquivo (`download`), e-mail (`mailto:`), telefone (`tel:`).
- Para **ações** na página (salvar, abrir drawer, excluir) use [Button](../Button/README.md) — `ttsc-btn-ghost` se precisar parecer leve.
- Para menu de vários destinos use [Dropdown](../Dropdown/README.md).

## Anatomia

```
[ ícone ][ rótulo ][ ícone ]      a.ttsc-link + sublinhado + cor + tamanho
   (opcional)        └ fa-arrow-right / fa-arrow-up-right-from-square (externo)
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Container | `a.ttsc-link` (`inline-flex`, gap 4px, peso 500, 13px) | sim |
| Sublinhado | `ttsc-link-underline` (só no hover) · `ttsc-link-underlined` (sempre) · `ttsc-link-dashed` (estilo tracejado, combine com `-underlined`) | não |
| Cor | (padrão `ttsc-accent-text`) · `ttsc-link-mono` (`ttsc-text`) · `ttsc-link-inverse` (sobre fundo `ttsc-accent`) | não |
| Tamanho | `ttsc-link-sm` (12px) · padrão (13px) · `ttsc-link-lg` (14px) | não |
| Desabilitado | `ttsc-link-disabled` + `aria-disabled="true"` + `tabindex="-1"` | não |
| Ícone | `<i class="fa-light …">` antes/depois do rótulo | não |

## Variantes

| Variante | Classe | Uso | Tokens |
|---|---|---|---|
| Padrão | `ttsc-link` | navegação em tabelas e cards | `ttsc-accent-text` — #006e46 claro (6,4:1 sobre `surface`), #3ecf8e escuro (9,6:1) |
| Hover sublinhado | `ttsc-link ttsc-link-underline` | listas, rodapés | sublinhado 4px de offset no hover |
| Sublinhado fixo | `ttsc-link ttsc-link-underlined` | **dentro de texto corrido** (obrigatório: a cor sozinha não basta) | idem |
| Tracejado | `ttsc-link ttsc-link-underlined ttsc-link-dashed` | termo com definição/tooltip, “ver regra” | traço 1px |
| Mono | `ttsc-link ttsc-link-mono` | nome do aluno em tabela densa, breadcrumb | `ttsc-text` (16:1); hover `ttsc-accent-text` (extensão) |
| Inversa | `ttsc-link ttsc-link-inverse` | sobre faixa `ttsc-accent` (banner de destaque) | runtime: `--background` (2:1 sobre o verde); extensão: `ttsc-accent-on` (9,6:1) |
| Desabilitado | `ttsc-link-disabled` | destino indisponível (sem permissão) | opacidade 50%, sem ponteiro |

O runtime puro pintaria o link com `--primary` (`ttsc-accent`, 2:1 sobre branco); a ponte do `bundle.css` sobrescreve para `ttsc-accent-text`.

## Estados

| Estado | Como aplicar |
|---|---|
| Hover | automático: sublinhado (`-underline`) ou mistura de `ttsc-accent-text` com `ttsc-text` (extensão) |
| Foco | anel 2px (`:focus-visible`, ring do runtime + contorno global `ttsc-accent`) |
| Visitado | não diferenciado (o produto é uma aplicação, não um site) |
| Externo | `target="_blank"` + `rel="noopener"` + ícone `fa-arrow-up-right-from-square` + texto oculto “(abre em nova aba)” |

## API

Sem JavaScript. Para links que dependem de permissão, o servidor decide entre `<a href>` e o link desabilitado (ver SQL do [Button](../Button/README.md)).

## Acessibilidade

- Sempre `<a href>` real; nunca `<a>` sem `href` ou com `href="#"` + `onclick` (isso é um botão).
- Texto descreve o destino: “Ver matrícula MAT-2026-0381”, não “clique aqui”. Em listas repetidas use `aria-label` com o contexto.
- Em texto corrido, use `ttsc-link-underlined`: cor não pode ser o único sinal de link (WCAG 1.4.1).
- Desabilitado: `aria-disabled="true"`, `tabindex="-1"` e remova o `href`.
- Nunca use `ttsc-accent` (#3ecf8e) como cor de texto no tema claro (2:1); o token certo é `ttsc-accent-text`.

## Modelos

### HTML

```html
<!-- Nome do aluno na tabela (mono, verde no hover) -->
<a class="ttsc-link ttsc-link-mono" href="/academic/students/<?= $this->e($row['student_uuid']) ?>"
   aria-label="Abrir ficha de <?= $this->e($row['student_name']) ?>"><?= $this->e($row['student_name']) ?></a>

<!-- Rodapé de card -->
<a class="ttsc-link ttsc-link-sm ttsc-link-underline" href="/academic/enrollments?course=<?= $this->e($course['uuid']) ?>">
  Ver todas as matrículas <i class="fa-light fa-arrow-right"></i>
</a>

<!-- Texto corrido -->
<p>Consulte o <a class="ttsc-link ttsc-link-underlined" href="/docs/regimento.pdf" download>regimento escolar (PDF, 1,2 MB)</a>
   ou fale com a secretaria em <a class="ttsc-link ttsc-link-underlined" href="mailto:secretaria@colegio.edu.br">secretaria@colegio.edu.br</a>.</p>

<!-- Termo com explicação -->
<a class="ttsc-link ttsc-link-underlined ttsc-link-dashed" href="/help/frequencia-minima">frequência mínima</a>

<!-- Externo -->
<a class="ttsc-link" href="https://www.gov.br/inep" target="_blank" rel="noopener">
  Portal do INEP <i class="fa-light fa-arrow-up-right-from-square"></i><span class="sr-only">(abre em nova aba)</span>
</a>

<!-- Sem permissão -->
<a class="ttsc-link ttsc-link-disabled" aria-disabled="true" tabindex="-1">Histórico financeiro</a>
```

### CSS

```css
/* Ponte (bundle.css) — texto verde é sempre o token de TEXTO */
.ttsc-link { color: var(--ttsc-accent-text); }

/* Extensão TTSC */
.ttsc-link:hover { color: color-mix(in oklab, var(--ttsc-accent-text) 80%, var(--ttsc-text)); }
.ttsc-link-mono { color: var(--ttsc-text); }
.ttsc-link-mono:hover { color: var(--ttsc-accent-text); }
.ttsc-link-underlined { text-decoration-color: color-mix(in oklab, currentColor 50%, transparent); }
.ttsc-link-underlined:hover { text-decoration-color: currentColor; }
.ttsc-link-inverse { color: var(--ttsc-accent-on); }   /* sobre ttsc-accent: 9,6:1 */
.ttsc-link i { font-size: 12px; }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
```

### JS

```js
// assets/js/core/ttsc.links.js — marca links externos e trata links desabilitados
document.querySelectorAll('a.ttsc-link[href^="http"]').forEach((a) => {
  if (new URL(a.href).origin === location.origin) return;
  a.target = '_blank';
  a.rel = 'noopener noreferrer';
  if (!a.querySelector('.fa-arrow-up-right-from-square')) {
    a.insertAdjacentHTML('beforeend', ' <i class="fa-light fa-arrow-up-right-from-square" aria-hidden="true"></i><span class="sr-only">(abre em nova aba)</span>');
  }
});

document.addEventListener('click', (event) => {
  const link = event.target.closest('a.ttsc-link-disabled, a[aria-disabled="true"]');
  if (link) event.preventDefault();
});
```

### SQL

Links apontam para registros; a URL usa o `uuid` (nunca o `id` numérico). Exemplo da coluna “Aluno” e “Curso” da listagem:

```sql
SELECT e.uuid          AS enrollment_uuid,
       e.code          AS enrollment_code,
       s.uuid          AS student_uuid,
       s.name          AS student_name,
       c.uuid          AS course_uuid,
       c.name          AS course_name
  FROM enrollments e
  JOIN users s   ON s.uuid = e.student_uuid AND s.deleted_at IS NULL
  JOIN courses c ON c.uuid = e.course_uuid  AND c.deleted_at IS NULL
 WHERE e.unit_uuid = :unit_uuid
   AND e.deleted_at IS NULL
 ORDER BY s.name
 LIMIT 20;
```

A view monta `href="/academic/students/{student_uuid}"` e `href="/academic/courses/{course_uuid}"`; se o usuário não tem a permissão da página de destino, o mesmo texto sai como `ttsc-link-disabled`.

## Faça / Não faça

- **Faça:** `ttsc-link-mono` para nomes em tabelas densas (verde em todas as linhas cansa).
- **Faça:** `ttsc-link-underlined` dentro de parágrafos.
- **Faça:** ícone de seta só quando o link leva a uma lista/página (“Ver todas →”).
- **Não faça:** link para ação destrutiva ou que envia formulário — use botão.
- **Não faça:** `ttsc-accent` como cor de texto; nem link verde sobre fundo verde (use `ttsc-link-inverse`).
