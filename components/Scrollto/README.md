# Scrollto

Gatilho que rola a janela ou um painel até um elemento-alvo (`data-ttsc-scrollto`, ttscui), com rolagem suave e deslocamento para compensar cabeçalhos fixos.

## Quando usar

- Atalhos pontuais: “Ir para pendências”, “Ver primeiro erro do formulário”, “Voltar ao topo”, chips de resumo que levam à turma correspondente.
- Dentro de drawers ou cards roláveis (`parent` = corpo rolável).
- **Não use** como índice de várias seções com destaque da seção atual: use [Scrollspy](../Scrollspy/README.md).
- **Não use** para trocar de conteúdo: use [Tabs](../Tabs/README.md). Para navegar para outra página use um link comum.

## Anatomia

```
[ Ir para ADM-2026-1N ]  ──click──▶  parent.scrollTo({ top: alvo.offsetTop + offset })
 data-ttsc-scrollto="#turma-adm-2026-1n"
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Gatilho | `a`/`button` com `data-ttsc-scrollto="#alvo"` | sim |
| Alvo | elemento com `id`; ou `data-ttsc-scrollto-target` quando o valor do atributo principal for `true` | sim |
| Contêiner | `data-ttsc-scrollto-parent="#painel"` (padrão `body` = `window`) | não |
| Deslocamento | `data-ttsc-scrollto-offset="-16"` | não |

## Variantes

| Variante | Marcação | Tokens |
|---|---|---|
| Link de atalho | `a.ttsc-link` + `data-ttsc-scrollto` | `ttsc-accent-text` |
| Chip de resumo | `button.ttsc-badge.ttsc-badge-outline` | borda `ttsc-border`, texto `ttsc-text-2` |
| Voltar ao topo | `button.ttsc-btn.ttsc-btn-outline.ttsc-btn-icon` fixo no canto | `ttsc-surface`, `ttsc-shadow-md` |
| Destaque de chegada | classe `.ttsc-scrollto-flash` no alvo (JS abaixo) | fundo `ttsc-accent-soft` |

## API

Conferida em `src/components/scrollto/scrollto.ts`. Opções por `data-ttsc-scrollto-<opção>` no gatilho, objeto no construtor ou `window.ttscGlobalComponentsConfig.scrollto`.

| Opção | Atributo | Padrão | Descrição |
|---|---|---|---|
| alvo | `data-ttsc-scrollto` | — | seletor do alvo; também liga a instância |
| `target` | `data-ttsc-scrollto-target` | `""` | alvo alternativo quando o atributo principal não é seletor |
| `parent` | `data-ttsc-scrollto-parent` | `"body"` | elemento que rola; `body` ou ausente → `window` |
| `offset` | `data-ttsc-scrollto-offset` | `0` | **somado** a `alvo.offsetTop` (`parseInt`) — use negativo para parar antes (ex.: `-16`, ou `-60` com cabeçalho fixo) |
| `smooth` | `data-ttsc-scrollto-smooth` | `true` | `behavior: "smooth"` ou `"instant"` |

| Método | Descrição |
|---|---|
| `ttscScrollto.getInstance(el)` / `getOrCreateInstance(el, cfg)` | instância do gatilho |
| `scroll()` | executa a rolagem programaticamente |
| `getOption(nome)` | lê a opção efetiva |

Não há eventos: o clique faz `preventDefault()` e chama `scroll()`. O cálculo usa `offsetTop`, então o `parent` precisa ser o `offsetParent` do alvo (`position: relative`).

## Acessibilidade

- Use `<a href="#alvo">` quando o destino tem `id` — sem JS continua funcionando pelo hash.
- Depois de rolar, mova o foco para o alvo (`tabindex="-1"` + `focus({ preventScroll: true })`) para o leitor de tela acompanhar; o ttscui não faz isso sozinho (ver JS).
- Botão “Voltar ao topo” só-ícone: `aria-label="Voltar ao topo"`.
- Com `prefers-reduced-motion: reduce`, passe `smooth: false`.

## Modelos

### HTML

```html
<!-- Resumo de turmas no topo da ficha do curso: cada chip rola até o card da turma -->
<div class="flex items-center gap-2">
  <?php foreach ($classes as $cl): ?>
    <button type="button" class="ttsc-badge ttsc-badge-outline"
            data-ttsc-scrollto="#turma-<?= $this->e(strtolower($cl['code'])) ?>"
            data-ttsc-scrollto-parent="#course-body" data-ttsc-scrollto-offset="-12">
      <?= $this->e($cl['code']) ?> · <?= (int) $cl['enrolled'] ?>/<?= (int) $cl['max_students'] ?>
    </button>
  <?php endforeach ?>
</div>

<div id="course-body" class="ttsc-scroll-panel">
  <?php foreach ($classes as $cl): ?>
    <article id="turma-<?= $this->e(strtolower($cl['code'])) ?>" tabindex="-1" class="ttsc-card"> … </article>
  <?php endforeach ?>
</div>

<!-- Formulário: atalho para o primeiro erro -->
<a class="ttsc-link" href="#field-cpf" data-ttsc-scrollto="#field-cpf" data-ttsc-scrollto-offset="-80">Corrigir CPF</a>

<!-- Voltar ao topo da página -->
<button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon ttsc-scrollto-top"
        data-ttsc-scrollto="#page-top" aria-label="Voltar ao topo"><i class="fa-light fa-arrow-up"></i></button>
```

### CSS

```css
/* O contêiner precisa ser offsetParent dos alvos para offsetTop bater */
.ttsc-scroll-panel { position: relative; overflow-y: auto; max-height: 60vh; }

/* Destaque breve no alvo ao chegar */
.ttsc-scrollto-flash { animation: ttsc-scrollto-flash 1.2s ease-out; }
@keyframes ttsc-scrollto-flash {
  from { background: var(--ttsc-accent-soft); box-shadow: 0 0 0 2px var(--ttsc-accent-border); }
  to   { background: var(--ttsc-surface); box-shadow: none; }
}
@media (prefers-reduced-motion: reduce) { .ttsc-scrollto-flash { animation: none; outline: 2px solid var(--ttsc-accent); } }

/* Botão "voltar ao topo" flutuante */
.ttsc-scrollto-top {
  position: fixed; inset-inline-end: var(--ttsc-space-6); bottom: var(--ttsc-space-6);
  z-index: var(--ttsc-z-floating); box-shadow: var(--ttsc-shadow-md); background: var(--ttsc-surface);
}
```

### JS

```js
TTSC.init(); // cria uma instância por [data-ttsc-scrollto]

// Foco + destaque no alvo depois da rolagem (o ttscui não emite evento: escute o clique)
document.addEventListener('click', (event) => {
  const trigger = event.target.closest('[data-ttsc-scrollto]');
  if (!trigger) return;
  const target = document.querySelector(trigger.getAttribute('data-ttsc-scrollto'));
  if (!target) return;
  setTimeout(() => {
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
    target.classList.remove('ttsc-scrollto-flash');
    void target.offsetWidth; // reinicia a animação
    target.classList.add('ttsc-scrollto-flash');
  }, 350);
});

// Programático: após validar o formulário, rola até o primeiro campo inválido
export function scrollToFirstError(form) {
  const field = form.querySelector('[aria-invalid="true"]');
  if (!field) return;
  const helper = document.createElement('a');
  helper.setAttribute('data-ttsc-scrollto', `#${field.id}`);
  new ttscScrollto(helper, { offset: -80, smooth: !matchMedia('(prefers-reduced-motion: reduce)').matches }).scroll();
  field.focus({ preventScroll: true });
}
```

### SQL

Os chips de resumo vêm das turmas ativas do curso, com ocupação:

```sql
SELECT cl.uuid, cl.code, COALESCE(cl.name, cl.code) AS label, cl.shift, cl.max_students,
       COUNT(e.id) AS enrolled
  FROM classes cl
  LEFT JOIN enrollments e
         ON e.class_uuid = cl.uuid AND e.deleted_at IS NULL AND e.status = 'active'
 WHERE cl.course_uuid = :course_uuid
   AND cl.deleted_at IS NULL
   AND cl.is_active = 1
 GROUP BY cl.uuid, cl.code, cl.name, cl.shift, cl.max_students
 ORDER BY cl.code;
```

O mesmo `$classes` gera os chips e os cards; o `id` do alvo é derivado de `code` (único por unidade em `uk_class_unit_code`), então nunca colide na página.

## Faça / Não faça

- **Faça:** `offset` negativo igual à altura do cabeçalho/toolbar fixo.
- **Faça:** levar o foco ao destino depois de rolar.
- **Não faça:** usar scrollto para “abrir” conteúdo escondido — o alvo precisa estar visível.
- **Não faça:** esquecer `position: relative` no `parent`; o destino fica errado.
