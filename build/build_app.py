"""Gera vendor/app/{app-1.css, app-2.css, app.js, chart.umd.min.js} do design system a partir do repo.
Uso: python3 build_app.py <repo> <saida-vendor-app>"""
import os, re, sys, shutil
R, A = sys.argv[1], sys.argv[2]
os.makedirs(A, exist_ok=True)

# ---- model-kit.js: renderizadores de docs/model/app/_assets/model-page.js sem shell/rota ----
src = open(R + '/docs/model/app/_assets/model-page.js', encoding='utf-8').read()
a = src.index("  /* ── navigation: rail + sub-sidebar swap, model links"); b = src.index("  /* ── shared markup pieces")
src = src[:a] + src[b:]
a = src.index("  var ROOT = 'docs/model/app/';"); b = src.index("  function esc(v)")
src = src[:a] + src[b:]
a = src.index("  function load(path) {"); b = src.index("  function hash(str)")
src = src[:a] + src[b:]
src = src.replace("  function render(t, spec, nav) {\n    var root = document.getElementById('model-page');\n    var page = spec && spec.pages && spec.pages[t.page.route];",
                  "  function render(t, page, opts) {\n    opts = opts || {};\n    var root = document.getElementById('model-page');\n    lastArgs = [t, page, opts];")
src = src.replace("    document.title = t.page.label + ' · ' + t.module.label + ' · ' + t.portal.label + ' (model)';\n    applyNav(nav, t);\n", "")
src = src.replace("    root.innerHTML = headerHtml(t, page) + bannerHtml(page.banner && Object.assign({}, page.banner, { pill: page.banner.pill ? page.banner.pill.replace('{count}', rows.length) : '' }), attention) + tabsHtml(tabs, page.defaultView || views[0], actionsHtml(page)) + body;",
                  "    root.innerHTML = (opts.header === false ? '' : headerHtml(t, page)) + (opts.banner === false ? '' : bannerHtml(page.banner && Object.assign({}, page.banner, { pill: page.banner.pill ? page.banner.pill.replace('{count}', rows.length) : '' }), attention)) + (opts.tabs === false ? '' : tabsHtml(tabs, page.defaultView || views[0], actionsHtml(page))) + body;")
src = src.replace("    if ((el = ev.target.closest('[data-model-refresh]'))) { route(); return; }",
                  "    if ((el = ev.target.closest('[data-model-refresh]'))) { if (lastArgs) render.apply(null, lastArgs); return; }")
src = src.replace("  var current = null;", "  var current = null, lastArgs = null;")
a = src.index("  function route() {"); b = src.index("})(window, document);")
src = src[:a] + '''  /* ── API pública (design system) ─────────────────────────────────────── */
  window.TTSCModelKit = {
    render: render, switchTab: switchTab, generate: generate,
    blocks: { header: headerHtml, banner: bannerHtml, tabs: tabsHtml, actions: actionsHtml, viewHeader: viewHeader,
      search: searchHtml, pager: pagerHtml, empty: emptyHtml, kpi: kpiHtml, breakdown: breakdownHtml, table: tableHtml,
      cards: cardsHtml, card: cardHtml, drawers: drawersHtml, settings: settingsHtml },
    mountKanban: mountKanban, mountAnalytics: mountAnalytics, fillView: fillView, tones: TONES,
    /* O tema do design system vem de <html data-theme>; o CSS do app usa html.dark. ttsc.js aplica o tema salvo
       no DOMContentLoaded, então a sincronização roda depois disso e acompanha mudanças de data-theme. */
    syncTheme: function () {
      var html = document.documentElement;
      function apply() {
        var dark = html.getAttribute('data-theme') === 'dark';
        if (html.classList.contains('dark') !== dark) html.classList.toggle('dark', dark);
        if (html.classList.contains('light') === dark) html.classList.toggle('light', !dark);
      }
      apply();
      new MutationObserver(apply).observe(html, { attributes: true, attributeFilter: ['data-theme', 'class'] });
    }
  };
''' + src[b:]
# rótulos em pt-BR, mesmos termos de resources/views/app/pages/developer/dashboard.php
PT = [
 (">No ' + esc(page.entity.plural.toLowerCase()) + ' match these filters<", ">Nenhum registro em ' + esc(page.entity.plural.toLowerCase()) + ' para estes filtros<"),
 ("Adjust the search or clear the filters to see every record.", "Ajuste a busca ou limpe os filtros para ver todos os registros."),
 ("Adjust the search to see every record.", "Ajuste a busca para ver todos os registros."),
 (">Refresh<", ">Atualizar<"), (">Filter<", ">Filtrar<"), (">Export<", ">Exportar<"), (">Showing<", ">Exibindo<"),
 ("> <span>of</span> <", "> <span>de</span> <"), (">Per page:<", ">Por página:<"), ('"Per page"', '"Por página"'),
 (">Clear filters<", ">Limpar filtros<"), (">Save changes<", ">Salvar alterações<"), (">Discard<", ">Descartar<"),
 (">Edit Data<", ">Editar dados<"), (">Delete Selected<", ">Excluir selecionados<"), (">Delete<", ">Excluir<"),
 (">Close<", ">Fechar<"), (">Clear<", ">Limpar<"), (">Cancel<", ">Cancelar<"), (">Apply filters<", ">Aplicar filtros<"),
 (">Applies to KPI, table, cards and Kanban<", ">Vale para KPI, tabela, cards e Kanban<"), (">All<", ">Todos<"),
 (">Adjust the search to see every record.<", ">Ajuste a busca para ver todos os registros.<"), (">Actions<", ">Ações<"),
 (">View Record<", ">Ver registro<"), ('"View Details"', '"Ver detalhes"'), ('"Edit"', '"Editar"'), ('"Delete"', '"Excluir"'),
 ('"Select row"', '"Selecionar linha"'), ('"Select all"', '"Selecionar todos"'), ('"Previous page"', '"Página anterior"'),
 ('"Next page"', '"Próxima página"'), ('"Pagination"', '"Paginação"'), ('"Close"', '"Fechar"'), ('"Clear selection"', '"Limpar seleção"'),
 ("'Yes'", "'Sim'"), ("|| 'No')", "|| 'Não')"), ("'Search '", "'Buscar '"), ("'Filter '", "'Filtrar '"),
 ("'Fill in the '", "'Preencha os dados de '"), ("'Data Table'", "'Tabela de Dados'"), ("'Cards / Grid'", "'Cards / Grade'"),
 ("'Kanban Board'", "'Quadro Kanban'"), ("'Export as CSV'", "'Exportar como CSV'"), ("'Excel Spreadsheet'", "'Planilha Excel'"),
 ("'PDF Document'", "'Documento PDF'"), ("'JSON Dataset'", "'Conjunto de Dados JSON'"), ("'Export Selected'", "'Exportar selecionados'"),
 ("'No data for this chart'", "'Sem dados para este gráfico'"), ("'Current snapshot'", "'Situação atual'"), ("'Total '", "'Total '"),
 ("'In production this calls '", "'Em produção esta ação chama '"), ("'Page model'", "'Modelo de página'"),
 ("' SELECTED'", "' SELECIONADOS'"),
 ("'Last ' + (a.months || 12) + ' months'", "'Últimos ' + (a.months || 12) + ' meses'"),
 ("label: 'Visualization'", "label: 'Visualização'"), ("['bar', 'Bars']", "['bar', 'Barras']"), ("['line', 'Line']", "['line', 'Linha']"), ("['doughnut', 'Doughnut']", "['doughnut', 'Rosca']"),
 ("unit: unit && unit !== 'money' ? unit : undefined", "unit: unit === 'count' ? page.entity.plural.toLowerCase() : (unit && unit !== 'money' ? unit : undefined)"), ("'Record'", "'Registro'"), ("'Records'", "'Registros'"),
 (">Export ' + esc(page.entity.plural)", ">Exportar ' + esc(page.entity.plural)"),
]
PT += [
 ("currency: valueF && valueF.type === 'money' ? (page.currency || 'BRL') : ''", "currency: valueF && valueF.type === 'money' ? (page.currency === 'BRL' || !page.currency ? 'R$' : page.currency) : ''"),
 ("Edit ' + esc", "Editar ' + esc"), ('aria-label="Page \' + n', 'aria-label="Página \' + n'),
 ("Full Breakdown • ", "Detalhamento • "), ("' Details'", "' · detalhes'"), ("</i>Delete<", "</i>Excluir<"),
 ('title="Delete"', 'title="Excluir"'), ('title="Edit"', 'title="Editar"'), ('title="View Details"', 'title="Ver detalhes"'),
 ("<span>New ' + esc(page.entity.singular) + '</span>", "<span>' + esc(page.entity.newLabel || ('Novo ' + page.entity.singular)) + '</span>"),
 ("drawerShell('model-drawer-new', 'fa-plus', 'New ' + page.entity.singular,", "drawerShell('model-drawer-new', 'fa-plus', page.entity.newLabel || ('Novo ' + page.entity.singular),"),
 ("addLabel: 'Add', allowNewStage: false", "addLabel: 'Adicionar', allowNewStage: false, strings: { stages: 'Etapas do ciclo', all: 'Todas as etapas', boardValue: 'Valor no quadro', search: 'Buscar nesta etapa...', noItems: 'Nenhum item nesta etapa', noResults: 'Nenhum resultado para', page: 'Página', of: 'de', perPage: 'por página', newStage: 'Nova etapa', stageName: 'Nome da etapa', create: 'Criar', cancel: 'Cancelar', add: 'Adicionar', title: 'Título do item', value: 'Valor (opcional)', collapse: 'Recolher etapa', expand: 'Expandir etapa', showing: 'Exibindo', movedTo: 'movido para' }"),
 ("page.entity.singular + ' Board'", "'Quadro de ' + page.entity.plural.toLowerCase()"),
 ("'Drag & drop changes the ' + (field(page, page.stageField).label || 'stage').toLowerCase()", "'Arrastar e soltar altera ' + (field(page, page.stageField).label || 'a etapa').toLowerCase()"),
]
for o, n in PT: src = src.replace(o, n)
kit = '''/*
 * TotusTuus Design System — model-kit.js
 * Renderizadores de docs/model/app/_assets/model-page.js (markup de resources/views/app/pages/developer/dashboard.php),
 * sem shell, catálogo nem rota por hash, com os rótulos em pt-BR do dashboard real.
 * TTSCModelKit.render({portal:{label}, module:{label}, page:{label, route}}, fichaDaPagina, {header, banner, tabs})
 * desenha cabeçalho, banner, abas, KPI, distribuição, tabela, cards, Kanban v2.3, Analytics e drawers em #model-page.
 */
''' + src

# ---- CSS do app na ordem de docs/model/app/developer.html ----
def clean(s):
    s = re.sub(r'@font-face\s*\{[^}]*\.\./fonts/[^}]*\}', '', s)
    return re.sub(r"url\(\s*['\"]?\.\./media/[^)]*\)", 'none', s)
def asc(s): return ''.join(ch if ord(ch) < 128 else '\\%x ' % ord(ch) for ch in s)
groups = {'app-1.css': ['ttsc.design-system', 'ttsc.supabase', 'ttsc.luxury-commercial', 'ttsc.shell-layout', 'ttsc.header', 'ttsc.commercial'],
          'app-2.css': ['ttsc.commercial.model', 'ttsc.widgets', 'ttsc.kpi-widgets', 'ttsc.notifications', 'ttsc.drawer', 'ttsc.chat-widget', 'ttsc.session-timeout', 'ttsc.pii-reveal', 'ttsc.rtl', 'ttsc.datepicker', 'ttsc', 'ttsc.pagination', 'ttsc.developer-dashboard', 'ttsc.kanban', 'ttsc.analytics-panels']}
for name, g in groups.items():
    out = '/* TotusTuus SoftCloud — CSS do app (assets/css), ordem de docs/model/app/developer.html: ' + ', '.join(x + '.css' for x in g) + ' */\n'
    for x in g: out += '\n/* ===== ' + x + '.css ===== */\n' + clean(open(f'{R}/assets/css/{x}.css', encoding='utf-8').read())
    open(f'{A}/{name}', 'w').write(asc(out))
js = ['ttsc.chart-defaults', 'ttsc.kanban-board', 'ttsc.analytics-panels', 'ttsc', 'ttsc.events', 'ttsc.tabs-overflow', 'ttsc.drawer', 'ttsc.select', 'ttsc.pagination', 'ttsc.overlays']
out = '/* TotusTuus SoftCloud — JS do app (assets/js) + model-kit, ordem de docs/model/app/developer.html */\n'
APT = [('>Filters<', '>Filtros<'), ('>Apply filters<', '>Aplicar filtros<'), ('aria-label="Filter ', 'aria-label="Filtrar '), ('aria-label="Close', 'aria-label="Fechar')]
for x in js:
    code = open(f'{R}/assets/js/{x}.js', encoding='utf-8').read()
    if x == 'ttsc.analytics-panels':
        for o, n in APT: code = code.replace(o, n)
    if x == 'ttsc.kanban-board':
        for o, n in [('aria-label="Scroll left"', 'aria-label="Rolar para a esquerda"'), ('aria-label="Scroll right"', 'aria-label="Rolar para a direita"'),
                     ('aria-label="Clear"', 'aria-label="Limpar"'), ('aria-label="First page"', 'aria-label="Primeira página"'),
                     ('aria-label="Items per page"', 'aria-label="Itens por página"'), ('aria-label="Last page"', 'aria-label="Última página"'),
                     ('aria-label="Next page"', 'aria-label="Próxima página"'), ('aria-label="Page number"', 'aria-label="Número da página"'),
                     ('aria-label="Previous page"', 'aria-label="Página anterior"'), ('aria-label="Color"', 'aria-label="Cor"')]:
            code = code.replace(o, n)
    out += '\n/* ===== ' + x + '.js ===== */\n;' + code + '\n'
out += '\n/* ===== model-kit.js ===== */\n;' + kit
assert '</script' not in out
open(f'{A}/app.js', 'w').write(out)
shutil.copy(R + '/assets/vendors/chartjs/chart.umd.min.js', A + '/chart.umd.min.js')
print('ok', {f: os.path.getsize(f'{A}/{f}') for f in os.listdir(A)})
