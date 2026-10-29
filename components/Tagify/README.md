# Tagify

Campo de tags com Tagify 4.17.9: tags livres ou restritas a uma whitelist (etiquetas reais de `crm_tags`, com cor), dropdown de sugestões e tags inválidas sinalizadas, tematizado por variáveis CSS ligadas aos tokens.

## Quando usar

- Etiquetar registros com um vocabulário controlado: etiquetas de leads e negociações do CRM (`crm_tags`).
- Listas curtas de termos livres digitados pelo usuário: interesses do aluno, palavras-chave de um documento.
- **Não use** para escolher entidades com muitos atributos (aluno, curso): use [Select2](../Select2/README.md) com AJAX.
- **Não use** para seleção hierárquica: use [MultiSelectSplitter](../MultiSelectSplitter/README.md).
- Para mostrar etiquetas sem edição, prefira [Badge](../Badge/README.md) em vez de Tagify `readonly`.

## Anatomia

```
Etiquetas do CRM
┌ tags.tagify ─────────────────────────────────────────────┐
│ (● Bolsista ×) (● Visita agendada ×) ┊● Promoção 2027┊ × │  tag / tag inválida (tracejado)
│ |cursor                                                   │  span.tagify__input
└───────────────────────────────────────────────────────────┘
┌ .tagify__dropdown ─────────────────┐
│ ● Transferência          31 leads  │  .tagify__dropdown__item(--active)
└────────────────────────────────────┘
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Origem | `<input name>` (ou `<textarea>`) com `<label for>` | sim |
| Container | `tags.tagify` (gerado; o input original fica oculto e recebe o valor) | gerado |
| Tag | `tag.tagify__tag` > `x.tagify__tag__removeBtn` + `div > span.tagify__tag-text` | gerado |
| Tag inválida | `tag.tagify--notAllowed[aria-invalid=true]` | gerado |
| Dropdown | `.tagify__dropdown` > `.tagify__dropdown__item` | gerado |
| Ponto de cor | `.tt-dot` (template personalizado, cor de `crm_tags.color`) | não |

## Variantes

| Variante | Opções | Tokens |
|---|---|---|
| Livre | `delimiters: ','`, `maxTags`, `dropdown.enabled: false` | tag `ttsc-surface-2`, texto `ttsc-text` |
| Whitelist | `whitelist`, `enforceWhitelist: true`, `dropdown.enabled: 0` | dropdown `ttsc-surface`, item ativo `ttsc-canvas-2` |
| Inválida mantida | `skipInvalid: false`, `keepInvalidTags: true` | borda tracejada `ttsc-danger`, texto `ttsc-danger-text` |
| Somente leitura | atributo `readonly` | fundo `ttsc-canvas-2`, sem × |
| Foco | automático | borda `ttsc-accent` + halo `ttsc-accent-soft` |

## API

Opções (Tagify 4.17.9): `whitelist` (strings ou objetos `{ id, value, … }`), `enforceWhitelist`, `blacklist`, `maxTags`, `delimiters`, `pattern` (RegExp de validação), `duplicates`, `skipInvalid`, `keepInvalidTags`, `editTags`, `mode` (`'select'`, `'mix'`), `tagTextProp`, `originalInputValueFormat(values)` (formato gravado no input original; padrão é JSON), `dropdown: { enabled, maxItems, closeOnSelect, highlightFirst, searchKeys, position }`, `templates: { tag, dropdownItem }`, `transformTag(tagData)`, `validate(tagData)`.

Métodos: `addTags(tags, clearInput?, skipInvalid?)`, `removeTags(tags?)`, `removeAllTags()`, `loadOriginalValues(value)`, `getTagElmByValue(v)`, `settings.whitelist = [...]` + `dropdown.show(term)` (whitelist remota), `dropdown.hide()`, `setReadonly(bool)`, `setDisabled(bool)`, `destroy()`. Valor atual: `tagify.value` (array de objetos).

Eventos (`tagify.on(nome, fn)`, dado em `e.detail.data`): `add`, `remove`, `change` (no input original), `invalid` (`e.detail.message`: `'already exists'`, `'not allowed'`, `'number of tags exceeded'`), `input` (para buscar whitelist no servidor), `edit:updated`, `dropdown:select`, `focus`, `blur`.

## Acessibilidade

- O botão × recebe `role="button"` e `aria-label="Remover <etiqueta>"` (template acima); `Backspace` remove a última tag.
- Teclado: `Enter`/`,` cria a tag, setas navegam no dropdown, `Esc` fecha, duplo clique edita (`editTags`).
- Tag inválida tem `aria-invalid="true"`, borda tracejada **e** texto em `ttsc-danger-text` (não só cor).
- A cor da etiqueta é um ponto decorativo ao lado do texto; o texto continua `ttsc-text` (contraste independente da cor do banco).
- Mantenha `<label for>` apontando para o input original; o Tagify copia o `placeholder`.

## Modelos

### HTML

```html
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="lead-tags">Etiquetas do CRM</label>
  <input id="lead-tags" name="tag_uuids" placeholder="Buscar etiqueta..." data-ttsc-tagify="whitelist"
         value="<?= $this->e(implode(',', array_column($leadTags, 'id'))) ?>">
  <script type="application/json" id="lead-tags-whitelist"><?= json_encode($crmTags, JSON_HEX_TAG | JSON_HEX_AMP) ?></script>
  <span class="ds-note">Somente etiquetas cadastradas em CRM › Etiquetas.</span>
</div>

<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="lead-interests">Interesses</label>
  <input id="lead-interests" name="interests" data-ttsc-tagify="free" placeholder="Digite e pressione Enter"
         value="<?= $this->e($lead['interests'] ?? '') ?>">
</div>
```

### CSS

```css
/* assets/css/ttsc.tagify.css — carregar depois de vendor/tagify/tagify.css */
.tagify {
  --tags-border-color: var(--ttsc-border);
  --tags-hover-border-color: var(--ttsc-border-strong);
  --tags-focus-border-color: var(--ttsc-accent);
  --tags-disabled-bg: var(--ttsc-surface-2);
  --tag-bg: var(--ttsc-surface-2);
  --tag-hover: var(--ttsc-border);
  --tag-text-color: var(--ttsc-text);
  --tag-text-color--edit: var(--ttsc-text);
  --tag-pad: .25em .6em;
  --tag-border-radius: var(--ttsc-radius-pill);
  --tag-invalid-color: var(--ttsc-danger);
  --tag-invalid-bg: var(--ttsc-surface);
  --tag-remove-bg: var(--ttsc-surface-2);
  --tag-remove-btn-color: var(--ttsc-text-muted);
  --tag-remove-btn-bg--hover: var(--ttsc-danger);
  --input-color: var(--ttsc-text);
  --placeholder-color: var(--ttsc-text-muted);
  --placeholder-color-focus: var(--ttsc-text-muted);
  --readonly-striped: 0;
  min-height: 36px; padding: 2px 4px; font-size: 13px;
  background: var(--ttsc-surface); border-radius: var(--ttsc-radius-control); box-shadow: var(--ttsc-shadow-xs);
}
.tagify--focus { box-shadow: 0 0 0 3px var(--ttsc-accent-soft); }
.tagify__tag > div { display: inline-flex; align-items: center; }
.tagify__tag .tt-dot { width: 8px; height: 8px; border-radius: 50%; margin-inline-end: 6px; }
.tagify__tag__removeBtn:hover { color: var(--ttsc-surface); }
.tagify__tag.tagify--notAllowed div > span { opacity: 1 !important; }
.tagify__tag.tagify--notAllowed > div { outline: 1px dashed var(--ttsc-danger); outline-offset: -1px; border-radius: var(--ttsc-radius-pill); }
.tagify__tag.tagify--notAllowed > div::before { box-shadow: 0 0 0 1.1em var(--ttsc-surface) inset !important; }
.tagify__tag.tagify--notAllowed .tagify__tag-text { color: var(--ttsc-danger-text); }
.tagify--readonly { background: var(--ttsc-canvas-2); }
.tagify__dropdown { --tagify-dd-bg-color: var(--ttsc-surface); --tagify-dd-color-primary: var(--ttsc-accent-soft); color: var(--ttsc-text); font-size: 13px; }
.tagify__dropdown__wrapper { border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-sm); box-shadow: var(--ttsc-shadow-md); background: var(--ttsc-surface); }
.tagify__dropdown__item { display: flex; align-items: center; gap: 8px; margin: 2px 4px; padding: 6px 8px; border-radius: 6px; color: var(--ttsc-text); }
.tagify__dropdown__item--active { background: var(--ttsc-canvas-2); color: var(--ttsc-text); }
.tagify__dropdown__item small { margin-inline-start: auto; color: var(--ttsc-text-muted); font-size: 11px; }
```

### JS

```js
// assets/js/core/ttsc.tagify.js — requer vendor/tagify/tagify.min.js
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

export function initTagify(root = document) {
  root.querySelectorAll('input[data-ttsc-tagify="free"]').forEach((el) => {
    if (el.__tagify) return;
    new Tagify(el, {
      maxTags: 8,
      delimiters: ',',
      dropdown: { enabled: false },
      originalInputValueFormat: (values) => values.map((t) => t.value).join(','),   // grava "Robótica,Futsal"
    });
  });

  root.querySelectorAll('input[data-ttsc-tagify="whitelist"]').forEach((el) => {
    if (el.__tagify) return;
    const whitelist = JSON.parse(document.getElementById(`${el.id}-whitelist`).textContent);   // [{id, value, color, usage_count}]
    const selected = el.value.split(',').filter(Boolean);
    el.value = '';
    const tagify = new Tagify(el, {
      whitelist,
      enforceWhitelist: true,
      skipInvalid: false,
      keepInvalidTags: true,
      dropdown: { enabled: 0, maxItems: 8, closeOnSelect: false, highlightFirst: true, searchKeys: ['value'] },
      originalInputValueFormat: (values) => values.filter((t) => t.id).map((t) => t.id).join(','),  // grava UUIDs
      templates: {
        tag(t) {
          return `<tag title="${esc(t.value)}" contenteditable="false" spellcheck="false" tabIndex="-1"
                    class="${this.settings.classNames.tag} ${t.class || ''}" ${this.getAttributes(t)}>
                    <x title="Remover" class="${this.settings.classNames.tagX}" role="button" aria-label="Remover ${esc(t.value)}"></x>
                    <div><span class="tt-dot" style="background:${esc(t.color || 'var(--ttsc-meta)')}"></span>
                    <span class="${this.settings.classNames.tagText}">${esc(t.value)}</span></div></tag>`;
        },
        dropdownItem(item) {
          return `<div ${this.getAttributes(item)} class="${this.settings.classNames.dropdownItem}" tabindex="0" role="option">
                    <span class="tt-dot" style="background:${esc(item.color)}"></span>${esc(item.value)}
                    <small>${Number(item.usage_count) || 0} leads</small></div>`;
        },
      },
    });
    tagify.addTags(whitelist.filter((t) => selected.includes(t.id)));
    tagify.on('invalid', (e) => {
      if (e.detail.message === 'not allowed') TTSC.Toast.show({ message: 'Etiqueta não cadastrada no CRM.', variant: 'warning' });
    });
  });
}
document.addEventListener('DOMContentLoaded', () => initTagify());
```

### SQL

```sql
-- Whitelist: etiquetas ativas do CRM (as mais usadas primeiro). MariaDB 10.11 / MySQL 8
SELECT t.uuid AS id, t.name AS value, t.color, t.usage_count
  FROM crm_tags t
 WHERE t.status = 'active'
   AND t.deleted_at IS NULL
   AND (t.tenant_id = :tenant_id OR t.tenant_id IS NULL)
 ORDER BY t.usage_count DESC, t.name
 LIMIT 200;

-- Não há tabela de vínculo lead × etiqueta no esquema: DDL proposta
CREATE TABLE IF NOT EXISTS crm_lead_tags (
  id         bigint unsigned NOT NULL AUTO_INCREMENT,
  uuid       char(36) NOT NULL,
  lead_uuid  char(36) NOT NULL,
  tag_uuid   char(36) NOT NULL,
  created_by char(36) DEFAULT NULL,
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_crm_lead_tags_uuid (uuid),
  UNIQUE KEY uk_crm_lead_tags_pair (lead_uuid, tag_uuid),
  KEY idx_crm_lead_tags_tag (tag_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Etiquetas atuais do lead (valor inicial do input)
SELECT t.uuid AS id, t.name AS value, t.color
  FROM crm_lead_tags lt
  JOIN crm_tags t ON t.uuid = lt.tag_uuid AND t.deleted_at IS NULL
 WHERE lt.lead_uuid = :lead_uuid
 ORDER BY t.name;

-- Gravação (transação): só UUIDs que existem e estão ativos entram
DELETE FROM crm_lead_tags WHERE lead_uuid = :lead_uuid AND tag_uuid NOT IN (:t1, :t2);
INSERT IGNORE INTO crm_lead_tags (uuid, lead_uuid, tag_uuid, created_by, created_at)
SELECT UUID(), :lead_uuid, t.uuid, :user_uuid, NOW()
  FROM crm_tags t
 WHERE t.uuid IN (:t1, :t2) AND t.status = 'active' AND t.deleted_at IS NULL;
UPDATE crm_tags t
   SET t.usage_count = (SELECT COUNT(*) FROM crm_lead_tags lt WHERE lt.tag_uuid = t.uuid)
 WHERE t.uuid IN (:t1, :t2);
```

O PHP imprime a whitelist em `<script type="application/json">` e os UUIDs atuais no `value`; o POST chega como `tag_uuids=uuid1,uuid2` (`originalInputValueFormat`), o servidor faz `explode` e expande os placeholders. Tags inválidas nunca são enviadas (sem `id`).

## Faça / Não faça

- **Faça:** gravar UUIDs (whitelist) ou texto normalizado (livre), nunca o JSON padrão do Tagify.
- **Faça:** `enforceWhitelist` para vocabulário controlado e revalidar os UUIDs no servidor.
- **Faça:** escapar `value`/`color` nos templates (vêm do banco).
- **Não faça:** usar a cor da etiqueta como cor do texto (contraste imprevisível); use o ponto.
- **Não faça:** deixar o tema padrão do Tagify (branco) — no escuro o dropdown fica ilegível.
