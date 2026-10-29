# Symbol

Marca visual de uma entidade (`.ttsc-symbol`) — quadrado ou círculo com ícone ou iniciais, em cinco tamanhos e cores por token — e grupo empilhado com “+N”.

## Quando usar

- Identificar **coisas**: curso (sigla “ENF”), unidade, tipo de documento, módulo, categoria financeira — à esquerda de títulos em listas e cards.
- Iniciais de pessoas **quando não há foto** e não há status de presença (ex.: professores de uma turma num card compacto).
- Grupo empilhado de responsáveis/participantes com contador “+3”.
- **Symbol × Avatar:** use [Avatar](../Avatar/README.md) (`.ttsc-avatar`) para a **pessoa** com foto, fallback e indicador de status online/ausente (`ttsc-avatar-status-*`). Use Symbol para entidades e marcas, ou para iniciais genéricas sem foto/status. Avatar é sempre círculo de pessoa; Symbol é marca (quadrado por padrão).
- **Não use** como botão — se for clicável, envolva num `<a>`/`<button>` com rótulo.

## Anatomia

```
┌─────┐   ( JL )   [MA][CS][PN][+3]
│ ENF │   círculo   .ttsc-symbol-group
└─────┘
.ttsc-symbol (+ ícone <i> ou 1–3 letras) + .ttsc-symbol-badge opcional
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Container | `span.ttsc-symbol` | sim |
| Conteúdo | `<i class="fa-light …">` **ou** iniciais (1–3 caracteres) | sim |
| Forma | (quadrado `ttsc-radius-sm`) · `ttsc-symbol-circle` | não |
| Tamanho | `ttsc-symbol-xs` 20 · `-sm` 28 · (40) · `-lg` 52 · `-xl` 68 px | não |
| Cor | (neutro) · `ttsc-symbol-accent` · `-info` · `-warning` · `-danger` · `-solid` · `-mono` · `-outline` | não |
| Marcador | `span.ttsc-symbol-badge` (ponto de status da entidade) | não |
| Grupo | `div.ttsc-symbol-group[role="group"][aria-label]` | não |

## Variantes

| Cor | Classe | Tokens (fundo / conteúdo) |
|---|---|---|
| Neutro | `ttsc-symbol` | `ttsc-canvas-2` / `ttsc-text-2` |
| Accent | `ttsc-symbol-accent` | `ttsc-accent-soft` / `ttsc-accent-text` |
| Info | `ttsc-symbol-info` | `ttsc-info` 14% / `ttsc-info-text` |
| Warning | `ttsc-symbol-warning` | `ttsc-warning` 16% / `ttsc-warning-text` |
| Danger | `ttsc-symbol-danger` | `ttsc-danger` 12% / `ttsc-danger-text` |
| Solid | `ttsc-symbol-solid` | `ttsc-accent` / `ttsc-accent-on` (marca da instituição) |
| Mono | `ttsc-symbol-mono` | `ttsc-text` / `ttsc-surface` (contador +N) |
| Outline | `ttsc-symbol-outline` | `ttsc-surface` + borda `ttsc-border-strong` (ação “adicionar”) |

Tamanho de fonte/ícone é proporcional (`--ttsc-symbol-size × .38/.45`).

## API

Somente CSS (implementação TTSC). Variáveis no elemento:

| Variável | Padrão | Efeito |
|---|---|---|
| `--ttsc-symbol-size` | `40px` | lado do símbolo |
| `--ttsc-symbol-bg` | `ttsc-canvas-2` | fundo |
| `--ttsc-symbol-fg` | `ttsc-text-2` | cor do texto/ícone |

No grupo, o fundo é composto sobre `ttsc-surface` (fica opaco ao sobrepor) e cada item recebe anel de 2px `ttsc-surface`.

## Acessibilidade

- Símbolo ao lado de um nome em texto é decorativo: `aria-hidden="true"`.
- Símbolo sozinho (grupo, célula estreita) precisa de nome acessível: `title` + `aria-label` no grupo listando as pessoas (“Professores: Marina Alves, Carlos Souza… e mais 3”).
- Iniciais em `ttsc-*-text` sobre fundo suave: ≥ 4,5:1 nos dois temas; não use `ttsc-accent` como cor de letra.
- O `+N` deve abrir a lista completa (popover/drawer) quando for interativo.

## Modelos

### HTML

```html
<!-- Curso em lista -->
<div class="flex items-center gap-3">
  <span class="ttsc-symbol ttsc-symbol-accent" aria-hidden="true"><?= $this->e(strtoupper(substr($course['code'], 0, 3))) ?></span>
  <div>
    <div class="font-semibold"><?= $this->e($course['name']) ?></div>
    <div class="text-xs text-muted-foreground"><?= (int) $course['classes_count'] ?> turmas</div>
  </div>
</div>

<!-- Professores da turma (grupo empilhado, máx. 4 + contador) -->
<?php $shown = array_slice($teachers, 0, 4); $rest = count($teachers) - count($shown); ?>
<div class="ttsc-symbol-group" role="group"
     aria-label="Professores: <?= $this->e(implode(', ', array_column($shown, 'name'))) ?><?= $rest > 0 ? ' e mais ' . $rest : '' ?>">
  <?php foreach ($shown as $i => $t): ?>
    <span class="ttsc-symbol ttsc-symbol-sm ttsc-symbol-circle ttsc-symbol-<?= ['accent', 'info', 'warning', 'danger'][$i % 4] ?>"
          title="<?= $this->e($t['name']) ?>"><?= $this->e($t['initials']) ?></span>
  <?php endforeach ?>
  <?php if ($rest > 0): ?>
    <span class="ttsc-symbol ttsc-symbol-sm ttsc-symbol-circle ttsc-symbol-mono">+<?= (int) $rest ?></span>
  <?php endif ?>
</div>
```

### CSS

```css
.ttsc-symbol { --ttsc-symbol-size: 40px; --ttsc-symbol-bg: var(--ttsc-canvas-2); --ttsc-symbol-fg: var(--ttsc-text-2);
  position: relative; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0;
  width: var(--ttsc-symbol-size); height: var(--ttsc-symbol-size); border-radius: var(--ttsc-radius-sm);
  background: var(--ttsc-symbol-bg); color: var(--ttsc-symbol-fg); font-weight: 600; line-height: 1;
  font-size: calc(var(--ttsc-symbol-size) * .38); text-transform: uppercase; user-select: none; }
.ttsc-symbol > i { font-size: calc(var(--ttsc-symbol-size) * .45); }
.ttsc-symbol-circle { border-radius: var(--ttsc-radius-pill); }
.ttsc-symbol-xs { --ttsc-symbol-size: 20px; border-radius: var(--ttsc-radius-xs); }
.ttsc-symbol-sm { --ttsc-symbol-size: 28px; border-radius: var(--ttsc-radius-xs); }
.ttsc-symbol-lg { --ttsc-symbol-size: 52px; border-radius: var(--ttsc-radius-control); }
.ttsc-symbol-xl { --ttsc-symbol-size: 68px; border-radius: var(--ttsc-radius-surface); }
.ttsc-symbol-circle[class*="ttsc-symbol-"] { border-radius: var(--ttsc-radius-pill); }
.ttsc-symbol-accent  { --ttsc-symbol-bg: var(--ttsc-accent-soft); --ttsc-symbol-fg: var(--ttsc-accent-text); }
.ttsc-symbol-info    { --ttsc-symbol-bg: color-mix(in oklab, var(--ttsc-info) 14%, transparent);    --ttsc-symbol-fg: var(--ttsc-info-text); }
.ttsc-symbol-warning { --ttsc-symbol-bg: color-mix(in oklab, var(--ttsc-warning) 16%, transparent); --ttsc-symbol-fg: var(--ttsc-warning-text); }
.ttsc-symbol-danger  { --ttsc-symbol-bg: color-mix(in oklab, var(--ttsc-danger) 12%, transparent);  --ttsc-symbol-fg: var(--ttsc-danger-text); }
.ttsc-symbol-solid   { --ttsc-symbol-bg: var(--ttsc-accent); --ttsc-symbol-fg: var(--ttsc-accent-on); }
.ttsc-symbol-mono    { --ttsc-symbol-bg: var(--ttsc-text);   --ttsc-symbol-fg: var(--ttsc-surface); }
.ttsc-symbol-outline { --ttsc-symbol-bg: var(--ttsc-surface); box-shadow: inset 0 0 0 1px var(--ttsc-border-strong); }
.ttsc-symbol-badge { position: absolute; right: -2px; bottom: -2px; width: 10px; height: 10px; border-radius: var(--ttsc-radius-pill);
  background: var(--ttsc-success); box-shadow: 0 0 0 2px var(--ttsc-surface); }
.ttsc-symbol-group { display: inline-flex; align-items: center; }
.ttsc-symbol-group > .ttsc-symbol { box-shadow: 0 0 0 2px var(--ttsc-surface); font-size: 11px;
  background: linear-gradient(var(--ttsc-symbol-bg), var(--ttsc-symbol-bg)), var(--ttsc-surface); }
.ttsc-symbol-group > .ttsc-symbol + .ttsc-symbol { margin-left: calc(var(--ttsc-symbol-size) * -.15); }
.ttsc-symbol-group > .ttsc-symbol:hover { z-index: 1; }
```

### JS

```js
// Iniciais consistentes no cliente (mesma regra do helper PHP): primeira + última palavra, ignorando "da/de/do/dos/das/e"
const PARTICLES = new Set(['da', 'de', 'do', 'das', 'dos', 'e']);
export function initials(name) {
  const parts = name.trim().split(/\s+/).filter((p) => !PARTICLES.has(p.toLowerCase()));
  if (parts.length === 0) return '?';
  const first = parts[0][0];
  const last = parts.length > 1 ? parts[parts.length - 1][0] : (parts[0][1] || '');
  return (first + last).toUpperCase();
}

export function symbolFor(name, variant = 'accent', size = 'sm') {
  const el = document.createElement('span');
  el.className = `ttsc-symbol ttsc-symbol-${size} ttsc-symbol-circle ttsc-symbol-${variant}`;
  el.title = name;
  el.textContent = initials(name);
  return el;
}
```

### SQL

```sql
-- Professores de uma turma (grupo empilhado)
SELECT u.uuid, u.name, u.avatar, COUNT(*) AS subjects
  FROM class_subjects cs
  JOIN users u ON u.uuid = cs.teacher_uuid AND u.deleted_at IS NULL
 WHERE cs.class_uuid = :class_uuid
 GROUP BY u.uuid, u.name, u.avatar
 ORDER BY u.name;

-- Cursos da unidade (símbolo com a sigla)
SELECT co.uuid, co.code, co.name, co.type, COUNT(cl.id) AS classes_count
  FROM courses co
  LEFT JOIN classes cl ON cl.course_uuid = co.uuid AND cl.deleted_at IS NULL
 WHERE co.deleted_at IS NULL AND co.unit_uuid = :unit_uuid
 GROUP BY co.uuid, co.code, co.name, co.type
 ORDER BY co.name;
```

O controller calcula `initials` em PHP (mesma regra do JS) e entrega `$teachers`; quem tem `avatar` preenchido é renderizado com [Avatar](../Avatar/README.md), os demais com Symbol.

## Faça / Não faça

- **Faça:** quadrado para entidades, círculo para pessoas sem foto.
- **Faça:** no máximo 4 itens + “+N” no grupo.
- **Não faça:** iniciais com mais de 3 letras ou ícone e letras juntos.
- **Não faça:** usar Symbol quando há foto ou status de presença — isso é Avatar.
