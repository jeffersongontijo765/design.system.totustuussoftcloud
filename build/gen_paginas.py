"""Gera uma página por tela nomeada nas fichas do kit-starter, renderizada pelo TTSCModelKit do design system.

Uso: python3 build/gen_paginas.py
Entrada: kit-starter/**/*.md (seção "3. Telas": itens "- **Nome**: descrição").
Saída:   paginas/<portal>/<caminho-da-ficha>/<tela>.html  e  paginas/index.html

Cada página carrega components/bundle.js e chama TTSCModelKit.render com uma especificação no
formato de models/academico.json (campos, status, KPIs, Kanban, Analytics, gaveta e formulário).
Os campos e status vêm do domínio que o módulo gerencia (ver DOMINIOS). Registros de exemplo são
gerados pelo próprio renderizador a partir da especificação.
"""
import glob, html, json, os, re, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KIT = os.path.join(ROOT, 'kit-starter')
OUT = os.path.join(ROOT, 'paginas')
TOKENS = os.path.join(ROOT, 'components', '__tokens.css')
BUNDLE_CSS = os.path.join(ROOT, 'components', 'bundle.css')
BUNDLE_JS = os.path.join(ROOT, 'components', 'bundle.js')

TONS = ['blue', 'emerald', 'amber', 'purple', 'slate', 'rose']


def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-') or 'tela'


def md_texto(s):
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    return s.replace('**', '').replace('`', '').strip()


def secoes(texto):
    out = []
    for p in re.split(r'^## ', texto, flags=re.M)[1:]:
        t, _, corpo = p.partition('\n')
        out.append((t.strip(), corpo))
    return out


def ler_ficha(caminho):
    t = open(caminho, encoding='utf8').read()
    cab = {}
    for k in ('Portal', 'Área'):
        m = re.search(rf'^- {k}: (.*)$', t, re.M)
        if m:
            cab[k] = md_texto(m.group(1))
    m = re.search(r'^# (.+)$', t, re.M)
    cab['titulo'] = m.group(1).strip() if m else os.path.basename(caminho)
    telas = []
    for titulo_s, corpo in secoes(t):
        if re.match(r'^3\. Telas', titulo_s):
            vistos = set()
            for linha in corpo.splitlines():
                m = re.match(r'^- \*\*(.+?)\*\*\s*[:(—-]?\s*(.*)$', linha)
                if m and m.group(1).strip().lower() not in vistos:
                    vistos.add(m.group(1).strip().lower())
                    telas.append((m.group(1).strip(), md_texto(m.group(2))))
    return cab, telas


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


# ---------------------------------------------------------------- domínios
# Cada domínio define campos (tipos aceitos pelo renderizador), status e KPIs do que o módulo gerencia.

def enum(key, label, opcoes):
    return {'key': key, 'label': label, 'type': 'enum',
            'values': [{'id': o, 'label': o, 'tone': TONS[i % len(TONS)], 'weight': max(1, 4 - i)}
                       for i, o in enumerate(opcoes)]}


def campo(key, label, tipo, **kw):
    return dict({'key': key, 'label': label, 'type': tipo}, **kw)


def st(*itens):
    return [{'id': i, 'label': l, 'tone': t, 'weight': 2} for i, l, t in itens]


DOMINIOS = {
    'contabil': dict(icon='fa-book', fields=[
        campo('name', 'Descrição', 'title', samples=['Receita de mensalidades', 'Despesa com energia', 'Depreciação de bens', 'Retenção de ISS', 'Pagamento de fornecedor']),
        campo('code', 'Lançamento', 'code', prefix='LAN'),
        enum('natureza', 'Natureza', ['débito', 'crédito']),
        enum('conta', 'Conta', ['receita', 'despesa', 'ativo', 'passivo']),
        campo('valor', 'Valor', 'money', min=40, max=9000),
        campo('competencia', 'Competência', 'date', **{'from': -120, 'to': 0}),
        campo('status', 'Situação', 'status')],
        statuses=st(('rascunho', 'Rascunho', 'slate'), ('revisado', 'Revisado', 'blue'), ('fechado', 'Fechado', 'emerald'), ('cancelado', 'Cancelado', 'rose')),
        kpis=[('Em rascunho', 'Aguardando revisão', 'fa-pen', 'rascunho', 'count'), ('Revisados', 'Prontos para fechar', 'fa-circle-check', 'revisado', 'count'), ('Fechados', 'Período encerrado', 'fa-lock', 'fechado', 'count')]),
    'financeiro': dict(icon='fa-sack-dollar', fields=[
        campo('name', 'Título', 'title', samples=['Mensalidade 11/2026', 'Taxa de matrícula', 'Multa da biblioteca', 'Transporte escolar', 'Material didático']),
        campo('person', 'Pagador', 'person'),
        campo('code', 'Título nº', 'code', prefix='TIT'),
        campo('valor', 'Valor', 'money', min=120, max=2400),
        campo('vencimento', 'Vencimento', 'date', **{'from': -60, 'to': 60}),
        enum('meio', 'Meio de pagamento', ['boleto', 'pix', 'cartão']),
        campo('status', 'Situação', 'status')],
        statuses=st(('aberto', 'Aberto', 'blue'), ('pago', 'Pago', 'emerald'), ('vencido', 'Vencido', 'rose'), ('cancelado', 'Cancelado', 'slate')),
        kpis=[('Em aberto', 'Aguardando pagamento', 'fa-receipt', 'aberto', 'count'), ('Vencidos', 'Acima do prazo', 'fa-triangle-exclamation', 'vencido', 'count'), ('Recebido', 'Títulos pagos', 'fa-sack-dollar', 'pago', 'money')]),
    'pessoas': dict(icon='fa-users', fields=[
        campo('name', 'Cargo', 'title', samples=['Auxiliar de secretaria', 'Professora de Matemática', 'Coordenador pedagógico', 'Técnico de laboratório', 'Assistente financeiro']),
        campo('person', 'Colaborador', 'person'),
        campo('code', 'Matrícula funcional', 'code', prefix='COL'),
        enum('setor', 'Setor', ['Administrativo', 'Pedagógico', 'Financeiro', 'Manutenção']),
        campo('salario', 'Salário', 'money', min=2100, max=9800),
        campo('admissao', 'Admissão', 'date', **{'from': -2000, 'to': -30}),
        campo('status', 'Situação', 'status')],
        statuses=st(('ativo', 'Ativo', 'emerald'), ('ferias', 'Em férias', 'blue'), ('afastado', 'Afastado', 'amber'), ('desligado', 'Desligado', 'slate')),
        kpis=[('Ativos', 'Colaboradores em atividade', 'fa-users', 'ativo', 'count'), ('Afastados', 'Afastamentos em curso', 'fa-user-clock', 'afastado', 'count'), ('Folha bruta', 'Soma dos salários ativos', 'fa-sack-dollar', 'ativo', 'money')]),
    'sst': dict(icon='fa-hard-hat', fields=[
        campo('name', 'Registro', 'title', samples=['ASO admissional', 'Exame periódico', 'CAT de trajeto', 'Entrega de EPI', 'Treinamento NR-10']),
        campo('person', 'Colaborador', 'person'),
        campo('code', 'Registro nº', 'code', prefix='SST'),
        enum('tipo', 'Tipo', ['admissional', 'periódico', 'demissional']),
        enum('resultado', 'Resultado', ['apto', 'apto com restrição']),
        campo('validade', 'Validade', 'date', **{'from': -30, 'to': 365}),
        campo('status', 'Situação', 'status')],
        statuses=st(('valido', 'Válido', 'emerald'), ('vencendo', 'Vence em 30 dias', 'amber'), ('vencido', 'Vencido', 'rose'), ('pendente', 'Pendente', 'blue')),
        kpis=[('Válidos', 'Dentro da validade', 'fa-shield-heart', 'valido', 'count'), ('Vencendo', 'Renovar em 30 dias', 'fa-clock', 'vencendo', 'count'), ('Vencidos', 'Renovação obrigatória', 'fa-triangle-exclamation', 'vencido', 'count')]),
    'academico': dict(icon='fa-graduation-cap', fields=[
        campo('name', 'Registro', 'title', samples=['1ª série A', 'Matemática II', 'Diário de Biologia', 'Conselho de classe 1º bimestre', 'Plano de aula semana 12']),
        campo('person', 'Aluno', 'person'),
        campo('code', 'Registro nº', 'code', prefix='ACA'),
        enum('curso', 'Curso', ['Ensino Médio', 'Fundamental II', 'Técnico em Informática']),
        enum('turno', 'Turno', ['manhã', 'tarde', 'noite']),
        campo('frequencia', 'Frequência', 'pct', min=62, max=100),
        campo('data', 'Data', 'date', **{'from': -200, 'to': 30}),
        campo('status', 'Situação', 'status')],
        statuses=st(('ativo', 'Ativo', 'emerald'), ('pendente', 'Pendente', 'amber'), ('concluido', 'Concluído', 'blue'), ('cancelado', 'Cancelado', 'slate')),
        kpis=[('Ativos', 'Em andamento', 'fa-circle-check', 'ativo', 'count'), ('Pendentes', 'Aguardam ação', 'fa-hourglass-half', 'pendente', 'count'), ('Concluídos', 'Encerrados no período', 'fa-flag-checkered', 'concluido', 'count')]),
    'documentos': dict(icon='fa-folder-open', fields=[
        campo('name', 'Documento', 'title', samples=['Declaração de matrícula', 'Histórico escolar', 'Requerimento de transferência', 'Ofício interno', 'Contrato de prestação']),
        campo('person', 'Solicitante', 'person'),
        campo('code', 'Protocolo', 'code', prefix='PRO'),
        enum('tipo', 'Tipo', ['declaração', 'histórico', 'requerimento', 'ofício']),
        enum('canal', 'Canal', ['portal', 'balcão', 'e-mail']),
        campo('prazo', 'Prazo', 'date', **{'from': -30, 'to': 30}),
        campo('status', 'Situação', 'status')],
        statuses=st(('recebido', 'Recebido', 'blue'), ('em_analise', 'Em análise', 'amber'), ('pendente', 'Pendente', 'rose'), ('concluido', 'Concluído', 'emerald'), ('indeferido', 'Indeferido', 'slate')),
        kpis=[('Recebidos', 'Aguardando triagem', 'fa-inbox', 'recebido', 'count'), ('Em análise', 'Em tramitação', 'fa-magnifying-glass', 'em_analise', 'count'), ('Concluídos', 'Entregues ao solicitante', 'fa-circle-check', 'concluido', 'count')]),
    'patrimonio': dict(icon='fa-boxes-stacked', fields=[
        campo('name', 'Bem', 'title', samples=['Notebook administrativo', 'Veículo de transporte escolar', 'Projetor multimídia', 'Bebedouro industrial', 'Rota Norte']),
        campo('person', 'Responsável', 'person'),
        campo('code', 'Plaqueta', 'code', prefix='BEM'),
        enum('categoria', 'Categoria', ['informática', 'veículo', 'mobiliário', 'equipamento']),
        campo('valor', 'Valor de aquisição', 'money', min=300, max=180000),
        campo('aquisicao', 'Aquisição', 'date', **{'from': -2000, 'to': -10}),
        campo('status', 'Situação', 'status')],
        statuses=st(('em_uso', 'Em uso', 'emerald'), ('em_manutencao', 'Em manutenção', 'amber'), ('disponivel', 'Disponível', 'blue'), ('baixado', 'Baixado', 'slate')),
        kpis=[('Em uso', 'Bens alocados', 'fa-check', 'em_uso', 'count'), ('Em manutenção', 'Ordens abertas', 'fa-wrench', 'em_manutencao', 'count'), ('Valor em uso', 'Soma de aquisição', 'fa-sack-dollar', 'em_uso', 'money')]),
    'suprimentos': dict(icon='fa-cart-shopping', fields=[
        campo('name', 'Item', 'title', samples=['Papel A4 resma', 'Gêneros para merenda', 'Material de limpeza', 'Kit de laboratório', 'Uniformes']),
        campo('person', 'Solicitante', 'person'),
        campo('code', 'Pedido', 'code', prefix='PED'),
        campo('quantidade', 'Quantidade', 'int', min=1, max=300),
        campo('valor', 'Valor total', 'money', min=80, max=40000),
        campo('entrega', 'Entrega prevista', 'date', **{'from': -10, 'to': 45}),
        campo('status', 'Situação', 'status')],
        statuses=st(('solicitada', 'Solicitada', 'blue'), ('aprovada', 'Aprovada', 'emerald'), ('cotada', 'Cotada', 'amber'), ('pedida', 'Pedida', 'purple'), ('recebida', 'Recebida', 'slate')),
        kpis=[('Solicitadas', 'Aguardam aprovação', 'fa-hand', 'solicitada', 'count'), ('Aprovadas', 'Prontas para cotar', 'fa-thumbs-up', 'aprovada', 'count'), ('Em pedido', 'Valor pedido', 'fa-truck', 'pedida', 'money')]),
    'contratos': dict(icon='fa-file-signature', fields=[
        campo('name', 'Contrato', 'title', samples=['Transporte escolar', 'Limpeza predial', 'Matrícula 2026', 'Professor horista', 'Aditivo de reajuste']),
        campo('person', 'Contraparte', 'person'),
        campo('code', 'Contrato nº', 'code', prefix='CTR'),
        enum('tipo', 'Tipo', ['fornecedor', 'aluno', 'pessoal']),
        campo('valor', 'Valor mensal', 'money', min=200, max=60000),
        campo('vigencia', 'Vigência até', 'date', **{'from': 0, 'to': 720}),
        campo('status', 'Situação', 'status')],
        statuses=st(('rascunho', 'Rascunho', 'slate'), ('em_assinatura', 'Em assinatura', 'blue'), ('vigente', 'Vigente', 'emerald'), ('encerrado', 'Encerrado', 'amber')),
        kpis=[('Vigentes', 'Contratos em execução', 'fa-file-circle-check', 'vigente', 'count'), ('Em assinatura', 'Aguardam assinatura', 'fa-pen-nib', 'em_assinatura', 'count'), ('Mensal vigente', 'Soma dos valores', 'fa-sack-dollar', 'vigente', 'money')]),
    'biblioteca': dict(icon='fa-book-open', fields=[
        campo('name', 'Obra', 'title', samples=['Dom Casmurro', 'Atlas de geografia', 'Revista de ciências', 'Introdução à álgebra', 'Coleção digital']),
        campo('person', 'Leitor', 'person'),
        campo('code', 'Tombo', 'code', prefix='TOM'),
        enum('acervo', 'Acervo', ['livro', 'periódico', 'digital']),
        campo('devolucao', 'Devolução prevista', 'date', **{'from': -10, 'to': 20}),
        campo('status', 'Situação', 'status')],
        statuses=st(('disponivel', 'Disponível', 'emerald'), ('emprestado', 'Emprestado', 'blue'), ('reservado', 'Reservado', 'purple'), ('em_atraso', 'Em atraso', 'rose')),
        kpis=[('Disponíveis', 'Prontos para empréstimo', 'fa-check', 'disponivel', 'count'), ('Emprestados', 'Em circulação', 'fa-arrow-right-arrow-left', 'emprestado', 'count'), ('Em atraso', 'Cobrar devolução', 'fa-clock', 'em_atraso', 'count')]),
    'simulados': dict(icon='fa-clipboard-check', fields=[
        campo('name', 'Prova', 'title', samples=['Simulado ENEM 1', 'Prova de Matemática 2º bimestre', 'Avaliação diagnóstica', 'Vestibular interno', 'Banco de questões de Física']),
        campo('person', 'Autor', 'person'),
        campo('code', 'Prova nº', 'code', prefix='PRV'),
        enum('perfil', 'Perfil', ['ENEM', 'vestibular', 'interna']),
        campo('questoes', 'Questões', 'int', min=10, max=90),
        campo('acerto', 'Acerto médio', 'pct', min=30, max=95),
        campo('aplicacao', 'Aplicação', 'date', **{'from': -30, 'to': 60}),
        campo('status', 'Situação', 'status')],
        statuses=st(('rascunho', 'Rascunho', 'slate'), ('revisada', 'Revisada', 'blue'), ('publicada', 'Publicada', 'emerald'), ('arquivada', 'Arquivada', 'amber')),
        kpis=[('Publicadas', 'Disponíveis aos alunos', 'fa-eye', 'publicada', 'count'), ('Em revisão', 'Aguardam revisão', 'fa-glasses', 'revisada', 'count'), ('Rascunhos', 'Em elaboração', 'fa-pen', 'rascunho', 'count')]),
    'atendimento': dict(icon='fa-headset', fields=[
        campo('name', 'Assunto', 'title', samples=['Não recebi o boleto', 'Alteração de dados cadastrais', 'Problema de acesso ao portal', 'Segunda via de documento', 'Dúvida sobre bolsa']),
        campo('person', 'Solicitante', 'person'),
        campo('code', 'Ticket', 'code', prefix='TKT'),
        enum('prioridade', 'Prioridade', ['baixa', 'média', 'alta']),
        enum('fila', 'Fila', ['SAC', 'helpdesk', 'chat']),
        campo('aberto', 'Aberto em', 'datetime', **{'from': -30, 'to': 0}),
        campo('status', 'Situação', 'status')],
        statuses=st(('aberto', 'Aberto', 'blue'), ('em_atendimento', 'Em atendimento', 'amber'), ('aguardando_cliente', 'Aguardando cliente', 'purple'), ('resolvido', 'Resolvido', 'emerald')),
        kpis=[('Abertos', 'Sem resposta', 'fa-envelope-open', 'aberto', 'count'), ('Em atendimento', 'Com responsável', 'fa-user-headset', 'em_atendimento', 'count'), ('Resolvidos', 'Encerrados', 'fa-circle-check', 'resolvido', 'count')]),
    'seguranca': dict(icon='fa-shield-halved', fields=[
        campo('name', 'Registro', 'title', samples=['Login do administrador', 'Alteração de papel', 'Exportação de auditoria', 'Pedido de acesso do titular', 'Certificado do domínio', 'Backup do banco master']),
        campo('person', 'Usuário', 'person'),
        campo('code', 'Evento', 'code', prefix='EVT'),
        enum('portal', 'Portal', ['Desenvolvedor', 'Gestão', 'Professor', 'Aluno']),
        enum('resultado', 'Resultado', ['sucesso', 'bloqueado', 'negado']),
        campo('data', 'Data', 'datetime', **{'from': -30, 'to': 0}),
        campo('status', 'Situação', 'status')],
        statuses=st(('ativo', 'Ativo', 'emerald'), ('pendente', 'Pendente', 'amber'), ('bloqueado', 'Bloqueado', 'rose'), ('revogado', 'Revogado', 'slate')),
        kpis=[('Ativos', 'Em vigor', 'fa-circle-check', 'ativo', 'count'), ('Pendentes', 'Aguardam aprovação', 'fa-hourglass-half', 'pendente', 'count'), ('Bloqueados', 'Acesso negado', 'fa-ban', 'bloqueado', 'count')]),
    'planejamento': dict(icon='fa-bullseye', fields=[
        campo('name', 'Item', 'title', samples=['Plano de ensino 2027', 'Meta institucional 3', 'PDI do colaborador', 'Dotação de manutenção', 'Nota de empenho']),
        campo('person', 'Responsável', 'person'),
        campo('code', 'Plano nº', 'code', prefix='PLN'),
        campo('valor', 'Valor', 'money', min=500, max=250000),
        campo('execucao', 'Execução', 'pct', min=0, max=100),
        enum('ano', 'Ano', ['2026', '2027']),
        campo('status', 'Situação', 'status')],
        statuses=st(('planejado', 'Planejado', 'blue'), ('em_execucao', 'Em execução', 'amber'), ('concluido', 'Concluído', 'emerald'), ('suspenso', 'Suspenso', 'slate')),
        kpis=[('Planejados', 'Aguardando início', 'fa-calendar', 'planejado', 'count'), ('Em execução', 'Em andamento', 'fa-person-running', 'em_execucao', 'count'), ('Concluídos', 'Metas entregues', 'fa-flag-checkered', 'concluido', 'count')]),
    'generico': dict(icon='fa-table-list', fields=[
        campo('name', 'Nome', 'title', samples=['Registro 1', 'Registro 2', 'Registro 3', 'Registro 4', 'Registro 5']),
        campo('person', 'Responsável', 'person'),
        campo('code', 'Referência', 'code', prefix='REF'),
        enum('unidade', 'Unidade', ['Centro', 'Norte', 'Sul']),
        campo('atualizado', 'Atualizado em', 'date', **{'from': -60, 'to': 0}),
        campo('status', 'Situação', 'status')],
        statuses=st(('ativo', 'Ativo', 'emerald'), ('pendente', 'Pendente', 'amber'), ('inativo', 'Inativo', 'slate')),
        kpis=[('Ativos', 'Em vigor', 'fa-circle-check', 'ativo', 'count'), ('Pendentes', 'Aguardam ação', 'fa-hourglass-half', 'pendente', 'count'), ('Inativos', 'Fora de uso', 'fa-box-archive', 'inativo', 'count')]),
}

# Ordem importa: o primeiro domínio cujo padrão casa com o texto da tela (e da ficha) é usado.
REGRAS_DOMINIO = [
    ('contabil', r'contábil|contabil|plano de contas|lançamento|razão|balancete|fechamento|tributo|retenç|obrigaç|nfs|fiscal'),
    ('financeiro', r'financ|cobran|título|titulo|mensalidade|pagamento|boleto|pix|cart[aã]o|caixa|cheque|conciliação|\bdre\b|gateway|split|fatura|receita|faturamento|carteira|régua|multa'),
    ('sst', r'\bsst\b|ocupacional|\baso\b|\bepi\b|\bcat\b|medicina|segurança do trabalho|\bnr-?\d|pgr'),
    ('pessoas', r'pessoas|colaborador|folha|ponto|férias|ferias|\brh\b|hcm|recrut|desempenho|admiss|afastament|rescis|departamento pessoal|benef|funcionári'),
    ('patrimonio', r'patrim|\bbens?\b|depreci|inventário|frota|veículo|veiculo|manutenç|\brotas?\b|reserva de veículo'),
    ('suprimentos', r'suprimento|requisi|cotaç|cotac|pedido de compra|almoxarif|estoque|merenda|compra|fornecedor'),
    ('contratos', r'contrato|aditivo'),
    ('biblioteca', r'biblioteca|acervo|empréstim|emprestim|livro'),
    ('simulados', r'simulad|prova|questão|questao|gabarito|ranking|correção|correcao'),
    ('atendimento', r'atendimento|\bsac\b|helpdesk|chat|ticket|chamado|base de conhecimento|\bsla\b|protocolo|solicitação'),
    ('academico', r'matr[ií]cul|turma|grade|diário|diario|boletim|conselho|calendário|calendario|evento|plano de aula|plano de ensino|estágio|estagio|\btcc\b|prontuário|portfólio|portfolio|preceptoria|pastoral|aula|curso|disciplina|avalia|ocorrênci|censo|aluno|ensino|sistema avaliativo|eletiva'),
    ('documentos', r'documento|declara|histórico|historico|ofício|oficio|tramita|emiss|transfer|enturma|processo seletivo|lista de espera|ficha cadastral|modelo'),
    ('planejamento', r'planejamento|plano institucional|\bpdi\b|empenho|dotação|dotacao|liquidação|liquidacao|meta'),
    ('seguranca', r'acesso|\bmfa\b|auditoria|\bdpo\b|privacidade|titular|\bti\b|tecnologia|backup|certificado|integra|configura|banco de dados|bancos|sess|break|monitoramento|incidente|cofre|pentest|intrus|build|slsa|exclusão lógica|navegação|arquitetura|implementa|segredo|portaria|domínio|dominio'),
]


def dominio_de(texto):
    t = texto.lower()
    for nome, padrao in REGRAS_DOMINIO:
        if re.search(padrao, t):
            return nome
    return 'generico'


def tela_spec(nome, desc, ficha_titulo, arq, dom):
    base = DOMINIOS[dom]
    campos = base['fields']
    tem_money = next((c['key'] for c in campos if c['type'] == 'money'), None)
    tem_date = next((c['key'] for c in campos if c['type'] in ('date', 'datetime')), None)
    enums = [c for c in campos if c['type'] == 'enum']
    chave_enum = enums[0]['key'] if enums else None
    kpis = []
    for label, sub, icone, status_id, unidade in base['kpis']:
        if unidade == 'money' and tem_money:
            valor = {'agg': 'sum', 'field': tem_money, 'where': {'status': status_id}}
            un = 'money'
        else:
            valor = {'agg': 'count', 'where': {'status': status_id}}
            un = 'count'
        kpis.append({'label': label, 'sub': sub, 'icon': icone, 'tone': 'blue', 'value': valor, 'unitLabel': 'Registros', 'unit': un})
    desc_curta = (desc or ficha_titulo)[:180]
    spec = {
        'title': nome, 'icon': base['icon'], 'currency': 'BRL', 'create': arq != 'painel',
        'entity': {'singular': nome, 'plural': nome, 'icon': base['icon'], 'newLabel': 'Novo registro'},
        'banner': {'icon': base['icon'], 'title': nome, 'desc': desc_curta, 'pill': '{count} registros'},
        'titleField': 'name', 'codeField': 'code', 'subField': chave_enum or 'status', 'statusField': 'status',
        'stageField': 'status', 'count': 24,
        'fields': campos, 'statuses': base['statuses'], 'stages': base['statuses'], 'kpis': kpis,
        'breakdown': {'by': chave_enum or 'status', 'title': 'Distribuição', 'desc': 'Distribuição atual', 'icon': 'fa-layer-group'},
        'cardFields': [c['key'] for c in campos if c['key'] not in ('name', 'status', 'code')][:2],
        'cardLine': chave_enum or 'status',
        'kanbanTitle': nome, 'kanbanDesc': desc_curta,
        'kanbanValue': tem_money, 'kanbanDate': tem_date,
        'drawer': {'metrics': [k for k in (tem_money, tem_date) if k],
                   'sections': [{'title': 'Registro', 'icon': 'fa-id-card', 'fields': [c['key'] for c in campos if c['key'] not in ('name',)]}]},
        'form': [c['key'] for c in campos if c['key'] not in ('status', 'code')],
        'analytics': [
            {'title': 'Por ' + (enums[0]['label'].lower() if enums else 'situação'), 'desc': 'Situação atual', 'by': chave_enum or 'status', 'type': 'bar', 'measure': {'agg': 'count', 'unit': 'count'}},
            {'title': 'Por situação', 'desc': 'Distribuição por status', 'by': 'status', 'type': 'doughnut', 'measure': {'agg': 'count', 'unit': 'count'}},
        ],
    }
    if chave_enum is None:
        spec.pop('breakdown')
    return spec


def aba_inicial(arq):
    return {'painel': 'kpi', 'kanban': 'kanban'}.get(arq, 'table')


def pagina(nome, spec, portal, modulo, rota, arq, ficha_rel, sdd_rel, tok, bun, js):
    dados = json.dumps(spec, ensure_ascii=False).replace('</', '<\\/')
    return f'''<!doctype html>
<html lang="pt-BR" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(nome)} · {html.escape(modulo)}</title>
<link rel="stylesheet" href="{tok}">
<link rel="stylesheet" href="{bun}">
<script src="{js}"></script>
<style>html,body{{margin:0}} #main-viewport{{padding:14px 16px 24px}} .pg-fonte{{font:12px/1.5 Inter,system-ui,sans-serif;color:var(--ttsc-text-muted);padding:0 16px 24px}} .pg-fonte a{{color:var(--ttsc-accent-text)}}</style>
</head>
<body>
<main id="main-viewport" class="bg-slate-50">
  <div id="model-page" class="space-y-3.5" aria-live="polite"></div>
  <p class="pg-fonte">Tela gerada a partir de <a href="{ficha_rel}">{html.escape(modulo)}</a> (SDD v2: <a href="{sdd_rel}">índice</a>). Registros de exemplo.</p>
</main>
<script>
  (function () {{
    var SPEC = {dados};
    TTSCModelKit.syncTheme();
    TTSCModelKit.render(
      {{ portal: {{ label: {json.dumps(portal, ensure_ascii=False)} }}, module: {{ label: {json.dumps(modulo, ensure_ascii=False)} }}, page: {{ label: {json.dumps(nome, ensure_ascii=False)}, route: {json.dumps(rota, ensure_ascii=False)} }} }},
      SPEC, {{}}
    );
    TTSCModelKit.switchTab({json.dumps(aba_inicial(arq))});
  }})();
</script>
</body>
</html>
'''


def main():
    fichas = []
    for caminho in sorted(glob.glob(os.path.join(KIT, '**', '*.md'), recursive=True)):
        if re.match(r'^(README|MODELO)', os.path.basename(caminho)):
            continue
        cab, telas = ler_ficha(caminho)
        if telas:
            fichas.append((caminho, os.path.relpath(caminho, KIT).replace(os.sep, '/'), cab, telas))
    if os.path.isdir(OUT):
        import shutil
        shutil.rmtree(OUT)
    indice, total = [], 0
    for caminho, rel, cab, telas in fichas:
        portal = re.sub(r'\s*\(`[^`]*`\)', '', cab.get('Portal', rel.split('/')[0])).strip()
        modulo = cab['titulo']
        pasta = os.path.join(OUT, rel[:-3])
        os.makedirs(pasta, exist_ok=True)
        for nome, desc in telas:
            arq = arquetipo(nome, desc)
            dom = dominio_de(' '.join([portal, cab.get('Área', ''), modulo, nome, desc]))
            spec = tela_spec(nome, desc, modulo, arq, dom)
            fn = os.path.join(pasta, slug(nome) + '.html')
            d = os.path.dirname(fn)
            rel_ = lambda alvo: os.path.relpath(alvo, d).replace(os.sep, '/')
            rota = '/' + '/'.join(slug(x) for x in rel[:-3].split('/'))
            src = pagina(nome, spec, portal, modulo, rota, arq, rel_(caminho), rel_(os.path.join(ROOT, 'docs', 'v2', '00-README.md')),
                         rel_(TOKENS), rel_(BUNDLE_CSS), rel_(BUNDLE_JS))
            open(fn, 'w', encoding='utf8').write(src)
            total += 1
            indice.append((portal, modulo, nome, arq, dom, rel_(fn) if False else os.path.relpath(fn, OUT).replace(os.sep, '/')))
    grupos = {}
    for portal, modulo, nome, arq, dom, link in indice:
        grupos.setdefault((portal, modulo), []).append((nome, arq, dom, link))
    corpo = ''
    for (portal, modulo), itens in grupos.items():
        lis = ''.join(f'<li><a href="{html.escape(l)}">{html.escape(n)}</a> <small>({a} · {d})</small></li>' for n, a, d, l in itens)
        corpo += f'<section><h3>{html.escape(portal)} · {html.escape(modulo)}</h3><ul>{lis}</ul></section>'
    idx = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Páginas geradas do kit-starter</title><link rel="stylesheet" href="../components/__tokens.css"><link rel="stylesheet" href="../components/bundle.css">
<style>body{{font:14px/1.5 Inter,system-ui,sans-serif;margin:0;padding:20px;background:var(--ttsc-canvas);color:var(--ttsc-text)}} li{{margin:2px 0}} small{{color:var(--ttsc-text-muted)}} h3{{margin:18px 0 4px}}</style></head>
<body><h1>Páginas geradas do kit-starter</h1><p>{total} telas a partir de {len(fichas)} fichas. Cada tela usa o renderizador TTSCModelKit do design system.</p>{corpo}</body></html>'''
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(idx)
    print('fichas com telas:', len(fichas), '| páginas:', total)


if __name__ == '__main__':
    main()
