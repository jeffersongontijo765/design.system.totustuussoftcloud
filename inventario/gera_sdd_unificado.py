"""Gera docs/SDD-UNIFICADO.md: v2 e v1 organizadas por documento da v2.

Uso: python3 inventario/gera_sdd_unificado.py

Estrutura:
- Índice: uma entrada por documento da v2 (00 a 80), com as especificações da v1 que ele absorveu.
- Para cada documento da v2: o texto integral dele e, logo abaixo, o texto integral de cada
  especificação da v1 que ele absorveu (segundo a seção 3 do documento 79).
- Cada especificação da v1 aparece uma única vez, no primeiro documento da v2 que a absorve.
  Nos demais, aparece um link para ela.
- No fim: especificações absorvidas no kit-starter, substituídas em bloco, fora do escopo e vazias.

Nada é reescrito à mão: o arquivo é montado a partir dos fontes e do documento 79.
Não editar à mão: regere depois de mudar a v1, a v2 ou o documento 79.
"""
import datetime, glob, os, re, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
V2 = os.path.join(ROOT, 'docs', 'v2')
ANEXO = os.path.join(V2, 'anexo-v1')
RASTREIO = os.path.join(V2, '79-rastreabilidade-v1-v2.md')
SAIDA = os.path.join(ROOT, 'docs', 'SDD-UNIFICADO.md')


def ancora(texto):
    t = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


V1_NOMES = set()


def desvincula(texto):
    """Nenhum link aponta para fora do arquivo: documentos viram âncoras, caminhos do repositório viram texto.

    - link para documento da v2 (NN-*.md) -> âncora do documento;
    - link para arquivo da v1 (anexo-v1/ ou nome direto) -> âncora da especificação;
    - link para caminho do repositório (kit-starter/, docs/, ../) -> só o texto;
    - link http(s) e âncora interna (#...) -> mantidos.
    """
    def troca(m):
        rotulo, alvo = m.group(1), m.group(2).strip()
        if alvo.startswith(('http://', 'https://', 'mailto:')) or alvo.startswith('#'):
            return m.group(0)
        base = os.path.basename(alvo.split('#')[0])
        mm = re.match(r'^(\d\d)-', base)
        if mm and base.endswith('.md') and mm.group(1) in NUMEROS_V2:
            return f'[{rotulo}](#doc-{mm.group(1)})'
        if base in V1_NOMES:
            return f'[{rotulo}](#v1-{ancora(base)})'
        return rotulo
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', troca, texto)


def rebaixa(texto, niveis, teto=6):
    saida, em_codigo = [], False
    for linha in texto.splitlines():
        if linha.lstrip().startswith('```'):
            em_codigo = not em_codigo
        m = re.match(r'^(#{1,6}) ', linha)
        if not em_codigo and m:
            linha = '#' * min(teto, len(m.group(1)) + niveis) + linha[len(m.group(1)):]
        saida.append(linha)
    return '\n'.join(saida)


def sem_titulo(texto):
    linhas = texto.splitlines()
    if linhas and linhas[0].startswith('# '):
        linhas = linhas[1:]
    return '\n'.join(linhas).strip()


def le(caminho):
    try:
        return open(caminho, encoding='utf8').read()
    except UnicodeDecodeError:
        return open(caminho, encoding='latin-1').read()


def docs_v2():
    """Lista (NN, caminho, título) dos documentos numerados da v2."""
    saida = []
    for c in sorted(glob.glob(os.path.join(V2, '[0-9][0-9]-*.md'))):
        n = os.path.basename(c)[:2]
        t = le(c).splitlines()[0].lstrip('# ').strip() if le(c).strip() else n
        t = re.sub(r'^' + n + r'\s*[—-]\s*', '', t)
        saida.append((n, c, t))
    return saida


def mapeamento():
    """Lê a seção 3 do documento 79: para cada arquivo da v1, situação e destino."""
    itens = []  # (arquivo, linhas, situação, [NN...], [caminho do kit])
    numeros_v2 = {os.path.basename(c)[:2] for c in glob.glob(os.path.join(V2, '[0-9][0-9]-*.md'))}
    for linha in le(RASTREIO).splitlines():
        m = re.match(r'^\| \[`([^`]+)`\]\(anexo-v1/[^)]+\) \| (\d+) \| ([^|]+) \| ([^|]+) \|', linha)
        if not m:
            continue
        arq, linhas, situacao, destino = m.group(1), int(m.group(2)), m.group(3).strip(), m.group(4).strip()
        nums = [n for n in re.findall(r'\b(\d\d)\b', destino) if n in numeros_v2]
        kit = re.findall(r'kit-starter/[^\s`\)]+\.md', destino)
        itens.append((arq, linhas, situacao, nums, kit))
    return itens


NUMEROS_V2 = set()


def main():
    global NUMEROS_V2
    docs = docs_v2()
    NUMEROS_V2 = {n for n, _, _ in docs}
    V1_NOMES.update(os.listdir(ANEXO))
    itens = mapeamento()
    v1_por_doc = {n: [] for n, _, _ in docs}
    colocado = set()
    grupos = {'kit': [], 'substituido': [], 'fora': [], 'vazio': [], 'nao_classificado': []}
    for arq, linhas, situacao, nums, kit in itens:
        if kit:
            grupos['kit'].append((arq, linhas, situacao, kit))
            continue
        if 'Fora do escopo' in situacao or 'Removido' in situacao:
            grupos['fora'].append((arq, linhas, situacao, []))
            continue
        if 'vazio' in situacao.lower():
            grupos['vazio'].append((arq, linhas, situacao, []))
            continue
        if not nums:
            grupos['nao_classificado'].append((arq, linhas, situacao, []))
            continue
        alvo = nums[0]
        v1_por_doc[alvo].append((arq, linhas, situacao, nums))
        colocado.add(arq)

    def bloco_v1(arq, linhas, situacao, outros):
        caminho = os.path.join(ANEXO, arq)
        texto = rebaixa(desvincula(le(caminho).strip()), 3) if os.path.isfile(caminho) else '_Arquivo ausente._'
        return (f'<a id="v1-{ancora(arq)}"></a>\n\n#### v1 — `{arq}` ({linhas} linhas)\n\n'
                f'*Situação na v2: {situacao}.*\n\n{texto}\n')

    hoje = datetime.date.today().isoformat()
    indice = [
        '# SDD unificado: v1 e v2',
        '',
        f'Gerado em {hoje} por `inventario/gera_sdd_unificado.py`. Não editar à mão.',
        '',
        'Cada documento da v2 vem com as especificações da v1 que ele absorveu, logo abaixo do texto dele. '
        'A situação de cada arquivo da v1 está na seção 3 do [79](#doc-79).',
        '',
        '## Índice',
        '',
    ]
    for n, _, t in docs:
        indice.append(f'- [{n} — {t}](#doc-{n})')
        for arq, linhas, situacao, nums in v1_por_doc[n]:
            indice.append(f'  - [v1 `{arq}`](#v1-{ancora(arq)}) — {situacao.lower()}')
    indice += ['', '- [Especificações v1 absorvidas no kit-starter (texto integral)](#v1-no-kit)',
               '- [Substituídas, fora do escopo e vazias](#v1-resto)', '']

    corpo = []
    for n, caminho, t in docs:
        texto = rebaixa(desvincula(sem_titulo(le(caminho))), 2)
        corpo.append(f'<a id="doc-{n}"></a>\n\n## {n} — {t}\n\n{texto}\n')
        for arq, linhas, situacao, nums in v1_por_doc[n]:
            corpo.append(bloco_v1(arq, linhas, situacao, nums))
    corpo.append('<a id="v1-no-kit"></a>\n\n## Especificações v1 absorvidas no kit-starter\n\n'
                 'Estas especificações viraram fichas do kit-starter. Aqui está o texto integral da v1; a ficha tem as regras da v2 por cima.\n')
    for arq, linhas, situacao, kit in grupos['kit']:
        corpo.append(bloco_v1(arq, linhas, situacao, []) + f'\n*Ficha do kit-starter: `{kit[0]}`.*\n')
    corpo.append('\n<a id="v1-resto"></a>\n\n## Substituídas, fora do escopo e vazias\n')
    for grupo, titulo in (('fora', 'Fora do escopo'),
                          ('vazio', 'Vazias'), ('nao_classificado', 'Sem destino declarado')):
        if not grupos[grupo]:
            continue
        corpo.append(f'### {titulo}\n')
        for arq, linhas, situacao, nums in grupos[grupo]:
            corpo.append(bloco_v1(arq, linhas, situacao, nums))

    saida = '\n'.join(indice) + '\n' + '\n'.join(corpo)
    open(SAIDA, 'w', encoding='utf8').write(saida)
    print('gerado:', os.path.relpath(SAIDA, ROOT), len(saida.splitlines()), 'linhas,',
          len(saida.encode('utf8')) // 1024, 'KB |', sum(len(v) for v in v1_por_doc.values()), 'v1 por documento |',
          len(grupos['kit']), 'no kit |', len(grupos['substituido']), 'substituídas |',
          len(grupos['fora']), 'fora |', len(grupos['vazio']), 'vazias |', len(grupos['nao_classificado']), 'sem destino')


if __name__ == '__main__':
    main()
