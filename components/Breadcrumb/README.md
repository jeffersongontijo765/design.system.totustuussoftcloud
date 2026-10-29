# Breadcrumb

Trilha de navegação hierárquica do chassi (`.ttsc-breadcrumb`): unidade › módulo › registro, com separador decorativo em `ttsc-meta` e item atual marcado com `aria-current="page"`.

> Também listado em: **Base › Breadcrumb**.

## Quando usar

- No [PageHeader](../PageHeader/README.md) de toda página com profundidade ≥ 2 (ex.: Acadêmico › Cursos › Administração › Turma ADM-2026-1N).
- Em drawers de detalhe que abrem um registro filho, para mostrar de onde o usuário veio.
- **Não use** para etapas de um processo (dados → turma → financeiro): use [Stepper](../Stepper/README.md).
- **Não use** para alternar visões da mesma página: use [Tabs](../Tabs/README.md) ou [SegmentedTabs](../SegmentedTabs/README.md).

## Anatomia

```
[ícone] Acadêmico  ›  Cursos  ›  …  ›  Administração  ›  Turma ADM-2026-1N
  link            sep   link   ellipsis    link        sep   página atual
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Landmark | `<nav aria-label="Trilha de navegação">` | sim |
| Lista | `ol.ttsc-breadcrumb` | sim |
| Item | `li.ttsc-breadcrumb-item` | sim |
| Link | `a.ttsc-breadcrumb-link` | sim (exceto o último) |
| Separador | `li.ttsc-breadcrumb-separator` + `aria-hidden="true"` + `<i class="fa-light fa-chevron-right">` em `ttsc-meta` | sim |
| Página atual | `span.ttsc-breadcrumb-page` + `aria-current="page"` | sim |
| Reticências | `button.ttsc-breadcrumb-ellipsis` + `aria-label` + `aria-expanded` | não (trilhas com 5+ níveis) |

## Variantes

| Variante | Como | Tokens |
|---|---|---|
| Padrão | `ttsc-breadcrumb` (13px, gap 6px) | links `ttsc-text-muted` (4,9:1 claro), hover e atual `ttsc-text` |
| Com ícone inicial | `<i class="fa-light fa-house">` dentro do primeiro link | herda a cor do link |
| Separador barra | `<span>/</span>` no lugar do chevron | `ttsc-meta` (decorativo) |
| Recolhida | itens do meio com `hidden` + botão `ttsc-breadcrumb-ellipsis` | botão `ttsc-text-muted`, hover `ttsc-canvas-2` |
| Compacta | `.ttsc-breadcrumb.text-xs` em drawers | — |

## Estados

| Estado | Como aplicar |
|---|---|
| Hover do link | automático — cor `--foreground` (`ttsc-text`) |
| Foco | contorno 2px `ttsc-accent` (extensão CSS abaixo) |
| Atual | `span.ttsc-breadcrumb-page[aria-current="page"]` — não é link |
| Expandida | clique no `ttsc-breadcrumb-ellipsis` remove `hidden` dos itens recolhidos e o próprio botão some |

## API

Sem JavaScript no ttscui; o breadcrumb é marcação + CSS do runtime. A única interação (expandir reticências) é a implementação TTSC abaixo:

| Atributo | Elemento | Efeito |
|---|---|---|
| `data-ttsc-breadcrumb-collapsed` | `li` recolhido | escondido (`hidden`) até expandir |
| `data-ttsc-breadcrumb-expand` | `button.ttsc-breadcrumb-ellipsis` | mostra os itens recolhidos e dispara `ttsc.breadcrumb.expand` |

| Evento | Alvo | `detail` |
|---|---|---|
| `ttsc.breadcrumb.expand` | `ol.ttsc-breadcrumb` | `{ items: HTMLElement[] }` |

## Acessibilidade

- `<nav aria-label="Trilha de navegação">` cria o landmark; use `<ol>` (a ordem importa).
- Separadores são `aria-hidden="true"` — o leitor de tela anuncia só “link, Cursos”.
- O último item é texto com `aria-current="page"`, nunca link para a própria página.
- Contraste: links em `ttsc-text-muted` (4,9:1 claro / 5,6:1 escuro sobre `ttsc-surface`); o separador usa `ttsc-meta` (1,9:1) e por isso **só** pode ser decorativo.
- Reticências: `<button>` com `aria-label="Mostrar níveis ocultos"` e `aria-expanded`.

## Modelos

### HTML

```html
<!-- resources/views/academic/classes/show.php — dados vindos de $crumbs (ver SQL) -->
<nav aria-label="Trilha de navegação">
  <ol class="ttsc-breadcrumb">
    <li class="ttsc-breadcrumb-item">
      <a class="ttsc-breadcrumb-link" href="/academic/dashboard"><i class="fa-light fa-graduation-cap"></i> Acadêmico</a>
    </li>
    <li class="ttsc-breadcrumb-separator" aria-hidden="true"><i class="fa-light fa-chevron-right"></i></li>
    <li class="ttsc-breadcrumb-item">
      <a class="ttsc-breadcrumb-link" href="/academic/courses">Cursos</a>
    </li>
    <li class="ttsc-breadcrumb-separator" aria-hidden="true"><i class="fa-light fa-chevron-right"></i></li>
    <li class="ttsc-breadcrumb-item">
      <a class="ttsc-breadcrumb-link" href="/academic/courses/<?= $this->e($crumbs['course_uuid']) ?>"><?= $this->e($crumbs['course_name']) ?></a>
    </li>
    <li class="ttsc-breadcrumb-separator" aria-hidden="true"><i class="fa-light fa-chevron-right"></i></li>
    <li class="ttsc-breadcrumb-item">
      <span class="ttsc-breadcrumb-page" aria-current="page">Turma <?= $this->e($crumbs['class_label']) ?></span>
    </li>
  </ol>
</nav>

<!-- Trilha longa recolhida -->
<nav aria-label="Trilha de navegação">
  <ol class="ttsc-breadcrumb">
    <li class="ttsc-breadcrumb-item"><a class="ttsc-breadcrumb-link" href="/academic/dashboard">Acadêmico</a></li>
    <li class="ttsc-breadcrumb-separator" aria-hidden="true"><i class="fa-light fa-chevron-right"></i></li>
    <li class="ttsc-breadcrumb-item">
      <button type="button" class="ttsc-breadcrumb-ellipsis" data-ttsc-breadcrumb-expand aria-label="Mostrar níveis ocultos" aria-expanded="false">
        <i class="fa-light fa-ellipsis"></i>
      </button>
    </li>
    <li class="ttsc-breadcrumb-item hidden" data-ttsc-breadcrumb-collapsed><a class="ttsc-breadcrumb-link" href="/academic/courses">Cursos</a></li>
    <li class="ttsc-breadcrumb-separator hidden" data-ttsc-breadcrumb-collapsed aria-hidden="true"><i class="fa-light fa-chevron-right"></i></li>
    <li class="ttsc-breadcrumb-item hidden" data-ttsc-breadcrumb-collapsed><a class="ttsc-breadcrumb-link" href="/academic/courses/adm">Administração</a></li>
    <li class="ttsc-breadcrumb-separator" aria-hidden="true"><i class="fa-light fa-chevron-right"></i></li>
    <li class="ttsc-breadcrumb-item"><span class="ttsc-breadcrumb-page" aria-current="page">Diário de classe</span></li>
  </ol>
</nav>
```

### CSS

```css
/* Ponte (bundle.css): links leem --muted-foreground, a página atual lê --foreground */
:root {
  --muted-foreground: var(--ttsc-text-muted);
  --foreground: var(--ttsc-text);
}

/* Extensões do chassi: separador decorativo, foco visível e reticências */
.ttsc-breadcrumb-separator { color: var(--ttsc-meta); font-size: 10px; display: inline-flex; }
.ttsc-breadcrumb .hidden { display: none; }
.ttsc-breadcrumb-link { border-radius: var(--ttsc-radius-xs); }
.ttsc-breadcrumb-link:focus-visible,
.ttsc-breadcrumb-ellipsis:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-breadcrumb-ellipsis {
  display: inline-flex; align-items: center; justify-content: center;
  width: 24px; height: 24px; border: 0; background: transparent; cursor: pointer;
  color: var(--ttsc-text-muted); border-radius: var(--ttsc-radius-xs);
}
.ttsc-breadcrumb-ellipsis:hover { background: var(--ttsc-canvas-2); color: var(--ttsc-text); }
.ttsc-breadcrumb-page { font-weight: 500; max-width: 32ch; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
```

### JS

```js
// assets/js/core/ttsc.breadcrumb.js — implementação TTSC: expande trilhas recolhidas
export function initBreadcrumbs(root = document) {
  root.querySelectorAll('[data-ttsc-breadcrumb-expand]').forEach((button) => {
    if (button.dataset.ttscBreadcrumbReady) return;
    button.dataset.ttscBreadcrumbReady = 'true';
    button.addEventListener('click', () => {
      const list = button.closest('.ttsc-breadcrumb');
      const items = [...list.querySelectorAll('[data-ttsc-breadcrumb-collapsed]')];
      items.forEach((item) => item.classList.remove('hidden'));
      button.setAttribute('aria-expanded', 'true');
      button.closest('.ttsc-breadcrumb-item').classList.add('hidden');
      items.find((i) => i.querySelector('a'))?.querySelector('a').focus();
      list.dispatchEvent(new CustomEvent('ttsc.breadcrumb.expand', { bubbles: true, detail: { items } }));
    });
  });
}

document.addEventListener('DOMContentLoaded', () => initBreadcrumbs());
```

### SQL

A trilha de uma turma resolve unidade, curso e turma numa consulta só (MariaDB 10.11 / MySQL 8):

```sql
SELECT u.name                       AS unit_name,
       c.uuid                       AS course_uuid,
       c.name                       AS course_name,
       cl.code                      AS class_code,
       COALESCE(cl.name, cl.code)   AS class_label
  FROM classes cl
  JOIN courses c ON c.uuid = cl.course_uuid AND c.deleted_at IS NULL
  JOIN units   u ON u.uuid = cl.unit_uuid
 WHERE cl.uuid = :class_uuid
   AND cl.deleted_at IS NULL;
```

O controller passa a linha como `$crumbs` para a view; sem linha (turma excluída) responde 404 em vez de renderizar uma trilha parcial. Os rótulos fixos (“Acadêmico”, “Cursos”) vêm do catálogo de i18n, não do banco.

## Faça / Não faça

- **Faça:** último item como texto com `aria-current="page"`; separadores `aria-hidden`.
- **Faça:** recolher os níveis do meio quando a trilha passar de 4 itens ou quebrar linha.
- **Não faça:** usar `ttsc-meta` para texto (1,9:1); só para o separador.
- **Não faça:** breadcrumb como substituto do menu lateral ou de abas.
