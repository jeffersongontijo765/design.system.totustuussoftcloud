"""Navigation: shell real (header + rail + sub-sidebar) capturado do render de main.php.
Uso: python3 gen_nav.py <render.html> <saida/components/Navigation/preview.html>"""
import re, sys
src, out = sys.argv[1], sys.argv[2]
L = open(src, encoding='utf-8').read().split('\n')
def find(pat, start=0):
    for i in range(start, len(L)):
        if pat in L[i]: return i
    raise SystemExit('nao achei ' + pat)
b0 = find('<body') + 1
m0 = find('<main id="main-viewport"')
k0 = find('<div id="view-kpi"')
body = L[b0:k0]
html = '\n'.join(body)
# 1) tema: o frame decide (data-theme); remove o script que le localStorage
html = re.sub(r'<script[^>]*>\s*\(function\(\)\{try\{var h=document\.documentElement;.*?</script>', '', html, count=1, flags=re.S)
# 2) sem polling de saude (fetch a cada 20s)
html = re.sub(r'// Initial latency check and recurring 20s interval.*?\}, 20000\);', '', html, flags=re.S)
# 3) logo servido pela API -> marca local
html = re.sub(r'<img src="[^"]*assets/serve[^"]*"[^>]*>', '<span class="w-7 h-7 rounded-lg bg-emerald-500 text-white font-bold text-sm flex items-center justify-center">T</span>', html)
html = html.replace('http://127.0.0.1:8080/totustuussoftcloud', '#').replace('http://127.0.0.1:8080', '#')
html = re.sub(r' nonce="[^"]*"', '', html)
assert 'assets/serve' not in html and '<img' not in html, 'imagem remota'
html += '\n</main>\n</div>\n'
import os
d = os.path.dirname(out)
shell = """<!doctype html>
<html lang="pt-BR" class="h-full bg-slate-50">
<head><meta charset="utf-8"><title>Shell</title>
<script>
/* Tema: segue o data-theme do preview (frame pai), igual ao ttsc.js do app (html.dark + data-theme). */
(function () {
  function apply() {
    var p = null; try { p = parent.document.documentElement.getAttribute('data-theme'); } catch (e) {}
    var t = p === 'dark' ? 'dark' : 'light', h = document.documentElement;
    h.setAttribute('data-theme', t); h.classList.toggle('dark', t === 'dark');
    try { localStorage.setItem('ttsc-theme', t); } catch (e) {}
  }
  apply();
  try { new MutationObserver(apply).observe(parent.document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'class'] }); } catch (e) {}
})();
</script>
<link rel="stylesheet" href="../bundle.css"><script src="../bundle.js"></script>
<meta name="ds-theme-sync" content="off">
<style>main#main-viewport > :not(:nth-child(-n+5)) { display: none; }</style>
</head>
<body class="sb-app h-full bg-slate-50 text-slate-800 font-sans antialiased overflow-hidden flex flex-col">
""" + html + "\n</body>\n</html>\n"
open(os.path.join(d, 'shell.html'), 'w', encoding='utf-8').write(shell)
head = """<!-- @dsCard group="Navegação" height=640 subtitle="shell real de main.php · header, rail (#primary-rail) e sub-sidebar (#sub-sidebar) · desktop, tablet e mobile" -->
<!doctype html>
<html lang="pt-BR">
<head><meta charset="utf-8"><title>Navigation</title>
<style>
  body { margin: 0; background: var(--ttsc-canvas, #f8fafc); font-family: Inter, system-ui, sans-serif; }
  .nv-bar { display: flex; align-items: center; gap: 8px; padding: 8px 12px; border-bottom: 1px solid var(--ttsc-border, #e2e8f0); background: var(--ttsc-surface, #fff); color: var(--ttsc-text-2, #64748b); font-size: 12px; }
  .nv-bar button { font: inherit; padding: 4px 10px; border-radius: 8px; border: 1px solid var(--ttsc-border, #e2e8f0); background: transparent; color: inherit; cursor: pointer; }
  .nv-bar button[aria-pressed="true"] { background: var(--ttsc-accent-soft, #ecfdf5); color: var(--ttsc-accent-text, #047857); border-color: var(--ttsc-accent-border, #a7f3d0); font-weight: 600; }
  .nv-stage { position: relative; height: calc(100vh - 45px); overflow: hidden; }
  .nv-stage iframe { position: absolute; top: 0; left: 0; border: 0; transform-origin: 0 0; background: #f8fafc; }
</style>
</head>
<body>
<div class="nv-bar" role="group" aria-label="Largura da tela">
  <button type="button" data-w="1440" aria-pressed="true">Desktop 1440</button>
  <button type="button" data-w="1024" aria-pressed="false">Tablet 1024</button>
  <button type="button" data-w="390" aria-pressed="false">Mobile 390</button>
  <span id="nv-note" style="margin-left:auto">rail + sub-sidebar fixos (&ge; 1100px)</span>
</div>
<div class="nv-stage" id="nv-stage"><iframe id="nv-shell" src="shell.html" title="Shell do app" width="1440" height="900"></iframe></div>
<script>
(function () {
  var stage = document.getElementById('nv-stage'), f = document.getElementById('nv-shell'), note = document.getElementById('nv-note'), w = 1440;
  var notes = { 1440: 'rail + sub-sidebar fixos (\\u2265 1100px)', 1024: 'abaixo de 1100px o sub-sidebar vira gaveta (ttsc.shell.js)', 390: 'mobile: rail e sub-sidebar em gaveta, header compacto' };
  function fit() {
    var s = Math.min(stage.clientWidth / w, 1), h = Math.ceil(stage.clientHeight / s);
    f.style.width = w + 'px'; f.style.height = h + 'px'; f.style.transform = 'scale(' + s + ')';
    f.style.left = Math.max(0, (stage.clientWidth - w * s) / 2) + 'px';
  }
  document.querySelectorAll('.nv-bar button').forEach(function (b) {
    b.addEventListener('click', function () {
      w = +b.dataset.w; note.textContent = notes[w];
      document.querySelectorAll('.nv-bar button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      fit();
    });
  });
  window.addEventListener('resize', fit); fit();
})();
</script>
</body>
</html>
"""
open(out, 'w', encoding='utf-8').write(head)
print(out, len(shell))
