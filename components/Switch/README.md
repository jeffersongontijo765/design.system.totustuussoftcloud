# Switch

Interruptor liga/desliga (`input[type=checkbox].ttsc-switch`) para configurações binárias com efeito imediato ou salvas no formulário, em três tamanhos.

## Quando usar

- Estado binário de **uma** configuração: curso ativo/inativo, receber notificações acadêmicas, exibir turma no portal.
- Em listas de preferências (`user_preferences.notify_*`) e na coluna "Ativo" de tabelas de cadastro.
- Aceite/termos ("Li e concordo") ou seleção de itens em lista → Checkbox (`ttsc-checkbox`).
- Escolha entre duas opções nomeadas (Presencial / EaD) → [Radio](../Radio/README.md) ou [ToggleGroup](../ToggleGroup/README.md).

## Anatomia

```
(●───)  Notificações acadêmicas           label.ttsc-form-control-inline
          Notas, faltas e avisos de turma  input.ttsc-switch + .ttsc-label + .ttsc-form-description
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Interruptor | `input[type=checkbox].ttsc-switch` (`appearance:none`; botão = `::before`) | sim |
| Função ARIA | `role="switch"` | sim |
| Tamanho | `ttsc-switch-sm` (26×18) · padrão (30×20) · `ttsc-switch-lg` (34×22) | não |
| Linha | `label.ttsc-form-control-inline` envolvendo input + texto | recomendado |
| Rótulo | `.ttsc-label` ou `.ttsc-form-label` **imediatamente após** o input (recebe opacidade 0,5 quando `disabled`) | sim |
| Descrição | `.ttsc-form-description` | não |

## Variantes

| Variante | Classe | Uso | Tokens |
|---|---|---|---|
| Pequeno | `ttsc-switch-sm` | coluna "Ativo" em tabela | trilho `--input` → `ttsc-border-strong` |
| Padrão | — | listas de preferências | ligado: `--primary` → `ttsc-accent` |
| Grande | `ttsc-switch-lg` | configuração principal de uma página | botão branco (`--color-white`) com sombra |

## Estados

| Estado | Como aplicar |
|---|---|
| Ligado | `checked` (ou `aria-checked="true"` em elemento não-input) |
| Foco | automático — anel 2px `--ring` |
| Desabilitado | `disabled` — opacidade 0,5 no switch e no rótulo irmão |
| Inválido | `aria-invalid="true"` (borda `ttsc-danger`) |
| Salvando | `aria-busy="true"` + `disabled` enquanto o PATCH não volta (ver JS) |

## API

Sem JavaScript obrigatório (checkbox nativo). **Atenção:** checkbox desmarcado não é enviado no POST — inclua `<input type="hidden" name="x" value="0">` **antes** do switch com o mesmo `name` e `value="1"` no switch.

## Acessibilidade

- `role="switch"`: o leitor anuncia "ligado/desligado" em vez de "marcado".
- O rótulo diz **o que** é ligado ("Notificações financeiras"), nunca "Ativar/Desativar".
- `Espaço` alterna (nativo). Não troque o rótulo conforme o estado.
- O trilho desligado (`ttsc-border-strong`) e ligado (`ttsc-accent`) são indicadores não textuais (≥ 3:1 contra a superfície); o estado também é exposto por ARIA.

## Modelos

### HTML

```html
<!-- Preferências do usuário — settings/notifications.php -->
<form method="post" action="/settings/notifications" class="flex flex-col gap-4">
  <input type="hidden" name="_token" value="<?= csrf_token() ?>">
  <?php foreach (['academic' => 'Notificações acadêmicas', 'financial' => 'Notificações financeiras',
                  'documents' => 'Documentos', 'marketing' => 'Novidades e campanhas'] as $key => $label): ?>
    <label class="ttsc-form-control-inline">
      <input type="hidden" name="notify_<?= $key ?>" value="0">
      <input type="checkbox" role="switch" class="ttsc-switch" name="notify_<?= $key ?>" value="1"
             data-ttsc-autosave="/api/v1/me/preferences"
             <?= !empty($prefs['notify_' . $key]) ? 'checked' : '' ?>>
      <span class="ttsc-label"><?= $this->e($label) ?></span>
    </label>
  <?php endforeach; ?>
  <label class="ttsc-form-control-inline">
    <input type="checkbox" role="switch" class="ttsc-switch" checked disabled>
    <span class="ttsc-label">Alertas de segurança (obrigatório)</span>
  </label>
</form>

<!-- Coluna "Ativo" na tabela de cursos -->
<td>
  <input type="checkbox" role="switch" class="ttsc-switch ttsc-switch-sm"
         aria-label="Curso <?= $this->e($course['name']) ?> ativo"
         data-ttsc-autosave="/api/v1/academic/courses/<?= $this->e($course['uuid']) ?>/active"
         <?= $course['is_active'] ? 'checked' : '' ?>>
</td>
```

### CSS

```css
/* Ponte (bundle.css) */
:root { --input: var(--ttsc-border-strong); --primary: var(--ttsc-accent); }

/* Extensão: estado "salvando" — pulso no trilho */
.ttsc-switch[aria-busy="true"] { animation: ttsc-switch-pulse 1s ease-in-out infinite; }
@keyframes ttsc-switch-pulse { 50% { opacity: .55; } }

/* Extensão: linha de preferência com descrição alinhada ao texto */
.ttsc-switch-row { display: grid; grid-template-columns: auto 1fr; column-gap: var(--ttsc-space-3); align-items: start; }
.ttsc-switch-row .ttsc-form-description { grid-column: 2; margin-top: 2px; color: var(--ttsc-text-muted); }
```

### JS

```js
// assets/js/core/ttsc.switch-autosave.js — salva o switch na hora, com rollback em erro
const csrf = document.querySelector('meta[name="csrf-token"]')?.content;

document.addEventListener('change', async (event) => {
  const sw = event.target.closest('input.ttsc-switch[data-ttsc-autosave]');
  if (!sw) return;
  const value = sw.checked;
  sw.disabled = true;
  sw.setAttribute('aria-busy', 'true');
  try {
    const res = await fetch(sw.dataset.ttscAutosave, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': csrf, Accept: 'application/json' },
      body: JSON.stringify({ field: sw.name || 'is_active', value: value ? 1 : 0 }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    window.TTSC?.Toast?.show?.({ message: 'Preferência salva.', variant: 'success' });
  } catch (err) {
    sw.checked = !value; // rollback visual
    window.TTSC?.Toast?.show?.({ message: 'Não foi possível salvar. Tente novamente.', variant: 'destructive' });
  } finally {
    sw.disabled = false;
    sw.removeAttribute('aria-busy');
  }
});
```

### SQL

```sql
-- Estado inicial das preferências (tenant). user_uuid é UNIQUE em user_preferences.
SELECT p.notify_academic, p.notify_financial, p.notify_documents,
       p.notify_security, p.notify_marketing
  FROM user_preferences p
 WHERE p.user_uuid = :user_uuid;

-- Autosave de um switch: upsert (o controller valida :field contra uma whitelist
-- notify_academic|notify_financial|notify_documents|notify_marketing — nunca interpola o nome cru)
INSERT INTO user_preferences (uuid, user_uuid, notify_financial)
VALUES (UUID(), :user_uuid, :value)
ON DUPLICATE KEY UPDATE notify_financial = VALUES(notify_financial), updated_at = NOW();

-- Coluna "Ativo" da tabela de cursos
UPDATE courses
   SET is_active = :is_active, updated_at = NOW()
 WHERE uuid = :course_uuid
   AND deleted_at IS NULL;
```

Sem linha em `user_preferences`, o PHP usa os defaults da tabela (`notify_* = 1`, `notify_marketing = 0`) para marcar `checked`. O nome da coluna do upsert vem de um `match ($field)` no controller; o valor é sempre `:value` (0/1).

## Faça / Não faça

- **Faça:** `role="switch"` + hidden `value="0"` antes; rollback visual se o servidor falhar.
- **Faça:** `ttsc-switch-sm` em tabelas, sempre com `aria-label` contendo o nome do registro.
- **Não faça:** switch que só tem efeito após "Salvar" misturado com switches de efeito imediato na mesma tela; rótulo que muda com o estado.
