"""Fichas do Portal dos Pais e Responsáveis (`portal-dos-responsaveis.`): uma ficha por área."""
R = 'responsaveis/'
DOM = 'entidade: banco da unidade; o responsável vê **só dependentes com vínculo ativo de responsabilidade**; dependente sem vínculo não aparece ([78]({78}), seção 4.5; [07]({07}))'
PAP = '- `guardian` (nível 0, escopo próprio e dependentes vinculados) ([78]({78}), seção 4.5).'
MODULOS = [
    dict(arquivo=R + 'acompanhamento.md', area='Acompanhamento', dominio=DOM, titulo='Acompanhamento',
         objetivo='Notas, faltas, ocorrências, comunicados e entradas e saídas da portaria dos dependentes; tarefas e prazos (DP-06).',
         telas="- **Início da família** (seletor de dependente; resumo de notas, faltas, avisos, faturas).\n- **Notas e boletim**.\n- **Faltas** (justificar falta).\n- **Ocorrências** (ver e contestar no prazo; nome de terceiro não aparece).\n- **Comunicados** (com confirmação de leitura).\n- **Portaria** (entradas e saídas; autorizações de retirada).\n- **Tarefas** (prazos e entregas, sem poder entregar, DP-06).",
         papeis=PAP, regras="- Só dependentes com vínculo ativo; ocorrência com sigilo ([63]({63}), seção 6).",
         fontes=[('62', '7'), ('61', '4'), ('61', '7'), ('63', '6'), ('63', '8'), ('35', '4'), ('57', '4')]),
    dict(arquivo=R + 'biblioteca-e-simulados.md', area='Biblioteca e simulados', dominio=DOM, titulo='Biblioteca e simulados',
         objetivo='Empréstimos e desempenho em simulados dos dependentes (somente leitura).',
         telas="- **Empréstimos dos filhos** (prazos e atrasos).\n- **Desempenho em simulados** (resultados liberados).",
         papeis=PAP, regras="- Somente leitura.", fontes=[('68', '11'), ('47', '7'), ('47', '8')]),
    dict(arquivo=R + 'protocolos-da-familia.md', area='Protocolos da família', dominio=DOM, titulo='Protocolos da família',
         objetivo='Requerimentos da família: mudança de turno, saída antecipada, documentos e outros tipos configurados.',
         telas="- **Protocolos** (lista por dependente).\n- **Novo requerimento** (tipo, dependente, justificativa, anexos).\n- **Autorizar saída antecipada** (com pessoa autorizada e documento).",
         papeis=PAP, regras="- Serviço de protocolo ([31]({31}), seção 3.2).", fontes=[('31', '3.2'), ('46', 'M-06')]),
    dict(arquivo=R + 'financeiro-e-matricula.md', area='Financeiro e matrícula', dominio=DOM, titulo='Financeiro e matrícula',
         objetivo='Faturas dos filhos, Pix, boleto, cartão, débito automático, rematrícula online e assinatura do contrato.',
         telas="- **Central financeira** (faturas por dependente; pagar; comprovantes; débito automático se aprovado).\n- **Rematrícula online** (wizard M-02 por dependente).\n- **Assinar contrato** (provedor de assinatura).",
         papeis=PAP, regras="- Bloqueio parcial por inadimplência: rematrícula, documentação e comunicação continuam ([26]({26}), seção 3; M-09).",
         fontes=[('34', '8'), ('46', 'M-02'), ('46', 'M-09'), ('46', '6'), ('26', '4'), ('71', '11')]),
    dict(arquivo=R + 'privacidade-e-menores.md', area='Privacidade e menores', dominio=DOM, titulo='Privacidade e menores',
         objetivo='Consentimento de imagem, dados dos filhos e direitos do titular exercidos pelo responsável legal.',
         telas="- **Consentimentos** (imagem por finalidade: site, redes, mural; revogável).\n- **Dados dos filhos** (ver e pedir correção).\n- **Solicitações LGPD**.",
         papeis=PAP, regras="- Termo de imagem por finalidade ([32]({32}), seção 3.2).", fontes=[('32', '3.2'), ('32', '3.3'), ('32', '4'), ('07', '4')]),
    dict(arquivo=R + 'agenda-e-comunicacao.md', area='Agenda e comunicação', dominio=DOM, titulo='Agenda e comunicação',
         objetivo='Horário e calendário dos dependentes, eventos e autorizações, notificações e perfil.',
         telas="- **Horário dos filhos**.\n- **Calendário e eventos** (inscrever dependente com autorização).\n- **Autorizações** (eventos, pastoral, passeios).\n- **Notificações**.\n- **Meu perfil** ([76]({76})).",
         papeis=PAP, regras="- Menor só participa com autorização do responsável ([43]({43}), seção 6).",
         fontes=[('60', '5'), ('58', '6'), ('43', '5'), ('43', '6'), ('57', '3.3'), ('57', '4'), ('76', None)]),
]
