# Skeleton

Placeholder animado (`.ttsc-skeleton`, animação `pulse`) que reserva o formato de cards, tabelas e listas enquanto os dados chegam por AJAX.

## Quando usar

- Conteúdo carregado depois do HTML inicial (fetch/AJAX) que leva mais de ~300 ms: KPIs do dashboard, lista de alunos de uma turma, tabela de mensalidades em um drawer.
- Quando o formato final é conhecido: o skeleton imita linhas, avatares e números para a página não “pular” (CLS).
- Progresso de uma tarefa (upload, importação) usa [Progress](../Progress/README.md).
- Ação de um botão usa o estado “carregando” do [Button](../Button/README.md).
- Resultado vazio depois de carregar usa [EmptyState](../EmptyState/README.md) — nunca deixe o skeleton para sempre.
- Conteúdo renderizado no servidor (Plates) não precisa de skeleton.

## Anatomia

```
.card[aria-busy=true]
  ├ .ttsc-skeleton (linha 10px, largura 40–80%)      ← título/rótulo
  ├ .ttsc-skeleton (bloco 28px)                       ← número do KPI
  └ ○ .ttsc-skeleton (círculo 32px) + 2 linhas        ← item de lista com avatar
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Bloco | `div.ttsc-skeleton` com largura/altura definidas | sim |
| Container | `aria-busy="true"` enquanto carrega | sim |
| Grupo de placeholders | `aria-hidden="true"` | sim |
| Formas (extensão TTSC) | `ttsc-skeleton-line` · `-title` · `-circle` · `-block` | não |

## Variantes

| Variante | Como | Uso | Tokens |
|---|---|---|---|
| Linha | `ttsc-skeleton ttsc-skeleton-line` (10px, raio `radius - 2px`) | textos | fundo `ttsc-border-strong` (ponte TTSC; runtime usa `--accent`) |
| Título | `ttsc-skeleton-title` (14px) | cabeçalho de card | idem |
| Círculo | `ttsc-skeleton-circle` (32px, `radius-pill`) | avatar com iniciais | idem |
| Bloco | `ttsc-skeleton-block` (altura livre) | número de KPI, gráfico | idem |
| Tabela | grade `2fr 1fr 1fr` de linhas | DataTable/Table | idem |

## Estados

| Estado | Como aplicar |
|---|---|
| Carregando | placeholders visíveis, container `aria-busy="true"`, texto `aria-live` “Carregando…” |
| Carregado | remova os placeholders (ou classe `is-loaded` no container), `aria-busy="false"` |
| Erro | troque por mensagem + botão “Tentar novamente”; não volte ao skeleton automaticamente em loop |
| Movimento reduzido | `prefers-reduced-motion: reduce` desliga o `pulse` |

## API

Somente CSS (`.ttsc-skeleton { animation: var(--animate-pulse) }`, 2 s, opacidade 1 → .5). Não há módulo JS no ttscui; o helper abaixo é implementação TTSC (`assets/js/core/ttsc.skeleton.js`):

| Função | Efeito |
|---|---|
| `TTSCSkeleton.lines(n, widths)` | HTML de `n` linhas com larguras variadas |
| `TTSCSkeleton.load(container, url, render)` | mostra skeleton, faz `fetch`, chama `render(json)` e troca o conteúdo; trata erro |

## Acessibilidade

- O container que está carregando recebe `aria-busy="true"`; os placeholders `aria-hidden="true"` (leitor de tela não deve ler “caixas vazias”).
- Anuncie o fim em uma região `aria-live="polite"` (“Lista de alunos carregada”).
- Placeholders são decorativos (sem requisito de contraste), mas `ttsc-border-strong` garante que fiquem visíveis nos dois temas; `--accent` padrão quase some no escuro.
- Respeite `prefers-reduced-motion`.

## Modelos

### HTML

```html
<!-- Card de KPI carregado por AJAX -->
<div class="ttsc-card" id="kpi-active-enrollments" aria-busy="true"
     data-kpi-url="<?= url('/app/academic/kpi/active-enrollments') ?>">
  <div class="ttsc-card-content flex flex-col gap-2">
    <div aria-hidden="true" class="flex flex-col gap-2" data-skeleton>
      <div class="ttsc-skeleton ttsc-skeleton-line" style="width: 50%"></div>
      <div class="ttsc-skeleton ttsc-skeleton-block" style="height: 28px; width: 45%"></div>
      <div class="ttsc-skeleton ttsc-skeleton-line" style="width: 80%"></div>
    </div>
    <div data-content hidden></div>
  </div>
</div>

<!-- Item de lista com avatar -->
<div class="flex items-center gap-3" aria-hidden="true">
  <div class="ttsc-skeleton ttsc-skeleton-circle"></div>
  <div class="flex flex-col gap-1 grow">
    <div class="ttsc-skeleton ttsc-skeleton-line" style="width: 70%"></div>
    <div class="ttsc-skeleton ttsc-skeleton-line" style="width: 40%"></div>
  </div>
</div>
```

### CSS

```css
/* Ponte: o runtime pinta com --accent (=canvas-2), fraco demais no escuro */
.ttsc-skeleton { background-color: var(--ttsc-border-strong); }

/* Formas TTSC */
.ttsc-skeleton-line   { height: 10px; }
.ttsc-skeleton-title  { height: 14px; width: 60%; }
.ttsc-skeleton-circle { width: 32px; height: 32px; border-radius: var(--ttsc-radius-pill); flex-shrink: 0; }
.ttsc-skeleton-block  { min-height: 28px; border-radius: var(--ttsc-radius-sm); }

@media (prefers-reduced-motion: reduce) { .ttsc-skeleton { animation: none; } }
```

### JS

```js
// assets/js/core/ttsc.skeleton.js — implementação TTSC
(function (w) {
  function lines(n, widths) {
    widths = widths || [80, 60, 70, 45];
    var html = '';
    for (var i = 0; i < n; i++) {
      html += '<div class="ttsc-skeleton ttsc-skeleton-line" style="width:' + widths[i % widths.length] + '%"></div>';
    }
    return '<div aria-hidden="true" class="flex flex-col gap-2" data-skeleton>' + html + '</div>';
  }

  async function load(container, url, render) {
    var content = container.querySelector('[data-content]');
    var skeleton = container.querySelector('[data-skeleton]');
    container.setAttribute('aria-busy', 'true');
    try {
      var response = await fetch(url, { headers: { Accept: 'application/json' } });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      content.innerHTML = render(await response.json());
    } catch (error) {
      content.innerHTML = '<p class="text-xs">Não foi possível carregar. ' +
        '<button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-sm" data-retry>Tentar novamente</button></p>';
      content.querySelector('[data-retry]').addEventListener('click', function () {
        content.hidden = true; if (skeleton) skeleton.hidden = false; load(container, url, render);
      }, { once: true });
    } finally {
      if (skeleton) skeleton.hidden = true;
      content.hidden = false;
      container.setAttribute('aria-busy', 'false');
    }
  }

  w.TTSCSkeleton = { lines: lines, load: load };
})(window);

var kpi = document.getElementById('kpi-active-enrollments');
TTSCSkeleton.load(kpi, kpi.dataset.kpiUrl, function (data) {
  return '<span class="text-xs">Matrículas ativas</span>' +
         '<strong class="text-2xl">' + Number(data.active).toLocaleString('pt-BR') + '</strong>';
});
```

### SQL

O skeleton cobre o tempo desta consulta do endpoint do KPI (matrículas ativas da unidade e variação sobre o mês anterior):

```sql
SELECT SUM(e.status = 'active') AS active,
       SUM(e.status = 'active' AND e.enrollment_date < DATE_FORMAT(CURRENT_DATE, '%Y-%m-01')) AS active_prev_month
  FROM enrollments e
 WHERE e.unit_uuid = :unit_uuid
   AND e.deleted_at IS NULL;
```

O controller responde `json_encode(['active' => (int) $row['active'], 'prev' => (int) $row['active_prev_month']])`; o `render` do JS monta o número formatado em pt-BR.

## Faça / Não faça

- **Faça:** imite o formato final (mesma altura de linha, avatar redondo, número grande).
- **Faça:** trate erro e vazio — o skeleton sempre sai de cena.
- **Não faça:** skeleton para respostas instantâneas (< 300 ms): pisca e atrapalha.
- **Não faça:** spinner + skeleton juntos no mesmo bloco.
