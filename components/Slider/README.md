# Slider

Controle deslizante de valor único sobre `<input type="range">` nativo, com preenchimento e saída de valor sincronizados pelo `[data-ttsc-range-slider]` do ttscui.

## Quando usar

- Escolher um número dentro de uma faixa conhecida quando a **posição relativa** importa mais que o valor exato: frequência mínima para aprovação (0–100%), tolerância de atraso (0–30 min), peso de uma avaliação.
- Filtros de relatório ("alunos com frequência abaixo de X%").
- Valor exato digitado (nota 7,25, mensalidade) → [Input](../Input/README.md) / [InputGroup](../InputGroup/README.md).
- **Faixa com duas alças** (de–até), passos não lineares, tooltips nas alças → [NoUiSlider](../NoUiSlider/README.md).

## Anatomia

```
Frequência mínima                         75%   ← output (data-ttsc-range-slider-output)
●━━━━━━━━━━━━━━━━━━━━━━━━━○───────────────────    input[type=range].range
0%                                        100%   ← marcas (opcional)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container | `div[data-ttsc-range-slider="true"]` (ou o próprio `input`) | sim |
| Trilho + alça | `input[type=range].range` (estilo do runtime: trilho 8px `--input`, alça 24px `--primary`) | sim |
| Saída | `data-ttsc-range-slider-output="#sel"` → `textContent` recebe `input.value` | não |
| Preenchimento | CSS var `--ttsc-range-fill` (0–1) escrita pelo JS no container — use no CSS (extensão abaixo) | não |
| Marcas | `<datalist>` + `list="…"` ou rótulos min/máx em texto | não |

## Variantes

| Variante | Como | Tokens |
|---|---|---|
| Padrão | `.range` | trilho `--input` → `ttsc-border-strong`; alça `--primary` → `ttsc-accent`, borda `--border` |
| Com preenchimento | `.range` + extensão `.ttsc-range-fill` | parte preenchida `ttsc-accent` |
| Com saída | `output` com `aria-live` | texto `ttsc-text`, peso 600 |
| Desabilitado | `disabled` | alça `--accent` (neutra), `pointer-events: none` |

## API

Conferido em `src/components/range-slider/range-slider.ts` (global `ttscRangeSlider` / `TTSC.RangeSlider`).

| Opção (`data-ttsc-range-slider-*`) | Padrão | Descrição |
|---|---|---|
| `output` | `""` | seletor procurado **dentro** do container e, se não achar, no documento |
| `lazy` | `false` | `true` = não inicializa em `TTSC.init()` |

| Método | Descrição |
|---|---|
| `ttscRangeSlider.getInstance(el)` / `getOrCreateInstance(el, config?)` | instância (precisa achar um `input[type=range]`) |
| `instance.getValue()` | número atual (`valueAsNumber`) |
| `instance.getRangeInput()` | o `<input type="range">` |
| `instance.on('input' \| 'change', fn)` | callback com payload |
| `instance.dispose()` | remove listeners e `--ttsc-range-fill` |

| Evento DOM (no container, bubbles) | `event.detail.payload` |
|---|---|
| `ttsc.range-slider.input` | `{ value, min, max, step }` — a cada movimento |
| `ttsc.range-slider.change` | idem — ao soltar a alça |

Para mudar o valor por código: `input.value = 80; input.dispatchEvent(new Event('input', { bubbles: true }))` (o módulo escuta `input`/`change` nativos).

## Acessibilidade

- `<label for>` no `input`; o leitor anuncia o valor nativo. Para unidade, use `aria-valuetext="75%"` (atualizado no JS).
- Teclado nativo: setas ±`step`, `PageUp/PageDown` ±10%, `Home/End` mín./máx.
- O `output` com `aria-live="polite"` é redundante para leitor de tela se `aria-valuetext` existir — mantenha só um anúncio (`aria-hidden` no output visual).
- Alça `ttsc-accent` sobre trilho `ttsc-border-strong`: indicadores não textuais ≥ 3:1.

## Modelos

### HTML

```html
<!-- Configurações › Acadêmico › Critérios de aprovação -->
<div class="ttsc-form-item" data-ttsc-range-slider="true" data-ttsc-range-slider-output="#min-att-out">
  <div class="flex items-center justify-between">
    <label class="ttsc-form-label" for="min-att">Frequência mínima para aprovação</label>
    <span class="text-sm font-semibold" id="min-att-out" aria-hidden="true"><?= (int) $minAttendance ?></span>
  </div>
  <input type="range" class="range ttsc-range-fill" id="min-att" name="min_attendance_pct"
         min="50" max="100" step="5" value="<?= (int) $minAttendance ?>" aria-valuetext="<?= (int) $minAttendance ?>%">
  <div class="flex justify-between text-xs text-muted-foreground" aria-hidden="true"><span>50%</span><span>100%</span></div>
  <p class="ttsc-form-description">LDB: mínimo legal de 75% da carga horária.</p>
</div>
```

### CSS

```css
/* Ponte (bundle.css): .range usa --input (trilho) e --primary (alça) */
:root { --input: var(--ttsc-border-strong); --primary: var(--ttsc-accent); --border: var(--ttsc-border); }

/* Extensão do chassi: preenchimento até a alça, lendo --ttsc-range-fill (0–1) escrito pelo ttscui no container */
.ttsc-range-fill::-webkit-slider-runnable-track {
  background: linear-gradient(to right,
    var(--ttsc-accent) 0 calc(var(--ttsc-range-fill, 0) * 100%),
    var(--ttsc-border-strong) calc(var(--ttsc-range-fill, 0) * 100%) 100%);
}
.ttsc-range-fill::-moz-range-progress { background: var(--ttsc-accent); height: .5rem; border-radius: .188rem; }
.range:focus-visible::-webkit-slider-thumb { box-shadow: 0 0 0 3px var(--ttsc-accent-soft); }
```

### JS

```js
// Atualiza aria-valuetext e recarrega o relatório ao soltar
TTSC.init();
const container = document.querySelector('[data-ttsc-range-slider]');
const slider = ttscRangeSlider.getOrCreateInstance(container);

container.addEventListener('ttsc.range-slider.input', (event) => {
  const { value } = event.detail.payload;
  slider.getRangeInput().setAttribute('aria-valuetext', `${value}%`);
  document.getElementById('min-att-out').textContent = `${value}%`;
});

container.addEventListener('ttsc.range-slider.change', async (event) => {
  const { value } = event.detail.payload;
  const res = await fetch(`/api/v1/academic/reports/low-attendance?class_uuid=${classUuid}&min_pct=${value}`,
    { headers: { Accept: 'application/json' } });
  if (res.ok) renderAtRiskTable((await res.json()).data);
});
```

### SQL

```sql
-- Valor salvo (settings do tenant; chave única por empresa)
SELECT s.value
  FROM settings s
 WHERE s.setting_key = 'academic.min_attendance_pct'
   AND s.company_id = :company_id;

-- Salvar o slider (upsert pela UNIQUE (setting_key, company_id))
INSERT INTO settings (id, code, uuid, setting_key, value, type, category, company_id)
VALUES (UUID(), :code, UUID(), 'academic.min_attendance_pct', :value, 'integer', 'academic', :company_id)
ON DUPLICATE KEY UPDATE value = VALUES(value);

-- Filtro do relatório: matrículas da turma com frequência abaixo do valor do slider
SELECT a.enrollment_uuid,
       COUNT(*) AS lessons,
       ROUND(100 * SUM(a.status = 'present') / COUNT(*), 1) AS attendance_pct
  FROM attendance a
 WHERE a.class_uuid = :class_uuid
 GROUP BY a.enrollment_uuid
HAVING attendance_pct < :min_pct
 ORDER BY attendance_pct;
```

O controller lê `settings.value` (padrão 75 quando não há linha), escreve no `value` do `<input type="range">` e valida `50 ≤ value ≤ 100` e múltiplo de 5 antes do upsert. O endpoint do relatório devolve `{"data":[…]}` da terceira consulta.

## Faça / Não faça

- **Faça:** mostrar o valor (output) e min/máx; `step` coerente com a regra (5 em 5%).
- **Faça:** buscar dados no `change` (ao soltar), não no `input` (a cada pixel).
- **Não faça:** slider para valor exato digitável; duas alças com dois ranges sobrepostos (use NoUiSlider).
