# Drawer

Painel lateral do ttscui (`data-ttsc-drawer`) que desliza da borda com backdrop — o formulário padrão do CRUD (criar/editar registro) e a ficha de detalhe, na largura `--ttsc-drawer-md` (560px).

> Também listado em: **Geral › Drawer**.

## Quando usar

- Criar/editar um registro sem sair da listagem: “Nova matrícula”, “Editar turma”, “Lançar ocorrência”.
- Ver detalhes de uma linha (ficha do aluno, histórico de pagamentos) mantendo a tabela visível ao fundo.
- Filtros extensos em telas pequenas (`ttsc-drawer-start`).
- Confirmação curta (“Excluir matrícula?”) → [Modal](../Modal/README.md). Fluxo longo com várias etapas → página própria.
- Menu de poucas ações → [Dropdown](../Dropdown/README.md).

## Anatomia

```
┌──────────── página (backdrop ttsc-scrim, blur 4px) ────┬ .ttsc-drawer.ttsc-drawer-end ─────────┐
│                                                        │ .ttsc-drawer-header                    │
│                                                        │   .ttsc-drawer-title        [x close]  │
│                                                        ├────────────────────────────────────────┤
│                                                        │ .ttsc-drawer-content (rola)            │
│                                                        │   formulário                           │
│                                                        ├────────────────────────────────────────┤
│                                                        │ .ttsc-drawer-footer  [Cancelar][Salvar]│
└────────────────────────────────────────────────────────┴────── width: var(--ttsc-drawer-md) ───┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Painel | `div#id.ttsc-drawer.hidden[data-ttsc-drawer="true"]` (o JS troca `hidden` ↔ `flex` e adiciona `open`) | sim |
| Lado | `ttsc-drawer-end` (direita) · `-start` · `-top` · `-bottom` | sim |
| Largura | `.ttsc-drawer-md` (extensão: `width: var(--ttsc-drawer-md)`) · `-sm` 360 · `-lg` 720 | sim (end/start) |
| Cabeçalho | `.ttsc-drawer-header` > `.ttsc-drawer-title` + `button.ttsc-drawer-close[data-ttsc-drawer-dismiss="true"]` | sim |
| Conteúdo | `.ttsc-drawer-content` (padding 20px, `overflow-y: auto`, cresce) | sim |
| Rodapé | `.ttsc-drawer-footer` (ações; `justify-between`) | formulários |
| Gatilho | qualquer elemento com `data-ttsc-drawer-toggle="#id"` | sim |
| Foco inicial | `[data-ttsc-drawer-focus]` no primeiro campo | recomendado |

## Variantes

| Variante | Configuração | Uso | Tokens |
|---|---|---|---|
| Formulário do CRUD | `ttsc-drawer-end ttsc-drawer-md` | criar/editar | fundo `--popover` (= `ttsc-surface`), sombra lg, bordas `ttsc-border` |
| Detalhe largo | `ttsc-drawer-lg` | ficha do aluno com abas | `--ttsc-drawer-lg` 720px |
| Filtros | `ttsc-drawer-start ttsc-drawer-sm` | filtros em mobile | `--ttsc-drawer-sm` 360px |
| Backdrop estático | `data-ttsc-drawer-backdrop-static="true"` | formulário com dados não salvos | clique no backdrop não fecha |
| Sem backdrop / persistente | `data-ttsc-drawer-backdrop="false"` + `data-ttsc-drawer-persistent="true"` | painel auxiliar que convive com a página | clique fora não fecha |

Backdrop: `.ttsc-drawer-backdrop` (preto 30% + blur 4px no runtime; extensão usa `ttsc-scrim`).

## API

Opções (`data-ttsc-drawer-<opção>` no painel):

| Opção | Padrão | Efeito |
|---|---|---|
| `backdrop` | `true` | cria `[data-ttsc-drawer-backdrop]` irmão do painel |
| `backdropStatic` | `false` | clique no backdrop não fecha |
| `backdropClass` | `ttsc-drawer-backdrop` | classe do backdrop |
| `persistent` | `false` | sem backdrop, clique fora não fecha |
| `disableScroll` | `true` | `overflow: hidden` no `body` enquanto aberto |
| `focus` | `true` | foca `[data-ttsc-drawer-focus]` ao abrir |
| `zindex` | `100` | z-index do painel (backdrop = −1) — no chassi use `1050` (`--ttsc-z-drawer`) |
| `container` | `""` | `"body"` move o painel para o `body` (evita `overflow` do pai); ou um seletor |
| `keepInPlaceWithin` | `""` | seletores em que o painel **não** é movido para o body |
| `class` / `enable` | `""` / `true` | classe aplicada enquanto habilitado (responsivo) |
| `shownClass` / `hiddenClass` | `flex` / `hidden` | classes de exibição |
| `keyboard` | `true` | declarado, mas o `Esc` fecha sempre no runtime atual |

Atributos de ação: `data-ttsc-drawer-toggle="#id"` (abre/fecha; aguarda até 5 s o painel existir — útil para HTML via AJAX), `data-ttsc-drawer-dismiss="true"` (fecha o drawer ancestral), `data-ttsc-drawer-hide` (fecha, delegado no painel).

Métodos (`ttscDrawer.getInstance(el)` / `TTSC.Drawer.getOrCreateInstance(el)`): `show(relatedTarget?)`, `hide()`, `toggle()`, `isOpen()`, `isEnabled()`, `update()`, `getRelatedTarget()` (o botão que abriu), estáticos `ttscDrawer.hide()` (fecha todos) e `ttscDrawer.reinit()`.

Eventos (CustomEvent no painel, `bubbles`): `toggle`, `show` (cancelável), `shown`, `hide` (cancelável), `hidden`.

## Acessibilidade

- O JS aplica `role="dialog"`, `aria-modal="true"` e `tabindex="-1"` ao abrir; adicione `aria-labelledby` apontando para o `.ttsc-drawer-title`.
- `Esc` fecha; o foco vai para `[data-ttsc-drawer-focus]`. Ao fechar, devolva o foco a `getRelatedTarget()` (modelo JS) — o runtime não faz isso.
- O botão fechar é `<button>` com `aria-label="Fechar"`; “Cancelar” no rodapé repete a saída.
- Mantenha o foco dentro do painel (trap) em formulários: o modelo JS faz o ciclo de `Tab`.
- Título `ttsc-text`, rótulos `ttsc-text-2`, ajuda `ttsc-text-muted`; erros `ttsc-danger-text`.

## Modelos

### HTML

```html
<button type="button" class="ttsc-btn ttsc-btn-primary" data-ttsc-drawer-toggle="#drawer-matricula">
  <i class="fa-light fa-plus"></i> Nova matrícula
</button>

<div class="ttsc-drawer ttsc-drawer-end ttsc-drawer-md hidden" id="drawer-matricula" data-ttsc-drawer="true"
     data-ttsc-drawer-container="body" data-ttsc-drawer-zindex="1050" data-ttsc-drawer-backdrop-static="true"
     aria-labelledby="drawer-matricula-title">
  <div class="ttsc-drawer-header">
    <div>
      <h3 class="ttsc-drawer-title" id="drawer-matricula-title"><?= $record ? 'Editar matrícula' : 'Nova matrícula' ?></h3>
      <p class="ttsc-drawer-subtitle">Unidade <?= $this->e($unit['name']) ?> · período 2026.2</p>
    </div>
    <button type="button" class="ttsc-drawer-close" data-ttsc-drawer-dismiss="true" aria-label="Fechar"><i class="fa-light fa-xmark"></i></button>
  </div>
  <form class="ttsc-drawer-content" id="form-matricula" method="post" action="/academic/enrollments<?= $record ? '/' . $this->e($record['uuid']) : '' ?>" data-ttsc-crud>
    <input type="hidden" name="_token" value="<?= $this->e($csrf) ?>">
    <div class="ttsc-form-item">
      <label class="ttsc-form-label" for="f-aluno">Aluno</label>
      <input class="ttsc-input" id="f-aluno" name="student_uuid" required data-ttsc-drawer-focus>
    </div>
    <div class="ttsc-form-item">
      <label class="ttsc-form-label" for="f-turma">Turma</label>
      <select class="ttsc-select" id="f-turma" name="class_uuid">
        <?php foreach ($classes as $c): ?>
        <option value="<?= $this->e($c['uuid']) ?>" <?= $c['enrolled'] >= $c['max_students'] ? 'disabled' : '' ?>>
          <?= $this->e($c['name']) ?> — <?= (int) $c['enrolled'] ?>/<?= (int) $c['max_students'] ?> vagas
        </option>
        <?php endforeach; ?>
      </select>
    </div>
  </form>
  <div class="ttsc-drawer-footer">
    <button type="button" class="ttsc-btn ttsc-btn-ghost" data-ttsc-drawer-dismiss="true">Cancelar</button>
    <button type="submit" form="form-matricula" class="ttsc-btn ttsc-btn-primary"><i class="fa-light fa-floppy-disk"></i> Salvar</button>
  </div>
</div>
```

### CSS

```css
/* Ponte (bundle.css): painel lê --popover; backdrop em ttsc-scrim */
:root { --popover: var(--ttsc-surface); --popover-foreground: var(--ttsc-text); }
.ttsc-drawer-backdrop { background-color: var(--ttsc-scrim); }

/* Extensão TTSC: larguras do chassi e cabeçalho com subtítulo */
.ttsc-drawer-sm { width: var(--ttsc-drawer-sm); }
.ttsc-drawer-md { width: var(--ttsc-drawer-md); }
.ttsc-drawer-lg { width: var(--ttsc-drawer-lg); }
.ttsc-drawer { box-shadow: var(--ttsc-shadow-xl); }
.ttsc-drawer-header { padding: var(--ttsc-space-4) var(--ttsc-space-5); align-items: flex-start; }
.ttsc-drawer-title { font-size: 15px; color: var(--ttsc-text); }
.ttsc-drawer-subtitle { margin-top: 2px; font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-drawer-content { display: flex; flex-direction: column; gap: var(--ttsc-space-4); }
.ttsc-drawer-footer { padding: var(--ttsc-space-3) var(--ttsc-space-5); background: var(--ttsc-canvas); }
.ttsc-drawer-close { color: var(--ttsc-text-muted); background: none; border: 0; }
@media (max-width: 640px) { .ttsc-drawer-md, .ttsc-drawer-lg { width: 100%; max-width: 100%; } }
```

### JS

```js
// assets/js/core/ttsc.drawer-form.js — drawer de formulário do CRUD
const drawerEl = document.querySelector('#drawer-matricula');
const drawer = TTSC.Drawer.getOrCreateInstance(drawerEl);
const form = drawerEl.querySelector('form');

// Avisa antes de fechar com alterações não salvas
form.addEventListener('input', () => { form.dataset.dirty = 'true'; });
drawerEl.addEventListener('hide', (event) => {
  if (form.dataset.dirty === 'true' && !confirm('Descartar as alterações desta matrícula?')) {
    event.detail.payload.cancel = true;
  }
});

// Devolve o foco ao botão que abriu e limpa o formulário
drawerEl.addEventListener('hidden', () => {
  drawer.getRelatedTarget()?.focus();
  form.reset();
  delete form.dataset.dirty;
});

// Trap de foco (Tab / Shift+Tab ficam dentro do painel)
drawerEl.addEventListener('keydown', (event) => {
  if (event.key !== 'Tab') return;
  const f = [...drawerEl.querySelectorAll('a[href], button:not([disabled]), input:not([type=hidden]), select, textarea')];
  const first = f[0], last = f[f.length - 1];
  if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
  else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
});

// Envio via fetch; fecha e recarrega a tabela ao salvar
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
  if (!res.ok) return; // erros de validação: renderize .ttsc-form-message nos campos
  delete form.dataset.dirty;
  drawer.hide();
  ttscDataTable.getInstance(document.querySelector('#dt-matriculas'))?.reload();
});

// Editar a partir da linha: carrega o parcial Plates e abre
document.addEventListener('click', async (event) => {
  const btn = event.target.closest('[data-edit-enrollment]');
  if (!btn) return;
  const html = await (await fetch(`/academic/enrollments/${btn.dataset.editEnrollment}/form`)).text();
  drawerEl.querySelector('.ttsc-drawer-content').outerHTML = html;
  drawer.show(btn);
});
```

### SQL

```sql
-- Opções de turma do curso com vagas (select do formulário)
SELECT cl.uuid, cl.name, cl.shift, cl.max_students, COUNT(e.id) AS enrolled
  FROM classes cl
  LEFT JOIN enrollments e
         ON e.class_uuid = cl.uuid AND e.status = 'active' AND e.deleted_at IS NULL
 WHERE cl.unit_uuid = :unit_uuid
   AND cl.course_uuid = :course_uuid
   AND cl.is_active = 1
   AND cl.deleted_at IS NULL
 GROUP BY cl.uuid, cl.name, cl.shift, cl.max_students
 ORDER BY cl.name;

-- Gravação (POST do drawer; DomainCrudController gera uuid e code)
INSERT INTO enrollments (uuid, code, student_uuid, course_uuid, class_uuid, period_uuid,
                         type, status, enrollment_date, shift, modality, unit_uuid, notes)
VALUES (:uuid, :code, :student_uuid, :course_uuid, :class_uuid, :period_uuid,
        'regular', 'active', :enrollment_date, :shift, :modality, :unit_uuid, :notes);
```

Para editar, o controller carrega `SELECT … FROM enrollments WHERE uuid = :uuid AND unit_uuid = :unit_uuid AND deleted_at IS NULL`, passa `$record` e `$classes` para o parcial do drawer e faz `UPDATE … SET … WHERE uuid = :uuid` no POST (mesma checagem de `_token` e permissão de escrita).

## Faça / Não faça

- **Faça:** `ttsc-drawer-md` (560px) para formulários do CRUD; `-lg` só para fichas com abas.
- **Faça:** `backdrop-static` em formulários, para um clique fora não perder dados.
- **Faça:** `container="body"` quando o drawer nasce dentro de cards/tabelas com `overflow`.
- **Não faça:** drawer sobre drawer; abra o segundo nível como página ou substitua o conteúdo.
- **Não faça:** confirmação de exclusão em drawer (use [Modal](../Modal/README.md)).
