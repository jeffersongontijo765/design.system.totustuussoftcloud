# Pulse

Ponto com anel pulsante (`.ttsc-pulse`) que sinaliza algo **ao vivo** ou em andamento — aula acontecendo agora, serviço monitorado, chamada ativa — padronizando o `.live-indicator-dot` do app.

## Quando usar

- Status em tempo real: “Ao vivo”, aula/evento em andamento, check-in de frequência aberto.
- Saúde de serviços (página de status do desenvolvedor, integrações bancárias, SMS).
- Chamar atenção para um ícone com algo novo/ativo (`ttsc-pulse-ring`: videochamada em curso, alerta crítico).
- **Não use** para status estático (“Ativa”, “Cancelada”) — use [Bullets](../Bullets/README.md) ou [Badge](../Badge/README.md).
- **Não use** mais de 2–3 pulsos visíveis na mesma tela: movimento demais compete com o conteúdo.
- Carregamento é [Indicator](../Indicator/README.md), não pulse.

## Anatomia

```
 ( ● )   .ttsc-pulse         ponto sólido + ::after expandindo e sumindo
((ícone)) .ttsc-pulse-ring   anel ::before ao redor de um símbolo/avatar
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Ponto | `span.ttsc-pulse` + `aria-hidden="true"` | sim |
| Cor | `ttsc-pulse-success` · `-warning` · `-danger` · `-info` (padrão accent) | não |
| Tamanho | `ttsc-pulse-sm` 6px · (8px) · `ttsc-pulse-lg` 12px | não |
| Desligado | `data-live="off"` (ponto cinza `ttsc-meta`, sem animação) ou `ttsc-pulse-paused` | não |
| Anel | `span.ttsc-pulse-ring` envolvendo ícone/[Symbol](../Symbol/README.md) | não |
| Texto | rótulo ao lado (“Ao vivo”, “operacional”) | sim |

## Variantes

| Variante | Classe | Uso | Token |
|---|---|---|---|
| Accent | `ttsc-pulse` | ao vivo, em andamento | `ttsc-accent` |
| Success | `ttsc-pulse-success` | serviço operacional | `ttsc-success` |
| Warning | `ttsc-pulse-warning` | degradado, lento | `ttsc-warning` |
| Danger | `ttsc-pulse-danger` | fora do ar, alerta crítico | `ttsc-danger` |
| Info | `ttsc-pulse-info` | sincronizando | `ttsc-info` |
| Off | `data-live="off"` | sem sinal / encerrado | `ttsc-meta` |

### Legado

`assets/css/ttsc.css` define `.live-indicator-dot` (8px, `var(--accent, #3ecf8e)`, `@keyframes pulse-live` com `box-shadow`). **Atenção:** no runtime ttscui `--accent` é o hover neutro (`ttsc-canvas-2`), então o ponto legado pode sair cinza. Migre para `.ttsc-pulse`, que usa `--ttsc-accent` direto.

## API

Somente CSS (implementação TTSC). Personalização por variáveis:

| Variável | Padrão | Efeito |
|---|---|---|
| `--ttsc-pulse-color` | `var(--ttsc-accent)` | cor do ponto e do anel |
| `--ttsc-pulse-size` | `8px` | diâmetro do ponto |

| Atributo | Efeito |
|---|---|
| `data-live="on"`/`"off"` | liga/desliga o pulso (útil para atualização via JS/SSE) |

## Acessibilidade

- O ponto é `aria-hidden`; o estado vem do texto ao lado (“Ao vivo · 2 aulas agora”, “fora do ar”).
- Atualizações em tempo real ficam num contêiner `role="status" aria-live="polite"` (sem anunciar cada pulso).
- `prefers-reduced-motion: reduce` remove a animação — o ponto continua visível.
- Cor não textual: os tokens de status têm ≥ 3:1 sobre `ttsc-surface` nos dois temas; `warning` sempre acompanhado de texto.

## Modelos

### HTML

```html
<!-- Chip "ao vivo" no cabeçalho da agenda -->
<?php if ($liveCount > 0): ?>
  <span class="ttsc-badge ttsc-badge-outline" role="status">
    <span class="ttsc-pulse ttsc-pulse-sm" aria-hidden="true"></span>
    Ao vivo · <?= (int) $liveCount ?> <?= $liveCount === 1 ? 'aula agora' : 'aulas agora' ?>
  </span>
<?php endif ?>

<!-- Lista de eventos em andamento -->
<?php foreach ($liveEvents as $ev): ?>
  <div class="flex items-center gap-2">
    <span class="ttsc-pulse" aria-hidden="true"></span>
    <span><?= $this->e($ev['title']) ?> <span class="text-xs text-muted-foreground"><?= $this->e(substr($ev['start_time'], 0, 5)) ?>–<?= $this->e(substr($ev['end_time'], 0, 5)) ?> · <?= $this->e($ev['location']) ?></span></span>
  </div>
<?php endforeach ?>

<!-- Serviço monitorado, atualizado por JS -->
<div class="flex items-center gap-2" role="status" aria-live="polite">
  <span class="ttsc-pulse ttsc-pulse-success" data-service="bank" aria-hidden="true"></span>
  Integração bancária <span class="text-xs text-muted-foreground" data-service-label="bank">operacional</span>
</div>
```

### CSS

```css
.ttsc-pulse { --ttsc-pulse-color: var(--ttsc-accent); --ttsc-pulse-size: 8px; position: relative; display: inline-block; flex-shrink: 0;
  width: var(--ttsc-pulse-size); height: var(--ttsc-pulse-size); border-radius: var(--ttsc-radius-pill); background: var(--ttsc-pulse-color); }
.ttsc-pulse::after { content: ""; position: absolute; inset: 0; border-radius: inherit; background: var(--ttsc-pulse-color);
  animation: ttsc-pulse-ring 2s cubic-bezier(.2, .6, .4, 1) infinite; }
.ttsc-pulse-sm { --ttsc-pulse-size: 6px; }
.ttsc-pulse-lg { --ttsc-pulse-size: 12px; }
.ttsc-pulse-success { --ttsc-pulse-color: var(--ttsc-success); }
.ttsc-pulse-warning { --ttsc-pulse-color: var(--ttsc-warning); }
.ttsc-pulse-danger  { --ttsc-pulse-color: var(--ttsc-danger); }
.ttsc-pulse-info    { --ttsc-pulse-color: var(--ttsc-info); }
.ttsc-pulse-paused::after, .ttsc-pulse[data-live="off"]::after { animation: none; opacity: 0; }
.ttsc-pulse[data-live="off"] { --ttsc-pulse-color: var(--ttsc-meta); }
.ttsc-pulse-ring { position: relative; display: inline-flex; border-radius: var(--ttsc-radius-pill); }
.ttsc-pulse-ring::before { content: ""; position: absolute; inset: -4px; border-radius: inherit; pointer-events: none;
  border: 2px solid var(--ttsc-pulse-color, var(--ttsc-accent)); animation: ttsc-pulse-halo 2s ease-out infinite; }
@keyframes ttsc-pulse-ring { 0% { transform: scale(1); opacity: .6; } 70%, 100% { transform: scale(2.6); opacity: 0; } }
@keyframes ttsc-pulse-halo { 0% { transform: scale(.9); opacity: .9; } 80%, 100% { transform: scale(1.35); opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .ttsc-pulse::after, .ttsc-pulse-ring::before { animation: none; opacity: 0; } }

/* Compatibilidade: o legado passa a usar o token correto */
.live-indicator-dot { background-color: var(--ttsc-accent); }
```

### JS

```js
// assets/js/core/ttsc.pulse.js — atualiza pulsos de serviço a cada 60 s
const VARIANTS = { healthy: 'success', attention: 'warning', down: 'danger' };
const LABELS = { healthy: 'operacional', attention: 'lenta', down: 'fora do ar', unknown: 'sem sinal' };

async function refreshServices() {
  const res = await fetch('/api/v1/status/services', { headers: { Accept: 'application/json' } });
  if (!res.ok) return;
  const services = await res.json(); // [{ key: 'bank', state: 'healthy' }, …]
  services.forEach(({ key, state }) => {
    const dot = document.querySelector(`.ttsc-pulse[data-service="${key}"]`);
    if (!dot) return;
    dot.classList.remove('ttsc-pulse-success', 'ttsc-pulse-warning', 'ttsc-pulse-danger');
    if (VARIANTS[state]) { dot.classList.add(`ttsc-pulse-${VARIANTS[state]}`); dot.dataset.live = 'on'; }
    else dot.dataset.live = 'off';
    const label = document.querySelector(`[data-service-label="${key}"]`);
    if (label) label.textContent = LABELS[state] || LABELS.unknown;
  });
}
refreshServices();
setInterval(refreshServices, 60000);
```

### SQL

```sql
-- Eventos acontecendo agora na unidade (pulso "ao vivo")
SELECT e.uuid, e.title, e.start_time, e.end_time, e.location
  FROM events e
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
   AND e.status <> 'cancelled'
   AND CURDATE() BETWEEN e.start_date AND COALESCE(e.end_date, e.start_date)
   AND CURTIME() BETWEEN e.start_time AND e.end_time
 ORDER BY e.start_time;
```

`$liveCount = count($liveEvents)`; quando é zero, a view não renderiza o chip. Use o fuso da unidade (`units.timezone`) na conexão (`SET time_zone`) para `CURDATE()/CURTIME()` corretos.

## Faça / Não faça

- **Faça:** pulso + texto curto do estado; poucos por tela.
- **Faça:** `data-live="off"` quando o evento termina, em vez de remover o ponto (evita salto).
- **Não faça:** pulsar status permanentes (“Matrícula ativa”).
- **Não faça:** usar `var(--accent)` para a cor — no runtime é cinza de hover.
