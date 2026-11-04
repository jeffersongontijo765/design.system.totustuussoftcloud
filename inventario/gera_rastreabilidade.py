"""Gera docs/v2/79-rastreabilidade-v1-v2.md: para onde foi cada arquivo da v1 dentro da v2.

Uso: python3 inventario/gera_rastreabilidade.py
Fontes: docs/v2/anexo-v1/ (arquivos da v1), docs/v2/12-catalogo-modulos.md (status) e os demais documentos da v2 (citações).
Não lê SDD-COMPLETO.md (é a concatenação dos demais).
"""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
V2 = os.path.join(ROOT, 'docs', 'v2')
ANEXO = os.path.join(V2, 'anexo-v1')
SAIDA = os.path.join(V2, '79-rastreabilidade-v1-v2.md')
GERAIS = {'00-README.md', '12-catalogo-modulos.md', '13-achados-v1.md', '45-pendencias-consolidadas.md', 'SDD-COMPLETO.md', '79-rastreabilidade-v1-v2.md'}

docs = {f: open(os.path.join(V2, f), encoding='utf8').read() for f in sorted(os.listdir(V2)) if f.endswith('.md') and f != 'SDD-COMPLETO.md' and f != '79-rastreabilidade-v1-v2.md'}
catalogo = docs['12-catalogo-modulos.md'].splitlines()


def cita(nome, texto):
    return re.search(r'(?<![\w.\-])' + re.escape(nome) + r'(?![\w.\-])', texto) is not None


def linha_catalogo(nome):
    for l in catalogo:
        if l.startswith('|') and cita(nome, l):
            return [c.strip() for c in l.strip().strip('|').split('|')]
    return None


def secao_catalogo(nome):
    sec = None
    for l in catalogo:
        if l.startswith('## '):
            sec = l
        if l.startswith('|') and cita(nome, l):
            return sec or ''
    return ''


def limpa(t):
    return re.sub(r'\[`?([^\]`]+)`?\]\([^)]*\)', r'\1', t).replace('|', '/').strip()


linhas_tab = []
contagem = {}
for nome in sorted(os.listdir(ANEXO), key=str.lower):
    caminho = os.path.join(ANEXO, nome)
    if not os.path.isfile(caminho):
        continue
    try:
        nlin = sum(1 for _ in open(caminho, encoding='utf8', errors='ignore'))
    except Exception:
        nlin = 0
    cat = linha_catalogo(nome)
    sec = secao_catalogo(nome)
    citado_em = [f for f, t in docs.items() if cita(nome, t) and f not in GERAIS]
    status = ''
    if os.path.getsize(caminho) < 10:
        status = 'Vazio'
        situacao = 'Arquivo vazio (placeholder), sem conteúdo a absorver'
    elif cat is None:
        situacao = 'LACUNA: não citado no catálogo nem nos documentos da v2'
    elif sec.startswith('## 4'):
        status = 'Substituído'
        situacao = 'Substituído por ' + limpa(cat[1])
    elif sec.startswith('## 3'):
        status = 'Não é especificação'
        situacao = 'Destino: ' + limpa(cat[2] if len(cat) > 2 else '')
    else:
        status = limpa(cat[2]) if len(cat) > 2 else ''
        if 'removido' in status.lower():
            situacao = 'Fora do escopo do produto'
        elif citado_em:
            situacao = 'Absorvido em parte em: ' + ', '.join(f.split('-')[0] for f in citado_em)
        else:
            situacao = 'Só catalogado: conteúdo ainda não absorvido na v2 (ler no anexo antes de implementar)'
    chave = situacao.split(':')[0].split(' por ')[0]
    contagem[chave] = contagem.get(chave, 0) + 1
    linhas_tab.append(f'| [`{nome}`](anexo-v1/{nome}) | {nlin} | {status} | {situacao} |')

resumo = '\n'.join(f'| {k} | {v} |' for k, v in sorted(contagem.items(), key=lambda x: -x[1]))
texto = f"""# 79 — Rastreabilidade v1 → v2

> Parte do [SDD v2](00-README.md). Gerado por `inventario/gera_rastreabilidade.py`. Não editar à mão: regere depois de mudar o catálogo ou um documento.
> **Objetivo:** mostrar, para cada arquivo da v1 (em [anexo-v1/](anexo-v1/)), para onde foi o conteúdo na v2 e o que ainda não foi absorvido. Nada da v1 fica sem destino declarado.

## 1. Como ler

- **Substituído:** o documento da v2 indicado cobre o assunto. A v1 fica só como histórico.
- **Absorvido em parte:** documentos da v2 citam e usam a especificação, mas não a reescreveram inteira. Ao implementar o módulo, ler a v1 no anexo e a v2 juntas; vale a v2 em caso de conflito.
- **Só catalogado:** o catálogo registra o arquivo, mas nenhum documento da v2 usa o conteúdo. **Ler no anexo antes de implementar** e trazer as regras para a v2.
- **Não é especificação:** arquivo de código ou de tarefas, com destino indicado.
- **Fora do escopo:** removido do produto por decisão registrada.
- **Arquivo vazio:** placeholder sem conteúdo.
- **LACUNA:** não citado em lugar nenhum da v2. Precisa de decisão.

## 2. Resumo

| Situação | Arquivos |
|---|---|
{resumo}

## 3. Arquivo por arquivo

| Arquivo da v1 | Linhas | Status no catálogo | Situação na v2 |
|---|---|---|---|
""" + '\n'.join(linhas_tab) + '\n'
open(SAIDA, 'w', encoding='utf8').write(texto)
print(resumo)
