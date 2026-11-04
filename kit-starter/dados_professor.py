"""Fichas do Portal do Professor (`portal-do-professor.`): uma ficha por área."""
P = 'professor/'
DOM = 'entidade: banco da unidade; o professor vê **só as turmas e disciplinas em que tem vínculo ativo** ([17]({17}), seção 4.4; [06]({06}), seção 12)'
PAP = '- `teacher` (nível 1, escopo turma): ações das próprias turmas.\n- `teacher.coordinator` (nível 2, unidade): aprova planos e lançamentos de nível 1 da unidade ([78]({78}), seção 4.3).'
MODULOS = [
    dict(arquivo=P + 'classe.md', area='Classe', dominio=DOM, titulo='Classe',
         objetivo='Espaço da turma para o professor: lista de turmas e disciplinas vinculadas, mural de avisos, materiais de apoio e tarefas com entrega (DP-06).',
         telas="""- **Minhas turmas** (cards por turma e disciplina): horário, nº de alunos, pendências do diário, próximas tarefas.
- **Turma — visão** (página com abas): *Alunos* (lista com foto só com termo de imagem), *Mural*, *Materiais*, *Tarefas*, *Diário* (atalho).
- **Mural** (lista de avisos; criar aviso com anexos; comentários desligados por padrão, DP-06).
- **Materiais** (lista e upload pelo armazenamento, com antivírus e limite).
- **Tarefas** (DataTable): título, prazo, entregas, corrigidas; **Nova tarefa** (instruções, prazo, anexos, forma de entrega, se é avaliação).
- **Entregas da tarefa** (DataTable por aluno: entregue, atrasada, não entregue; correção com nota e comentário; sugestão de IA opcional).""",
         papeis=PAP, regras="""- DP-06 do [80]({80}) rege mural, materiais e tarefas.
- Nota da tarefa só entra no diário se a tarefa for uma avaliação do sistema avaliativo ([59]({59}), seção 4).
- Arquivos pelo armazenamento ([21]({21}), seção 3).""",
         fontes=[('80', None), ('21', '3.3'), ('21', '3.9'), ('59', '4')]),
    dict(arquivo=P + 'diario.md', area='Diário', dominio=DOM, titulo='Diário',
         objetivo='Lançar frequência, conteúdo da aula, notas e plano de aula das próprias turmas, até o fechamento do diário.',
         telas="""- **Diário da turma** (página por turma, disciplina e período): aulas do período com estado.
- **Chamada** (lista de alunos com presente, falta, atraso; QR Code de 5 minutos; presença pendente).
- **Conteúdo da aula** (texto e vínculo com o plano de aula; conteúdo realizado).
- **Notas** (grade aluno × avaliação; média calculada pelo sistema avaliativo; recuperação).
- **Plano de aula** (formulário com estados e prazo; envio para revisão).
- **Fechar diário** (verificação de pendências; após fechar, só reabertura pela coordenação).""",
         papeis=PAP, regras="""- Nota só pelo professor da turma ([22]({22}), seção 5); lançamento só no período aberto ([17]({17}), seção 4.2).
- QR Code válido por 5 minutos por padrão; geolocalização só com consentimento.
- Diário fechado só reabre pela coordenação com motivo ([17]({17}), seção 4.3).""",
         fontes=[('61', '2'), ('61', '3'), ('61', '4'), ('61', '5'), ('61', '6'), ('61', '7'), ('64', '4'), ('64', '7')]),
    dict(arquivo=P + 'simulados.md', area='Simulados', dominio=DOM, titulo='Simulados',
         objetivo='Elaborar questões (com revisão antes de publicar), agendar simulados para as próprias turmas e ver resultados e correção.',
         telas="- **Minhas questões** (DataTable com situação).\n- **Editor de questão**.\n- **Agendar simulado** (turma, prova, data, duração).\n- **Resultados da turma** (dashboard; correção dissertativa com sugestão de IA e nota confirmada pelo professor).",
         papeis=PAP, regras="- Questão passa por revisão antes de publicar ([31]({31}), seção 3.6).\n- IA sugere, o professor confirma ([27]({27})).",
         fontes=[('47', '4'), ('47', '6'), ('47', '7'), ('47', '8'), ('31', '3.6')]),
    dict(arquivo=P + 'biblioteca.md', area='Biblioteca', dominio=DOM, titulo='Biblioteca',
         objetivo='Consultar o acervo e indicar leituras para as próprias turmas (somente leitura do acervo).',
         telas="- **Pesquisa de acervo** (busca com disponibilidade).\n- **Indicações de leitura** (lista por turma; criar indicação).\n- **Meus empréstimos** (do próprio professor).",
         papeis=PAP, regras="- Somente leitura do acervo ([31]({31}), seção 2.3).", fontes=[('68', '5'), ('68', '11')]),
    dict(arquivo=P + 'protocolos-e-pedidos.md', area='Protocolos e pedidos', dominio=DOM, titulo='Protocolos e pedidos',
         objetivo='Pedir material, reservar laboratório ou equipamento e registrar justificativas pelo serviço de protocolo.',
         telas="- **Meus pedidos** (lista com estado e protocolo).\n- **Solicitar material** (formulário que gera requisição em suprimentos).\n- **Reservar ambiente ou equipamento** (calendário de disponibilidade, [44]({44})).\n- **Justificativa** (formulário com anexo).",
         papeis=PAP, regras="- Usa o serviço de protocolo ([31]({31}), seção 3.2); reserva com conflito é recusada ([44]({44})).",
         fontes=[('31', '3.2'), ('44', '3'), ('44', '4')]),
    dict(arquivo=P + 'documentos-e-pessoal.md', area='Documentos e pessoal', dominio=DOM, titulo='Documentos e pessoal',
         objetivo='Dados do próprio docente: declarações, contrato de trabalho, holerite e ponto.',
         telas="- **Declarações** (pedido e download).\n- **Contrato de trabalho** (leitura e aditivos).\n- **Holerites** (lista por competência e PDF).\n- **Ponto** (espelho e pedido de ajuste com motivo).\n- **Plano de desenvolvimento (PDI)** próprio ([37]({37}), seção 4).",
         papeis="- `teacher`: só os próprios dados.", regras="- Só dados do próprio docente ([31]({31}), seção 2.3); holerite só consulta ([34]({34}), seção 8).",
         fontes=[('39', '6'), ('34', '8'), ('37', '6')]),
    dict(arquivo=P + 'relatorios.md', area='Relatórios', dominio=DOM, titulo='Relatórios',
         objetivo='Rendimento da turma e ficha individual do aluno das turmas vinculadas.',
         telas="- **Rendimento da turma** (dashboard: médias, distribuição, frequência).\n- **Ficha individual** (notas, faltas, ocorrências do aluno na disciplina).",
         papeis=PAP, regras="- Relatórios por portal ([69]({69}), seção 6); só turmas vinculadas.", fontes=[('69', '2'), ('69', '6'), ('56', '5')]),
    dict(arquivo=P + 'agenda-e-comunicacao.md', area='Agenda e comunicação', dominio=DOM, titulo='Agenda e comunicação',
         objetivo='Horário próprio e das turmas, calendário, aulas online, notificações e perfil do professor.',
         telas="- **Meu horário** (grade semanal; pedir troca de aula).\n- **Calendário** (eventos das próprias turmas; propor evento da turma).\n- **Aulas online** (criar e entrar na sessão; gravação com consentimento).\n- **Notificações** (central e preferências).\n- **Meu perfil** ([76]({76})).",
         papeis=PAP, regras="- Não vê horário de outro professor ([60]({60}), seção 5).",
         fontes=[('60', '5'), ('58', '6'), ('40', '4'), ('40', '5'), ('40', '7'), ('57', '3.3'), ('57', '4'), ('76', None)]),
    dict(arquivo=P + 'acompanhamento-pedagogico.md', area='Acompanhamento pedagógico', dominio=DOM, titulo='Acompanhamento pedagógico',
         objetivo='Ocorrências da turma, orientação de estágio e TCC, preceptoria (quando o professor é preceptor), portfólio dos alunos, formulários e pastoral.',
         telas="- **Ocorrências** (registrar ocorrência da própria turma).\n- **Orientandos** (estágio e TCC: horas, versões, banca).\n- **Preceptoria** (avaliar residentes vinculados, tutoria, metas, evidências).\n- **Portfólio** (avaliar evidências dos alunos).\n- **Formulários** (responder e, quando permitido, criar para a turma).\n- **Pastoral** (confirmar presença na própria escala).",
         papeis=PAP, regras="- Cada módulo só mostra alunos com vínculo à turma ou orientação do professor.",
         fontes=[('63', '8'), ('65', '4'), ('42', '5'), ('66', '4'), ('41', '6'), ('43', '5')], linhas_extra=['Preceptor']),
]
