# Select

Lista suspensa de escolha única: um `<select>` nativo que o `TTSCSelect` (`assets/js/ttsc.select.js`) troca automaticamente por gatilho + painel do app, ou que fica nativo com `data-no-custom`.

## Quando usar

- Escolher **uma** opção de uma lista carregada pelo servidor: curso, turma, unidade, período letivo, turno. É o campo padrão dos drawers (`partials/drawers/page/_field.php`, `kind = 'select'`).
- Basta escrever o `<select>`: o layout `main.php` carrega `ttsc.select.js`, que realça todos os `<select>` da página e os inseridos depois (drawers, modais, AJAX). Não há classe nem atributo para ligar.
- Filtros e ordenações de barra de ferramentas que devem continuar nativos (seletor do sistema no celular, sem painel flutuante) → `data-no-custom`.
- Cabeçalho de categoria, ícone por opção, ação no rodapé, modo compacto → [AdvancedSelect](../AdvancedSelect/README.md) (mesmo motor, atributos extras).
- Múltipla escolha curta ou média: o mesmo campo com `multiple` (caixas de seleção no painel; ver [AdvancedSelect](../AdvancedSelect/README.md)). Listas longas lado a lado → [MultiSelectSplitter](../MultiSelectSplitter/README.md); etiquetas livres → [Tagify](../Tagify/README.md).
- Até 5 opções sempre visíveis → [Radio](../Radio/README.md); alternância compacta → [ToggleGroup](../ToggleGroup/README.md).
- Linhas por página de uma tabela → não use este componente: o `ttsc.pagination.js` cuida (ver [Pagination](../Pagination/README.md)).

## Anatomia

```
Curso *                                     label (for = id do select)
┌────────────────────────────────────┐
│ [ícone] EM-01 · Ensino Médio     ⌄ │      button.ttsc-select-trigger  (gerado)
└────────────────────────────────────┘
  <select id name required> escondido        guarda o valor e vai no POST
  painel .ttsc-select-dropdown no <body>     abre ao clicar
Informe o curso.                             .ttsc-form-message (só com aria-invalid="true")
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Container do campo | `div.ttsc-form-item` | recomendado (liga a mensagem de erro) |
| Rótulo | `label.ttsc-form-label[for]` | sim |
| Campo | `<select id name>` com `<option value>` | sim |
| Placeholder | primeira `<option value="">Selecione…</option>` | recomendado |
| Mensagem | `.ttsc-form-message` (aparece quando algo dentro do item tem `aria-invalid="true"`) | quando valida |
| Gerado pelo motor | `.ttsc-select-wrapper[data-target-select]`, `.ttsc-select-trigger`, `.ttsc-select-dropdown`, `.ttsc-select-item` | — |
| Nativo | `data-no-custom` (ou `.no-custom-select`) + `class="ttsc-select"` | quando fica nativo |

## Variantes

| Variante | Marcação | Resultado |
|---|---|---|
| Realçado (padrão) | `<select>` sem atributos especiais | gatilho `rounded-xl` com ícone da opção, painel com cabeçalho (texto do `<label>`) e check na opção atual; busca a partir de 7 opções |
| Nativo | `data-no-custom` + `class="ttsc-select"` | seletor do sistema; seta e cores do runtime (`--input`, `--background`, `--ring`) |
| Dependente | o filho é repovoado por JS | gatilho e lista acompanham as novas opções (observer do campo; `change` ou `TTSCSelect.refresh()` forçam na hora) |
| Agrupado | `<optgroup label>` | cabeçalho por grupo no painel |

Tamanhos: o motor ignora as classes do `<select>` (só repassa `font-mono`); o gatilho tem uma altura só (`py-2 text-xs`).

## Estados

| Estado | Como aplicar | Visual |
|---|---|---|
| Aberto | clique no gatilho | `aria-expanded="true"`, anel `ring-2 ring-emerald-500`, chevron girado |
| Selecionado | opção atual | `.is-selected`, fundo `bg-emerald-50`, texto `text-emerald-700`, check |
| Inválido | `aria-invalid="true"` no `<select>` + `.ttsc-form-message` no `.ttsc-form-item` | a mensagem aparece pelo CSS do runtime; a borda do gatilho precisa da extensão CSS abaixo |
| Desabilitado | `disabled` no `<select>` (ou na `<option>` / `<optgroup>`) | gatilho `disabled` + `aria-disabled`, opacidade .55; opção `.is-disabled` não escolhível. Alternar `disabled` por JS atualiza o gatilho sozinho |

## Features

Categorias seguem a documentação do ktui (Select). Onde o recurso não existe no motor nativo, a seção diz qual alternativa do DS usar.

### Basic Usage

Um `<select>` comum, com `<label for>`. O motor troca o campo por gatilho + painel sem nenhuma classe extra.

```html
<label class="ttsc-form-label" for="turno">Turno</label>
<select id="turno" name="turno">
  <option value="manha">Manhã</option>
  <option value="tarde">Tarde</option>
</select>
```

### Placeholder Text

- Primeira opção vazia: `<option value="">Selecione o curso</option>` (o texto aparece no gatilho enquanto nada estiver escolhido).
- Sem opção vazia, use `data-placeholder="Selecione…"` no `<select>`; vale também para `multiple` sem seleção.

### Disabled Select

`disabled` no `<select>`: o gatilho fica desabilitado (`aria-disabled`, opacidade .55) e não abre o painel. Alternar `disabled` por JS atualiza o gatilho sem chamar nada.

### Disabled Option

`<option value="x" disabled>`: a opção aparece na lista, mas não pode ser escolhida (`.is-disabled`). `<optgroup disabled>` desabilita o grupo inteiro.

### Size Variants

O tamanho do gatilho é único: as classes de tamanho do `<select>` são ignoradas. Para uma versão menor, use `data-compact-select` (só escolha única, sem cabeçalho, busca nem rodapé; ver [AdvancedSelect](../AdvancedSelect/README.md)).

### Multiple Selection

`multiple` no `<select>` (use `name="campo[]"`). No painel cada opção vira caixa de seleção, e o painel fica aberto entre cliques. O gatilho mostra os rótulos escolhidos ou “N selecionados”.

```html
<select name="turnos[]" multiple data-placeholder="Selecione os turnos">
  <option value="manha">Manhã</option>
  <option value="tarde">Tarde</option>
  <option value="noite">Noite</option>
</select>
```

### Maximum Selection

Não suportado no Select nativo: o motor não limita a quantidade de opções escolhidas. Para limitar, use [Select2](../Select2/README.md) (`maximumSelectionLength`) ou valide no `submit`.

### Enhanced Tags

Não suportado: o Select não tem chips nem criação de etiquetas. Para etiquetas livres, use [Tagify](../Tagify/README.md).

### Tags with Icons

Não suportado (sem chips). Opções com ícone no painel são de [Icons](#icons) abaixo.

### Basic Tags

Não há chips no Select. No múltiplo, as escolhas aparecem como rótulos no gatilho (até duas) e, acima disso, como contagem. Para chips com criação de tags, use [Select2](../Select2/README.md) (`tags: true`) ou [Tagify](../Tagify/README.md).

### Pre-selected Tags

Opções marcadas com `selected` (em `multiple` ou não) aparecem já escolhidas: no gatilho e, no painel, com check ou caixa marcada.

```html
<select name="turnos[]" multiple>
  <option value="manha" selected>Manhã</option>
  <option value="tarde">Tarde</option>
</select>
```

### Tags: selected count

No múltiplo, o gatilho mostra os rótulos escolhidos quando há até duas opções e “N selecionados” a partir de três, com `title` listando todas. Para contar fora do campo, leia `select.selectedOptions.length` (ver [Reading the current selection](#reading-the-current-selection)).

### Search & Filtering

Com mais de 6 opções, o painel mostra o campo “Filtrar opções...”. A busca ignora acentos e maiúsculas. Sem resultado, aparece “Nenhuma opção encontrada”.

### Search

É a mesma busca da seção acima. Ela não é remota: todas as opções precisam estar no `<select>`. Para lista grande vinda do servidor, use [Select2](../Select2/README.md) com AJAX.

### Remote Data

Não há carregamento remoto no Select. Carregue as opções por JS e dispare `change` (o padrão do exemplo “Select dependente” em [Modelos](#modelos)). Para busca remota com paginação, use [Select2](../Select2/README.md).

### Icons

`data-icon` na `<option>` com a classe completa do Font Awesome (`fa-light fa-graduation-cap`). Sem o atributo, o motor escolhe o ícone pelo texto da opção (mapa por palavra inteira, por exemplo “Sede Matriz” → `fa-building-columns`); sem casamento, usa `fa-circle-dot`.

### Multiple Icons

No múltiplo o gatilho mostra `fa-list-check`, e cada opção do painel mostra o próprio `data-icon` (ou o ícone pelo texto) ao lado da caixa de seleção.

### Avatar

Não suportado: o Select não renderiza imagens nem iniciais de avatar. Para opções com avatar, use [Select2](../Select2/README.md) com `templateResult`.

### Country Selection

Não suportado: sem bandeiras nem lista de países pronta. Monte a lista no servidor e use `data-icon` ou, para bandeiras, [Select2](../Select2/README.md) com `templateResult`.

### Description

Não há linha secundária por opção no Select. A descrição do campo vai no `<label>` e na ajuda do `.ttsc-form-item`. Para texto por opção, use [Select2](../Select2/README.md) (`templateResult`).

### Modal Integration

Funciona dentro de drawers e modais: o motor realça também os selects inseridos depois (por JS ou AJAX) e move o painel para o `<body>` com `position: fixed`, então ele não fica cortado pelo container.

### Template Customization

O Select não tem objeto de template. A aparência vem das classes do `ttsc.commercial.css` (`.ttsc-select-trigger`, `.ttsc-select-dropdown`, `.ttsc-select-item`) e dos tokens do DS. Para mudar a marcação de cada opção, use [Select2](../Select2/README.md) (`templateResult` e `templateSelection`).

## API Reference

`window.TTSCSelect` (objeto, sem instâncias):

| Método | Efeito |
|---|---|
| `TTSCSelect.initAll(root?)` | realça todo `select:not([data-no-custom]):not(.no-custom-select)` dentro de `root` (padrão `document`), pulando selects de paginação |
| `TTSCSelect.enhance(select)` | realça um `<select>`; respeita `data-no-custom` / `.no-custom-select`; se já estiver realçado e ligado, não faz nada |
| `TTSCSelect.refresh(select)` | relê opções, rótulo, categoria e `disabled` e redesenha o gatilho e a lista |
| `TTSCSelect.closeAll()` | fecha todos os painéis abertos |

### Data Attributes

| Atributo | Onde | Efeito |
|---|---|---|
| `data-category` | `<select>` | título do cabeçalho do painel |
| `data-icon` | `<option>` | classe do ícone daquela opção |
| `data-placeholder` | `<select>` | texto do gatilho sem seleção (padrão “Selecione...”) |
| `data-action-label` | `<select>` | botão no rodapé do painel (mostra um aviso, sem ação real) |
| `data-compact-select` | `<select>` | modo compacto (só escolha única) |
| `data-no-custom` / `.no-custom-select` | `<select>` | o motor não toca no campo, inclusive quando inserido por JS |
| `data-pagination-select` | `<select>` | marca como seletor de linhas por página (fica com o `ttsc.pagination.js`) |

Selects de paginação nunca são realçados: `data-pagination-select`, `id`/`name` com `per_page`, `per-page`, `page_size` ou `pagesize`, ou dentro de `.pagination`, `.per-page` e `[data-ttsc-page-size-control]`.

### Template Configuration

Não há opção de configuração de template. Para personalizar, sobrescreva as classes do `ttsc.commercial.css` ou use [Select2](../Select2/README.md).

### Option Data

Cada `<option>` tem `value` (valor enviado) e texto (rótulo). O motor lê `data-icon` dela.

### Events

| Evento | Onde | Quando |
|---|---|---|
| `change` e `input` (borbulham) | `<select>` nativo | a cada escolha no painel (no múltiplo, a cada marcação) |

Escute no `<select>`, não no gatilho. Um `change` que você dispara pelo seu código também faz o motor atualizar o gatilho e a lista.

### Programmatic selection

```js
const turno = document.getElementById('turno');
turno.value = 'tarde';                                  // escolhe a opção
TTSCSelect.refresh(turno);                              // redesenha o gatilho e a lista
turno.dispatchEvent(new Event('change', { bubbles: true }));  // avisa quem escuta o campo
```

Para múltiplo, marque as opções: `option.selected = true`, depois `refresh` e `change`.

### Reading the current selection

```js
turno.value;                                            // valor escolhido (string)
Array.from(turnos.selectedOptions).map((o) => o.value); // múltiplo: lista de valores
```

### Search Autofocus

O motor não foca o campo de busca ao abrir. Ao abrir pelo teclado, o foco vai para a opção selecionada.

### Enter Key Behavior

- No gatilho: Enter ou Espaço abrem o painel.
- Na lista: Enter ou Espaço escolhem a opção em foco (no múltiplo, marcam ou desmarcam).
- Na busca: Enter escolhe o primeiro resultado.
- `Esc` fecha e devolve o foco ao gatilho.

### Global Dropdown Management

Para fechar todos os painéis (por exemplo, ao abrir um modal): `TTSCSelect.closeAll()`.

### TypeScript

O motor é JavaScript puro e não traz tipos. Se o projeto usa TypeScript, declare a superfície usada:

```ts
declare global {
  interface Window {
    TTSCSelect: {
      initAll(root?: ParentNode): void;
      enhance(select: HTMLSelectElement): void;
      refresh(select: HTMLSelectElement): void;
      closeAll(): void;
    };
  }
}
export {};
```

### Correções aplicadas

Correções aplicadas (branch `claude/design-system-extraction-srfpiz`): antes o motor ignorava `disabled`, achatava `<optgroup>`, transformava `multiple` em escolha única, ignorava `data-no-custom` em selects inseridos por JS e escrevia os rótulos com `innerHTML`; o `multiselect` de `partials/drawers/page/_field.php` agora sai realçado como múltiplo e com os valores atuais marcados.

## Acessibilidade

- `<label for>` sempre: o motor liga o rótulo ao gatilho (`aria-labelledby` = rótulo + valor) e clicar no rótulo foca o gatilho.
- `required` não basta: o `<select>` realçado tem 0×0 px, o navegador não consegue focá-lo e o balão nativo não aparece. Valide no `submit`, marque `aria-invalid="true"`, ligue a mensagem com `aria-describedby` e devolva o foco ao gatilho.
- Teclado do realçado: ↓ / ↑ / Enter / Espaço abrem; no painel ↑ / ↓, Home / End, digitação para saltar, Enter / Espaço escolhem, `Esc` e `Tab` fecham e devolvem o foco ao gatilho. Lista com `role="listbox"` e opções `role="option"` + `aria-selected`.
- Mensagem de erro em `--ttsc-danger-text` (≥ 4,5:1), nunca só a cor da borda.

## Modelos

### HTML

```php
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="enr-course">Curso *</label>
  <select id="enr-course" name="course_uuid" required data-category="Cursos" aria-describedby="enr-course-msg">
    <option value="">Selecione o curso</option>
    <?php foreach ($courses as $c): ?>
      <option value="<?= $this->e($c['uuid']) ?>"<?= $c['uuid'] === ($enrollment['course_uuid'] ?? '') ? ' selected' : '' ?>>
        <?= $this->e($c['code'] . ' · ' . $c['name']) ?>
      </option>
    <?php endforeach; ?>
  </select>
  <p class="ttsc-form-message" id="enr-course-msg">Informe o curso.</p>
</div>

<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="enr-class">Turma</label>
  <select id="enr-class" name="class_uuid" data-category="Turmas do curso"
          data-source="<?= $this->e(url('/api/v1/academic/lookup/classes')) ?>">
    <option value="">Escolha o curso primeiro</option>
  </select>
</div>

<!-- Ordenação de toolbar: nativo -->
<select class="ttsc-select" data-no-custom name="order" aria-label="Ordenar por">
  <option value="name">Nome (A–Z)</option>
  <option value="recent">Mais recentes</option>
</select>
```

O endpoint de turmas acima é ilustrativo: aponte `data-source` para a rota de lookup do seu módulo.

### CSS

O gatilho e o painel são estilizados por `ttsc.commercial.css` (seção “TTSC CUSTOM SELECT SYSTEM” + regras `html.dark`); o nativo, pelo `.ttsc-select` de `tailwind-runtime.css`. O runtime já mostra `.ttsc-form-message` quando o item tem `[aria-invalid=true]`; falta só levar o erro ao gatilho:

```css
/* Erro no gatilho gerado (o aria-invalid fica no <select> escondido) */
.ttsc-select-wrapper:has(> select[aria-invalid="true"]) .ttsc-select-trigger {
  border-color: var(--ttsc-danger) !important;
  box-shadow: 0 0 0 3px color-mix(in oklab, var(--ttsc-danger) 18%, transparent);
}
.ttsc-form-item .ttsc-form-message { color: var(--ttsc-danger-text); font-size: 12px; margin-top: var(--ttsc-space-1); }

/* Nativo: opções seguem o tema */
select.ttsc-select option { background-color: var(--ttsc-surface); color: var(--ttsc-text); }
```

### JS

```js
// Select dependente: curso → turmas. O motor já realçou os dois campos;
// basta trocar as <option> do filho e disparar 'change' para o painel redesenhar.
document.addEventListener('DOMContentLoaded', function () {
  var course = document.getElementById('enr-course');
  var cls = document.getElementById('enr-class');
  if (!course || !cls) return;

  async function loadClasses() {
    cls.replaceChildren(new Option(course.value ? 'Carregando…' : 'Escolha o curso primeiro', ''));
    cls.dispatchEvent(new Event('change', { bubbles: true }));
    if (!course.value) return;
    var res = await fetch(cls.dataset.source + '?course_uuid=' + encodeURIComponent(course.value), {
      headers: { Accept: 'application/json' }, credentials: 'same-origin'
    });
    var rows = res.ok ? ((await res.json()).data || []) : [];
    cls.replaceChildren(new Option(rows.length ? 'Selecione a turma' : 'Nenhuma turma ativa', ''));
    rows.forEach(function (r) { cls.add(new Option(r.code + ' · ' + r.name, r.uuid)); }); // new Option escapa o texto
    cls.dispatchEvent(new Event('change', { bubbles: true }));                          // gatilho + lista redesenham
  }

  course.addEventListener('change', function () { setInvalid(course, false); loadClasses(); });
  if (course.value) loadClasses();

  // Validação no submit (o balão nativo não aparece com o select escondido)
  function setInvalid(select, invalid) {
    select.setAttribute('aria-invalid', invalid ? 'true' : 'false');
    var trigger = select.parentNode.querySelector('.ttsc-select-trigger');
    if (trigger) {
      if (invalid) trigger.setAttribute('aria-describedby', select.getAttribute('aria-describedby') || '');
      else trigger.removeAttribute('aria-describedby');
    }
  }
  course.form && course.form.addEventListener('submit', function (e) {
    if (!course.value) {
      e.preventDefault();
      setInvalid(course, true);
      var trigger = course.parentNode.querySelector('.ttsc-select-trigger');
      (trigger || course).focus();
    }
  });
});
```

### SQL

```sql
-- Opções do select "Curso" (tenant): ativos da unidade do usuário
SELECT c.uuid, c.code, c.name
  FROM courses c
 WHERE c.deleted_at IS NULL
   AND c.is_active = 1
   AND c.unit_uuid = :unit_uuid
 ORDER BY c.name;

-- Endpoint do select dependente: turmas ativas do curso
SELECT cl.uuid, cl.code, cl.name, cl.shift
  FROM classes cl
 WHERE cl.course_uuid = :course_uuid
   AND cl.is_active = 1
   AND cl.deleted_at IS NULL
 ORDER BY cl.name;
```

A primeira consulta vira `$courses` na view Plates (cada `<option>` com `$this->e()`); a segunda é devolvida pelo endpoint como `{"data": […]}` e montada pelo JS com `new Option()`.

## Faça / Não faça

- **Faça:** placeholder `value=""` como primeira opção e validação no `submit` com `aria-invalid` + `.ttsc-form-message`.
- **Faça:** depois de repovoar ou mudar o valor por código, dispare `change` no `<select>`.
- **Faça:** `data-no-custom` em filtros que devem continuar nativos; `name="campo[]"` em `<select multiple>`.
- **Não faça:** contar com o balão nativo de `required` no campo realçado; valide no `submit`.
- **Não faça:** montar `<option>` com `innerHTML` a partir de dados do banco; use `new Option()`.
- **Não faça:** `ttsc-select-sm` / `ttsc-select-lg` esperando outro tamanho: no campo realçado a classe fica no `<select>` escondido.
