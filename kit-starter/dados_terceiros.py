"""Fichas do Portal de Terceiros (`portal-de-terceiros.`): uma ficha por área."""
T = 'terceiros/'
DOM = 'entidade: banco da unidade; o prestador vê **só o que é da própria organização e do contrato vinculado**; nunca financeiro interno, contábil, folha ou dado de aluno ([31]({31}), seção 2.6; [38]({38}), seção 6)'
PAP = '- `thirdparty` (nível 0, contrato vinculado) e `thirdparty.manager` (nível 1, gestão de entregas e faturas do contrato) ([78]({78}), seção 4.6; papéis do prestador em [38]({38}), seção 2).'
MODULOS = [
    dict(arquivo=T + 'faturamento-de-servicos.md', area='Faturamento de serviços', dominio=DOM, titulo='Faturamento de serviços',
         objetivo='Enviar NF-e de serviço, acompanhar pagamento e extrato.',
         telas="- **Enviar nota** (upload XML ou PDF vinculado ao pedido ou ordem de serviço).\n- **Pagamentos** (estado da liquidação).\n- **Extrato** (por período).",
         papeis=PAP, regras="- Recebe só pagamento liquidado ([37]({37}), seção 6; [34]({34}), seção 8).", fontes=[('34', '5'), ('34', '8'), ('38', '1')]),
    dict(arquivo=T + 'pedidos-e-contratos.md', area='Pedidos e contratos', dominio=DOM, titulo='Pedidos e contratos',
         objetivo='Pedidos de compra pendentes e contratos em vigor da própria organização.',
         telas="- **Pedidos** (aceitar, informar prazo de entrega).\n- **Contratos** (leitura, aditivos, assinatura).",
         papeis=PAP, regras="- Contrato e unidades ([38]({38}), seção 4); páginas do contrato ([33]({33}), seção 9).", fontes=[('38', '4'), ('33', '9')]),
    dict(arquivo=T + 'documentos-da-empresa.md', area='Documentos da empresa', dominio=DOM, titulo='Documentos da empresa',
         objetivo='Certidões, contrato social, alvarás e seguro com validade e alerta.',
         telas="- **Documentos** (lista com validade; enviar nova versão).\n- **Alertas de vencimento**.",
         papeis=PAP, regras="- Habilitação depende de documentos válidos ([38]({38}), seção 5).", fontes=[('38', '5')]),
    dict(arquivo=T + 'prestacao-de-servico.md', area='Prestação de serviço', dominio=DOM, titulo='Prestação de serviço',
         objetivo='Ordens de serviço, relatórios de execução e cronograma, com regras por tipo de prestador.',
         telas="- **Ordens de serviço** (aceitar, executar, concluir com evidência).\n- **Relatórios de execução**.\n- **Cronograma** (calendário).",
         papeis=PAP, regras="- Regras específicas por tipo de prestador ([38]({38}), seção 3).", fontes=[('38', '3')]),
    dict(arquivo=T + 'chamados.md', area='Chamados', dominio=DOM, titulo='Chamados',
         objetivo='Abrir chamado de manutenção e pedir acesso à unidade.',
         telas="- **Meus chamados** (modelo único de ticket).\n- **Pedir acesso à unidade** (pessoas, datas, horários; aprovação pela portaria).",
         papeis=PAP, regras="- Atendimento ([31]({31}), seção 3.7); acesso físico ([35]({35}), seção 4).", fontes=[('32', '2.8'), ('35', '4')]),
    dict(arquivo=T + 'configuracoes-e-integracoes.md', area='Configurações e integrações', dominio=DOM, titulo='Configurações e integrações',
         objetivo='Dados da empresa, responsáveis técnicos, dados bancários (com MFA) e integrações via API.',
         telas="- **Dados da empresa**.\n- **Responsáveis técnicos**.\n- **Dados bancários** (alteração com MFA e aviso à entidade).\n- **Integrações via API** (tokens com escopo do contrato).",
         papeis=PAP, regras="- Dados bancários exigem MFA ([31]({31}), seção 2.6); tokens de API ([06]({06}), seção 8).", fontes=[('06', '8'), ('38', '6')]),
    dict(arquivo=T + 'habilitacao-e-acesso.md', area='Habilitação e acesso', dominio=DOM, titulo='Habilitação e acesso',
         objetivo='Cadastro e habilitação do prestador, pessoas e papéis do prestador, tipo de prestador e perfil.',
         telas="- **Habilitação** (etapas e estado).\n- **Pessoas do prestador** (convidar, papéis, desligar).\n- **Meu perfil** ([76]({76})).",
         papeis=PAP, regras="- Modelo, ciclo de vida e segregação ([38]({38}), seções 1, 5 e 6).", fontes=[('38', None), ('76', None)]),
]
