"""Fichas do Portal de Gestão (`gestao.`). Usado por kit-starter/fichas_portais.py.

Placeholders: {NN} vira o caminho relativo do documento NN do SDD v2.
"""

A = 'gestao/academico/'
ACAD = 'Acadêmico'

MODULOS = [
    dict(
        arquivo=A + 'administracao-escolar-estrutura-academica.md', area=ACAD,
        titulo='Administração escolar (estrutura acadêmica)',
        objetivo='Cadastrar a estrutura acadêmica da unidade: tipos de curso (básico, técnico e superior, ACA-01), cursos, disciplinas, grades curriculares versionadas, projeto pedagógico (PPC), equivalências entre cursos e períodos letivos. É a base de turmas, diário, boletim, matrícula e relatórios ([55]({55}), seção 3, ordem 1).',
        telas="""- **Cursos** (lista com DataTable): nome, tipo de curso, nível, modalidade, situação, nº de grades; filtros por tipo e situação. Drawer de detalhe com abas *Dados*, *Grades*, *PPC*, *Equivalências*, *Histórico*.
- **Curso — formulário** (página): dados do curso, tipo de curso (regras do tipo na seção 13), carga horária total, regime (seriado, por módulo, por crédito), sistema avaliativo padrão.
- **Disciplinas** (lista): código, nome, carga horária, tipo (obrigatória, optativa, eletiva), pré-requisitos; ação *Nova versão*.
- **Grade curricular** (página por curso e versão): matriz por período/série com disciplinas, carga e pré-requisitos; estados rascunho → publicada → encerrada; publicar exige aprovação da gestão; grade publicada só muda por nova versão.
- **Projeto pedagógico (PPC)** (página com editor e anexos versionados).
- **Equivalências** (lista e formulário): disciplina de origem × disciplina de destino, carga mínima, validade.
- **Períodos letivos** (lista por ano): início, fim, etapas (bimestre, trimestre, semestre), datas de lançamento de nota; vínculo com o calendário ([58]({58})).
- **Painel da estrutura** (dashboard): cursos ativos, grades em rascunho, disciplinas sem professor, períodos sem calendário.""",
        papeis="""- `unit.manager`: aprovar e publicar grade, encerrar curso.
- `unit.coordinator`: cadastrar curso, disciplina, grade, PPC e equivalência; publicar só com aprovação.
- `unit.secretary`: consulta.
- `platform.developer` (portal do desenvolvedor): publicar modelos de tipo de curso e de sistema avaliativo, sem dado da entidade.""",
        regras="""- Turma aponta sempre para curso, grade e **versão** da grade ([60]({60}), seção 6).
- Grade publicada não é editada: mudança gera nova versão; alunos ficam na versão em que entraram.
- Período letivo depende do calendário da unidade ([58]({58})); nota só é lançada dentro do período aberto ([17]({17}), seção 4.2).
- Sistemas avaliativos ficam na ficha [regras de aprovação](regras-de-aprovacao-sistemas-avaliativos-boletim-e-conselho.md).""",
        fontes=[('59', None), ('17', '4'), ('55', None)],
        v1=['spec_gestao_academica_completo.md'],
        integracoes='- Turmas e grade ([60]({60})), calendário ([58]({58})), matrícula ([46]({46})), censo ([69]({69})), importação ([70]({70})).',
    ),
    dict(
        arquivo=A + 'pedagogico-coordenacao-e-diario.md', area=ACAD,
        titulo='Pedagógico (coordenação e diário)',
        objetivo='Acompanhar e supervisionar o diário escolar de todas as turmas da unidade: aulas, chamada, faltas e justificativas, notas, médias e fechamento do diário. O lançamento é do professor (portal do professor); a coordenação acompanha, cobra pendências, aprova justificativas e reabre o diário com motivo.',
        telas="""- **Painel pedagógico** (dashboard): diários pendentes por turma e professor, aulas sem conteúdo, chamadas pendentes, notas fora do prazo, alunos com frequência abaixo do mínimo.
- **Diários da unidade** (DataTable): turma, disciplina, professor, período, estado (`aberto`, `fechado`, `reaberto`), % de chamada e de conteúdo; drawer com o diário em leitura.
- **Justificativas de falta** (fila com aprovação): documento anexado, período, decisão com motivo.
- **Reabrir diário** (modal): motivo obrigatório, prazo de reabertura, aviso ao professor; gera evento de auditoria.
- **Alunos em risco** (lista): frequência e média abaixo do limite, com encaminhamento à coordenação ou ao responsável.""",
        papeis="""- `unit.coordinator`: acompanhar, aprovar justificativa, reabrir diário com motivo.
- `unit.manager`: leitura e relatórios.
- `teacher` (portal do professor): lança chamada, conteúdo e nota **só das turmas vinculadas**; nota só pelo professor da turma ([22]({22}), seção 5).""",
        regras="""- Estados do diário: `aberto`, `fechado`, `reaberto` (com justificativa) ([17]({17}), seção 4.3).
- Presença por QR Code válida por 5 minutos por padrão; geolocalização só com consentimento ([17]({17}), seção 4.2).
- A coordenação **não altera** nota nem chamada do professor; corrige por reabertura do diário, e o professor relança.""",
        fontes=[('61', None)],
        v1_em=['gestao/academico/administracao-escolar-estrutura-academica.md'],
    ),
    dict(
        arquivo=A + 'calendario-e-eventos.md', area=ACAD,
        titulo='Calendário e eventos',
        objetivo='Definir o calendário letivo da unidade (dias letivos, feriados, recesso, períodos) e os eventos escolares com inscrição, presença e certificado.',
        telas="""- **Calendário letivo** (calendário mensal e anual): dias letivos, não letivos, feriados e recesso; contador de dias letivos por período; publicar.
- **Eventos** (lista e calendário): título, tipo, público, local, inscrição, estado; kanban por estado.
- **Evento — formulário** (página): tipo (seção 13), público-alvo, limite de vagas, inscrição, aprovação exigida, recurso agendado ([44]({44})).
- **Inscrições e presença** (DataTable por evento): inscritos, autorização de responsável para menor, check-in, emissão de certificado.
- **Aprovações** (fila): eventos que exigem aprovação da gestão (público acima de 500, seção 13).""",
        papeis="""- `unit.manager`: definir calendário, aprovar evento.
- `unit.secretary`: períodos, dias não letivos, eventos e inscrições; emitir certificado.
- `unit.coordinator`: eventos pedagógicos (reunião de pais, conselho).""",
        regras="""- Evento só é publicado depois da aprovação da gestão quando o tipo exigir.
- Calendário de uma unidade não altera o de outra.
- Mudança de data publicada gera notificação ([57]({57})).""",
        fontes=[('58', None)],
    ),
    dict(
        arquivo=A + 'series-e-turmas-grade-de-horarios.md', area=ACAD,
        titulo='Séries e turmas (grade de horários)',
        objetivo='Criar turmas, cadastrar salas de referência, grupos de horários, enturmar alunos e montar, validar e publicar a grade de horários da unidade sem conflito de professor, sala ou turma.',
        telas="""- **Turmas** (DataTable): curso, grade e versão, série/período, turno, sala, vagas, ocupação, estado; ações abrir, encerrar.
- **Turma — formulário** (página): campos da seção 13 (cadastro), capacidade, sala de referência.
- **Salas** (lista): capacidade, recursos, acessibilidade (integra [44]({44})).
- **Grupos de horários** (lista e editor de tempos por turno).
- **Montagem da grade** (quadro semanal com arrastar e soltar): aulas por turma, professor e sala; validação de conflito em tempo real; carga docente (limite de 40 horas-aula por semana, [37]({37})).
- **Publicar grade** (modal): lista de conflitos bloqueantes; publicar exige aprovação da gestão; versão anterior preservada.
- **Consultas** (por professor, por sala, por turma) e **ocupação da unidade** (dashboard).""",
        papeis="""- `unit.manager`: aprovar grade, abrir e encerrar turma, ver ocupação.
- `unit.coordinator`: montar turmas, enturmar, montar e publicar grade, autorizar troca de professor.
- `unit.secretary`: enturmar com autorização, cadastrar sala, consultar grade; não cria turma nem aula.""",
        regras="""- Não se publica grade com conflito ([60]({60}), seção 4.2).
- Grade publicada só muda por nova versão.
- Enturmação respeita vaga com bloqueio de concorrência ([15]({15}), seção 7).""",
        fontes=[('60', None)],
    ),
    dict(
        arquivo=A + 'regras-de-aprovacao-sistemas-avaliativos-boletim-e-conselho.md', area=ACAD,
        titulo='Regras de aprovação (sistemas avaliativos, boletim e conselho de classe)',
        objetivo='Configurar os sistemas avaliativos (escalas, médias, conceitos, recuperação, regra de aprovação), emitir boletins, conduzir a recuperação paralela, o conselho de classe com ata e o fechamento e a reabertura do resultado final.',
        telas="""- **Sistemas avaliativos** (lista e editor): escala (nota ou conceito), fórmula de média por etapa e final, peso, arredondamento, frequência mínima, recuperação; simulador de cálculo.
- **Boletins** (DataTable por turma): emissão individual, em lote, parcial e oficial (tipos de emissão na seção 13); pré-visualização.
- **Recuperação paralela** (lista por turma e disciplina): alunos elegíveis, notas de recuperação, substituição conforme regra.
- **Conselho de classe** (página por turma): convocação e pauta, participantes, quadro de alunos com notas e frequência, decisão por aluno com motivo, ata com assinatura.
- **Resultado final** (DataTable): aprovado, reprovado, em recuperação, aprovado pelo conselho; fechar resultado; reabrir com motivo e aprovação.""",
        papeis="""- `unit.coordinator`: configurar sistema avaliativo (com aprovação da gestão), conduzir conselho, recuperação.
- `unit.manager`: aprovar sistema avaliativo, fechar e reabrir resultado.
- `unit.secretary`: emitir boletim.
- `teacher`: participa do conselho das próprias turmas.""",
        regras="""- Sistema avaliativo em uso por turma com nota lançada não é alterado; nova versão vale para o próximo período.
- Decisão do conselho exige motivo registrado por aluno e consta da ata.
- Resultado fechado só reabre com motivo, aprovação e auditoria ([62]({62}), seção 6).""",
        fontes=[('59', '4'), ('62', None)],
    ),
    dict(
        arquivo=A + 'ocorrencias-disciplinares.md', area=ACAD,
        titulo='Ocorrências disciplinares',
        objetivo='Registrar ocorrências disciplinares com tipo e gravidade, fluxo de análise, medidas educativas, contestação, afastamento e notificação ao responsável, com sigilo do relato e proteção de dado de terceiro.',
        telas="""- **Ocorrências** (DataTable): aluno, turma, tipo, gravidade, estado, data; filtros; relato mascarado na lista.
- **Nova ocorrência** (formulário): campos da seção 13 (4.1), envolvidos, testemunhas, anexos; dado de terceiro marcado.
- **Ocorrência — detalhe** (página): linha do tempo do fluxo, medidas, contestação, notificação ao responsável, decisão.
- **Denúncia de violência** (fluxo restrito): canal sigiloso e encaminhamento obrigatório (seção 13, 6.3).
- **Painel** (dashboard agregado, sem identificação): ocorrências por tipo, gravidade e turma.""",
        papeis="""- `unit.coordinator`: registrar, analisar, aplicar medida, notificar responsável.
- `unit.manager`: afastamento e decisões de gravidade alta.
- `teacher`: registrar ocorrência da própria turma.""",
        regras="""- Relato visível só a quem a seção 13 (6.1) permite; nome de terceiro não aparece para o responsável do outro aluno.
- Contestação do responsável ou aluno tem prazo e decisão fundamentada.
- Denúncia de violência segue o encaminhamento legal descrito na seção 13.""",
        fontes=[('63', None)],
    ),
    dict(
        arquivo=A + 'planos-de-aula-e-de-ensino.md', area=ACAD,
        titulo='Planos de aula e de ensino',
        objetivo='Receber, revisar e aprovar os planos de ensino (por disciplina e período) e os planos de aula (por aula), com prazos, conteúdo realizado e apoio opcional de IA.',
        telas="""- **Planos de ensino** (DataTable): disciplina, turma, professor, período, estado, prazo; fila de revisão.
- **Plano de ensino — revisão** (página): campos da seção 13 (3.1), comentários por campo, aprovar ou devolver com motivo.
- **Planos de aula** (DataTable por turma): data, aula, estado, conteúdo realizado × planejado.
- **Pendências de plano** (dashboard): planos atrasados por professor e turma.""",
        papeis="""- `unit.coordinator` e `teacher.coordinator`: revisar e aprovar.
- `teacher`: elaborar (portal do professor).""",
        regras="""- Plano de aula se relaciona ao plano de ensino aprovado (seção 13, 2).
- Conteúdo realizado alimenta o diário ([61]({61})).
- IA só sugere; o professor é autor e responsável (seção 13, 6; [27]({27})).""",
        fontes=[('64', None)],
    ),
    dict(
        arquivo=A + 'estagio-e-tcc.md', area=ACAD,
        titulo='Estágio e TCC',
        objetivo='Gerir estágios (obrigatórios quando o curso exigir, ACA-03) com termo, seguro, supervisão e horas, e o TCC com orientação, prazos, banca, versão final e repositório.',
        telas="""- **Estágios** (DataTable): aluno, empresa concedente (CNPJ), tipo, supervisor, horas cumpridas, estado.
- **Estágio — cadastro** (página): campos da seção 13 (2.2), apólice de seguro com validade, termo de compromisso com assinatura.
- **Horas e supervisão** (lista de registros com validação).
- **TCC** (DataTable): aluno, orientador, tema, estado, prazo.
- **Banca de defesa** (página): membros (inclusive externos, seção 13, 6), data, ata e nota.
- **Repositório de TCC** (lista pública da entidade, conforme autorização do autor).""",
        papeis="""- `unit.coordinator`: aprovar estágio e TCC, compor banca.
- `unit.secretary`: termos e documentos.
- `teacher`: orientar (portal do professor).""",
        regras="""- Estados do estágio: `solicitado`, `ativo`, `concluido`, `cancelado` ([17]({17}), seção 4.3).
- Empresa concedente com CNPJ válido; apólice com validade durante todo o estágio ([17]({17}), seção 4.2).
- Pessoa de fora do sistema (banca externa, supervisor) entra por convite com escopo limitado (seção 13, 6).""",
        fontes=[('65', None)],
    ),
    dict(
        arquivo=A + 'prontuario-e-portfolio-do-aluno.md', area=ACAD,
        titulo='Prontuário e portfólio do aluno',
        objetivo='Oferecer a visão consolidada do aluno (prontuário: dados acadêmicos, frequência, ocorrências, saúde e apoio educacional com acesso restrito) e o portfólio de evidências avaliadas.',
        telas="""- **Prontuário do aluno** (página com abas): dados, matrícula, boletins, frequência, ocorrências, documentos, saúde e apoio educacional (restrito), histórico após saída.
- **Portfólio** (galeria de evidências): envio, avaliação, compartilhamento e exportação.
- **Registro de acesso** (lista): quem viu a aba de saúde e quando.""",
        papeis="""- `unit.coordinator`: prontuário completo, exceto saúde sem papel próprio.
- `unit.secretary`: dados cadastrais e documentos.
- Aba de saúde e apoio educacional: só papéis indicados na seção 13 (2.3).""",
        regras="""- O prontuário é **visão**, não cópia: lê dos módulos donos (seção 13, 2.1).
- Dado de saúde é sensível: acesso restrito, motivo e auditoria ([07]({07})).""",
        fontes=[('66', None)],
    ),
    dict(
        arquivo=A + 'livros-digitais-e-arquivo-morto.md', area=ACAD,
        titulo='Livros digitais e arquivo morto',
        objetivo='Gerar e travar os livros de registro (matrícula, resultados, diplomas) e de atas, e gerir o arquivo morto físico e digitalizado com prazos de guarda e eliminação.',
        telas="""- **Livros de registro** (lista): tipo, ano, numeração, estado (aberto, travado, enviado); gerar, travar, enviar.
- **Livro de atas** (lista e editor): ata, assinaturas, estados.
- **Arquivo morto** (DataTable): caixa, localização física, documentos, digitalização verificada, prazo de guarda.
- **Eliminação** (fluxo com aprovação): lista de eliminação, termo e auditoria.""",
        papeis="""- `unit.secretary`: gerar livros, cadastrar arquivo morto, digitalizar.
- `unit.manager`: travar livro, aprovar eliminação.""",
        regras="""- Livro travado não é alterado; correção por termo de retificação (seção 13, 2.2).
- Eliminação só depois do prazo de guarda e com aprovação (seção 13, 4.4).""",
        fontes=[('67', None)],
    ),
    dict(
        arquivo=A + 'preceptoria.md', area=ACAD,
        titulo='Preceptoria',
        objetivo='Gerir a preceptoria em duas partes: (A) avaliação e autoavaliação de residentes por instrumentos e ciclos com cálculo e alertas de divergência; (B) tutoria, metas, PDI e evidências.',
        telas="""- **Programas e ciclos** (lista e formulário): instrumentos, pesos, ciclos de avaliação.
- **Instrumentos** (editor de questões e escalas).
- **Relatório agregado** (dashboard): médias por competência, divergência entre avaliação e autoavaliação.
- **Alertas de divergência** (fila).
- **Devoluções** (fila de aprovação).""",
        papeis="""- `unit.preceptoria.manager`: criar instrumento, ciclo, programa e pesos; relatório agregado; alertas; aprovar devolução; exportar com auditoria. Não vê resposta individual nem anotação de tutoria.""",
        regras="""- Avaliação do preceptor é anônima para o residente (seção 13, 5).
- Campo de estágio (terceiro) vê só o mínimo para supervisionar (seção 13, 5; [38]({38})).""",
        fontes=[('42', None)],
        v1=['spec-gestao-preceptoria-autoavaliacao.md'],
    ),
    dict(
        arquivo=A + 'gestao-pastoral.md', area=ACAD,
        titulo='Gestão pastoral',
        objetivo='Gerir agenda pastoral, escalas litúrgicas, intenções, eventos e celebrações, tradições religiosas (ecumênico) e ações sociais com beneficiários e doações, protegendo dados de alto risco.',
        telas="""- **Agenda pastoral** (calendário) e **escalas** (quadro por celebração).
- **Eventos e inscrições** (lista; autorização do responsável para menor).
- **Campanhas e ações sociais** (lista; beneficiários com acesso restrito; doações).
- **Relatório agregado** (dashboard para a gestão, sem identificação).""",
        papeis="""- `unit.pastoral`: agenda, escala, evento, campanha e beneficiário dentro da campanha.
- `unit.manager`: aprovar evento, relatório agregado, gerenciar escalas.""",
        regras="""- Confissões: só horário público (seção 13, 2.1). Acompanhamento espiritual: restrito ao acompanhante (2.2).
- Beneficiário é dado de vulnerabilidade: exportação só com auditoria (2.3).
- Menores: regras da seção 13, 6.""",
        fontes=[('43', None)],
    ),
    dict(
        arquivo=A + 'aulas-online.md', area=ACAD,
        titulo='Aulas online e reuniões ao vivo',
        objetivo='Configurar e acompanhar aulas online e reuniões (tipos de sessão, entrada, interface da sala, gravação com consentimento, transcrição, presença online) na unidade.',
        telas="""- **Sessões** (DataTable): tipo, turma, professor, data, estado, gravação.
- **Configuração** (página): provedor de mídia, política de gravação e retenção, consentimento.
- **Gravações** (lista com acesso controlado e prazo de retenção).
- **Presença online** (relatório por sessão, integra o diário).""",
        papeis="""- `unit.manager`: política de gravação e retenção.
- `unit.coordinator`: acompanhar sessões e presença.
- `teacher`: criar e conduzir sessões (portal do professor).""",
        regras="""- Gravação só com aviso e consentimento conforme a seção 13 (5).
- Presença online segue a regra da seção 13 (6) e alimenta o diário ([61]({61})).""",
        fontes=[('40', None)],
        v1=['global_meeting_spec_v2_complete.md'],
    ),
    dict(
        arquivo=A + 'agendamento-de-ambientes-e-equipamentos.md', area=ACAD,
        titulo='Agendamento de ambientes e equipamentos',
        objetivo='Cadastrar ambientes (salas, laboratórios, quadras, auditório) e equipamentos e gerir reservas com aprovação, conflito e check-in.',
        telas="""- **Recursos** (DataTable): tipo, capacidade, regras de reserva, responsável.
- **Agenda de reservas** (calendário por recurso).
- **Aprovações** (fila).
- **Ocupação** (dashboard).""",
        papeis="""- `unit.manager`: cadastrar recursos e regras.
- `unit.coordinator`: aprovar reservas pedagógicas.
- `teacher`: pedir reserva (portal do professor).""",
        regras="""- Reserva em conflito é recusada; aula da grade tem prioridade ([60]({60})).""",
        fontes=[('44', None)],
    ),
    dict(
        arquivo=A + 'formularios-e-pesquisas.md', area=ACAD,
        titulo='Formulários e pesquisas',
        objetivo='Motor compartilhado de formulários e pesquisas (estilo Google Forms e Microsoft Forms) usado por todos os módulos, com anonimato real, dado sensível protegido e relatórios.',
        telas="""- **Formulários** (DataTable): título, módulo dono, público, estado, respostas.
- **Editor de formulário** (página): tipos de pergunta, lógica condicional, anonimato, público-alvo, prazo.
- **Respostas e relatórios** (dashboard com gráficos; exportação).""",
        papeis="""- `unit.manager` e `unit.coordinator`: criar e publicar no escopo da unidade.
- Módulo dono do formulário define quem vê as respostas ([41]({41}), seção 6).""",
        regras="""- Pesquisa anônima não guarda vínculo com o respondente (seção 13, 3).
- Dado sensível segue a seção 13 (4) e o [07]({07}).""",
        fontes=[('41', None)],
    ),
    dict(
        arquivo=A + 'relatorios-academicos-e-censo.md', area=ACAD,
        titulo='Relatórios acadêmicos e censo',
        objetivo='Emitir os relatórios acadêmicos pelo modelo comum (tipos, ciclo, formatos) e o censo escolar e formatos oficiais, inclusive CPA/SINAES (ACA-02).',
        telas="""- **Catálogo de relatórios** (lista por módulo, seção 13, 3): filtros, agendamento, formato.
- **Execuções** (DataTable): estado, autor, arquivo, validade do link.
- **Censo escolar** (assistente): fonte, validação, pendências, exportação no formato oficial.
- **CPA/SINAES** (página de ciclo de autoavaliação institucional).""",
        papeis="""- `unit.manager` e `unit.coordinator`: relatórios da unidade.
- `unit.secretary`: relatórios da secretaria e censo.""",
        regras="""- Relatório respeita o escopo de quem pede; dado pessoal só com permissão ([69]({69}), seção 2.4).
- Relatórios da secretaria, do diário, do financeiro e da biblioteca: [56]({56}), seções 4 a 7.""",
        fontes=[('69', None), ('56', '4'), ('56', '5')],
    ),
]

S = 'gestao/secretaria/'
SEC = 'Secretaria'
D = 'gestao/gestao-de-documentos/'
GD = 'Gestão de documentos'
SI = 'gestao/simulados/'
SIM = 'Simulados'
B = 'gestao/biblioteca/'
BIB = 'Biblioteca'
MAT = 'gestao/secretaria/matriculas.md'

MODULOS += [
    dict(arquivo=MAT, area=SEC, titulo='Matrículas',
         objetivo='Conduzir a matrícula do ingresso à efetivação: pedido (wizard ou balcão), análise de documentos e pagamento, matrícula condicional com prazo, contrato assinado e efetivação, com vaga reservada e bloqueio de concorrência.',
         telas="""- **Matrículas** (DataTable e kanban por estado): `lista_espera`, `solicitada`, `em_analise`, `condicional`, `ativa`, `trancada`, `transferida`, `concluida`, `cancelada`, `nao_rematriculada`.
- **Nova matrícula — balcão** (wizard em etapas, igual ao do portal, M-02): aluno e responsável (busca por CPF antes de cadastrar, alerta de duplicidade), turma e eletivas, documentos, plano financeiro, contrato e aceite de LGPD, primeira parcela.
- **Análise** (página): checklist de documentos por tipo (M-08), situação financeira, decisão `ativa`, `condicional` (com prazo) ou `cancelada` com motivo.
- **Condicionais a vencer** (lista com prazo e aviso).
- **Trancamento** (fluxo com motivo, aprovação por níveis e protocolo, M-06).
- **Painel de matrículas** (dashboard): vagas por turma, ocupação, condicionais, lista de espera.""",
         papeis="""- `unit.secretary`: matrícula, análise, trancamento (até a alçada), enturmação.
- `unit.coordinator`: aprova trancamento até o prazo do regimento; transferência de turma.
- `unit.manager`: trancamento acima do prazo (com a secretaria), liberar vaga de não rematriculado.""",
         regras="""- Um vínculo ativo por aluno e turma; vaga reservada na transação de confirmação; empate na última vaga gera uma matrícula e uma `lista_espera` ([15]({15}), seção 7).
- Condicional vencida vira `cancelada` por job com aviso e registro; a vaga volta à lista de espera (M-04).
- Sem contrato e termo de LGPD assinados, não passa de `em_analise` (M-08).
- Inadimplente de outro período mantém acesso à rematrícula e documentação ([26]({26}), seção 3).""",
         fontes=[('46', None), ('31', '3.5'), ('17', '4')],
         v1_em=['gestao/academico/administracao-escolar-estrutura-academica.md'],
         integracoes='- Contrato e assinatura ([33]({33}), seção 5); gateway da unidade ([34]({34})); enturmação ([60]({60}), seção 2.4); CRM do tenant para candidatos ([22]({22}), seção 4.2); notificações ([57]({57})).'),
    dict(arquivo=S + 'rematriculas.md', area=SEC, titulo='Rematrículas',
         objetivo='Abrir a janela de rematrícula por série e curso, acompanhar a confirmação das famílias pelo kanban e tratar os não rematriculados.',
         telas="""- **Janelas de rematrícula** (lista e formulário por série e curso): abertura, fechamento, prazo de confirmação.
- **Kanban de rematrícula** (M-01): `não iniciada`, `em preenchimento`, `confirmada`, `em pendência`, `não rematriculada`; filtros por série e turma; ação em lote de lembrete.
- **Não rematriculados** (lista, M-05): avisos enviados, decisão de liberar vaga.""",
         papeis="- `unit.secretary`: configurar janela e acompanhar.\n- `unit.manager`: liberar vaga de não rematriculado.",
         regras="""- Fora da janela, a confirmação é recusada e a tela mostra a data de abertura (M-01).
- Não rematriculado após o fim da janela mais 30 dias; aviso em até 2 dias úteis e aos 30 dias; não é cancelamento (M-05).""",
         fontes=[('46', '2'), ('46', 'M-01'), ('46', 'M-02'), ('46', 'M-05'), ('46', '6')],
         v1_em=['gestao/academico/administracao-escolar-estrutura-academica.md']),
    dict(arquivo=S + 'transferencias.md', area=SEC, titulo='Transferências',
         objetivo='Transferir aluno de turma na mesma unidade, entre unidades da mesma entidade e para fora da entidade, com histórico por registro e documentos de transferência.',
         telas="""- **Transferências** (DataTable): tipo (turma, unidade, externa), origem, destino, estado.
- **Nova transferência** (formulário): verificação de vaga e pré-requisito, aprovação da coordenação.
- **Transferência entre unidades** (fluxo): nova matrícula no destino com histórico transferido por registro.
- **Transferência externa** (emissão de histórico e declaração pelo [48]({48})).
- **Reopção e aproveitamento de estudos** (seção 13, 5).""",
         papeis="- `unit.secretary`: registrar e emitir documentos.\n- `unit.coordinator`: aprovar transferência de turma.",
         regras="""- Transferência entre unidades exige matrícula nova no destino; o histórico é transferido por registro, não por cópia (M-07).
- Estado `transferida` na origem ([46]({46}), seção 2).""",
         fontes=[('46', '2'), ('46', 'M-07'), ('46', '5')],
         v1_em=['gestao/academico/administracao-escolar-estrutura-academica.md']),
    dict(arquivo=S + 'enturmacao.md', area=SEC, titulo='Enturmação',
         objetivo='Distribuir os alunos matriculados nas turmas, respeitando vagas, pré-requisitos e o bloqueio de concorrência.',
         telas="""- **Enturmação** (quadro de turmas com contadores de vaga; arrastar aluno entre turmas com validação).
- **Pendentes de enturmação** (lista).
- **Enturmação em lote** (assistente com pré-visualização e relatório de recusas).""",
         papeis="- `unit.secretary`: enturmar com autorização.\n- `unit.coordinator`: montar turmas e autorizar.",
         regras="- Vaga com bloqueio de concorrência (M-03); turma encerrada não recebe aluno ([60]({60}), seção 2.3).",
         fontes=[('46', 'M-03'), ('46', 'M-07'), ('60', '2.4')]),
    dict(arquivo=S + 'ficha-cadastral.md', area=SEC, titulo='Ficha cadastral',
         objetivo='Manter o cadastro civil do aluno e dos responsáveis (no banco de identidade da entidade, D-19), os vínculos de responsabilidade e os documentos pessoais versionados.',
         telas="""- **Alunos** (DataTable): nome, CPF mascarado, matrícula, turma, situação; busca por CPF.
- **Ficha do aluno** (página com abas): dados civis, endereço, contatos, responsáveis e vínculos, saúde (restrito), documentos versionados, campos personalizados ([72]({72})), histórico de alterações.
- **Responsáveis** (lista e ficha): vínculo, tipo (legal, financeiro, pedagógico), autorização de retirada.
- **Documentos pessoais** (lista versionada com validade e hash).""",
         papeis="- `unit.secretary`: cadastrar e alterar.\n- `unit.coordinator`: leitura.\n- Aba de saúde: só papéis com permissão própria.",
         regras="""- CPF único por tenant; busca antes de cadastrar; alerta de duplicidade ([17]({17}), seção 4.2).
- Documentos versionados com data, validade, responsável e hash ([17]({17}), seção 4.2).
- Conta global por e-mail verificado; dados civis no banco de identidade da entidade ([06]({06}), seção 12).
- Responsável só vê dependente com vínculo ativo ([07]({07}), seção 1).""",
         fontes=[('17', '4'), ('06', '12'), ('66', '2')],
         v1_em=['gestao/academico/administracao-escolar-estrutura-academica.md']),
    dict(arquivo=S + 'protocolo-de-atendimento.md', area=SEC, titulo='Protocolo de atendimento',
         objetivo='Registrar e acompanhar requerimentos e solicitações (secretaria, pedagógico, financeiro, LGPD) com número de protocolo, prazo, responsável e consulta pública por número e CPF.',
         telas="""- **Protocolos** (DataTable e kanban por estado): número, tipo, solicitante, prazo, responsável.
- **Novo protocolo — balcão** (formulário por tipo de requerimento).
- **Protocolo — detalhe** (página): linha do tempo, anexos, despacho, resposta, documento emitido.
- **Tipos de requerimento** (configuração): prazo, setor, documentos exigidos, taxa.
- **Consulta pública** (página sem login): número e CPF, com limite de tentativas.""",
         papeis="- `unit.secretary`: abrir, despachar e responder.\n- `unit.coordinator` e `unit.finance`: despachar os do próprio setor.",
         regras="""- Protocolo é serviço comum, separado do CRM comercial e do atendimento (helpdesk) ([31]({31}), seção 3.2).
- Consulta pública por número e CPF, sem login, com limite de tentativas ([17]({17}), seção 4.2).""",
         fontes=[('31', '3.2'), ('54', '5'), ('17', '4')]),
    dict(arquivo=S + 'emissao-de-documentos.md', area=SEC, titulo='Emissão de documentos (gerador de documentos)',
         objetivo='Emitir declarações, históricos, certidões, boletins oficiais e diplomas a partir de modelos aprovados, com elegibilidade, emissão em lote, assinatura, validação pública por código e revogação.',
         telas="""- **Emitir documento** (assistente): tipo, aluno ou lote, verificação de elegibilidade, pré-visualização, assinatura.
- **Documentos emitidos** (DataTable): código de validação, tipo, aluno, estado (seção 13, ciclo de vida), revogação.
- **Modelos** (lista; editor de modelo com aprovação, seção 13, 5 e 12).
- **Painel de assinaturas** (seção 13, 19).
- **Validação pública** (página sem login pelo código).
- **Configuração de impressão** (seção 13, 17).""",
         papeis="- `unit.secretary`: emitir e revogar com motivo.\n- `unit.manager`: aprovar modelo.\n- `platform.developer`: publicar modelos-base, sem dado.",
         regras="""- Modelo só é usado depois de aprovado; documento emitido é imutável e só é revogado com motivo (seção 13, 12 e 15).
- Editor de modelos do gerador **não é** o Editor de portais ([31]({31}), seção 3.4).""",
         fontes=[('48', None)],
         v1=['spec-builder-documentos-academicos.md']),
    dict(arquivo=S + 'processo-seletivo-e-lista-de-espera.md', area=SEC, titulo='Processo seletivo e lista de espera',
         objetivo='Gerir processos seletivos (inscrição, prova ou análise, classificação, convocação) e a lista de espera por prioridade, integrados ao CRM do tenant.',
         telas="""- **Processos seletivos** (lista e formulário): curso, vagas, etapas, datas, critérios.
- **Inscritos e classificação** (DataTable com notas e ordem).
- **Lista de espera** (lista ordenada por prioridade; convocação com prazo).""",
         papeis="- `unit.secretary`: conduzir o processo.\n- `unit.commercial`: captação no CRM ([22]({22}), seção 4.2).",
         regras="- Vaga liberada convoca o próximo da lista de espera, com prazo ([46]({46}), seções 2 e 4).",
         fontes=[('46', '4'), ('46', '2')]),

    dict(arquivo=D + 'documentos-recebidos-validacao.md', area=GD, titulo='Documentos recebidos (validação)',
         objetivo='Contexto A: receber, conferir e validar os documentos enviados por alunos, responsáveis, candidatos, colaboradores e terceiros, com pendências e prazos.',
         telas="""- **Fila de validação** (DataTable): documento, dono, tipo, enviado em, estado; filtros por tipo e prazo.
- **Validar documento** (página lado a lado: visualizador e checklist): aprovar, recusar com motivo, pedir novo envio.
- **Pendências por pessoa** (lista).""",
         papeis="- `unit.secretary` e o setor dono do tipo de documento.",
         regras="- Regras do contexto A ([54]({54}), seção 2); documento sensível com acesso restrito ([07]({07})).",
         fontes=[('54', '1'), ('54', '2'), ('54', '6'), ('54', '7')],
         v1_em=[D + 'servicos-comuns-assinatura-protocolo-e-armazenamento.md']),
    dict(arquivo=D + 'documentos-administrativos-tramitacao.md', area=GD, titulo='Documentos administrativos (tramitação)',
         objetivo='Contexto B: criar e tramitar documentos administrativos (ofícios, memorandos, processos internos) entre setores, com despacho, prazo e assinatura.',
         telas="""- **Caixa de entrada do setor** (DataTable).
- **Documento — tramitação** (página): linha do tempo de despachos, anexos, assinaturas, prazo.
- **Novo documento** (editor com modelo).""",
         papeis="- Usuários do setor com permissão do contexto B; `unit.manager` vê todos da unidade.",
         regras="- Regras do contexto B ([54]({54}), seção 3).",
         fontes=[('54', '1'), ('54', '3'), ('54', '6'), ('54', '7')],
         v1_em=[D + 'servicos-comuns-assinatura-protocolo-e-armazenamento.md']),
    dict(arquivo=D + 'documentos-emitidos-modelos-e-emissao.md', area=GD, titulo='Documentos emitidos (modelos e emissão)',
         objetivo='Contexto C: documentos emitidos pela entidade a partir de modelos. A emissão acadêmica é operada pela ficha [Emissão de documentos](../secretaria/emissao-de-documentos.md); esta ficha trata do contexto comum a todos os módulos emissores.',
         telas="""- **Documentos emitidos** (DataTable de todos os módulos emissores).
- **Modelos** (lista por módulo, com aprovação).""",
         papeis="- Módulo emissor define quem emite; `unit.manager` aprova modelos.",
         regras="- Regras do contexto C ([54]({54}), seção 4) e do gerador ([48]({48})).",
         fontes=[('54', '1'), ('54', '4'), ('54', '6'), ('54', '7')],
         v1_em=[S + 'emissao-de-documentos.md']),
    dict(arquivo=D + 'servicos-comuns-assinatura-protocolo-e-armazenamento.md', area=GD, titulo='Serviços comuns (assinatura, protocolo e armazenamento)',
         objetivo='Serviços usados pelos três contextos: assinatura eletrônica, protocolo, armazenamento com versão e hash, temporalidade e eliminação.',
         telas="""- **Assinaturas** (painel de pendências por documento e signatário).
- **Temporalidade** (configuração de prazos de guarda por tipo).
- **Armazenamento documental** (visão por contexto; integra Arquivos, [21]({21})).""",
         papeis="- `unit.manager`: temporalidade e eliminação.\n- `unit.legal`: bloqueio legal.",
         regras="- Serviços comuns e DDL dos contextos ([54]({54}), seções 5 e 10); o que muda nos documentos existentes (seção 8).",
         fontes=[('54', None)],
         v1=['spec_gestao_documentos_completo.md']),

    dict(arquivo=SI + 'banco-de-questoes.md', area=SIM, titulo='Banco de questões',
         objetivo='Manter o banco de questões da unidade com origem, autoria, revisão e situação, base para provas e simulados.',
         telas="""- **Questões** (DataTable): enunciado resumido, disciplina, habilidade, dificuldade, autor, situação (`rascunho`, `revisada`, `publicada`, `arquivada`).
- **Questão — editor** (página): enunciado com mídia, alternativas, gabarito, comentário, classificação.
- **Fila de revisão** (aprovação por revisor diferente do autor).""",
         papeis="- `unit.coordinator`: revisar e publicar.\n- `teacher`: elaborar (portal do professor).",
         regras="- Questão passa por revisão antes de publicar ([31]({31}), seção 3.6).\n- IA só sugere; nota final nunca é só da IA ([27]({27})).",
         fontes=[('47', None), ('31', '3.6'), ('19', '12')],
         v1=['spec_gestao_simulados_ia.md']),
    dict(arquivo=SI + 'geracao-de-provas.md', area=SIM, titulo='Geração de provas',
         objetivo='Gerar provas e simulados por perfil (ENEM, vestibular, interna), com sorteio, versões e agendamento.',
         telas="- **Provas** (DataTable).\n- **Gerar prova** (assistente: perfil, filtros, sorteio, versões, pré-visualização, agendamento).",
         papeis="- `unit.coordinator`: gerar e agendar.", regras="- Perfis e estados da prova ([47]({47}), seções 3 e 4).",
         fontes=[('47', '3'), ('47', '4'), ('47', '7')], v1_em=[SI + 'banco-de-questoes.md']),
    dict(arquivo=SI + 'correcao.md', area=SIM, titulo='Correção',
         objetivo='Corrigir provas objetivas (leitor óptico próprio ou de terceiro, por configuração) e dissertativas com sugestão de IA confirmada pelo professor.',
         telas="- **Correções** (DataTable por prova).\n- **Envio de folhas e OCR** (upload com fallback manual).\n- **Correção dissertativa** (lado a lado: resposta, sugestão de IA, nota confirmada).",
         papeis="- `teacher`: confirmar nota.\n- `unit.coordinator`: acompanhar.",
         regras="- Aluno anonimizado no envio ao provedor de IA ([19]({19}), seção 12); a IA sugere e o professor confirma ([27]({27})).\n- Correção por IA é recurso do plano PRO ([31]({31}), seção 3.6).",
         fontes=[('47', '5'), ('47', '6'), ('47', '10')], v1_em=[SI + 'banco-de-questoes.md']),
    dict(arquivo=SI + 'gabarito.md', area=SIM, titulo='Gabarito',
         objetivo='Publicar gabarito e comentários após a prova, com controle de liberação.',
         telas="- **Gabaritos** (lista por prova; liberar para alunos e responsáveis).",
         papeis="- `unit.coordinator`: liberar gabarito.", regras="- Liberação só depois do fim da aplicação ([47]({47}), seção 9).",
         fontes=[('47', '4'), ('47', '9')], v1_em=[SI + 'banco-de-questoes.md']),
    dict(arquivo=SI + 'ranking.md', area=SIM, titulo='Ranking',
         objetivo='Relatórios e ranking de desempenho por turma, unidade e habilidade.',
         telas="- **Ranking** (dashboard com filtros).\n- **Relatório por habilidade** (gráficos).",
         papeis="- `unit.coordinator` e `unit.manager`: unidade.", regras="- Ranking é recurso do plano PRO ([31]({31}), seção 3.6); relatórios por portal ([47]({47}), seção 8).",
         fontes=[('47', '8'), ('47', '7')], v1_em=[SI + 'banco-de-questoes.md']),

    dict(arquivo=B + 'acervo.md', area=BIB, titulo='Acervo',
         objetivo='Catalogar obras e exemplares, perfis e prazos, inventário e baixa da biblioteca da unidade.',
         telas="- **Acervo** (DataTable de obras; drawer com exemplares).\n- **Obra — cadastro** (formulário com ISBN e classificação).\n- **Exemplares** (lista com tombo e situação).\n- **Inventário e baixa** (fluxo com aprovação).\n- **Perfis e prazos** (configuração).",
         papeis="- `unit.librarian`: acervo, inventário, perfis.\n- `unit.manager`: aprovar baixa.",
         regras="- Fronteira com gestão de documentos ([31]({31}), seção 3.1).",
         fontes=[('68', None), ('31', '3.1')], v1=['spec_gestao_biblioteca_completo.md', 'spec_gestao_biblioteca_academica.md']),
    dict(arquivo=B + 'emprestimos.md', area=BIB, titulo='Empréstimos', objetivo='Empréstimo, renovação e devolução de exemplares, inclusive entre unidades.',
         telas="- **Balcão de circulação** (página: leitor, exemplar, empréstimo, devolução).\n- **Empréstimos ativos e atrasados** (DataTable).\n- **Empréstimo entre unidades** (fluxo).",
         papeis="- `unit.librarian`.", regras="- Prazos por perfil ([68]({68}), seção 4); renovação bloqueada se houver reserva.",
         fontes=[('68', '4'), ('68', '5'), ('68', '10'), ('68', '11')], v1_em=[B + 'acervo.md']),
    dict(arquivo=B + 'reservas.md', area=BIB, titulo='Reservas', objetivo='Fila de reservas por obra e salas de leitura.',
         telas="- **Reservas** (lista por obra com ordem).\n- **Salas de leitura** (agenda).", papeis="- `unit.librarian`.",
         regras="- Regras de reserva e salas ([68]({68}), seções 5.3 e 9).", fontes=[('68', '5.3'), ('68', '9')], v1_em=[B + 'acervo.md']),
    dict(arquivo=B + 'multas.md', area=BIB, titulo='Multas', objetivo='Calcular e cobrar multas por atraso, com integração ao financeiro.',
         telas="- **Multas** (DataTable: leitor, valor, situação).\n- **Regras de multa** (configuração).", papeis="- `unit.librarian`: lançar e isentar com motivo.\n- `unit.finance`: cobrança.",
         regras="- Regras de multa ([68]({68}), seção 6).", fontes=[('68', '6'), ('68', '12')], v1_em=[B + 'acervo.md']),
    dict(arquivo=B + 'biblioteca-digital.md', area=BIB, titulo='Biblioteca digital', objetivo='Acervo digital (e-books, periódicos, bases) com licenças e acesso controlado.',
         telas="- **Acervo digital** (lista).\n- **Licenças e acessos** (relatório).", papeis="- `unit.librarian`.",
         regras="- Regras da biblioteca digital ([68]({68}), seção 8).", fontes=[('68', '8')], v1_em=[B + 'acervo.md']),
]
