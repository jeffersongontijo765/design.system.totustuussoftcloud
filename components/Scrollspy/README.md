# Scrollspy

Índice lateral que destaca a seção visível de uma página longa ou de um painel rolável e rola suavemente até ela ao clicar (`data-ttsc-scrollspy`, ttscui).

## Quando usar

- Páginas de detalhe e configuração com 4+ seções empilhadas (ficha do curso, configurações da unidade, regulamento).
- Drawers `lg` com formulário longo, rolando dentro do corpo do drawer (`target` = corpo).
- **Não use** quando só uma seção deve aparecer por vez: use [Tabs](../Tabs/README.md).
- **Não use** para um único botão “ir para”: use [Scrollto](../Scrollto/README.md).
- Para processos sequenciais com validação por passo use [Stepper](../Stepper/README.md).

## Anatomia

```
┌ nav[data-ttsc-scrollspy] ┐  ┌ #course-body (target, rolável, position: relative) ┐
│ ▌ Visão geral   ← active │  │ <section id="sec-overview">  …                      │
│   Grade curricular       │  │ <section id="sec-curriculum"> …                     │
│   Turmas                 │  │ <section id="sec-classes"> …                        │
│   Financeiro             │  │ <section id="sec-billing"> …                        │
└──────────────────────────┘  └────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Raiz (índice) | `[data-ttsc-scrollspy="true"]` | sim |
| Alvo rolável | `data-ttsc-scrollspy-target="#id"` (padrão `body` = janela) | não |
| Âncora | `a[data-ttsc-scrollspy-anchor][href="#secao"]` | sim |
| Seção | elemento com o `id` do `href` | sim |
| Grupo | `[data-ttsc-scrollspy-group]` — ao ativar um filho, a primeira âncora do grupo também recebe `active` | não |
| Estilo ativo | variantes `ttsc-scrollspy-active:font-medium`, `ttsc-scrollspy-active:text-primary`, `ttsc-scrollspy-active:before:bg-primary` (existem no runtime) ou CSS local | sim |

## Estados

| Estado | Como | Tokens |
|---|---|---|
| Normal | âncora `ttsc-text-muted` | — |
| Hover | `ttsc-text` + fundo `ttsc-canvas-2` | — |
| Ativa | classe `active` (posta pelo JS) | texto `ttsc-accent-text`, barra 2px `ttsc-accent`, fundo `ttsc-accent-soft` |
| Foco | contorno 2px `ttsc-accent` | — |

## API

Conferida em `src/components/scrollspy/scrollspy.ts` (ttscui). Opções por `data-ttsc-scrollspy-<opção>` no elemento raiz, por objeto no construtor ou por `window.ttscGlobalComponentsConfig.scrollspy`.

| Opção | Atributo | Padrão | Descrição |
|---|---|---|---|
| `target` | `data-ttsc-scrollspy-target` | `"body"` | seletor do elemento que rola; `body` escuta `window` |
| `offset` | `data-ttsc-scrollspy-offset` | `0` | px somados ao `scrollTop` antes de comparar com `section.offsetTop` (compensa cabeçalho fixo); `parseInt`, aceita `"80px"` |
| `smooth` | `data-ttsc-scrollspy-smooth` | `true` | rolagem suave ao clicar |
| — | `data-ttsc-scrollspy-anchor-offset` (na âncora) | — | sobrescreve `offset` só para aquela âncora |

| Método | Descrição |
|---|---|
| `ttscScrollspy.getInstance(el)` / `getOrCreateInstance(el, cfg)` | instância |
| `scrollTo(anchorEl)` | rola até a seção da âncora |
| `updateAnchor(anchorEl)` | recalcula uma âncora (use após inserir conteúdo; `update()` do build atual chama a si mesmo — evite) |
| `isActive(anchorEl)` | `true` se a âncora tem `active` |
| `on('activate', fn)` / `off` | callback interno |

| Evento (DOM, no elemento raiz) | `detail.payload` |
|---|---|
| `activate` | `{ element: anchorEl }` — disparado a cada rolagem para a âncora vigente |

Regras do fonte: a seção é comparada por `offsetTop` — o alvo rolável precisa ser o `offsetParent` das seções (`position: relative`). O clique faz `preventDefault()` e usa `scrollTo({ behavior })`, sem alterar o hash.

## Acessibilidade

- Índice em `<nav aria-label="Seções da página">` com lista de links reais (`href="#id"`): funciona sem JS.
- Marque a âncora ativa também com `aria-current="true"` (listener de `activate`, ver JS) — a classe sozinha não é anunciada.
- Cada `<section>` tem `aria-labelledby` apontando para seu `<h2>`; o alvo rolável tem `tabindex="0"` para rolar pelo teclado.
- Ativo em `ttsc-accent-text` (6,9:1 claro), não `text-primary` (`#3ecf8e` = 2:1 sobre branco).
- Respeite `prefers-reduced-motion`: passe `smooth: false`.

## Modelos

### HTML

```html
<!-- resources/views/academic/courses/show.php -->
<div class="grid grid-cols-4 gap-4">
  <nav aria-label="Seções do curso" class="ttsc-spy-nav"
       data-ttsc-scrollspy="true" data-ttsc-scrollspy-target="#course-body" data-ttsc-scrollspy-offset="24">
    <a href="#sec-overview" data-ttsc-scrollspy-anchor class="ttsc-spy-link">Visão geral</a>
    <a href="#sec-curriculum" data-ttsc-scrollspy-anchor class="ttsc-spy-link">
      Grade curricular <span class="ttsc-badge ttsc-badge-sm ttsc-badge-outline"><?= (int) $course['curriculums_count'] ?></span>
    </a>
    <a href="#sec-classes" data-ttsc-scrollspy-anchor class="ttsc-spy-link">
      Turmas <span class="ttsc-badge ttsc-badge-sm ttsc-badge-outline"><?= (int) $course['classes_count'] ?></span>
    </a>
    <a href="#sec-billing" data-ttsc-scrollspy-anchor class="ttsc-spy-link">Financeiro</a>
  </nav>

  <div id="course-body" class="ttsc-spy-body col-span-3" tabindex="0">
    <section id="sec-overview" aria-labelledby="h-overview"><h2 id="h-overview">Visão geral</h2> …</section>
    <section id="sec-curriculum" aria-labelledby="h-curriculum"><h2 id="h-curriculum">Grade curricular</h2> …</section>
    <section id="sec-classes" aria-labelledby="h-classes"><h2 id="h-classes">Turmas</h2> …</section>
    <section id="sec-billing" aria-labelledby="h-billing"><h2 id="h-billing">Financeiro</h2> …</section>
  </div>
</div>
```

### CSS

```css
/* Ponte: as variantes ttsc-scrollspy-active:* leem --primary (= --ttsc-accent). Para TEXTO ativo use o token de texto: */
.ttsc-spy-nav { display: flex; flex-direction: column; gap: 2px; position: sticky; top: var(--ttsc-space-4); }
.ttsc-spy-link {
  position: relative; display: flex; align-items: center; justify-content: space-between;
  padding: 6px 10px 6px 14px; border-radius: var(--ttsc-radius-sm);
  color: var(--ttsc-text-muted); font-size: 13px; text-decoration: none;
}
.ttsc-spy-link:hover { color: var(--ttsc-text); background: var(--ttsc-canvas-2); }
.ttsc-spy-link:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-spy-link.active { color: var(--ttsc-accent-text); background: var(--ttsc-accent-soft); font-weight: 500; }
.ttsc-spy-link.active::before {
  content: ""; position: absolute; inset-inline-start: 4px; top: 6px; bottom: 6px;
  width: 2px; border-radius: var(--ttsc-radius-pill); background: var(--ttsc-accent);
}
.ttsc-spy-body { position: relative; overflow-y: auto; max-height: calc(100vh - var(--ttsc-header-h) - 96px); }
.ttsc-spy-body section + section { margin-top: var(--ttsc-space-8); }
```

### JS

```js
// Inicialização: TTSC.init() cria todas as instâncias [data-ttsc-scrollspy]
TTSC.init();

const nav = document.querySelector('[data-ttsc-scrollspy]');
const spy = ttscScrollspy.getOrCreateInstance(nav, {
  smooth: !matchMedia('(prefers-reduced-motion: reduce)').matches,
});

// aria-current acompanha a classe active
nav.addEventListener('activate', (event) => {
  const anchor = event.detail.payload.element;
  nav.querySelectorAll('[data-ttsc-scrollspy-anchor]').forEach((a) => a.removeAttribute('aria-current'));
  anchor.setAttribute('aria-current', 'true');
});

// Conteúdo carregado depois (ex.: lista de turmas via fetch): recalcule as âncoras
document.addEventListener('ttsc.classes.loaded', () => {
  nav.querySelectorAll('[data-ttsc-scrollspy-anchor]').forEach((a) => spy.updateAnchor(a));
});

// Abrir já na seção pedida pela URL (?section=sec-classes)
const wanted = new URLSearchParams(location.search).get('section');
if (wanted) spy.scrollTo(nav.querySelector(`[href="#${CSS.escape(wanted)}"]`));
```

### SQL

O índice mostra contagens por seção; uma consulta alimenta o cabeçalho e os badges:

```sql
SELECT c.code, c.name, c.description, c.total_hours,
       (SELECT COUNT(*) FROM curriculums cu
         WHERE cu.course_uuid = c.uuid AND cu.deleted_at IS NULL)                          AS curriculums_count,
       (SELECT COUNT(*) FROM classes cl
         WHERE cl.course_uuid = c.uuid AND cl.deleted_at IS NULL AND cl.is_active = 1)      AS classes_count,
       (SELECT COUNT(*) FROM enrollments e
         WHERE e.course_uuid = c.uuid AND e.deleted_at IS NULL AND e.status = 'active')     AS active_enrollments
  FROM courses c
 WHERE c.uuid = :course_uuid
   AND c.deleted_at IS NULL;
```

O controller entrega `$course` à view; seções com contagem zero continuam no índice (com o estado vazio dentro), para a posição das âncoras não mudar entre cursos.

## Faça / Não faça

- **Faça:** `position: relative` no alvo rolável e `offset` igual à altura do que fica fixo no topo.
- **Faça:** rótulos do índice idênticos aos `<h2>` das seções.
- **Não faça:** scrollspy com 2 seções — role normalmente.
- **Não faça:** usar `ttsc-scrollspy-active:text-primary` em fundo claro (2:1).
