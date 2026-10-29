"""Gera o site de documentação (estilo ktui.io) a partir do design system em <projeto>.
Uso: gen_site.py <projeto> <saida>"""
import os, re, sys, json, shutil
P, O = sys.argv[1], sys.argv[2]
if os.path.exists(O + '/components'): shutil.rmtree(O + '/components')
os.makedirs(O, exist_ok=True)
BLOBS = {'7dea5e7432b0eec9f13a5acc991fc877': 'ckeditor5-classic-41.4.2.js'}
ORDER = ['Componentes', 'Navegação', 'Formulários', 'Base', 'Formulários · Plugins', 'Editores', 'Gráficos', 'Componentes do painel', 'Geral',
         'Modelos', 'Starter Kits', 'Arquétipos de página', 'Widgets', 'Outros']

def split_readme(md):
    """Separa o README em visão geral, API e os modelos HTML/CSS/JS/SQL."""
    md = md.replace('\r\n', '\n')
    title = re.match(r'#\s+(.+)', md)
    body = md[title.end():] if title else md
    parts = re.split(r'(?m)^##\s+', body)
    head, sections = parts[0], parts[1:]
    out = {'overview': head.strip(), 'api': '', 'html': '', 'css': '', 'js': '', 'sql': '', 'extra': ''}
    rest = []
    for s in sections:
        name, _, content = s.partition('\n')
        key = name.strip().lower()
        if key.startswith('api'):
            out['api'] += content.strip() + '\n'
        elif key.startswith('modelos'):
            subs = re.split(r'(?m)^###\s+', content)
            if subs[0].strip(): rest.append('## ' + name + '\n' + subs[0])
            for sub in subs[1:]:
                sname, _, scontent = sub.partition('\n')
                k = sname.strip().lower()
                k = 'js' if k.startswith(('js', 'javascript')) else 'html' if k.startswith(('html', 'php')) else 'css' if k.startswith('css') else 'sql' if k.startswith('sql') else None
                if k: out[k] += scontent.strip() + '\n\n'
                else: rest.append('### ' + sub)
        else:
            rest.append('## ' + s)
    # a primeira frase vira o resumo do topo e "Também listado em" vira chip: não repetir na visão geral
    lead = [p for p in re.split(r'\n\s*\n', out['overview'].strip()) if p.strip()]
    lead = [p for p in lead if not p.lstrip().startswith('> Também listado')]
    if lead and not lead[0].lstrip().startswith(('#', '|', '-', '>', '`')): lead = lead[1:]
    out['overview'] = ('\n\n'.join(lead) + '\n\n' + '\n\n'.join(rest)).strip()
    return (title.group(1).strip() if title else ''), out

def summary_of(text):
    for line in text.split('\n'):
        l = line.strip()
        if l and not l.startswith(('#', '>', '|', '-', '`')):
            m = re.match(r'(.+?[.!?])(\s|$)', l)
            return (m.group(1) if m else l)
    return ''

def tokens_css():
    t = json.load(open(P + '/tokens.json'))
    themes = [x['id'] for x in t['color']['themes']]
    def val(tok, th):
        v = tok['value']
        if isinstance(v, str): return v if th == themes[0] else None
        return v.get(th)
    css = []
    for th in themes:
        sel = ':root, [data-theme="%s"]' % th if th == themes[0] else '[data-theme="%s"]' % th
        lines = ['--%s:%s;' % (tok['name'], val(tok, th)) for tok in t['color']['tokens'] if val(tok, th)]
        if th == themes[0]:
            lines += ['--%s:%s;' % (tok['name'], tok['value']) for tok in t.get('shadow', {}).get('tokens', [])]
        css.append(sel + '{' + ''.join(lines) + '}')
    lines = []
    for fam, d in t.items():
        if fam in ('color', 'type', 'shadow', 'name', 'version', 'meta'): continue
        lines += ['--%s:%s;' % (tok['name'], tok['value']) for tok in d['tokens']]
    lines += ['--font-%s:%s;' % (k, v) for k, v in t['type']['families'].items()]
    css.append(':root{' + ''.join(lines) + '}')
    return '/* TotusTuus SoftCloud — gerado de tokens.json */\n' + '\n'.join(css) + '\n'

# arquivos estáticos
for d in ('vendor', 'fonts', 'models'):
    if os.path.exists(O + '/' + d): shutil.rmtree(O + '/' + d)
    if os.path.exists(P + '/' + d): shutil.copytree(P + '/' + d, O + '/' + d)
os.makedirs(O + '/vendor/blob', exist_ok=True)
for bid, name in BLOBS.items():
    shutil.copy(P + '/_blob/' + bid, O + '/vendor/blob/' + name)
os.makedirs(O + '/components', exist_ok=True)
for f in ('bundle.css', 'bundle.js'):
    shutil.copy(P + '/components/' + f, O + '/components/' + f)
open(O + '/components/tokens.css', 'w', encoding='utf-8').write(tokens_css())

items = []
for c in sorted(os.listdir(P + '/components')):
    d = P + '/components/' + c
    if not os.path.isdir(d) or not os.path.exists(d + '/preview.html') or c == 'Cover': continue
    prev = open(d + '/preview.html', encoding='utf-8').read()
    m = re.match(r'<!--\s*@dsCard(.*?)-->', prev, re.S)  # o subtítulo pode conter '>' (ex.: '> 6 opções')
    meta = m.group(1) if m else ''
    group = (re.search(r'group="([^"]*)"', meta) or [None, 'Outros'])[1]
    height = int((re.search(r'height=(\d+)', meta) or [None, '360'])[1])
    width = int((re.search(r'width=(\d+)', meta) or [None, '0'])[1])
    subtitle = (re.search(r'subtitle="([^"]*)"', meta) or [None, ''])[1]
    for bid, name in BLOBS.items():
        prev = prev.replace('/_blob/' + bid, '../../vendor/blob/' + name)
    head = '<link rel="stylesheet" href="../tokens.css"><link rel="stylesheet" href="../bundle.css"><script src="../bundle.js"></script>'
    if re.search(r'<head[^>]*>', prev): frame = re.sub(r'(<head[^>]*>)', lambda mm: mm.group(1) + head, prev, count=1)
    else: frame = '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">' + head + '</head><body>' + prev + '</body></html>'
    frame = re.sub(r'<html([^>]*)>', lambda mm: '<html' + re.sub(r'\sdata-theme="[^"]*"', '', mm.group(1)) + ' data-theme="light">', frame, count=1)
    if '<!doctype' not in frame[:300].lower(): frame = '<!doctype html>\n' + frame
    # arquivos irmaos do preview (kit*.html, shell.html, assets/) que ele carrega por caminho relativo
    shutil.copytree(d, O + '/components/' + c, dirs_exist_ok=True, ignore=shutil.ignore_patterns('preview.html'))
    open(O + '/components/' + c + '/preview.html', 'w', encoding='utf-8').write(frame)
    readme = open(d + '/README.md', encoding='utf-8').read() if os.path.exists(d + '/README.md') else '# ' + c + '\n\nDocumentação em preparação.'
    title, secs = split_readme(readme)
    first = readme.split('\n', 1)[1] if readme.startswith('#') else readme
    also = re.search(r'>\s*Também listado em:\s*(.+)', readme)
    items.append({'id': c, 'title': title or c, 'group': group, 'summary': summary_of(first), 'subtitle': subtitle,
                  'also': also.group(1).strip() if also else '', 'height': height, 'width': width, 'sections': secs})
items.sort(key=lambda x: (ORDER.index(x['group']) if x['group'] in ORDER else 99, x['title'].lower()))
docs = {'readme': open(P + '/README.md', encoding='utf-8').read(),
        'inventory': open(P + '/Inventario.md', encoding='utf-8').read() if os.path.exists(P + '/Inventario.md') else '',
        'tokens': json.load(open(P + '/tokens.json')), 'groups': ORDER, 'items': items}
data = json.dumps(docs, ensure_ascii=False)
open(O + '/docs.json', 'w', encoding='utf-8').write(data)
open(O + '/.htaccess', 'w', encoding='utf-8').write(
    '# Gerado por gen_site.py — o catálogo local revalida com o servidor a cada visita\n'
    '<IfModule mod_headers.c>\n'
    '  <Files "docs.json">\n'
    '    Header set Cache-Control "no-cache"\n'
    '  </Files>\n'
    '</IfModule>\n')
print(len(items), 'items;', round(len(data) / 1024), 'KB docs.json')
