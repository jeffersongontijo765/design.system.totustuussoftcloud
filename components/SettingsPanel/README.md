# SettingsPanel

Corpo das páginas de configuração: abas segmentadas = grupos de parâmetros, cada grupo com seções em cartão (tile, título, origem dos dados) e campos em grade de 2 colunas — texto, número, select, toggle e textarea — com Descartar / Salvar alterações na barra de abas.

## Quando usar

- Parâmetros de um módulo que valem para toda a instituição ou unidade: ano letivo, abertura de rematrícula, vencimento, multa, frequência mínima.
- Valores únicos (chave → valor), não listas de registros. Se o usuário cria/edita várias linhas (calendários, períodos, regras), é uma página Records com [RecordsTable](../RecordsTable/README.md) — como `/academic/settings/calendar`.
- Página completa no arquétipo: [PageSettings](../PageSettings/README.md).
- Preferência pessoal do usuário (tema, idioma) não é configuração de módulo: vai no drawer de perfil.

## Anatomia

```
[[filtros] Matrícula] [[cal] Frequência]                              [↺ Descartar] [[salvar] Salvar alterações]
┌ section ──────────────────────────────────────────────────────────────────────┐
│ [[cal]] Período de matrícula                                                      │
│      academic_periods                                                          │
│ Ano letivo            [2026 ▾]          Abertura da rematrícula [2026-11-03]   │
│ ┌ toggle ───────────────────────────────┐                                      │
│ │ [x] Exigir documentação completa        │                                      │
│ │   Matrícula só passa para análise …   │                                      │
│ └───────────────────────────────────────┘                                      │
└────────────────────────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Abas de grupo | `#chassis-segmented-tabs` com `button#tab-btn-<grupo>[data-model-tab]` ([SegmentedTabs](../SegmentedTabs/README.md)) | sim |
| Ações | `button[data-model-api=reset]` "Descartar" (outline) + `button[data-model-api=save]` "Salvar alterações" (primário) | sim |
| Painel do grupo | `div#view-<grupo>.space-y-4[role=tabpanel]` (demais com `display:none`) | sim |
| Seção | `section.bg-white.border.rounded-2xl.p-5.shadow-xs` + cabeçalho com tile 40px, `h3`, `p` | sim |
| Grade de campos | `div.grid.grid-cols-1.md:grid-cols-2.gap-4.text-xs` | sim |
| Campo | `label.font-bold.text-slate-700` + `input/select/textarea.rounded-xl.border-slate-200.p-2.5` (`font-mono` com `mono`) | sim |
| Toggle | `label.flex.p-3.rounded-xl.border.bg-slate-50/60` com `checkbox` + título + `hint` | não |
| Dica | `p.text-[10px].text-slate-400` | não |
| Campo largo | wrapper `md:col-span-2` (`wide` ou `textarea`) | não |

## Variantes

| `fields[].type` | Controle | Notas |
|---|---|---|
| `text` (padrão) | `input type=text` | `mono:true` para datas/códigos |
| `number` | `input type=number` | percentuais e dias |
| `select` | `select` com `options[]`, `value` selecionado | enriquecido pelo `ttsc.select.js` (`.ttsc-select-trigger`) |
| `toggle` | checkbox em cartão com `hint` | liga/desliga regra |
| `textarea` | `textarea rows=3` | ocupa 2 colunas |

## API

**Ficha** (`layout: "settings"`)

| Campo | Uso |
|---|---|
| `groups[] = {id, label, icon, sections[]}` | abas; o primeiro grupo abre visível |
| `sections[] = {title, desc, icon, fields[]}` | cartões; `desc` documenta a origem (`academic_periods`, `module_settings academic.*`) |
| `fields[] = {label, type, value, options, hint, mono, wide}` | campos |
| `title`, `icon`, `banner` | cabeçalho e banner da página |

**JS**

| API | Efeito |
|---|---|
| `TTSCModelKit.blocks.settings(page)` | HTML dos painéis de grupo |
| `TTSCModelKit.render(t, page)` com `layout:"settings"` | cabeçalho + banner + abas (grupos) + Descartar/Salvar + painéis |
| `TTSCModelKit.switchTab('<grupo>')` | troca o grupo |
| `[data-model-api="save"\|"reset"]` | no kit mostra o endpoint; na página real, salvar/descartar |

**PHP**: não há partial de settings no chassi; `/academic/settings` e `/academic/settings/calendar` são páginas `domain_page.php` sobre fontes somente leitura (`writable => false`): `/academic/settings` lê a view `inst_settings_academic` (= `module_settings` com `module = 'academic'`, colunas `label`, `setting_key`, `value_type`, `display_value`, `default_value`, `status` `default|customized|locked`). Uma página de configuração real monta `chassis/chassis.php` com `$chassis['tabs']` = grupos, `$panes[<grupo>]` = seções e as ações próprias.

**Endpoints reais de configuração**

| Rota | Uso |
|---|---|
| `GET /api/v1/academic/settings/calendar/data-table` | lista de calendários (tabela) |
| `PATCH /api/v1/academic/settings/calendar/data-table/{calendar}` | editar um calendário |
| `POST /api/v1/academic/settings/calendar/data-table/export` | exportar |
| `GET\|PUT /api/v1/supplies/settings`, `GET\|POST /api/v1/meetings/settings` | padrão de leitura/gravação chave-valor de outros módulos — use o mesmo formato para `academic.*` |

## Acessibilidade

- Associe cada `label` ao controle com `for`/`id` (o kit não faz isso; o select enriquecido herda o rótulo pelo menu).
- Toggle: o `label` inteiro é clicável; o texto da dica fica dentro do rótulo e é lido junto.
- "Salvar alterações" deve ficar desabilitado sem mudanças e anunciar o resultado (toast `role=status`).
- `text-slate-700` em rótulos e `text-slate-400` só para dicas curtas (≥ 4,5:1 sobre branco só a partir de `slate-500` — prefira `--ttsc-text-muted`).

## Modelos

### HTML

1) PHP — página de configuração montada com o chassi (grupos como abas):

```php
<?php
$chassis = [
    'prefix' => 'academic-settings', 'active' => 'enrollment', 'tone' => 'emerald',
    'tabs' => [
        ['id' => 'enrollment', 'label' => 'Matrícula',  'icon' => 'fa-id-card'],
        ['id' => 'attendance', 'label' => 'Frequência', 'icon' => 'fa-calendar-check'],
    ],
    'banner' => ['icon' => 'fa-gear', 'title' => 'Regras do ano letivo',
                 'desc' => 'Parâmetros aplicados a matrículas, frequência e avaliação de todas as unidades.'],
];
$panes = [
    'enrollment' => $this->fetch('app::partials/academic/settings_enrollment', ['period' => $currentPeriod, 'settings' => $settings]),
    'attendance' => $this->fetch('app::partials/academic/settings_attendance', ['settings' => $settings]),
];
require base_path('resources/views/app/partials/chassis/chassis.php');
```

2) HTML gerado (preview; uma seção do grupo Matrícula):

```html
<div id="view-enrollment" class="space-y-4" role="tabpanel" aria-labelledby="tab-btn-enrollment">
  <section class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs space-y-4">
    <div class="flex items-start gap-3 border-b border-slate-100 pb-3">
      <span class="grid h-10 w-10 shrink-0 place-items-center rounded-xl border border-emerald-200 bg-emerald-50 text-emerald-600"><i class="fa-light fa-calendar text-base"></i></span>
      <div>
        <h3 class="text-sm font-bold text-slate-900">Período de matrícula</h3>
        <p class="mt-0.5 text-xs text-slate-500">academic_periods</p>
      </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
      <div>
        <label class="font-bold text-slate-700 block mb-1">Ano letivo</label>
        <select class="w-full rounded-xl border border-slate-200 bg-white p-2.5 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500/40 font-medium">
          <option selected>2026</option><option>2027</option>
        </select>
      </div>
      <div>
        <label class="font-bold text-slate-700 block mb-1">Abertura da rematrícula</label>
        <input type="text" value="2026-11-03" class="w-full rounded-xl border border-slate-200 bg-white p-2.5 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500/40 font-mono">
      </div>
      <div>
        <label class="flex items-start gap-3 p-3 rounded-xl border border-slate-200 bg-slate-50/60 cursor-pointer">
          <input type="checkbox" checked class="rounded text-emerald-600 mt-0.5">
          <span><span class="block font-bold text-slate-700">Exigir documentação completa</span>
            <span class="block text-[10px] text-slate-400 mt-0.5">Matrícula só passa para análise com todos os documentos</span></span>
        </label>
      </div>
    </div>
  </section>
</div>
```

O `select` aparece enriquecido em runtime (`.ttsc-select-wrapper` + `.ttsc-select-trigger` + `.ttsc-select-dropdown[role=listbox]`), com o nativo escondido e ainda emitindo `change`.

### CSS

Utilitários do runtime; o escuro vem de `assets/css/ttsc.commercial.model.css` (`html.dark .bg-white`, `.bg-slate-50\/60`, `.border-slate-200`) e o select enriquecido é estilizado pelo próprio `ttsc.select.js` + `ttsc.design-system.css`.

```css
/* Extensão por tokens: campo alterado e não salvo */
#model-page [role="tabpanel"] [data-dirty="true"] {
  border-color: var(--ttsc-warning);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--ttsc-warning) 18%, transparent);
}
#model-page [role="tabpanel"] input:focus-visible,
#model-page [role="tabpanel"] select:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 1px; }
```

### JS

```js
// Carrega, marca alterações, descarta e salva as configurações academic.*
const API = '/api/v1/academic/settings';          // novo endpoint no formato de /api/v1/supplies/settings
const csrf = () => document.querySelector('meta[name="csrf-token"]')?.content || '';
const form = document.getElementById('model-page');
let saved = {};

function read() {
  const out = {};
  form.querySelectorAll('[name]').forEach((el) => { out[el.name] = el.type === 'checkbox' ? (el.checked ? '1' : '0') : el.value; });
  return out;
}
function write(values) {
  form.querySelectorAll('[name]').forEach((el) => {
    if (!(el.name in values)) return;
    if (el.type === 'checkbox') el.checked = values[el.name] === '1'; else el.value = values[el.name];
    el.dataset.dirty = 'false';
  });
}
form.addEventListener('input', (ev) => { if (ev.target.name) ev.target.dataset.dirty = String(read()[ev.target.name] !== saved[ev.target.name]); });

fetch(API, { credentials: 'same-origin' }).then((r) => r.json()).then((b) => { saved = b.settings || {}; write(saved); });

document.querySelector('[data-model-api="reset"]').addEventListener('click', () => write(saved));
document.querySelector('[data-model-api="save"]').addEventListener('click', async () => {
  const res = await fetch(API, {
    method: 'PUT', credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': csrf() },
    body: JSON.stringify({ settings: read() }),
  });
  if (!res.ok) return window.showToast?.('Não foi possível salvar as configurações.', 'error');
  saved = read(); write(saved);
  window.showToast?.('Configurações salvas.', 'success');
});
```

### SQL

```sql
-- Leitura: parâmetros do módulo acadêmico — a mesma tabela da view inst_settings_academic,
-- fonte real de /academic/settings (segredos mascarados como na view)
SELECT setting_key, label, value_type,
       CASE WHEN is_sensitive = 1 THEN '********' ELSE display_value END AS display_value,
       default_value, status
  FROM module_settings
 WHERE module = 'academic'
   AND deleted_at IS NULL
   AND (tenant_id = :tenant_id OR tenant_id IS NULL)
 ORDER BY setting_key;

-- Gravação (Salvar alterações): uma linha por chave alterada; 'customized' marca o desvio do padrão
UPDATE module_settings
   SET display_value = :value,
       status = CASE WHEN :value = default_value THEN 'default' ELSE 'customized' END,
       updated_by = :actor_uuid, updated_at = NOW()
 WHERE module = 'academic' AND setting_key = :setting_key
   AND tenant_id = :tenant_id AND status <> 'locked' AND deleted_at IS NULL;

-- Chave ainda sem linha do tenant: cria a partir do padrão global (module_settings não tem índice único por chave)
INSERT INTO module_settings (uuid, tenant_id, module, setting_key, label, value_type, display_value, default_value, status, updated_by)
SELECT UUID(), :tenant_id, g.module, g.setting_key, g.label, g.value_type, :value, g.default_value, 'customized', :actor_uuid
  FROM module_settings g
 WHERE g.module = 'academic' AND g.setting_key = :setting_key AND g.tenant_id IS NULL AND g.deleted_at IS NULL
   AND NOT EXISTS (SELECT 1 FROM module_settings t
                    WHERE t.module = 'academic' AND t.setting_key = :setting_key AND t.tenant_id = :tenant_id AND t.deleted_at IS NULL);

-- Grupo "Matrícula": período corrente (select Ano letivo) e opções
SELECT uuid, name, year, start_date, end_date, is_current
  FROM academic_periods
 WHERE deleted_at IS NULL AND year IN (:year, :year + 1)
 ORDER BY year, start_date;

-- Seção "Financeiro": vencimento e regras ativas por curso
SELECT c.name AS curso, abr.due_day, abr.monthly_tuition, abr.enrollment_fee, abr.payment_method
  FROM academic_billing_rules abr
  JOIN courses c ON c.uuid = abr.course_uuid
 WHERE abr.status = 'active';
```

O controlador devolve `{settings: {chave: valor}}` e grava `UPDATE` + `INSERT` na mesma transação, registrando a mudança em `audit_logs` (`table_name = 'module_settings'`). Linhas `locked` não mudam. A tabela genérica `settings` (chave única `setting_key` + `company_id`) guarda configurações de plataforma, como as do `VaultConfigService`; parâmetros de módulo ficam em `module_settings`.

## Faça / Não faça

- **Faça:** escrever em `desc` de cada seção a origem do dado (tabela ou prefixo de chave) — é o contrato do backend.
- **Faça:** confirmar "Descartar" quando houver alterações.
- **Não faça:** misturar listas editáveis (vários registros) com parâmetros únicos na mesma seção.
- **Não faça:** salvar campo a campo no `change`; um "Salvar alterações" por página.
