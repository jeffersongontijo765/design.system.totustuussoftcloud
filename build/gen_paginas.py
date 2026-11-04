"""Gera uma página HTML por tela nomeada nas fichas do kit-starter, com o chassi do design system.

Uso: python3 build/gen_paginas.py
Entrada: kit-starter/**/*.md (seção "3. Telas" com itens "- **Nome**: descrição").
Saída:   paginas/<portal>/<caminho-da-ficha>/<tela>.html  e  paginas/index.html

As páginas são de apresentação: estrutura, componentes, permissões e regras vêm da ficha.
Colunas, valores e registros são ilustrativos e provisórios até a ficha ser detalhada.
Arquétipos: painel, kanban, assistente, formulário, detalhe e lista.
"""
import glob, html, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KIT = os.path.join(ROOT, 'kit-starter')
OUT = os.path.join(ROOT, 'paginas')
TOKENS = os.path.join(ROOT, 'components', '__tokens.css')
BUNDLE_CSS = os.path.join(ROOT, 'components', 'bundle.css')

PORTAL_KEY = {'desenvolvedor': 'Desenvolvedor', 'gestao': 'Gestão', 'professor': 'Professor',
              'aluno': 'Aluno', 'responsaveis': 'Responsáveis', 'terceiros': 'Terceiros',
              'transversal': 'Transversal'}


def slug(t):
    import unicodedata
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-') or 'tela'


def md_texto(s):
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    return s.replace('**', '').replace('`', '').strip()


def secoes(texto):
    """Lista de (título, corpo) para cada seção '## ...'."""
    partes = re.split(r'^## ', texto, flags=re.M)
    out = []
    for p in partes[1:]:
        t, _, corpo = p.partition('\n')
        out.append((t.strip(), corpo))
    return out


def ler_ficha(caminho):
    t = open(caminho, encoding='utf8').read()
    cab = {}
    for k in ('Portal', 'Área', 'Domínio'):
        m = re.search(rf'^- {k}: (.*)$', t, re.M)
        if m:
            cab[k] = m.group(1).strip()
    titulo = re.search(r'^# (.+)$', t, re.M)
    cab['titulo'] = titulo.group(1).strip() if titulo else os.path.basename(caminho)
    telas, papeis, regras = [], [], []
    for titulo_s, corpo in secoes(t):
        if re.match(r'^3\. Telas', titulo_s) and 'índice da v1' not in titulo_s:
            vistos = set()
            for linha in corpo.splitlines():
                m = re.match(r'^- \*\*(.+?)\*\*\s*[:(—-]?\s*(.*)$', linha)
                if m and m.group(1).strip().lower() not in vistos:
                    vistos.add(m.group(1).strip().lower())
                    telas.append((m.group(1).strip(), md_texto(m.group(2))))
        elif re.match(r'^\d+\. (Papéis|Permissões e papéis)', titulo_s):
            papeis += [md_texto(l[2:]) for l in corpo.splitlines() if l.startswith('- ')][:5]
        elif re.search(r'Regras|Correções', titulo_s) and not regras:
            regras += [md_texto(l[2:]) for l in corpo.splitlines() if l.startswith('- ')][:4]
    return cab, telas, papeis, regras


def arquetipo(nome, desc):
    s = (nome + ' ' + desc).lower()
    if re.search(r'kanban|funil', s):
        return 'kanban'
    if re.search(r'assistente|wizard|etapa|passo a passo', s):
        return 'assistente'
    if re.search(r'painel|dashboard|indicador|kpi|agregad|ocupação|resultado', s):
        return 'painel'
    if re.search(r'formulário|formulario|editor|cadastro|configura|nova |novo |novas |novos |solicitar|pedido|abrir|lançar|regras|definir|emitir|inscrição|reserva', s):
        return 'formulario'
    if re.search(r'detalhe|ficha|perfil|visão|histórico|prontuário|resumo', s):
        return 'detalhe'
    return 'lista'


ACAO = {'painel': None, 'kanban': 'Novo registro', 'assistente': 'Iniciar', 'formulario': 'Salvar',
        'detalhe': 'Editar', 'lista': 'Novo registro'}
COLUNAS = ['Registro', 'Situação', 'Responsável', 'Atualizado em']
LINHAS = [('REG-0001', 'Em andamento', 'Equipe da unidade', '12/11/2026'),
          ('REG-0002', 'Concluído', 'Coordenação', '11/11/2026'),
          ('REG-0003', 'Pendente', 'Secretaria', '10/11/2026')]


def chip(texto, tom='info'):
    return f'<span class="ttsc-badge ttsc-badge-{tom} ttsc-badge-light ttsc-badge-sm">{html.escape(texto)}</span>'


def corpo_lista(nome):
    cab = ''.join(f'<th>{html.escape(c)}</th>' for c in COLUNAS)
    linhas = ''.join(
        f'<tr><td>{html.escape(a)}</td><td>{chip(b, "success" if b == "Concluído" else "warning" if b == "Pendente" else "info")}</td>'
        f'<td>{html.escape(c)}</td><td>{d}</td></tr>' for a, b, c, d in LINHAS)
    return f'''
<section class="ttsc-card" aria-labelledby="lst">
  <div class="ttsc-card-header"><div class="ttsc-card-heading">
    <h2 class="ttsc-card-title" id="lst">{html.escape(nome)}</h2>
    <p class="ttsc-card-description">Lista com busca, filtros e exportação. Dados ilustrativos.</p></div></div>
  <div class="ttsc-card-content">
    <div class="pg-toolbar">
      <input class="ttsc-input" type="search" placeholder="Buscar registros..." aria-label="Buscar registros">
      <select class="ttsc-select" aria-label="Situação"><option>Todas as situações</option><option>Em andamento</option><option>Concluído</option><option>Pendente</option></select>
    </div>
    <div class="ttsc-table-wrapper"><table class="ttsc-table ttsc-table-zebra">
      <thead><tr>{cab}</tr></thead><tbody>{linhas}</tbody></table></div>
    <nav class="pg-paginacao" aria-label="Paginação"><span>1 a 3 de 3</span><span>Estados: carregando, vazio, sem resultado, erro e acesso negado.</span></nav>
  </div>
</section>'''


def corpo_painel(nome):
    kpis = [('Registros no período', '1.248', 'fa-list-check'), ('Concluídos', '86%', 'fa-circle-check'),
            ('Pendências', '37', 'fa-triangle-exclamation')]
    cards = ''.join(f'''<section class="ttsc-card ttsc-card-kpi"><div class="ttsc-card-content">
      <span class="ttsc-kpi-label"><i class="fa-light {i}"></i> {html.escape(l)}</span>
      <div class="ttsc-kpi-value">{v}</div></div></section>''' for l, v, i in kpis)
    return f'''
<div class="pg-kpis">{cards}</div>
<section class="ttsc-card" aria-labelledby="grf">
  <div class="ttsc-card-header"><div class="ttsc-card-heading">
    <h2 class="ttsc-card-title" id="grf">Evolução do período</h2>
    <p class="ttsc-card-description">Gráfico ilustrativo. Filtro por unidade e período.</p></div></div>
  <div class="ttsc-card-content"><div class="pg-grafico" role="img" aria-label="Gráfico de barras ilustrativo">
    <span style="height:40%"></span><span style="height:65%"></span><span style="height:52%"></span><span style="height:80%"></span><span style="height:72%"></span><span style="height:90%"></span></div></div>
</section>
<section class="ttsc-card" aria-labelledby="pnd">
  <div class="ttsc-card-header"><div class="ttsc-card-heading"><h2 class="ttsc-card-title" id="pnd">Itens que exigem atenção</h2></div></div>
  <div class="ttsc-card-content"><ul class="pg-lista">
    <li>{chip("Pendente", "warning")} Registro sem responsável atribuído</li>
    <li>{chip("Atrasado", "danger")} Prazo vencido há mais de 5 dias</li></ul></div>
</section>'''


def corpo_kanban(nome):
    colunas = [('Novo', 3), ('Em análise', 2), ('Aprovado', 4), ('Concluído', 1)]
    cols = ''.join(f'''<div class="pg-coluna"><div class="pg-coluna-titulo">{n} <span class="ttsc-badge ttsc-badge-light ttsc-badge-xs">{q}</span></div>
      {''.join(f'<div class="pg-cartao">REG-00{i}<br><small>Responsável: equipe da unidade</small></div>' for i in range(1, q + 1))}</div>''' for n, q in colunas)
    return f'''
<section class="ttsc-card" aria-labelledby="kb">
  <div class="ttsc-card-header"><div class="ttsc-card-heading"><h2 class="ttsc-card-title" id="kb">{html.escape(nome)}</h2>
    <p class="ttsc-card-description">Arraste um cartão para mudar de etapa. Mudança é registrada na auditoria.</p></div></div>
  <div class="ttsc-card-content"><div class="pg-kanban">{cols}</div></div>
</section>'''


def corpo_assistente(nome):
    etapas = ['Dados', 'Vínculo e regras', 'Documentos', 'Confirmação']
    nav = ''.join(f'<li class="{"is-ativo" if i == 0 else ""}"><span>{i + 1}</span> {e}</li>' for i, e in enumerate(etapas))
    return f'''
<section class="ttsc-card" aria-labelledby="wz">
  <div class="ttsc-card-header"><div class="ttsc-card-heading"><h2 class="ttsc-card-title" id="wz">{html.escape(nome)}</h2>
    <p class="ttsc-card-description">Cada etapa é salva e pode ser retomada.</p></div></div>
  <div class="ttsc-card-content">
    <ol class="pg-etapas" aria-label="Etapas">{nav}</ol>
    {campos_form()}
    <div class="pg-acoes"><button class="ttsc-btn ttsc-btn-outline" type="button">Voltar</button><button class="ttsc-btn ttsc-btn-primary" type="button">Próxima etapa</button></div>
  </div>
</section>'''


def campos_form():
    campos = [('Nome completo', 'text', True), ('CPF', 'text', True), ('Unidade', 'select', True),
              ('Data de referência', 'date', False), ('Observações', 'textarea', False)]
    partes = []
    for label, tipo, obrig in campos:
        idc = slug(label)
        req = ' <span class="ttsc-form-required" aria-hidden="true">*</span>' if obrig else ''
        if tipo == 'select':
            ctrl = f'<select class="ttsc-select" id="{idc}"><option>Selecione</option><option>Unidade Centro</option></select>'
        elif tipo == 'textarea':
            ctrl = f'<textarea class="ttsc-textarea" id="{idc}" rows="3"></textarea>'
        else:
            ctrl = f'<input class="ttsc-input" id="{idc}" type="{tipo}"{" required" if obrig else ""}>'
        partes.append(f'<div class="pg-campo"><label class="ttsc-form-label" for="{idc}">{label}{req}</label>{ctrl}</div>')
    return '<form class="pg-form" novalidate>' + ''.join(partes) + '</form>'


def corpo_formulario(nome):
    return f'''
<section class="ttsc-card" aria-labelledby="fm">
  <div class="ttsc-card-header"><div class="ttsc-card-heading"><h2 class="ttsc-card-title" id="fm">{html.escape(nome)}</h2>
    <p class="ttsc-card-description">Campos obrigatórios marcados com *. Alterações ficam na auditoria.</p></div></div>
  <div class="ttsc-card-content">{campos_form()}
    <div class="pg-acoes"><button class="ttsc-btn ttsc-btn-outline" type="button">Cancelar</button><button class="ttsc-btn ttsc-btn-primary" type="button">Salvar</button></div>
  </div>
</section>'''


def corpo_detalhe(nome):
    dados = [('Código', 'REG-0001'), ('Situação', 'Em andamento'), ('Responsável', 'Coordenação'), ('Última alteração', '12/11/2026 14:30')]
    kv = ''.join(f'<div class="pg-kv"><span>{k}</span><b>{v}</b></div>' for k, v in dados)
    return f'''
<section class="ttsc-card" aria-labelledby="dt">
  <div class="ttsc-card-header"><div class="ttsc-card-heading"><h2 class="ttsc-card-title" id="dt">{html.escape(nome)}</h2>
    <p class="ttsc-card-description">Visão somente leitura. Edição conforme permissão.</p></div></div>
  <div class="ttsc-card-content">{kv}</div>
</section>
<section class="ttsc-card" aria-labelledby="hst">
  <div class="ttsc-card-header"><div class="ttsc-card-heading"><h2 class="ttsc-card-title" id="hst">Histórico</h2></div></div>
  <div class="ttsc-card-content"><ul class="pg-lista"><li>12/11/2026 14:30 · Registro atualizado</li><li>10/11/2026 09:12 · Criado</li></ul></div>
</section>'''


CORPO = {'painel': corpo_painel, 'kanban': corpo_kanban, 'assistente': corpo_assistente,
         'formulario': corpo_formulario, 'detalhe': corpo_detalhe, 'lista': corpo_lista}

ESTILO = """
:root{color-scheme:light dark}
body{margin:0;background:var(--ttsc-canvas);color:var(--ttsc-text);font:13px/1.5 Inter,system-ui,sans-serif}
.pg{padding:16px;max-width:1280px;margin:0 auto}
@media(min-width:640px){.pg{padding:20px}}
.pg-cabeca{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;margin:8px 0 16px}
.pg-titulo{font-size:20px;line-height:28px;font-weight:700;letter-spacing:-.01em;margin:0}
.pg-layout{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:16px;align-items:start}
@media(max-width:900px){.pg-layout{grid-template-columns:1fr}}
.pg-principal{display:flex;flex-direction:column;gap:16px;min-width:0}
.pg-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}
.pg-kpis .ttsc-kpi-value{font-size:28px;font-weight:600}
.pg-toolbar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.pg-toolbar .ttsc-input{flex:1 1 220px}
.pg-paginacao{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-top:12px;color:var(--ttsc-text-muted);font-size:12px}
.pg-grafico{display:flex;align-items:flex-end;gap:10px;height:180px;padding:8px 0}
.pg-grafico span{flex:1;background:var(--ttsc-accent-soft);border-top:3px solid var(--ttsc-accent);border-radius:6px 6px 0 0}
.pg-lista{margin:0;padding-left:0;list-style:none;display:flex;flex-direction:column;gap:8px}
.pg-kanban{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.pg-coluna{background:var(--ttsc-canvas-2);border:1px solid var(--ttsc-border-soft);border-radius:var(--ttsc-radius-surface);padding:10px;display:flex;flex-direction:column;gap:8px;min-height:160px}
.pg-coluna-titulo{font-weight:600;font-size:12px;color:var(--ttsc-text-2)}
.pg-cartao{background:var(--ttsc-surface);border:1px solid var(--ttsc-border);border-radius:var(--ttsc-radius-sm);padding:8px;font-size:12px}
.pg-cartao small{color:var(--ttsc-text-muted)}
.pg-etapas{display:flex;flex-wrap:wrap;gap:12px;list-style:none;padding:0;margin:0 0 16px;color:var(--ttsc-text-muted)}
.pg-etapas li{display:flex;align-items:center;gap:6px}
.pg-etapas li span{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:999px;border:1px solid var(--ttsc-border-strong);font-size:11px}
.pg-etapas li.is-ativo{color:var(--ttsc-text);font-weight:600}
.pg-etapas li.is-ativo span{background:var(--ttsc-accent);color:var(--ttsc-accent-on);border-color:transparent}
.pg-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.pg-campo{display:flex;flex-direction:column;gap:6px}
.pg-campo textarea,.pg-form textarea{grid-column:1/-1}
.pg-acoes{display:flex;justify-content:flex-end;gap:8px;margin-top:16px;flex-wrap:wrap}
.pg-kv{display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid var(--ttsc-border-soft)}
.pg-kv span{color:var(--ttsc-text-muted)}
.pg-lateral .ttsc-card-content{display:flex;flex-direction:column;gap:10px}
.pg-lateral h3{font-size:13px;margin:0;color:var(--ttsc-text)}
.pg-lateral ul{margin:0;padding-left:16px;color:var(--ttsc-text-2);font-size:12px}
.pg-lateral a{color:var(--ttsc-accent-text);font-size:12px}
.pg-aviso{font-size:12px;color:var(--ttsc-text-muted);margin:0}
"""


def pagina(cab, nome, arq, papeis, regras, ficha_rel, sdd_rel, tokens_rel, bundle_rel, portal_nome):
    arq_corpo = CORPO[arq](nome)
    acao = ACAO[arq]
    botao = f'<button class="ttsc-btn ttsc-btn-primary" type="button"><i class="fa-light fa-plus"></i> {acao}</button>' if acao else ''
    papeis_html = ''.join(f'<li>{html.escape(p)}</li>' for p in papeis) or '<li>Ver a ficha da tela.</li>'
    regras_html = ''.join(f'<li>{html.escape(r)}</li>' for r in regras) or '<li>Ver a ficha da tela.</li>'
    area = cab.get('Área', '')
    portal_nome = re.sub(r'\s*\(`[^`]*`\)', '', portal_nome).strip()
    migalhas = [portal_nome] + ([area] if area and area != cab['titulo'] else []) + [cab['titulo'], nome]
    bc = ''.join(
        f'<li class="ttsc-breadcrumb-item"><a class="ttsc-breadcrumb-link" href="#">{html.escape(m)}</a></li>'
        f'<li class="ttsc-breadcrumb-separator" aria-hidden="true"><i class="fa-light fa-chevron-right"></i></li>'
        for m in migalhas[:-1])
    return f'''<!doctype html>
<html lang="pt-BR" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(nome)} · {html.escape(cab['titulo'])}</title>
<link rel="stylesheet" href="{tokens_rel}">
<link rel="stylesheet" href="{bundle_rel}">
<style>{ESTILO}</style>
</head>
<body>
<main class="pg" data-arquetipo="{arq}">
  <nav aria-label="Trilha de navegação"><ol class="ttsc-breadcrumb">{bc}<li class="ttsc-breadcrumb-item"><span class="ttsc-breadcrumb-page" aria-current="page">{html.escape(nome)}</span></li></ol></nav>
  <div class="pg-cabeca">
    <h1 class="pg-titulo">{html.escape(nome)}</h1>
    <div class="pg-botoes" style="display:flex;gap:8px"><button class="ttsc-btn ttsc-btn-outline ttsc-btn-sm" type="button"><i class="fa-light fa-download"></i> Exportar</button>{botao}</div>
  </div>
  <div class="pg-layout">
    <div class="pg-principal">{arq_corpo}</div>
    <aside class="pg-lateral">
      <section class="ttsc-card"><div class="ttsc-card-content">
        <h3>Quem acessa</h3><ul>{papeis_html}</ul>
        <h3>Regras essenciais</h3><ul>{regras_html}</ul>
        <p class="pg-aviso">Ficha de origem: <a href="{ficha_rel}">{html.escape(cab['titulo'])}</a> · <a href="{sdd_rel}">SDD v2</a></p>
      </div></section>
    </aside>
  </div>
</main>
</body>
</html>
'''


def main():
    fichas = []
    for caminho in sorted(glob.glob(os.path.join(KIT, '**', '*.md'), recursive=True)):
        rel = os.path.relpath(caminho, KIT).replace(os.sep, '/')
        if re.match(r'^(README|MODELO)', os.path.basename(caminho)):
            continue
        cab, telas, papeis, regras = ler_ficha(caminho)
        if telas:
            fichas.append((caminho, rel, cab, telas, papeis, regras))
    if os.path.isdir(OUT):
        import shutil
        shutil.rmtree(OUT)
    indice = []
    total = 0
    for caminho, rel, cab, telas, papeis, regras in fichas:
        portal_chave = rel.split('/')[0]
        portal_nome = cab.get('Portal', PORTAL_KEY.get(portal_chave, portal_chave))
        pasta_ficha = rel[:-3]
        pasta = os.path.join(OUT, pasta_ficha)
        os.makedirs(pasta, exist_ok=True)
        for nome, desc in telas:
            arq = arquetipo(nome, desc)
            fn = os.path.join(pasta, slug(nome) + '.html')
            d = os.path.dirname(fn)
            tok = os.path.relpath(TOKENS, d).replace(os.sep, '/')
            bun = os.path.relpath(BUNDLE_CSS, d).replace(os.sep, '/')
            ficha_rel = os.path.relpath(caminho, d).replace(os.sep, '/')
            sdd_rel = os.path.relpath(os.path.join(ROOT, 'docs', 'v2', '00-README.md'), d).replace(os.sep, '/')
            src = pagina(cab, nome, arq, papeis, regras, ficha_rel, sdd_rel, tok, bun, portal_nome)
            open(fn, 'w', encoding='utf8').write(src)
            total += 1
            indice.append((portal_nome, cab.get('Área', ''), cab['titulo'], nome, arq, os.path.relpath(fn, OUT).replace(os.sep, '/')))
    grupos = {}
    for portal, area, mod, nome, arq, link in indice:
        grupos.setdefault((portal, area, mod), []).append((nome, arq, link))
    corpo = ''
    for (portal, area, mod), itens in grupos.items():
        lis = ''.join(f'<li><a href="{html.escape(link)}">{html.escape(nome)}</a> <small>({arq})</small></li>'
                      for nome, arq, link in itens)
        corpo += f'<section><h3>{html.escape(portal)} · {html.escape(area)} · {html.escape(mod)}</h3><ul class="pg-lista">{lis}</ul></section>'
    idx = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Páginas geradas do kit-starter</title><link rel="stylesheet" href="../components/__tokens.css"><link rel="stylesheet" href="../components/bundle.css">
<style>{ESTILO}</style></head><body><main class="pg"><h1 class="pg-titulo">Páginas geradas do kit-starter</h1>
<p class="pg-aviso">{total} telas geradas a partir de {len(fichas)} fichas. Colunas e dados são ilustrativos; a ficha de cada tela tem as regras.</p>
{corpo}</main></body></html>'''
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(idx)
    print('fichas com telas:', len(fichas), '| páginas:', total)


if __name__ == '__main__':
    main()
