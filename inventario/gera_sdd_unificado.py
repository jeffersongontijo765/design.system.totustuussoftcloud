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
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from sdd_partes import PARTES, KIT_PARTE
    docs = {n: (c, t) for n, c, t in docs_v2()}
    NUMEROS_V2 = set(docs)
    V1_NOMES.update(os.listdir(ANEXO))
    parte_do_doc = {d: P['n'] for P in PARTES for d in P['docs']}
    faltam = sorted(set(docs) - set(parte_do_doc))
    if faltam:
        raise SystemExit(f'documentos sem parte: {faltam}')

    # onde entra cada especificação da v1
    v1_apos_doc = {n: [] for n in docs}          # logo depois do documento que a absorveu
    v1_fim_parte = {P['n']: [] for P in PARTES}   # no fim da parte (absorvidas no kit, fora do escopo, vazias)
    for arq, linhas, situacao, nums, kit in mapeamento():
        if kit:
            parte = next((pn for pref, pn in KIT_PARTE if kit[0].startswith('kit-starter/' + pref)), PARTES[-1]['n'])
            v1_fim_parte[parte].append((arq, linhas, situacao, f'ficha do kit-starter: `{kit[0]}`'))
        elif nums:
            v1_apos_doc[nums[0]].append((arq, linhas, situacao, ''))
        else:
            v1_fim_parte[PARTES[-1]['n']].append((arq, linhas, situacao, ''))

    def bloco_v1(arq, linhas, situacao, nota):
        caminho = os.path.join(ANEXO, arq)
        texto = rebaixa(desvincula(le(caminho).strip()), 3) if os.path.isfile(caminho) else '_Arquivo ausente._'
        extra = f' Destino: {nota}.' if nota else ''
        return (f'<a id="v1-{ancora(arq)}"></a>\n\n### v1 — `{arq}` ({linhas} linhas)\n\n'
                f'> Situação na v2: {situacao}.{extra} Quando este texto diverge da v2, vale a v2.\n\n{texto}\n')

    hoje = datetime.date.today().isoformat()
    out = [
        '# SDD TotusTuus SoftCloud — documento único (v1 + v2)',
        '',
        f'Gerado em {hoje} por `inventario/gera_sdd_unificado.py`. Não editar à mão: a fonte são os documentos da v2, '
        'as especificações da v1 e a estrutura em `inventario/sdd_partes.py`.',
        '',
        '## Como ler',
        '',
        '- O SDD está dividido em 19 partes, por assunto. Cada parte começa com uma visão geral: resumo, diagramas dos fluxos e estados e regras principais.',
        '- Depois da visão geral vem o texto integral de cada documento da v2 da parte e, logo abaixo de cada um, o texto integral das especificações da v1 que ele absorveu.',
        '- No fim de cada parte estão as especificações da v1 que viraram fichas do kit-starter.',
        '- Quando a v1 e a v2 divergem, vale a v2. Nenhum link aponta para fora deste arquivo.',
        '',
        '## Índice',
        '',
    ]
    for P in PARTES:
        out.append(f'- [Parte {P["n"]} — {P["titulo"]}](#parte-{P["n"]})')
        for d in P['docs']:
            out.append(f'  - [{d} — {docs[d][1]}](#doc-{d})')
            for arq, *_ in v1_apos_doc[d]:
                out.append(f'    - [v1 `{arq}`](#v1-{ancora(arq)})')
        for arq, *_ in v1_fim_parte[P['n']]:
            out.append(f'  - [v1 `{arq}`](#v1-{ancora(arq)})')
    out.append('')
    for P in PARTES:
        out += ['---', '', f'<a id="parte-{P["n"]}"></a>', '', f'# Parte {P["n"]} — {P["titulo"]}', '',
                f'## Visão geral da parte {P["n"]}', '', P['abertura'].strip(), '']
        for d in P['docs']:
            caminho, t = docs[d]
            out.append(f'<a id="doc-{d}"></a>\n\n## {d} — {t}\n\n{rebaixa(desvincula(sem_titulo(le(caminho))), 2)}\n')
            for item in v1_apos_doc[d]:
                out.append(bloco_v1(*item))
        if v1_fim_parte[P['n']]:
            out.append(f'## Especificações da v1 desta parte absorvidas no kit-starter ou sem destino\n')
            for item in v1_fim_parte[P['n']]:
                out.append(bloco_v1(*item))
    saida = '\n'.join(out) + '\n'
    open(SAIDA, 'w', encoding='utf8').write(saida)
    n_v1 = sum(len(v) for v in v1_apos_doc.values()) + sum(len(v) for v in v1_fim_parte.values())
    print('gerado:', os.path.relpath(SAIDA, ROOT), len(saida.splitlines()), 'linhas,', len(saida.encode('utf8')) // 1024,
          'KB |', len(PARTES), 'partes |', len(docs), 'documentos v2 |', n_v1, 'especificações v1')


if __name__ == '__main__':
    main()
