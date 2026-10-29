# Select2

Select com busca, seleção múltipla, criação de tags e carregamento remoto (Select2 4.1.0-rc.0 + jQuery 3.7.1), com textos pt-BR e tema por tokens nos dois temas.

## Quando usar

- Listas longas que precisam de busca: curso, turma, unidade, responsável financeiro.
- Busca no servidor (AJAX) quando a lista não cabe na página: aluno por nome, CPF ou matrícula.
- Seleção múltipla compacta (turnos, modalidades) e tags livres simples.
- **Não use** para menos de ~8 opções sem busca: use o [Select](../Select/README.md) do ttscui (sem jQuery).
- Para dois níveis com muitas opções (curso → disciplinas) use [MultiSelectSplitter](../MultiSelectSplitter/README.md); para etiquetas com cores e whitelist rica use [Tagify](../Tagify/README.md).

## Anatomia

```
Curso
[ Administração                    × ▾ ]   .select2-selection--single
┌─────────────────────────────────────┐
│ [ busca                           ] │    .select2-search--dropdown
│ GRADUAÇÃO                           │    .select2-results__group (optgroup)
│ ▌Administração                      │    --highlighted / --selected
│  Enfermagem (sem vagas)             │    --disabled
└─────────────────────────────────────┘    .select2-dropdown (anexado ao body)
Turnos  [ × Manhã ][ × Noite ] ______      .select2-selection--multiple / __choice
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Origem | `<select>` com `name`, `<label for>`, `data-placeholder` (+ `<option></option>` vazia para placeholder no single) | sim |
| Seleção | `.select2-selection--single` / `--multiple` | gerado |
| Chip | `.select2-selection__choice` + `__choice__remove` | gerado |
| Dropdown | `.select2-dropdown` (no `body` ou em `dropdownParent`) | gerado |
| Opção | `.select2-results__option` (`--highlighted`, `--selected`, `--disabled`) | gerado |

## Variantes

| Variante | Opções | Tokens |
|---|---|---|
| Single com busca | `placeholder`, `allowClear: true` | campo `ttsc-surface`/`ttsc-border`, foco `ttsc-accent` + halo `ttsc-accent-soft` |
| Multiple | `multiple` no select, `closeOnSelect: false` | chips `ttsc-surface-2`, texto `ttsc-text` |
| Tags | `tags: true`, `tokenSeparators: [',']` | idem |
| AJAX | `ajax: { url, delay, data, processResults }`, `minimumInputLength: 2` | linha secundária `ttsc-text-muted` |
| Dentro de drawer/modal | `dropdownParent: $('#drawer-id')` | z-index do container |

## Features

Categorias seguem a documentação do ktui (Select). Todas as opções citadas são do Select2 4.1 (`$.fn.select2`); o que o DS acrescenta está indicado em cada seção.

### Basic Usage

`<select>` com `data-ttsc-select2` e `<label for>`. A inicialização está no `initSelect2()` do bloco [JS](#js).

```html
<label class="ttsc-form-label" for="enr-course">Curso</label>
<select id="enr-course" name="course_uuid" data-ttsc-select2 data-placeholder="Selecione o curso">
  <option></option>
  <option value="adm">Administração</option>
  <option value="enf">Enfermagem</option>
</select>
```

### Placeholder Text

`data-placeholder` no `<select>`. No modo single, a primeira `<option></option>` vazia é obrigatória para o placeholder aparecer.

### Disabled Select

`disabled` no `<select>`: o Select2 desabilita o campo inteiro. Alternar a propriedade por JS também atualiza o campo.

### Disabled Option

`<option value="x" disabled>`: o resultado aparece desabilitado (`.select2-results__option--disabled`) e não pode ser escolhido.

### Size Variants

O Select2 não tem variantes de tamanho. O DS fixa `min-height: 34px` no campo. Para outro tamanho, crie uma classe e passe em `containerCssClass`:

```css
.s2-sm .select2-container--default .select2-selection--single { min-height: 28px; }
.s2-sm .select2-container--default .select2-selection__rendered { line-height: 26px; }
```

```js
$(el).select2({ containerCssClass: 's2-sm' });
```

### Multiple Selection

`multiple` no `<select>` (use `name="campo[]"`) e `closeOnSelect: false` para o painel continuar aberto. Cada escolha vira um chip.

### Maximum Selection

`maximumSelectionLength: 3` limita quantas opções podem ser escolhidas. Ao atingir o limite, aparece a mensagem “Você só pode selecionar 3 itens” (texto em pt-BR no bloco [JS](#js)).

```js
$(el).select2({ multiple: true, closeOnSelect: false, maximumSelectionLength: 3 });
```

### Enhanced Tags

`tags: true` cria uma opção nova quando o texto digitado não existe. `tokenSeparators: [',']` transforma a vírgula em separador. Para criar só valores válidos, use `createTag` retornando `null` em casos inválidos.

```js
$(el).select2({
  tags: true,
  tokenSeparators: [','],
  createTag: (p) => (p.term.trim().length >= 2 ? { id: p.term.trim(), text: p.term.trim(), newTag: true } : null),
});
```

Valores criados pelo usuário devem ser validados no servidor antes de gravar.

### Tags with Icons

`templateSelection` monta o chip com ícone. Use `.text()` para o rótulo, nunca concatenação de HTML:

```js
templateSelection: (s) => (s.element ? $('<span>').append($('<i>').addClass($(s.element).data('icon')), ' ', document.createTextNode(s.text)) : s.text),
```

### Basic Tags

`tags: true` sem mais nada: o texto digitado aparece como opção nova, e o chip fica no campo depois de escolhê-lo. O campo `<select multiple>` mantém as escolhas como `<option>` selecionadas.

### Pre-selected Tags

Valor inicial com `<option selected>` (ou `.val([...]).trigger('change')`). Para valores vindos do AJAX, crie a opção e marque-a:

```js
const opt = new Option(aluno.text, aluno.id, true, true);
$(el).append(opt).trigger('change');
```

### Tags: selected count

Conte as escolhas com `$(el).val().length` ou `$(el).select2('data').length`. Para mostrar um contador ao lado do campo, atualize-o no evento `select2:select` e `select2:unselect`.

### Search & Filtering

Busca local por padrão. `minimumResultsForSearch: Infinity` esconde a busca em listas curtas. Para filtro próprio (por exemplo, ignorar acentos), passe `matcher`:

```js
matcher: (params, data) => {
  if (!params.term || !data.text) return data;
  const norm = (t) => t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  return norm(data.text).includes(norm(params.term)) ? data : null;
},
```

### Search

Com `minimumResultsForSearch` padrão (0), a busca aparece em qualquer lista.

### Remote Data

`ajax` com `url`, `delay`, `data`, `processResults` e `cache` (ver o bloco [JS](#js) e o [SQL](#sql) do endpoint). O servidor devolve `{ results: [...], pagination: { more: bool } }`, e `minimumInputLength: 2` evita consultas com um caractere.

### Icons

`templateResult` com um ícone do Font Awesome por opção. Lê o `data-icon` da `<option>`:

```js
templateResult: (s) => (s.id ? $('<span>').append($('<i>').addClass($(s.element).data('icon')), ' ', document.createTextNode(s.text)) : s.text),
```

### Multiple Icons

Mesmo `templateResult` com `multiple: true`; o `templateSelection` da seção [Tags with Icons](#tags-with-icons) mostra o ícone em cada chip.

### Avatar

`templateResult` com uma imagem circular e iniciais quando não houver foto. Use `.attr('src', url)` (nunca `src` montado com HTML):

```js
templateResult: (s) => {
  if (!s.id) return s.text;
  const img = s.avatar ? $('<img class="s2-avatar">').attr('src', s.avatar).attr('alt', '') : $('<span class="s2-avatar s2-initials">').text(s.initials || '?');
  return $('<span class="s2-row">').append(img, document.createTextNode(s.text));
},
```

Estilos `.s2-avatar`, `.s2-initials` e `.s2-row` ficam na extensão CSS do bloco [CSS](#css).

### Country Selection

Monte a bandeira com o código do país em `data-flag` na `<option>` (por exemplo, `data-flag="🇧🇷"`) e mostre-a no `templateResult`. O DS não traz lista de países: o servidor ou um JSON local fornece as opções.

### Description

`templateResult` com uma segunda linha em `.s2-meta`, que já existe no CSS do bloco [CSS](#css):

```js
templateResult: (s) => (s.id ? $('<span>').text(s.text).append($('<span class="s2-meta">').text(s.description || '')) : s.text),
```

### Modal Integration

Em drawers e modais use `dropdownParent` com o container aberto, como no bloco [JS](#js). Sem isso, o dropdown fica atrás da camada do modal.

### Template Customization

`templateResult` (lista), `templateSelection` (campo fechado), `escapeMarkup` (padrão escapa HTML). Mantenha `escapeMarkup` ligado: os textos vêm do banco.

## API Reference

Opções principais: `placeholder`, `allowClear`, `multiple`, `tags`, `tokenSeparators`, `createTag`, `maximumSelectionLength`, `minimumInputLength`, `minimumResultsForSearch` (`Infinity` esconde a busca), `closeOnSelect`, `dropdownParent`, `containerCssClass`, `dropdownCssClass`, `width` (`'100%'`), `language` (objeto pt-BR do bloco [JS](#js)), `matcher`, `templateResult`, `templateSelection`, `escapeMarkup`, `data`, `ajax` (`url`, `delay`, `data(params)`, `processResults(data, params)`, `transport(params, success, failure)`, `cache`).

Formato de resultados do AJAX: `{ results: [{ id, text, disabled?, children? }], pagination: { more: bool } }`.

### Data Attributes

| Atributo | Onde | Efeito |
|---|---|---|
| `data-ttsc-select2` | `<select>` | inicializa com as opções padrão do DS (`initSelect2()`) |
| `data-placeholder` | `<select>` | texto do campo sem seleção |
| `data-ttsc-select2-ajax="/url"` | `<select>` | inicializa com busca remota (`ajax`) |
| `data-icon`, `data-flag`, `data-description` | `<option>` | dados lidos pelos templates (não são do Select2) |

### Template Configuration

`templateResult`, `templateSelection`, `escapeMarkup`, `containerCssClass` e `dropdownCssClass`. Os exemplos das seções acima mostram cada um.

### Option Data

Os `data-*` da `<option>` ficam acessíveis em `s.element` e `$(s.element).data('nome')`. Em `ajax`, os campos do resultado (`id`, `text` e os extras que você devolver) aparecem em `s` e nos templates.

### Events

Eventos jQuery: `select2:open`, `select2:close`, `select2:opening`, `select2:closing`, `select2:select` (`e.params.data`), `select2:unselect`, `select2:clear`, `select2:clearing`. O `change` nativo do `<select>` também é disparado.

### Programmatic selection

```js
$(el).val('adm').trigger('change');          // escolhe um valor existente
$(el).val(['adm', 'enf']).trigger('change'); // múltiplo
```

### Reading the current selection

```js
$(el).val();                  // valor (ou array no múltiplo)
$(el).select2('data');        // objetos completos: [{ id, text, element, ... }]
```

### Search Autofocus

Não há opção de foco: por padrão o Select2 leva o foco ao campo de busca quando ele está visível. Se o foco não for para lá, force-o com o evento de abertura:

```js
$(el).on('select2:open', () => {
  document.querySelector('.select2-container--open .select2-search__field')?.focus();
});
```

### Enter Key Behavior

Padrão do Select2: Enter ou Espaço abrem o campo; na lista, Enter escolhe a opção destacada; `Esc` fecha; `Backspace` remove o último chip no múltiplo. Em `tags: true`, Enter também cria a tag digitada.

### Global Dropdown Management

Para fechar todos os dropdowns abertos: `$('select[data-ttsc-select2]').select2('close')`. Um dropdown por vez é o comportamento padrão do Select2.

### TypeScript

O DS não traz tipos do jQuery nem do Select2. Com TypeScript, instale `@types/jquery` e `@types/select2` e use os tipos deles; `$(el).select2(...)` aceita as opções acima.

## Acessibilidade

- O Select2 aplica `role="combobox"`, `aria-expanded`, `aria-controls`, `aria-activedescendant` e `role="option"`; mantenha o `<label for>` no select original (ele é ligado à seleção).
- Teclado: `Enter`/`Espaço`/`↓` abre, setas navegam, `Enter` seleciona, `Esc` fecha, `Backspace` remove o último chip.
- Textos de estado em pt-BR (“Buscando…”, “Nenhum resultado encontrado”, “Digite 2 ou mais caracteres”).
- Contraste: opção destacada `ttsc-canvas-2` com texto `ttsc-text`; desabilitada em `ttsc-text-muted` + rótulo explicativo (“sem vagas”).
- O tema padrão do Select2 é branco fixo: sem o CSS abaixo, o dropdown fica ilegível no escuro.

## Modelos

### HTML

```html
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="enr-course">Curso</label>
  <select id="enr-course" name="course_uuid" data-ttsc-select2 data-placeholder="Selecione o curso">
    <option></option>
    <?php foreach ($coursesByType as $type => $courses): ?>
      <optgroup label="<?= $this->e($type) ?>">
        <?php foreach ($courses as $c): ?>
          <option value="<?= $this->e($c['uuid']) ?>" <?= $c['uuid'] === $selected ? 'selected' : '' ?>><?= $this->e($c['name']) ?></option>
        <?php endforeach; ?>
      </optgroup>
    <?php endforeach; ?>
  </select>
</div>

<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="enr-student">Aluno</label>
  <select id="enr-student" name="student_uuid" data-ttsc-select2-ajax="/api/v1/students/search"
          data-placeholder="Digite nome, CPF ou matrícula...">
    <?php if ($student): ?><option value="<?= $this->e($student['uuid']) ?>" selected><?= $this->e($student['name']) ?></option><?php endif; ?>
  </select>
</div>

<select name="shifts[]" multiple data-ttsc-select2 data-placeholder="Selecione os turnos">
  <option value="morning">Manhã</option><option value="afternoon">Tarde</option><option value="evening">Noite</option>
</select>
```

### CSS

```css
/* assets/css/ttsc.select2.css — carregar depois de vendor/select2/select2.min.css */
.select2-container { font-size: 13px; }
.select2-container--default .select2-selection--single,
.select2-container--default .select2-selection--multiple {
  min-height: 34px; border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control);
  background: var(--ttsc-surface); box-shadow: var(--ttsc-shadow-xs);
}
.select2-container--default .select2-selection--single .select2-selection__rendered { line-height: 32px; padding-inline: 12px 32px; color: var(--ttsc-text); }
.select2-container--default .select2-selection--single .select2-selection__placeholder,
.select2-container--default .select2-search--inline .select2-search__field::placeholder { color: var(--ttsc-text-muted); }
.select2-container--default .select2-selection--single .select2-selection__arrow { height: 32px; right: 6px; }
.select2-container--default .select2-selection--single .select2-selection__arrow b { border-color: var(--ttsc-text-muted) transparent transparent; }
.select2-container--default.select2-container--focus .select2-selection--multiple,
.select2-container--default.select2-container--open .select2-selection { border-color: var(--ttsc-accent); box-shadow: 0 0 0 3px var(--ttsc-accent-soft); }
.select2-container--default .select2-selection--multiple .select2-selection__choice {
  margin: 4px 4px 0 0; padding: 0 8px 0 22px; position: relative; font-size: 12px; line-height: 20px;
  border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-pill); background: var(--ttsc-surface-2); color: var(--ttsc-text);
}
.select2-container--default .select2-selection--multiple .select2-selection__choice__remove {
  border: 0; left: 4px; top: 1px; height: 18px; width: 16px; border-radius: 50%; background: transparent; color: var(--ttsc-text-muted);
}
.select2-container--default .select2-search--inline .select2-search__field { color: var(--ttsc-text); font-family: inherit; }
.select2-dropdown { border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-sm); background: var(--ttsc-surface);
  color: var(--ttsc-text); box-shadow: var(--ttsc-shadow-md); overflow: hidden; z-index: var(--ttsc-z-dropdown); }
.select2-container--open .select2-dropdown--below { margin-top: 4px; border-top: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-sm); }
.select2-container--default .select2-search--dropdown .select2-search__field {
  border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-sm); background: var(--ttsc-canvas-2); color: var(--ttsc-text); padding: 6px 8px; outline: none;
}
.select2-results__option { padding: 7px 10px; border-radius: 6px; margin: 0 4px; }
.select2-container--default .select2-results__option--highlighted.select2-results__option--selectable { background: var(--ttsc-canvas-2); color: var(--ttsc-text); }
.select2-container--default .select2-results__option--selected { background: var(--ttsc-accent-soft); color: var(--ttsc-text); font-weight: 500; }
.select2-container--default .select2-results__option--disabled { color: var(--ttsc-text-muted); }
.select2-container--default .select2-results__group { padding: 8px 10px 4px; font-size: 11px; font-weight: 500; letter-spacing: .04em;
  text-transform: uppercase; color: var(--ttsc-text-muted); }
.select2-results__message { color: var(--ttsc-text-muted); }
.s2-meta { display: block; font-size: 11px; color: var(--ttsc-text-muted); }
.s2-row { display: inline-flex; align-items: center; gap: 8px; }
.s2-avatar { width: 22px; height: 22px; border-radius: 50%; object-fit: cover; flex: 0 0 auto; }
.s2-initials { display: inline-grid; place-items: center; background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text); font-size: 10px; font-weight: 600; }
/* Drawers/modais do ttscui ficam acima do dropdown padrão: */
.ttsc-drawer .select2-dropdown, .ttsc-modal .select2-dropdown { z-index: calc(var(--ttsc-z-modal) + 1); }
```

### JS

```js
// assets/js/core/ttsc.select2.js — requer jQuery 3.7.1 + vendor/select2/select2.min.js
const ptBR = {
  errorLoading: () => 'Os resultados não puderam ser carregados.',
  inputTooLong: (a) => { const n = a.input.length - a.maximum; return `Apague ${n} caractere${n > 1 ? 's' : ''}`; },
  inputTooShort: (a) => `Digite ${a.minimum - a.input.length} ou mais caracteres`,
  loadingMore: () => 'Carregando mais resultados…',
  maximumSelected: (a) => `Você só pode selecionar ${a.maximum} ite${a.maximum > 1 ? 'ns' : 'm'}`,
  noResults: () => 'Nenhum resultado encontrado',
  searching: () => 'Buscando…',
  removeAllItems: () => 'Remover todos os itens',
  removeItem: () => 'Remover item',
  search: () => 'Buscar',
};
$.fn.select2.defaults.set('language', ptBR);
$.fn.select2.defaults.set('width', '100%');

export function initSelect2(root = document) {
  $(root).find('select[data-ttsc-select2]').each(function () {
    const $el = $(this);
    if ($el.hasClass('select2-hidden-accessible')) return;          // idempotente
    $el.select2({
      placeholder: $el.data('placeholder'),
      allowClear: !this.multiple,
      closeOnSelect: !this.multiple,
      dropdownParent: $el.closest('.ttsc-drawer, .ttsc-modal').length ? $el.closest('.ttsc-drawer, .ttsc-modal') : $(document.body),
    });
  });

  $(root).find('select[data-ttsc-select2-ajax]').each(function () {
    const $el = $(this);
    if ($el.hasClass('select2-hidden-accessible')) return;
    $el.select2({
      placeholder: $el.data('placeholder'),
      allowClear: true,
      minimumInputLength: 2,
      ajax: {
        url: $el.data('ttscSelect2Ajax'),
        delay: 250,
        data: (params) => ({ q: params.term, page: params.page || 1 }),
        processResults: (data) => data,             // servidor já devolve {results, pagination}
        cache: true,
      },
      templateResult: (s) => (s.id
        ? $('<span>').text(s.text).append($('<span class="s2-meta">').text(`${s.enrollment_code || 'sem matrícula'} · CPF ${s.cpf || '—'}`))
        : s.text),
      templateSelection: (s) => s.text,
    });
  });
}

$(() => initSelect2());
$('#enr-student').on('select2:select', (e) => {
  document.querySelector('#student-summary').textContent = e.params.data.text;
});
```

### SQL

```sql
-- GET /api/v1/students/search?q=ana&page=1  (banco do tenant). MariaDB 10.11 / MySQL 8
SELECT u.uuid AS id, u.name AS text, u.cpf, MAX(e.code) AS enrollment_code
  FROM users u
  LEFT JOIN enrollments e ON e.student_uuid = u.uuid AND e.deleted_at IS NULL
 WHERE u.deleted_at IS NULL
   AND u.type = 'student'
   AND (u.name LIKE CONCAT('%', :q, '%')
        OR u.cpf LIKE CONCAT(:q_digits, '%')
        OR e.code LIKE CONCAT(:q_code, '%'))
 GROUP BY u.uuid, u.name, u.cpf
 ORDER BY u.name
 LIMIT 21 OFFSET :offset;                 -- 20 por página; a 21ª linha indica pagination.more

-- Opções do select de curso (agrupadas por tipo no PHP)
SELECT c.uuid, c.name, c.type
  FROM courses c
 WHERE c.unit_uuid = :unit_uuid AND c.is_active = 1 AND c.deleted_at IS NULL
 ORDER BY c.type, c.name;
```

O endpoint busca 21 linhas, devolve 20 em `results` e `pagination.more = (count === 21)`; `:offset = (page - 1) * 20`. `:q_digits` é o termo sem máscara (CPF guardado só com dígitos). O tipo `student` vem do cadastro de usuários do tenant. O JSON vai cru (`json_encode`); quem protege contra HTML é o `templateResult`, que usa `.text()`.

## Faça / Não faça

- **Faça:** `minimumInputLength: 2` e `delay: 250` no AJAX; paginação no servidor.
- **Faça:** `dropdownParent` dentro de drawer/modal; o CSS de tokens acima para os dois temas.
- **Faça:** `templateResult` com `.text()` (nunca concatenar HTML com dados do banco).
- **Não faça:** Select2 para 3 ou 4 opções fixas, nem carregar milhares de `<option>` na página.
- **Não faça:** confiar no `tags: true` para valores que precisam existir no banco; valide no servidor.
