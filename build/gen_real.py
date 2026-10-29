"""Gera previews a partir de renders REAIS do app (PHP), sem reescrever markup.
  DataTable  <- resources/views/app/partials/chassis/domain_page.php + table.php (aba Tabela)
Uso: gen_real.py <projeto> <domain_render.html>"""
import re, sys, os
P, DOMAIN = sys.argv[1], sys.argv[2]
def strip_assets(h):
    h = re.sub(r'<script[^>]*src="https://cdn\.jsdelivr\.net/npm/chart\.js[^"]*"[^>]*></script>', '', h)  # Chart.js já vem no bundle
    h = re.sub(r'<link[^>]*href="[^"]*/assets/css/[^"]*"[^>]*>', '', h)                                  # CSS do app já vem no bundle
    h = re.sub(r'<script[^>]*src="[^"]*/assets/js/[^"]*"[^>]*></script>', '', h)                         # JS do app já vem no bundle
    return h.replace('http://127.0.0.1:8080/totustuussoftcloud/', '../../')
frag = strip_assets(open(DOMAIN, encoding='utf-8').read())
doc = '''<!-- @dsCard group="Componentes" height=1100 width=1280 subtitle="Render real de partials/chassis/table.php via domain_page.php · busca, ordenação, linha expansível, lote, ações, paginação ttsc.pagination" -->
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>DataTable</title>
<style>
  html, body { margin: 0; }
  #main-viewport { padding: 14px 16px 24px; }
  /* só a aba Tabela do domain_page: o restante da página fica no DOM (os behaviors leem os dados de lá) */
  .ds-only-table > :not(#view-table):not([id^="domain-drawer"]):not(.sb-drawer):not(script):not(style):not(template):not(#domain-row-tooltip) { display: none !important; }
</style>
</head>
<body>
<main id="main-viewport" class="bg-slate-50">
<div class="ds-only-table space-y-3.5">
''' + frag + '''
</div>
</main>
<div id="backdrop-overlay" class="fixed inset-0 bg-slate-900/40 backdrop-blur-[2px] z-40 transition-opacity hidden"></div>
<script>
  /* Página real: /academic/enrollment/re-enrollment (inst_secretariat_reenrollment), com 18 registros ilustrativos injetados no render. */
  document.addEventListener('DOMContentLoaded', function () { if (window.switchDomainTab) window.switchDomainTab('table'); });
</script>
</body>
</html>
'''
os.makedirs(P + '/components/DataTable', exist_ok=True)
open(P + '/components/DataTable/preview.html', 'w').write(doc)
print('DataTable', len(doc))
