"""Cria a estrutura do kit inicial do Portal do Desenvolvedor a partir de inventario/inventario-paginas.md.

Uso: python3 kit-starter/gera_kit.py
Gera kit-starter/desenvolvedor/<area>/<modulo>.md (um arquivo por módulo, status "pendente").
Não cria telas: elas são detalhadas e aprovadas módulo a módulo.
"""
import os, re, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INV = os.path.join(ROOT, 'inventario', 'inventario-paginas.md')
DEST = os.path.join(ROOT, 'kit-starter', 'desenvolvedor')


def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


linhas = open(INV, encoding='utf8').read().splitlines()
ini = next(i for i, l in enumerate(linhas) if l.startswith('## 2.1 '))
fim = next(i for i, l in enumerate(linhas) if l.startswith('## 2.2 '))
area = None
escopo = ''
total = 0
for l in linhas[ini + 1:fim]:
    if l.startswith('### '):
        area = l[4:].strip()
        escopo = ''
        os.makedirs(os.path.join(DEST, slug(area)), exist_ok=True)
    elif l.startswith('Escopo: '):
        escopo = l[len('Escopo: '):].strip()
    elif l.startswith('- [ ] ') and area:
        modulo = l[6:].strip()
        caminho = os.path.join(DEST, slug(area), slug(modulo) + '.md')
        if os.path.exists(caminho) and 'Status: pendente' not in open(caminho, encoding='utf8').read():
            continue  # ficha já detalhada: não sobrescrever
        rel = os.path.relpath(os.path.join(ROOT, 'docs', 'v2'), os.path.dirname(caminho)).replace(os.sep, '/')
        escopo_ficha = escopo.replace('](../docs/v2/', f']({rel}/')
        open(caminho, 'w', encoding='utf8').write(
            f'# {modulo}\n\n'
            f'- Portal: Desenvolvedor (`desenvolvedor.`)\n'
            f'- Área: {area}\n'
            f'- Escopo: {escopo_ficha}\n'
            f'- Status: pendente (telas por detalhar)\n\n'
            '## Telas\n\n_A definir e aprovar antes da implementação._\n\n'
            '## Referências no SDD\n\n- `docs/31-matriz-portais-modulos.md`, seção 2.1\n')
        total += 1
print('módulos criados:', total)
