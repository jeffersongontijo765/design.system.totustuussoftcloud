# AdvancedSelect

Opções avançadas do `TTSCSelect` (`assets/js/ttsc.select.js`), o motor que o app aplica sozinho a todo `<select>`: cabeçalho de categoria, ícone por opção, busca acima de 6 opções, grupos (`<optgroup>`), múltipla escolha, ação no rodapé e modo compacto, sempre com o `<select>` nativo como fonte do valor.

## Quando usar

- Campos em drawers e formulários em que o painel precisa dizer **o que** se escolhe (`data-category`) e mostrar um ícone por opção: unidade, curso, frequência de cobrança, responsável.
- Listas de 7 a ~60 opções: a caixa “Filtrar opções...” aparece quando o `<select>` tem mais de 6 `<option>` (reavaliado a cada redesenho, então um select dependente que cresce ganha a busca).
- Opções agrupadas (`<optgroup>`): turmas por curso, disciplinas por série.
- Escolha de **algumas** opções de uma lista curta ou média (`<select multiple>`): turmas de um professor, unidades de acesso. O painel mostra caixas de seleção e o gatilho resume (“1º A, 1º B” ou “5 selecionados”).
- Um atalho de cadastro no rodapé do painel (`data-action-label`). O botão só dispara um `showToast()`; não abre drawer nem cria registro.
- Seletor pequeno em barra de ferramentas sem cabeçalho nem busca → `data-compact-select` (não vale para `multiple`).
- Campo comum, sem nenhum desses atributos → [Select](../Select/README.md) (é o mesmo motor com os padrões).
- Seleção múltipla com muitas opções e lado a lado (“disponíveis / escolhidas”) → [MultiSelectSplitter](../MultiSelectSplitter/README.md); valores livres como etiquetas → [Tagify](../Tagify/README.md).
- Busca no servidor, milhares de opções ou carregamento paginado: o motor não faz `fetch`; use [Select2](../Select2/README.md) (telas com jQuery) ou carregue as opções pelo endpoint e chame `TTSCSelect.refresh()`.
- 2–4 opções sempre visíveis → [SegmentedTabs](../SegmentedTabs/README.md) ou [Radio](../Radio/README.md).

## Anatomia

```
.ttsc-select-wrapper[data-target-select="as-course"][data-ttsc-wired="true"] (.is-disabled)
  ├ <select data-ttsc-enhanced="true" tabindex="-1" aria-hidden="true">   (invisível; guarda valor e name)
  ├ button.ttsc-select-trigger[aria-haspopup="listbox"][aria-expanded][aria-controls][aria-labelledby]
  │    ├ i.ttsc-trigger-icon   (ícone da opção atual; fa-list-check no múltiplo)
  │    ├ span.ttsc-trigger-label#<listbox>-value
  │    └ i.ttsc-trigger-chevron
  └ div.ttsc-select-dropdown.hidden   ← movido para <body> na 1ª abertura (position: fixed)
       ├ cabeçalho: categoria + fa-list-check                     (não no compacto)
       ├ input.ttsc-select-search "Filtrar opções..."             (oculto com ≤ 6 opções)
       ├ div.ttsc-select-options[role="listbox"][aria-multiselectable]
       │    ├ div.ttsc-select-group-label[role="presentation"]    (<optgroup label>)
       │    └ button.ttsc-select-item[role="option"][aria-selected][aria-disabled][data-index][data-val]
       │         (+ .is-selected, .is-disabled, .is-multi com i.ttsc-select-checkbox)
       └ rodapé: button.ttsc-select-action "+ <data-action-label>"  (opcional, não no compacto)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Fonte | `<select>` com `id`, `name` e `<option>` (ou `<optgroup>`) | sim |
| Rótulo | `<label for="id">` (vira `aria-labelledby` do gatilho e da lista) | sim |
| Categoria | `data-category="Cursos ativos"` no `<select>` | recomendado |
| Ícone da opção | `data-icon="fa-light fa-graduation-cap"` na `<option>` (classe completa) | não |
| Texto vazio | `data-placeholder="Selecione…"` (múltiplo sem seleção, ou simples sem opção) | não |
| Ação no rodapé | `data-action-label="Nova Unidade"` no `<select>` | não |
| Compacto | `data-compact-select` no `<select>` (ignorado com `multiple`) | não |
| Fora do motor | `data-no-custom` ou `class="no-custom-select"` | não |

## Variantes

| Variante | Como | Efeito |
|---|---|---|
| Padrão | qualquer `<select>` | gatilho `rounded-xl`, painel `rounded-2xl` com cabeçalho e lista; opção atual com fundo verde-claro e check |
| Com categoria | `data-category` | texto do cabeçalho (sem ele: o primeiro `<label>` dentro do `div` pai mais próximo, depois palavras inteiras do `id`/`name`, por fim “Opções Disponíveis”) |
| Com ícones | `data-icon` por opção | sem ele o ícone sai de um mapa por **palavra inteira** do texto + valor, sem acento (“Sede Matriz” → `fa-building-columns`); sem casamento, `fa-circle-dot` |
| Com grupos | `<optgroup label>` | cabeçalho por grupo; grupo sem resultado na busca some; `<optgroup disabled>` desabilita as opções |
| Múltiplo | `multiple` | caixa de seleção por opção, o painel fica aberto entre cliques; gatilho com até 2 rótulos ou “N selecionados” e `title` com todos |
| Com busca | > 6 opções | filtra pelo texto sem acento, mensagem “Nenhuma opção encontrada” |
| Com ação | `data-action-label` | rodapé “+ rótulo” → `showToast('Assistente de configuração para <rótulo> acionado.', 'info', <rótulo>)` |
| Compacto | `data-compact-select` | gatilho `.ttsc-select-trigger-compact`, painel `.ttsc-select-dropdown-compact`, sem cabeçalho, busca, ícones nem rodapé |
| Desabilitado | `disabled` no `<select>` ou na `<option>` | gatilho `disabled` + `aria-disabled` (opacidade .55); opção `.is-disabled`, não escolhível |

Cores: o motor escreve utilitários fixos (`border-slate-200`, `bg-emerald-50`, `text-emerald-700`, `ring-emerald-500`); tema escuro, foco por teclado, desabilitado e grupos estão em `ttsc.commercial.css` (`html.dark .ttsc-select-*`, `.ttsc-select-item:focus-visible`, `.ttsc-select-group-label`). O compacto só tem acabamento em `ttsc.developer-status.css`, escopado a `body.developer-status`; fora dessa página use a extensão CSS abaixo.

## API

`window.TTSCSelect` (objeto, sem instâncias):

| Método | Efeito |
|---|---|
| `TTSCSelect.initAll(root?)` | realça todo `select:not([data-no-custom]):not(.no-custom-select)` dentro de `root` (padrão `document`), pulando selects de paginação |
| `TTSCSelect.enhance(select)` | realça um `<select>`; respeita `data-no-custom` / `.no-custom-select` e selects de paginação; se já realçado e ligado, não faz nada; se veio com marcação congelada do servidor, refaz |
| `TTSCSelect.refresh(select)` | relê opções, rótulo, categoria e `disabled` do `<select>` e redesenha |
| `TTSCSelect.closeAll()` | fecha todos os painéis abertos |

Automático: `initAll()` no `DOMContentLoaded`; um `MutationObserver` em `document.body` realça selects inseridos depois (drawers, modais, AJAX); outro, por campo, chama o `refresh` quando opções, `disabled`, `label` ou `selected` mudam; um `IntersectionObserver` reatualiza o rótulo quando o gatilho entra na tela (valor definido por código sem evento, ex.: drawer de edição preenchido antes de abrir).

| Atributo | Onde | Efeito |
|---|---|---|
| `data-category` | `<select>` | título do cabeçalho |
| `data-icon` | `<option>` | classe do ícone daquela opção |
| `data-placeholder` | `<select>` | texto do gatilho sem seleção (padrão “Selecione...”) |
| `data-action-label` | `<select>` | botão no rodapé (só `showToast`) |
| `data-compact-select` | `<select>` | modo compacto (só escolha única) |
| `data-no-custom` / `.no-custom-select` | `<select>` | o motor não toca no campo, inclusive quando inserido por JS |
| `data-pagination-select` | `<select>` | marca como seletor de linhas por página (fica com o `ttsc.pagination.js`) |
| `multiple`, `disabled`, `<optgroup>`, `<option disabled>` | nativos | suportados |
| `data-ttsc-enhanced="true"` | `<select>` | escrito pelo motor |

Selects de paginação nunca são realçados: `data-pagination-select`, `id`/`name` com `per_page`, `per-page`, `page_size`, `pagesize`, ou dentro de `.pagination`, `.pagination-perpage`, `.per-page`, `[data-ttsc-page-size-control]` com todas as opções numéricas.

| Evento | Onde | Quando |
|---|---|---|
| `change` e `input` (borbulham) | `<select>` nativo | a cada escolha no painel (no múltiplo, a cada marcação) |
| `change` disparado pelo seu código | `<select>` nativo | o motor atualiza gatilho e lista |

**Correções aplicadas** (branch `claude/design-system-extraction-srfpiz`, commit `fix(select)`): textos de opção, categoria, grupo e ação são escritos com `textContent` (antes `innerHTML`, que reexecutava marcação vinda do banco); `enhance()` respeita `data-no-custom` em todos os caminhos; `multiple`, `<optgroup>`, `disabled`, teclado e ARIA de listbox passaram a existir; o mapa de ícones e as categorias/ações automáticas casam palavra inteira (“Rafael”, “Israel” e “Docente” não ganham mais ícone por acaso); a busca é reavaliada a cada redesenho; e `TTSCSelect.refresh()` foi adicionado.

Ainda vale: sem busca remota nem botão limpar; o rodapé automático aparece quando `id`/`name` tem a palavra `product`, `source`, `ae` ou `owner` (ex.: `owner_uuid` → “Novo Responsável”); o compacto anuncia `aria-label="Per page: …"` em inglês.

## Acessibilidade

- Sempre `<label for="id">`: o motor liga o rótulo ao gatilho (`aria-labelledby="<label> <valor>"`) e à lista, e clicar no rótulo foca o gatilho.
- Gatilho: `aria-haspopup="listbox"`, `aria-expanded`, `aria-controls`; `disabled` + `aria-disabled` quando o `<select>` está desabilitado.
- Lista: `role="listbox"` (+ `aria-multiselectable="true"` no múltiplo), opções `role="option"` com `aria-selected` e `aria-disabled`; cabeçalhos de grupo `role="presentation"`.
- Teclado no gatilho: ↓ / ↑ / Enter / Espaço abrem com foco na opção selecionada; `Esc` fecha. No painel: ↑ / ↓ navegam (↑ na primeira volta à busca), Home / End, Enter / Espaço escolhem, digitar salta para a opção que começa pelas letras, `Tab` e `Esc` fecham e devolvem o foco ao gatilho. Na busca, Enter escolhe o primeiro resultado.
- `required` no `<select>` escondido continua sem balão nativo (campo 0×0, `aria-hidden`): valide no `submit` e mostre a mensagem com `aria-invalid` (ver [Select](../Select/README.md)).
- Contraste: opção selecionada `text-emerald-700` sobre `bg-emerald-50` (≥ 5:1) e marcada também por check ou caixa marcada; inativas `text-slate-600`; foco por teclado com anel verde.

## Modelos

### HTML

```php
<!-- Unidade: categoria + ação no rodapé (ícones automáticos por "Sede"/"Matriz"/"Filial") -->
<div>
  <label class="ttsc-form-label" for="enr-unit">Unidade</label>
  <select id="enr-unit" name="unit_uuid" data-category="Unidades da instituição" data-action-label="Nova Unidade">
    <?php foreach ($units as $u): ?>
      <option value="<?= $this->e($u['uuid']) ?>"<?= $u['uuid'] === $unitUuid ? ' selected' : '' ?>><?= $this->e($u['name']) ?></option>
    <?php endforeach; ?>
  </select>
</div>

<!-- Curso: ícone explícito por opção; com mais de 6 cursos a busca aparece -->
<div>
  <label class="ttsc-form-label" for="enr-course">Curso</label>
  <select id="enr-course" name="course_uuid" data-category="Cursos ativos">
    <?php foreach ($courses as $c): ?>
      <option value="<?= $this->e($c['uuid']) ?>"
              data-icon="fa-light <?= $this->e($courseIcons[$c['type']] ?? 'fa-graduation-cap') ?>"
              <?= $c['uuid'] === $courseUuid ? 'selected' : '' ?>><?= $this->e($c['code'] . ' · ' . $c['name']) ?></option>
    <?php endforeach; ?>
  </select>
</div>

<!-- Turmas do professor: múltiplo com grupos por curso -->
<div>
  <label class="ttsc-form-label" for="teacher-classes">Turmas</label>
  <select id="teacher-classes" name="class_uuids[]" multiple data-category="Turmas por curso" data-placeholder="Nenhuma turma">
    <?php foreach ($classesByCourse as $courseName => $rows): ?>
      <optgroup label="<?= $this->e($courseName) ?>">
        <?php foreach ($rows as $cl): ?>
          <option value="<?= $this->e($cl['uuid']) ?>"<?= in_array($cl['uuid'], $selected, true) ? ' selected' : '' ?><?= $cl['is_active'] ? '' : ' disabled' ?>><?= $this->e($cl['name']) ?></option>
        <?php endforeach; ?>
      </optgroup>
    <?php endforeach; ?>
  </select>
</div>

<!-- Frequência de cobrança: compacto -->
<select id="billing-frequency" name="billing_frequency" data-compact-select aria-label="Frequência de cobrança">
  <option value="monthly" selected>Mensal</option>
  <option value="annual">Anual</option>
  <option value="one-time">Única</option>
</select>
```

### CSS

Estilo real: `ttsc.commercial.css` (seção “TTSC CUSTOM SELECT SYSTEM”: `.ttsc-select-wrapper`, `.ttsc-select-trigger`, `.ttsc-select-dropdown` com animação `ttscDropdownFadeIn`, foco `.ttsc-select-item:focus-visible`, `.ttsc-select-trigger:disabled`, `.ttsc-select-item.is-disabled`, `.ttsc-select-group-label`, regras `html.dark`) e `ttsc.drawer.css` (`.drawer-panel .ttsc-select-dropdown` sem limite de largura). Extensão por tokens, incluindo o compacto fora da página de status:

```css
/* Gatilho e painel por token (sobrepõe os utilitários slate/emerald gerados pelo JS) */
.ttsc-select-trigger { border-color: var(--ttsc-border) !important; background: var(--ttsc-surface) !important; border-radius: var(--ttsc-radius-control) !important; }
.ttsc-select-trigger .ttsc-trigger-label { color: var(--ttsc-text) !important; }
.ttsc-select-dropdown { background: var(--ttsc-surface) !important; border-color: var(--ttsc-border) !important; box-shadow: var(--ttsc-shadow-popover) !important; }
.ttsc-select-item.is-selected { background: var(--ttsc-accent-soft) !important; color: var(--ttsc-accent-text) !important; border-color: var(--ttsc-accent-border) !important; }
.ttsc-select-item:not(.is-selected):hover,
.ttsc-select-item:focus-visible:not(.is-selected) { background: var(--ttsc-canvas-2) !important; }
.ttsc-select-group-label { color: var(--ttsc-text-muted); }
.ttsc-select-wrapper:has(> select[aria-invalid="true"]) .ttsc-select-trigger { border-color: var(--ttsc-danger) !important; }

/* Compacto: hoje só existe em body.developer-status */
.ttsc-select-trigger-compact { display: inline-flex; align-items: center; gap: var(--ttsc-space-2); height: 26px; padding: 0 var(--ttsc-space-2); border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-sm); background: var(--ttsc-surface); color: var(--ttsc-text); font-size: 12px; font-weight: 600; }
.ttsc-select-dropdown-compact { display: flex; flex-direction: column; padding: var(--ttsc-space-1); border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-surface); background: var(--ttsc-surface); box-shadow: var(--ttsc-shadow-popover); }
.ttsc-select-dropdown-compact.hidden { display: none; }
.ttsc-select-item-compact { padding: 6px 10px; border-radius: var(--ttsc-radius-sm); text-align: start; color: var(--ttsc-text-2); }
.ttsc-select-item-compact.is-selected { color: var(--ttsc-accent-text); font-weight: 600; }
```

### JS

```js
// Nada a chamar: o motor realça no DOMContentLoaded e observa inserções e mudanças.
document.addEventListener('DOMContentLoaded', function () {

  // 1. Ler o valor: sempre pelo <select> (no múltiplo, as opções selecionadas)
  document.getElementById('teacher-classes').addEventListener('change', function (e) {
    var uuids = Array.from(e.target.selectedOptions).map(function (o) { return o.value; });
    console.log('turmas', uuids);
  });

  // 2. Trocar a seleção por código: atribuir e disparar 'change' (ou chamar refresh)
  function selecionarUnidade(uuid) {
    var s = document.getElementById('enr-unit');
    s.value = uuid;
    s.dispatchEvent(new Event('change', { bubbles: true }));
  }

  // 3. Repovoar com dados do endpoint: o observer do campo redesenha sozinho;
  //    refresh() força na hora (útil antes de abrir o painel por código).
  async function carregarCursos(unitUuid) {
    var s = document.getElementById('enr-course');
    var res = await fetch('/api/v1/academic/lookup/courses?unit_uuid=' + encodeURIComponent(unitUuid), { credentials: 'same-origin' });
    var rows = res.ok ? ((await res.json()).data || []) : [];
    s.replaceChildren(new Option('Selecione o curso', ''));
    rows.forEach(function (r) { s.add(new Option(r.code + ' · ' + r.name, r.uuid)); });
    TTSCSelect.refresh(s);
  }

  // 4. Bloquear o campo enquanto carrega: o gatilho acompanha o disabled
  var course = document.getElementById('enr-course');
  course.disabled = true;
  carregarCursos(document.getElementById('enr-unit').value).finally(function () { course.disabled = false; });

  // 5. Fechar painéis antes de abrir outro overlay
  TTSCSelect.closeAll();
});
```

O endpoint de cursos é ilustrativo: aponte para a rota de lookup do seu módulo.

### SQL

Opções dos exemplos (banco do tenant). Os rótulos são texto do cadastro: o PHP escapa com `$this->e()` e o motor os escreve com `textContent`.

```sql
-- Unidade (categoria "Unidades da instituição")
SELECT u.uuid, u.name, u.is_headquarters
  FROM units u
 WHERE u.status = 'active'              -- units não tem deleted_at/is_active no esquema do tenant
 ORDER BY u.is_headquarters DESC, u.name;

-- Curso (ícone por tipo; mais de 6 linhas liga a busca)
SELECT c.uuid, c.code, c.name, c.type
  FROM courses c
 WHERE c.unit_uuid = :unit_uuid
   AND c.is_active = 1
   AND c.deleted_at IS NULL
 ORDER BY c.name;

-- Turmas por curso (múltiplo com <optgroup>)
SELECT co.name AS course_name, cl.uuid, cl.name, cl.is_active
  FROM classes cl
  JOIN courses co ON co.uuid = cl.course_uuid AND co.deleted_at IS NULL
 WHERE cl.unit_uuid = :unit_uuid
   AND cl.deleted_at IS NULL
 ORDER BY co.name, cl.name;
```

O controller passa `$units`, `$courses`, um mapa `$courseIcons` (ex.: `['undergraduate' => 'fa-building-columns', 'technical' => 'fa-laptop-code']`) e `$classesByCourse` (linhas agrupadas por `course_name`) para a view, que gera uma `<option>` por linha. Para listas maiores que algumas dezenas, filtre no servidor (por unidade ou período) antes de renderizar: o motor carrega tudo no HTML.

## Faça / Não faça

- **Faça:** `data-category` em todo campo; a heurística por `<label>` pega o primeiro rótulo do `div` pai, que pode ser o de outro campo da mesma grade.
- **Faça:** `data-icon` quando o rótulo é nome de pessoa ou texto livre.
- **Faça:** `name="campo[]"` no múltiplo, e `data-placeholder` para o estado sem seleção.
- **Faça:** depois de mudar valor por código, dispare `change` ou chame `TTSCSelect.refresh(select)`.
- **Não faça:** prometer cadastro pelo `data-action-label`: o botão só mostra um toast.
- **Não faça:** `data-ttsc-select-*` ou `TTSC.Select`: são do ttscui, que o layout do app não carrega.
