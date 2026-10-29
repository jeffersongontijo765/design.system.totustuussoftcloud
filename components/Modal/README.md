# Modal

Diálogo sobreposto do ttscui (`data-ttsc-modal`) com backdrop, cabeçalho, corpo e rodapé — usado para confirmações curtas, como a exclusão de uma matrícula.

> Também listado em: **Base › Modal**.

## Quando usar

- Confirmar ação destrutiva ou irreversível: “Excluir matrícula?”, “Cancelar boleto?”, “Fechar diário da turma?”.
- Decisão rápida que bloqueia o fluxo (aceitar termo, escolher unidade antes de continuar).
- Busca global (`Ctrl K`) em tela cheia, como o `search_modal` do chassi.
- Formulários de criação/edição → [Drawer](../Drawer/README.md) (padrão do CRUD).
- Mensagem que não exige decisão → toast ou alerta ([Dismiss](../Dismiss/README.md)).

## Anatomia

```
┌──────────── backdrop [data-ttsc-modal-backdrop] (ttsc-scrim, blur 4px) ─────────────┐
│        ┌ .ttsc-modal-content (max-width 440px) ──────────────────┐                  │
│        │ .ttsc-modal-header  (!) Excluir matrícula?          [x] │                  │
│        ├─────────────────────────────────────────────────────────┤                  │
│        │ .ttsc-modal-body   impacto + campo de confirmação       │                  │
│        ├─────────────────────────────────────────────────────────┤                  │
│        │ .ttsc-modal-footer            [Cancelar] [Excluir]      │                  │
│        └─────────────────────────────────────────────────────────┘                  │
└──────────── .ttsc-modal[data-ttsc-modal] (fixed, inset 0, rola) ─────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Raiz | `div#id.ttsc-modal[data-ttsc-modal="true"]` (escondido por `:not(.open)`) | sim |
| Centralizado | `.ttsc-modal-center` na raiz | não |
| Caixa | `.ttsc-modal-content` + largura (`.ttsc-modal-sm` 440px, extensão) | sim |
| Cabeçalho | `.ttsc-modal-header` > `h3.ttsc-modal-title` + `button.ttsc-modal-close[data-ttsc-modal-dismiss="true"]` | sim |
| Corpo | `.ttsc-modal-body` (rola) | sim |
| Rodapé | `.ttsc-modal-footer` (ações; `justify-between`) | sim |
| Gatilho | `[data-ttsc-modal-toggle="#id"]` | sim |
| Foco inicial | `[data-ttsc-modal-input-focus]` | recomendado |

## Variantes

| Variante | Configuração | Uso | Tokens |
|---|---|---|---|
| Confirmação destrutiva | `.ttsc-modal-center` + `backdrop-static` + botão `ttsc-btn-destructive` | excluir/cancelar | ícone em círculo `ttsc-danger` 10% + `ttsc-danger-text`; botão `ttsc-danger` com texto branco (4,8:1) |
| Topo | sem `.ttsc-modal-center`; `.ttsc-modal-content` com `margin-top` | busca global, listas | — |
| Fit | `.ttsc-modal-fit` | conteúdo sem padding (imagem, vídeo) | — |
| Persistente | `data-ttsc-modal-persistent="true"` | aceite obrigatório (nem backdrop nem clique fora fecham) | — |

Caixa: fundo `--popover` (= `ttsc-surface`), borda `ttsc-border`, raio `--radius`, sombra (extensão `ttsc-shadow-popover`); backdrop do runtime preto 30% + blur (extensão `ttsc-scrim`).

## API

Opções (`data-ttsc-modal-<opção>` na raiz):

| Opção | Padrão | Efeito |
|---|---|---|
| `backdrop` | `true` | cria `[data-ttsc-modal-backdrop]` no `body` |
| `backdropStatic` | `false` | clique no backdrop/fora da caixa não fecha |
| `backdropClass` | `ttsc-modal-backdrop` | classe do backdrop |
| `persistent` | `false` | idem ao estático, também sem backdrop |
| `disableScroll` | `true` | trava a rolagem do `body` |
| `focus` | `true` | foca `[data-ttsc-modal-input-focus]` ao abrir |
| `zindex` | `90` | z-index mínimo (sobe acima do maior da página) — no chassi use `1060` (`--ttsc-z-modal`) |
| `hiddenClass` | `hidden` | classe removida ao abrir |
| `keyboard` | `true` | declarado; o `Esc` fecha sempre no runtime atual |

Atributos de ação: `data-ttsc-modal-toggle="#id"` (abre/fecha; guarda o gatilho), `data-ttsc-modal-dismiss="true"` (fecha o modal ancestral).

Métodos (`ttscModal.getInstance(el)` / `TTSC.Modal.getOrCreateInstance(el)`): `show(gatilho?)`, `hide()`, `toggle()`, `isOpen()`, `getTargetElement()` (o gatilho que abriu); estático `ttscModal.hide()` fecha todos. Abrir um modal fecha os demais.

Eventos (CustomEvent na raiz, `bubbles`): `toggle`, `show` (cancelável), `shown`, `hide` (cancelável), `hidden`.

## Acessibilidade

- O JS aplica `role="dialog"`, `aria-modal="true"` e `tabindex="-1"`; use `role="alertdialog"` em confirmações (sobrescreva em `shown`) e `aria-labelledby`/`aria-describedby` apontando para título e texto.
- Foco inicial no botão **seguro** (“Cancelar”) ou no campo de confirmação; ao fechar, devolva o foco a `getTargetElement()`.
- `Esc` fecha; em exclusão use `backdrop-static` para evitar fechar por clique acidental, mas mantenha `Esc` e “Cancelar”.
- O título diz a ação e o objeto (“Excluir a matrícula MAT-2026-0381?”); o botão repete o verbo (“Excluir matrícula”), nunca “OK”/“Sim”.
- Contraste: título `ttsc-text`, corpo `ttsc-text-2`; botão destrutivo branco sobre `ttsc-danger` 4,8:1.

## Modelos

### HTML

```html
<!-- Gatilho na linha (ou no dropdown de ações) -->
<button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" data-ttsc-modal-toggle="#modal-excluir"
        data-uuid="<?= $this->e($row['uuid']) ?>" data-code="<?= $this->e($row['code']) ?>" aria-label="Excluir matrícula <?= $this->e($row['code']) ?>">
  <i class="fa-light fa-trash"></i>
</button>

<div class="ttsc-modal ttsc-modal-center" id="modal-excluir" data-ttsc-modal="true" data-ttsc-modal-backdrop-static="true"
     data-ttsc-modal-zindex="1060" aria-labelledby="modal-excluir-title" aria-describedby="modal-excluir-desc">
  <div class="ttsc-modal-content ttsc-modal-sm">
    <div class="ttsc-modal-header">
      <div class="flex items-center gap-3">
        <span class="ttsc-modal-icon ttsc-modal-icon-danger"><i class="fa-light fa-triangle-exclamation"></i></span>
        <h3 class="ttsc-modal-title" id="modal-excluir-title">Excluir a matrícula <span data-field="code"></span>?</h3>
      </div>
      <button type="button" class="ttsc-modal-close" data-ttsc-modal-dismiss="true" aria-label="Fechar"><i class="fa-light fa-xmark"></i></button>
    </div>
    <form class="ttsc-modal-body" id="form-excluir" method="post">
      <input type="hidden" name="_token" value="<?= $this->e($csrf) ?>">
      <input type="hidden" name="uuid">
      <p id="modal-excluir-desc">A matrícula sai das listagens e do diário. <strong data-field="impact"></strong> ficam preservados no histórico.</p>
      <label class="ttsc-form-label" for="confirm-code">Digite o código para confirmar</label>
      <input class="ttsc-input" id="confirm-code" autocomplete="off" data-ttsc-modal-input-focus>
    </form>
    <div class="ttsc-modal-footer">
      <button type="button" class="ttsc-btn ttsc-btn-ghost" data-ttsc-modal-dismiss="true">Cancelar</button>
      <button type="submit" form="form-excluir" class="ttsc-btn ttsc-btn-destructive" disabled><i class="fa-light fa-trash"></i> Excluir matrícula</button>
    </div>
  </div>
</div>
```

### CSS

```css
/* Ponte (bundle.css) */
:root { --popover: var(--ttsc-surface); --popover-foreground: var(--ttsc-text); --destructive: var(--ttsc-danger); }
.ttsc-modal-backdrop { background-color: var(--ttsc-scrim); }

/* Extensão TTSC */
.ttsc-modal-sm { width: 100%; max-width: 440px; }
.ttsc-modal-md { width: 100%; max-width: 600px; }
.ttsc-modal-content { box-shadow: var(--ttsc-shadow-popover); border-radius: var(--ttsc-radius-control); }
.ttsc-modal-title { font-size: 15px; color: var(--ttsc-text); margin: 0; }
.ttsc-modal-body { display: flex; flex-direction: column; gap: var(--ttsc-space-2); color: var(--ttsc-text-2); font-size: 13px; line-height: 1.6; }
.ttsc-modal-footer { justify-content: flex-end; background: var(--ttsc-canvas); border-radius: 0 0 var(--ttsc-radius-control) var(--ttsc-radius-control); }
.ttsc-modal-close { color: var(--ttsc-text-muted); background: none; border: 0; }
.ttsc-modal-icon { display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: var(--ttsc-radius-pill); flex: 0 0 auto; }
.ttsc-modal-icon-danger { background: color-mix(in oklab, var(--ttsc-danger) 10%, var(--ttsc-surface)); color: var(--ttsc-danger-text); }
```

### JS

```js
// assets/js/core/ttsc.confirm-delete.js — modal de confirmação de exclusão do CRUD
const modalEl = document.querySelector('#modal-excluir');
const modal = TTSC.Modal.getOrCreateInstance(modalEl);
const form = modalEl.querySelector('form');
const submit = modalEl.querySelector('[type="submit"]');
const confirmInput = modalEl.querySelector('#confirm-code');

modalEl.addEventListener('show', async () => {
  const trigger = modal.getTargetElement();
  form.uuid.value = trigger.dataset.uuid;
  modalEl.querySelectorAll('[data-field="code"]').forEach((el) => { el.textContent = trigger.dataset.code; });
  confirmInput.value = '';
  submit.disabled = true;
  const res = await fetch(`/academic/enrollments/${trigger.dataset.uuid}/impact`, { headers: { Accept: 'application/json' } });
  const impact = res.ok ? await res.json() : null;
  modalEl.querySelector('[data-field="impact"]').textContent = impact
    ? `${impact.attendance_records} registros de frequência e ${impact.report_cards} boletins` : 'Os registros acadêmicos';
});
modalEl.addEventListener('shown', () => modalEl.setAttribute('role', 'alertdialog'));
modalEl.addEventListener('hidden', () => modal.getTargetElement()?.focus());

confirmInput.addEventListener('input', () => {
  submit.disabled = confirmInput.value.trim().toUpperCase() !== modalEl.querySelector('[data-field="code"]').textContent;
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  submit.disabled = true;
  submit.setAttribute('aria-busy', 'true');
  const res = await fetch(`/academic/enrollments/${form.uuid.value}/delete`, { method: 'POST', body: new FormData(form) });
  submit.removeAttribute('aria-busy');
  if (!res.ok) { submit.disabled = false; return; }
  modal.hide();
  ttscDataTable.getInstance(document.querySelector('#dt-matriculas'))?.reload();
});
```

### SQL

```sql
-- GET /academic/enrollments/{uuid}/impact — o que a exclusão afeta (mostrado no corpo do modal)
SELECT e.uuid, e.code, s.name AS student_name,
       (SELECT COUNT(*) FROM attendance a
         WHERE a.enrollment_uuid = e.uuid)                                    AS attendance_records,
       (SELECT COUNT(*) FROM academic_report_cards rc
         WHERE rc.enrollment_uuid = e.uuid AND rc.deleted_at IS NULL)         AS report_cards
  FROM enrollments e
  JOIN users s ON s.uuid = e.student_uuid
 WHERE e.uuid = :uuid
   AND e.unit_uuid = :unit_uuid
   AND e.deleted_at IS NULL;

-- POST /academic/enrollments/{uuid}/delete — soft delete (nunca DELETE físico)
UPDATE enrollments
   SET deleted_at = NOW()
 WHERE uuid = :uuid
   AND unit_uuid = :unit_uuid
   AND deleted_at IS NULL;
```

O controller responde o impacto como JSON para o evento `show`; no POST valida `_token` e a permissão `academic.enrollments.delete`, executa o `UPDATE` e registra em `audit_logs`. Se `ROW_COUNT() = 0`, devolve 404 (já excluída por outro usuário).

## Faça / Não faça

- **Faça:** título com verbo + objeto; botão destrutivo à direita, “Cancelar” à esquerda dele.
- **Faça:** `backdrop-static` e, para exclusões com histórico, confirmação digitando o código.
- **Faça:** mostrar o impacto (quantos registros dependem) antes de confirmar.
- **Não faça:** modal sobre modal; formulário longo em modal (use [Drawer](../Drawer/README.md)).
- **Não faça:** foco inicial no botão “Excluir”.
