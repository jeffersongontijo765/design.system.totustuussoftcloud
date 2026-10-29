# Reparent

Move um bloco de marcação para outro container (`prepend` ou `append`) via `data-ttsc-reparent`, reavaliando no redimensionamento — usado para levar filtros, ações e menus da toolbar desktop para o drawer mobile sem duplicar HTML.

## Quando usar

- O mesmo bloco precisa morar em lugares diferentes conforme o viewport: filtros da listagem (toolbar no desktop → drawer de filtros no mobile), ações do cabeçalho de página (header → rodapé fixo), seletor de unidade (topbar → sub-sidebar).
- Evita duplicar formulários (dois `<select name="course_uuid">` no mesmo `<form>` enviariam o campo duas vezes).
- **Não use** para mostrar/esconder conteúdo — use classes responsivas (`hidden lg:flex`) ou [Toggle](../Toggle/README.md).
- **Não use** para abrir painéis: isso é [Drawer](../Drawer/README.md) ou Modal. Reparent só troca o pai do nó.

## Anatomia

```
#slot-toolbar (desktop)                 #slot-mobile (drawer)
  └ [data-ttsc-reparent] ── resize ──▶    └ [data-ttsc-reparent]  (mesmo nó, listeners preservados)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Bloco móvel | `[data-ttsc-reparent="true"]` | sim |
| Destino | `data-ttsc-reparent-target="#seletor"` (ou `--ttsc-reparent-target` em CSS) | sim |
| Modo | `data-ttsc-reparent-mode="prepend\|append"` (ou `--ttsc-reparent-mode`) | sim |
| Containers | dois elementos com `id`, ambos presentes no DOM | sim |

## Variantes

| Variante | Como | Uso |
|---|---|---|
| Fixa | só atributos `data-ttsc-reparent-*` | mover uma vez no load (ex.: injetar ações do módulo no header do chassi) |
| Responsiva | atributos = posição desktop; `@media` redefine `--ttsc-reparent-target`/`--ttsc-reparent-mode` | toolbar ↔ drawer |
| Programática | `TTSC.Reparent.getInstance(el).update()` depois de trocar uma classe | quando o gatilho não é resize (troca de aba, modo foco) |

Tokens: o componente não tem visual próprio; o bloco herda o estilo do container de destino.

## API

O ttscui lê cada opção primeiro da **variável CSS** `--ttsc-reparent-<opção>` do elemento e, se vazia, do atributo — é isso que torna o reparent responsivo.

| Atributo / variável CSS | Padrão | Efeito |
|---|---|---|
| `data-ttsc-reparent` | — | ativa |
| `data-ttsc-reparent-target` / `--ttsc-reparent-target` | `""` | seletor do novo pai (`document.querySelector`) |
| `data-ttsc-reparent-mode` / `--ttsc-reparent-mode` | `""` | `prepend` (primeiro filho) ou `append` (último filho); vazio = não move |

| Método | Efeito |
|---|---|
| `TTSC.Reparent.getInstance(el)` | instância existente (ou `undefined`) |
| `TTSC.Reparent.getOrCreateInstance(el, config)` | cria com config `{ mode, target }` |
| `inst.update()` | reavalia destino/modo e move se o pai mudou |
| `TTSC.Reparent.init()` | cria todas as instâncias e registra o listener de `resize` (throttle 200 ms) uma única vez |

Sem eventos próprios. Observação: a versão atual do ttscui escreve `console.log("reparent update")` a cada resize — inofensivo, mas aparece no console.

## Acessibilidade

- O nó é **movido**, não clonado: `id`, valores e listeners continuam; o foco é perdido se o elemento focado for movido — evite reparent enquanto o usuário digita (o resize em mobile acontece ao abrir o teclado virtual: prefira destino que não mude nesse caso).
- A ordem do DOM define a ordem de tabulação: depois de mover, confirme que o bloco aparece onde o leitor de tela espera (início do drawer = `prepend`).
- Não quebre `<form>`: se o bloco tem campos, os dois destinos devem estar dentro do mesmo formulário ou use o atributo `form="id-do-form"` nos campos.

## Modelos

### HTML

```html
<!-- Listagem de matrículas: filtros na toolbar (desktop) e no drawer (mobile) -->
<div class="flex items-center justify-between gap-2" id="enrollments-toolbar">
  <div id="enrollments-filters"
       class="flex flex-wrap items-center gap-2"
       data-ttsc-reparent="true"
       data-ttsc-reparent-mode="append"
       data-ttsc-reparent-target="#enrollments-toolbar">
    <select class="ttsc-select" name="course_uuid" form="enrollments-filter-form" aria-label="Curso">
      <option value="">Todos os cursos</option>
      <?php foreach ($courses as $c): ?>
      <option value="<?= $e($c['uuid']) ?>"><?= $e($c['name']) ?></option>
      <?php endforeach; ?>
    </select>
    <select class="ttsc-select" name="status" form="enrollments-filter-form" aria-label="Status">
      <option value="active">Ativa</option>
      <option value="locked">Trancada</option>
    </select>
  </div>
  <button type="button" class="ttsc-btn ttsc-btn-outline lg:hidden" data-ttsc-drawer-toggle="#drawer-enrollment-filters">
    <i class="fa-light fa-filter"></i> Filtros
  </button>
</div>

<div class="ttsc-drawer" id="drawer-enrollment-filters" data-ttsc-drawer="true">
  <div class="ttsc-drawer-content" id="enrollments-filters-mobile"><!-- destino mobile --></div>
</div>
```

### CSS

```css
/* Mobile: o mesmo bloco vai para o topo do drawer */
@media (max-width: 1023.98px) {
  #enrollments-filters {
    --ttsc-reparent-target: #enrollments-filters-mobile;
    --ttsc-reparent-mode: prepend;
    flex-direction: column; align-items: stretch;
    gap: var(--ttsc-space-3);
  }
}

/* Extensão útil: destaque breve depois de mover (ajuda a orientar o usuário) */
[data-ttsc-reparent].is-reparented { animation: ttsc-reparent-flash .6s var(--ttsc-ease, ease); }
@keyframes ttsc-reparent-flash { from { box-shadow: 0 0 0 3px var(--ttsc-accent-soft); } to { box-shadow: none; } }
```

### JS

```js
// TTSC.init() já cria as instâncias e registra o resize. Para gatilhos que não são resize:
var filters = document.getElementById('enrollments-filters');
var reparent = TTSC.Reparent.getOrCreateInstance(filters);

function moveAndFlag() {
  var before = filters.parentElement;
  reparent.update();
  if (filters.parentElement !== before) {
    filters.classList.add('is-reparented');
    setTimeout(function () { filters.classList.remove('is-reparented'); }, 600);
  }
}

// Ex.: modo "tela cheia" da tabela leva os filtros para a barra flutuante
document.getElementById('btn-table-fullscreen').addEventListener('click', function () {
  document.body.classList.toggle('table-fullscreen');
  filters.style.setProperty('--ttsc-reparent-target',
    document.body.classList.contains('table-fullscreen') ? '#floating-toolbar' : '');
  moveAndFlag();
});

// Mudança de breakpoint sem esperar o throttle do resize
window.matchMedia('(max-width: 1023.98px)').addEventListener('change', moveAndFlag);
```

### SQL

Reparent não persiste nada; ele move os filtros cuja lista vem do banco. Contagem por status para os rótulos (“Ativa (128)”):

```sql
SELECT e.status, COUNT(*) AS total
  FROM enrollments e
 WHERE e.unit_uuid = :unit_uuid
   AND e.deleted_at IS NULL
 GROUP BY e.status
 ORDER BY total DESC;
```

O controller passa `$statusCounts` para a view, que monta os `<option>` uma única vez — o reparent garante que esse mesmo HTML sirva desktop e mobile.

## Faça / Não faça

- **Faça:** declare a posição desktop nos atributos e a mobile por `@media` com `--ttsc-reparent-*`.
- **Faça:** mantenha campos movidos ligados ao formulário (`form="…"`).
- **Não faça:** duplicar o bloco com `hidden`/`lg:hidden` — campos duplicados vão no POST.
- **Não faça:** mover elementos enquanto têm foco ou durante animação de drawer.
