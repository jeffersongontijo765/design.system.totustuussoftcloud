# Repeater

Lista de blocos de formulário repetíveis (`[data-ttsc-repeater]` do ttscui): um botão clona um modelo para dentro de um wrapper, com limite máximo e botão de remover por linha.

> Também listado em: **Formulários › Form Repeater (plugins)**.

## Quando usar

- O registro principal tem N filhos simples digitados juntos: responsáveis/familiares do aluno, telefones de contato, disciplinas de um pacote, parcelas de um acordo.
- Até ~10 linhas com 2–4 campos cada. Mais que isso, ou filhos com ciclo de vida próprio (editar/arquivar um a um) → tabela com drawer ([DataTable](../DataTable/README.md) + [Drawer](../Drawer/README.md)).
- Uma lista de valores sem estrutura (tags, e-mails) → [Tagify](../Tagify/README.md).

## Anatomia

```
Responsáveis                                       ┐
┌─────────────────────────────────────────────┐    │ #family-list   (wrapper: data-ttsc-repeater-wrapper)
│ Nome [__________] Parentesco [Mãe ▾] Tel [_] (🗑)│ ← #family-row  (target: modelo clonado)
│ Nome [__________] Parentesco [Pai ▾] Tel [_] (🗑)│ ← clone        [data-ttsc-repeater-delete]
└─────────────────────────────────────────────┘    ┘
[ + Adicionar responsável ]   ← button[data-ttsc-repeater]  (fica disabled no limite)
```

| Parte | Atributo | Obrigatório |
|---|---|---|
| Gatilho "Adicionar" | `button[data-ttsc-repeater="true"]` — é o elemento da instância | sim |
| Modelo | `data-ttsc-repeater-target="#family-row"` → elemento clonado com `cloneNode(true)` | sim |
| Wrapper | `data-ttsc-repeater-wrapper="#family-list"` → recebe os clones; **cada filho direto conta como uma linha** | sim |
| Limite | `data-ttsc-repeater-limit="5"` (0 = sem limite) → gatilho recebe `disabled` ao atingir | não |
| Remover | `[data-ttsc-repeater-delete]` dentro de cada linha; desabilitado (`disabled` + `aria-disabled`) quando só resta 1 linha | recomendado |

## Estados

| Estado | Quem aplica |
|---|---|
| Limite atingido | ttscui: `disabled` no gatilho (volta ao remover) |
| Última linha | ttscui: botão remover com `disabled`/`aria-disabled="true"` |
| Linha nova | sua função no evento `add`: limpa valores, reindexa `name`, foca o primeiro campo |
| Linha inválida | `aria-invalid="true"` nos campos da linha (padrão do [Input](../Input/README.md)) |

## API

Conferido em `src/components/repeater/repeater.ts` (global `ttscRepeater` / `TTSC.Repeater`).

| Opção (`data-ttsc-repeater-*`) | Padrão | Descrição |
|---|---|---|
| `target` | `""` | seletor do elemento modelo (clonado por inteiro, **com os valores atuais dos campos** e o mesmo `id`) |
| `wrapper` | `""` | seletor do contêiner; sem wrapper a instância não liga |
| `limit` | `0` | máximo de filhos diretos no wrapper |

| Método | Descrição |
|---|---|
| `ttscRepeater.getInstance(el)` / `getOrCreateInstance(el, config?)` | instância do gatilho |
| `ttscRepeater.init()` / `createInstances()` | liga todos os `[data-ttsc-repeater]` |
| `instance.add()` | adiciona uma linha (respeita o limite) |
| `instance.on('add', fn)` / `off('add', id)` | callback `fn({ element })` |
| `instance.dispose()` | remove o listener de exclusão |

| Evento DOM (no gatilho, bubbles, **sem prefixo**) | `event.detail.payload` |
|---|---|
| `add` | `{ element }` — a linha recém-clonada |

Não há evento de remoção: a remoção acontece no `click` do wrapper; um listener seu no mesmo wrapper, registrado depois de `TTSC.init()`, roda em seguida (ver JS).

## Acessibilidade

- Cada linha é um `<fieldset>` com `<legend class="sr-only">Responsável 2</legend>` (reindexado no JS) e rótulos reais por campo.
- Botão remover só-ícone com `aria-label="Remover responsável 2"`.
- Após adicionar, mova o foco para o primeiro campo da nova linha; após remover, para o gatilho.
- Anuncie a contagem num `aria-live="polite"` ("2 de 5 responsáveis").

## Modelos

### HTML

```html
<!-- Drawer "Aluno" › aba Família — resources/views/app/partials/academic/student-family.php -->
<div class="flex flex-col gap-3">
  <div class="flex items-center justify-between">
    <span class="ttsc-form-label">Responsáveis e contatos</span>
    <span class="text-xs text-muted-foreground" id="family-count" aria-live="polite"></span>
  </div>

  <div id="family-list" class="flex flex-col gap-2">
    <?php foreach ($family ?: [[]] as $i => $m): ?>
    <fieldset class="ttsc-repeater-row" <?= $i === 0 ? 'id="family-row"' : '' ?>>
      <legend class="sr-only">Responsável <?= $i + 1 ?></legend>
      <input type="hidden" name="family[<?= $i ?>][uuid]" value="<?= $this->e($m['uuid'] ?? '') ?>">
      <input class="ttsc-input" name="family[<?= $i ?>][full_name]" aria-label="Nome" required
             value="<?= $this->e($m['full_name'] ?? '') ?>" placeholder="Nome completo">
      <select class="ttsc-select" name="family[<?= $i ?>][relationship]" aria-label="Parentesco">
        <?php foreach (['mother' => 'Mãe', 'father' => 'Pai', 'guardian' => 'Responsável legal', 'grandparent' => 'Avô/Avó', 'other' => 'Outro'] as $v => $l): ?>
          <option value="<?= $v ?>" <?= ($m['relationship'] ?? '') === $v ? 'selected' : '' ?>><?= $l ?></option>
        <?php endforeach; ?>
      </select>
      <input class="ttsc-input" name="family[<?= $i ?>][phone]" aria-label="Telefone" inputmode="tel"
             value="<?= $this->e($m['phone'] ?? '') ?>" placeholder="(11) 90000-0000">
      <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon" data-ttsc-repeater-delete
              aria-label="Remover responsável <?= $i + 1 ?>"><i class="fa-light fa-trash"></i></button>
    </fieldset>
    <?php endforeach; ?>
  </div>

  <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-sm self-start" id="family-add"
          data-ttsc-repeater="true" data-ttsc-repeater-target="#family-row"
          data-ttsc-repeater-wrapper="#family-list" data-ttsc-repeater-limit="5">
    <i class="fa-light fa-plus"></i> Adicionar responsável
  </button>
</div>
```

### CSS

```css
/* Extensão do chassi: linha do repeater em grid, alinhada e com separação por token */
.ttsc-repeater-row {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 1.2fr) minmax(0, 1.3fr) auto;
  gap: var(--ttsc-space-2);
  align-items: center;
  margin: 0; padding: var(--ttsc-space-2);
  border: 1px solid var(--ttsc-border-soft);
  border-radius: var(--ttsc-radius-control);
  background: var(--ttsc-surface);
}
.ttsc-repeater-row:focus-within { border-color: var(--ttsc-border-strong); }
.ttsc-repeater-row.is-new { animation: ttsc-repeater-in .2s ease-out; }
@keyframes ttsc-repeater-in { from { opacity: 0; transform: translateY(-4px); } }
```

### JS

```js
// assets/js/core/ttsc.repeater-rows.js — limpa clones, reindexa names (family[0][...]) e mantém contagem
TTSC.init();
const trigger = document.getElementById('family-add');
const list = document.getElementById('family-list');
const count = document.getElementById('family-count');
const limit = Number(trigger.dataset.ttscRepeaterLimit) || 0;

function reindex() {
  [...list.children].forEach((row, i) => {
    if (i > 0) row.removeAttribute('id');                 // só o modelo mantém o id
    row.querySelector('legend').textContent = `Responsável ${i + 1}`;
    row.querySelector('[data-ttsc-repeater-delete]').setAttribute('aria-label', `Remover responsável ${i + 1}`);
    row.querySelectorAll('[name]').forEach((field) => {
      field.name = field.name.replace(/^family\[\d+\]/, `family[${i}]`);
    });
  });
  count.textContent = `${list.children.length} de ${limit} responsáveis`;
}

trigger.addEventListener('add', (event) => {
  const row = event.detail.payload.element;
  row.querySelectorAll('input').forEach((input) => { input.value = ''; input.removeAttribute('aria-invalid'); });
  row.querySelectorAll('select').forEach((select) => { select.selectedIndex = 0; });
  row.classList.add('is-new');
  reindex();
  row.querySelector('input:not([type=hidden])').focus();
});

// Remoção: o ttscui remove a linha no click do wrapper; este listener roda depois dele
list.addEventListener('click', (event) => {
  if (!event.target.closest('[data-ttsc-repeater-delete]')) return;
  if (!list.querySelector('#family-row')) list.firstElementChild.id = 'family-row'; // modelo removido? promove o 1º
  reindex();
  trigger.focus();
});

reindex();
```

### SQL

Tabela filha real do tenant: `user_family_members` (`user_uuid` → aluno em `users`). O controller recebe `family[i][…]`, valida, e grava tudo numa transação: apaga (soft delete) quem saiu e insere/atualiza o resto.

```sql
-- Carrega as linhas do repeater
SELECT f.uuid, f.full_name, f.relationship, f.phone, f.email
  FROM user_family_members f
 WHERE f.user_uuid = :student_uuid
   AND f.deleted_at IS NULL
 ORDER BY f.created_at, f.id;

-- Salvar (dentro de BEGIN … COMMIT no PHP)
-- 1) Soft delete das linhas removidas na tela (uuids enviados ficam fora da lista)
UPDATE user_family_members
   SET deleted_at = NOW()
 WHERE user_uuid = :student_uuid
   AND deleted_at IS NULL
   AND uuid NOT IN (:kept_uuid_1, :kept_uuid_2);   -- lista montada com placeholders; vazia → sem NOT IN

-- 2) Linhas novas: INSERT múltiplo (um grupo de placeholders por linha nova)
INSERT INTO user_family_members (uuid, user_uuid, full_name, relationship, phone)
VALUES (UUID(), :student_uuid, :name_0, :rel_0, :phone_0),
       (UUID(), :student_uuid, :name_1, :rel_1, :phone_1);

-- 3) Linhas existentes editadas
UPDATE user_family_members
   SET full_name = :full_name, relationship = :relationship, phone = :phone, updated_at = NOW()
 WHERE uuid = :uuid
   AND user_uuid = :student_uuid
   AND deleted_at IS NULL;
```

O PHP monta `VALUES (...), (...)` com placeholders gerados (`:name_{$i}`) — nunca concatena valores. O resultado do SELECT vira `$family` na view; lista vazia renderiza uma linha em branco (`$family ?: [[]]`), que também serve de modelo.

## Faça / Não faça

- **Faça:** `name` indexado (`family[0][phone]`) e reindexação no `add`/remover; limpar os valores do clone.
- **Faça:** `limit` coerente com a regra de negócio e validação igual no servidor.
- **Não faça:** usar como modelo um elemento com `class="hidden"` (o clone nasce escondido) ou um `<template>` (o ttscui clona o nó, não o conteúdo); `name="family[][phone]"` (quebra o agrupamento por linha).
