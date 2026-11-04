"""Gera inventario/inventario-paginas.md a partir da seção 2 de docs/31-matriz-portais-modulos.md.

Uso: python3 inventario/gera_inventario.py
Saída: portal -> área -> módulos (com escopo e referência do SDD). Telas individuais são detalhadas por módulo, depois.
"""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MATRIZ = os.path.join(ROOT, 'docs', '31-matriz-portais-modulos.md')
SAIDA = os.path.join(ROOT, 'inventario', 'inventario-paginas.md')

linhas = open(MATRIZ, encoding='utf8').read().splitlines()
inicio = next(i for i, l in enumerate(linhas) if l.startswith('## 2. Matriz por portal'))
fim = next(i for i, l in enumerate(linhas) if l.startswith('## 3. Fronteiras'))
portal = None
saida = ['# Inventário de telas por portal', '',
         'Gerado por `inventario/gera_inventario.py` a partir de `docs/31-matriz-portais-modulos.md`, seção 2.',
         'Nível: portal → área → módulo. As telas de cada módulo são detalhadas antes de implementar.', '']
total = 0
for l in linhas[inicio:fim]:
    m = re.match(r'### (2\.\d) (.+)', l)
    if m:
        portal = m.group(2).strip()
        saida += [f'## {m.group(1)} {portal}', '']
        continue
    if portal and l.startswith('|') and not l.startswith('| Área') and not re.match(r'\|\s*-', l):
        celulas = [c.strip() for c in l.strip().strip('|').split('|')]
        area = celulas[0]
        modulos = celulas[1]
        escopo = celulas[-1] if len(celulas) >= 3 else ''
        itens = [x.strip() for x in modulos.split(', ') if x.strip()]
        total += len(itens)
        saida += [f'### {area}', '', f'Escopo: {escopo}', '']
        saida += [f'- [ ] {x}' for x in itens]
        saida.append('')

saida.insert(4, f'Total de módulos listados: {total}. Status inicial: nenhum implementado.\n')
open(SAIDA, 'w', encoding='utf8').write('\n'.join(saida) + '\n')
print('módulos:', total)
