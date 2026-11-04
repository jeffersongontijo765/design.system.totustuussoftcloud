"""Cria a estrutura do kit inicial de todos os portais a partir de inventario/inventario-paginas.md.

Uso: python3 kit-starter/gera_kit.py
Gera kit-starter/<portal>/<area>/<modulo>.md (um arquivo por módulo, status "pendente").
Não cria telas: elas são detalhadas e aprovadas módulo a módulo.
"""
import os, re, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INV = os.path.join(ROOT, 'inventario', 'inventario-paginas.md')
DEST = os.path.join(ROOT, 'kit-starter', 'desenvolvedor')


def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


POR_AREA = {'2.3', '2.4', '2.5', '2.6'}  # portais de uso pessoal: uma ficha por área, módulos viram telas
PASTAS = {'2.1': 'desenvolvedor', '2.2': 'gestao', '2.3': 'professor', '2.4': 'aluno', '2.5': 'responsaveis', '2.6': 'terceiros'}

linhas = open(INV, encoding='utf8').read().splitlines()
area = escopo = portal = sec = pasta = None
total = 0
for l in linhas:
    m = re.match(r'## (2\.\d) (.+)', l)
    if m:
        sec, pasta = m.group(1), PASTAS[m.group(1)]
        portal = m.group(2).split(' — ')[0].replace('Portal do ', '').replace('Portal de ', '').replace('Portal dos ', '')
        area = None
        continue
    if not pasta:
        continue
    if l.startswith('### '):
        area = l[4:].strip()
        escopo = ''
        os.makedirs(os.path.join(ROOT, 'kit-starter', pasta) if sec in POR_AREA else os.path.join(ROOT, 'kit-starter', pasta, slug(area)), exist_ok=True)
    elif l.startswith('Escopo: '):
        escopo = l[len('Escopo: '):].strip()
    elif l.startswith('- [ ] ') and area and sec in POR_AREA:
        caminho = os.path.join(ROOT, 'kit-starter', pasta, slug(area) + '.md')
        if os.path.exists(caminho):
            t = open(caminho, encoding='utf8').read()
            if 'Status: pendente' in t and l[6:].strip() not in t:
                open(caminho, 'a', encoding='utf8').write(f'- {l[6:].strip()}\n')
            continue
        rel = os.path.relpath(os.path.join(ROOT, 'docs', 'v2'), os.path.dirname(caminho)).replace(os.sep, '/')
        escopo_ficha = escopo.replace('](../docs/v2/', f']({rel}/')
        escopo_ficha = re.sub(r'\]\((\d\d-)', f']({rel}/\\1', escopo_ficha)
        open(caminho, 'w', encoding='utf8').write(
            f'# {area}\n\n- Portal: {portal}\n- Escopo: {escopo_ficha}\n- Status: pendente (telas por detalhar)\n'
            f'- Referência: [31]({rel}/31-matriz-portais-modulos.md), seção {sec}\n\n## Módulos\n\n- {l[6:].strip()}\n')
        total += 1
    elif l.startswith('- [ ] ') and area:
        modulo = l[6:].strip()
        caminho = os.path.join(ROOT, 'kit-starter', pasta, slug(area), slug(modulo)[:60].strip('-') + '.md')
        if os.path.exists(caminho) and 'Status: pendente' not in open(caminho, encoding='utf8').read():
            continue  # ficha já detalhada: não sobrescrever
        rel = os.path.relpath(os.path.join(ROOT, 'docs', 'v2'), os.path.dirname(caminho)).replace(os.sep, '/')
        escopo_ficha = escopo.replace('](../docs/v2/', f']({rel}/')
        open(caminho, 'w', encoding='utf8').write(
            f'# {modulo[0].upper() + modulo[1:]}\n\n'
            f'- Portal: {portal}\n'
            f'- Área: {area}\n'
            f'- Escopo: {escopo_ficha}\n'
            f'- Status: pendente (telas por detalhar)\n\n'
            '## Telas\n\n_A definir e aprovar antes da implementação._\n\n'
            f'## Referências no SDD\n\n- [31]({rel}/31-matriz-portais-modulos.md), seção {sec}\n')
        total += 1
print('módulos criados:', total)
