# StarterKitSupportPortal

Kit do portal de suporte do cliente (SAC): o render real de `resources/views/web/layouts/portal.php` com o painel `web/pages/support_portal_dashboard.php` — navegação enxuta, saudação, três indicadores, filtros por status e a tabela de tickets.

## Quando usar

- Telas do cliente final do SAC (responsável, ex-aluno, fornecedor) que entra só com e-mail + código: `/support/portal` (login), `verify`, `dashboard`, `new`, `tickets/{uuid}`, `kb` — `web/pages/support_portal_*.php` sobre `web::layouts/portal`.
- Páginas públicas de autoatendimento com tema próprio leve e sem o chassi do app.
- Atendente/agente do SAC trabalha dentro do app → [StarterKitAppShell](../StarterKitAppShell/README.md). Login de usuários do sistema → [StarterKitAuth](../StarterKitAuth/README.md). Site institucional → [StarterKitPublicSite](../StarterKitPublicSite/README.md).

## Anatomia

```
nav.portal-nav     [headset] Portal de Suporte          Atendimentos  Base de Conhecimento  ← Site  [tema] [engrenagem v]
main.portal-main   (máx. 1100px, centralizado)
  section('content') — dashboard:
    .page-header   "Olá, Mariana Albuquerque" · "Acompanhe seus tickets de suporte"        [+ Novo Ticket]
    .stats-row     .stat-card × 3: [4 Total de Atendimentos] [2 Aberto] [2 Resolvido]
    .portal-tabs   Todos 4 · Aberto 2 · Resolvido 2 · Em Andamento · Aguardando   (role="tab", data-filter)
    table          # · Assunto (+ categoria) · Status (.badge-status.badge-<status>) · Prioridade (cor da prioridade) · Data
footer.portal-footer   Atendimentos · Base de Conhecimento · Privacidade · Termos · DPO · Site Principal
`.portal-toast` · SSE /support/portal/api/events · consent-cookie.js · section('scripts')
```

| Parte | Origem real | Obrigatório |
|---|---|---|
| Layout | `web/layouts/portal.php` (`$this->layout('web::layouts/portal', ['title' => …])`) | sim |
| Tema e estilos | `<style>` no próprio layout: variáveis `--accent`, `--bg`, `--surface`, `--text`, `--fg-2`, `--border`, `--muted`, `--radius` (claro em `:root`, escuro em `[data-theme="dark"]`) | sim |
| Navegação | `nav.portal-nav` + `.portal-nav-links` + `#settingsDropdown` (opções `.portal-theme-option[data-theme]`) | sim |
| Conteúdo | `main.portal-main` ← `section('content')` | sim |
| Rodapé | `footer.portal-footer` | sim |
| Toasts | `window.portalToast(msg, tipo, duração)` | sim |
| Tempo real | `EventSource('/support/portal/api/events')`: `ticket.created`, `ticket.message`, `ticket.typing` | opcional |
| Slots | `section('content')`, `section('scripts')` | — |

## Variantes / Estados

| Estado | Como | Observação |
|---|---|---|
| Claro / escuro / sistema | `localStorage['portal_theme']` + cookie `portal_theme` (o PHP usa o cookie no `data-theme` inicial); `#themeToggle` cicla Claro → Escuro → Sistema | chave própria do portal |
| ≤ 768px | links da nav viram menu (hambúrguer); só tema e engrenagem ficam | Mobile 390 |
| ≤ 640px | indicadores e tabela compactos | Mobile 390 |
| Filtro | `.portal-tab[data-filter]` mostra/oculta `tr.ticket-row[data-status]`; também lê `?filter=` da URL; "Aberto" = tudo que não é `resolved`/`closed` | sem recarregar |
| Sem tickets | a página mostra o estado vazio com "Novo Ticket" | — |
| Status | `new`, `open`, `in_progress`, `waiting_customer`, `resolved`, `closed` (`badge-<status>`) | rótulo por `__('portal_status_<status>', 'portal', …)` |

Corrigido no repo (commit `243e7a45c` fix(views)): os status agora saem traduzidos ("Aberto", "Em andamento", "Resolvido", "Fechado") e o JS de tema de `portal.php` não tem mais o erro de sintaxe — o kit usa o arquivo como está. Única adaptação que restou no kit: o `EventSource('/support/portal/api/events')` (caminho absoluto) foi desligado por não haver servidor.

## API

| Ponto | Efeito |
|---|---|
| `SupportPortalController` | `login` (e-mail) → código → sessão `sac_portal_sessions.token`; `dashboard`, `ticketDetail`, `newTicket`, `kb` |
| Dados da view do painel | `customer` (objeto com `name`), `tickets` (objetos `uuid, number, subject, status, priority_name, priority_color, category_name, created_at`), `stats` (`total`, `open`, `resolved`), `title` |
| `window.portalToast(message, type, duration)` | toast do portal (`success`, `info`, `error`) |
| `window.onPortalTyping(d)` | gancho da página para o evento `ticket.typing` |
| `.portal-tab[data-filter="all|open|resolved|in_progress|waiting_customer"]` | filtro local da tabela |

## Acessibilidade

- As abas de filtro são `button role="tab"` com contagem em texto; a tabela tem cabeçalhos `th`.
- A linha inteira é clicável (`onclick` em `tr`), mas o número do ticket deve continuar sendo um link focável — mantenha um `<a>` na primeira célula ao estender.
- Prioridade mostrada por texto ("Alta", "Média", "Baixa") além da cor vinda de `sac_priorities.color`.
- Botão de tema com `aria-label` descritivo do ciclo (Claro / Escuro / Sistema).

## Modelos

### HTML

```php
<?php $this->layout('web::layouts/portal', ['title' => $title ?? 'Meus Atendimentos']) ?>
<?php $this->start('content') ?>
<div class="page-header">
  <div>
    <h1>Olá, <?= $this->e($customer->name ?? 'Cliente') ?></h1>
    <p>Acompanhe seus tickets de suporte</p>
  </div>
  <a href="<?= url('/support/portal/new') ?>" class="portal-btn" id="newTicketBtn"><i class="fa-light fa-plus" aria-hidden="true"></i> Novo Ticket</a>
</div>

<div class="portal-tabs" role="tablist">
  <button class="portal-tab active" data-filter="all" role="tab" aria-selected="true">Todos <span class="tab-count"><?= (int) ($stats['total'] ?? 0) ?></span></button>
  <button class="portal-tab" data-filter="open" role="tab" aria-selected="false">Aberto <span class="tab-count"><?= (int) ($stats['open'] ?? 0) ?></span></button>
</div>

<table>
  <thead><tr><th>#</th><th>Assunto</th><th>Status</th><th>Prioridade</th><th>Data</th></tr></thead>
  <tbody>
  <?php foreach ($tickets as $t): ?>
    <tr class="ticket-row" data-status="<?= $this->e($t->status) ?>">
      <td><a href="<?= url('/support/portal/tickets/' . $this->e($t->uuid)) ?>"><?= $this->e($t->number) ?></a></td>
      <td><?= $this->e($t->subject) ?><div class="ticket-meta"><?= $this->e($t->category_name ?? '') ?></div></td>
      <td><span class="badge-status badge-<?= $this->e($t->status) ?>"><?= $this->e(__('portal_status_' . $t->status, 'portal', 'Aberto')) ?></span></td>
      <td><span class="priority-pill" style="--prio: <?= $this->e($t->priority_color ?? '#94a3b8') ?>"><?= $this->e($t->priority_name ?? '—') ?></span></td>
      <td><?= $this->e(date('d/m/Y', strtotime($t->created_at))) ?></td>
    </tr>
  <?php endforeach; ?>
  </tbody>
</table>
<?php $this->stop() ?>
```

### CSS

O CSS do portal vive no `<style>` do layout (sem arquivo externo além de `fonts/fontawesome.v7.2.0/css/all.css` e `ttsc.rtl.css`). Ao estender, use as variáveis do portal com a ponte dos tokens do DS:

```css
.priority-pill {
  display: inline-flex; align-items: center; gap: 6px; padding: 2px 8px; border-radius: var(--ttsc-radius-pill, 9999px);
  font-size: 11px; font-weight: 600; color: var(--text, var(--ttsc-text));
  background: color-mix(in oklab, var(--prio) 14%, transparent);
}
.priority-pill::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--prio); }
.ticket-meta { font-size: 11px; color: var(--muted, var(--ttsc-text-muted)); margin-top: 2px; }
```

### JS

```js
// Filtro com teclado (setas) e aria-selected sobre as abas reais .portal-tab
(function () {
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.portal-tab[data-filter]'));
  function select(tab) {
    tabs.forEach(function (t) { var on = t === tab; t.classList.toggle('active', on); t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; });
    var f = tab.dataset.filter;
    document.querySelectorAll('tr.ticket-row').forEach(function (row) {
      var s = row.dataset.status;
      row.hidden = !(f === 'all' || s === f || (f === 'open' && s !== 'resolved' && s !== 'closed'));
    });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(t); });
    t.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      var n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; n.focus(); select(n);
    });
  });
})();
```

### SQL

Banco do **tenant** (mesmas consultas do `SupportPortalController`); o controller converte as linhas em objetos (`FETCH_OBJ`) e calcula `stats` contando `resolved`/`closed` contra os demais.

```sql
-- cliente da sessão do portal
SELECT c.id, c.uuid, c.name, c.email
  FROM sac_portal_sessions ps
  JOIN sac_customers c ON c.id = ps.customer_id
 WHERE ps.token = :code AND ps.tenant_id = :tenant_id AND ps.expires_at > NOW();

-- tickets do cliente (tabela do painel)
SELECT t.uuid, t.number, t.subject, t.status, t.created_at,
       p.name AS priority_name, p.color AS priority_color
  FROM sac_tickets t
  LEFT JOIN sac_priorities p ON p.id = t.priority_id
 WHERE t.customer_id = :customer_id AND t.tenant_id = :tenant_id
 ORDER BY t.created_at DESC;
```

A view usa `category_name`, mas a consulta real do controller não faz `JOIN` com `sac_categories` — a categoria só aparece se o controller passar a juntar `LEFT JOIN sac_categories c ON c.id = t.category_id`. Os 4 tickets do kit são ilustrativos, montados em memória no harness (nada foi gravado no banco).

## Como começar um projeto a partir do kit

1. **Arquivos do kit**: `kit.html`, `assets/css/ttsc.rtl.css`, `assets/js/consent-cookie.js`, `assets/fa.css`; gerado por `$SPD/dsh/gen_kits.py` a partir de `php $SPD/app/view_harness.php /support/portal web::pages/support_portal_dashboard <saída> '<json com customer, stats, tickets>'`.
2. **Nova tela do portal no repo**: view em `web/pages/support_portal_<nome>.php` com `$this->layout('web::layouts/portal', ['title' => …])` e método no `SupportPortalController` validando a sessão (`sac_portal_sessions`).
3. **Outro projeto**: copie `web/layouts/portal.php` (traz todo o CSS e o JS do portal), `app/partials/locale_init.php`, `assets/css/ttsc.rtl.css`, `assets/js/consent-cookie.js` e `fonts/fontawesome.v7.2.0/`; se a instalação não ficar na raiz do domínio, troque o `EventSource` para `url('/support/portal/api/events')`.

## Faça / Não faça

- **Faça:** valide `sac_portal_sessions.expires_at` em toda requisição do portal.
- **Faça:** mantenha as traduções `portal_status_*` ao criar status novos — o cliente final não deve ver `in_progress`.
- **Não faça:** mostrar mensagens internas (`sac_ticket_messages.is_internal = 1`) no portal.
- **Não faça:** reaproveitar o CSS do app (`ttsc.design-system.css`) aqui; o portal é leve de propósito.
