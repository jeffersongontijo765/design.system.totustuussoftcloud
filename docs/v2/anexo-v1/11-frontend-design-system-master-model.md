# SDD 11 — Modelo Master de Frontend & Design System (TotusTuus SoftCloud)

> **Documento derivado do SDD Mestre** · **Data:** 05/09/2026 (atualizado)  
> **Página de Referência / Gold Standard:** `https://localhost/totustuussoftcloud/developer/commercial`  
> **Arquivo Fonte Master:** `resources/views/app/pages/developer/commercial.php`
> **Controller:** `app/Http/Controllers/Admin/DeveloperController.php` (método `commercial`)  
> **Rota:** `/developer/commercial` registrada em `routes/web.php`, nav configurada em `app/Config/sidebar-nav.php` (chave `commercial`)

---

## 1. Visão Geral & Modelo de Referência

A página do **Commercial Workspace** (`/developer/commercial`) é estabelecida como o **Modelo Arquitetural Master (Gold Standard)** para todas as telas administrativas, operacionais, analíticas e de gestão do ecossistema TotusTuus SoftCloud.

Qualquer nova tela, refatoração de módulo ou componente deve seguir estritamente a arquitetura, padrões visuais, convenções de ícones e comportamentos assíncronos estabelecidos nesta página.

> [!IMPORTANT]
> **Antecedente:** Esta página substitui `/developer/settings/billing/modules` (`modules.php`) como referência canônica. O `code.html` original também não é mais a autoridade. O Commercial Workspace foi escolhido por representar o layout mais completo do ecossistema, com suporte nativo a i18n (10 idiomas, RTL apenas para árabe `ar`, `en-gb` como alias de inglês), formatação monetária via `Intl.NumberFormat`, sistema de temas dark/light com engine próprio, e a estrutura completa de 5 visões com drawers, kanban e analytics.

---

## 2. Padrões de Design System (Supabase Theme 3-Layer Dark)

### 2.1 Paleta de Cores em 3 Camadas (Dark Mode)
- **Layer 1 (Canvas Principal):** `#14171c`
- **Layer 2 (Containers & Outer Boxes):** `#1a1d24` com borda `#282c37`
- **Layer 3 (Cards, Tabelas & Modais):** `#242832` com borda `#323745`
- **Cor Primária de Destaque (Accent):** `#10b981` (Supabase Emerald)
- **Texto Principal:** `#f3f4f6` (Light: `#18181b`)
- **Texto Secundário / Muted:** `#9ca3af` (Light: `#71717a`)

### 2.2 Tipografia & Espaçamento
- **Fonte Geral:** Sans-serif moderna (Inter / Circular fallback)
- **Fonte Numérica / Telemetria:** Monospace (`Source Code Pro` / `var(--font-mono)`)
- **Wrapper Principal:** Padding `18px 24px`, espaçamento `gap: 8px` vertical entre seções.

---

## 3. Padrão de Iconografia Oficial (FontAwesome Pro 7.2 Light)

> [!IMPORTANT]
> Todos os ícones do sistema devem utilizar obrigatoriamente o prefixo **`fa-light`**, conforme a biblioteca FontAwesome Pro 7.2 instalada em `assets/`.

### Exemplos Canônicos:
- **Sincronização / Refresh:** `<i class="fa-light fa-arrows-rotate"></i>`
- **Histórico / Timestamp:** `<i class="fa-light fa-clock-rotate-left"></i>`
- **Filtros Avançados:** `<i class="fa-light fa-filter"></i>`
- **Exportação:** `<i class="fa-light fa-file-export"></i>`
- **Novo Registro / CTA:** `<i class="fa-light fa-plus"></i>`
- **Voltar / Navegação:** `<i class="fa-light fa-arrow-left"></i>`
- **Formatos de Arquivo:** `fa-light fa-file-csv`, `fa-light fa-file-excel`, `fa-light fa-file-pdf`, `fa-light fa-file-code`, `fa-light fa-code`, `fa-light fa-database`, `fa-light fa-file-lines`.

---

## 4. Sistema de Navegação em 5 Visões (Segmented Pill Tabs)

A página canônica `/developer/commercial` controla as 5 visões com botões `.tab-btn` (ids `tab-btn-<view>`, contadores em `.tab-badge`) e views correspondentes em `#view-<view>` (`view-kpi`, `view-table`, `view-cards`, `view-kanban`, `view-analytics`):

```html
<div class="inline-flex p-1 bg-slate-200/75 rounded-2xl border border-slate-200 text-xs font-medium text-slate-600 gap-1 overflow-x-auto">
    <button id="tab-btn-kpi" type="button" onclick="switchCommercialTab('kpi')" class="tab-btn is-active px-3.5 py-1.5 rounded-xl ...">
        <i class="fa-light fa-chart-simple text-xs"></i>
        <span>KPI</span>
        <span class="tab-badge px-1.5 py-0.5 bg-slate-300 text-slate-700 rounded-full text-[10px]">10</span>
    </button>
    <button id="tab-btn-table" type="button" onclick="switchCommercialTab('table')" class="tab-btn px-3.5 py-1.5 rounded-xl ...">
        <i class="fa-light fa-table-list text-emerald-600 text-xs"></i>
        <span>Data Table</span>
        <span class="tab-badge ..."><?= $totalDeals ?></span>
    </button>
    <button id="tab-btn-cards" type="button" onclick="switchCommercialTab('cards')" class="tab-btn ...">
        <i class="fa-light fa-border-all text-xs"></i>
        <span>Cards / Grid</span>
    </button>
    <button id="tab-btn-kanban" type="button" onclick="switchCommercialTab('kanban')" class="tab-btn ...">
        <i class="fa-light fa-bars-progress text-xs"></i>
        <span>Kanban Board</span>
    </button>
    <button id="tab-btn-analytics" type="button" onclick="switchCommercialTab('analytics')" class="tab-btn ...">
        <i class="fa-light fa-chart-line text-xs"></i>
        <span>Analytics</span>
    </button>
</div>
```

O alternador é definido na própria view e exportado no `window` (também como alias `window.switchChassisTab`, usado pelo shell):

```js
function switchCommercialTab(tabName) {
  const tabs = ['kpi', 'table', 'cards', 'kanban', 'analytics'];
  tabs.forEach(function (t) {
    document.getElementById('view-' + t).style.display = (t === tabName ? 'block' : 'none');
    document.getElementById('tab-btn-' + t).className = 'tab-btn ... ' +
      (t === tabName ? 'bg-white text-slate-900 shadow-sm font-semibold is-active' : 'text-slate-600 bg-transparent font-normal');
  });
  document.getElementById('main-viewport')?.scrollTo({ top: 0, behavior: 'smooth' });
}
window.switchCommercialTab = switchCommercialTab;
window.switchChassisTab = switchCommercialTab;
```

> [!NOTE]
> **Duas variantes coexistem no repositório.** O padrão `.ud-tab-segmented` + `.ud-tab-btn` + `data-view`/`data-target` (handler global por delegação de click em `assets/js/app.js`) é o chassis usado pelas demais páginas de módulo (`academic/*`, `accounting/*`, `databases/*`). A página canônica `/developer/commercial` **não** usa esse markup: ela usa `.tab-btn` + `switchCommercialTab()` acima. Ao copiar para uma nova tela, escolha **uma** das duas variantes e mantenha `#view-<nome>` ↔ `tab-btn-<nome>` em sincronia.

> [!IMPORTANT]
> O texto das abas nasce em **EN** no markup (base `en`); rótulos traduzidos entram apenas via `__('key', 'group', 'Fallback')` com entrada em `lang/{locale}/developer.php`.

---

## 5. Toolbar & Dropdown de Exportação Universal (7 Formatos)

O menu de exportação padronizado deve oferecer 7 formatos com cor uniforme de ícone em Esmeralda (`#10b981`) e badge de extensão:

```html
<div class="export-dd" id="toolbarExportDropdown">
    <button type="button" class="qa-customize-btn" id="btnToggleExportDD">
        <i class="fa-light fa-file-export text-emerald-500"></i>
        <span>Exportar</span>
        <i class="fa-light fa-chevron-down text-[9px] text-muted ml-0.5"></i>
    </button>
    <div class="dd-menu" id="toolbarExportDDMenu">
        <div class="item" data-export-format="csv"><i class="fa-light fa-file-csv text-emerald-500"></i> CSV<span class="ext">.csv</span></div>
        <div class="item" data-export-format="xlsx"><i class="fa-light fa-file-excel text-emerald-500"></i> XLSX<span class="ext">.xlsx</span></div>
        <div class="item" data-export-format="pdf"><i class="fa-light fa-file-pdf text-emerald-500"></i> PDF<span class="ext">.pdf</span></div>
        <div class="sep"></div>
        <div class="item" data-export-format="json"><i class="fa-light fa-file-code text-emerald-500"></i> JSON<span class="ext">.json</span></div>
        <div class="item" data-export-format="xml"><i class="fa-light fa-code text-emerald-500"></i> XML<span class="ext">.xml</span></div>
        <div class="item" data-export-format="sql"><i class="fa-light fa-database text-emerald-500"></i> SQL<span class="ext">.sql</span></div>
        <div class="item" data-export-format="txt"><i class="fa-light fa-file-lines text-emerald-500"></i> TXT<span class="ext">.txt</span></div>
    </div>
</div>
```

---

## 6. Prevenção de Duplicação de Ações & Sincronização AJAX

> [!NOTE]
> **Padrão de integração futura ao shell.** O snippet abaixo NÃO é código copiado do `commercial.php` (que é uma página standalone). É o padrão que deve ser aplicado quando as páginas forem migradas para o layout compartilhado via `main.php` e `$this->start()`/`$this->end()`.

Para evitar conflito entre o recarregamento total da página e o recarregamento assíncrono:

1. **No Cabeçalho (Breadcrumb):** Declarar a seção `actions` da view:
   ```php
   <?php $this->start('actions') ?>
   <div class="flex items-center gap-2">
       <span class="text-xs font-mono text-muted hidden sm:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg border border-border bg-surface">
           <i class="fa-light fa-clock-rotate-left text-[11px] text-emerald-500"></i>
           <span>Synced:</span>
           <strong id="ttscLastSync" class="text-fg"><?= date('H:i:s') ?></strong>
       </span>
       <a href="<?= url('/developer/dashboard') ?>" class="qa-customize-btn">
           <i class="fa-light fa-arrow-left text-xs"></i> <span>Portal</span>
       </a>
   </div>
   <?php $this->end() ?>
   ```

2. **Na Toolbar da Tabela:** Botão específico para requisição AJAX assíncrona:
   ```html
   <button type="button" class="qa-customize-btn" id="btnReloadTable" title="Sincronizar dados via AJAX">
       <i class="fa-light fa-arrows-rotate text-emerald-500" id="iconReloadTable"></i>
       <span>Sincronizar</span>
   </button>
   ```

---

## 7. Suporte Bimoeda & Matriz i18n (10 Idiomas)

- **Moedas Nativas:** Suporte dinâmico a USD ($) e BRL (R$) com conversão baseada em taxa de câmbio configurável e alternador no topo (`#btnCurrBrl` / `#btnCurrUsd`).
- **10 Idiomas:** Geração automática e persistência de matriz de tradução: `en`, `pt-br`, `es`, `fr`, `de`, `it`, `zh`, `ja`, `ru`, `ar`.
- **Serviço de Tradução:** Integração transparente via `App\Services\I18n\TranslationService`.

---

## 8. Drawers Seguros (Safe Delete & Impact Assessment)

Ações destrutivas ou de arquivamento utilizam drawers com verificação de segurança (estilo Supabase/GitHub):
- **Impact Assessment:** Mostra número de planos afetados e garantia de *Grace Period*.
- **Desbloqueio Seguro:** Campo de digitação de palavra-chave (`DELETE` ou `ARCHIVE`) com validação reativa e proteção contra duplo clique.

---

## 9. Checklist de Conformidade para Novas Telas

Conforme estabelecido em `totustuus-layout-design/SKILL.md` e detalhado no [SDD 12 — Especificação de Portais, Navegação e Páginas](file:///c:/Xampp/htdocs/totustuussoftcloud/docs/sdd/12-portals-navigation-sidebar-pages-spec.md), toda tela desenvolvida nos 6 portais (`Developer`, `SaaS Acadêmico`, `Professor`, `Aluno`, `Pais/Responsáveis`, `Terceiros`) deve cumprir integralmente a checklist de 21 itens:

| Requisito | Padrão Esperado | Status |
|---|---|---|
| **1. Base em Inglês** | Código, comentários, variáveis, chaves e fallbacks primários em EN | Obrigatório |
| **2. 100% Funcional** | Sem erros de console JS, requisições quebradas ou elementos estáticos | Obrigatório |
| **3. Banco de Dados** | Integridade referencial, UUIDs e predicado estrito `tenant_id` | Obrigatório |
| **4. Migrations** | Versionadas e automatizadas em `database/migrations/` | Obrigatório |
| **5. 5-View TABs** | 5 visões (`kpi` │ `table` │ `cards` │ `kanban` │ `analytics`) com `#view-*` ↔ `tab-btn-*` sincronizados (padrão da canônica §4) — ou o chassis `.ud-tab-segmented` das demais páginas | Obrigatório |
| **6. Aba KPI Ativa** | Aba KPI selecionada por padrão e renderizada instantaneamente | Obrigatório |
| **7. Botões & Toolbar** | Input com debounce + filtros select + dropdown 7 formatos + CTA Emerald | Obrigatório |
| **8. Analytics / Charts** | Chart.js 4.4 (Line, Bar, Doughnut) com paleta Dark Emerald | Obrigatório |
| **9. Integrações** | APIs bancárias, PIX, Asaas, SEFAZ e webhooks | Obrigatório |
| **10. i18n / l10n** | Função `__('key', 'group', 'Fallback')` nos 10 idiomas do sistema | Obrigatório |
| **11. Stepper Drawers** | Painel lateral deslizante com stepper de 5 passos (`.drawer-step-grid`) | Obrigatório |
| **12. LGPD & Privacidade**| Mascaramento PII na UI e trilhas de auditoria para visualizações | Obrigatório |
| **13. Automações** | Rotinas assíncronas, webhooks e alertas em tempo real | Obrigatório |
| **14. Segurança** | Sem BOLA/IDOR, SQLi, XSS, CSRF e com Nonce CSP universal | Obrigatório |
| **15. Testes** | Cobertura de testes unitários e de integração em `tests/` | Obrigatório |
| **16. Colunas Sticky** | Coluna check (`left:0`) e ações (`right:0`) com `position: sticky; z-index:10` | Obrigatório |
| **17. Botões CRUD** | No mínimo 3 botões na tabela: 👁️ View, ✏️ Edit, 🗑️ Delete (`text-red-500`) | Obrigatório |
| **18. 3 Drawers** | View Drawer + Create/Edit 5-Step Drawer + Exclusão com keyword `"DELETE"` | Obrigatório |
| **19. Paginação Universal**| Paginação completa na Tabela e nos Grids de Cards (independente por grid) | Obrigatório |
| **20. Zero Inline JS** | Zero `onclick`/`onchange`/`oninput`; 100% via `data-action` e delegação | Obrigatório |
| **21. Kanban Drag & Drop**| HTML5 nativo (`draggable="true"`), indicador `.drag-over` e update otimista | Obrigatório |

Para a relação completa de todas as sidebars, sub-sidebars, accordions e páginas dos 6 portais, consulte o [SDD 12 — Especificação de Portais, Navegação e Páginas](file:///c:/Xampp/htdocs/totustuussoftcloud/docs/sdd/12-portals-navigation-sidebar-pages-spec.md).

---

## 10. Guardrails de Propagação a partir de /developer/commercial

Ao derivar novas páginas ou refatorar existentes a partir do Commercial Workspace, os seguintes guardrails são mandatórios:

### 10.1 Copiar estrutura e interações, NÃO copiar hardcodes

- **Estrutura a copiar:** Hierarquia visual (rail → sub-sidebar → header → segmented tabs → toolbar → view panes → drawers), padrão de 5 visões, padrão de 3 drawers (View/Create-Edit/Delete), batch action bar, pagination, kanban drag-and-drop.
- **Hardcodes a NÃO copiar:**
  - Wrapper transitório `tComm('key', 'Default')` — em migração para `__('key', 'group', 'Fallback')` do `TranslationService`. Não replicar o wrapper nem arrays inline de tradução.
  - Valores monetários fixos (`R$ 35.000,00`) — usar `formatCurrency()` ou `Intl.NumberFormat`.
  - Datas fixas — usar formatação via locale do projeto.
  - Cores hardcoded em inline styles — usar tokens CSS (`var(--accent)`, `var(--fg)`, etc.).
  - Dados mockados de oportunidades — conectar a dados reais via controller.

### 10.2 i18n / l10n — Verificar antes de propagar

- O Commercial usa `tComm()` como wrapper transitório para arrays inline de traduções. Este wrapper está em migração para o `__('key', 'group', 'Fallback')` padronizado via `TranslationService`. Novas páginas devem usar diretamente `__()` — não replicar `tComm()` nem arrays inline.
- **10 idiomas obrigatórios:** `en`, `pt-br`, `es`, `fr`, `de`, `it`, `zh`, `ja`, `ru`, `ar`.
- **RTL árabe:** A página define `dir="rtl"` para `ar`. Qualquer layout derivado deve suportar `rtl` via CSS (usar `margin-inline-start`/`end` em vez de `margin-left`/`right`).
- **Persistência de idioma:** O Commercial lê `$_GET['locale']` — a propagação deve respeitar o `cookie`/`session` de idioma do usuário via `locale_init.php`.

### 10.3 Formatação monetária, data e locale

- Usar `Intl.NumberFormat` com `style: 'currency'` e a moeda do locale ativo.
- **Não** copiar formatação hardcoded (`number_format($val, 2, ',', '.')`) — usar `formatCurrency()` do projeto.
- Datas via `Intl.DateTimeFormat` ou `Carbon` com locale.

### 10.4 Estados JS e drawers

- O Commercial tem extenso inline JS. Ao propagar a estrutura, migrar lógica para arquivos JS dedicados (`assets/js/ttsc.<modulo>.js`) com delegação via `data-action`.
- Drawers devem seguir o padrão: backdrop + panel + head/body/foot + stepper quando aplicável.
- **Verificar antes de propagar:** Que os drawers abrem/fecham corretamente, que o stepper funciona, que a validação de delete com keyword está ativa.

### 10.5 Autenticação e acesso

- A rota `/developer/commercial` requer autenticação (session middleware). Não foi possível acessar via ferramentas externas sem credenciais — a verificação visual depende de runtime autenticado.
- Qualquer página derivada herda o mesmo middleware de autenticação e isolamento de tenant.

### 10.6 O que NÃO fazer

- Não copiar inline `<style>` bloco — usar classes CSS compartilhadas de `ttsc.css` / `ttsc.supabase.css`.
- Não copiar inline JS — usar `data-action` + delegação em JS externo.
- Não copiar SVGs de bandeiras inline — usar asset externo ou componente reutilizável.
- Não inventar observações de browser — declarar explicitamente quando uma verificação requer autenticação.
