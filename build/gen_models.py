"""Gera components/<Modelo>/preview.html sobre vendor/app (CSS/JS reais do app) + models/academico.json."""
import sys, os, json
P = sys.argv[1]
M = [
 # nome, grupo, rota, label, opts, aba, extra-js, css extra, subtítulo
 ('DataTable', 'Componentes', '/academico/turmas', 'Turmas', {'header': False, 'banner': False, 'tabs': False}, 'table', "var c=document.querySelectorAll('#model-table .row-checkbox');if(c[2]){c[2].click();}", '', 'Padrão do template (/developer/dashboard) · cabeçalho da visão, busca, ordenação, linha expansível, lote, ações, paginação global'),
 ('PageModel', 'Modelos', '/academico/matriculas/funil', 'Funil de Matrícula', {}, 'kpi', '', '', 'Página completa · cabeçalho, banner, abas, KPI, tabela, cards, Kanban, Analytics e drawers'),
 ('PageHeader', 'Modelos', '/academico/matriculas', 'Matrículas', {'banner': False, 'tabs': False}, None, '', '#model-page [role="tabpanel"]{display:none!important}', 'Cabeçalho da página · ícone, título, breadcrumb, Atualizar'),
 ('ContextBanner', 'Modelos', '/academico/matriculas', 'Matrículas', {'header': False, 'tabs': False}, None, '', '#model-page [role="tabpanel"]{display:none!important}', 'Banner de contexto · descrição e pill de contagem com alerta'),
 ('SegmentedTabs', 'Modelos', '/academico/matriculas/funil', 'Funil de Matrícula', {'header': False, 'banner': False}, 'kpi', "document.querySelector('[data-model-toggle=\"model-dropdown-export\"]').click();", '#model-page [role="tabpanel"]{display:none!important} #model-page{min-height:380px}', 'Abas segmentadas com contadores · Filtrar, Exportar (menu aberto), Nova matrícula'),
 ('KpiView', 'Modelos', '/academico/matriculas', 'Matrículas', {'header': False, 'banner': False, 'tabs': False}, 'kpi', '', '', 'KPI cards (valor, unidade, chips, rodapé) + distribuição + lista de atenção'),
 ('RecordsTable', 'Modelos', '/academico/matriculas/registros', 'Matrículas', {'header': False, 'banner': False, 'tabs': False}, 'table', "var c=document.querySelectorAll('#model-table .row-checkbox');if(c[1]){c[1].click();c[2].click();} var r=document.querySelector('#model-table tr.model-row td:nth-child(3)'); r&&r.click();", '', 'Data Table · busca, ordenação, linha expansível, barra de lote, paginação global'),
 ('RecordCards', 'Modelos', '/academico/matriculas/registros', 'Matrículas', {'header': False, 'banner': False, 'tabs': False}, 'cards', '', '', 'Cards / Grade · status, métricas, barra de progresso, ações e paginação'),
 ('KanbanBoard', 'Modelos', '/academico/matriculas/funil', 'Funil de Matrícula', {'header': False, 'banner': False, 'tabs': False}, 'kanban', '', '', 'Quadro Kanban v2.3 · chips de etapa, busca e paginação por coluna, arrastar e soltar, recolher, reordenar'),
 ('AnalyticsPanels', 'Modelos', '/academico/matriculas', 'Matrículas', {'header': False, 'banner': False, 'tabs': False}, 'analytics', '', '', 'Analytics · TTSCAnalytics com barras, rosca e linha, filtros por gráfico'),
 ('RecordDrawers', 'Modelos', '/academico/matriculas/registros', 'Matrículas', {'header': False, 'banner': False, 'tabs': False}, 'table', "document.querySelector('[data-model-view]').click();", '#main-viewport{min-height:760px}', 'Drawers View / Novo / Filtro no padrão view_item (View aberto)'),
 ('SettingsPanel', 'Modelos', '/academico/configuracoes', 'Configurações', {'header': False, 'banner': False}, None, '', '', 'Configurações · grupos em abas, seções e campos (texto, número, select, toggle)'),
 ('PageDashboard', 'Arquétipos de página', '/academico', 'Painel Acadêmico', {}, 'kpi', '', '', 'Dashboard · KPI + distribuição + Analytics, sem Novo'),
 ('PageRecords', 'Arquétipos de página', '/academico/matriculas/registros', 'Matrículas', {}, 'table', '', '', 'Records · KPI · Tabela · Cards · Analytics (padrão de 2 em cada 3 páginas)'),
 ('PagePipeline', 'Arquétipos de página', '/academico/matriculas/funil', 'Funil de Matrícula', {}, 'kanban', '', '', 'Pipeline · etapas reais com Kanban'),
 ('PageHistory', 'Arquétipos de página', '/academico/frequencia/historico', 'Histórico de Frequência', {}, 'table', '', '', 'History · somente leitura, abre na tabela, exporta CSV/PDF'),
 ('PageReport', 'Arquétipos de página', '/academico/relatorios/matriculas', 'Relatório de Matrículas', {}, 'analytics', '', '', 'Report · abre em Analytics, sem Novo'),
 ('PageSettings', 'Arquétipos de página', '/academico/configuracoes', 'Configurações Acadêmicas', {}, None, '', '', 'Settings · grupos em abas, Descartar / Salvar alterações'),
]
for name, group, route, label, opts, tab, extra, css, sub in M:
    doc = f'''<!-- @dsCard group="{group}" height=900 width=1280 {"page " if group != "Modelos" or name == "PageModel" else ""}subtitle="{sub}" -->
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{name}</title>
<style>html, body {{ margin: 0; }} #main-viewport {{ padding: 14px 16px 24px; }} {css}</style>
</head>
<body>
<main id="main-viewport" class="bg-slate-50">
  <div id="model-page" class="space-y-3.5" aria-live="polite"></div>
</main>
<div id="backdrop-overlay" class="fixed inset-0 bg-slate-900/40 backdrop-blur-[2px] z-40 transition-opacity hidden" onclick="window.closeAllDrawers && window.closeAllDrawers()"></div>
<script>
  TTSCModelKit.syncTheme();
  var ROUTE = '{route}';
  fetch('../../models/academico.json').then(function (r) {{ return r.json(); }}).then(function (sheet) {{
    TTSCModelKit.render(
      {{ portal: {{ label: 'Administração' }}, module: {{ label: 'Acadêmico' }}, page: {{ label: '{label}', route: ROUTE }} }},
      sheet.pages[ROUTE], {json.dumps(opts)}
    );
    {"TTSCModelKit.switchTab('%s');" % tab if tab else ""}
    setTimeout(function () {{ {extra} }}, 300);
  }});
</script>
</body>
</html>
'''
    os.makedirs(f'{P}/components/{name}', exist_ok=True)
    open(f'{P}/components/{name}/preview.html', 'w').write(doc)
print(len(M))
