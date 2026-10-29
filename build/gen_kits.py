"""Starter Kits: gera kit*.html (render REAL dos layouts do repo, sem rede) + preview.html por kit.

Generaliza gen_nav.py. Fontes (renders reais, produzidos pelos harnesses):
  - shell do app (app/layouts/main.php): $SPD/kits/r_shell_<rota>.html (copias de /tmp/render_<rota>.html, render_harness.php)
  - auth/web/errors/install: $SPD/kits/r_*.html (view_harness.php -> PlatesEngine real)
  - e-mails e PDF: $SPD/kits/r_mail_*.html, r_print_pdf.html (mail_print_harness.php)
Uso: python3 gen_kits.py [Kit ...]   (sem argumentos = todos)
"""
import json, os, re, shutil, subprocess, sys

SPD = os.environ.get('DS_WORK', os.path.abspath('work'))  # pasta de trabalho: ds/project, dtr/, kits/
REPO = os.environ.get('DS_REPO', os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
P = SPD + '/ds/project'
COMP = P + '/components'
K = SPD + '/kits'
HOSTS = ['http://127.0.0.1:8080/totustuussoftcloud', 'http://127.0.0.1:8080', 'https://localhost/totustuussoftcloud', 'http://localhost/totustuussoftcloud', '/totustuussoftcloud']

# ---------------------------------------------------------------- helpers
_hashes = None
def hashes():
    global _hashes
    if _hashes is None:
        f = K + '/hashes.json'
        _hashes = json.load(open(f)) if os.path.exists(f) else {}
    return _hashes

def resolve_hashes(html):
    """garante que todo serve?h= do HTML esta no mapa (AssetPathMapper::getRelativePath)."""
    need = sorted(set(re.findall(r'serve\?h=([0-9a-f]{16})', html)) - set(hashes()))
    if not need:
        return
    open(K + '/hashes.txt', 'w').write('\n'.join(need) + '\n')
    out = subprocess.run(['php', '-r', 'require "vendor/autoload.php"; \\TotusTuus\\Config\\Env::load(); $m=[]; foreach(file($argv[1],FILE_IGNORE_NEW_LINES) as $h){ $m[$h]=\\App\\Security\\AssetPathMapper::getRelativePath($h);} echo json_encode($m);', K + '/hashes.txt'],
                         cwd=REPO, capture_output=True, text=True).stdout
    hashes().update(json.loads(out[out.find('{'):]))
    json.dump(hashes(), open(K + '/hashes.json', 'w'), indent=1)

def copy_repo(rel, kitdir):
    """copia assets/<x> do repo para <kit>/assets/<x>; devolve o caminho relativo usado no HTML."""
    rel = rel.split('?')[0].split('#')[0]
    src = os.path.join(REPO, rel)
    if not os.path.isfile(src):
        return None
    dst = os.path.join(kitdir, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    if rel.endswith('.css'):
        fix_css(dst, rel, kitdir)
    return rel

def fix_css(dst, rel, kitdir):
    """copia o que o CSS referencia por url(relativa); remove @import remoto."""
    css = open(dst, encoding='utf-8', errors='replace').read()
    css = re.sub(r'@import\s+url\((["\']?)https?://[^)]*\)\s*;?', '', css)
    css = re.sub(r'@import\s+["\']https?://[^"\']*["\']\s*;?', '', css)
    base = os.path.dirname(rel)
    for u in set(re.findall(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', css)):
        if u.startswith(('data:', '#', 'http')):
            continue
        tgt = os.path.normpath(os.path.join(base, u.split('?')[0].split('#')[0]))
        if os.path.isfile(os.path.join(REPO, tgt)) and not tgt.startswith('..'):
            d = os.path.join(kitdir, tgt); os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copyfile(os.path.join(REPO, tgt), d)
    open(dst, 'w', encoding='utf-8').write(css)

_fa_full = None
_fa_used = {}
def fa_css(kitdir, used_html):
    """Font Awesome do bundle (somente peso light servido em $P/fonts), reduzido aos icones usados."""
    global _fa_full
    if _fa_full is None:
        s = open(COMP + '/bundle.css', encoding='utf-8').read()
        i = s.find('/* ===== fontawesome.css'); j = s.find('/* ===== dataTables', i)
        _fa_full = s[i:j]
    # varias variantes do mesmo kit dividem assets/fa.css: acumula os icones de todas
    used = _fa_used.setdefault(kitdir, set())
    used.update(re.findall(r'\bfa-[a-z0-9-]+', used_html))
    def rule(m):  # regra de icone (pode agrupar aliases): fica se algum seletor e usado
        names = re.findall(r'\.(fa-[a-z0-9-]+)', m.group(1))
        return m.group(0) if any(n in used for n in names) else ''
    keep = [re.sub(r'((?:\.fa-[a-z0-9-]+\s*,\s*)*\.fa-[a-z0-9-]+)\s*\{\s*--fa:[^}]*\}\n?', rule, _fa_full)]
    head = ('@font-face{font-family:"Font Awesome 7 Pro";font-style:normal;font-weight:300;font-display:block;'
            'src:url(../../../fonts/fa-light-300.woff2) format("woff2")}\n'
            ':root{--fa-family-classic:"Font Awesome 7 Pro";--fa-style-family-classic:"Font Awesome 7 Pro"}\n'
            '.fa-light,.fal{--fa-style:300}\n'
            '/* Pesos solid/regular/brands caem no unico arquivo servido (light 300). */\n')
    os.makedirs(kitdir + '/assets', exist_ok=True)
    open(kitdir + '/assets/fa.css', 'w', encoding='utf-8').write(head + '\n'.join(keep))

THEME_SYNC = """<script>
/* Starter Kit: segue o tema do preview (frame pai) e grava as chaves reais de tema de cada layout:
   app/web/erros = html.dark + data-theme + localStorage 'ttsc-theme'; auth = 'od-theme'; portal de suporte = 'portal_theme'. */
(function () {
  function apply() {
    var p = null; try { p = parent.document.documentElement.getAttribute('data-theme'); } catch (e) {}
    var t = p === 'dark' ? 'dark' : 'light', h = document.documentElement;
    h.setAttribute('data-theme', t); h.classList.toggle('dark', t === 'dark'); h.classList.toggle('light', t !== 'dark');
    try { ['ttsc-theme', 'od-theme', 'theme', 'portal_theme'].forEach(function (k) { localStorage.setItem(k, t); }); } catch (e) {}
  }
  apply();
  try { if (parent !== window) new MutationObserver(apply).observe(parent.document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'class'] }); } catch (e) {}
})();
</script>"""

LIGHT_ONLY = ("<script>/* Starter Kit: layout sem tema escuro -> grava 'light' nas chaves reais (o localStorage e compartilhado entre kits) */"
              "(function(){var h=document.documentElement;h.setAttribute('data-theme','light');h.classList.remove('dark');h.classList.add('light');"
              "try{['ttsc-theme','od-theme','theme','portal_theme'].forEach(function(k){localStorage.setItem(k,'light')})}catch(e){}})();</script>")

def theme_script(theme):
    return LIGHT_ONLY if theme == 'light' else (THEME_SYNC if theme else '')

def strip_common(html):
    html = re.sub(r' nonce="[^"]*"', '', html)
    html = re.sub(r'<link[^>]*(fonts\.googleapis|fonts\.gstatic)[^>]*>\s*', '', html)
    html = re.sub(r'<link[^>]*rel="(icon|shortcut icon|apple-touch-icon)"[^>]*>\s*', '', html)
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*>\s*', '', html)
    html = re.sub(r'<meta[^>]*(og:image|twitter:image)[^>]*>\s*', '', html)
    html = re.sub(r'<base [^>]*>\s*', '', html)
    html = re.sub(r'<script[^>]*cdn\.tailwindcss\.com[^>]*></script>\s*', '', html)
    # polling de saude do header (fetch a cada 20s)
    html = re.sub(r'// Initial latency check and recurring 20s interval.*?\}, 20000\);', '', html, flags=re.S)
    return html

def rewrite_urls(html, kitdir, app_mode=False):
    resolve_hashes(html)
    def serve(m):
        rel = hashes().get(m.group(2))
        loc = copy_repo(rel, kitdir) if rel else None
        return m.group(1) + (loc or 'data:,')
    html = re.sub(r'(["\'(])(?:https?://[^"\'()]*?)/api/v1/assets/serve\?h=([0-9a-f]{16})[^"\')]*', serve, html)
    def asset(m):
        rel = 'assets/' + m.group(2)
        if 'fontawesome' in rel and rel.endswith('all.css'):
            return m.group(1) + 'assets/fa.css'
        if app_mode and re.match(r'assets/(js|css)/', rel):
            return m.group(1) + '#drop'
        loc = copy_repo(rel, kitdir)
        return m.group(1) + (loc or '#')
    # URLs JSON-escapadas (json_encode em <script>): viram relativas ao kit (fixtures em <kit>/api/...)
    for h in HOSTS[:4]:
        html = html.replace(h.replace('/', '\\/') + '\\/', '')
    for h in HOSTS:
        html = re.sub(r'(["\'(])' + re.escape(h) + r'/assets/([^"\'()?#\s]+)(\?[^"\')\s]*)?', asset, html)
    for h in HOSTS:
        html = html.replace(h, '#')
    if app_mode:  # scripts do app ja estao no ../bundle.js
        html = re.sub(r'<script[^>]*src="#drop"[^>]*>\s*</script>\s*', '', html)
        html = re.sub(r'<link[^>]*href="#drop"[^>]*>\s*', '', html)
    return html

def check_offline(html, name):
    bad = re.findall(r'(?:src|href)=["\'](https?://[^"\']+)', html)
    bad = [b for b in bad if 'w3.org' not in b]
    bad += re.findall(r'url\(\s*["\']?(https?://[^"\')]+)', html)
    assert not bad, (name, bad[:5])

# ---------------------------------------------------------------- shell (app/layouts/main.php)
SLOT_CSS = """<style>
/* Starter Kit — slot de conteudo (so tokens). Some na pagina real: ali entra $this->section('content'). */
.kit-slot { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; min-height: 340px;
  border: 2px dashed color-mix(in srgb, var(--muted-foreground, #64748b) 55%, transparent); border-radius: var(--ttsc-radius-surface, 16px);
  background: var(--ttsc-surface, var(--surface, #fff)); color: var(--ttsc-text-muted, #64748b); text-align: center; padding: 24px; }
.kit-slot i { font-size: 28px; color: var(--ttsc-accent-text, #047857); }
.kit-slot strong { color: var(--ttsc-text, #0f172a); font-size: 14px; }
.kit-slot code { font-size: 12px; color: var(--ttsc-text-2, #475569); background: var(--ttsc-canvas-2, #f1f5f9); padding: 2px 8px; border-radius: 6px; }
</style>"""

SLOT_HTML = """
<!-- ===== SLOT DE CONTEUDO (Starter Kit) — na view real: <?php $this->start('content') ?> ... <?php $this->stop() ?> ===== -->
<section class="kit-slot" aria-label="Slot de conteúdo da página" data-kit-slot="content">
  <i class="fa-light fa-square-dashed" aria-hidden="true"></i>
  <strong>Slot de conteúdo</strong>
  <span>Visões KPI, Tabela, Cartões, Kanban ou Analytics entram aqui.</span>
  <code>&lt;?= $pageContent ?&gt; &middot; app/layouts/main.php</code>
</section>
"""

def find(L, pat, start=0, end=None):
    for i in range(start, end or len(L)):
        if pat in L[i]:
            return i
    raise SystemExit('nao achei ' + pat)

def shell_kit(src, kitdir, out_name, main_mode='slot', collapsed=False, extra_css='', title='Shell', theme=True):
    """main_mode: 'slot' (header+banner+abas + slot), 'kpi' (inclui #view-kpi real), 'full' (conteudo inteiro do main)."""
    L = open(src, encoding='utf-8').read().split('\n')
    b0 = find(L, '<body') + 1
    m0 = find(L, '<main id="main-viewport"')
    f0 = find(L, '<footer', m0)
    m1 = max(i for i in range(m0, f0) if '</main>' in L[i])
    pg = find(L, '<!-- Page-level modals/drawers', f0)
    if main_mode == 'full':
        content = L[m0 + 1:m1]
    else:
        k0 = find(L, '<div id="view-kpi"', m0, m1)
        if main_mode == 'slot':
            content = L[m0 + 1:k0] + [SLOT_HTML]
        else:
            t0 = find(L, '<div id="view-table"', k0, m1)
            content = L[m0 + 1:t0]
    body = L[b0:m0 + 1] + content + L[m1:pg]
    body.append('    <div id="totus-toast-container" class="fixed top-5 right-5 z-[99999] flex flex-col gap-2.5 max-w-sm w-full pointer-events-none" aria-live="polite"></div>')
    html = '\n'.join(body)
    # tema: o kit decide (THEME_SYNC); remove o boot que le localStorage
    html = re.sub(r'<script[^>]*>\s*\(function\(\)\{try\{var h=document\.documentElement;.*?</script>', '', html, count=1, flags=re.S)
    html = strip_common(html)
    html = rewrite_urls(html, kitdir, app_mode=True)
    pref = "<script>try{localStorage.setItem('ttsc:sub-sidebar:collapsed','%s')}catch(e){}</script>" % ('1' if collapsed else '0')
    # ../bundle.js roda os motores no DOMContentLoaded e repassa a eles os listeners desse evento.
    doc = ('<!doctype html>\n<html lang="pt-BR" dir="ltr" class="h-full bg-slate-50" data-ttsc-theme="true">\n<head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>%s</title>\n' % title + theme_script(theme) + '\n' + pref +
           '\n<!-- CSS/JS do app em uma peca so: assets/css (ordem de $coreStyleAssets em main.php) + assets/js/ttsc.*.js -->\n'
           '<link rel="stylesheet" href="../bundle.css"><script src="../bundle.js"></script>\n'
           '<meta name="ds-theme-sync" content="off">\n' + SLOT_CSS + extra_css + '\n</head>\n'
           '<body class="sb-app h-full bg-slate-50 text-slate-800 font-sans antialiased overflow-hidden flex flex-col">\n' + html + '\n</body>\n</html>\n')
    check_offline(doc, out_name)
    open(os.path.join(kitdir, out_name), 'w', encoding='utf-8').write(doc)
    return doc

# ---------------------------------------------------------------- layouts com <head> proprio (auth, web, portal, erros, e-mail)
PATCHES = [
    # SSE do portal de suporte (GET /support/portal/api/events, caminho absoluto fixo): sem servidor no kit -> desligado.
    ("    es = new EventSource('/support/portal/api/events');",
     "    return; /* Starter Kit: SSE desligado (sem servidor). Real: es = new EventSource('/support/portal/api/events'); */"),
]

def page_kit(src, kitdir, out_name, theme=True, extra_head='', drop=()):
    html = open(src, encoding='utf-8').read()
    for a, b in PATCHES:
        html = html.replace(a, b)
    html = strip_common(html)
    for pat in drop:
        html = re.sub(pat, '', html, flags=re.S)
    html = rewrite_urls(html, kitdir)
    if 'assets/fa.css' in html or 'fa-' in html:
        fa_css(kitdir, html)
        if 'assets/fa.css' not in html:
            extra_head = '<link rel="stylesheet" href="assets/fa.css">' + extra_head
    # banner de cookies (consent-cookie.js) ja decidido, para o kit mostrar a pagina; apague a chave para ver o banner
    consent = "<script>try{localStorage.setItem('ttsc_cookie_consent','accepted_all')}catch(e){}</script>" if 'consent-cookie.js' in html else ''
    inject = theme_script(theme) + consent + extra_head
    html = re.sub(r'<head([^>]*)>', lambda m: '<head' + m.group(1) + '>\n<meta charset="utf-8">' + inject, html, count=1)
    if '<head' not in html:
        raise SystemExit('sem head: ' + src)
    check_offline(html, out_name)
    open(os.path.join(kitdir, out_name), 'w', encoding='utf-8').write(html)
    return html

# ---------------------------------------------------------------- preview
PREVIEW = """<!-- @dsCard group="Starter Kits" height=%(height)d subtitle="%(subtitle)s" -->
<!doctype html>
<html lang="pt-BR">
<head><meta charset="utf-8"><title>%(name)s</title>
<style>
  html, body { height: 100%%; }
  body { margin: 0; display: flex; flex-direction: column; overflow: hidden; background: var(--ttsc-canvas, #f8fafc); font-family: Inter, system-ui, sans-serif; }
  .sk-bar { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; padding: 8px 12px; border-bottom: 1px solid var(--ttsc-border, #e2e8f0); background: var(--ttsc-surface, #fff); color: var(--ttsc-text-2, #475569); font-size: 12px; }
  .sk-bar button { font: inherit; padding: 4px 10px; border-radius: var(--ttsc-radius-sm, 8px); border: 1px solid var(--ttsc-border, #e2e8f0); background: transparent; color: inherit; cursor: pointer; }
  .sk-bar button[aria-pressed="true"] { background: var(--ttsc-accent-soft, #ecfdf5); color: var(--ttsc-accent-text, #047857); border-color: var(--ttsc-accent-border, #a7f3d0); font-weight: 600; }
  .sk-bar button:focus-visible { outline: 2px solid var(--ttsc-accent, #3ecf8e); outline-offset: 1px; }
  .sk-sep { width: 1px; height: 18px; background: var(--ttsc-border, #e2e8f0); margin: 0 4px; }
  .sk-note { margin-left: auto; color: var(--ttsc-text-muted, #64748b); }
  .sk-stage { position: relative; flex: 1 1 auto; min-height: 0; overflow: hidden; background: var(--ttsc-canvas-2, #f1f5f9); }
  .sk-stage iframe { position: absolute; top: 0; left: 0; border: 0; transform-origin: 0 0; background: var(--ttsc-canvas, #f8fafc); box-shadow: 0 0 0 1px var(--ttsc-border, #e2e8f0); }
</style>
</head>
<body>
<div class="sk-bar">
  %(variant_buttons)s
  <span role="group" aria-label="Largura da tela" style="display:contents">%(width_buttons)s</span>
  <span class="sk-note" id="sk-note" aria-live="polite"></span>
</div>
<div class="sk-stage" id="sk-stage"><iframe id="sk-frame" src="%(first)s" title="%(name)s" width="1440" height="900"></iframe></div>
<script>
(function () {
  var stage = document.getElementById('sk-stage'), f = document.getElementById('sk-frame'), note = document.getElementById('sk-note');
  var widths = %(widths_json)s, notes = %(notes_json)s, vnotes = %(vnotes_json)s, w = widths[0], v = %(first_json)s;
  function fit() {
    var s = Math.min(stage.clientWidth / w, 1), h = Math.ceil(stage.clientHeight / s);
    f.style.width = w + 'px'; f.style.height = h + 'px'; f.style.transform = 'scale(' + s + ')';
    f.style.left = Math.max(0, (stage.clientWidth - w * s) / 2) + 'px';
    note.textContent = (vnotes[v] ? vnotes[v] + ' \\u00b7 ' : '') + (notes[w] || '');
  }
  function press(sel, el) { document.querySelectorAll(sel).forEach(function (x) { x.setAttribute('aria-pressed', x === el ? 'true' : 'false'); }); }
  document.querySelectorAll('[data-w]').forEach(function (b) {
    b.addEventListener('click', function () { w = +b.dataset.w; press('[data-w]', b); fit(); });
  });
  document.querySelectorAll('[data-src]').forEach(function (b) {
    b.addEventListener('click', function () { v = b.dataset.src; f.src = v; press('[data-src]', b); fit(); });
  });
  window.addEventListener('resize', fit); fit();
  try { new ResizeObserver(fit).observe(stage); } catch (e) {}
})();
</script>
</body>
</html>
"""

def preview(kitdir, name, variants, height, subtitle, widths=None, notes=None):
    """variants: [(rotulo, arquivo, nota)]."""
    widths = widths or [(1440, 'Desktop 1440'), (1024, 'Tablet 1024'), (390, 'Mobile 390')]
    notes = notes or {1440: 'rail + sub-sidebar fixos (≥ 1100px)', 1024: '≤ 1099px: rail e sub-sidebar viram gaveta (ttsc.shell.js)', 390: 'mobile: gavetas + header compacto'}
    vb = ''
    if len(variants) > 1:
        vb = '<span role="group" aria-label="Variante" style="display:contents">' + ''.join(
            '<button type="button" data-src="%s" aria-pressed="%s">%s</button>' % (f, 'true' if i == 0 else 'false', lbl)
            for i, (lbl, f, _) in enumerate(variants)) + '</span><span class="sk-sep" aria-hidden="true"></span>'
    wb = ''.join('<button type="button" data-w="%d" aria-pressed="%s">%s</button>' % (wd, 'true' if i == 0 else 'false', lbl) for i, (wd, lbl) in enumerate(widths))
    s = PREVIEW % dict(height=height, subtitle=subtitle, name=name, variant_buttons=vb, width_buttons=wb, first=variants[0][1],
                       barh=45, widths_json=json.dumps([w for w, _ in widths]), notes_json=json.dumps({str(k): v for k, v in notes.items()}, ensure_ascii=False),
                       vnotes_json=json.dumps({f: n for _, f, n in variants}, ensure_ascii=False), first_json=json.dumps(variants[0][1]))
    open(os.path.join(kitdir, 'preview.html'), 'w', encoding='utf-8').write(s)

def kitdir(name):
    d = os.path.join(COMP, name)
    os.makedirs(d, exist_ok=True)
    for sub in ('assets', 'api'):
        if os.path.isdir(d + '/' + sub):
            shutil.rmtree(d + '/' + sub)
    for f in os.listdir(d):
        if f.startswith('kit') and f.endswith('.html'):
            os.remove(os.path.join(d, f))
    return d

# ---------------------------------------------------------------- kits
SHELL_SRC = K + '/r_shell_academic_enrollment_re-enrollment.html'  # /academic/enrollment/re-enrollment

def k_app_shell():
    d = kitdir('StarterKitAppShell')
    shell_kit(SHELL_SRC, d, 'kit.html', 'slot', title='Starter Kit — App Shell')
    preview(d, 'StarterKitAppShell', [('Shell', 'kit.html', '')], 640,
            'app/layouts/main.php real: header, rail, sub-sidebar, cabeçalho, banner, abas segmentadas e slot de conteúdo · desktop, tablet e mobile')

def k_app_shell_collapsed():
    d = kitdir('StarterKitAppShellCollapsed')
    shell_kit(SHELL_SRC, d, 'kit.html', 'slot', collapsed=True, title='Starter Kit — App Shell recolhido')
    preview(d, 'StarterKitAppShellCollapsed', [('Recolhido', 'kit.html', '#sub-sidebar.collapsed + botão Menu')], 640,
            'sub-sidebar recolhido (#sub-sidebar.collapsed, localStorage ttsc:sub-sidebar:collapsed=1, Ctrl+B) · só o rail',
            notes={1440: 'rail 60px + conteúdo em largura total', 1024: '≤ 1099px a preferência é ignorada: gavetas', 390: 'mobile: gavetas'})

def k_portal():
    d = kitdir('StarterKitPortalStudent')
    shell_kit(K + '/r_shell_student_next-lessons.html', d, 'kit.html', 'kpi', title='Starter Kit — Portal do Aluno')
    shell_kit(K + '/r_shell_parents_classroom_classes.html', d, 'kit-parents.html', 'kpi', title='Starter Kit — Portal do Responsável')
    shell_kit(K + '/r_shell_teacher_diary_assessments.html', d, 'kit-teacher.html', 'kpi', title='Starter Kit — Portal do Professor')
    shell_kit(K + '/r_shell_thirdparty_delivery_approvals.html', d, 'kit-thirdparty.html', 'kpi', title='Starter Kit — Portal de Terceiros')
    preview(d, 'StarterKitPortalStudent', [('Aluno', 'kit.html', '/student/next-lessons'), ('Responsável', 'kit-parents.html', '/parents/classroom/classes'),
                                           ('Professor', 'kit-teacher.html', '/teacher/diary/assessments'), ('Terceiros', 'kit-thirdparty.html', '/thirdparty/delivery/approvals')], 660,
            'mesmo main.php com o rail de cada portal (student, guardian, teacher, third-party) e a visão KPI real · desktop, tablet e mobile')

def k_auth():
    d = kitdir('StarterKitAuth')
    v = [('Login', 'r_login.html', 'kit.html', 'auth/pages/login.php'),
         ('Login aluno', 'r_auth_login-student.html', 'kit-login-student.html', 'login-student.php'),
         ('Portal', 'r_auth_select-portal.html', 'kit-select-portal.html', 'select-portal.php'),
         ('Entidade', 'r_auth_select-entity.html', 'kit-select-entity.html', 'select-entity.php'),
         ('MFA', 'r_auth_mfa-verify.html', 'kit-mfa-verify.html', 'mfa-verify.php'),
         ('Senha', 'r_auth_forgot-password.html', 'kit-forgot-password.html', 'forgot-password.php')]
    for _, src, out, _n in v:
        page_kit(K + '/' + src, d, out)
    # fixture do GET api/v1/installed (SystemController::installed) chamado por auth.v2.js -> checkInstalledStatus()
    os.makedirs(d + '/api/v1', exist_ok=True)
    open(d + '/api/v1/installed', 'w').write('{"success":true,"installed":true}\n')
    # fixture do GET api/v1/entities (EntityUnitController::entities -> TenantManager::getAccessibleTenants), dados ilustrativos
    open(d + '/api/v1/entities', 'w').write(json.dumps({'success': True, 'data': [
        {'id': '7d1e2c3a-0000-4000-8000-000000000001', 'name': 'Colégio Santa Clara', 'code': 'TNT-00000000001'},
        {'id': '7d1e2c3a-0000-4000-8000-000000000002', 'name': 'Instituto Educacional Vale Verde', 'code': 'TNT-00000000002'},
        {'id': '7d1e2c3a-0000-4000-8000-000000000003', 'name': 'Faculdade São Bento', 'code': 'TNT-00000000003'}]}, ensure_ascii=False))
    preview(d, 'StarterKitAuth', [(a, o, n) for a, _, o, n in v], 640,
            'auth/layouts/main.php real com login, login por perfil, seleção de portal/entidade, MFA e esqueci a senha',
            notes={1440: 'cartão dividido (marca + formulário)', 1024: 'cartão dividido', 390: '≤ 768px: só o formulário'})

def k_error():
    d = kitdir('StarterKitError')
    shell_kit(K + '/r_404.html', d, 'kit.html', 'full', title='Starter Kit — Erro 404')
    shell_kit(K + '/r_500.html', d, 'kit-500.html', 'full', title='Starter Kit — Erro 500')
    page_kit(K + '/r_errgen.html', d, 'kit-generic.html')
    page_kit(REPO + '/resources/views/errors/404.html', d, 'kit-static-404.html')
    preview(d, 'StarterKitError', [('404 no shell', 'kit.html', 'errors/pages/404.php'), ('500 no shell', 'kit-500.html', 'errors/pages/500.php'),
                                   ('Genérico (503)', 'kit-generic.html', 'errors/pages/error.php'), ('Estático 404', 'kit-static-404.html', 'errors/404.html')], 640,
            '404 e 500 dentro do shell (main.php), página genérica errors/pages/error.php e 404.html estático do servidor web',
            notes={1440: 'desktop', 1024: '\u2264 1099px: shell em gavetas', 390: 'mobile'})

def k_public():
    d = kitdir('StarterKitPublicSite')
    page_kit(K + '/r_home.html', d, 'kit.html')
    preview(d, 'StarterKitPublicSite', [('Home', 'kit.html', 'web/pages/home.php')], 680,
            'web/layouts/main.php real com a landing (web/pages/home.php): navbar, hero, módulos, rodapé',
            notes={1440: 'navbar completa', 1024: 'navbar completa', 390: 'menu hambúrguer'})

def k_support():
    d = kitdir('StarterKitSupportPortal')
    page_kit(K + '/r_support.html', d, 'kit.html')
    preview(d, 'StarterKitSupportPortal', [('Meus tickets', 'kit.html', 'support_portal_dashboard.php')], 620,
            'web/layouts/portal.php real com o painel do cliente (support_portal_dashboard.php) · dados ilustrativos em memória',
            notes={1440: 'max-width 1100px', 1024: 'max-width 1100px', 390: 'nav compacta'})

def k_install():
    d = kitdir('StarterKitInstall')
    # install/index.php usa classes claras fixas (bg-white, text-gray-*) sem variante dark: o kit fica sempre claro
    page_kit(K + '/r_install.html', d, 'kit.html', theme='light')
    preview(d, 'StarterKitInstall', [('Instalação', 'kit.html', 'install/index.php')], 680,
            'install/index.php real (formulário único dentro de web/layouts/main.php) · sempre claro',
            notes={1440: 'grid de 2 colunas (md:grid-cols-2)', 1024: 'grid de 2 colunas', 390: '1 coluna'})

PRINT_SCREEN_CSS = """<style>
/* Starter Kit — pré-visualização de impressão: replica na tela as regras @media print reais
   (ttsc.financial-pages.css / pages/standard/module.php) e mostra a folha A4 paisagem. */
html, body { background: #e5e7eb !important; }
body.kit-print-preview aside, body.kit-print-preview nav, body.kit-print-preview header[data-od-id="topnav"], body.kit-print-preview footer,
body.kit-print-preview #floating-actions-container, body.kit-print-preview .print\\:hidden, body.kit-print-preview #domain-tab-toolbar,
body.kit-print-preview #sub-sidebar-expand-btn { display: none !important; }
body.kit-print-preview { overflow: auto !important; display: block !important; }
body.kit-print-preview > .flex-1 { display: block !important; overflow: visible !important; }
body.kit-print-preview #main-viewport { width: 297mm !important; max-width: 100% !important; min-height: 210mm; margin: 16px auto !important; padding: 12mm !important;
  background: #fff !important; color: #000 !important; box-shadow: 0 1px 6px rgba(0,0,0,.18); overflow: visible !important; }
@media print { html, body { background: #fff !important; } body.kit-print-preview #main-viewport { margin: 0 !important; box-shadow: none; padding: 0 !important; } }
</style>"""

PRINT_REPORT_HTML = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Relatório de matrículas 2026/2</title>
<style>
  /* Folha A4 paisagem: a impressão usa @page; na tela, a folha fica centralizada sobre fundo cinza. */
  @page { size: A4 landscape; margin: 12mm 12mm 16mm;
    @bottom-left { content: "TotusTuus SoftCloud · Secretaria Acadêmica"; font: 9px sans-serif; color: #666; }
    @bottom-right { content: "Página " counter(page) " de " counter(pages); font: 9px sans-serif; color: #666; } }
  * { box-sizing: border-box; }
  html { background: #e5e7eb; }
  body { font: 11px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif; color: #111; background: #fff;
    width: 297mm; min-height: 210mm; margin: 16px auto; padding: 12mm; box-shadow: 0 1px 6px rgba(0,0,0,.18); }
  .doc-head { display: grid; grid-template-columns: 1fr auto; gap: 16px; align-items: end; padding-bottom: 10px; border-bottom: 2px solid #111; }
  .brand { display: flex; gap: 10px; align-items: center; }
  .brand-mark { width: 34px; height: 34px; border-radius: 8px; background: #0f766e; color: #fff; display: grid; place-items: center; font-weight: 700; font-size: 14px; }
  .brand b { display: block; font-size: 14px; }
  .brand span { color: #555; font-size: 10px; }
  .doc-meta { text-align: right; color: #444; font-size: 10px; }
  .doc-meta h1 { margin: 0 0 2px; font-size: 17px; color: #111; }
  .filters { display: flex; gap: 6px; flex-wrap: wrap; margin: 10px 0 12px; }
  .chip { border: 1px solid #cfd4dc; border-radius: 999px; padding: 2px 9px; font-size: 10px; color: #333; }
  .chip b { font-weight: 600; }
  .kpis { display: grid; grid-template-columns: repeat(4, 1fr); border: 1px solid #cfd4dc; border-radius: 6px; margin-bottom: 12px; }
  .kpi { padding: 8px 12px; border-right: 1px solid #cfd4dc; }
  .kpi:last-child { border-right: 0; }
  .kpi span { display: block; font-size: 9.5px; text-transform: uppercase; letter-spacing: .05em; color: #555; }
  .kpi b { font-size: 16px; font-variant-numeric: tabular-nums; }
  .kpi small { color: #555; font-size: 10px; }
  table { width: 100%; border-collapse: collapse; }
  thead { display: table-header-group; }
  tr { break-inside: avoid; }
  th { background: #f1f3f6; text-align: left; font-weight: 600; font-size: 10px; color: #333; padding: 6px 8px; border-bottom: 1px solid #111; }
  td { padding: 6px 8px; border-bottom: 1px solid #e3e6eb; font-variant-numeric: tabular-nums; }
  tbody tr:nth-child(even) td { background: #fafbfc; }
  .num { text-align: right; }
  .st { display: inline-block; padding: 1px 7px; border-radius: 999px; font-size: 9.5px; border: 1px solid currentColor; }
  .st-ok { color: #047857; }
  .st-warn { color: #b45309; }
  .st-bad { color: #b91c1c; }
  tfoot td { font-weight: 700; border-top: 1.5px solid #111; border-bottom: 0; padding-top: 8px; }
  .sign { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 36px; break-inside: avoid; }
  .sign div { border-top: 1px solid #111; padding-top: 4px; text-align: center; font-size: 10px; }
  .note { margin-top: 14px; font-size: 9.5px; color: #666; }
  @media print { html { background: #fff; } body { margin: 0; box-shadow: none; width: auto; padding: 0; min-height: 0; } }
</style>
</head>
<body>
  <header class="doc-head">
    <div class="brand">
      <div class="brand-mark" aria-hidden="true">TT</div>
      <div><b>Escola Exemplo</b><span>Secretaria Acadêmica · Unidade Centro</span></div>
    </div>
    <div class="doc-meta">
      <h1>Relatório de matrículas</h1>
      Emitido em 22/10/2026 às 12:23 por Joana Silva
    </div>
  </header>

  <div class="filters" aria-label="Filtros aplicados">
    <span class="chip">Período <b>2026/2</b></span>
    <span class="chip">Unidade <b>Centro</b></span>
    <span class="chip">Situação <b>Todas</b></span>
    <span class="chip">Cursos <b>6 selecionados</b></span>
  </div>

  <section class="kpis" aria-label="Resumo">
    <div class="kpi"><span>Matrículas no período</span><b>1.284</b> <small>100%</small></div>
    <div class="kpi"><span>Ativas</span><b>1.102</b> <small>85,8%</small></div>
    <div class="kpi"><span>Inadimplentes</span><b>61</b> <small>R$ 84.320 em aberto</small></div>
    <div class="kpi"><span>Trancadas</span><b>38</b> <small>3,0%</small></div>
  </section>

  <table>
    <caption style="text-align:left;font-weight:600;padding-bottom:6px">Matrículas listadas</caption>
    <thead>
      <tr>
        <th scope="col">Matrícula</th>
        <th scope="col">Aluno</th>
        <th scope="col">Curso</th>
        <th scope="col">Turma</th>
        <th scope="col">Situação</th>
        <th scope="col" class="num">Mensalidade</th>
        <th scope="col" class="num">Em aberto</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>MAT-2026-0142</td><td>Pedro Henrique Alves</td><td>Engenharia de Software</td><td>3º A</td><td><span class="st st-ok">Ativa</span></td><td class="num">R$ 1.250,00</td><td class="num">R$ 0,00</td></tr>
      <tr><td>MAT-2026-0157</td><td>Ana Beatriz Souza</td><td>Administração</td><td>1º B</td><td><span class="st st-bad">Inadimplente</span></td><td class="num">R$ 980,00</td><td class="num">R$ 980,00</td></tr>
      <tr><td>MAT-2026-0163</td><td>Lucas Ferreira</td><td>Direito</td><td>2º C</td><td><span class="st st-warn">Trancada</span></td><td class="num">R$ 0,00</td><td class="num">R$ 0,00</td></tr>
      <tr><td>MAT-2026-0171</td><td>Marina Oliveira</td><td>Pedagogia</td><td>4º A</td><td><span class="st st-ok">Ativa</span></td><td class="num">R$ 1.100,00</td><td class="num">R$ 0,00</td></tr>
      <tr><td>MAT-2026-0188</td><td>Rafael Lima</td><td>Engenharia Civil</td><td>5º B</td><td><span class="st st-bad">Inadimplente</span></td><td class="num">R$ 1.420,00</td><td class="num">R$ 1.420,00</td></tr>
      <tr><td>MAT-2026-0194</td><td>Joana Costa</td><td>Psicologia</td><td>2º A</td><td><span class="st st-warn">Em atraso</span></td><td class="num">R$ 1.190,00</td><td class="num">R$ 595,00</td></tr>
    </tbody>
    <tfoot>
      <tr><td colspan="5">Total exibido · 6 matrículas</td><td class="num">R$ 6.940,00</td><td class="num">R$ 2.995,00</td></tr>
    </tfoot>
  </table>

  <div class="sign">
    <div>Joana Silva · Secretária acadêmica</div>
    <div>Direção acadêmica</div>
  </div>
  <p class="note">Relatório gerado pelo sistema. Valores em reais, referentes à data de emissão. Dados pessoais: uso restrito à secretaria (LGPD).</p>
</body>
</html>
"""

PRINT_DECLARACAO_HTML = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Declaração de matrícula</title>
<style>
  /* Folha A4 retrato. Documento oficial: timbre, número, código de validação e assinatura. */
  @page { size: A4 portrait; margin: 16mm 18mm 18mm; }
  * { box-sizing: border-box; }
  html { background: #e5e7eb; }
  body { font: 12px/1.6 Georgia, "Times New Roman", serif; color: #111; background: #fff;
    width: 210mm; min-height: 297mm; margin: 16px auto; padding: 16mm 18mm; box-shadow: 0 1px 6px rgba(0,0,0,.18); display: flex; flex-direction: column; }
  .timbre { display: flex; justify-content: space-between; align-items: center; padding-bottom: 10px; border-bottom: 2px solid #111; font-family: system-ui, sans-serif; }
  .timbre b { font-size: 15px; display: block; }
  .timbre span { font-size: 10px; color: #555; }
  .mark { width: 44px; height: 44px; border-radius: 10px; background: #0f766e; color: #fff; display: grid; place-items: center; font: 700 16px system-ui, sans-serif; }
  h1 { font-size: 16px; text-align: center; letter-spacing: .12em; margin: 26px 0 2px; }
  .num { text-align: center; font: 11px system-ui, sans-serif; color: #555; margin: 0 0 24px; }
  p { margin: 0 0 14px; text-align: justify; }
  dl { display: grid; grid-template-columns: 180px 1fr; gap: 6px 12px; margin: 18px 0 22px; font-family: system-ui, sans-serif; font-size: 11px; }
  dt { color: #555; }
  dd { margin: 0; font-weight: 600; }
  .closing { margin-top: 8px; }
  .place { text-align: center; margin: 26px 0 40px; }
  .sign { width: 70%; margin: 0 auto; text-align: center; border-top: 1px solid #111; padding-top: 6px; font: 11px system-ui, sans-serif; }
  .sign small { display: block; color: #555; }
  .verify { margin-top: auto; display: grid; grid-template-columns: 1fr 84px; gap: 14px; align-items: center; border: 1px solid #cfd4dc; border-radius: 6px; padding: 12px 14px;
    font: 10px/1.5 system-ui, sans-serif; color: #333; }
  .verify b { font-family: ui-monospace, Menlo, monospace; font-size: 12px; letter-spacing: .08em; color: #111; }
  .qr { width: 84px; height: 84px; border: 1px dashed #888; display: grid; place-items: center; font: 10px system-ui, sans-serif; color: #666; }
  @media print { html { background: #fff; } body { margin: 0; box-shadow: none; width: auto; padding: 0; min-height: 0; } }
</style>
</head>
<body>
  <header class="timbre">
    <div style="display:flex;gap:12px;align-items:center"><div class="mark" aria-hidden="true">TT</div><div><b>Escola Exemplo</b><span>Secretaria Acadêmica · Rua das Flores, 120 · Centro</span></div></div>
    <span>CNPJ 00.000.000/0001-00</span>
  </header>

  <h1>DECLARAÇÃO DE MATRÍCULA</h1>
  <p class="num">Nº 2026/0412 · emitida em 22/10/2026</p>

  <p>A Secretaria Acadêmica da Escola Exemplo declara, para os devidos fins, que <strong>Ana Beatriz Souza</strong>, portadora do CPF ***.***.***-21, encontra-se regularmente matriculada no curso de Administração, no período letivo 2026/2, conforme os dados abaixo.</p>

  <dl>
    <dt>Número da matrícula</dt><dd>MAT-2026-0157</dd>
    <dt>Curso</dt><dd>Administração (bacharelado)</dd>
    <dt>Série e turma</dt><dd>1º ano, turma B</dd>
    <dt>Turno</dt><dd>Matutino</dd>
    <dt>Período letivo</dt><dd>2026/2</dd>
    <dt>Início da matrícula</dt><dd>01/08/2026</dd>
    <dt>Situação</dt><dd>Ativa</dd>
  </dl>

  <p class="closing">Por ser verdade, firmamos a presente declaração, que não gera direito a nenhum benefício além do expressamente informado.</p>

  <p class="place">Centro, 22 de outubro de 2026.</p>

  <div class="sign">Joana Silva<small>Secretária acadêmica · Registro 1234</small></div>

  <section class="verify" aria-label="Validação do documento">
    <div>
      Para conferir a autenticidade, acesse <b>escola.exemplo/validar</b> e informe o código:<br>
      <b>7F3K-9QWD-2X8M</b><br>
      O código vale enquanto a matrícula estiver ativa. Dados pessoais protegidos pela LGPD.
    </div>
    <div class="qr" role="img" aria-label="QR code de validação">QR</div>
  </section>
</body>
</html>
"""

def k_print():
    d = kitdir('StarterKitPrint')
    # (1) relatório tabular institucional, A4 paisagem: marca, filtros, indicadores, tabela com cabeçalho repetido, totais e assinaturas
    open(d + '/kit.html', 'w', encoding='utf-8').write(PRINT_REPORT_HTML)
    # (2) declaração oficial, A4 retrato: timbre, número, dados, código de validação e assinatura
    open(d + '/kit-declaracao.html', 'w', encoding='utf-8').write(PRINT_DECLARACAO_HTML)
    # (3) página do app com as regras de impressão aplicadas (sem header, rail, sub-sidebar, abas e rodapé)
    # papel é sempre claro: a pré-visualização de impressão ignora o tema do preview
    doc = shell_kit(SHELL_SRC, d, 'kit-app.html', 'kpi', title='Starter Kit — Impressão do app', extra_css=PRINT_SCREEN_CSS, theme='light')
    doc = doc.replace('<body class="sb-app', '<body class="kit-print-preview sb-app', 1)
    open(d + '/kit-app.html', 'w', encoding='utf-8').write(doc)
    preview(d, 'StarterKitPrint', [('Relatório (A4 paisagem)', 'kit.html', 'relatório institucional: filtros, indicadores, tabela e assinaturas'),
                                   ('Declaração oficial (A4 retrato)', 'kit-declaracao.html', 'documento com timbre, número e código de validação'),
                                   ('Página do app impressa', 'kit-app.html', '@media print do app')], 660,
            'modelos de impressão: relatório institucional, declaração oficial com validação e página do app com @media print',
            widths=[(1440, 'Tela 1440'), (1024, 'Tela 1024')], notes={1440: 'folha A4 (297 mm paisagem ou 210 mm retrato)', 1024: 'a folha encolhe com max-width 100%'})


def k_email():
    d = kitdir('StarterKitEmail')
    for src, out in [('r_mail_new_message.html', 'kit.html'), ('r_mail_sla_breach.html', 'kit-sla.html'), ('r_mail_dsr.html', 'kit-dsr.html')]:
        page_kit(K + '/' + src, d, out, theme=False)
    preview(d, 'StarterKitEmail', [('SAC: nova mensagem', 'kit.html', 'emails/sac/layout.php + new_message.php'),
                                   ('SAC: SLA', 'kit-sla.html', 'emails/sac/layout.php + sla_breach.php'),
                                   ('LGPD: DSR', 'kit-dsr.html', 'emails/dsr_notification.php')], 640,
            'layout de e-mail real (emails/sac/layout.php, 600px, CSS no <style> do head) e dsr_notification.php · sempre claro',
            widths=[(1440, 'Webmail 1440'), (390, 'Celular 390')], notes={1440: 'contêiner 600px centralizado', 390: 'contêiner fluido (max-width 600px)'})

KITS = {'StarterKitAppShell': k_app_shell, 'StarterKitAppShellCollapsed': k_app_shell_collapsed, 'StarterKitPortalStudent': k_portal,
        'StarterKitAuth': k_auth, 'StarterKitError': k_error, 'StarterKitPublicSite': k_public, 'StarterKitSupportPortal': k_support,
        'StarterKitInstall': k_install, 'StarterKitPrint': k_print, 'StarterKitEmail': k_email}

if __name__ == '__main__':
    for n in (sys.argv[1:] or list(KITS)):
        KITS[n]()
        print('ok', n)
