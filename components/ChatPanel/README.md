# ChatPanel

Caixa de entrada de atendimento embutida no painel, com lista de conversas, histórico com anexos, contexto do contato e campo de resposta com atalhos de teclado.

## Quando usar

- Central de atendimento (SAC, comercial ou acadêmico) em que o agente precisa ver a conversa e o contexto do contato na mesma tela.
- Times que atendem WhatsApp, chat do site e e-mail e alternam entre canais sem sair da página.
- Conversas que fazem parte de um fluxo maior (proposta, matrícula, cobrança) e dependem do histórico e dos dados do contato para a resposta.
- Ao lado de sugestões da IA, combine com [InsightPanel](../InsightPanel/README.md) para transformar a leitura do atendimento em próximos passos.
- Para uma conversa única e somente leitura dentro de um registro, prefira [Timeline](../Timeline/README.md) ou [RecordDrawers](../RecordDrawers/README.md).

Não use este componente em páginas públicas de marketing nem como substituto do widget flutuante. Para o botão de pré-atendimento em qualquer página, use `assets/js/ttsc.chat-widget.js`.

### Relação com o widget flutuante

O widget (`assets/js/ttsc.chat-widget.js`) é o chat de pré-atendimento do site: abre em um botão flutuante, coleta nome e assunto e envia a sessão para `/api/chat/widget/session`, que registra o pré-atendimento na fila do SAC. O ChatPanel é a outra ponta: a caixa de entrada interna onde o agente lê, responde e consulta o contexto. Eles podem compartilhar a mesma fila e o mesmo histórico por API, mas não compartilham markup, estado nem atalhos. Não troque um pelo outro: o widget atende o visitante; o painel atende o agente.

## Anatomia

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Caixa de entrada · 4 conversas · 2 não lidas           Novo atendimento    │
├──────────────┬────────────────────────────────────────────┬────────────────┤
│ Buscar...    │ Comercial · Proposta 2041  Online · ...    │ Tatiane Faria  │
│ ABERTAS   4  ├────────────────────────────────────────────┤ Contato        │
│ [conversa]   │ Hoje                                       │ Tags           │
│ [conversa]   │  Tatiane  Bom dia! ...                     │ Resumo da IA   │
│ [conversa]   │                     Você  Sim, ...         │ Atendimento    │
│ [conversa]   │  contrato.pdf · 248 KB                     │ [Criar tarefa] │
│              ├────────────────────────────────────────────┤ [Abrir ficha]  │
│ /atalho      │ Tatiane está digitando...                  │                │
│ Resolvidas   │ [Escreva uma resposta...]        [Enviar]  │                │
└──────────────┴────────────────────────────────────────────┴────────────────┘
```

| Parte | Classe / elemento | Obrigatório | Função |
|---|---|---|---|
| Contêiner | `section.inbox` | sim | Superfície, borda e recorte do painel. |
| Cabeçalho | `.inbox-h` > `.inbox-id`, `.inbox-tools` | sim | Título, contagem de não lidas e ação principal. |
| Lista | `aside.convs` > `ul.conv-list` > `button.conv[data-conv]` | sim | Conversas disponíveis e canal de origem. |
| Busca | `#convSearch` | recomendado | Filtra a lista por nome, assunto ou prévia. |
| Não lidas | `.unread` + `.sr-only` | opcional | Contador visual e texto para leitor de tela. |
| Lista sobreposta no mobile | `#listToggle`, `#convScrim`, `#convClose` | sim abaixo de 820 px | Abre e fecha a lista sobre a conversa. |
| Conversa | `section.thread` > `.thread-h` | sim | Cabeçalho da conversa, status e ações. |
| Histórico | `#threadLog[role="log"]` | sim | Mensagens, dia, mensagens de sistema e anexos. |
| Mensagem | `.msg.msg-in` / `.msg.msg-out` | sim | Entrada ou saída, com autor e horário. |
| Mensagem de sistema | `.sys` | opcional | Transferência, assumir atendimento, resolução. |
| Anexo | `button.attach` | opcional | Nome, tamanho, tipo e ação de abrir. |
| Digitando | `#typingRow[role="status"]` | opcional | Indicador de digitação do contato ou da IA. |
| Campo de resposta | `form.composer#chatComposer` | sim | Texto, anexo, atalhos e envio. |
| Erro do campo | `#composerError` | sim | Validação de texto vazio e de arquivo grande. |
| Contexto | `aside.ctx` | recomendado | Contato, tags, resumo da IA, SLA e ações. |
| Resumo da IA | `.ai-card` | opcional | Leitura rápida com fontes e aviso de revisão. |
| Anúncio | `#chatLive[aria-live="polite"]` | sim | Mensagens de envio, anexo e IA para leitor de tela. |

## Variantes

| Variante | Classe / opção | Uso |
|---|---|---|
| Conversa humana | `.conv` + `.chan` | WhatsApp, chat ou e-mail, com ícone e rótulo do canal. |
| Conversa do assistente | `.conv.conv-ai`, `.msg-av-ai` | Histórico interno com a IA; o avatar usa o ícone de faíscas. |
| Lista sobreposta | `@media (max-width:819px)` + `.is-list-open` | A lista cobre a conversa com scrim e fecha ao escolher. |
| Sem coluna de contexto | `@media (max-width:1099px)` | Abaixo de 1100 px o contexto é oculto para preservar a conversa. |
| Anexo | `button.attach` | Arquivo de até 10 MB, com nome e tamanho legíveis. |
| Anexo pendente | `.pending` | Prévia antes do envio, com botão de remover. |
| Tema | `data-theme` + tokens `--ttsc-*` | Claro e escuro sem CSS específico de tema. |

## Estados

- **Ativa:** `.conv.is-active` com `aria-current="true"`; a conversa selecionada perde o contador de não lidas.
- **Não lida:** `.unread` com o número e um `.sr-only` com “mensagens não lidas”. A cor não é o único sinal.
- **Busca vazia:** `#convEmpty` aparece com “Limpar busca” e o contador vai para zero.
- **Digitando:** `.typing` visível; `.typing.is-off` esconde sem remover do fluxo. Com movimento reduzido, os pontos param.
- **Resposta do assistente:** após o envio, `setTyping(true, 'Assistente IA')` e a resposta simulada entram depois de `replyDelay`.
- **Erro de envio:** `#composerError` visível, `aria-invalid="true"` no textarea e foco de volta no campo.
- **Arquivo grande:** o mesmo erro informa o limite de 10 MB e o anexo é descartado.
- **Lista aberta no mobile:** `aria-expanded="true"`, foco na busca, scrim visível e `inert` na conversa e no contexto.
- **Sem resultado de busca:** a lista continua no lugar; o vazio ocupa o espaço restante.

## Acessibilidade

- O histórico é `role="log"` com `aria-live="polite"` e `aria-relevant="additions"`; mensagens novas são anunciadas sem interromper a leitura.
- `#chatLive` é uma região separada para confirmar envio, anexo, IA e ações de menu. O texto é trocado em dois passos para o leitor perceber a atualização.
- No mobile, o botão “Conversas (4)” tem `aria-expanded` e `aria-controls`; ao abrir, o foco vai para a busca. `Esc`, o scrim e o botão de fechar devolvem o foco ao alternador, e a conversa/contexto ficam `inert`.
- Teclado: `Enter` envia, `Shift+Enter` quebra linha, `↑`/`↓` percorrem a lista, `Esc` fecha emoji, menu e lista. O foco visível usa `:focus-visible` com o token de acento.
- O campo de resposta tem rótulo acessível, dica de teclado e erro associado. O anexo é um botão com nome, tamanho e tipo no `aria-label`.
- Contraste: o texto não depende do verde; status, não lidas e anexos têm rótulo textual. A digitação tem texto além dos pontos animados.
- `prefers-reduced-motion` reduz animações e transições, inclusive os pontos de digitação e o deslizamento da lista.

## Faça / Não faça

- Faça: mantenha o contexto do contato ao lado da conversa em telas largas; ele evita trocar de página no meio do atendimento.
- Faça: mostre canal, SLA e não lidas no nível da conversa; são os sinais que definem a prioridade.
- Faça: peça confirmação antes de ações externas (enviar proposta, cobrar, cancelar) e registre a decisão.
- Faça: use `appendMessage` para a resposta confirmada pelo servidor, com o horário oficial.
- Não faça: autoenviar a resposta do assistente ao cliente; o texto é um rascunho interno até uma pessoa aprovar.
- Não faça: usar cor sozinha para não lida, risco ou status; some sempre um rótulo ou número.
- Não faça: esconder a lista no mobile sem um caminho de volta visível e focável.
- Não faça: reaproveitar este componente como widget público; o contexto e as ações são de agente.

## API

O preview se autoinicializa em `#chatInbox` ao carregar. Para montar em outro ponto:

```js
const chat = window.TTSCChatPanel.init(document.getElementById('chatInbox'), {
  replyDelay: 900,
  contactTypingDelay: 1400,
  maxFileSize: 10 * 1024 * 1024
});
```

`init` é idempotente por elemento e devolve a instância existente. Retorna `null` se o elemento não existir.

| Opção | Padrão | Efeito |
|---|---|---|
| `replyDelay` | `900` | Tempo, em ms, até a resposta do assistente. |
| `contactTypingDelay` | `1400` | Tempo, em ms, do indicador de digitação do contato. |
| `maxFileSize` | `10485760` | Limite do anexo em bytes (10 MB). |

| Método | Retorno | Efeito |
|---|---|---|
| `setConversation(id, focusTitle = true)` | instância | Troca a conversa pelo `data-conv`, limpa não lidas e carrega o histórico. `focusTitle: false` evita mover o foco. |
| `appendMessage(msg)` | instância | Acrescenta uma mensagem ao histórico e rola para o fim. |
| `setTyping(on, name)` | instância | Mostra ou esconde o indicador; `name` troca o texto. |
| `destroy()` | — | Remove listeners e timers e libera a instância do elemento. |

Formato de `appendMessage`:

```js
chat.appendMessage({
  direction: 'in',                 // 'in' (contato) ou 'out' (equipe)
  text: 'Recebi, obrigado.',
  author: 'Tatiane Faria',         // opcional; o padrão usa o contato ou a equipe
  time: '14:30',                   // opcional; o padrão usa a hora local
  attachment: { name: 'contrato.pdf', size: '248 KB', type: 'PDF' } // opcional
});
```

| Evento | `detail` | Quando |
|---|---|---|
| `ttsc:chat:send` | `{ conversationId, text, attachment }` | Ao enviar pelo campo de resposta ou por `Enter`. `attachment` é `null` ou o metadado `{ name, size, type }`. |

Atributos usados pelo preview: `data-conv` na conversa, `data-emoji` no seletor e `data-action` no menu de ações. O componente não persiste nada: o host decide o que fazer com o evento e devolve a mensagem confirmada via `appendMessage`.

O preview usa IDs fixos (`#threadLog`, `#composerError` etc.) e, por isso, monta **um painel por página**. Para mais de um, clone o bloco com IDs únicos e ajuste as consultas, ou renderize a segunda conversa em outra rota. No preview, os IDs de conversa são de demonstração (`comercial`, `suporte`, `ia`, `academico`); `setConversation` só encontra conversas que existam no `data-conv` e nos dados locais. Para dados reais, hidrate as threads pelo host ou adapte a fonte de dados do componente.

Anexos do preview são apenas metadados (`name`, `size`, `type`); o arquivo real não é enviado. Capture o `File` do input no host e faça o upload em uma chamada própria antes de confirmar a mensagem.

## Modelos

### HTML

```html
<section class="inbox" id="chatInbox" aria-labelledby="inboxTitle">
  <header class="inbox-h">
    <div class="inbox-id">
      <span class="inbox-mark" aria-hidden="true"><i class="fa-light fa-inbox"></i></span>
      <div>
        <h2 class="inbox-title" id="inboxTitle">Atendimento · Caixa de entrada</h2>
        <p class="inbox-sub"><b><?= (int) $naoLidas ?></b> não lidas · SLA médio de resposta <?= $this->e($slaMedio) ?></p>
      </div>
    </div>
    <button class="btn-new" type="button" id="newTicket"><i class="fa-light fa-plus" aria-hidden="true"></i>Novo atendimento</button>
  </header>

  <div class="inbox-body">
    <aside class="convs" id="convPanel" aria-label="Conversas">
      <div class="convs-h">
        <div class="convs-search-row">
          <label class="sr-only" for="convSearch">Buscar conversa</label>
          <div class="search">
            <i class="fa-light fa-magnifying-glass" aria-hidden="true"></i>
            <input id="convSearch" type="search" placeholder="Buscar conversa...">
          </div>
          <button class="convs-close" id="convClose" type="button" aria-label="Fechar lista de conversas">
            <i class="fa-light fa-xmark" aria-hidden="true"></i>
          </button>
        </div>
        <div class="convs-label"><span>Abertas</span><b id="openCount"><?= count($conversas) ?></b></div>
      </div>

      <div class="convs-scroll">
        <ul class="conv-list" id="convList">
          <?php foreach ($conversas as $c): ?>
          <li>
            <button class="conv<?= $c['ativa'] ? ' is-active' : '' ?>" type="button"
                    data-conv="<?= $this->e($c['uuid']) ?>" aria-current="<?= $c['ativa'] ? 'true' : 'false' ?>">
              <span class="conv-av" aria-hidden="true"><?= $this->e($c['iniciais']) ?></span>
              <span class="conv-main">
                <span class="conv-top">
                  <span class="conv-name"><?= $this->e($c['assunto']) ?></span>
                  <time class="conv-time" datetime="<?= $this->e($c['hora_iso']) ?>"><?= $this->e($c['hora']) ?></time>
                </span>
                <span class="conv-prev"><?= $this->e($c['previa']) ?></span>
                <span class="conv-foot">
                  <span class="chan"><i class="fa-light fa-comment" aria-hidden="true"></i><?= $this->e($c['canal']) ?></span>
                  <?php if ($c['nao_lidas']): ?>
                    <span class="unread"><?= (int) $c['nao_lidas'] ?></span>
                    <span class="sr-only">mensagens não lidas</span>
                  <?php endif; ?>
                </span>
              </span>
            </button>
          </li>
          <?php endforeach; ?>
        </ul>
        <div class="conv-empty" id="convEmpty" hidden>
          <i class="fa-light fa-magnifying-glass" aria-hidden="true"></i>
          <span>Nenhuma conversa encontrada.</span><br>
          <button type="button" id="clearSearch">Limpar busca</button>
        </div>
      </div>
    </aside>

    <button class="conv-scrim" id="convScrim" type="button" aria-label="Fechar lista de conversas" hidden></button>

    <section class="thread" aria-labelledby="threadTitle">
      <header class="thread-h">
        <button class="list-toggle" id="listToggle" type="button" aria-expanded="false" aria-controls="convPanel">
          <i class="fa-light fa-chevron-left" aria-hidden="true"></i> Conversas <span>(<?= count($conversas) ?>)</span>
        </button>
        <span class="thread-av" aria-hidden="true"><?= $this->e($contato['iniciais']) ?></span>
        <div class="thread-id">
          <h3 class="thread-title" id="threadTitle" tabindex="-1"><?= $this->e($conversa['assunto']) ?></h3>
          <p class="thread-status" id="threadStatus">
            <span class="st-on"><span class="dot" aria-hidden="true"></span>Online</span>
            <span aria-hidden="true">·</span>
            <span><?= $this->e($conversa['canal']) ?> · resposta em <?= $this->e($conversa['resposta_media']) ?></span>
          </p>
        </div>
      </header>

      <div class="thread-log" id="threadLog" role="log" aria-live="polite" aria-relevant="additions"
           aria-label="Mensagens da conversa <?= $this->e($conversa['assunto']) ?>" tabindex="0">
        <?php foreach ($mensagens as $m): ?>
          <?php if ($m['tipo'] === 'sistema'): ?>
            <div class="sys"><i class="fa-light fa-arrow-right-arrow-left" aria-hidden="true"></i><span><?= $this->e($m['texto']) ?></span></div>
          <?php else: ?>
            <div class="msg <?= $m['direcao'] === 'out' ? 'msg-out' : 'msg-in' ?>">
              <?php if ($m['direcao'] === 'in'): ?>
                <span class="msg-av" aria-hidden="true"><?= $this->e($m['iniciais']) ?></span>
              <?php endif; ?>
              <div class="msg-body">
                <div class="msg-meta">
                  <span class="msg-author"><?= $this->e($m['autor']) ?></span>
                  <time datetime="<?= $this->e($m['hora_iso']) ?>"><?= $this->e($m['hora']) ?></time>
                </div>
                <div class="msg-bubble">
                  <p><?= nl2br($this->e($m['texto'])) ?></p>
                  <?php if (!empty($m['anexo'])): ?>
                    <button class="attach" type="button" aria-label="Abrir <?= $this->e($m['anexo']['nome']) ?>, <?= $this->e($m['anexo']['tamanho']) ?>">
                      <span class="attach-ic" aria-hidden="true"><i class="fa-light fa-file-pdf"></i></span>
                      <span class="attach-txt">
                        <span class="attach-name"><?= $this->e($m['anexo']['nome']) ?></span>
                        <span class="attach-size"><?= $this->e($m['anexo']['tamanho']) ?> · <?= $this->e($m['anexo']['tipo']) ?></span>
                      </span>
                      <i class="fa-light fa-download attach-dl" aria-hidden="true"></i>
                    </button>
                  <?php endif; ?>
                </div>
              </div>
            </div>
          <?php endif; ?>
        <?php endforeach; ?>
      </div>

      <div class="typing is-off" id="typingRow" role="status">
        <span class="tdots" aria-hidden="true"><i></i><i></i><i></i></span>
        <span id="typingText"><?= $this->e($contato['primeiro_nome']) ?> está digitando…</span>
      </div>

      <form class="composer" id="chatComposer" novalidate>
        <div class="composer-box">
          <div class="pending" id="pendingFile" hidden>
            <i class="fa-light fa-paperclip" aria-hidden="true"></i>
            <span id="pendingName"></span>
            <button type="button" id="removeFile" aria-label="Remover anexo">
              <i class="fa-light fa-xmark" aria-hidden="true"></i>
            </button>
          </div>
          <label class="sr-only" for="msgInput">Mensagem</label>
          <textarea id="msgInput" rows="1" maxlength="2000" placeholder="Escreva uma resposta..."
                    aria-describedby="composerHint composerError"></textarea>
          <div class="composer-bar">
            <div class="composer-tools">
              <button class="tool" type="button" id="attachBtn" aria-label="Anexar arquivo">
                <i class="fa-light fa-paperclip" aria-hidden="true"></i>
              </button>
              <input type="file" id="fileInput" accept=".pdf,.png,.jpg,.jpeg,.doc,.docx" hidden>
              <span class="hint" id="composerHint">Enter envia · Shift+Enter quebra linha</span>
            </div>
            <button class="send" type="submit"><i class="fa-light fa-paper-plane" aria-hidden="true"></i>Enviar</button>
          </div>
        </div>
        <p class="composer-error" id="composerError" hidden></p>
      </form>
    </section>

    <aside class="ctx" aria-label="Contexto do contato">
      <div class="ctx-top">
        <span class="ctx-av" aria-hidden="true"><?= $this->e($contato['iniciais']) ?></span>
        <div>
          <h3 class="ctx-name"><?= $this->e($contato['nome']) ?></h3>
          <p class="ctx-org"><?= $this->e($contato['vinculo']) ?></p>
        </div>
      </div>
      <!-- Contato, tags, resumo da IA e ações -->
    </aside>
  </div>
</section>
<p class="sr-only" id="chatLive" aria-live="polite" aria-atomic="true"></p>
```

### CSS

Recorte das classes principais; o CSS completo, com todos os estados e o responsivo, está em `preview.html`.

```css
.inbox{background:var(--ttsc-surface);border:1px solid var(--ttsc-border);border-radius:var(--ttsc-radius-surface);box-shadow:var(--ttsc-shadow-sm);overflow:hidden}
.inbox-body{position:relative;display:grid;grid-template-columns:290px minmax(0,1fr) 250px;height:590px}
.thread{display:flex;flex-direction:column;min-width:0;min-height:0;background:var(--ttsc-surface)}
.thread-log{flex:1;min-height:0;overflow-y:auto;padding:8px 16px 2px;display:flex;flex-direction:column;gap:6px}
.thread-log > :first-child{margin-top:auto}
.msg{display:flex;gap:7px;align-items:flex-end;min-width:0}
.msg-out{justify-content:flex-end}
.msg-body{display:flex;flex-direction:column;gap:3px;min-width:0;max-width:min(78%,470px)}
.msg-bubble{padding:6px 9px;border:1px solid var(--ttsc-border-soft);border-radius:12px;border-bottom-left-radius:4px;background:var(--ttsc-surface-2);overflow-wrap:anywhere}
.msg-out .msg-bubble{background:color-mix(in srgb,var(--ttsc-accent) 13%,var(--ttsc-surface));border-color:var(--ttsc-accent-border);border-bottom-left-radius:12px;border-bottom-right-radius:4px}
.conv-scrim{display:none}
.thread-title:focus-visible,.icon-btn:focus-visible,.send:focus-visible{outline:2px solid var(--ttsc-accent);outline-offset:2px}

@media (max-width:1099px){
  .inbox-body{grid-template-columns:272px minmax(0,1fr)}
  .ctx{display:none}
}
@media (max-width:819px){
  .inbox-body{display:block;height:580px}
  .convs{position:absolute;inset:0 auto 0 0;z-index:5;width:min(304px,88%);visibility:hidden;transform:translateX(-102%);box-shadow:var(--ttsc-shadow-lg);transition:transform .2s,visibility 0s .2s}
  .inbox.is-list-open .convs{visibility:visible;transform:none;transition:transform .2s,visibility 0s 0s}
  .conv-scrim{position:absolute;inset:0;z-index:4;border:0;background:var(--ttsc-scrim);opacity:0;visibility:hidden;transition:opacity .2s,visibility 0s .2s}
  .inbox.is-list-open .conv-scrim{opacity:1;visibility:visible;transition:opacity .2s,visibility 0s 0s}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}
}
```

### JS

```js
const el = document.getElementById('chatInbox');
const chat = window.TTSCChatPanel.init(el, { replyDelay: 900, maxFileSize: 10 * 1024 * 1024 });

// Abre direto na conversa vinda da URL ou da fila.
if (el.dataset.conversationInicial) {
  chat.setConversation(el.dataset.conversationInicial, false);
}

// Capture o arquivo real antes do envio; o evento entrega apenas metadados.
let anexoPendente = null;
document.getElementById('fileInput').addEventListener('change', (event) => {
  const file = event.target.files[0] || null;
  anexoPendente = file && file.size <= 10 * 1024 * 1024 ? file : null;
});
document.getElementById('removeFile').addEventListener('click', () => {
  anexoPendente = null;
});

// Envia para o servidor e mantém o painel apenas como interface.
el.addEventListener('ttsc:chat:send', async (event) => {
  const { conversationId, text } = event.detail;
  const body = new FormData();
  body.append('conversation_uuid', conversationId);
  body.append('body', text);
  if (anexoPendente) body.append('attachment', anexoPendente);

  try {
    const response = await fetch('/api/atendimento/mensagens', { method: 'POST', body });
    if (!response.ok) throw new Error('falha no envio');
    anexoPendente = null;
  } catch (error) {
    const box = document.getElementById('composerError');
    box.textContent = 'Não foi possível enviar agora. Tente novamente.';
    box.hidden = false;
  }
});

// A resposta confirmada pelo servidor entra com o horário oficial.
// chat.appendMessage({ direction: 'out', text: mensagem.body, time: mensagem.hora });
```

O anexo do preview é só um metadado (`name`, `size`, `type`); o arquivo real não sai do navegador. Faça o upload em uma chamada própria e só então chame `appendMessage`.

### SQL

Estas tabelas **não existem** no dump atual. As tabelas reais de SAC são `sac_chat_sessions` e `sac_chat_messages`; a DDL abaixo é uma proposta normalizada para o inbox embutido. Para reaproveitar o SAC, mapeie `chat_conversations` → `sac_chat_sessions`, `chat_messages` → `sac_chat_messages` e `chat_participants` → `sac_customers` / `sac_agents`.

```sql
CREATE TABLE chat_conversations (
  uuid char(36) NOT NULL,
  tenant_uuid char(36) NOT NULL,
  subject varchar(180) NOT NULL,
  channel enum('whatsapp','chat','email') NOT NULL DEFAULT 'chat',
  status enum('open','pending','resolved') NOT NULL DEFAULT 'open',
  priority enum('low','normal','high') NOT NULL DEFAULT 'normal',
  contact_name varchar(150) NOT NULL,
  contact_email varchar(160) NULL,
  contact_phone varchar(40) NULL,
  assigned_user_uuid char(36) NULL,
  last_message_at datetime NULL,
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at datetime NULL,
  PRIMARY KEY (uuid),
  KEY idx_chat_conv_inbox (tenant_uuid, status, last_message_at),
  KEY idx_chat_conv_assignee (assigned_user_uuid, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE chat_participants (
  uuid char(36) NOT NULL,
  conversation_uuid char(36) NOT NULL,
  participant_type enum('contact','agent','ai') NOT NULL,
  participant_uuid char(36) NULL,
  display_name varchar(150) NOT NULL,
  role varchar(40) NOT NULL DEFAULT 'member',
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (uuid),
  UNIQUE KEY uq_chat_participant (conversation_uuid, participant_type, participant_uuid),
  KEY idx_chat_participant_user (participant_uuid),
  CONSTRAINT fk_chat_participant_conv FOREIGN KEY (conversation_uuid)
    REFERENCES chat_conversations (uuid) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE chat_messages (
  uuid char(36) NOT NULL,
  conversation_uuid char(36) NOT NULL,
  sender_uuid char(36) NULL,
  sender_type enum('contact','agent','ai','system') NOT NULL DEFAULT 'agent',
  body text NOT NULL,
  attachment_uuid char(36) NULL,
  attachment_name varchar(180) NULL,
  attachment_size int UNSIGNED NULL,
  attachment_mime varchar(120) NULL,
  read_at datetime NULL,
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at datetime NULL,
  PRIMARY KEY (uuid),
  KEY idx_chat_message_thread (conversation_uuid, created_at),
  KEY idx_chat_message_unread (conversation_uuid, sender_type, read_at),
  CONSTRAINT fk_chat_message_conv FOREIGN KEY (conversation_uuid)
    REFERENCES chat_conversations (uuid) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Consultas do painel (prepared statements):

```sql
-- Lista da caixa de entrada, com não lidas calculadas no banco.
SELECT c.uuid, c.subject, c.channel, c.status, c.contact_name, c.last_message_at,
       (SELECT COUNT(*) FROM chat_messages m
         WHERE m.conversation_uuid = c.uuid
           AND m.sender_type = 'contact'
           AND m.read_at IS NULL
           AND m.deleted_at IS NULL) AS unread
FROM chat_conversations c
WHERE c.tenant_uuid = :tenant_uuid
  AND c.deleted_at IS NULL
  AND c.status <> 'resolved'
ORDER BY c.last_message_at DESC
LIMIT 50;

-- Thread.
SELECT m.uuid, m.sender_type, m.body, m.attachment_name, m.attachment_size, m.attachment_mime, m.created_at
FROM chat_messages m
WHERE m.conversation_uuid = :conversation_uuid
  AND m.deleted_at IS NULL
ORDER BY m.created_at ASC
LIMIT 200;

-- Envio + atualização da conversa (na mesma transação).
INSERT INTO chat_messages
  (uuid, conversation_uuid, sender_uuid, sender_type, body, attachment_name, attachment_size, attachment_mime)
VALUES
  (:uuid, :conversation_uuid, :sender_uuid, 'agent', :body, :attachment_name, :attachment_size, :attachment_mime);

UPDATE chat_conversations
SET last_message_at = CURRENT_TIMESTAMP
WHERE uuid = :conversation_uuid AND tenant_uuid = :tenant_uuid;

-- Leitura da conversa.
UPDATE chat_messages
SET read_at = CURRENT_TIMESTAMP
WHERE conversation_uuid = :conversation_uuid
  AND sender_type = 'contact'
  AND read_at IS NULL;
```

Email e telefone são dados pessoais: carregue-os só quando o contexto for exibido e registre o acesso conforme a política de LGPD do tenant.
