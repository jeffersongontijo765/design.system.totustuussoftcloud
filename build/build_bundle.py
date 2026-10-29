"""Gera components/bundle.css e components/bundle.js do design system com a camada REAL do app.
Ordem idêntica à de resources/views/app/layouts/main.php. Uso: python3 build_bundle.py <repo> <projeto>"""
import json, os, re, sys
R, P = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
A = R + '/assets'
def rd(p): return open(p, encoding='utf-8').read()
def asc(s): return ''.join(ch if ord(ch) < 128 else '\\%x ' % ord(ch) for ch in s)
def clean(s):
    s = re.sub(r'/\*# sourceMappingURL=[^*]*\*/', '', s)
    s = re.sub(r'@charset[^;]*;', '', s)
    s = re.sub(r'@font-face\s*\{[^}]*\.\./fonts/[^}]*\}', '', s)
    return re.sub(r"url\(\s*['\"]?\.\./media/[^)]*\)", 'none', s)

# ---------- CSS ----------
runtime = clean(rd(A + '/css/tailwind-runtime.css'))
D = ':is(.dark,[data-theme=dark])'
runtime = runtime.replace('.dark *)', D + ' *)').replace('.dark .', D + ' .')
APP_CSS = ['ttsc.design-system', 'ttsc.supabase', 'ttsc.luxury-commercial', 'ttsc.shell-layout', 'ttsc.header', 'ttsc.commercial',
           'ttsc.commercial.model', 'ttsc.widgets', 'ttsc.kpi-widgets', 'ttsc.notifications', 'ttsc.drawer', 'ttsc.chat-widget',
           'ttsc.session-timeout', 'ttsc.pii-reveal', 'ttsc.rtl', 'ttsc.datepicker', 'ttsc', 'ttsc.pagination',
           # módulos de rota usados pelos modelos (domain_page / dashboard)
           'ttsc.kanban', 'ttsc.analytics-panels', 'ttsc.developer-dashboard']
fa = clean(rd(A + '/fonts/fontawesome.v7.2.0/css/fontawesome.css'))
dt = clean(rd(A + '/vendors/datatables-net/dataTables.dataTables.css'))
head = '''@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap");
/* TotusTuus SoftCloud Design System - components/bundle.css
 * A mesma camada CSS que resources/views/app/layouts/main.php carrega, na mesma ordem:
 * tailwind-runtime.css -> ttsc.design-system ... ttsc.pagination -> Font Awesome -> dataTables.
 * Antes do app: helpers ds-* e correcoes de contraste do runtime (o CSS do app vence onde estiliza o mesmo seletor).
 */
'''
base = '''
@font-face{font-family:"Font Awesome 7 Pro";font-style:normal;font-weight:300;font-display:block;src:url(../fonts/fa-light-300.woff2) format("woff2")}
:root{--fa-family-classic:"Font Awesome 7 Pro";--fa-style-family-classic:"Font Awesome 7 Pro"}
.fa-light,.fal{--fa-style:300}
html,body{font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;-webkit-font-smoothing:antialiased}
body{background:var(--ttsc-canvas,#fcfcfc);color:var(--ttsc-text,#1c1c1c);font-size:13px;line-height:1.5}
/* Helpers de layout das paginas de documentacao (ds-*) - nao usar em telas do produto. */
.ds-pad{padding:16px}
.ds-row{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.ds-stack{display:flex;flex-direction:column;gap:12px}
.ds-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.ds-label{font-size:11px;line-height:16px;font-weight:500;letter-spacing:.04em;text-transform:uppercase;color:var(--ttsc-text-muted,#6b6b6b)}
.ds-note{font-size:12px;line-height:16px;color:var(--ttsc-text-muted,#6b6b6b)}
'''
extra = rd(HERE + '/extra.css') if os.path.exists(HERE + '/extra.css') else ''
css = head + runtime + '\n' + base + extra
for name in APP_CSS:
    css += '\n/* ===== assets/css/%s.css ===== */\n' % name + clean(rd('%s/css/%s.css' % (A, name)))
css += '\n/* ===== fontawesome.css ===== */\n' + fa + '\n/* ===== dataTables.dataTables.css ===== */\n' + dt
css = asc(css)
assert '</style' not in css.lower()
open(P + '/components/bundle.css', 'w').write(css)

# ---------- JS ----------
ttscui = re.sub(r'//# sourceMappingURL=.*', '', rd(A + '/vendors/ttscui/ttscui.js'))
ns = '''
;(function (w) {
  /* Namespace TTSC para as paginas que documentam o ttscui (assets/vendors/ttscui).
   * ATENCAO: o app NAO carrega o ttscui; o comportamento real vem dos motores de assets/js abaixo. */
  var names = ["Accordion","Carousel","Clipboard","Collapse","ContextMenu","DataTable","Dismiss","Drawer","Dropdown","ImageInput","Modal","PinInput","RangeSlider","Rating","Reparent","Repeater","Scrollable","Scrollspy","Scrollto","Select","Stepper","Sticky","Tabs","ThemeSwitch","Toast","Toggle","TogglePassword","Tooltip"];
  var ns = { version: "1.1.0", components: w.ttscComponents };
  names.forEach(function (n) { if (w["ttsc" + n]) ns[n] = w["ttsc" + n]; });
  ns.init = function () { if (w.ttscComponents) w.ttscComponents.init(); };
  w.TTSC = ns;
})(window);
'''
APP_JS = ['ttsc.chart-defaults', 'ttsc.kanban-board', 'ttsc.analytics-panels', 'ttsc.workspace-search', 'ttsc', 'ttsc.events',
          'ttsc.tabs-overflow', 'ttsc.sidebar', 'ttsc.drawer', 'ttsc.select', 'ttsc.pagination', 'ttsc.datepicker',
          'ttsc.notifications', 'ttsc.overlays', 'ttsc.shell']
js = ttscui + ns + '\n/* ===== assets/vendors/chartjs/chart.umd.min.js ===== */\n;' + rd(A + '/vendors/chartjs/chart.umd.min.js') + '\n'
app = rd(P + '/vendor/app/app.js') if os.path.exists(P + '/vendor/app/app.js') else ''
kit = app[app.index('/* ===== model-kit.js ===== */'):] if '/* ===== model-kit.js ===== */' in app else ''
APT = {'ttsc.analytics-panels': [('>Filters<', '>Filtros<'), ('>Apply filters<', '>Aplicar filtros<'), ('aria-label="Filter ', 'aria-label="Filtrar '), ('aria-label="Close', 'aria-label="Fechar')],
       # No app o script fica no fim do <body>; no frame o bundle fica no <head> e document.body ainda e null.
       # Adia o MutationObserver para o DOMContentLoaded, sem mudar o comportamento.
       'ttsc.pagination': [('  if (window.MutationObserver && document.body) {\n', '  function observeBody() {\n    if (!(window.MutationObserver && document.body)) return;\n'),
                           ('})(window, document);', "  if (document.body) observeBody(); else document.addEventListener('DOMContentLoaded', observeBody);\n})(window, document);")]}
LIBS = {'ttsc.chart-defaults', 'ttsc.kanban-board', 'ttsc.analytics-panels'}
js += '''
;(function () {
  window.__ttscBoot = [];
  function boot() {
    var q = window.__ttscBoot; window.__ttscBoot = { push: function (c) { (0, eval)(c); } };
    for (var i = 0; i < q.length; i++) { try { (0, eval)(q[i]); } catch (e) { console.error(e); } }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else setTimeout(boot, 0);
})();
'''
for name in APP_JS:
    code = rd('%s/js/%s.js' % (A, name))
    for o, n in APT.get(name, []):
        assert o in code, (name, o)
        code = code.replace(o, n)
    if name in LIBS:
        js += '\n/* ===== assets/js/%s.js ===== */\n;' % name + code + '\n'
    else:
        # Motores do shell: no app ficam no fim do <body>. No frame o bundle esta no <head>, entao rodam no
        # DOMContentLoaded (eval global, para manter as funcoes globais como no app).
        js += '\n/* ===== assets/js/%s.js (DOMContentLoaded) ===== */\nwindow.__ttscBoot.push(%s);\n' % (name, json.dumps(code))
js += '\n' + kit + '''
;(function () {
  /* O tema do frame vem de <html data-theme>; o CSS do app usa html.dark e o ttsc.js reaplica o tema salvo.
     <meta name="ds-theme-sync" content="off"> desliga a sincronizacao (telas fora do shell, como o login). */
  function go() {
    var off = document.querySelector('meta[name="ds-theme-sync"][content="off"]');
    if (!off && window.TTSCModelKit && TTSCModelKit.syncTheme) TTSCModelKit.syncTheme();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
'''
assert '</script' not in js and '<!--' not in js
open(P + '/components/bundle.js', 'w').write(js)
print('bundle.css', len(css), 'bundle.js', len(js))
