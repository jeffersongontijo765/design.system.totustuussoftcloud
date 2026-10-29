# Timeline

Linha do tempo vertical de eventos de um registro — ícone por ação, autor, mudança de status (antigo → novo) e observação — em CSS com tokens (implementação TTSC), aplicada ao histórico da solicitação de matrícula (`enrollment_request_history`).

## Quando usar

- Histórico/auditoria de **um** registro: solicitação de matrícula, ocorrência disciplinar, chamado de suporte, contrato, título financeiro.
- Quando a ordem cronológica e “quem fez o quê” importam mais que comparar colunas.
- **Não use** para listas de muitos registros diferentes (log do sistema com filtros): use [DataTable](../DataTable/README.md) / o arquétipo [PageHistory](../PageHistory/README.md).
- **Não use** para etapas futuras de um processo (wizard): isso é [Stepper](../Stepper/README.md).
- **Não use** para agenda por datas: [FullCalendar](../FullCalendar/README.md).

## Anatomia

```
ol.ttsc-timeline
└── li.ttsc-timeline-item.tl-<tom>
    ├── .ttsc-timeline-icon (32px, círculo)  <i class="fa-light fa-…">
    │   ╎  linha vertical 2px (::before) até o próximo item
    └── .ttsc-timeline-body
        ├── .ttsc-timeline-head  .ttsc-timeline-title "Aprovada"      time.ttsc-timeline-time "18/10/2026 às 09:00"
        ├── .ttsc-timeline-meta  (fa-user) Juliana Prado · [Em análise] → [Aprovada]
        └── .ttsc-timeline-note  observação (details)                 (opcional)
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Lista | `ol.ttsc-timeline` (ordem importa) | sim |
| Item | `li.ttsc-timeline-item` + tom `tl-success \| tl-danger \| tl-info \| tl-warning` | sim |
| Ícone | `.ttsc-timeline-icon` com `fa-light` (`aria-hidden`) | sim |
| Título | `.ttsc-timeline-title` (ação em pt-BR) | sim |
| Data/hora | `time.ttsc-timeline-time[datetime]` | sim |
| Autor + mudança | `.ttsc-timeline-meta` com badges de status | recomendado |
| Observação | `.ttsc-timeline-note` | não |

## Variantes

| `action` | Título | Ícone | Tom | Tokens (fundo / ícone) |
|---|---|---|---|---|
| `created` | Solicitação criada | `fa-file-circle-plus` | neutro | `ttsc-surface-2` / `ttsc-text-muted` |
| `submitted` | Enviada para análise | `fa-paper-plane` | `tl-info` | `ttsc-info` 12% / `ttsc-info-text` |
| `auto_evaluated` | Avaliação automática | `fa-microchip` | `tl-info` | idem |
| `reviewed` | Em revisão | `fa-magnifying-glass` | `tl-warning` | `ttsc-warning` 14% / `ttsc-warning-text` |
| `approved` | Aprovada | `fa-circle-check` | `tl-success` | `ttsc-accent-soft` / `ttsc-accent-text` |
| `confirmed` | Matrícula confirmada | `fa-badge-check` | `tl-success` | idem |
| `rejected` | Recusada | `fa-circle-xmark` | `tl-danger` | `ttsc-danger` 12% / `ttsc-danger-text` |
| `cancelled` | Cancelada | `fa-ban` | `tl-danger` | idem |
| `notified` | Responsável notificado | `fa-bell` | neutro | — |

Linha vertical `ttsc-border-soft`; observação em `ttsc-canvas` + `ttsc-border-soft`; data `ttsc-text-muted`.

## API

Sem JavaScript obrigatório: o PHP renderiza a lista. Contrato de dados por item:

| Campo | Origem | Uso |
|---|---|---|
| `action` | `enrollment_request_history.action` | título, ícone e tom (mapa acima) |
| `old_status` / `new_status` | colunas homônimas | badges “Em análise → Aprovada” (rótulos do catálogo de `enrollment_requests.status`) |
| `actor_name` / `actor_type` | cache do nome / `student \| admin \| system` | autor; sem nome → “Responsável/aluno”, “Secretaria”, “Sistema” |
| `details` | texto livre | `.ttsc-timeline-note` (escapado) |
| `created_at` | timestamp | `<time datetime>` + “dd/mm/aaaa às hh:mm” |

| Ordem | Uso |
|---|---|
| Decrescente (mais recente no topo) | painel/drawer do registro (padrão) |
| Crescente | relatório impresso / exportação |

## Acessibilidade

- `<ol>` (lista ordenada) dentro de uma seção com título (`aria-labelledby`); cada item é lido como “Aprovada, 18/10/2026 às 09:00, Juliana Prado, Em análise para Aprovada”.
- Ícones decorativos (`aria-hidden`); o sentido está no texto do título. A seta entre status tem `aria-label="para"`.
- `<time datetime="2026-10-18T09:00:00">` para máquinas; texto formatado em pt-BR para pessoas.
- Tom por cor **e** por ícone/título (recusada ≠ aprovada mesmo sem cor). Textos `ttsc-text`/`ttsc-text-2`; ícones em `*-text` (≥ 4,5:1).

## Modelos

### HTML

```html
<?php
$actions = [
  'created' => ['Solicitação criada', 'fa-file-circle-plus', ''],
  'submitted' => ['Enviada para análise', 'fa-paper-plane', 'tl-info'],
  'auto_evaluated' => ['Avaliação automática', 'fa-microchip', 'tl-info'],
  'reviewed' => ['Em revisão', 'fa-magnifying-glass', 'tl-warning'],
  'approved' => ['Aprovada', 'fa-circle-check', 'tl-success'],
  'confirmed' => ['Matrícula confirmada', 'fa-badge-check', 'tl-success'],
  'rejected' => ['Recusada', 'fa-circle-xmark', 'tl-danger'],
  'cancelled' => ['Cancelada', 'fa-ban', 'tl-danger'],
  'notified' => ['Responsável notificado', 'fa-bell', ''],
];
$actorLabel = ['student' => 'Responsável/aluno', 'admin' => 'Secretaria', 'system' => 'Sistema'];
?>
<section class="ttsc-card" aria-labelledby="hist-title">
  <div class="ttsc-card-header"><h3 class="ttsc-card-title" id="hist-title">Histórico da solicitação</h3></div>
  <div class="ttsc-card-content">
    <ol class="ttsc-timeline">
      <?php foreach ($history as $h): [$label, $icon, $tone] = $actions[$h['action']] ?? [$h['action'], 'fa-circle', '']; ?>
        <li class="ttsc-timeline-item <?= $tone ?>">
          <span class="ttsc-timeline-icon" aria-hidden="true"><i class="fa-light <?= $icon ?>"></i></span>
          <div class="ttsc-timeline-body">
            <div class="ttsc-timeline-head">
              <span class="ttsc-timeline-title"><?= $this->e($label) ?></span>
              <time class="ttsc-timeline-time" datetime="<?= $this->e(date('c', strtotime($h['created_at']))) ?>">
                <?= date('d/m/Y \à\s H:i', strtotime($h['created_at'])) ?>
              </time>
            </div>
            <div class="ttsc-timeline-meta">
              <i class="fa-light <?= $h['actor_type'] === 'system' ? 'fa-gear' : 'fa-user' ?>"></i>
              <?= $this->e($h['actor_name'] ?: ($actorLabel[$h['actor_type']] ?? '')) ?>
              <?php if ($h['old_status'] && $h['new_status']): ?>
                · <span class="ttsc-badge ttsc-badge-sm ttsc-badge-outline"><?= $this->e($statusLabel[$h['old_status']] ?? $h['old_status']) ?></span>
                <i class="fa-light fa-arrow-right" aria-label="para"></i>
                <span class="ttsc-badge ttsc-badge-sm ttsc-badge-outline"><?= $this->e($statusLabel[$h['new_status']] ?? $h['new_status']) ?></span>
              <?php endif; ?>
            </div>
            <?php if ($h['details']): ?><div class="ttsc-timeline-note"><?= $this->e($h['details']) ?></div><?php endif; ?>
          </div>
        </li>
      <?php endforeach; ?>
    </ol>
  </div>
</section>
```

### CSS

```css
/* assets/css/ttsc.timeline.css */
.ttsc-timeline { list-style: none; margin: 0; padding: 0; }
.ttsc-timeline-item { position: relative; display: grid; grid-template-columns: 32px 1fr; gap: var(--ttsc-space-3); padding-bottom: 18px; }
.ttsc-timeline-item:not(:last-child)::before { content: ""; position: absolute; left: 15px; top: 32px; bottom: 0; width: 2px; background: var(--ttsc-border-soft); }
.ttsc-timeline-icon { width: 32px; height: 32px; border-radius: var(--ttsc-radius-pill); display: flex; align-items: center; justify-content: center; font-size: 14px;
  background: var(--tl-soft, var(--ttsc-surface-2)); color: var(--tl-text, var(--ttsc-text-muted)); border: 1px solid var(--tl-border, var(--ttsc-border)); }
.ttsc-timeline-body { min-width: 0; padding-top: 5px; }
.ttsc-timeline-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 10px; }
.ttsc-timeline-title { font-size: 13px; font-weight: 600; color: var(--ttsc-text); }
.ttsc-timeline-time { margin-left: auto; font-size: 12px; color: var(--ttsc-text-muted); white-space: nowrap; }
.ttsc-timeline-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-top: 2px; font-size: 12px; color: var(--ttsc-text-2); }
.ttsc-timeline-meta i { color: var(--ttsc-text-muted); }
.ttsc-timeline-note { margin-top: 6px; padding: 8px 10px; font-size: 12px; line-height: 1.5; color: var(--ttsc-text-2);
  background: var(--ttsc-canvas); border: 1px solid var(--ttsc-border-soft); border-radius: var(--ttsc-radius-control); }
.tl-success { --tl-soft: var(--ttsc-accent-soft); --tl-text: var(--ttsc-accent-text); --tl-border: var(--ttsc-accent-border); }
.tl-danger  { --tl-soft: color-mix(in srgb, var(--ttsc-danger) 12%, transparent);  --tl-text: var(--ttsc-danger-text);  --tl-border: color-mix(in srgb, var(--ttsc-danger) 35%, transparent); }
.tl-info    { --tl-soft: color-mix(in srgb, var(--ttsc-info) 12%, transparent);    --tl-text: var(--ttsc-info-text);    --tl-border: color-mix(in srgb, var(--ttsc-info) 35%, transparent); }
.tl-warning { --tl-soft: color-mix(in srgb, var(--ttsc-warning) 14%, transparent); --tl-text: var(--ttsc-warning-text); --tl-border: color-mix(in srgb, var(--ttsc-warning) 40%, transparent); }
/* compacta (drawer estreito) */
.ttsc-timeline-compact .ttsc-timeline-time { margin-left: 0; width: 100%; }
@media print { .ttsc-timeline-item { break-inside: avoid; } }
```

### JS

Renderização no servidor dispensa JS. Para atualizar a linha do tempo no drawer após uma ação (sem recarregar), o mesmo mapa em JS:

```js
// assets/js/core/ttsc.timeline.js
const ACTIONS = {
  created: ['Solicitação criada', 'fa-file-circle-plus', ''], submitted: ['Enviada para análise', 'fa-paper-plane', 'tl-info'],
  auto_evaluated: ['Avaliação automática', 'fa-microchip', 'tl-info'], reviewed: ['Em revisão', 'fa-magnifying-glass', 'tl-warning'],
  approved: ['Aprovada', 'fa-circle-check', 'tl-success'], confirmed: ['Matrícula confirmada', 'fa-badge-check', 'tl-success'],
  rejected: ['Recusada', 'fa-circle-xmark', 'tl-danger'], cancelled: ['Cancelada', 'fa-ban', 'tl-danger'],
  notified: ['Responsável notificado', 'fa-bell', ''],
};
const STATUS = { draft: 'Rascunho', submitted: 'Enviada', pending_review: 'Em análise', approved: 'Aprovada',
  rejected: 'Recusada', confirmed: 'Confirmada', cancelled: 'Cancelada', expired: 'Expirada' };
const ACTOR = { student: 'Responsável/aluno', admin: 'Secretaria', system: 'Sistema' };
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fmt = new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });

export function renderTimeline(list, rows) {
  list.innerHTML = rows.map((r) => {
    const [label, icon, tone] = ACTIONS[r.action] || [r.action, 'fa-circle', ''];
    const iso = r.created_at.replace(' ', 'T');
    const change = r.old_status && r.new_status
      ? ` · <span class="ttsc-badge ttsc-badge-sm ttsc-badge-outline">${esc(STATUS[r.old_status] || r.old_status)}</span>
         <i class="fa-light fa-arrow-right" aria-label="para"></i>
         <span class="ttsc-badge ttsc-badge-sm ttsc-badge-outline">${esc(STATUS[r.new_status] || r.new_status)}</span>` : '';
    return `<li class="ttsc-timeline-item ${tone}">
      <span class="ttsc-timeline-icon" aria-hidden="true"><i class="fa-light ${icon}"></i></span>
      <div class="ttsc-timeline-body">
        <div class="ttsc-timeline-head"><span class="ttsc-timeline-title">${esc(label)}</span>
          <time class="ttsc-timeline-time" datetime="${esc(iso)}">${fmt.format(new Date(iso)).replace(',', ' às')}</time></div>
        <div class="ttsc-timeline-meta"><i class="fa-light ${r.actor_type === 'system' ? 'fa-gear' : 'fa-user'}"></i>${esc(r.actor_name || ACTOR[r.actor_type] || '')}${change}</div>
        ${r.details ? `<div class="ttsc-timeline-note">${esc(r.details)}</div>` : ''}
      </div></li>`;
  }).join('');
}

export async function reloadTimeline(list, requestUuid) {
  const res = await fetch(`/admin/enrollment/requests/${encodeURIComponent(requestUuid)}/history`, { headers: { Accept: 'application/json' } });
  if (res.ok) renderTimeline(list, (await res.json()).data);
}
```

### SQL

```sql
-- Histórico de uma solicitação, mais recente primeiro (id desempata eventos no mesmo segundo)
SELECT h.action, h.old_status, h.new_status, h.actor_name, h.actor_type, h.details, h.created_at
  FROM enrollment_request_history h
  JOIN enrollment_requests r ON r.uuid = h.request_uuid AND r.deleted_at IS NULL
 WHERE h.request_uuid = :request_uuid
 ORDER BY h.created_at DESC, h.id DESC
 LIMIT 50;
```

A tabela é **somente inserção** (cada ação do fluxo grava uma linha — ver o `INSERT` em [SweetAlert](../SweetAlert/README.md)); `actor_name` é cache para não depender do usuário existir. O controller passa `$history` e `$statusLabel` (catálogo `ref_enum_enrollment_requests_status_*`) para a view. `ip_address` não é exibido na timeline (dado pessoal; fica para auditoria).

## Faça / Não faça

- **Faça:** `<ol>` + `<time datetime>`, título da ação em pt-BR e autor sempre visível.
- **Faça:** tom por ação com ícone **e** texto; neutro para eventos informativos.
- **Faça:** paginar/limitar (50) e oferecer “ver histórico completo”.
- **Não faça:** editar ou apagar linhas de histórico — corrija com um novo evento.
- **Não faça:** mostrar IP, user agent ou CPF na linha do tempo.
- **Não faça:** usar a timeline para comparar vários registros (tabela).
