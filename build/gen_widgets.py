"""Gera components/<Nome>/preview.html a partir de docs/model/widgets/index.html (markup aprovado).
Cada página carrega o catálogo inteiro (widgets.js espera todos os widgets) e mostra só o que lhe cabe.
Uso: gen_widgets.py <repo> <projeto> 'Nome|w:balance,income|h:470|t:subtítulo' 'Nome|s:.medium-widget-section|h:900'"""
import sys, os, json
R, P = sys.argv[1], sys.argv[2]
h = open(R + '/docs/model/widgets/index.html', encoding='utf-8').read()
main = h[h.index('<main'):h.index('</main>')]
start = main.index('<section class="widgets-grid"')
content = main[start:main.rindex('</section>') + len('</section>')]
dialogs_and_rest = main[main.rindex('</section>') + len('</section>'):]
tail = h[h.index('</main>') + len('</main>'):h.index('<script', h.index('</main>'))]
for spec in sys.argv[3:]:
    parts = spec.split('|'); name = parts[0]; o = dict(p.split(':', 1) for p in parts[1:])
    widgets = o.get('w', '').split(',') if o.get('w') else []
    section = o.get('s', '')
    cols = int(o.get('c', '2' if len(widgets) > 1 else '1'))
    doc = f'''<!-- @dsCard group="Widgets" height={o.get('h', '520')} subtitle="{o.get('t', 'docs/model/widgets')}" -->
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{name}</title>
<link rel="stylesheet" href="../../vendor/app/widgets/widgets.css">
<style>
  html, body {{ margin: 0; }}
  .ds-host {{ padding: 16px; }}
  .ds-host [data-ds-hidden] {{ display: none !important; }}
  .ds-host .ds-focus {{ display: grid !important; grid-template-columns: repeat({cols}, minmax(0, 1fr)) !important; gap: 16px; }}
  .ds-host .ds-focus > * {{ grid-column: auto !important; }}
</style>
</head>
<body>
<button id="theme-toggle" type="button" hidden></button>
<div class="ds-host">
{content}
{dialogs_and_rest}
</div>
{tail}
<script>TTSCModelKit.syncTheme();</script>
<script src="../../vendor/app/widgets/widgets.js"></script>
<script>
  /* Mostra só {', '.join(widgets) or section}: o restante do catálogo continua no DOM porque widgets.js atualiza todos. */
  (function () {{
    var host = document.querySelector('.ds-host'), widgets = {json.dumps(widgets)}, section = {json.dumps(section)};
    var keep = section ? Array.prototype.slice.call(host.querySelectorAll(section)) :
      widgets.map(function (w) {{ return host.querySelector('[data-widget="' + w + '"]'); }}).filter(Boolean);
    function inKeep(el) {{ return keep.some(function (k) {{ return k === el || k.contains(el) || el.contains(k); }}); }}
    (function hide(parent) {{
      Array.prototype.forEach.call(parent.children, function (el) {{
        if (el.tagName === 'DIALOG' || el.matches('.widget-toast, .widget-tooltip')) return;
        if (!inKeep(el)) {{ el.setAttribute('data-ds-hidden', ''); return; }}
        if (keep.indexOf(el) === -1) hide(el);
      }});
    }})(host);
    if (!section) keep.forEach(function (k) {{ k.parentElement.classList.add('ds-focus'); }});
  }})();
</script>
</body>
</html>
'''
    os.makedirs(f'{P}/components/{name}', exist_ok=True)
    open(f'{P}/components/{name}/preview.html', 'w').write(doc)
    print(name, len(doc))
