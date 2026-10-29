"""Gera references/componentes.md a partir dos README de um design system.

Uso: python3 gera_indice.py <pasta-do-design-system> <saida.md>
A pasta do DS deve ter uma subpasta por componente, cada uma com README.md.
"""
import os, re, sys

DS, OUT = sys.argv[1], sys.argv[2]


def resumo(md):
    corpo = re.sub(r'^#\s+.*\n', '', md, count=1)
    for bloco in re.split(r'\n\s*\n', corpo):
        b = bloco.strip()
        if b and not b.startswith(('#', '|', '```', '-', '*', '>', '<')):
            return re.sub(r'\s+', ' ', b)[:220].replace('|', '/')
    return ''


linhas = ['# Índice de componentes', '', f'Gerado a partir de `{DS}`. Não editar à mão.', '',
          '| Componente | Para que serve | Documentação |', '|---|---|---|']
for nome in sorted(os.listdir(DS), key=str.lower):
    readme = os.path.join(DS, nome, 'README.md')
    if not os.path.isfile(readme):
        continue
    md = open(readme, encoding='utf8').read()
    titulo = re.search(r'^#\s+(.+)', md, re.M)
    linhas.append(f"| {titulo.group(1).strip() if titulo else nome} | {resumo(md)} | `{nome}/README.md` |")

open(OUT, 'w', encoding='utf8').write('\n'.join(linhas) + '\n')
print('componentes:', len(linhas) - 5)
