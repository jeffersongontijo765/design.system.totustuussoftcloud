# Checkbox

Caixa de seleção do chassi (`.ttsc-checkbox`, runtime ttscui) em três tamanhos, com estados marcado, indeterminado, desabilitado e inválido — usada em listas com “selecionar todos”, aceites e filtros múltiplos.

## Quando usar

- Escolhas independentes de sim/não ou múltiplas de uma lista: selecionar matrículas para ação em lote, marcar documentos entregues, aceitar o contrato.
- Coluna de seleção do [DataTable](../DataTable/README.md) (o ttscui usa a mesma classe em `datatable-checkbox`).
- **Não use** para ligar/desligar algo com efeito imediato (curso ativo, notificação por e-mail): use `.ttsc-switch` ([Forms](../Forms/README.md)).
- **Não use** para escolha única entre opções: use `.ttsc-radio`; com muitas opções, `select` ou [Select2](../Select2/README.md).

## Anatomia

```
[✓] Rótulo do item                     input.ttsc-checkbox + label
    Dica opcional                      .ttsc-form-description
[–] Selecionar todos (3 de 12)          :indeterminate (só via JS)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Controle | `input[type=checkbox].ttsc-checkbox` | sim |
| Tamanho | `ttsc-checkbox-sm` (18px) · padrão (20px) · `ttsc-checkbox-lg` (22px) | não |
| Cor neutra | `ttsc-checkbox-mono` (marcado em `--mono` = `ttsc-text`) | não |
| Rótulo | `label.ttsc-label` / `label.ttsc-form-label` com `for`, ou `label` envolvendo | sim |
| Linha | `.ttsc-form-control-inline` (gap 10px, alinhado ao centro) | recomendado |
| Grupo | `fieldset` + `legend` | em listas |

## Variantes

| Variante | Classe | Tokens |
|---|---|---|
| Padrão | `ttsc-checkbox` | borda `--input` (`ttsc-border-strong`), fundo `ttsc-surface`; marcado `ttsc-accent` |
| Mono | `ttsc-checkbox-mono` | marcado `ttsc-text`; check escuro no tema escuro (extensão) |
| Pequeno / grande | `-sm` / `-lg` | mesmos tokens |

## Estados

| Estado | Como aplicar | Visual |
|---|---|---|
| Marcado | `checked` (ou `aria-checked="true"` em `role=checkbox` custom) | fundo `ttsc-accent`, check (extensão: `ttsc-accent-on`) |
| Indeterminado | `el.indeterminate = true` (não existe atributo HTML) | fundo `ttsc-accent`, traço |
| Desabilitado | `disabled` | 50%; o `label` seguinte (`+ .ttsc-label` / `+ .ttsc-form-label`) também fica 50% e `not-allowed` |
| Inválido | `aria-invalid="true"` | borda e anel `--destructive` (`ttsc-danger`) |
| Foco | automático | anel 2px `--ring` (`ttsc-accent`) com offset 2px |

## API

Sem JavaScript no ttscui para o checkbox isolado (é CSS sobre o input nativo). Comportamentos de lista são da implementação TTSC abaixo:

| Atributo | Elemento | Efeito |
|---|---|---|
| `data-ttsc-check-all="#lista"` | checkbox mestre | marca/desmarca todos os `data-ttsc-check-item` da lista; fica `indeterminate` em seleção parcial |
| `data-ttsc-check-item` | itens | participam da contagem |
| `data-ttsc-check-count` | qualquer | recebe “3 de 12 selecionadas” |

| Evento | Alvo | `detail` |
|---|---|---|
| `ttsc.check.change` | lista | `{ checked: string[], total }` (valores dos itens marcados) |
| `change` nativo | cada input | continua disponível |

## Acessibilidade

- Sempre com `<label for>` (ou envolvendo): a área de clique inclui o texto.
- Grupo com `fieldset` + `legend` (“Documentos entregues”).
- Indeterminado é anunciado como “misto” pelos leitores; mantenha o texto de contagem com `aria-live="polite"`.
- Obrigatório (aceite): `required` + mensagem `.ttsc-form-message` ligada por `aria-describedby`.
- Contraste do check: o runtime desenha check **branco** sobre `#3ecf8e` (1,9:1); a extensão abaixo troca para `ttsc-accent-on` (9,6:1). A borda vazia em `ttsc-border-strong` sobre branco tem 1,5:1 — use `ttsc-border-prominent` em fundos `ttsc-canvas-2` se precisar de mais contraste de contorno.

## Modelos

### HTML

```html
<fieldset class="ttsc-check-list">
  <legend>Matrículas da turma ADM-2026-1N</legend>
  <div class="ttsc-form-control-inline">
    <input type="checkbox" class="ttsc-checkbox" id="check-all" data-ttsc-check-all="#enrollment-list" aria-describedby="check-count">
    <label class="ttsc-form-label" for="check-all">Selecionar todas</label>
    <span class="ttsc-check-count" id="check-count" data-ttsc-check-count aria-live="polite"></span>
  </div>
  <ul id="enrollment-list">
    <?php foreach ($enrollments as $e): ?>
      <li class="ttsc-form-control-inline">
        <input type="checkbox" class="ttsc-checkbox ttsc-checkbox-sm" id="enr-<?= $this->e($e['uuid']) ?>"
               name="enrollment_uuids[]" value="<?= $this->e($e['uuid']) ?>" data-ttsc-check-item
               <?= $e['status'] !== 'active' ? 'disabled' : '' ?>>
        <label class="ttsc-label" for="enr-<?= $this->e($e['uuid']) ?>"><?= $this->e($e['code']) ?> · <?= $this->e($e['student_name']) ?></label>
      </li>
    <?php endforeach ?>
  </ul>
</fieldset>

<!-- Aceite obrigatório -->
<div class="ttsc-form-item">
  <div class="ttsc-form-control-inline">
    <input type="checkbox" class="ttsc-checkbox" id="accept-contract" name="accept" required aria-describedby="accept-error">
    <label class="ttsc-form-label" for="accept-contract">Li e aceito o contrato de prestação de serviços educacionais</label>
  </div>
  <div class="ttsc-form-message" id="accept-error" role="alert">É preciso aceitar o contrato para concluir a matrícula.</div>
</div>
```

### CSS

```css
/* Ponte (bundle.css): marcado = --primary (= --ttsc-accent); borda = --input (= --ttsc-border-strong); inválido = --destructive */
/* Check escuro sobre o verde: o path é o mesmo do runtime, com stroke na cor de --ttsc-accent-on (#0f0f0f) —
   data-URI não lê variáveis CSS, então este hex espelha o token. */
.ttsc-checkbox:checked:not(.ttsc-checkbox-mono) {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath fill='none' stroke='%230f0f0f' stroke-linecap='round' stroke-linejoin='round' stroke-width='2.2' d='M5 10.5l3.2 3.2L15 7'/%3E%3C/svg%3E");
}
.ttsc-checkbox:indeterminate:not(.ttsc-checkbox-mono) {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath fill='none' stroke='%230f0f0f' stroke-linecap='round' stroke-width='2.2' d='M6 10h8'/%3E%3C/svg%3E");
}
/* Mono no tema escuro: fundo vira --ttsc-text (claro), o check branco do runtime some — stroke = --ttsc-surface escuro (#1c1c1c) */
:is([data-theme="dark"], .dark) .ttsc-checkbox-mono:checked {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath fill='none' stroke='%231c1c1c' stroke-linecap='round' stroke-linejoin='round' stroke-width='2.2' d='M5 10.5l3.2 3.2L15 7'/%3E%3C/svg%3E");
}
.ttsc-check-list legend { font-size: 12px; font-weight: 500; color: var(--ttsc-text-muted); padding: 0 4px; }
.ttsc-check-list ul { list-style: none; margin: 0; padding: 0; }
.ttsc-check-list li { padding: 6px 0; border-top: 1px solid var(--ttsc-border-soft); }
.ttsc-check-count { margin-inline-start: auto; font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-form-message { color: var(--ttsc-danger-text); }
```

### JS

```js
// assets/js/core/ttsc.check-list.js — implementação TTSC: "selecionar todos" com indeterminado
export function initCheckAll(master) {
  const list = document.querySelector(master.dataset.ttscCheckAll);
  const items = () => [...list.querySelectorAll('[data-ttsc-check-item]:not(:disabled)')];
  const counter = master.closest('fieldset, form, body').querySelector('[data-ttsc-check-count]');

  function sync() {
    const all = items(), on = all.filter((i) => i.checked);
    master.checked = all.length > 0 && on.length === all.length;
    master.indeterminate = on.length > 0 && on.length < all.length;
    if (counter) counter.textContent = `${on.length} de ${all.length} selecionadas`;
    list.dispatchEvent(new CustomEvent('ttsc.check.change', {
      bubbles: true, detail: { checked: on.map((i) => i.value), total: all.length },
    }));
  }

  master.addEventListener('change', () => {
    items().forEach((i) => { i.checked = master.checked; });
    sync();
  });
  list.addEventListener('change', (e) => { if (e.target.matches('[data-ttsc-check-item]')) sync(); });

  // Shift+clique marca o intervalo
  let last = null;
  list.addEventListener('click', (e) => {
    const box = e.target.closest('[data-ttsc-check-item]');
    if (!box) return;
    if (e.shiftKey && last) {
      const all = items(), [a, b] = [all.indexOf(last), all.indexOf(box)].sort((x, y) => x - y);
      all.slice(a, b + 1).forEach((i) => { i.checked = box.checked; });
      sync();
    }
    last = box;
  });
  sync();
}

document.querySelectorAll('[data-ttsc-check-all]').forEach(initCheckAll);

// Ação em lote: envia os selecionados
document.querySelector('#btn-lock')?.addEventListener('click', async () => {
  const uuids = [...document.querySelectorAll('[data-ttsc-check-item]:checked')].map((i) => i.value);
  if (!uuids.length) return;
  await fetch('/academic/enrollments/bulk-lock', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': document.querySelector('[name="_token"]').value },
    body: JSON.stringify({ uuids }),
  });
});
```

### SQL

Lista da turma para a seleção, e a ação em lote que os checkboxes disparam:

```sql
-- Itens da lista (desabilita os que não estão ativos)
SELECT e.uuid, e.code, e.status, c.name AS course_name
  FROM enrollments e
  JOIN courses c ON c.uuid = e.course_uuid AND c.deleted_at IS NULL
 WHERE e.deleted_at IS NULL
   AND e.class_uuid = :class_uuid
 ORDER BY e.code;

-- Trancar as selecionadas (o PHP expande :uuid_0, :uuid_1… a partir do array, máx. 500)
UPDATE enrollments
   SET status = 'locked'
 WHERE uuid IN (:uuid_0, :uuid_1, :uuid_2)
   AND unit_uuid = :unit_uuid
   AND status = 'active'
   AND deleted_at IS NULL;
```

O controller lê `enrollment_uuids[]`, gera um placeholder por item (nunca concatena valores), executa dentro de transação e devolve `rowCount()` para o toast (“3 matrículas trancadas”). Itens que mudaram de status entre a tela e o envio são ignorados pelo filtro `status = 'active'`.

## Faça / Não faça

- **Faça:** rótulo clicável e `fieldset` em grupos.
- **Faça:** `indeterminate` no mestre quando a seleção for parcial.
- **Não faça:** checkbox para ação imediata — use switch.
- **Não faça:** confiar no check branco do runtime sobre o verde; aplique a extensão de contraste.
