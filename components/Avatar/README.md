# Avatar

Foto ou iniciais de uma pessoa (`.ttsc-avatar`), com ponto de presença online/ausente/ocupado/offline e versão empilhada para grupos.

## Quando usar

- Identificar aluno, professor ou atendente ao lado do nome: linhas de tabela, cabeçalho de drawer, cartões do Kanban, chat do SAC.
- Grupo empilhado para “quem está na turma / no atendimento” quando o nome individual não é essencial (máx. 4 visíveis + contador).
- Ponto de status somente onde a presença importa (chat, atendimento, lista de plantonistas). Em listagens de matrícula não mostre status.
- Para ícone de entidade que não é pessoa (curso, unidade, documento) use um tile de ícone do [Card](../Card/README.md), não avatar.
- Para status textual do registro (Ativa, Trancada) use [Badge](../Badge/README.md).

## Anatomia

```
 ┌───────┐
 │  AB   │  .ttsc-avatar  (40px)
 │       │    ├ .ttsc-avatar-image > img   ou   .ttsc-avatar-fallback (iniciais)
 └─────(●)    └ .ttsc-avatar-indicator > .ttsc-avatar-status.ttsc-avatar-status-online
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Container | `.ttsc-avatar` (40×40, `position: relative`) + tamanho `size-8` · `size-12` · `size-14` | sim |
| Imagem | `.ttsc-avatar-image > img[alt]` (círculo, `object-fit` pela proporção 1:1) | um dos dois |
| Iniciais | `.ttsc-avatar-fallback` (círculo, borda `ttsc-border`, fundo `canvas-2`) | um dos dois |
| Indicador | `.ttsc-avatar-indicator` (caixa 24px absoluta; posicione com a extensão CSS) | não |
| Status | `.ttsc-avatar-status` + `-online` · `-away` · `-busy` · `-offline` | não |
| Grupo | `.ttsc-avatar-group` (extensão TTSC) + contador `.ttsc-avatar-more` | não |

## Variantes

| Variante | Como | Uso | Tokens |
|---|---|---|---|
| Iniciais neutras | `.ttsc-avatar-fallback` | padrão | fundo `--accent` (= `ttsc-canvas-2`), texto `ttsc-text`, borda `ttsc-border` |
| Iniciais tonais | `.ttsc-avatar-fallback` + `.ttsc-avatar-tone-1…4` (extensão) | distinguir pessoas numa lista | `ttsc-accent-soft`/`ttsc-accent-text`, `ttsc-info-text`, `ttsc-warning-text` sobre `ttsc-surface-2` |
| Foto | `.ttsc-avatar-image > img` | quando `users.avatar` existe | — |
| Tamanhos | `size-8` (32px) · padrão (40px) · `size-12` (48px) · `size-14` (56px, cabeçalho de drawer) | — | — |

## Estados

| Status | Classe | Cor (runtime) | Significado no TotusTuus |
|---|---|---|---|
| Online | `ttsc-avatar-status-online` | `--color-green-600` | sessão com atividade nos últimos 5 min |
| Ausente | `ttsc-avatar-status-away` | `--color-blue-600` | sessão ativa, sem atividade há 5–30 min (`idle_timeout_minutes`) |
| Ocupado | `ttsc-avatar-status-busy` | `--color-yellow-600` | marcado pelo cliente (em aula ao vivo, em atendimento); não persiste |
| Offline | `ttsc-avatar-status-offline` | `--mono` a 50% | sem sessão válida |

O anel do ponto usa `border: 2px var(--background)` (= `ttsc-surface`), então ele “recorta” o avatar nos dois temas.

## API

Componente só de CSS — não há módulo JS no ttscui. A extensão `assets/js/core/ttsc.avatar.js` (abaixo) gera iniciais a partir do nome e troca a foto quebrada pelo fallback.

| Atributo (extensão) | Efeito |
|---|---|
| `data-ttsc-avatar-name="Ana Beatriz Souza"` | gera “AS” no fallback e o `aria-label` |
| `data-ttsc-avatar-presence="online\|away\|busy\|offline"` | cria/atualiza o ponto de status |

## Acessibilidade

- Foto: `alt` com o nome da pessoa; se o nome já está ao lado em texto, use `alt=""` (decorativa).
- Iniciais: o container recebe `role="img"` + `aria-label="Ana Beatriz Souza"`; as letras em si ficam `aria-hidden="true"`.
- Status nunca só por cor: inclua texto oculto no `aria-label` (“Ana Beatriz Souza, online”) ou um rótulo visível ao lado.
- Contraste: iniciais em `ttsc-text` sobre `ttsc-canvas-2` (≥14:1); tons usam `*-text` dos tokens (≥4,5:1 nos dois temas).
- Contador do grupo (“+5”) tem `aria-label="Mais 5 alunos"`.

## Modelos

### HTML

```html
<!-- Linha de tabela: iniciais + nome -->
<div class="flex items-center gap-2">
  <div class="ttsc-avatar size-8" role="img" aria-label="Ana Beatriz Souza">
    <div class="ttsc-avatar-fallback ttsc-avatar-tone-1" aria-hidden="true">AS</div>
  </div>
  <div class="flex flex-col">
    <span class="text-sm font-medium text-foreground">Ana Beatriz Souza</span>
    <span class="text-xs text-muted-foreground">MAT-2026-0381</span>
  </div>
</div>

<!-- Atendente do SAC com foto e presença (dados de users.avatar + user_sessions) -->
<?php $p = $user['presence']; ?>
<div class="ttsc-avatar" role="img" aria-label="<?= $this->e($user['name']) ?>, <?= $this->e(__('presence_' . $p)) ?>">
  <?php if (!empty($user['avatar'])): ?>
    <div class="ttsc-avatar-image"><img src="<?= $this->e($user['avatar']) ?>" alt=""></div>
  <?php else: ?>
    <div class="ttsc-avatar-fallback" aria-hidden="true"><?= $this->e($user['initials']) ?></div>
  <?php endif; ?>
  <div class="ttsc-avatar-indicator"><div class="ttsc-avatar-status ttsc-avatar-status-<?= $this->e($p) ?>"></div></div>
</div>

<!-- Grupo empilhado: professores da turma -->
<div class="ttsc-avatar-group">
  <div class="ttsc-avatar size-8" role="img" aria-label="Carlos Henrique Lima"><div class="ttsc-avatar-fallback" aria-hidden="true">CL</div></div>
  <div class="ttsc-avatar size-8" role="img" aria-label="Juliana Ferreira"><div class="ttsc-avatar-fallback ttsc-avatar-tone-2" aria-hidden="true">JF</div></div>
  <div class="ttsc-avatar size-8" role="img" aria-label="Mariana Costa"><div class="ttsc-avatar-fallback ttsc-avatar-tone-3" aria-hidden="true">MC</div></div>
  <span class="ttsc-avatar ttsc-avatar-more size-8" aria-label="Mais 5 professores"><span class="ttsc-avatar-fallback">+5</span></span>
</div>
```

### CSS

```css
/* Ponte (já em bundle.css): o fallback usa --accent (hover neutro = ttsc-canvas-2) e o anel do status --background */
:root { --accent: var(--ttsc-canvas-2); --background: var(--ttsc-surface); }

/* Extensão TTSC: posição do ponto, iniciais em 12px semibold */
.ttsc-avatar-indicator { inset-inline-end: -8px; bottom: -8px; }
.ttsc-avatar-status { width: 10px; height: 10px; }
.ttsc-avatar-fallback { font-size: 12px; font-weight: 600; color: var(--ttsc-text); text-transform: uppercase; }
.ttsc-avatar.size-12 .ttsc-avatar-fallback, .ttsc-avatar.size-14 .ttsc-avatar-fallback { font-size: 15px; }
.ttsc-avatar.size-12 .ttsc-avatar-status, .ttsc-avatar.size-14 .ttsc-avatar-status { width: 12px; height: 12px; }

/* Tons de iniciais (sempre cor de TEXTO dos tokens) */
.ttsc-avatar-tone-1 { background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text); border-color: var(--ttsc-accent-border); }
.ttsc-avatar-tone-2 { background: var(--ttsc-surface-2); color: var(--ttsc-info-text); }
.ttsc-avatar-tone-3 { background: var(--ttsc-surface-2); color: var(--ttsc-warning-text); }
.ttsc-avatar-tone-4 { background: var(--ttsc-surface-2); color: var(--ttsc-text-2); }

/* Grupo empilhado */
.ttsc-avatar-group { display: flex; align-items: center; }
.ttsc-avatar-group > .ttsc-avatar + .ttsc-avatar { margin-inline-start: -6px; }
.ttsc-avatar-group .ttsc-avatar-fallback { font-size: 11px; }
.ttsc-avatar-group .ttsc-avatar-fallback,
.ttsc-avatar-group .ttsc-avatar-image { box-shadow: 0 0 0 2px var(--ttsc-surface); }
.ttsc-avatar-more .ttsc-avatar-fallback { background: var(--ttsc-surface-2); color: var(--ttsc-text-2); font-size: 11px; }
```

### JS

```js
// assets/js/core/ttsc.avatar.js — iniciais, fallback de foto quebrada e presença
export function initials(name) {
  const parts = String(name || '').trim().split(/\s+/).filter(Boolean);
  if (!parts.length) return '?';
  const first = parts[0][0];
  const last = parts.length > 1 ? parts[parts.length - 1][0] : '';
  return (first + last).toUpperCase();
}

export function setPresence(avatar, presence) {
  let indicator = avatar.querySelector('.ttsc-avatar-indicator');
  if (!indicator) {
    indicator = document.createElement('div');
    indicator.className = 'ttsc-avatar-indicator';
    indicator.innerHTML = '<div class="ttsc-avatar-status"></div>';
    avatar.appendChild(indicator);
  }
  indicator.firstElementChild.className = `ttsc-avatar-status ttsc-avatar-status-${presence}`;
  const labels = { online: 'online', away: 'ausente', busy: 'ocupado', offline: 'offline' };
  avatar.setAttribute('aria-label', `${avatar.dataset.ttscAvatarName}, ${labels[presence] || presence}`);
}

export function initAvatars(root = document) {
  root.querySelectorAll('.ttsc-avatar[data-ttsc-avatar-name]').forEach((avatar) => {
    const name = avatar.dataset.ttscAvatarName;
    avatar.setAttribute('role', 'img');
    avatar.setAttribute('aria-label', name);
    const img = avatar.querySelector('.ttsc-avatar-image img');
    const fallback = () => {
      avatar.querySelector('.ttsc-avatar-image')?.remove();
      if (!avatar.querySelector('.ttsc-avatar-fallback')) {
        avatar.insertAdjacentHTML('afterbegin', `<div class="ttsc-avatar-fallback" aria-hidden="true">${initials(name)}</div>`);
      }
    };
    if (!img) fallback();
    else img.addEventListener('error', fallback, { once: true });
    if (avatar.dataset.ttscAvatarPresence) setPresence(avatar, avatar.dataset.ttscAvatarPresence);
  });
}

document.addEventListener('DOMContentLoaded', () => initAvatars());

// Chat do SAC: atualiza a presença a cada 60s
setInterval(async () => {
  const res = await fetch('/api/v1/sac/agents/presence', { headers: { Accept: 'application/json' } });
  if (!res.ok) return;
  const { data } = await res.json(); // [{ uuid, presence }]
  data.forEach(({ uuid, presence }) => {
    const el = document.querySelector(`.ttsc-avatar[data-user-uuid="${uuid}"]`);
    if (el) setPresence(el, presence);
  });
}, 60000);
```

### SQL

Nome e foto vêm de `users` (banco master; o tenant tem a mesma estrutura); a presença é derivada de `user_sessions.last_activity_at`:

```sql
-- Avatares + presença de um conjunto de usuários (MariaDB 10.11 / MySQL 8)
SELECT u.uuid, u.name, u.avatar,
       UPPER(CONCAT(LEFT(u.name, 1),
             IF(LOCATE(' ', u.name) > 0, LEFT(SUBSTRING_INDEX(u.name, ' ', -1), 1), ''))) AS initials,
       s.last_activity_at,
       CASE
         WHEN s.last_activity_at >= NOW() - INTERVAL 5 MINUTE  THEN 'online'
         WHEN s.last_activity_at >= NOW() - INTERVAL 30 MINUTE THEN 'away'
         ELSE 'offline'
       END AS presence
  FROM users u
  LEFT JOIN (
        SELECT user_id, MAX(last_activity_at) AS last_activity_at
          FROM user_sessions
         WHERE tenant_id = :tenant_id
           AND revoked_at IS NULL
           AND expires_at > NOW()
         GROUP BY user_id
       ) s ON s.user_id = u.uuid
 WHERE u.tenant_id = :tenant_id
   AND u.uuid IN (:uuid_1, :uuid_2, :uuid_3)
   AND u.deleted_at IS NULL
 ORDER BY u.name;
```

O PHP passa cada linha para a view (`$user['initials']`, `$user['avatar']`, `$user['presence']`); “ocupado” não é persistido — o front aplica `busy` quando o atendente está em aula ao vivo ou em chamada. Para o grupo da turma, troque o `IN (...)` por `JOIN class_subjects cs ON cs.teacher_uuid = u.uuid AND cs.class_uuid = :class_uuid`.

## Faça / Não faça

- **Faça:** iniciais de primeiro + último nome (“Ana Beatriz Souza” → “AS”).
- **Faça:** `size-8` em tabelas, padrão em listas, `size-14` no cabeçalho de drawer do aluno.
- **Faça:** ponto de status só onde presença muda decisão (chat, fila de atendimento).
- **Não faça:** foto de banco de imagens como placeholder; use iniciais.
- **Não faça:** mais de 4 avatares no grupo — use `+N`.
- **Não faça:** iniciais em `ttsc-accent` sobre branco (2:1); use o tom `ttsc-avatar-tone-1`.
