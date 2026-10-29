# InsightPanel

Painel de insights de IA com resumo executivo, recomendações priorizadas, confiança, fontes e decisão humana explícita.

## Quando usar

- Visão geral ou dashboard em que os dados precisam virar recomendações curtas e acionáveis, não só gráficos.
- Situações em que a IA sugere um próximo passo (cobrança, nova turma, revisão de campanha) e uma pessoa decide aplicar ou descartar.
- Blocos de 3 a 6 sinais priorizados, com confiança, número de fontes e evidências a um clique.
- Ao lado do atendimento, combine com [ChatPanel](../ChatPanel/README.md) para levar o insight ao contexto da conversa.
- Para uma métrica isolada, use [KpiView](../KpiView/README.md); para comparar cenários, [ScenarioCards](../ScenarioCards/README.md); para fila de aprovação, [ApprovalQueue](../ApprovalQueue/README.md).

Não use este componente como substituto de um relatório analítico. Para séries históricas, use [ApexCharts](../ApexCharts/README.md); para tabelas detalhadas, [DataTable](../DataTable/README.md). Também não use se o insight não tiver fonte, confiança e um caminho claro de decisão: o painel perde a função.

## Anatomia

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Insights da IA · IA · 12 sinais              Como a IA chegou aqui?        │
│ Resumo executivo em duas linhas        Receita projetada      +6,4%        │
│ [Todos 4] [Risco 1] [Oportunidade 1] [Anomalia 1] [Previsão 1]             │
│ ┌ Risco · 3 fontes ───────────┐  ┌ Oportunidade · 4 fontes ────┐           │
│ │ Título do insight           │  │ Título do insight           │           │
│ │ métrica    Confiança 87%    │  │ métrica    Confiança 94%    │           │
│ │ [Aplicar] [Detalhes]        │  │ [Aplicar] [Detalhes]        │           │
│ └─────────────────────────────┘  └─────────────────────────────┘           │
│ Gerado a partir de 12 sinais · LGPD         Ver histórico >                │
└────────────────────────────────────────────────────────────────────────────┘
```

| Parte | Classe / elemento | Obrigatório | Função |
|---|---|---|---|
| Contêiner | `section.panel` | sim | Superfície, borda e recorte do painel. |
| Cabeçalho | `.panel-h`, `.badge-ai`, `.panel-sub` | sim | Título, selo “IA · 12 sinais” e horário da análise. |
| Fontes | `details.why` > `summary` + `.why-pop` | recomendado | Explica de onde vieram os sinais, em linguagem simples. |
| Resumo executivo | `.exec`, `.exec-text`, `.exec-kpi` | sim | Leitura de 10 segundos e um número de destaque. |
| Filtros | `.filters` > `.chip[data-filter]` | sim | Recorte por tipo, com contagem e `aria-pressed`. |
| Grade | `.grid` > `article.insight` | sim | Quatro cards em 2×2 no desktop e uma coluna no mobile. |
| Tipo | `.ins-type` | sim | Risco, oportunidade, anomalia ou previsão, com ícone e cor. |
| Fontes do card | `.ins-src` | recomendado | Quantidade de fontes usadas naquele insight. |
| Descartar | `button.dismiss` | sim | Remove o insight da lista e mantém a decisão no histórico. |
| Título e descrição | `.ins-title`, `.ins-desc` | sim | O que aconteceu, em uma frase e um complemento. |
| Métrica | `.ins-metric` | sim | Valor objetivo que sustenta o insight. |
| Confiança | `.conf` + `.meter[role="progressbar"]` | sim | Percentual numérico e barra; não é probabilidade. |
| Ação sugerida | `.ins-suggest` | sim | O próximo passo recomendado pela IA. |
| Aplicar | `button.apply` | sim | Sinaliza a decisão humana; o host registra a ação. |
| Detalhes | `button.details` + `.more` | recomendado | Evidências e link para a ficha completa. |
| Vazio | `#insightEmpty` | sim | Explica o filtro sem resultado e oferece restaurar. |
| Rodapé | `.panel-foot`, `#historyBtn` | sim | Origem dos dados, LGPD e acesso ao histórico. |
| Anúncio | `#insightLive[aria-live="polite"]` | sim | Filtros, aplicação, descarte e restauração para leitor de tela. |

## Variantes

| Variante | Classe / opção | Uso |
|---|---|---|
| Risco | `data-type="risco"` | Ameaça com impacto financeiro ou operacional; tom de perigo. |
| Oportunidade | `data-type="oportunidade"` | Ganho possível; tom de acento. |
| Anomalia | `data-type="anomalia"` | Desvio fora do padrão; tom de atenção. |
| Previsão | `data-type="previsao"` | Tendência projetada; tom informativo. |
| Aplicado | `.insight.is-applied`, `.apply.is-done` | A decisão foi registrada; borda de acento e check no botão. |
| Descartado | `data-dismissed="true"` | Sai da lista após o fade e deixa de contar nos filtros. |
| Filtrado | `.chip[aria-pressed="true"]` | Mostra apenas um tipo; os contadores refletem o que sobrou. |
| Itens via API | `TTSCInsights.init(el, { items })` | Substitui os cards estáticos por dados do servidor. |
| Tema | `data-theme` + tokens `--ttsc-*` | Claro e escuro com as mesmas classes. |

## Estados

- **Novo:** card neutro, com tipo, confiança e ação sugerida. É o estado inicial de cada insight.
- **Aplicado:** o botão vira “Aplicado” com check, recebe `aria-disabled="true"` e o card ganha borda de acento. O texto e o ícone comunicam o estado; a cor não é o único sinal.
- **Descartado:** fade de 170 ms, depois `hidden`; os contadores são recalculados e o histórico recebe o anúncio. Com movimento reduzido, a saída é imediata.
- **Filtro ativo:** o chip usa `aria-pressed="true"`, os demais ficam `false` e o número ao lado mostra quantos itens ativos existem naquele tipo.
- **Vazio por filtro:** `#insightEmpty` aparece com “Ver todos” e “Restaurar insights”; o anúncio informa que não há itens ativos.
- **Vazio por descarte:** o mesmo estado vale quando todos os insights foram descartados; “Restaurar” volta ao estado inicial do preview.
- **Carregando:** o painel não busca dados sozinho. Enquanto o host carrega, use [Skeleton](../Skeleton/README.md) no lugar da grade.
- **Erro:** também é responsabilidade do host; mostre [Alert](../Alert/README.md) acima do painel e mantenha a última lista válida.
- **Desabilitado:** depois de aplicar, o botão continua focável para o leitor ouvir o novo rótulo; não é removido do teclado.
## Acessibilidade

- `#insightLive` é `aria-live="polite"` com `aria-atomic="true"`; anuncia “Mostrando 1 de 4 insights”, aplicação, descarte e restauração sem interromper a navegação.
- Os filtros são um grupo rotulado, com `aria-pressed` em cada chip. O número não substitui o nome do tipo.
- A confiança tem texto (`87%`) e `role="progressbar"` com `aria-valuemin`, `aria-valuemax` e `aria-valuenow`; a barra é um reforço visual.
- “Aplicar” e “Detalhes” têm `aria-label` contextual com a ação e o título. Depois de aplicar, o rótulo muda para “Aplicado: …” e o botão fica `aria-disabled`.
- “Detalhes” usa `aria-expanded` e `aria-controls`; o painel de evidências fecha com `Esc` e devolve o foco ao botão. Clique fora também fecha.
- O botão de descartar tem alvo de 24×24 px e nome com o título do insight; não depende do “x” visual.
- O seletor de fontes usa `<details>` nativo, com foco e teclado do navegador.
- `prefers-reduced-motion` remove o fade de descarte e as transições; o estado aplicado continua legível por texto, check e borda.
- Contraste e hierarquia: títulos em `h3`, cards em `article` com `aria-labelledby`, tipos com rótulo textual e nunca só a cor.

## Faça / Não faça

- Faça: resuma em duas linhas e deixe o número principal no resumo; o gestor precisa entender o sinal sem abrir o card.
- Faça: mostre confiança, quantidade de fontes e evidências. “IA diz” sem origem não é insight.
- Faça: registre quem aplicou ou descartou, com data e hora, e mantenha o histórico acessível.
- Faça: trate a confiança como pontuação do modelo, não como probabilidade; o texto “Confiança” já ajuda, não prometa acerto.
- Faça: deixe a decisão final com uma pessoa. A IA recomenda; o botão “Aplicar” é uma ação humana.
- Não faça: aplicar, cobrar ou abrir turma automaticamente a partir do insight.
- Não faça: esconder o insight descartado sem deixar rastro no histórico.
- Não faça: usar o painel para 10 cards; priorize de 3 a 6 e mande o resto para a ficha completa.
- Não faça: usar vermelho/verde como único código de tipo ou de estado.

## API

O preview se autoinicializa em `#insightPanel` ao carregar. Para montar com dados do servidor:

```js
const panel = window.TTSCInsights.init(document.getElementById('insightPanel'), {
  items: window.INSIGHTS_DATA
});
```

Sem `items`, o componente usa os cards já renderizados no HTML. Com `items`, a grade é substituída e os contadores são recalculados.

Cada item aceita:

| Campo | Tipo | Uso |
|---|---|---|
| `id` | string | Identificador estável; vira `data-id` e é devolvido nos eventos. |
| `type` | `risco` \| `oportunidade` \| `anomalia` \| `previsao` | Define ícone, rótulo e tom. |
| `title` | string | Título do card e nome acessível. |
| `description` | string | Complemento de uma ou duas linhas. |
| `metricLabel` | string | Rótulo da métrica (ex.: “Impacto estimado”). |
| `metric` | string | Valor já formatado (ex.: “R$ 42 mil”). |
| `confidence` | number | 0 a 100; vira a barra e o texto “Confiança”. |
| `sourceCount` | number | Quantidade de fontes do card. |
| `suggestedAction` | string | Ação recomendada, usada também no rótulo de “Aplicar”. |
| `evidence` | string[] | Linhas exibidas em “Detalhes”. |

| Método | Retorno | Efeito |
|---|---|---|
| `apply(id)` | instância | Marca o insight como aplicado, anuncia e emite `ttsc:insight:apply`. |
| `dismiss(id)` | instância | Descarta com fade, recalcula contadores e emite `ttsc:insight:dismiss`. |
| `filter(type)` | instância | Aplica `all`, `risco`, `oportunidade`, `anomalia` ou `previsao`. |
| `reset()` | instância | Restaura cards, remove o estado aplicado, recalcula contadores e volta ao filtro “Todos”. |
| `destroy()` | — | Remove listeners, timers e a instância do elemento. |

`id` é procurado em `data-id`; se não existir, o componente usa o `id` do título (`ins-title-1` etc.).

| Evento | `detail` | Quando |
|---|---|---|
| `ttsc:insight:apply` | `{ id, type, title, confidence }` | Ao clicar em “Aplicar” ou chamar `apply(id)`. |
| `ttsc:insight:dismiss` | `{ id, type, title }` | Ao descartar ou chamar `dismiss(id)`. |

Atributos do preview: `data-filter` nos chips, `data-id`, `data-type`, `data-confidence`, `data-title` e `data-dismissed` nos cards. O estado visual é otimista e local; a fonte da verdade é o servidor. Se a gravação falhar, recarregue a lista em vez de manter o card como aplicado.

O preview usa IDs fixos (`#insightGrid`, `#insightEmpty`, `#insightLive`) e monta **um painel por página**. Para mais de um, use IDs únicos e ajuste as consultas, ou renderize o segundo painel em outra rota.

## Modelos

### HTML

```html
<section class="panel" id="insightPanel" aria-labelledby="insightTitle">
  <header class="panel-h">
    <div class="panel-id">
      <span class="panel-mark" aria-hidden="true"><i class="fa-light fa-sparkles"></i></span>
      <div>
        <div class="title-row">
          <h2 class="panel-title" id="insightTitle">Insights da IA</h2>
          <span class="badge-ai"><i class="fa-light fa-sparkles" aria-hidden="true"></i>IA · <?= (int) $totalSinais ?> sinais</span>
        </div>
        <p class="panel-sub"><i class="fa-light fa-clock" aria-hidden="true"></i>Atualizado <?= $this->e($atualizadoEm) ?> · análise do tenant</p>
      </div>
    </div>

    <details class="why" id="whyDetails">
      <summary>
        <i class="fa-light fa-circle-question" aria-hidden="true"></i>
        <span>Como a IA chegou aqui?</span>
        <i class="fa-light fa-chevron-down chev" aria-hidden="true"></i>
      </summary>
      <div class="why-pop">
        <p class="why-h">Fontes dos últimos sinais</p>
        <ul>
          <?php foreach ($fontes as $fonte): ?>
            <li><?= $this->e($fonte) ?></li>
          <?php endforeach; ?>
        </ul>
        <p class="why-note">
          <i class="fa-light fa-shield-halved" aria-hidden="true"></i>
          Somente leitura. A IA não aplica nenhuma ação sem decisão humana.
        </p>
      </div>
    </details>
  </header>

  <div class="exec">
    <span class="exec-ic" aria-hidden="true"><i class="fa-light fa-sparkles"></i></span>
    <div>
      <p class="exec-label">Resumo executivo</p>
      <p class="exec-text"><?= $this->e($resumo['texto']) ?></p>
    </div>
    <div class="exec-kpi" aria-label="<?= $this->e($resumo['kpi_label']) ?>: <?= $this->e($resumo['kpi_valor']) ?>">
      <span><?= $this->e($resumo['kpi_label']) ?></span>
      <strong><i class="fa-light fa-arrow-trend-up" aria-hidden="true"></i><?= $this->e($resumo['kpi_valor']) ?></strong>
      <small><?= $this->e($resumo['kpi_nota']) ?></small>
    </div>
  </div>

  <div class="filters" role="group" aria-label="Filtrar insights por tipo">
    <button class="chip" type="button" data-filter="all" aria-pressed="true">Todos <span class="chip-n"><?= count($insights) ?></span></button>
    <?php foreach ($tipos as $tipo): ?>
      <button class="chip" type="button" data-filter="<?= $this->e($tipo['slug']) ?>" aria-pressed="false">
        <?= $this->e($tipo['nome']) ?> <span class="chip-n"><?= (int) $tipo['total'] ?></span>
      </button>
    <?php endforeach; ?>
  </div>

  <div class="grid" id="insightGrid">
    <?php foreach ($insights as $i): ?>
      <article class="insight" data-id="<?= $this->e($i['uuid']) ?>" data-type="<?= $this->e($i['tipo']) ?>"
               data-confidence="<?= (int) $i['confianca'] ?>" data-title="<?= $this->e($i['titulo']) ?>"
               aria-labelledby="ins-title-<?= $this->e($i['uuid']) ?>">
        <div class="ins-top">
          <span class="ins-type">
            <i class="fa-light <?= $this->e($i['icone']) ?>" aria-hidden="true"></i><?= $this->e($i['tipo_nome']) ?>
          </span>
          <div class="ins-tools">
            <span class="ins-src"><i class="fa-light fa-link" aria-hidden="true"></i><?= (int) $i['fontes'] ?> fontes</span>
            <button class="dismiss" type="button" aria-label="Descartar insight: <?= $this->e($i['titulo']) ?>">
              <i class="fa-light fa-xmark" aria-hidden="true"></i>
            </button>
          </div>
        </div>

        <h3 class="ins-title" id="ins-title-<?= $this->e($i['uuid']) ?>"><?= $this->e($i['titulo']) ?></h3>
        <p class="ins-desc"><?= $this->e($i['descricao']) ?></p>

        <div class="ins-data">
          <div class="ins-metric">
            <span><?= $this->e($i['metrica_label']) ?></span>
            <b><?= $this->e($i['metrica_valor']) ?></b>
          </div>
          <div class="conf">
            <div class="conf-h"><span>Confiança</span><b><?= (int) $i['confianca'] ?>%</b></div>
            <div class="meter" role="progressbar" aria-label="Confiança: <?= (int) $i['confianca'] ?>%"
                 aria-valuemin="0" aria-valuemax="100" aria-valuenow="<?= (int) $i['confianca'] ?>">
              <span style="width:<?= (int) $i['confianca'] ?>%"></span>
            </div>
          </div>
        </div>

        <div class="ins-foot">
          <p class="ins-suggest">
            <i class="fa-light fa-wand-magic-sparkles" aria-hidden="true"></i>
            <span>Ação sugerida</span><b><?= $this->e($i['acao']) ?></b>
          </p>
          <div class="ins-actions">
            <button class="apply" type="button" aria-label="Aplicar sugestão: <?= $this->e($i['acao']) ?>">Aplicar</button>
            <button class="details" type="button" aria-label="Ver detalhes e evidências: <?= $this->e($i['titulo']) ?>"
                    aria-expanded="false" aria-controls="more-<?= $this->e($i['uuid']) ?>">Detalhes</button>
          </div>
        </div>

        <div class="more" id="more-<?= $this->e($i['uuid']) ?>" hidden>
          <p class="more-h">Evidências usadas</p>
          <ul>
            <?php foreach ($i['evidencias'] as $evidencia): ?>
              <li><?= $this->e($evidencia) ?></li>
            <?php endforeach; ?>
          </ul>
        </div>
      </article>
    <?php endforeach; ?>
  </div>

  <div class="empty" id="insightEmpty" hidden>
    <span class="empty-ic" aria-hidden="true"><i class="fa-light fa-sparkles"></i></span>
    <p><strong>Nenhum insight com este filtro.</strong><br>Ajuste o filtro ou restaure os insights descartados.</p>
    <div class="empty-actions">
      <button type="button" data-empty="all">Ver todos</button>
      <button type="button" data-empty="reset">Restaurar insights</button>
    </div>
  </div>

  <footer class="panel-foot">
    <p><i class="fa-light fa-shield-halved" aria-hidden="true"></i>Gerado a partir de <?= (int) $totalSinais ?> sinais · dados do tenant · LGPD</p>
    <button class="foot-link" type="button" id="historyBtn">Ver histórico <i class="fa-light fa-chevron-right" aria-hidden="true"></i></button>
  </footer>
</section>
<p id="insightLive" class="sr-only" aria-live="polite" aria-atomic="true"></p>
```

### CSS

Recorte das classes principais; o CSS completo, com todos os estados e o responsivo, está em `preview.html`.

```css
.panel{background:var(--ttsc-surface);border:1px solid var(--ttsc-border);border-radius:var(--ttsc-radius-surface);box-shadow:var(--ttsc-shadow-sm);padding:17px 20px 0;overflow:hidden}
.exec{display:grid;grid-template-columns:29px minmax(0,1fr) auto;align-items:center;gap:11px;margin-top:12px;padding:11px 13px;border:1px solid var(--ttsc-accent-border);border-radius:var(--ttsc-radius-sm);background:linear-gradient(100deg,color-mix(in srgb,var(--ttsc-accent) 11%,var(--ttsc-surface)),color-mix(in srgb,var(--ttsc-accent) 3%,var(--ttsc-surface)) 58%,var(--ttsc-surface))}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:11px;margin-top:11px}
.insight{position:relative;display:flex;flex-direction:column;padding:12px 13px 10px;border:1px solid var(--ttsc-border);border-radius:var(--ttsc-radius-sm);background:var(--ttsc-surface);min-width:0;transition:border-color .15s,opacity .17s,transform .17s}
.insight.is-applied{border-color:var(--ttsc-accent-border);box-shadow:inset 0 0 0 1px var(--ttsc-accent-border)}
.insight.is-dismissing{opacity:0;transform:scale(.985)}
.ins-type{display:inline-flex;align-items:center;gap:4px;padding:1px 6px;border:1px solid var(--ins-border,var(--ttsc-border));border-radius:var(--ttsc-radius-pill);background:var(--ins-soft,var(--ttsc-canvas-2));color:var(--ins-text,var(--ttsc-text-2));font-size:9px;font-weight:700;text-transform:uppercase}
.dismiss{width:24px;height:24px;display:grid;place-items:center;border:0;border-radius:6px;background:transparent;color:var(--ttsc-text-muted)}
.apply,.details{height:26px;padding:0 9px;border-radius:var(--ttsc-radius-sm);font-size:10px;font-weight:700}
.apply{border:1px solid var(--ttsc-accent-border);background:var(--ttsc-accent);color:var(--ttsc-accent-on)}
.apply.is-done{border-color:var(--ttsc-accent-border);background:var(--ttsc-accent-soft);color:var(--ttsc-accent-text);cursor:default}
.details{border:1px solid var(--ttsc-border);background:var(--ttsc-surface);color:var(--ttsc-text-2)}
.more{position:absolute;left:10px;right:10px;bottom:44px;z-index:30;padding:9px 10px;border:1px solid var(--ttsc-border);border-radius:var(--ttsc-radius-sm);background:var(--ttsc-surface);box-shadow:var(--ttsc-shadow-lg)}
.meter{height:5px;border-radius:var(--ttsc-radius-pill);background:var(--ttsc-surface-2);overflow:hidden;border:1px solid var(--ttsc-border-soft)}
.meter span{display:block;height:100%;border-radius:var(--ttsc-radius-pill);background:var(--ins-tone,var(--ttsc-accent))}
[data-type="risco"]{--ins-tone:var(--ttsc-danger);--ins-text:var(--ttsc-danger-text);--ins-border:color-mix(in srgb,var(--ttsc-danger) 30%,transparent);--ins-soft:color-mix(in srgb,var(--ttsc-danger) 10%,var(--ttsc-surface))}
[data-type="oportunidade"]{--ins-tone:var(--ttsc-accent);--ins-text:var(--ttsc-accent-text);--ins-border:var(--ttsc-accent-border);--ins-soft:var(--ttsc-accent-soft)}
[data-type="anomalia"]{--ins-tone:var(--ttsc-warning);--ins-text:var(--ttsc-warning-text);--ins-border:color-mix(in srgb,var(--ttsc-warning) 38%,transparent);--ins-soft:color-mix(in srgb,var(--ttsc-warning) 13%,var(--ttsc-surface))}
[data-type="previsao"]{--ins-tone:var(--ttsc-info);--ins-text:var(--ttsc-info-text);--ins-border:color-mix(in srgb,var(--ttsc-info) 32%,transparent);--ins-soft:color-mix(in srgb,var(--ttsc-info) 10%,var(--ttsc-surface))}
.apply:focus-visible,.details:focus-visible,.dismiss:focus-visible,.chip:focus-visible{outline:2px solid var(--ttsc-accent);outline-offset:2px}

@media (max-width:900px){
  .exec{grid-template-columns:29px minmax(0,1fr)}
  .exec-kpi{grid-column:2;padding-left:0;border-left:0;text-align:left}
}
@media (max-width:720px){
  .grid{grid-template-columns:1fr}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}
}
```

### JS

```js
// Se o HTML já vem renderizado pelo servidor, chame init sem opções.
// Se os insights chegam em JSON, passe items; a grade é substituída.
const el = document.getElementById('insightPanel');
const panel = window.TTSCInsights.init(el, {
  items: window.INSIGHTS_DATA // opcional
});

async function registrarDecisao(acao, id, title) {
  try {
    const response = await fetch(`/api/insights/${encodeURIComponent(id)}/${acao}`, {
      method: 'POST',
      headers: { 'X-CSRF-Token': window.TTSC.csrf, 'Accept': 'application/json' }
    });
    if (!response.ok) throw new Error('falha ao registrar');
  } catch (error) {
    const live = document.getElementById('insightLive');
    live.textContent = `Não foi possível registrar a decisão de ${title}. Recarregue e tente novamente.`;
    // Em produção, recarregue a lista do servidor para desfazer o estado otimista.
  }
}

el.addEventListener('ttsc:insight:apply', (event) => {
  registrarDecisao('aplicar', event.detail.id, event.detail.title);
});

el.addEventListener('ttsc:insight:dismiss', (event) => {
  registrarDecisao('descartar', event.detail.id, event.detail.title);
});

// A instância também permite ações programáticas:
// panel.filter('risco'); panel.apply('uuid-do-insight'); panel.reset();
```

O componente não aplica nada por conta própria: ele só muda o estado visual, anuncia e emite o evento. A gravação, a permissão e a auditoria ficam com o host.

### SQL

A tabela `ai_insights` **não existe** no dump atual. A DDL abaixo é nova e foi pensada para o painel; os dados do preview são ilustrativos.

```sql
CREATE TABLE ai_insights (
  uuid char(36) NOT NULL,
  tenant_uuid char(36) NOT NULL,
  type enum('risco','oportunidade','anomalia','previsao') NOT NULL,
  title varchar(180) NOT NULL,
  description varchar(500) NOT NULL,
  metric_label varchar(80) NOT NULL,
  metric_value varchar(80) NOT NULL,
  confidence tinyint unsigned NOT NULL,
  source_count smallint unsigned NOT NULL DEFAULT 0,
  evidence json NULL,
  suggested_action varchar(180) NOT NULL,
  status enum('new','applied','dismissed') NOT NULL DEFAULT 'new',
  generated_at datetime NOT NULL,
  applied_at datetime NULL,
  applied_by_uuid char(36) NULL,
  dismissed_at datetime NULL,
  dismissed_by_uuid char(36) NULL,
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at datetime NULL,
  PRIMARY KEY (uuid),
  KEY idx_ai_insights_feed (tenant_uuid, status, generated_at),
  KEY idx_ai_insights_type (tenant_uuid, type, status),
  KEY idx_ai_insights_decision (applied_by_uuid, applied_at),
  CONSTRAINT chk_ai_insights_confidence CHECK (confidence BETWEEN 0 AND 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Feed do painel, priorizando risco e anomalia:

```sql
SELECT uuid, type, title, description, metric_label, metric_value,
       confidence, source_count, suggested_action, generated_at
FROM ai_insights
WHERE tenant_uuid = :tenant_uuid
  AND status = 'new'
  AND deleted_at IS NULL
ORDER BY FIELD(type, 'risco', 'anomalia', 'oportunidade', 'previsao'),
         confidence DESC, generated_at DESC
LIMIT 12;
```

Aplicação — só acontece com uma pessoa autenticada; a IA nunca executa esta chamada sozinha:

```sql
UPDATE ai_insights
SET status = 'applied',
    applied_at = CURRENT_TIMESTAMP,
    applied_by_uuid = :user_uuid
WHERE uuid = :insight_uuid
  AND tenant_uuid = :tenant_uuid
  AND status = 'new'
  AND deleted_at IS NULL;

-- Confirme rowCount = 1 antes de responder 200 ao painel.
```

Descarte e histórico:

```sql
UPDATE ai_insights
SET status = 'dismissed',
    dismissed_at = CURRENT_TIMESTAMP,
    dismissed_by_uuid = :user_uuid
WHERE uuid = :insight_uuid
  AND tenant_uuid = :tenant_uuid
  AND status = 'new'
  AND deleted_at IS NULL;

SELECT uuid, type, title, status, applied_at, applied_by_uuid, dismissed_at, dismissed_by_uuid
FROM ai_insights
WHERE tenant_uuid = :tenant_uuid
  AND status IN ('applied', 'dismissed')
  AND deleted_at IS NULL
ORDER BY COALESCE(applied_at, dismissed_at) DESC
LIMIT 50;
```

O `confidence` é uma pontuação do modelo, não uma probabilidade calibrada. Guarde a versão do modelo e a data da análise no pipeline de origem se precisar reproduzir a recomendação.
