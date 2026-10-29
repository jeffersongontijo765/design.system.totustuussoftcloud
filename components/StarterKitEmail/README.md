# StarterKitEmail

Kit de e-mail transacional: o layout real `resources/views/emails/sac/layout.php` (contêiner de 600px, cabeçalho em degradê azul, corpo, botão de ação e rodapé) com os corpos `sac/new_message.php` e `sac/sla_breach.php`, mais o e-mail independente `emails/dsr_notification.php` (LGPD).

## Quando usar

- Notificação por e-mail disparada pelo sistema: nova mensagem em ticket, SLA violado, ticket atribuído, solicitação de titular (LGPD), e por extensão avisos acadêmicos e financeiros (boleto disponível, matrícula confirmada).
- Um único layout com `$bodyContent` trocável: crie só o corpo (`emails/<módulo>/<evento>.php`) e envolva com o `layout.php`.
- Aviso dentro do app (sino, toast) → notificações do [StarterKitAppShell](../StarterKitAppShell/README.md). Documento para imprimir/anexar → [StarterKitPrint](../StarterKitPrint/README.md).

## Anatomia

```
body (#f3f4f6)
└─ .container (máx. 600px, margem 40px, raio 12px, borda #e5e7eb)
   ├─ .header   (degradê #1e3a8a → #0f172a)  h1 $companyName · p $moduleName
   ├─ .content
   │   └─ $bodyContent  ← corpo renderizado à parte:
   │        .alert-bar (faixa azul com a frase principal)
   │        .grid > .grid-item / .grid-item-full (.label + .value / .value-highlight / .badge)
   │        .message-box (prévia da mensagem)
   │   └─ .actions > a.ttsc-btn ($actionUrl, $actionLabel)
   └─ .footer   "Esta é uma notificação automática…" · © ano
```

| Parte | Origem real | Obrigatório |
|---|---|---|
| Layout | `emails/sac/layout.php` — `$subject`, `$companyName`, `$moduleName`, `$bodyContent`, `$actionUrl`, `$actionLabel` | sim |
| Corpos | `emails/sac/new_message.php`, `sla_breach.php`, `ticket_assigned.php` | um por evento |
| Independente | `emails/dsr_notification.php` (HTML completo próprio, mesmo visual, cabeçalho "Privacidade e Proteção de Dados") | — |
| Render | `Mailer::template($nome, $dados)` / `SacNotificationService::renderTemplate()` = `extract($dados)` + `include` + `ob_get_clean()` (PHP puro, não Plates) | sim |
| Estilos | `<style>` no `<head>` com classes (não inline por elemento); o botão traz `style="color:#ffffff"` inline | sim |

## Variantes / Estados

| Variante (botão) | Composição | Dados |
|---|---|---|
| SAC: nova mensagem | `layout` + `new_message` | `ticketNumber`, `ticketSubject`, `senderName`, `customerName`, `ticketStatus`, `messagePreview` |
| SAC: SLA | `layout` + `sla_breach` | `ticketNumber`, `ticketSubject`, `slaType`, `customerName`, `priorityName`, `priorityColor`, `slaDeadline` |
| LGPD: DSR | `dsr_notification` | `companyName`, `protocol`, `requestTypeLabel`, `lawCode`, `subjectName`, `subjectEmail`, `subjectDocument`, `receivedAt`, `deadlineAt`, `description`, `actionUrl` |
| Webmail (1440) | contêiner centralizado de 600px | — |
| Celular (390) | ≤ 480px `layout.php` e `dsr_notification.php` passam `.grid` para 1 coluna e reduzem o padding | — |
| Tema | **sempre claro** — e-mail não segue o tema do app; o kit não aplica o tema do preview | — |

Corrigido no repo (commit `a2b03b61a` fix(mail,auth,logging)): `Mailer::template()` aceita nomes com subpasta (`sac/layout`), então os e-mails do SAC voltaram a ser enviados; `notifyTicketAssigned()` usa `sac/layout`; `getCompanyName()` lê `tenants.company_name`; `Mailer::loadFromDatabase()` funciona com a coluna `settings.is_deleted` criada pela migração `2026_10_22_000001`; e `dsr_notification.php` ganhou regra para telas estreitas (uma coluna no celular, como no kit). Pendentes: nenhum código envia `dsr_notification` hoje, e os assuntos/rótulos do serviço continuam em inglês ("View Ticket", "New message from…").

## API

| Ponto | Efeito |
|---|---|
| `Mailer::to($email)->subject($s)->template('sac/layout', [...])->send()` | renderiza e envia (`From:` montado com as configurações) |
| `Mailer::template($nome)` | aceita `nome` ou `pasta/nome` (`#^[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*$#`), resolve `views/emails/<nome>.php` |
| `Mailer::loadFromDatabase()` | lê `settings` (`category = 'email'`) para host/porta/remetente |
| `->html($html)`, `->attach($arquivo, $nome)`, `->header($k, $v)` | corpo pronto, anexos, cabeçalhos |
| `SacNotificationService::notifyNewMessage()`, `notifySlaBreach()`, `notifyTicketAssigned()` | montam os dados e enviam; também gravam a notificação in-app |

## Acessibilidade

- `<html>` sem `lang` no layout real — acrescente `lang="pt-BR"` ao copiar (leitores de tela de webmail usam).
- Uma única ação principal (`a.ttsc-btn`) com texto descritivo ("Ver mensagem", não "Clique aqui"); o link também deve aparecer em texto para clientes que bloqueiam estilos.
- Contraste: texto `#1f2937` sobre branco e `.label` `#6b7280` (4,8:1); botão branco sobre `#1e3a8a`.
- Não dependa de cor para prioridade/status: `.badge` sempre com o nome ("Alta").

## Modelos

### HTML

Corpo novo (boleto disponível) para o mesmo layout:

```php
<?php // resources/views/emails/financial/boleto_disponivel.php — corpo; vai em $bodyContent ?>
<div class="alert-bar">
  <p>O boleto da mensalidade de <strong><?= htmlspecialchars($competencia) ?></strong> de <strong><?= htmlspecialchars($alunoNome) ?></strong> já está disponível.</p>
</div>
<div class="grid">
  <div class="grid-item"><div class="label">Vencimento</div><div class="value-highlight"><?= htmlspecialchars($vencimento) ?></div></div>
  <div class="grid-item"><div class="label">Valor</div><div class="value"><?= htmlspecialchars($valorFormatado) ?></div></div>
  <div class="grid-item-full"><div class="label">Linha digitável</div><div class="value"><span class="inline-code"><?= htmlspecialchars($linhaDigitavel) ?></span></div></div>
</div>
```

```php
// envio (mesma composição do SacNotificationService)
$render = static function (string $tpl, array $d): string {   // mesmo extract + include do SacNotificationService::renderTemplate()
    extract($d, EXTR_SKIP); ob_start(); include resource_path('views/emails/' . $tpl . '.php'); return ob_get_clean();
};
Mailer::to($responsavelEmail)
    ->subject('Boleto de outubro disponível — Pedro Albuquerque')
    ->template('sac/layout', [
        'companyName' => 'Colégio Santa Clara', 'moduleName' => 'Financeiro — Mensalidades',
        'bodyContent' => $render('financial/boleto_disponivel', [
            'competencia' => 'outubro/2026', 'alunoNome' => 'Pedro Albuquerque', 'vencimento' => '10/11/2026',
            'valorFormatado' => 'R$ 1.280,00', 'linhaDigitavel' => '34191.79001 01043.510047 91020.150008 1 98760000128000',
        ]),
        'actionUrl' => url('/parents/financial/invoices'), 'actionLabel' => 'Ver boleto',
        'subject' => 'Boleto de outubro disponível',
    ])
    ->send();
```

### CSS

E-mail não usa tokens do DS (clientes de e-mail não resolvem `var()` de forma confiável): os valores do layout são literais. Ao estender, mantenha literais e espelhe a paleta do app:

```css
/* acrescentar no <style> do layout.php */
.badge-success { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }   /* = --ttsc-accent-soft / --ttsc-accent-text */
.badge-warning { background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }
.value-money { font-variant-numeric: tabular-nums; font-weight: 700; color: #111827; }
@media (max-width: 480px) { .container { margin: 0; border-radius: 0; } .actions .ttsc-btn { display: block; text-align: center; } }
```

### JS

E-mail não executa JavaScript. O JS deste kit é o da pré-visualização no app (ex.: tela de modelos de e-mail), que injeta o HTML renderizado num `iframe` isolado:

```js
// Pré-visualização segura de um e-mail renderizado pelo servidor (GET .../email-preview?template=sac/new_message)
(function () {
  var frame = document.getElementById('emailPreview');
  if (!frame) return;
  frame.setAttribute('sandbox', '');               // sem scripts, sem formulários, sem navegação
  fetch(frame.dataset.src, { credentials: 'same-origin', headers: { 'Accept': 'text/html' } })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
    .then(function (html) { frame.srcdoc = html; })
    .catch(function (err) { frame.srcdoc = '<p style="font-family:sans-serif;color:#b91c1c">Não foi possível carregar a prévia (' + err.message + ').</p>'; });
  document.querySelectorAll('[data-email-width]').forEach(function (b) {
    b.addEventListener('click', function () { frame.style.width = b.dataset.emailWidth + 'px'; });
  });
})();
```

### SQL

```sql
-- 1) Dados do ticket para o corpo (banco do tenant) — SacNotificationService::getTicketSummary()
SELECT t.subject, t.status,
       c.name AS customer_name, p.name AS priority_name, p.color AS priority_color,
       q.name AS queue_name, ch.name AS channel_name,
       t.sla_deadline_response, t.sla_deadline_resolution
  FROM sac_tickets t
  LEFT JOIN sac_customers c  ON c.id = t.customer_id
  LEFT JOIN sac_priorities p ON p.id = t.priority_id
  LEFT JOIN sac_queues q     ON q.id = t.queue_id
  LEFT JOIN sac_channels ch  ON ch.id = t.channel_id
 WHERE t.id = :ticket_id AND t.tenant_id = :tenant_id;

-- 2) Nome da instituição no cabeçalho (banco master) — SacNotificationService::getCompanyName()
SELECT company_name FROM tenants WHERE uuid = :tenant_id LIMIT 1;

-- 3) Configuração de envio — Mailer::loadFromDatabase()
SELECT setting_key, value
  FROM settings
 WHERE category = 'email' AND (is_deleted = 0 OR is_deleted IS NULL)
 ORDER BY setting_key;
```

O serviço formata `sla_deadline_*` com `date('d/m/Y H:i')`, passa as linhas como variáveis para o corpo e o corpo pronto como `$bodyContent` para o layout. Os dados dos 3 e-mails do kit são ilustrativos (montados em memória no harness).

## Como começar um projeto a partir do kit

1. **Arquivos do kit**: `kit.html` (nova mensagem), `kit-sla.html`, `kit-dsr.html` — HTML exatamente como o PHP gera (sem assets externos); produzidos por `php $SPD/app/mail_print_harness.php <saída>` (mesmo `extract` + `include` do serviço) e copiados por `$SPD/dsh/gen_kits.py`.
2. **No repo**: corpo novo em `resources/views/emails/<módulo>/<evento>.php`; envie com `Mailer::to(…)->template('sac/layout', ['bodyContent' => $corpo, …])`.
3. **Outro projeto**: copie `emails/sac/layout.php` e os corpos; qualquer mailer serve (o layout é HTML+CSS no `<head>`). Teste em Gmail, Outlook e Apple Mail; para Outlook, considere inlinar o CSS na hora do envio.

## Faça / Não faça

- **Faça:** um layout, muitos corpos; `htmlspecialchars()` em toda variável (o layout já faz).
- **Faça:** assunto e botão em pt-BR e específicos ("Boleto de outubro disponível", "Ver boleto").
- **Faça:** largura máxima de 600px e uma coluna abaixo de 480px.
- **Não faça:** `var(--ttsc-…)`, fontes da web, JavaScript ou imagens remotas no e-mail.
- **Não faça:** enviar dados pessoais completos (CPF, saldo) no corpo — mascare como o `dsr_notification` (`***.482.***-**`).
