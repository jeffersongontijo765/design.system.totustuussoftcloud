# Gantt

Cronograma de projeto com uma linha por tarefa, barras proporcionais ao período, progresso, marcos, dependências e caminho crítico.

## Quando usar

- Acompanhar um projeto com datas de início e fim por tarefa, progresso e responsável.
- Mostrar a ordem de execução e o impacto de uma tarefa atrasada em outra (dependências e caminho crítico).
- Dar uma visão de semanas ou meses do mesmo conjunto de tarefas, sem trocar de página.

Não use quando:

- as tarefas não têm datas — uma fila ou quadro sem calendário resolve melhor: [KanbanBoard](../KanbanBoard/README.md), [ChecklistGrid](../ChecklistGrid/README.md) ou [QueueList](../QueueList/README.md);
- o assunto é uma sequência de eventos pontuais, não um plano com duração: use [Timeline](../Timeline/README.md);
- o usuário precisa marcar compromissos por dia e hora: use [PageCalendar](../PageCalendar/README.md) ou [FullCalendar](../FullCalendar/README.md);
- o intervalo é muito longo (mais de um ano) ou tem centenas de tarefas: agrupe por fase e use [FunnelBars](../FunnelBars/README.md) ou uma tabela de [DataTable](../DataTable/README.md).

## Anatomia

```
(1) Roadmap · Plataforma 2026.3                        [Semana|Mês] [Hoje · 26/10]
(2) Concluído  Em andamento  Em risco  Planejado  Marco  -- Caminho crítico
(3) TAREFA / RESPONSÁVEL   Out 2026   Nov 2026   Dez 2026
(4) API de matrículas   ████████░░░░ 72%          (5)  Hoje
    Bruno Tavares  [crítica]      └──── (6) dependência ────┐
(7) Detalhe da tarefa   Tarefa · Período · Responsável · Progresso · Status · Dependências
```

| Parte | Classe / elemento | Obrigatório | Função |
|---|---|---|---|
| (1) Cabeçalho | `.card-h`, `#g-today` | sim | Nome do projeto, escala e linha de hoje |
| (2) Legenda | `.legend` | sim | Traduz cada cor de status em texto |
| (3) Coluna fixa | `.tl-task` | sim | Nome da tarefa, responsável e marca de caminho crítico |
| (4) Barra | `.bar`, `.bar-fill`, `--c` | sim | Período, progresso proporcional e status |
| (5) Linha de hoje | `.today`, `.today-chip` | recomendado | Data de referência do cronograma |
| (6) Dependência | `svg.deps` + `.dep` / `.dep-crit` | não | Liga a tarefa predecessora à sucessora |
| (7) Detalhe | `.detail`, `.d-grid` | sim | Ficha da tarefa selecionada |
| Coluna móvel | `.gantt-list`, `.m-item` | sim | Troca a timeline por lista vertical abaixo de 820 px |

A barra é um trilho claro do status com o preenchimento sólido do progresso. O percentual fica sempre em texto ao lado da barra, nunca apenas na cor. O losango marca a tarefa de data única (`status: 'milestone'`).

## Variantes

| Variante | Classe / opção | Uso |
|---|---|---|
| Mensal | `options.scale: 'month'` (padrão) | Três faixas de mês com o total de dias. Visão de diretoria. |
| Semanal | `options.scale: 'week'` | Faixas `S40`…`S53` com o intervalo de dias. Visão de execução. |
| Compacto | `.gantt--compact` | Linhas de 28 px sem a linha do responsável. Muitas tarefas na mesma tela. |
| Com dependências | `deps: ['uuid']` em cada tarefa | Liga predecessoras às sucessoras com setas. |
| Caminho crítico | `critical: true` | Marca a tarefa com a etiqueta "crítica" e desenha a cadeia em vermelho. |
| Marco | `status: 'milestone'` | Losango com a data no lugar da barra. |

A escala não move as barras: as datas mandam. Trocar de semana para mês muda a régua, os rótulos e as linhas de grade.

## Estados

| Estado | Como aparece |
|---|---|
| Concluído | Barra cheia em `ttsc-success` e rótulo "Concluído". |
| Em andamento | Preenchimento parcial em `ttsc-info`; o restante fica no trilho claro. |
| Em risco | Preenchimento em `ttsc-danger` com hachura no trilho e rótulo "Em risco". |
| Planejado | Trilho neutro, 0% e rótulo "Planejado". |
| Marco | Losango âmbar, data e rótulo "Marco"; sem barra de progresso. |
| Selecionado | `.is-selected` na linha, `aria-selected="true"` e a ficha atualizada. |
| Foco | Anel de 2 px em `ttsc-accent` dentro da linha. |
| Vazio | Sem tarefas, mostre [EmptyState](../EmptyState/README.md) no lugar da grade e mantenha o cabeçalho. |
| Carregando | Use [Skeleton](../Skeleton/README.md) com nove linhas de 36 px e a régua já desenhada. |
| Erro | Mensagem em `ttsc-danger-text` acima da grade, com a ação "Tentar novamente". |
| Desabilitado | `opacity: .5`, `pointer-events: none` e `aria-disabled="true"` no contêiner. |

Atraso não é um status: calcule comparando `due_date` com a data de hoje e mostre a etiqueta "Atrasada" junto do status real.

## Acessibilidade

- A grade usa `role="grid"`, `aria-rowcount` e uma linha por tarefa com `role="row"`, `tabindex="0"` e `aria-selected`.
- Teclado: `Tab` entra na grade, `↑`/`↓` movem entre tarefas, `Home`/`End` vão à primeira e à última, `Enter`/`Espaço` selecionam. O detalhe é atualizado e anunciado em uma região `aria-live="polite"`.
- Cada barra tem `aria-label` com nome, período, responsável, progresso e status; o tooltip do mouse repete os mesmos dados, nunca informação exclusiva.
- O status aparece como texto na legenda, na barra e na ficha. Cor sozinha não comunica estado.
- No modo lista (< 820 px) os itens são `<button>` com `aria-pressed`, sem rolagem horizontal.
- Foco visível em todos os controles; `prefers-reduced-motion` desliga transições. A linha de hoje tem 2 px de `ttsc-accent` além da cor.

## Faça / Não faça

- Faça: comece a barra na data real de início e termine no `due_date`; o progresso é do preenchimento, não do comprimento.
- Faça: mostre o responsável em todas as tarefas e a dependência em texto na ficha.
- Faça: destaque no máximo uma cadeia crítica; se tudo é crítico, nada é.
- Não faça: usar a cor da barra como único status nem esconder o percentual.
- Não faça: desenhar dependência de uma tarefa para ela mesma ou criar ciclos; valide no servidor.
- Não faça: cortar a coluna de tarefas no celular — troque para a lista vertical.

## API

Namespace global `window.TTSCGantt`.

### `TTSCGantt.render(el, data, options)`

Monta o cronograma dentro de `el` (o card que contém `#g-body`, `#g-list` e `#g-detail`). Retorna a própria API.

| Opção | Tipo | Padrão | Efeito |
|---|---|---|---|
| `scale` | `'month'` \| `'week'` | `'month'` | Régua inicial |
| `selected` | `string` | primeira tarefa | Tarefa aberta na ficha |
| `today` | `'AAAA-MM-DD'` | data do servidor | Posição da linha de hoje |

Cada tarefa:

```js
{
  id: 't3',                         // obrigatório, único
  name: 'API de matrículas',        // obrigatório
  owner: 'Bruno Tavares',           // obrigatório
  start: '2026-10-14',              // obrigatório (AAAA-MM-DD)
  end: '2026-11-05',                // obrigatório; igual a start em marcos
  progress: 72,                     // 0–100
  status: 'doing',                  // done | doing | risk | planned | milestone
  deps: ['t2'],                     // ids das predecessoras
  critical: true                    // opcional
}
```

### Métodos

| Método | Efeito |
|---|---|
| `setScale('month' \| 'week')` | Redesenha a régua e as linhas de grade, mantendo a seleção |
| `select(id)` | Seleciona a tarefa, atualiza a ficha e emite o evento |
| `destroy()` | Remove o conteúdo montado e os listeners do contêiner |
| `getState()` | Devolve `{ scale, selected }` |

### Eventos

| Evento | `detail` | Quando |
|---|---|---|
| `ttsc:gantt:select` | `{ id, name, start, end, progress, status }` | Clique, `Enter`/`Espaço` ou `select()` |

### Classes e atributos

| Seletor | Efeito |
|---|---|
| `.gantt--compact` | Linhas de 28 px, sem responsável |
| `.is-selected` / `aria-selected` | Destaque da linha |
| `.bar.is-done` `.is-doing` `.is-risk` `.is-planned` | Cor e padrão da barra |
| `--c` na barra | Cor do status (token) |
| `.dep` / `.dep-crit` | Conector comum / do caminho crítico |

## Modelos

### HTML

```php
<section class="card" aria-labelledby="roadmap-title"
         data-ttsc-gantt data-scale="month" data-selected="t3">
  <div class="card-h">
    <div>
      <h2 id="roadmap-title" class="card-t"><?= $this->e($project['name']) ?></h2>
      <p class="card-s">
        Projeto <?= $this->e($project['code']) ?> ·
        <?= $this->e($project['start_label']) ?> a <?= $this->e($project['due_label']) ?> ·
        <?= count($tasks) ?> tarefas
      </p>
    </div>
    <div class="tools">
      <div class="seg" role="group" aria-label="Escala do cronograma">
        <button type="button" class="seg-btn" data-scale="week" aria-pressed="false">Semana</button>
        <button type="button" class="seg-btn" data-scale="month" aria-pressed="true">Mês</button>
      </div>
      <button type="button" class="btn-today" id="gantt-today" aria-pressed="true">
        <i class="fa-light fa-calendar-day" aria-hidden="true"></i> Hoje · <?= $this->e($today_label) ?>
      </button>
    </div>
  </div>

  <ul class="legend" aria-label="Legenda de status">
    <li><span class="sw" style="--c:var(--g-done)" aria-hidden="true"></span>Concluído</li>
    <li><span class="sw" style="--c:var(--g-doing)" aria-hidden="true"></span>Em andamento</li>
    <li><span class="sw" style="--c:var(--g-risk)" aria-hidden="true"></span>Em risco</li>
    <li><span class="sw" style="--c:var(--g-planned)" aria-hidden="true"></span>Planejado</li>
    <li><span class="sw sw-mile" aria-hidden="true"></span>Marco</li>
    <li><span class="sw sw-crit" aria-hidden="true"></span>Caminho crítico</li>
  </ul>

  <div class="gantt-grid" id="gantt-grid" role="grid" aria-label="Cronograma de tarefas do projeto">
    <div class="tl-head" role="row">
      <div class="tl-head-l" role="columnheader">Tarefa / responsável</div>
      <div class="tl-head-r" role="columnheader" id="gantt-bands" aria-label="Período"></div>
    </div>
    <div class="tl-body" id="gantt-body"></div>
  </div>

  <ul class="gantt-list" id="gantt-list" aria-label="Tarefas do projeto"></ul>

  <section class="detail" aria-labelledby="gantt-detail-title">
    <h3 id="gantt-detail-title" class="detail-t">
      <i class="fa-light fa-circle-info" aria-hidden="true"></i> Detalhe da tarefa
    </h3>
    <div id="gantt-detail"></div>
  </section>

  <p class="sr-only" aria-live="polite" id="gantt-live"></p>
</section>

<div class="tip" id="gantt-tip" role="tooltip" hidden></div>

<script type="application/json" id="gantt-data">
  <?= json_encode($tasks_json, JSON_UNESCAPED_UNICODE) ?>
</script>
```

### CSS

```css
.gantt-grid { min-width: 0; }
.tl-head { display: grid; grid-template-columns: 240px minmax(0, 1fr); border-bottom: 1px solid var(--ttsc-border); }
.tl-body { position: relative; display: grid; grid-auto-rows: 36px; }
.tl-row { display: grid; grid-template-columns: 240px minmax(0, 1fr); border-bottom: 1px solid var(--ttsc-border-soft); cursor: pointer; }
.tl-row:hover { background: var(--ttsc-canvas-2); }
.tl-row.is-selected { background: var(--ttsc-accent-soft); }
.tl-track { position: relative; min-width: 0; }
.bar { position: absolute; top: 50%; transform: translateY(-50%); height: 20px; border-radius: 6px;
       background: color-mix(in srgb, var(--c) 15%, var(--ttsc-surface));
       border: 1px solid color-mix(in srgb, var(--c) 34%, transparent); }
.bar-fill { position: absolute; inset: 0 auto 0 0; border-radius: 5px; background: var(--c); }
.today { position: absolute; top: 0; bottom: -1px; width: 2px; background: var(--ttsc-accent); }
.deps { position: absolute; inset: 0; pointer-events: none; }
.dep { fill: none; stroke: var(--ttsc-border-prominent); stroke-width: 1.4; stroke-dasharray: 3 3; }
.dep-crit { fill: none; stroke: var(--ttsc-danger); stroke-width: 1.6; }

@media (max-width: 820px) {
  .gantt-grid { display: none; }
  .gantt-list { display: grid; gap: 8px; list-style: none; margin: 0; padding: 0; }
  .m-item { display: grid; gap: 6px; width: 100%; text-align: left; font: inherit; color: inherit;
            background: var(--ttsc-surface); border: 1px solid var(--ttsc-border-soft);
            border-radius: var(--ttsc-radius-control); padding: 9px 11px; }
  .m-item[aria-pressed="true"] { border-color: var(--ttsc-accent-border); background: var(--ttsc-accent-soft); }
}
```

### JS

```js
// assets/js/core/ttsc.gantt.js — sem dependências
(function () {
  'use strict';

  function boot(el) {
    var raw = document.getElementById('gantt-data');
    var tasks = raw ? JSON.parse(raw.textContent) : [];
    var done = { done: 1, doing: 1, risk: 1, planned: 1, milestone: 1 };

    tasks = tasks.filter(function (t) {
      // descarta linha inválida em vez de quebrar a régua
      return t && t.id && t.start && t.end && !isNaN(Date.parse(t.start)) && !isNaN(Date.parse(t.end));
    }).map(function (t) {
      return {
        id: String(t.id),
        name: String(t.name || 'Tarefa'),
        owner: String(t.owner || 'Sem responsável'),
        start: t.start,
        end: t.end < t.start ? t.start : t.end,
        progress: Math.min(100, Math.max(0, Number(t.progress) || 0)),
        status: done[t.status] ? t.status : 'planned',
        deps: Array.isArray(t.deps) ? t.deps : [],
        critical: !!t.critical
      };
    });

    var api = window.TTSCGantt.render(el, tasks, {
      scale: el.dataset.scale || 'month',
      selected: el.dataset.selected
    });

    // Persistência opcional: a seleção vira hash para sobreviver ao refresh.
    el.addEventListener('ttsc:gantt:select', function (ev) {
      history.replaceState(null, '', '#tarefa=' + encodeURIComponent(ev.detail.id));
    });

    return api;
  }

  document.querySelectorAll('[data-ttsc-gantt]').forEach(boot);
})();
```

### SQL

As tabelas `projects` e `project_tasks` existem no dump do tenant, mas **não** têm `start_date`, `progress`, `status` nem `depends_on_uuid`. A migration abaixo cria essas colunas; o `due_date` e o `completed_at` já existem.

```sql
-- database/migrations/20261026_001_gantt_task_dates.sql (MariaDB 10.11 / MySQL 8)
ALTER TABLE project_tasks
  ADD COLUMN start_date date DEFAULT NULL AFTER milestone_id,
  ADD COLUMN progress tinyint unsigned NOT NULL DEFAULT 0 AFTER priority,
  ADD COLUMN status varchar(24) NOT NULL DEFAULT 'planned' AFTER progress,
  ADD COLUMN depends_on_uuid char(36) DEFAULT NULL AFTER status,
  ADD CONSTRAINT chk_project_tasks_progress CHECK (progress BETWEEN 0 AND 100),
  ADD KEY idx_tasks_window (tenant_id, project_id, start_date, due_date, deleted_at),
  ADD KEY idx_tasks_depends (depends_on_uuid);

-- a predecessora é opcional, mas nunca pode ser a própria tarefa
UPDATE project_tasks SET depends_on_uuid = NULL WHERE depends_on_uuid = uuid;
```

O banco guarda **uma** predecessora por tarefa (`depends_on_uuid`), enquanto o componente aceita uma lista em `deps`. O preview usa lista porque "Testes integrados" depende de três frentes; para isso em produção, crie a tabela de ligação `project_task_dependencies (task_uuid, depends_on_uuid)` e devolva o `deps` já agrupado na consulta.

Cronograma do projeto, com a predecessora resolvida em nome:

```sql
SELECT t.uuid, t.title, t.start_date, t.due_date, t.progress, t.status,
       t.priority, t.completed_at,
       u.full_name AS assignee_name,
       p.title AS depends_on_title
FROM project_tasks t
LEFT JOIN rh_employees u ON u.uuid = t.assignee_id AND u.deleted_at IS NULL
LEFT JOIN project_tasks p ON p.uuid = t.depends_on_uuid AND p.deleted_at IS NULL
WHERE t.tenant_id = :tenant_uuid
  AND t.project_id = :project_uuid
  AND t.deleted_at IS NULL
ORDER BY t.start_date IS NULL, t.start_date, t.id;
```

Cadeia completa de dependências a partir das tarefas sem predecessora, com profundidade limitada para não girar em ciclo:

```sql
WITH RECURSIVE cadeia (uuid, title, depends_on_uuid, nivel, caminho) AS (
  SELECT t.uuid, t.title, t.depends_on_uuid, 1, CAST(t.uuid AS CHAR(400))
  FROM project_tasks t
  WHERE t.tenant_id = :tenant_uuid
    AND t.project_id = :project_uuid
    AND t.depends_on_uuid IS NULL
    AND t.deleted_at IS NULL
  UNION ALL
  SELECT f.uuid, f.title, f.depends_on_uuid, c.nivel + 1,
         CONCAT(c.caminho, '>', f.uuid)
  FROM project_tasks f
  JOIN cadeia c ON f.depends_on_uuid = c.uuid
  WHERE f.tenant_id = :tenant_uuid
    AND f.deleted_at IS NULL
    AND c.nivel < 20
)
SELECT uuid, title, nivel, caminho
FROM cadeia
ORDER BY nivel, title;
```

O caminho crítico do protótipo é uma sequência marcada à mão (`critical`). Em produção, a cadeia sai da CTE acima: as tarefas com `nivel` maior e sem folga entre `due_date` e o início da sucessora formam o caminho; recalcule após cada replanejamento e grave o resultado em cache por projeto.
