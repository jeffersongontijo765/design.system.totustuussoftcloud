"""Gera docs/v2/SDD-COMPLETO.md: todos os documentos numerados da v2 em um único arquivo.

Uso: python3 inventario/gera_sdd_completo.py
- Um índice só, com uma entrada por documento.
- Cada documento vira uma parte com âncora `parte-NN`; títulos descem um nível.
- Links entre documentos (`NN-nome.md`) viram âncoras (`#parte-NN`). Links para `anexo-v1/` são mantidos.
Não editar o arquivo gerado à mão: regere depois de mudar qualquer documento.
"""
import datetime, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
V2 = os.path.join(ROOT, 'docs', 'v2')
SAIDA = os.path.join(V2, 'SDD-COMPLETO.md')

arquivos = sorted(f for f in os.listdir(V2) if re.match(r'^\d\d-.+\.md$', f))


def ajusta_links(texto):
    texto = re.sub(r'\]\((\d\d)-[^)#\s]*\.md(#[^)]*)?\)', lambda m: f'](#parte-{m.group(1)})', texto)
    return texto


def desce_titulos(texto):
    saida, em_codigo = [], False
    for linha in texto.splitlines():
        if linha.lstrip().startswith('```'):
            em_codigo = not em_codigo
        if not em_codigo and re.match(r'^#{1,5} ', linha):
            linha = '#' + linha
        saida.append(linha)
    return '\n'.join(saida)


indice, partes = [], []
for f in arquivos:
    num = f[:2]
    texto = open(os.path.join(V2, f), encoding='utf8').read()
    titulo = re.search(r'^#\s+(.+)$', texto, re.M)
    titulo = titulo.group(1).strip() if titulo else f
    indice.append(f'- [{titulo}](#parte-{num})')
    partes.append(f'---\n\n<a id="parte-{num}"></a>\n\n' + desce_titulos(ajusta_links(texto)).strip() + '\n')

hoje = datetime.date.today().strftime('%d/%m/%Y')
cabecalho = (f'# SDD v2 — TotusTuus SoftCloud (especificação completa)\n\n'
             f'> Documento consolidado dos documentos {arquivos[0][:2]} a {arquivos[-1][:2]} ({len(arquivos)} documentos), '
             f'gerado por `inventario/gera_sdd_completo.py` em {hoje}. Não editar à mão: a fonte são os documentos numerados desta pasta. '
             f'A v1 está incorporada em `anexo-v1/`; veja a rastreabilidade na [parte 79](#parte-79).\n\n'
             '## Índice\n\n' + '\n'.join(indice) + '\n\n')
open(SAIDA, 'w', encoding='utf8').write(cabecalho + '\n'.join(partes))
print('documentos:', len(arquivos), '| linhas:', sum(1 for _ in open(SAIDA, encoding='utf8')))
