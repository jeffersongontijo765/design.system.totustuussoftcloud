"""Monta as fichas detalhadas dos portais de entidade (gestão, professor, aluno, responsáveis, terceiros).

Uso: python3 kit-starter/fichas_portais.py
Dados: kit-starter/dados_<portal>.py (lista MODULOS).

Cada ficha é autossuficiente:
- seções 1 a 12: objetivo, telas, permissões por portal (extraídas do SDD), papéis, regras, dados, integrações,
  exportação, estados de interface, frontend, aceite e pendências;
- seção 13: texto integral das seções do SDD v2 que regem o módulo, sem corte;
- seção 14 (quando houver): texto integral da especificação da v1 absorvida, que perde para as seções 1 a 13.
"""
import glob, importlib, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
V2 = os.path.join(ROOT, 'docs', 'v2')
KIT = os.path.join(ROOT, 'kit-starter')
sys.path.insert(0, KIT)

PORTAIS = {
    'gestao': ('Gestão (`gestao.`)', ['Gestão', 'Coordenação', 'Secretaria']),
    'professor': ('Professor (`portal-do-professor.`)', ['Professor']),
    'aluno': ('Aluno (`portal-do-aluno.`)', ['Aluno']),
    'responsaveis': ('Pais e Responsáveis (`portal-dos-responsaveis.`)', ['Responsáveis']),
    'terceiros': ('Terceiros (`portal-de-terceiros.`)', ['Terceiros']),
}
DOMINIO = ('entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; '
           'nenhum dado de outra entidade ou unidade é visível ([03]({03}), [06]({06}), seção 12)')


def arq(num):
    achados = glob.glob(os.path.join(V2, f'{num}-*.md'))
    if not achados:
        raise SystemExit(f'documento {num} não encontrado')
    return achados[0]


def rel(destino_dir, alvo):
    return os.path.relpath(alvo, destino_dir).replace(os.sep, '/')


def rebaixa(texto, extra=2):
    out, codigo = [], False
    for linha in texto.splitlines():
        if linha.lstrip().startswith('```'):
            codigo = not codigo
        if not codigo:
            m = re.match(r'^(#{1,4}) ', linha)
            if m:
                linha = '#' * min(6, len(m.group(1)) + extra) + linha[len(m.group(1)):]
        out.append(linha)
    return '\n'.join(out)


def reescreve_links(texto, d, origem):
    """Links do texto copiado de docs/v2/<origem> passam a valer a partir da pasta da ficha."""
    base = rel(d, V2)
    texto = re.sub(r'\]\((\d\d-[^)#\s]+\.md)', lambda m: f']({base}/{m.group(1)}', texto)
    texto = re.sub(r'\]\(anexo-v1/', f']({base}/anexo-v1/', texto)
    texto = re.sub(r'\]\(#', f']({base}/{os.path.basename(origem)}#', texto)
    return texto


def secao(num_doc, sec):
    """Texto de uma seção (`'4'` para `## 4.`, `'2.3'` para `### 2.3`) ou do documento inteiro (None)."""
    caminho = arq(num_doc)
    linhas = open(caminho, encoding='utf8').read().splitlines()
    if sec is None:
        return '\n'.join(linhas[1:]).strip(), linhas[0].lstrip('# ').strip()
    nivel = '###' if ('.' in sec or not sec[0].isdigit()) else '##'
    pad = re.compile(rf'^{nivel} {re.escape(sec)}[. ]')
    ini = next((i for i, l in enumerate(linhas) if pad.match(l)), None)
    if ini is None:
        raise SystemExit(f'seção {sec} não encontrada em {os.path.basename(caminho)}')
    fim = len(linhas)
    for j in range(ini + 1, len(linhas)):
        l = linhas[j]
        if l.startswith('## ') or (nivel == '###' and l.startswith('### ')):
            fim = j
            break
    return '\n'.join(linhas[ini:fim]).strip().rstrip('-').strip(), linhas[ini].lstrip('# ').strip()


def tabelas_por_portal(num_doc):
    """Tabelas cuja primeira coluna é Portal (seção "Por portal" e similares)."""
    linhas = open(arq(num_doc), encoding='utf8').read().splitlines()
    tabs, i = [], 0
    while i < len(linhas):
        l = linhas[i]
        if re.match(r'^\|\s*(Portal|Perfil|Papel)\s*\|', l) and i + 1 < len(linhas) and re.match(r'^\|\s*-', linhas[i + 1]):
            cab, j = [l, linhas[i + 1]], i + 2
            corpo = []
            while j < len(linhas) and linhas[j].startswith('|'):
                corpo.append(linhas[j])
                j += 1
            tabs.append((cab, corpo))
            i = j
        else:
            i += 1
    return tabs


def linhas_portal(nums, nomes):
    blocos = []
    for n in nums:
        for cab, corpo in tabelas_por_portal(n):
            if not cab[0].startswith('| Portal'):
                continue
            sel = [c for c in corpo if any(c.split('|')[1].strip().strip('*').strip().startswith(x) for x in nomes)]
            if sel:
                blocos.append((n, cab, sel))
    return blocos


def monta(cfg, portal_key):
    destino = os.path.join(KIT, cfg['arquivo'])
    d = os.path.dirname(destino)
    os.makedirs(d, exist_ok=True)
    r = lambda n: rel(d, arq(n))
    sub = lambda t: re.sub(r'\{(\d\d)\}', lambda m: r(m.group(1)), t or '')
    nome_portal, nomes_linha = PORTAIS[portal_key]
    nomes_linha = cfg.get('linhas', nomes_linha)

    fontes = cfg['fontes']  # lista de (doc, seção|None)
    docs = []
    for n, _ in fontes:
        if n not in docs:
            docs.append(n)
    fonte_v2 = '; '.join(
        f"[{n}]({r(n)})" + (f", seção {s}" if s else ' (integral)') for n, s in fontes)

    v1 = cfg.get('v1', [])
    v1_txt = [(n, open(os.path.join(V2, 'anexo-v1', n), encoding='utf8').read()) for n in v1]
    if v1_txt:
        fonte_v1 = '- Fonte da v1: ' + '; '.join(
            f"[{n}]({rel(d, os.path.join(V2, 'anexo-v1', n))}) ({len(t.splitlines())} linhas)" for n, t in v1_txt) + \
            ' — absorvida integralmente na seção 14'
    elif cfg.get('v1_em'):
        fonte_v1 = '- Fonte da v1: absorvida integralmente em ' + ', '.join(
            f"[{os.path.basename(x)}]({rel(d, os.path.join(KIT, x))})" for x in cfg['v1_em']) + ' (mesma especificação, uma única cópia no kit)'
    else:
        fonte_v1 = '- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)'

    # permissões por portal (extraídas)
    blocos = linhas_portal(docs, nomes_linha + cfg.get('linhas_extra', []))
    if blocos:
        perm = '\n\n'.join(
            f"Do [{n}]({r(n)}):\n\n" + '\n'.join(cab + sel) for n, cab, sel in blocos)
        perm = reescreve_links(perm, d, arq(docs[0]))
    else:
        perm = '- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.'

    integral = []
    for n, s in fontes:
        texto, titulo = secao(n, s)
        texto = reescreve_links(texto, d, arq(n))
        if s is None:
            integral.append(f"### 13.{len(integral) + 1} [{titulo}]({r(n)}) (documento integral)\n\n{rebaixa(texto, 2)}")
        else:
            integral.append(f"### 13.{len(integral) + 1} [{n}]({r(n)}), seção {s}\n\n{rebaixa(texto, 2)}")
    sec13 = '## 13. Regras da v2 (texto integral das fontes, sem corte)\n\n' + '\n\n'.join(integral)

    sec14 = ''
    if v1_txt:
        partes = '\n\n'.join((f'### Fonte: {n}\n\n' if len(v1_txt) > 1 else '') + rebaixa(t, 3 if len(v1_txt) > 1 else 2)
                             for n, t in v1_txt)
        sec14 = f'\n\n## 14. Conteúdo integral da v1 (absorvido)\n\n{partes}'

    corpo = f"""# {cfg['titulo']}

- Portal: {nome_portal}
- Área: {cfg['area']}
- Domínio: {sub(cfg.get('dominio', DOMINIO))}
- Status: detalhado; regras da v2 copiadas integralmente (seção 13){'; especificação da v1 absorvida integralmente (seção 14)' if v1_txt else ''}
- Fonte da v2: {fonte_v2}
{fonte_v1}

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida.{' A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2.' if v1_txt else ''} Decisões tomadas por padrão estão no [80]({rel(d, os.path.join(V2, '80-decisoes-por-padrao.md'))}).

## 2. Objetivo e escopo

{sub(cfg['objetivo'])}

## 3. Telas

{sub(cfg['telas'])}

## 4. Permissões por portal (extraídas do SDD)

{perm}

## 5. Papéis

{sub(cfg['papeis'])}
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78]({rel(d, os.path.join(V2, '78-permissoes-e-papeis.md'))}), seções 2 e 5).

## 6. Regras de negócio essenciais

{sub(cfg['regras'])}

## 7. Dados

{sub(cfg.get('dados', '- Tabelas e campos conforme a seção 13 e o DDL do [51]({51}), quando o módulo estiver lá. Toda tabela tem `entidade_id`, `unidade_id`, `created_at`, `updated_at`, `created_by` e exclusão lógica com `deleted_at` e `deleted_by` ([03]({03}), seção 6; [15]({15}); [19]({19}), seção 14).'))}

## 8. Integrações

{sub(cfg.get('integracoes', '- Ver a seção de integrações do documento de origem, na seção 13.'))}

## 9. Exportação, auditoria e privacidade

- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08]({r('08')}), seção 3).
- Toda criação, alteração, aprovação, exclusão lógica, exportação e leitura de dado sensível gera evento de auditoria no banco da unidade ([29]({r('29')})).
- Dados pessoais conforme [07]({r('07')}): mínimo necessário, mascaramento em listas, base legal registrada.
{sub(cfg.get('privacidade', ''))}

## 10. Estados de interface

- Carregando (skeleton), vazio com chamada para ação, sem resultado de filtro, erro com nova tentativa, acesso negado, registro bloqueado, fechado ou baixado (somente leitura), conflito de edição (versão).

## 11. Requisitos de frontend

- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08]({r('08')})).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`): página de lista com DataTable, KPIs, drawer de detalhe, formulário em página ou modal, kanban quando houver fluxo de estados.
- Seletor de unidade no topo quando o usuário tiver mais de uma; a troca reemite o token com o novo contexto ([06]({r('06')}), seção 12).

## 12. Critérios de aceite e pendências

- Critérios de aceite: os do documento de origem (seção 13) e os de [31]({r('31')}), seção 6.
- Testes de isolamento: usuário de outra unidade ou entidade recebe 404 em toda rota do módulo ([03]({r('03')})).
{sub(cfg.get('pendencias', '- As pendências do documento de origem estão na seção 13 e consolidadas no [45]({45}).'))}

{sec13}{sec14}
"""
    corpo = re.sub(r'\n{3,}', '\n\n', corpo)
    open(destino, 'w', encoding='utf8').write(corpo)
    return destino, len(corpo.splitlines())


if __name__ == '__main__':
    pedidos = sys.argv[1:] or [p for p in PORTAIS if os.path.exists(os.path.join(KIT, f'dados_{p}.py'))]
    for p in pedidos:
        mod = importlib.import_module(f'dados_{p}')
        for cfg in mod.MODULOS:
            destino, n = monta(cfg, p)
            print(os.path.relpath(destino, ROOT), n, 'linhas')
