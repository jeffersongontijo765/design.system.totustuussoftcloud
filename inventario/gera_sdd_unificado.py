"""Gera docs/SDD-UNIFICADO.md: o texto integral da v2 e da v1 em um único arquivo.

Uso: python3 inventario/gera_sdd_unificado.py
- Parte 1: SDD v2 (docs/v2/SDD-COMPLETO.md, gerado a partir dos 81 documentos numerados).
- Parte 2: especificações da v1 (docs/v2/anexo-v1/, 62 arquivos), uma seção por arquivo,
  com os títulos rebaixados para ficar abaixo da seção da parte.
- Nada é reescrito à mão: o arquivo é a concatenação dos fontes.
Não editar à mão: regere depois de mudar a v1 ou a v2.
"""
import datetime, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
V2 = os.path.join(ROOT, 'docs', 'v2')
ANEXO = os.path.join(V2, 'anexo-v1')
V2_COMPLETO = os.path.join(V2, 'SDD-COMPLETO.md')
SAIDA = os.path.join(ROOT, 'docs', 'SDD-UNIFICADO.md')


def rebaixa(texto, niveis):
    """Acrescenta `niveis` # aos títulos fora de blocos de código (limite de 6)."""
    saida, em_codigo = [], False
    for linha in texto.splitlines():
        if linha.lstrip().startswith('```'):
            em_codigo = not em_codigo
        m = re.match(r'^(#{1,6}) ', linha)
        if not em_codigo and m:
            linha = '#' * min(6, len(m.group(1)) + niveis) + linha[len(m.group(1)):]
        saida.append(linha)
    return '\n'.join(saida)


def sem_cabecalho(texto):
    """Remove a primeira linha de título (é repetida pelo cabeçalho da parte)."""
    linhas = texto.splitlines()
    if linhas and linhas[0].startswith('# '):
        linhas = linhas[1:]
    return '\n'.join(linhas).strip()


def main():
    v2 = sem_cabecalho(open(V2_COMPLETO, encoding='utf8').read())
    anexos = sorted(f for f in os.listdir(ANEXO) if os.path.isfile(os.path.join(ANEXO, f)))
    partes_v1 = []
    for nome in anexos:
        caminho = os.path.join(ANEXO, nome)
        try:
            texto = open(caminho, encoding='utf8').read()
        except UnicodeDecodeError:
            texto = open(caminho, encoding='latin-1').read()
        titulo = nome
        partes_v1.append((nome, len(texto.splitlines()), rebaixa(texto.strip(), 2)))
    hoje = datetime.date.today().isoformat()
    cab = [
        '# SDD unificado: v1 e v2',
        '',
        f'Gerado em {hoje} por `inventario/gera_sdd_unificado.py`. Não editar à mão.',
        '',
        f'- Parte 1: SDD v2, {v2.count(chr(10) + "## ") + 1 if v2 else 0} seções de nível 2, a partir dos 81 documentos numerados.',
        f'- Parte 2: especificações da v1, {len(partes_v1)} arquivos de `docs/v2/anexo-v1/`.',
        '- Para a situação de cada arquivo da v1 na v2, ver a seção 2 do documento 79 (dentro da parte 1).',
        '',
        '## Índice',
        '',
        '### Parte 1 — SDD v2',
        '',
        '- [SDD v2 completo](#parte-1-sdd-v2)',
        '',
        '### Parte 2 — Especificações da v1',
        '',
    ]
    for nome, linhas, _ in partes_v1:
        ancora = re.sub(r'[^a-z0-9]+', '-', nome.lower()).strip('-')
        cab.append(f'- [{nome}](#v1-{ancora}) ({linhas} linhas)')
    cab += ['', '---', '', '# Parte 1 — SDD v2', '', v2, '', '---', '', '# Parte 2 — Especificações da v1', '']
    corpo = []
    for nome, linhas, texto in partes_v1:
        ancora = re.sub(r'[^a-z0-9]+', '-', nome.lower()).strip('-')
        corpo.append(f'<a id="v1-{ancora}"></a>\n\n## v1 — `{nome}`\n\n{texto}\n')
    saida = '\n'.join(cab) + '\n' + '\n'.join(corpo)
    open(SAIDA, 'w', encoding='utf8').write(saida)
    print('gerado:', os.path.relpath(SAIDA, ROOT), len(saida.splitlines()), 'linhas,', len(saida.encode('utf8')) // 1024, 'KB')


if __name__ == '__main__':
    main()
