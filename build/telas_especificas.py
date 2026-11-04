"""Especificações específicas de telas (campos, cálculos, situações e permissões).

Substituem o padrão por domínio de gen_paginas.py. Chave: (caminho da ficha sem .md, nome da tela).
Cada permissão vem da ficha de origem e do doc 78. Onde a ficha não decide, a decisão está no doc 80.
"""

PAPEIS_COMERCIAIS = [
    ('platform.sales.ae', 'Vendedor (nível 1, carteira própria)'),
    ('platform.sales.manager', 'Gerente comercial (nível 2, equipe)'),
    ('platform.finance', 'Financeiro da empresa (nível 1)'),
    ('platform.developer', 'Desenvolvedor (nível 7)'),
]

def _situacao_meta(pct):
    return 'atingida' if pct >= 100 else ('no_prazo' if pct >= 70 else 'abaixo')

META_STATUS = [
    {'id': 'atingida', 'label': 'Atingida', 'tone': 'emerald', 'weight': 2},
    {'id': 'no_prazo', 'label': 'No ritmo', 'tone': 'blue', 'weight': 2},
    {'id': 'abaixo', 'label': 'Abaixo do ritmo', 'tone': 'rose', 'weight': 2},
]

ESPECIFICAS = {
    ('desenvolvedor/comercial-da-plataforma/comissoes', 'Metas'): dict(
        titulo='Metas', icone='fa-bullseye',
        descricao='Meta e realizado por vendedor e período. O realizado vem das oportunidades ganhas, não é digitado.',
        campos=[
            {'key': 'name', 'label': 'Meta', 'type': 'title', 'samples': ['Meta mensal de propostas', 'Meta trimestral de matrículas']},
            {'key': 'person', 'label': 'Vendedor', 'type': 'person'},
            {'key': 'code', 'label': 'Meta nº', 'type': 'code', 'prefix': 'MET'},
            {'key': 'periodo', 'label': 'Período (AAAA-MM)', 'type': 'enum', 'values': [
                {'id': '2026-09', 'label': '2026-09', 'tone': 'slate', 'weight': 1},
                {'id': '2026-10', 'label': '2026-10', 'tone': 'blue', 'weight': 2},
                {'id': '2026-11', 'label': '2026-11', 'tone': 'emerald', 'weight': 3}]},
            {'key': 'meta', 'label': 'Meta (R$)', 'type': 'money', 'min': 20000, 'max': 90000},
            {'key': 'realizado', 'label': 'Realizado (R$)', 'type': 'money', 'min': 0, 'max': 120000, 'calc_from': 'oportunidades ganhas'},
            {'key': 'percentual', 'label': 'Percentual', 'type': 'pct', 'calc': ('realizado', 'meta')},
            {'key': 'status', 'label': 'Situação', 'type': 'status', 'calc': 'situacao_meta'},
        ],
        statuses=META_STATUS,
        kpis=[('Metas atingidas', 'Percentual igual ou acima de 100%', 'fa-trophy', 'atingida', 'count'),
              ('No ritmo', 'Entre 70% e 99%', 'fa-gauge-high', 'no_prazo', 'count'),
              ('Abaixo do ritmo', 'Menos de 70%', 'fa-triangle-exclamation', 'abaixo', 'count')],
        analise=[('Realizado por vendedor', 'Comparação com a meta', 'person', 'bar'),
                 ('Situação das metas', 'Distribuição', 'status', 'doughnut')],
        permissoes=[
            ('platform.sales.ae', 'Ver a própria meta e o próprio realizado', 'Ver metas dos colegas'),
            ('platform.sales.manager', 'Ver e cadastrar metas da equipe', 'Alterar meta já encerrada sem nova versão'),
            ('platform.finance', 'Nada nesta tela', 'Ver metas'),
            ('platform.developer', 'Ver todas as metas, com auditoria', 'Alterar realizado (é calculado)'),
        ],
    ),
    ('desenvolvedor/comercial-da-plataforma/comissoes', 'Acompanhamento'): dict(
        titulo='Acompanhamento', icone='fa-chart-line',
        descricao='Progresso de cada vendedor no período: realizado contra meta.',
        campos=[
            {'key': 'name', 'label': 'Vendedor', 'type': 'title', 'samples': ['Equipe Comercial Norte', 'Equipe Comercial Sul']},
            {'key': 'person', 'label': 'Responsável', 'type': 'person'},
            {'key': 'code', 'label': 'Referência', 'type': 'code', 'prefix': 'ACP'},
            {'key': 'meta', 'label': 'Meta (R$)', 'type': 'money', 'min': 20000, 'max': 90000},
            {'key': 'realizado', 'label': 'Realizado (R$)', 'type': 'money', 'min': 0, 'max': 120000},
            {'key': 'percentual', 'label': 'Percentual', 'type': 'pct', 'calc': ('realizado', 'meta')},
            {'key': 'status', 'label': 'Situação', 'type': 'status', 'calc': 'situacao_meta'},
        ],
        statuses=META_STATUS,
        kpis=[('Realizado da equipe', 'Soma no período', 'fa-sack-dollar', 'atingida', 'money'),
              ('Abaixo do ritmo', 'Vendedores abaixo de 70%', 'fa-triangle-exclamation', 'abaixo', 'count'),
              ('Metas atingidas', 'Vendedores em 100% ou mais', 'fa-trophy', 'atingida', 'count')],
        analise=[('Realizado contra meta', 'Por vendedor', 'person', 'bar'),
                 ('Situação', 'Distribuição', 'status', 'doughnut')],
        permissoes=[
            ('platform.sales.ae', 'Ver o próprio progresso', 'Ver progresso dos colegas'),
            ('platform.sales.manager', 'Ver o progresso da equipe', 'Exportar com dado de vendedor sem auditoria'),
            ('platform.finance', 'Nada nesta tela', 'Ver progresso'),
            ('platform.developer', 'Ver todas as equipes, com auditoria', 'Alterar percentual'),
        ],
    ),
    ('desenvolvedor/comercial-da-plataforma/comissoes', 'Regras de comissão'): dict(
        titulo='Regras de comissão', icone='fa-sliders',
        descricao='Percentual fixo, escalonado ou por plano. Toda alteração exige aprovação de outra pessoa.',
        campos=[
            {'key': 'name', 'label': 'Regra', 'type': 'title', 'samples': ['Percentual fixo sobre venda', 'Escalonada por faixa de meta', 'Por plano contratado']},
            {'key': 'person', 'label': 'Criada por', 'type': 'person'},
            {'key': 'code', 'label': 'Regra nº', 'type': 'code', 'prefix': 'REG'},
            {'key': 'tipo', 'label': 'Tipo', 'type': 'enum', 'values': [
                {'id': 'fixo', 'label': 'Fixo', 'tone': 'blue', 'weight': 3},
                {'id': 'escalonado', 'label': 'Escalonado', 'tone': 'purple', 'weight': 2},
                {'id': 'por_plano', 'label': 'Por plano', 'tone': 'amber', 'weight': 2}]},
            {'key': 'percentual', 'label': 'Percentual base', 'type': 'pct', 'min': 1, 'max': 12},
            {'key': 'status', 'label': 'Situação', 'type': 'status'},
        ],
        statuses=[
            {'id': 'rascunho', 'label': 'Rascunho', 'tone': 'slate', 'weight': 2},
            {'id': 'aguardando', 'label': 'Aguarda aprovação', 'tone': 'amber', 'weight': 2},
            {'id': 'vigente', 'label': 'Vigente', 'tone': 'emerald', 'weight': 2},
        ],
        kpis=[('Vigentes', 'Regras em uso', 'fa-circle-check', 'vigente', 'count'),
              ('Aguardam aprovação', 'Precisam de outra pessoa', 'fa-hourglass-half', 'aguardando', 'count'),
              ('Rascunhos', 'Em elaboração', 'fa-pen', 'rascunho', 'count')],
        analise=[('Regras por tipo', 'Quantidade', 'tipo', 'bar'),
                 ('Situação', 'Distribuição', 'status', 'doughnut')],
        permissoes=[
            ('platform.sales.ae', 'Nada nesta tela', 'Ver regras'),
            ('platform.sales.manager', 'Criar e editar rascunho de regra', 'Aprovar a própria regra'),
            ('platform.finance', 'Ver regras vigentes', 'Editar regra'),
            ('platform.developer', 'Aprovar regra criada por outra pessoa', 'Aprovar a própria regra'),
        ],
    ),
    ('desenvolvedor/comercial-da-plataforma/comissoes', 'Relatório de comissão a pagar'): dict(
        titulo='Relatório de comissão a pagar', icone='fa-file-invoice-dollar',
        descricao='Comissão a pagar por período. A comissão vai para o financeiro da plataforma, nunca para uma entidade.',
        campos=[
            {'key': 'name', 'label': 'Vendedor', 'type': 'title', 'samples': ['Equipe Comercial Norte', 'Equipe Comercial Sul']},
            {'key': 'person', 'label': 'Vendedor', 'type': 'person'},
            {'key': 'code', 'label': 'Comissão nº', 'type': 'code', 'prefix': 'COM'},
            {'key': 'periodo', 'label': 'Período', 'type': 'enum', 'values': [
                {'id': '2026-09', 'label': '2026-09', 'tone': 'slate', 'weight': 1},
                {'id': '2026-10', 'label': '2026-10', 'tone': 'blue', 'weight': 2}]},
            {'key': 'valor', 'label': 'Comissão (R$)', 'type': 'money', 'min': 300, 'max': 9000},
            {'key': 'status', 'label': 'Situação', 'type': 'status'},
        ],
        statuses=[
            {'id': 'a_pagar', 'label': 'A pagar', 'tone': 'amber', 'weight': 2},
            {'id': 'pago', 'label': 'Pago', 'tone': 'emerald', 'weight': 2},
            {'id': 'retido', 'label': 'Retido', 'tone': 'rose', 'weight': 2},
        ],
        kpis=[('A pagar', 'Comissões do período', 'fa-clock', 'a_pagar', 'money'),
              ('Pagas', 'Já liquidadas', 'fa-circle-check', 'pago', 'money'),
              ('Retidas', 'Aguardam conferência', 'fa-lock', 'retido', 'count')],
        analise=[('Comissão por período', 'Valor', 'periodo', 'bar'),
                 ('Situação', 'Distribuição', 'status', 'doughnut')],
        permissoes=[
            ('platform.sales.ae', 'Ver a própria comissão', 'Ver comissão dos colegas'),
            ('platform.sales.manager', 'Ver comissões da equipe', 'Liberar pagamento'),
            ('platform.finance', 'Liberar pagamento e exportar', 'Alterar valor calculado'),
            ('platform.developer', 'Ver todas, com auditoria', 'Liberar pagamento sem segundo aprovador'),
        ],
    ),
}
