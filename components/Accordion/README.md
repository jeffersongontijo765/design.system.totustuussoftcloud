# Accordion

Lista de seções recolhíveis do ttscui (`data-ttsc-accordion`) em que cada item abre e fecha o próprio painel, com uma ou várias seções abertas ao mesmo tempo (`expandAll`).

> Também listado em: **Base › Accordion**.

## Quando usar

- FAQ de curso, regulamentos, “Como funciona” do portal do aluno: perguntas curtas com respostas que o usuário lê uma de cada vez.
- Agrupar blocos longos de um formulário de configuração que raramente são editados juntos (ex.: “Regras de frequência”, “Regras de nota”).
- Para **um único** bloco que mostra/esconde (ex.: “Filtros avançados”) use [Collapse](../Collapse/README.md) — não precisa de lista.
- Para alternar entre vistas paralelas do mesmo registro (Dados, Matrículas, Financeiro) use abas, não accordion: o usuário precisa ver qual está ativa.
- Não esconda em accordion informação obrigatória para concluir uma tarefa (campos obrigatórios, avisos de bloqueio).

## Anatomia

```
┌ .ttsc-accordion [data-ttsc-accordion] ───────────────────────┐
│ ┌ .ttsc-accordion-item [data-ttsc-accordion-item] .active ─┐ │
│ │ [toggle] Título da pergunta ........................ [–] │ │
│ │ ┌ .ttsc-accordion-content #id ─────────────────────────┐ │ │
│ │ │ .ttsc-accordion-wrapper  resposta                    │ │ │
│ └─────────────────────────────────────────────────────────┘ │
│ ┌ item fechado: [toggle] Título ...................... [+] ┐ │
└──────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Raiz | `.ttsc-accordion` + `data-ttsc-accordion="true"` | sim |
| Variante com bordas | `.ttsc-accordion-outline` na raiz | não |
| Item | `.ttsc-accordion-item` + `data-ttsc-accordion-item="true"` (+ `.active` se abre aberto) | sim |
| Gatilho | `button.ttsc-accordion-toggle` + `data-ttsc-accordion-toggle="true"` + `aria-controls="<id do conteúdo>"` | sim |
| Título | `.ttsc-accordion-title` | sim |
| Indicador | `.ttsc-accordion-indicator` com `.ttsc-accordion-indicator-on` (fechado) e `.ttsc-accordion-indicator-off` (aberto) | não |
| Conteúdo | `.ttsc-accordion-content#id` (+ `.hidden` se começa fechado) | sim |
| Miolo | `.ttsc-accordion-wrapper` (padding e tipografia) | sim |

O JS encontra o painel **pelo `aria-controls` do gatilho** (`#id`); sem ele o item não abre.

## Variantes

| Variante | Classe | Uso | Tokens |
|---|---|---|---|
| Padrão (linhas) | `.ttsc-accordion` | Dentro de um card, FAQ compacto | divisória `ttsc-border`; título `ttsc-text`; resposta `ttsc-text` |
| Outline | `.ttsc-accordion .ttsc-accordion-outline` | FAQ solto na página, cada item como bloco | borda `ttsc-border`, raio `--radius`; ícone `ttsc-text-muted` |
| Um aberto por vez | `data-ttsc-accordion-expand-all="false"` (padrão) | FAQ | — |
| Vários abertos | `data-ttsc-accordion-expand-all="true"` | Seções de configuração | — |

## Estados

| Estado | Como aplicar |
|---|---|
| Aberto ao carregar | `.active` no item + painel **sem** `.hidden` |
| Fechado | painel com `.hidden` (classe `hiddenClass`) |
| Animando | o JS põe `animating="true"` no item durante a transição de altura |
| Foco | contorno 2px `ttsc-accent` no `<button>` (regra global de `:focus-visible`) |

## API

Atributos (lidos por `_buildConfig`: `data-ttsc-accordion-<opção>` na raiz):

| Atributo | Padrão | Efeito |
|---|---|---|
| `data-ttsc-accordion="true"` | — | cria a instância em `TTSC.init()` / `ttscAccordion.init()` |
| `data-ttsc-accordion-expand-all` | `false` | `false` fecha os irmãos ao abrir um item |
| `data-ttsc-accordion-active-class` | `active` | classe do item aberto |
| `data-ttsc-accordion-hidden-class` | `hidden` | classe do painel fechado |
| `data-ttsc-accordion-item` / `-toggle` | — | marcam item e gatilho (o clique é delegado na raiz) |

Métodos (`const acc = ttscAccordion.getInstance(el)` ou `TTSC.Accordion.getOrCreateInstance(el, { expandAll: true })`):

| Método | Descrição |
|---|---|
| `show(item)` / `hide(item)` / `toggle(item)` | recebem o **elemento do item** (`[data-ttsc-accordion-item]`) |
| `getOption(nome)` / `getElement()` | leitura de configuração / raiz |
| `on(evento, fn)` / `off(evento, id)` | ouvintes da instância (`fn(payload)`) |
| `ttscAccordion.init()` / `createInstances()` | inicializa todos `[data-ttsc-accordion]` da página |

Eventos (CustomEvent disparado na raiz, `bubbles: true`; `detail.payload.cancel = true` cancela os “antes”):

| Evento | Quando | Cancelável |
|---|---|---|
| `toggle` | clique no gatilho, antes de decidir abrir/fechar | sim |
| `show` / `shown` | antes de abrir / ao fim da animação | `show` sim |
| `hide` / `hidden` | antes de fechar / ao fim da animação | `hide` sim |

## Acessibilidade

- Gatilho é sempre `<button type="button">` com `aria-controls` apontando para o painel; o painel tem `role="region"` + `aria-labelledby` no id do botão.
- O runtime grava `aria-expanded` no **item**, não no botão. Use a ponte de JS abaixo para espelhar `aria-expanded` no `<button>` (leitores de tela anunciam “expandido/recolhido”).
- Teclado: `Tab` percorre os gatilhos, `Enter`/`Espaço` abre e fecha (comportamento nativo do botão).
- Indicador é decorativo (`aria-hidden="true"`); o estado é comunicado pelo `aria-expanded`.
- Título em `ttsc-text` (≥16:1) e resposta em `ttsc-text`/`ttsc-text-2` (≥8:1) sobre `ttsc-surface`; ícone em `ttsc-text-muted` (≥4,5:1).

## Modelos

### HTML

```html
<!-- FAQ do curso (portal do aluno) — um aberto por vez -->
<div class="ttsc-accordion ttsc-accordion-outline" data-ttsc-accordion="true" id="faq-curso">
  <?php foreach ($faqs as $i => $faq): $open = $i === 0; ?>
  <div class="ttsc-accordion-item<?= $open ? ' active' : '' ?>" data-ttsc-accordion-item="true">
    <button type="button" class="ttsc-accordion-toggle" data-ttsc-accordion-toggle="true"
            id="faq-<?= $this->e($faq['uuid']) ?>-t" aria-controls="faq-<?= $this->e($faq['uuid']) ?>"
            aria-expanded="<?= $open ? 'true' : 'false' ?>">
      <span class="ttsc-accordion-title"><?= $this->e($faq['question']) ?></span>
      <span class="ttsc-accordion-indicator" aria-hidden="true">
        <i class="fa-light fa-plus ttsc-accordion-indicator-on"></i>
        <i class="fa-light fa-minus ttsc-accordion-indicator-off"></i>
      </span>
    </button>
    <div class="ttsc-accordion-content<?= $open ? '' : ' hidden' ?>" id="faq-<?= $this->e($faq['uuid']) ?>"
         role="region" aria-labelledby="faq-<?= $this->e($faq['uuid']) ?>-t">
      <div class="ttsc-accordion-wrapper"><?= nl2br($this->e($faq['answer'])) ?></div>
    </div>
  </div>
  <?php endforeach; ?>
</div>

<!-- Configurações da turma — várias seções abertas ao mesmo tempo -->
<div class="ttsc-accordion" data-ttsc-accordion="true" data-ttsc-accordion-expand-all="true">
  <div class="ttsc-accordion-item active" data-ttsc-accordion-item="true">
    <button type="button" class="ttsc-accordion-toggle" data-ttsc-accordion-toggle="true" aria-controls="cfg-frequencia" aria-expanded="true">
      <span class="ttsc-accordion-title">Regras de frequência</span>
      <span class="ttsc-accordion-indicator" aria-hidden="true"><i class="fa-light fa-chevron-down ttsc-accordion-indicator-on"></i><i class="fa-light fa-chevron-up ttsc-accordion-indicator-off"></i></span>
    </button>
    <div class="ttsc-accordion-content" id="cfg-frequencia" role="region">
      <div class="ttsc-accordion-wrapper">Mínimo de 75% de presença por disciplina; faltas justificadas não contam.</div>
    </div>
  </div>
</div>
```

### CSS

```css
/* Ponte TTSC (obrigatória): o runtime compilado ainda usa os seletores sem prefixo
   [data-accordion-item].active > [data-accordion-toggle] para trocar o indicador.
   Estas regras fazem o + / – funcionar com os atributos data-ttsc-* (e vencem o
   display:inline-block do Font Awesome em <i class="fa-light …">). */
[data-ttsc-accordion-item] .ttsc-accordion-indicator-off { display: none; }
[data-ttsc-accordion-item].active > [data-ttsc-accordion-toggle] .ttsc-accordion-indicator-on  { display: none; }
[data-ttsc-accordion-item].active > [data-ttsc-accordion-toggle] .ttsc-accordion-indicator-off { display: inline-block; }

/* Tipografia do chassi (corpo 13px): título 14px, resposta em texto secundário */
.ttsc-accordion-title   { font-size: 14px; color: var(--ttsc-text); }
.ttsc-accordion-wrapper { font-size: 13px; line-height: 1.6; color: var(--ttsc-text-2); }
.ttsc-accordion-outline .ttsc-accordion-item { background: var(--ttsc-surface); border-radius: var(--ttsc-radius-sm); }

/* Extensão: item aberto destacado no outline */
.ttsc-accordion-outline .ttsc-accordion-item.active { border-color: var(--ttsc-accent-border); }
.ttsc-accordion-outline .ttsc-accordion-item.active .ttsc-accordion-indicator { color: var(--ttsc-accent-text); }
```

### JS

```js
// assets/js/core/ttsc.accordion-a11y.js — espelha aria-expanded no <button> e registra leitura da FAQ
function syncAria(root) {
  root.querySelectorAll('[data-ttsc-accordion-item]').forEach((item) => {
    const toggle = item.querySelector('[data-ttsc-accordion-toggle]');
    if (toggle) toggle.setAttribute('aria-expanded', item.classList.contains('active') ? 'true' : 'false');
  });
}

document.querySelectorAll('[data-ttsc-accordion]').forEach((root) => {
  const accordion = TTSC.Accordion.getOrCreateInstance(root);
  syncAria(root);
  ['shown', 'hidden'].forEach((evt) => root.addEventListener(evt, () => syncAria(root)));

  // Impede fechar a seção "Regras de frequência" enquanto houver alteração não salva
  root.addEventListener('hide', (event) => {
    if (root.querySelector('form[data-dirty="true"]')) event.detail.payload.cancel = true;
  });

  // Abre um item vindo da URL: /portal/cursos/abc#faq-<uuid>
  if (location.hash) {
    const panel = root.querySelector(location.hash);
    const item = panel && panel.closest('[data-ttsc-accordion-item]');
    if (item) accordion.show(item);
  }
});
```

### SQL

O esquema não tem FAQ por curso (`sac_knowledge_articles` é base de conhecimento do SAC, sem vínculo com curso). DDL nova, nas convenções do tenant:

```sql
CREATE TABLE IF NOT EXISTS course_faqs (
  id          bigint unsigned NOT NULL AUTO_INCREMENT,
  uuid        char(36)     NOT NULL,
  course_uuid char(36)     DEFAULT NULL COMMENT 'NULL = FAQ geral da unidade',
  unit_uuid   char(36)     NOT NULL,
  question    varchar(300) NOT NULL,
  answer      text         NOT NULL,
  sort_order  smallint unsigned NOT NULL DEFAULT 0,
  status      varchar(64)  NOT NULL DEFAULT 'published',
  created_at  datetime DEFAULT CURRENT_TIMESTAMP,
  updated_at  datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at  datetime DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_course_faqs_uuid (uuid),
  KEY idx_course_faqs_course (course_uuid, status, sort_order),
  KEY idx_course_faqs_unit (unit_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Perguntas frequentes por curso';

-- Perguntas do curso + perguntas gerais da unidade (as do curso primeiro)
SELECT f.uuid, f.question, f.answer, c.name AS course_name
  FROM course_faqs f
  LEFT JOIN courses c ON c.uuid = f.course_uuid AND c.deleted_at IS NULL
 WHERE f.unit_uuid = :unit_uuid
   AND (f.course_uuid = :course_uuid OR f.course_uuid IS NULL)
   AND f.status = 'published'
   AND f.deleted_at IS NULL
 ORDER BY f.course_uuid IS NULL, f.sort_order, f.id;
```

O controller executa a consulta com PDO (`FETCH_ASSOC`) e passa `$faqs` para a view; o laço do modelo HTML gera um item por linha, usando o `uuid` como id do painel (permite link direto `#faq-<uuid>`).

## Faça / Não faça

- **Faça:** pergunta como título (frase curta, termina com “?”), resposta de 1–3 parágrafos.
- **Faça:** primeiro item aberto no FAQ; todos fechados em listas de configuração longas.
- **Faça:** sempre `aria-controls` + id único (o JS depende dele).
- **Não faça:** accordion dentro de accordion; tabela larga dentro do painel (use um card com [DataTable](../DataTable/README.md)).
- **Não faça:** usar `ttsc-accent` como cor do título ou do ícone (2:1); para verde use `ttsc-accent-text`.
