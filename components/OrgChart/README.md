# OrgChart

Organograma hierárquico com conectores, recolher e expandir, busca e ficha rápida da pessoa selecionada.

## Quando usar

- Mostrar a estrutura de diretorias, gerências e coordenações de uma unidade ou da instituição.
- Explicar quem responde a quem antes de abrir uma vaga, redistribuir equipe ou aprovar uma despesa.
- Localizar uma pessoa pelo nome, cargo ou departamento em uma estrutura com várias camadas.

Não use quando:

- a lista de pessoas é longa e o objetivo é consultar cargos e contatos: prefira uma tabela de [DataTable](../DataTable/README.md);
- a pergunta é "quantas pessoas por área" e não "quem responde a quem": use [RankedBars](../RankedBars/README.md) ou [UnitGrid](../UnitGrid/README.md);
- o vínculo é temporário ou matricial, com a mesma pessoa em vários times: um [KanbanBoard](../KanbanBoard/README.md) por frente descreve melhor que uma árvore;
- a hierarquia tem mais de três níveis e centenas de nós: use uma árvore navegável ([JsTree](../JsTree/README.md)) com busca no servidor.

## Anatomia

```
(1) Estrutura organizacional                    Posições atualizadas em 26/10/2026
(2) [ Buscar por nome, cargo ou departamento... ] [Expandir tudo] [Recolher tudo]  14 de 14 visíveis
(3)        ┌──────────────┐
           │ Marina Duarte│──────┬──────────────┐
           │ CEO          │      │ (4) Rafael   │──┬── (5) Lucas Campos
           └──────────────┘      │  Tecnologia  │  └── Tatiane Faria
                                 └──────────────┘
(6) Ficha rápida: avatar · nome · cargo · status · e-mail · unidade · tempo de casa · gestor · equipe
```

| Parte | Classe / elemento | Obrigatório | Função |
|---|---|---|---|
| (1) Cabeçalho | `.card-h`, `.updated` | sim | Nome da estrutura e data da última atualização |
| (2) Barra | `.org-tools`, `#org-q` | sim | Busca, expandir, recolher e contador de visíveis |
| (3) Raiz | `.ceo-node`, `[data-node]` | sim | Pessoa no topo da hierarquia |
| (4) Gestor | `.node-dir` + `.chev` | sim | Diretoria, headcount e botão de recolher |
| (5) Liderado | `.node-rep` | sim | Nome, cargo, departamento e status |
| Conectores | `svg.org-lines` | sim no desktop | Liga gestor e liderados |
| (6) Ficha | `.ficha`, `.f-list` | sim | Dados rápidos da pessoa selecionada |
| Árvore móvel | `.org-tree` | sim | Versão indentada abaixo de 900 px |

Cada nó é composto por avatar de iniciais, nome, cargo, tag de departamento, headcount (quando é gestor) e status escrito. O botão de recolher é **irmão** do botão do nó, nunca aninhado, e aponta para a lista de liderados com `aria-controls`.

## Variantes

| Variante | Classe / opção | Uso |
|---|---|---|
| Horizontal | padrão ≥ 900 px | Raiz à esquerda, diretorias no meio e liderados à direita. É a leitura natural de um organograma de diretoria. |
| Vertical indentado | automático < 900 px | Árvore com recuo e linha-guia. Substitui os conectores por indentação para não criar rolagem horizontal. |
| Compacto | `.org--compact` no contêiner do gráfico | Esconde o cargo do liderado e reduz o espaçamento. Estruturas com muitos nós na mesma altura. |
| Ficha lateral | `.org-body` com 2 colunas ≥ 1100 px | Consulta rápida sem sair do organograma. |
| Ficha abaixo | automático < 1100 px | A estrutura ocupa a largura toda e a ficha desce. |
| Sem headcount | omitir `reports` | Nós folha não mostram a etiqueta de equipe. |

O layout horizontal é o padrão; a troca para a árvore vertical acontece por `max-width: 899px`, sem duplicar os dados.

## Estados

| Estado | Como aparece |
|---|---|
| Normal | Cartão em `ttsc-surface` com borda `ttsc-border`. |
| Selecionado | `.is-selected` com borda `ttsc-accent-border` e fundo `ttsc-accent-soft`; ficha atualizada. |
| Expandido | `.chev` com `aria-expanded="true"` e ícone de menos. |
| Recolhido | `.chev` com `aria-expanded="false"`, ícone de mais e liderados fora da árvore. |
| Correspondência | `.is-hit` com anel de 2 px em `ttsc-accent`. |
| Fora da busca | `.is-dim` com 40% de opacidade. |
| Sem resultado | `.org-empty` com texto em `ttsc-warning-text`. |
| Vazio | Sem pessoas, troque o gráfico por [EmptyState](../EmptyState/README.md) e mantenha a barra. |
| Carregando | [Skeleton](../Skeleton/README.md) com um cartão da raiz e quatro da diretoria. |
| Erro | Texto em `ttsc-danger-text` acima do gráfico, com "Tentar novamente". |

Status de presença são sempre texto: "Online", "Ausente" e "Offline". A cor acompanha, mas não substitui o rótulo.

## Acessibilidade

- O nó é um `<button>` real: recebe foco por `Tab`, abre a ficha com `Enter` e `Espaço` e expõe `aria-pressed` para a seleção.
- O botão de recolher é separado do nó, com `aria-expanded` e `aria-controls` apontando para o `ul`/`div` dos liderados. O rótulo diz o nome do gestor: "Recolher equipe de Rafael Lima".
- A busca tem `aria-label`, o contador usa `aria-live="polite"` e a ficha também, então mudanças de seleção e de visibilidade são anunciadas.
- A região `#org-live` anuncia "Equipe recolhida" e o total de pessoas visíveis após cada ação.
- No modo vertical, a indentação é reforçada por linhas-guia e pelo recuo; nada depende só de cor.
- Foco visível em nós, botões e busca; `prefers-reduced-motion` desliga transições. Nenhuma informação existe apenas no tooltip.

## Faça / Não faça

- Faça: mantenha o mesmo nível com cargos comparáveis; o organograma é uma leitura de autoridade.
- Faça: mostre headcount no gestor e o status em texto no nó.
- Faça: atualize a ficha no clique e no teclado, sem trocar de página.
- Não faça: aninhar um botão dentro de outro para "recolher" — use botões irmãos.
- Não faça: esconder pessoas recolhidas do contador; o total visível precisa bater com o que está na tela.
- Não faça: usar só cor para presença, nível ou área.
- Não faça: exibir CPF, salário ou data de nascimento na ficha rápida.

## API

Namespace global `window.TTSCOrgChart` (também exposto em `window.TTSC.OrgChart`).

### `TTSCOrgChart.render(el, data)`

Monta o organograma dentro de `el` — o card que contém `#org-chart`, `#org-ficha`, `#org-q` e os botões. Retorna a própria API.

| Campo | Tipo | Obrigatório | Efeito |
|---|---|---|---|
| `id` | `string` | sim | Identificador do nó |
| `name` | `string` | sim | Nome exibido |
| `role` | `string` | sim | Cargo ou diretoria |
| `dept` | `string` | sim | Departamento (tag e busca) |
| `manager` | `string \| null` | sim | `id` do gestor; `null` na raiz |
| `status` | `'online' \| 'away' \| 'offline'` | sim | Presença com rótulo em texto |
| `since` | `'AAAA-MM-DD'` | sim | Início na empresa, para "tempo de casa" |
| `unit` | `string` | sim | Unidade na ficha |
| `email` | `string` | sim | Contato na ficha |
| `reports` | `string[]` | sim | Ids dos liderados diretos |

### Métodos

| Método | Efeito |
|---|---|
| `expandAll()` | Expande todas as equipes e limpa a busca |
| `collapseAll()` | Recolhe as diretorias e mantém a raiz visível |
| `search(termo)` | Expande a árvore e destaca nome, cargo e departamento |
| `select(id)` | Abre a ficha da pessoa e emite o evento |
| `destroy()` | Limpa gráfico e ficha e remove os listeners do contêiner |
| `getState()` | Devolve `{ selected, collapsed }` |

### Eventos

| Evento | `detail` | Quando |
|---|---|---|
| `ttsc:orgchart:select` | `{ id, name, role, dept, status, manager }` | Clique, teclado ou `select()` |

### Classes e atributos

| Seletor | Efeito |
|---|---|
| `.org--compact` | Variante compacta dos liderados |
| `.is-selected` / `aria-pressed` | Nó selecionado |
| `.is-hit` / `.is-dim` | Resultado e resto da busca |
| `.chev[aria-expanded]` | Estado de expansão da equipe |
| `.org-tree` | Árvore vertical usada abaixo de 900 px |

## Modelos

### HTML

```php
<section class="card" aria-labelledby="org-title" data-ttsc-orgchart>
  <div class="card-h">
    <div>
      <h2 id="org-title" class="card-t">Estrutura organizacional</h2>
      <p class="card-s">
        <?= $this->e($org['root_label']) ?> ·
        <?= count($org['directorates']) ?> diretorias ·
        <?= $org['people_count'] ?> pessoas
      </p>
    </div>
    <span class="updated">Posições atualizadas em <?= $this->e($org['updated_label']) ?></span>
  </div>

  <div class="org-tools">
    <div class="search">
      <i class="fa-light fa-magnifying-glass" aria-hidden="true"></i>
      <input id="org-q" type="search"
             placeholder="Buscar por nome, cargo ou departamento..."
             aria-label="Buscar pessoa no organograma">
      <button class="q-clear" type="button" id="org-clear" aria-label="Limpar busca" hidden>
        <i class="fa-light fa-xmark" aria-hidden="true"></i>
      </button>
    </div>
    <div class="tool-btns">
      <button class="tbtn" type="button" id="org-expand">
        <i class="fa-light fa-angles-down" aria-hidden="true"></i> Expandir tudo
      </button>
      <button class="tbtn" type="button" id="org-collapse">
        <i class="fa-light fa-angles-up" aria-hidden="true"></i> Recolher tudo
      </button>
    </div>
    <span class="org-count" id="org-count" aria-live="polite"></span>
  </div>

  <p class="org-empty" id="org-empty" hidden>Nenhuma pessoa corresponde à busca. Tente outro nome, cargo ou departamento.</p>

  <div class="org-body">
    <div class="org-chart" id="org-chart"></div>
    <aside class="ficha" id="org-ficha" aria-live="polite" aria-label="Ficha rápida da pessoa selecionada"></aside>
  </div>

  <p class="sr-only" aria-live="polite" id="org-live"></p>
</section>

<script type="application/json" id="org-data">
  <?= json_encode($org['people'], JSON_UNESCAPED_UNICODE) ?>
</script>
```

### CSS

```css
.org-body { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 20px; align-items: start; }
.org-chart { position: relative; min-width: 0; }
.org-h { display: grid; grid-template-columns: 190px minmax(0, 1fr); gap: 26px; align-items: center; }
.branch { display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: 26px; align-items: center; }
.reports { display: grid; gap: 4px; }
.org-lines { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
.org-lines path { fill: none; stroke: var(--ttsc-border-strong); stroke-width: 1.5; stroke-linecap: round; }

.node-card { position: relative; z-index: 1; display: flex; background: var(--ttsc-surface);
             border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control); }
.node-card.is-selected { border-color: var(--ttsc-accent-border); background: var(--ttsc-accent-soft); }
.node { display: flex; align-items: center; gap: 8px; flex: 1; min-width: 0; padding: 8px 10px;
        border: 0; background: transparent; color: inherit; font: inherit; text-align: left; cursor: pointer; }
.chev { position: absolute; right: 5px; top: 50%; transform: translateY(-50%); width: 22px; height: 22px;
        display: grid; place-items: center; border: 1px solid var(--ttsc-border);
        border-radius: var(--ttsc-radius-xs); background: var(--ttsc-surface); cursor: pointer; }
.dept { border-radius: var(--ttsc-radius-pill); padding: 0 5px; font-size: 8.5px; font-weight: 700;
        text-transform: uppercase; color: var(--ttsc-info-text);
        background: color-mix(in srgb, var(--ttsc-info) 12%, transparent); }

.org-tree { display: none; list-style: none; margin: 0; padding: 0; }
.org-tree ul { list-style: none; margin: 0; padding: 8px 0 0 20px; position: relative; }
.org-tree ul::before { content: ""; position: absolute; left: 7px; top: 0; bottom: 16px;
                       border-left: 1.5px solid var(--ttsc-border-strong); }
.org-tree ul > li { padding-top: 8px; position: relative; }
.org-tree ul > li::before { content: ""; position: absolute; left: -13px; top: 30px;
                            width: 13px; border-top: 1.5px solid var(--ttsc-border-strong); }

@media (max-width: 1099px) {
  .org-body { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 899px) {
  .org-h { display: none; }
  .org-tree { display: block; }
  .org-chart .org-lines { display: none; }
}
```

### JS

```js
// assets/js/core/ttsc.orgchart.js — sem dependências
(function () {
  'use strict';

  var root = document.querySelector('[data-ttsc-orgchart]');
  if (!root) return;

  var raw = document.getElementById('org-data');
  var people = raw ? JSON.parse(raw.textContent) : [];

  // normaliza antes de renderizar: ids, status conhecidos e e-mails sem espaço
  var STATUS = { online: 1, away: 1, offline: 1 };
  people = people.filter(function (p) { return p && p.id && p.name; }).map(function (p) {
    return {
      id: String(p.id),
      name: String(p.name),
      role: String(p.role || ''),
      dept: String(p.dept || ''),
      manager: p.manager ? String(p.manager) : null,
      status: STATUS[p.status] ? p.status : 'offline',
      since: p.since || '',
      unit: String(p.unit || ''),
      email: String(p.email || '').trim(),
      reports: Array.isArray(p.reports) ? p.reports.map(String) : []
    };
  });

  var api = window.TTSCOrgChart.render(root, people);

  // Atalho: "/" foca a busca, como no restante do chassi.
  document.addEventListener('keydown', function (ev) {
    if (ev.key === '/' && !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) {
      ev.preventDefault();
      document.getElementById('org-q').focus();
    }
  });

  // Abre a ficha ao vir de um link #pessoa=<uuid>.
  var hash = /pessoa=([^&]+)/.exec(location.hash);
  if (hash) api.select(decodeURIComponent(hash[1]));

  window.addEventListener('resize', function () { api.render(root, people); });
})();
```

Chamar `render` novamente em `resize` é seguro: o componente remonta o layout e mantém a seleção. Em produção, prefira o `ResizeObserver` interno e só re-renderize ao cruzar 900 px.

### SQL

`rh_employees` já existe no dump do tenant com departamento, cargo, admissão, e-mail, status e `deleted_at`, mas **não** tem `manager_uuid` nem `unit_uuid`. A migration abaixo cria o vínculo de gestor e a unidade; `units` já existe.

```sql
-- database/migrations/20261026_002_orgchart_manager.sql (MariaDB 10.11 / MySQL 8)
ALTER TABLE rh_employees
  ADD COLUMN manager_uuid char(36) DEFAULT NULL AFTER job_title,
  ADD COLUMN unit_uuid char(36) DEFAULT NULL AFTER manager_uuid,
  ADD KEY idx_emp_manager (tenant_id, manager_uuid, deleted_at),
  ADD KEY idx_emp_unit (tenant_id, unit_uuid, deleted_at);

ALTER TABLE rh_employees
  ADD CONSTRAINT fk_emp_manager FOREIGN KEY (manager_uuid) REFERENCES rh_employees (uuid),
  ADD CONSTRAINT fk_emp_unit FOREIGN KEY (unit_uuid) REFERENCES units (uuid);

-- ninguém é gestor de si mesmo e a raiz não tem gestor
UPDATE rh_employees SET manager_uuid = NULL WHERE manager_uuid = uuid;
```

Árvore completa da raiz até o terceiro nível, com o nome do gestor e o headcount direto:

```sql
WITH RECURSIVE organograma (uuid, full_name, job_title, manager_uuid, nivel, caminho) AS (
  SELECT e.uuid, e.full_name, e.job_title, e.manager_uuid, 1,
         CAST(e.full_name AS CHAR(600))
  FROM rh_employees e
  WHERE e.tenant_id = :tenant_uuid
    AND e.manager_uuid IS NULL
    AND e.status = 'active'
    AND e.deleted_at IS NULL
  UNION ALL
  SELECT f.uuid, f.full_name, f.job_title, f.manager_uuid, o.nivel + 1,
         CONCAT(o.caminho, ' > ', f.full_name)
  FROM rh_employees f
  JOIN organograma o ON f.manager_uuid = o.uuid
  WHERE f.tenant_id = :tenant_uuid
    AND f.status = 'active'
    AND f.deleted_at IS NULL
    AND o.nivel < 8
)
SELECT o.nivel, o.full_name, o.job_title, d.name AS departamento,
       u.name AS unidade, gestor.full_name AS gestor,
       (SELECT COUNT(*) FROM rh_employees r
         WHERE r.manager_uuid = o.uuid AND r.deleted_at IS NULL) AS headcount_direto
FROM organograma o
LEFT JOIN rh_departments d ON d.uuid = (
       SELECT e.department_uuid FROM rh_employees e WHERE e.uuid = o.uuid)
LEFT JOIN units u ON u.uuid = (
       SELECT e.unit_uuid FROM rh_employees e WHERE e.uuid = o.uuid)
LEFT JOIN rh_employees gestor ON gestor.uuid = o.manager_uuid
ORDER BY o.nivel, o.full_name;
```

Busca por nome, cargo ou departamento, com `LIKE` parametrizado e sem colunas sensíveis:

```sql
SELECT e.uuid, e.full_name, e.job_title, e.email, e.hire_date,
       d.name AS departamento, u.name AS unidade, g.full_name AS gestor
FROM rh_employees e
LEFT JOIN rh_departments d ON d.uuid = e.department_uuid
LEFT JOIN units u ON u.uuid = e.unit_uuid
LEFT JOIN rh_employees g ON g.uuid = e.manager_uuid AND g.deleted_at IS NULL
WHERE e.tenant_id = :tenant_uuid
  AND e.deleted_at IS NULL
  AND e.status = 'active'
  AND (:termo = '' OR e.full_name LIKE CONCAT('%', :termo, '%')
       OR e.job_title LIKE CONCAT('%', :termo, '%')
       OR d.name LIKE CONCAT('%', :termo, '%'))
ORDER BY e.full_name
LIMIT 50;
```

A ficha rápida usa apenas `email`, `unit`, `hire_date` e o gestor; salário, CPF e dados bancários ficam fora da consulta da interface.
