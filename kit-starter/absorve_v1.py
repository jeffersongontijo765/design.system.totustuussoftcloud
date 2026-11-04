"""Monta fichas do kit-starter que absorvem integralmente uma especificação da v1.

Uso: python3 kit-starter/absorve_v1.py
Cada ficha tem: cabeçalho, regras da v2 que prevalecem, decisões por padrão, papéis, resumo das telas
(títulos da v1) e, na seção 13, o texto integral da especificação da v1, sem corte, com os títulos rebaixados.
Onde a v1 contradiz a v2 ou as decisões, vale o que está nas seções 1 a 12 da ficha.
"""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
V2 = os.path.join(ROOT, 'docs', 'v2')
KIT = os.path.join(ROOT, 'kit-starter')


def rel(destino_dir, alvo):
    return os.path.relpath(alvo, destino_dir).replace(os.sep, '/')


def links_locais(texto):
    """Links file:/// da v1 (máquina do autor) viram referência ao repositório do aplicativo."""
    return re.sub(r'\[([^\]]*)\]\(file:///[a-zA-Z]:/Xampp/htdocs/totustuussoftcloud/([^)]+)\)',
                  r'\1 (repositório do aplicativo `jeffersongontijo765/totustuussoftcloud.academic`, arquivo `\2`)', texto)


def rebaixa(texto, niveis=2):
    out, codigo = [], False
    for linha in links_locais(texto).splitlines():
        if linha.lstrip().startswith('```'):
            codigo = not codigo
        if not codigo and re.match(r'^#{1,4} ', linha):
            linha = '#' * niveis + linha
        out.append(linha)
    return '\n'.join(out)


def telas(texto):
    """Títulos de seção e subseção da v1, como índice das telas."""
    itens, codigo = [], False
    for linha in texto.splitlines():
        if linha.lstrip().startswith('```'):
            codigo = not codigo
        if not codigo:
            m = re.match(r'^(#{2,3}) (.+)$', linha)
            if m:
                itens.append(('  ' if len(m.group(1)) == 3 else '') + '- ' + m.group(2).strip())
    return '\n'.join(itens)


def monta(cfg):
    destino = os.path.join(KIT, cfg['arquivo'])
    d = os.path.dirname(destino)
    fontes = cfg['v1'] if isinstance(cfg['v1'], list) else [cfg['v1']]
    textos = [(n, open(os.path.join(V2, 'anexo-v1', n), encoding='utf8').read()) for n in fontes]
    r = lambda doc: rel(d, os.path.join(V2, doc))
    linha = lambda t: re.sub(r'\{(\d\d-[^}]+\.md)\}', lambda m: r(m.group(1)), t)
    if textos:
        fonte = '- Fonte da v1: ' + '; '.join(f"[{n}]({rel(d, os.path.join(V2, 'anexo-v1', n))}) ({len(t.splitlines())} linhas)" for n, t in textos)
        status = 'detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)'
        indice = '\n\n'.join((f'**{n}**\n\n' if len(textos) > 1 else '') + telas(t) for n, t in textos)
        integral = '\n\n'.join((f'### Fonte: {n}\n\n' if len(textos) > 1 else '') + rebaixa(t, 3 if len(textos) > 1 else 2) for n, t in textos)
        sec13 = f"## 13. Conteúdo integral da v1 (absorvido)\n\n{integral}\n"
        leitura = 'As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.'
    else:
        fonte = '- Fonte da v1: sem especificação própria (regras no SDD v2, seção 4 desta ficha)'
        status = 'detalhado a partir do SDD v2 (sem especificação própria na v1)'
        indice = linha(cfg.get('telas', '- Telas na seção 4.'))
        sec13 = ''
        leitura = 'Não há especificação própria na v1. Valem as regras do SDD v2 citadas nesta ficha.'
    corpo = f"""# {cfg['titulo']}

- Portal: {cfg['portal']}
- Área: {cfg['area']}
- Domínio: {linha(cfg['dominio'])}
- Status: {status}
{fonte}

## 1. Regra de leitura
{leitura}

## 2. Objetivo e escopo
{linha(cfg['objetivo'])}

## 3. Telas
{linha(TELAS_DET[cfg['arquivo']]) if cfg['arquivo'] in TELAS_DET else linha(cfg.get('telas', ''))}
{('**Títulos da v1 (referência, não são telas):**\n\n' + indice) if textos else ''}

## 4. Correções da v2 que prevalecem
{linha(cfg['correcoes'])}

## 5. Decisões por padrão aplicadas
{linha(cfg['decisoes'])}

## 6. Permissões e papéis
{linha(cfg['papeis'])}

## 7. Dados
{linha(cfg['dados'])}

## 8. Integrações
{linha(cfg['integracoes'])}

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08]({r('08-frontend-design-system.md')}), seção 3).
- Auditoria conforme [29]({r('29-auditoria.md')}); dados pessoais conforme [07]({r('07-privacidade-lgpd.md')}).
{linha(cfg.get('privacidade', ''))}

## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08]({r('08-frontend-design-system.md')})).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
{linha(cfg['pendencias'])}

{sec13}"""
    open(destino, 'w', encoding='utf8').write(corpo)
    return destino, len(corpo.splitlines())


PLAT = 'plataforma (banco master), instância separada do módulo das entidades ([31]({31-matriz-portais-modulos.md}), seção 2.1)'
TELAS_DET = {
 'desenvolvedor/seguranca-e-operacao/acesso.md': """- **Contas da plataforma** (datatable): contas de plataforma, papel, passkey cadastrada, último uso; máximo de cinco contas ativas.
- **Sessões ativas** (datatable): usuário, origem, início, expiração; encerrar sessão com motivo.
- **Papéis e permissões** (formulário): concessão e revogação de papel com justificativa e revisão.
- **Conta de emergência (break-glass)** (detalhe): credencial offline, último uso, alerta enviado.""",
 'desenvolvedor/seguranca-e-operacao/auditoria.md': """- **Trilha de auditoria** (datatable): evento, portal, usuário, entidade, data, resultado; filtros e mascaramento de dado pessoal.
- **Integridade da cadeia** (painel): verificação horária, ancoragem diária, último ponto válido.
- **Exportação de auditoria** (formulário): período, motivo, MFA recente; exportação registrada.""",
 'desenvolvedor/seguranca-e-operacao/privacidade-dpo.md': """- **Painel do DPO** (painel): pedidos de titulares abertos e vencidos, incidentes, consentimentos.
- **Pedidos de titulares** (datatable): protocolo, tipo, prazo, situação, resposta.
- **Registro de tratamento (ROPA)** (datatable): finalidade, base legal, categoria de dado, operador.
- **Incidentes de segurança** (kanban): registro, avaliação de risco, comunicação à ANPD.""",
 'desenvolvedor/seguranca-e-operacao/integracoes-globais.md': """- **Integrações da plataforma** (datatable): integração, estado, última execução, credencial por referência ao cofre.
- **Configurar integração** (formulário): provedor, ambiente, credencial, limites de uso.
- **Visualizar segredo de tenant** (formulário): motivo, step-up e alerta ao canal de segurança.""",
 'desenvolvedor/seguranca-e-operacao/ti.md': """- **Inventário de serviços** (datatable): serviço, versão, responsável, estado.
- **Backups e restauração** (painel): último backup por banco, teste de restauração, prazo de retenção.
- **Certificados** (datatable): domínio, validade, alerta a 14 dias.
- **Manutenção programada** (formulário): janela, aviso aos clientes, plano de volta; aprovação de segundo papel.
- **Monitoramento** (painel): filas, workers, cache e erros, sem dado pessoal.""",
 'desenvolvedor/seguranca-e-operacao/configuracoes-do-sistema.md': """- **Configurações globais** (formulário): grupos ligados ao documento do SDD que define cada regra.
- **Histórico de alterações** (datatable): valor anterior, novo valor, autor, motivo, versão; reverter com aprovação.""",
 'desenvolvedor/operacoes-internas/frotas.md': """- **Veículos da empresa** (datatable): placa, documentos com validade, situação, responsável.
- **Reservas** (calendário): veículo, solicitante, aprovação pela alçada.
- **Manutenções** (kanban): solicitada, aprovada, em execução, concluída.""",
 'desenvolvedor/operacoes-internas/patrimonio.md': """- **Bens da empresa** (datatable): plaqueta, categoria, localização, responsável, situação.
- **Depreciação** (painel): valor residual por categoria; categoria sem regra não deprecia.
- **Inventário** (datatable): contagem por localização, divergências.
- **Baixa de bem** (formulário): motivo, aprovação do aprovador de patrimônio.""",
 'desenvolvedor/operacoes-internas/suprimentos-da-empresa.md': """- **Requisições** (kanban): solicitada, aprovada, cotada, pedida, recebida.
- **Pedidos e cotações** (datatable): fornecedor, itens, valor, prazo de entrega.
- **Estoque** (datatable): item, saldo, lote, validade; saldo nunca negativo.""",
 'desenvolvedor/pessoas-da-plataforma/departamento-pessoal.md': """- **Colaboradores da empresa** (datatable): cadastro funcional, situação, unidade de lotação.
- **Folha** (painel): competência, bruto, descontos, líquido; folha fechada não muda.
- **Ponto** (datatable): espelho por colaborador; ajuste com motivo obrigatório.""",
 'desenvolvedor/pessoas-da-plataforma/recursos-humanos.md': """- **Recrutamento** (kanban): vaga, etapas, candidatos.
- **Avaliações de desempenho** (datatable): ciclo, colaborador, situação, consolidação.""",
 'desenvolvedor/pessoas-da-plataforma/medicina-e-seguranca-do-trabalho-da-empresa.md': """- **ASO** (datatable): colaborador, tipo de exame, validade, resultado (apto ou inapto); CID só para o médico do trabalho.
- **Ocorrências de SST** (datatable): registro, CAT, afastamento, providências.""",
 'desenvolvedor/suporte/base-de-conhecimento.md': """- **Artigos** (datatable): título, categoria, situação (rascunho, publicado, arquivado), autor.
- **Editor de artigo** (formulário): conteúdo, categoria, público, revisão antes de publicar.""",
 'desenvolvedor/suporte/chamados-dos-clientes.md': """- **Chamados dos clientes** (kanban): aberto, em atendimento, aguardando cliente, resolvido.
- **Chamado — detalhe** (detalhe): conversa, anexos, SLA, histórico.
- **SLA** (painel): tempo de primeira resposta e de resolução por fila.""",
 'transversal/exclusao-logica.md': """- **Regras de exclusão por tabela** (datatable): tabela, colunas, validação prévia, cascata lógica.
- **Pedido de restauração** (formulário): registro, motivo, permissão exigida.
- **Painel de exclusões e expurgos** (painel): exclusões do período, expurgos pelo job de retenção.""",
 'transversal/arquitetura-da-plataforma.md': """- **Mapa da arquitetura** (detalhe): camadas, bancos, filas, portais.
- **Saúde das camadas** (painel): estado de cada camada e do master.""",
 'transversal/build-e-procedencia-slsa.md': """- **Pipeline de build** (painel): etapas, duração, falhas, artefatos.
- **Gate de deploy** (lista): versão, SBOM, assinatura, aprovação; só publica com os três.
- **Cofre de segredos** (lista): segredo por referência, último rodízio, dono.""",
 'transversal/teste-de-intrusao.md': """- **Plano de teste de intrusão** (lista): fase, escopo, responsável, prazo.
- **Achados do teste** (lista): severidade, situação, prazo de correção.
- **Checklist de implementação** (lista): item, responsável, evidência.""",
 'transversal/navegacao-dos-portais.md': """- **Matriz de navegação por portal** (lista): portal, área, item de menu, papel exigido.
- **Checklist de layout** (lista): os 21 itens, por tela, com situação.""",
 'transversal/plano-de-implementacao-v1.md': """- **Fases e tarefas** (lista): fase, tarefa, dependência, situação.
- **Checklist por módulo** (lista): 18 itens de auditoria por módulo.""",
}

TRANSV = 'transversal: vale para todos os portais e módulos'
SEM_UNIDADE = '- **Instância da empresa:** sem filtro de unidade, entidade ou filial; dados no banco master; o portal do desenvolvedor não vê o módulo de nenhuma entidade.'
FICHAS = [
 dict(arquivo='desenvolvedor/operacoes-internas/patrimonio.md', v1='spec_patrimonio_completo.md',
  titulo='Patrimônio da empresa', portal='Desenvolvedor (`desenvolvedor.`)', area='Operações internas', dominio=PLAT,
  objetivo='Controlar os bens da própria empresa desenvolvedora: cadastro, depreciação, manutenção, transferência, inventário, descarte e seguros.',
  correcoes=f"""- **T-01:** todas as 12 tabelas recebem `tenant_id` NOT NULL e índice composto ([19]({{19-regras-modulos-3.md}}), seção 1; [03]({{03-dominio-tenancy.md}})).
- **T-04:** `current_value` é calculado, não editável. Guardar o último cálculo com data e método; recalcular, não sobrescrever.
- **Regras de campo** ([19]({{19-regras-modulos-3.md}}), seção 8.2): `acquisition_value` maior que zero e só alterável por correção com motivo; `residual_value` não negativo e não maior que `acquisition_value`; `dep_method` em `linear`, `accelerated`, `degressive`, `unit`; `dep_rate` entre 0 e 100%; ativo baixado não recebe depreciação nem movimento.
{SEM_UNIDADE}
- **Perfis da v1 (seção 2 da v1):** substituídos pelos papéis da seção 6 desta ficha.
- **Contabilização automática de depreciação:** gera lançamento no razão da empresa ([razao.md](../contabil-da-plataforma/razao.md)), não no contábil de entidade.""",
  decisoes="- **DP-02** ([80]({80-decisoes-por-padrao.md})): método e taxa por categoria aprovados pelo contábil; categoria sem regra aprovada não deprecia e aparece como pendência no painel.",
  papeis="- `platform.assets` (nível 1): cadastrar e movimentar bens, registrar manutenção, inventário e seguro.\n- `platform.assets.approver` (nível 2): aprovar transferência, descarte e manutenção acima do limite; não aprova o que ele mesmo registrou (DP-03; [78]({78-permissoes-e-papeis.md}), seção 4.1).",
  dados="- Modelo de dados da v1 (seção 13, \"Schema do Banco de Dados\"), com as correções T-01 e T-04 da seção 4.",
  integracoes="- Contábil da plataforma: lançamento de depreciação e de baixa.\n- Financeiro da plataforma: aquisição e venda de bem (contas a pagar e a receber).\n- Suprimentos da empresa: entrada de bem comprado.",
  pendencias="- Limite de valor que exige aprovação de manutenção: parâmetro obrigatório, configurado pelo `platform.assets.approver`; sem valor configurado, toda manutenção exige aprovação (critério 1 do [80]({80-decisoes-por-padrao.md})).\n- Regra de depreciação por categoria: configurada pelo contábil (DP-02)."),
 dict(arquivo='desenvolvedor/operacoes-internas/frotas.md', v1='spec_gestao_frotas_completo.md',
  titulo='Frotas da empresa', portal='Desenvolvedor (`desenvolvedor.`)', area='Operações internas', dominio=PLAT,
  objetivo='Gerir os veículos da própria empresa desenvolvedora: veículos, motoristas, reservas, manutenção, abastecimento, viagens, multas e documentos.',
  correcoes=f"""- **DP-01:** Frotas entra nesta versão ([80]({{80-decisoes-por-padrao.md}})).
- **T-01:** as 13 tabelas recebem `tenant_id` NOT NULL e índice composto ([19]({{19-regras-modulos-3.md}}), seção 1).
- **Regras** ([19]({{19-regras-modulos-3.md}}), seção 9): CNH vencida bloqueia a reserva e mostra alerta; conflito de horário bloqueia a reserva; veículo em manutenção bloqueia e sugere alternativo; validade do tacógrafo obrigatória quando aplicável; consumo é calculado (litros e quilometragem) e **nunca** campo de entrada, inclusive na tela que a v1 mostra como editável; abastecimento com litros maior que zero.
{SEM_UNIDADE}
- **Perfis da v1 (seção 2 da v1):** substituídos pelos papéis da seção 6 desta ficha.
- **Mapa (v1, \"Painel de Mapa\", opcional):** só com provedor de mapas aprovado como integração ([16]({{16-integracoes-externas.md}})); sem provedor, o painel não aparece.""",
  decisoes="- **DP-01:** módulo incluído.\n- **DP-03:** papéis de operador e aprovador separados.",
  papeis="- `platform.fleet` (nível 1): cadastrar veículos e motoristas, registrar reservas, abastecimentos, viagens, multas e documentos.\n- `platform.fleet.approver` (nível 2): aprovar reservas e ordens de manutenção, conforme as regras de aprovação da v1; não aprova a própria reserva (DP-03; [78]({78-permissoes-e-papeis.md}), seção 4.1).",
  dados="- Modelo de dados da v1 (seção 13, \"Schema SQL\"), com a correção T-01 e o consumo como valor calculado.",
  integracoes="- Financeiro da plataforma: custo de abastecimento, manutenção e multa (contas a pagar).\n- Patrimônio da empresa: veículo é também bem patrimonial.\n- Suprimentos da empresa: peças e serviços de manutenção.",
  privacidade="- CNH, multas e dados do motorista são dados pessoais: acesso só pelos papéis da seção 6, com retenção conforme [07]({07-privacidade-lgpd.md}).",
  pendencias="- Regras de aprovação de reservas: configuradas no módulo (v1, \"Regras de Aprovação de Reservas\"); sem regra configurada, toda reserva exige aprovação (critério 1 do [80]({80-decisoes-por-padrao.md}))."),
 dict(arquivo='desenvolvedor/operacoes-internas/suprimentos-da-empresa.md', v1='spec_gestao_suprimentos_v3_consolidado.md',
  titulo='Suprimentos da empresa', portal='Desenvolvedor (`desenvolvedor.`)', area='Operações internas', dominio=PLAT,
  objetivo='Gerir as compras e o estoque da própria empresa desenvolvedora: requisição, aprovação, cotação, pedido, entrega, recebimento, almoxarifado, fornecedores e contratos.',
  correcoes=f"""- **Dono do estoque** ([19]({{19-regras-modulos-3.md}}), seção 2, decidido em 03/11/2026): Suprimentos é dono de estoque e movimento. O antigo "Armazenamento" é sistema de arquivos, sem estoque.
- **Movimento de estoque** ([19]({{19-regras-modulos-3.md}}), seção 5; [15]({{15-validacoes.md}})): saldo nunca negativo, salvo item marcado como consumo sob encomenda; quantidade maior que zero; lote, série ou validade obrigatório para item controlado; item bloqueado não movimenta, com motivo.
- **Contratos e atas:** consumo de saldo é movimento no módulo de Contratos, disparado pelo Suprimentos ([14]({{14-integracao-modulos.md}})).
- **Nota do fornecedor:** recebida e validada pelo portal de terceiros, não emitida aqui ([34]({{34-pagamentos-fiscal-bancos-por-portal.md}}), seção 5.3).
{SEM_UNIDADE}
- **Perfis da v1 (seção 5 da v1):** substituídos pelos papéis da seção 6 desta ficha.
- **Merenda:** é do portal de gestão das entidades, não da empresa.""",
  decisoes="- **DP-03:** códigos dos papéis de compras, almoxarifado e aprovação, a partir do [22]({22-crm-canais-e-papeis.md}), seção 5.",
  papeis="Papéis do [22]({22-crm-canais-e-papeis.md}), seção 5, na empresa desenvolvedora (códigos em [78]({78-permissoes-e-papeis.md}), seção 4.1):\n- `platform.purchasing` (Compras, nível 1): criar cotação e pedido; cadastrar fornecedor. Não aprova a própria requisição; não recebe a própria compra.\n- `platform.warehouse` (Almoxarifado, nível 1): registrar recebimento e movimento. Não ajusta estoque sem motivo e aprovação.\n- `platform.purchasing.approver` (Aprovador de compras, nível 2): aprovar requisição dentro da alçada. Não é o solicitante.",
  dados="- Estrutura de dados da v1 (seção 13, \"Estrutura de Dados\"), com `tenant_id` em todas as tabelas ([03]({03-dominio-tenancy.md})).",
  integracoes="- Financeiro da plataforma: pedido aprovado gera conta a pagar; recebimento libera o pagamento.\n- Contratos: consumo de saldo de contrato e ata.\n- Portal de terceiros: fornecedor envia a nota e acompanha o pagamento.\n- Patrimônio da empresa: bem comprado entra no patrimônio.",
  pendencias="- Alçadas de aprovação de compra: parâmetro obrigatório; sem alçada configurada, toda requisição exige aprovação (critério 1 do [80]({80-decisoes-por-padrao.md}))."),
 dict(arquivo='desenvolvedor/pessoas-da-plataforma/departamento-pessoal.md', v1='spec_gestao_pessoas_completo.md',
  titulo='Departamento pessoal da empresa (Pessoas)', portal='Desenvolvedor (`desenvolvedor.`)', area='Pessoas da plataforma', dominio=PLAT,
  objetivo='Gerir o cadastro funcional e a rotina de pessoal dos funcionários da própria empresa desenvolvedora: admissão, folha, férias, afastamentos, ponto, rescisão, benefícios e eSocial. HCM da empresa no banco master, isolado do HCM de qualquer entidade (HCM-10 do [39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 11).',
  correcoes="""- **Módulo separado do RH** (HCM-01 do [39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 11): Pessoas é dono de cadastro funcional, folha, férias, rescisão, eSocial e ponto; não é dono de processo seletivo, avaliação e clima. O cadastro funcional nasce aqui, quando o RH passa o candidato contratado por referência.
- **Dados civis** ficam no banco de identidade; o HCM referencia `person_id` (D-19; [14]({14-integracao-modulos.md}), seção 3). Para a empresa, o banco é o master.
- **Regras do [39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 3** prevalecem sobre a v1: admissão, folha (folha fechada não é alterada), férias e afastamentos, ponto e jornada (ajuste manual só com motivo), rescisão (desligamento com afastamento ativo fica bloqueado) e benefícios.
- **Folha:** quem processa não aprova ([22]({22-crm-canais-e-papeis.md}), seção 5; [39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 7).
- **Medicina do trabalho:** não aparece aqui com CID nem prontuário; Pessoas recebe só apto, inapto ou restrição sem motivo clínico, validade do ASO e afastamento sem CID ([39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 5.1).
- **Perfis da v1:** a matriz de permissões da v1 é aproveitada com as correções da seção 7 do [39]({39-departamento-pessoal-rh-medicina-por-portal.md}); papéis na seção 6 desta ficha.
- **Instância da empresa:** sem filtro de unidade ou entidade; o portal do desenvolvedor não vê o HCM de nenhuma entidade.""",
  decisoes="- Nenhuma decisão nova: estrutura, isolamento e permissões já decididos no [39]({39-departamento-pessoal-rh-medicina-por-portal.md}) (HCM-01, HCM-06, HCM-10).\n- Valores legais (verbas, INSS, IRRF, FGTS, férias, 13.º, rescisão) seguem o critério 3 do [80]({80-decisoes-por-padrao.md}): parâmetro obrigatório, sem valor inventado; cálculo bloqueado enquanto a tabela da competência não estiver cadastrada.",
  papeis="Papéis do [22]({22-crm-canais-e-papeis.md}), seção 5, e do [39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 7, na empresa (códigos em [78]({78-permissoes-e-papeis.md}), seção 4.1):\n- `platform.people` (nível 1): cadastro funcional, férias, afastamentos, ponto (ajuste com motivo), rescisão, benefícios.\n- `platform.payroll` (Folha, nível 1): processar a folha. Folha fechada não muda.\n- `platform.payroll.approver` (nível 2): aprovar a folha; não aprova a folha que processou.\n- Todo funcionário: o próprio holerite, férias, ponto e documentos.",
  dados="- Modelo de dados da v1 (seção 13), com `tenant_id` em todas as tabelas e dados civis por `person_id` no banco de identidade.\n- DDL dos módulos novos, quando houver: [51]({51-ddl-modulos-novos.md}).",
  integracoes="- `hcm.employee.created` → SST (exame admissional) e Financeiro; `hcm.leave.started` → Financeiro (folha) ([14]({14-integracao-modulos.md}); [39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 8).\n- eSocial: S-2200, S-1200, S-1210 e S-2299 ausentes no SDD (HCM-04); transmissão conforme D-08 ([16]({16-integracoes-externas.md}), seção 6), com certificado da empresa.\n- Financeiro da plataforma: folha e encargos viram contas a pagar.",
  privacidade="- Salário, dependentes, conta bancária e afastamentos são dados pessoais; campos salariais só com permissão própria ([22]({22-crm-canais-e-papeis.md}), seção 5).",
  pendencias="- HCM-02 (verbas e tabelas de INSS, IRRF e FGTS), HCM-03 (férias, 13.º e rescisão), HCM-04 (eventos eSocial) e HCM-05 (REP e estatuto do servidor), já registradas no [39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 9."),
 dict(arquivo='desenvolvedor/pessoas-da-plataforma/recursos-humanos.md', v1='spec_gestao_rh_completo.md',
  titulo='Recursos humanos da empresa', portal='Desenvolvedor (`desenvolvedor.`)', area='Pessoas da plataforma', dominio=PLAT,
  objetivo='Gerir recrutamento, onboarding, avaliação de desempenho, clima, treinamento e movimentação interna dos funcionários da própria empresa desenvolvedora.',
  correcoes="""- **Módulo separado de Pessoas** (HCM-01 do [39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 11): RH é dono de recrutamento, onboarding, avaliação, clima e movimentação interna; não é dono de folha, admissão no eSocial nem cadastro civil. Candidato contratado passa para Pessoas por referência, sem cópia de dado.
- **Currículo de candidato não contratado** (HCM-09): guardado por prazo fixo e depois excluído; o candidato é informado no envio; nenhum uso fora do processo em que se candidatou.
- **Sem acesso a dado de saúde:** o RH não vê CID, diagnóstico nem prontuário em nenhuma tela ou API ([39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 5.1).
- **Avaliação e clima:** formulários pelo motor de formulários e pesquisas ([41]({41-formularios-e-pesquisas.md})).
- **Perfis da v1:** substituídos pelos papéis da seção 6 desta ficha.
- **Instância da empresa:** sem filtro de unidade ou entidade.""",
  decisoes="- Prazo de guarda do currículo (HCM-09): valor jurídico, configurado como parâmetro obrigatório; sem prazo configurado, o recrutamento não recebe currículo (critério 3 do [80]({80-decisoes-por-padrao.md})).",
  papeis="- `platform.hr` (RH do [22]({22-crm-canais-e-papeis.md}), seção 5, no escopo do HCM-01; nível 1): recrutamento, onboarding, avaliação, clima, treinamento.\n- Aprovação de movimentação interna e de contratação: `platform.manager` ou gestor da área (nível 2 ou acima), nunca o próprio solicitante ([78]({78-permissoes-e-papeis.md}), seção 2.2).\n- Funcionário: o próprio plano de desenvolvimento e treinamentos.",
  dados="- Modelo de dados da v1 (seção 13), com `tenant_id` e referência à pessoa por `person_id`.",
  integracoes="- Pessoas (DP): contratação passa a pessoa por referência.\n- Motor de formulários ([41]({41-formularios-e-pesquisas.md})): avaliações e pesquisas de clima.\n- Notificações: etapas do processo seletivo e do onboarding.",
  privacidade="- Dados de candidato: finalidade restrita ao processo seletivo e exclusão no fim do prazo (HCM-09).",
  pendencias="- HCM-09: valor do prazo de guarda do currículo (jurídico), no [39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 9."),
 dict(arquivo='desenvolvedor/pessoas-da-plataforma/medicina-e-seguranca-do-trabalho-da-empresa.md', v1='spec_gestao_seguranca_medicina_trabalho_completo.md',
  titulo='Medicina e segurança do trabalho da empresa', portal='Desenvolvedor (`desenvolvedor.`)', area='Pessoas da plataforma', dominio=PLAT,
  objetivo='Gerir a saúde e a segurança do trabalho dos funcionários da própria empresa desenvolvedora: ASO, PCMSO, PGR, LTCAT, CAT, EPI, CIPA, ergonomia e treinamentos de NR, com dado de saúde sob acesso restrito.',
  correcoes="""- **Regra central de privacidade** ([39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 5.1, e HCM-06): RH e gestão **nunca** veem CID, diagnóstico ou prontuário; veem apenas apto, inapto ou apto com restrição, validade do ASO, restrição funcional sem motivo clínico e afastamento sem CID. A permissão "SST — Gerenciar" da v1 **não existe**: cada papel tem permissão própria.
- **PCMSO, PGR, LTCAT, CIPA e ergonomia:** seguem o [52]({52-medicina-do-trabalho-especificacao.md}), que prevalece sobre a v1, inclusive o DDL proposto da seção 9.
- **Guarda do prontuário e do ASO:** no mínimo 20 anos após o desligamento (HCM-08; NR-7, 7.6.1.1).
- **Regras do [17]({17-regras-modulos.md}), seção 5** (ASO, CAT, EPI, NR, afastamento) prevalecem sobre a v1.
- **Resultado de exame:** registrado só pelo profissional responsável ([22]({22-crm-canais-e-papeis.md}), seção 5).
- **Instância da empresa:** sem filtro de unidade; dados no banco master, com acesso restrito.""",
  decisoes="- Nenhuma decisão nova: privacidade e papéis já decididos (HCM-06, HCM-08).",
  papeis="Papéis do [39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 11 (HCM-06), na empresa (códigos em [78]({78-permissoes-e-papeis.md}), seção 4.1):\n- `platform.sst.doctor` (médico do trabalho): ASO completo, prontuário, CID, restrição detalhada.\n- `platform.sst.technician` (técnico de SESMT): ocorrências, EPI, NR, PGR, CAT, sem diagnóstico.\n- `platform.people`, `platform.hr` e `platform.manager`: só o resultado sem CID nem motivo clínico.\n- Funcionário: o próprio ASO e o próprio resultado.\n- Auditor: leitura com motivo registrado, sem conteúdo de dado de saúde ([29]({29-auditoria.md}), seção 5).",
  dados="- Modelo de dados da v1 (seção 13) e DDL proposto do [52]({52-medicina-do-trabalho-especificacao.md}), seção 9, com `tenant_id`. Dado de saúde cifrado ([05]({05-seguranca.md})).",
  integracoes="- `smt.cat.created` → Pessoas (afastamento); `hcm.employee.created` → agenda do exame admissional ([39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 8).\n- eSocial S-2220, S-2230 e S-2240, conforme D-08 ([16]({16-integracoes-externas.md}), seção 6).\n- Clínica de ASO pelo portal de terceiros: recebe agendamento e devolve resultado ([38]({38-portal-de-terceiros-prestadores.md}), seção 3.11).",
  privacidade="- Dado de saúde é dado sensível (LGPD, art. 11): necessidade, acesso por papel, cifragem, registro de leitura e guarda mínima de 20 anos para prontuário e ASO.",
  pendencias="- CAT com CID emitida pelo médico, não pela gestão **(verificar)**, no [39]({39-departamento-pessoal-rh-medicina-por-portal.md}), seção 5.1.\n- Revisão do owner do [52]({52-medicina-do-trabalho-especificacao.md}) (HCM-07)."),
 dict(arquivo='desenvolvedor/suporte/chamados-dos-clientes.md', v1=['SPEC-HELPDESK.md', 'spec_chat_rapido_sac.md', 'SPEC-LAYOUT-TICKET.md'],
  titulo='Chamados dos clientes (suporte da plataforma)', portal='Desenvolvedor (`desenvolvedor.`)', area='Suporte', dominio=PLAT,
  objetivo='Atender as entidades clientes da plataforma: abertura, triagem, atendimento, escalonamento e encerramento dos chamados, por todos os canais.',
  correcoes="""- **Modelo único** ([32]({32-atendimento-privacidade-por-portal.md}), seção 2.1; [19]({19-regras-modulos-3.md}), seção 7): Helpdesk é a base; SAC e chat rápido são canais ou tipos do mesmo registro. As três especificações da v1 da seção 13 descrevem partes desse mesmo módulo.
- **Protocolo** (ATD-01): todo pedido com responsável e prazo recebe número de protocolo; pergunta resolvida pelo bot ou pela base de conhecimento, sem fila, não recebe.
- **Estados e transições** ([32]({32-atendimento-privacidade-por-portal.md}), seção 2.2): `novo`, `aberto`, `em_triagem`, `em_atendimento`, `aguardando_cliente`, `aguardando_terceiro`, `aguardando_aprovacao`, `em_pausa`, `resolvido`, `fechado`, `reaberto`, `escalonado`, `cancelado`. Transição inválida é recusada pela aplicação. Cancelar, escalonar e reabrir gravam motivo.
- **Prioridade, categoria e fila** (seção 2.4): baixa, média, alta e urgente; urgente só em categoria que permita; atribuição automática por fila.
- **Canais** (seção 2.5; [22]({22-crm-canais-e-papeis.md}), seções 2 e 3): opção "Abrir ticket" sem IA em todo ponto de atendimento (D-18); texto do solicitante guardado literal; campos obrigatórios por tipo e lista fixa de campos padrão.
- **Portal do cliente** (seção 2.6): nota interna nunca aparece para o solicitante; respostas públicas por padrão; avaliação do atendimento.
- **Visibilidade no portal do desenvolvedor** (seção 2.8): chamados das entidades; nenhum dado de aluno sem chamado vinculado ([29]({29-auditoria.md}), seção 8).
- **Bots** (seção 2.9): categoria sensível (saúde, denúncia, conflito) vai para humano (ATD-05).
- **Perfis da v1:** substituídos pelos papéis da seção 6.""",
  decisoes="- Nenhuma decisão nova: modelo, estados, SLA e categoria sensível já decididos no [32]({32-atendimento-privacidade-por-portal.md}) (ATD-01, ATD-02, ATD-05).",
  papeis="- `platform.operator` (nível 5): atender chamados das entidades; consulta de dado de cliente só com motivo registrado ([78]({78-permissoes-e-papeis.md}), seção 4.1).\n- `platform.manager` (nível 6): redistribuir filas, ver estouros de SLA, aprovar escalonamento.\n- `platform.chatbot.operator`: atender as conversas dos canais e transferir.\n- Solicitante (usuário da entidade): o próprio chamado.",
  dados="- DDL do atendimento em [51]({51-ddl-modulos-novos.md}), seção 1 (ATD-04, revisão do owner pendente), que prevalece sobre os modelos da v1.",
  integracoes="- SLA (ficha [sla.md](sla.md)); base de conhecimento ([base-de-conhecimento.md](base-de-conhecimento.md)).\n- Notificações por mudança de estado e por alerta de SLA ([57]({57-notificacoes-por-portal.md})).\n- CRM da plataforma: conversa de canal que vira oportunidade comercial.",
  privacidade="- Retenção de tickets e transcrições: ATD-03 (jurídico), ligado ao L-24 do [22]({22-crm-canais-e-papeis.md}).",
  pendencias="- ATD-03 (retenção) e revisão do DDL (ATD-04), no [32]({32-atendimento-privacidade-por-portal.md}), seção 2.10."),
 dict(arquivo='desenvolvedor/suporte/base-de-conhecimento.md', v1='spec_gestao_sac_base_conhecimento.md',
  titulo='Base de conhecimento da plataforma', portal='Desenvolvedor (`desenvolvedor.`)', area='Suporte', dominio=PLAT,
  objetivo='Manter os artigos de ajuda da plataforma, usados pelo atendimento, pelo portal do cliente e pelo bot.',
  correcoes="""- **Artigo** ([32]({32-atendimento-privacidade-por-portal.md}), seção 2.7): autor, revisor, versão, data de revisão e público (interno, portal ou público). Artigo com dado pessoal não é publicado.
- **Sugestão por IA:** só a partir de fonte cadastrada ([27]({27-inteligencia-artificial-e-portais.md}); D-18 do [22]({22-crm-canais-e-papeis.md})).
- **Bot:** responde só com artigos publicados para o público do canal; fora da base, encaminha para humano.
- **Perfis da v1:** substituídos pelos papéis da seção 6.""",
  decisoes="- Revisão obrigatória antes de publicar, por pessoa diferente do autor (critério 4 do [80]({80-decisoes-por-padrao.md})).",
  papeis="- `platform.operator`: escrever e atualizar artigos.\n- `platform.manager`: revisar e publicar; não publica artigo que ele mesmo escreveu.",
  dados="- Modelo de artigos da v1 (seção 13) e DDL do atendimento ([51]({51-ddl-modulos-novos.md}), seção 1), com versão e público.",
  integracoes="- Chamados: artigo sugerido ao atendente e ao solicitante antes de abrir o chamado.\n- Bot dos canais ([22]({22-crm-canais-e-papeis.md}), seção 3).",
  pendencias="- Nenhuma além das do atendimento ([32]({32-atendimento-privacidade-por-portal.md}), seção 2.10)."),
 dict(arquivo='desenvolvedor/suporte/sla.md', v1=[],
  titulo='SLA do suporte da plataforma', portal='Desenvolvedor (`desenvolvedor.`)', area='Suporte', dominio=PLAT,
  objetivo='Definir e acompanhar os prazos de atendimento dos chamados das entidades clientes.',
  telas="""- **Regras de SLA** (datatable): aplicação (entidade, cliente, fila, tipo, categoria, prioridade), tipo de prazo (primeira resposta, próxima resposta, resolução, fechamento) e valor. A regra mais específica vence.
- **Painel de SLA** (dashboard): chamados dentro do prazo, com 80% do prazo consumido e com prazo estourado, por fila e por prioridade; gráfico de cumprimento por período.
- **Calendário de dias úteis** (configuração): dias úteis e feriados usados na contagem.""",
  correcoes="""- **Tipos de prazo** ([32]({32-atendimento-privacidade-por-portal.md}), seção 2.3): primeira resposta, próxima resposta, resolução e fechamento.
- **Padrão aprovado** (ATD-02): urgente 1 h e 4 h; alta 4 h e 2 dias úteis; média 1 dia útil e 5 dias úteis; baixa 2 dias úteis e 10 dias úteis (primeira resposta e resolução). Ajustável por entidade dentro do limite do contrato.
- **Fechamento automático:** 3 dias úteis após `resolvido`, sem resposta do solicitante.
- **Pausa:** tempo em `aguardando_*` não conta.
- **Sem SLA:** sem valor definido, o chamado não recebe prazo e o painel mostra "sem SLA".
- **Alertas:** 80% do prazo consumido e prazo estourado; o estouro aparece no painel do gestor, não no portal do solicitante.""",
  decisoes="- Nenhuma decisão nova: valores e regras já aprovados (ATD-02).",
  papeis="- `platform.manager`: configurar regras e calendário; ver o painel completo.\n- `platform.operator`: ver o prazo dos próprios chamados.",
  dados="- Regras de SLA e contagem no DDL do atendimento ([51]({51-ddl-modulos-novos.md}), seção 1).",
  integracoes="- Chamados: prazo calculado na abertura e recalculado em cada mudança de estado.\n- Notificações de alerta e de estouro ([57]({57-notificacoes-por-portal.md})).\n- Contrato do cliente: limite de SLA contratado.",
  pendencias="- Nenhuma além das do atendimento ([32]({32-atendimento-privacidade-por-portal.md}), seção 2.10)."),
 dict(arquivo='desenvolvedor/seguranca-e-operacao/acesso.md', v1=['spec_gestao_autenticacao_completo.md', 'spec_gestao_cookies_sessions.md'],
  titulo='Acesso (identidade, autenticação, sessão e autorização)', portal='Desenvolvedor (`desenvolvedor.`)', area='Segurança e operação', dominio=PLAT,
  objetivo='Gerir contas, vínculos, papéis, sessões e tokens de toda a plataforma: conta global única, login no domínio de autenticação, RBAC com contexto e contas de plataforma.',
  correcoes="""- **O [06]({06-identidade-acesso.md}) prevalece em tudo** que as especificações da v1 duplicam ([19]({19-regras-modulos-3.md}), seção 2): tipos de identidade, autenticação, senhas, recuperação de conta, limites de tentativa, sessão, tokens de API, RBAC com contexto, contas de plataforma (break-glass) e conta global com vínculos (seção 12). A v1 fica só com o que é específico de tela.
- **Cookies e sessões** ficam no [06]({06-identidade-acesso.md}); a especificação de cookies da v1 é aproveitada só no que não contradiz o 06.
- **Conta global por e-mail verificado** (D-21) e **token só com o contexto ativo** (D-20) ([06]({06-identidade-acesso.md}), seção 12).
- **Login só no domínio de autenticação**, com OIDC e PKCE (D-22, [23]({23-dominios-provisionamento-ciclo-de-vida.md}), seção 2).
- **Papéis e níveis** conforme o [78]({78-permissoes-e-papeis.md}); criação de entidade e unidade só por `platform.developer` (L-02).
- **Contas de plataforma:** no máximo 5 ativas, passkey obrigatória, alerta em tempo real a cada uso; break-glass com credencial offline em dois cofres ([06]({06-identidade-acesso.md}), seção 10).""",
  decisoes="- Nenhuma decisão nova: regras do [06]({06-identidade-acesso.md}) e do [78]({78-permissoes-e-papeis.md}).",
  papeis="- `platform.security` (papel **Segurança** do [22]({22-crm-canais-e-papeis.md}), seção 5): investigar, bloquear conta; não concede permissão a si mesmo.\n- `platform.manager` e `platform.developer`: conceder papéis conforme o nível ([78]({78-permissoes-e-papeis.md}), seção 2.1).\n- Toda concessão e revogação com justificativa para níveis 3 e acima; revisão trimestral.",
  dados="- Contas e vínculos no master; dados civis no banco de identidade da entidade (D-19). Modelos da v1 (seção 13) só onde não contradizem o [06]({06-identidade-acesso.md}).",
  integracoes="- E-mail transacional da plataforma para verificação e recuperação (D-04, [16]({16-integracoes-externas.md}), seção 2).\n- Captcha após tentativas ([06]({06-identidade-acesso.md}), seção 6).",
  privacidade="- Login, sessão e vínculos registrados na auditoria do master ([29]({29-auditoria.md}), seção 3).",
  pendencias="- Nenhuma além das do [06]({06-identidade-acesso.md}) e do [45]({45-pendencias-consolidadas.md})."),
 dict(arquivo='desenvolvedor/seguranca-e-operacao/mfa.md', v1=[],
  titulo='MFA (autenticação multifator)', portal='Desenvolvedor (`desenvolvedor.`)', area='Segurança e operação', dominio=PLAT,
  objetivo='Configurar e acompanhar a autenticação multifator de todas as contas, com regra mais forte para contas de plataforma.',
  telas="""- **Política de MFA** (configuração): fatores aceitos, obrigatoriedade por tipo de conta e por papel.
- **Painel de MFA** (dashboard): contas com e sem MFA por portal, passkeys cadastradas, contas de plataforma sem passkey.
- **Fatores da conta** (drawer em Acesso): cadastrar, revogar e recuperar fator, com step-up.""",
  correcoes="""- **MFA** conforme o [06]({06-identidade-acesso.md}), seção 5: fatores, cadastro e recuperação. **SMS não é fator de MFA** ([16]({16-integracoes-externas.md}), seção 2).
- **Contas de plataforma:** passkey obrigatória; conta sem passkey é desativada no primeiro login após a migração ([06]({06-identidade-acesso.md}), seção 10).
- **Step-up:** ações sensíveis (exportação, alteração de papel, exclusão, ver segredo de integração) exigem autenticação recente ([78]({78-permissoes-e-papeis.md}), seção 5).
- A especificação de autenticação da v1 que trata de MFA está absorvida na ficha [acesso.md](acesso.md).""",
  decisoes="- Nenhuma decisão nova.",
  papeis="- `platform.security`: política de MFA e painel.\n- Cada usuário: os próprios fatores.",
  dados="- Fatores e passkeys no master, cifrados ([05]({05-seguranca.md})).",
  integracoes="- E-mail transacional para recuperação (D-04).",
  pendencias="- Nenhuma além das do [06]({06-identidade-acesso.md})."),
 dict(arquivo='desenvolvedor/seguranca-e-operacao/auditoria.md', v1=['spec_gestao_auditoria_completo.md', 'spec_gestao_logger_completo.md'],
  titulo='Auditoria', portal='Desenvolvedor (`desenvolvedor.`)', area='Segurança e operação', dominio=PLAT,
  objetivo='Registrar, proteger e consultar a trilha de auditoria de negócio e de segurança da plataforma, com integridade por cadeia de hash e acesso controlado.',
  correcoes="""- **O [29]({29-auditoria.md}) prevalece:** categorias, formato do evento, onde fica (ações da plataforma no master; ações de unidade no banco da unidade), integridade por cadeia de hash com verificação horária e ancoragem diária, imutabilidade (a aplicação só faz `INSERT` e `SELECT`), acesso por papel, mascaramento, retenção e alertas.
- **Auditoria × Logger** ([19]({19-regras-modulos-3.md}), seção 2): a Auditoria é dona da trilha de negócio e de segurança ([18]({18-regras-modulos-2.md}), seção 4); o logger técnico fica no [10]({10-implantacao-operacao.md}), seção 7. A especificação do Logger da v1 é absorvida só como referência técnica, sem dado pessoal nos logs ([07]({07-privacidade-lgpd.md}), seção 6).
- **Toda leitura gera evento** (`audit.read`); exportação exige MFA recente e motivo; auditoria de outra entidade é impossível pela aplicação ([29]({29-auditoria.md}), seção 5).
- **Suporte da plataforma** vê eventos técnicos e de sessão do chamado, sem dado de aluno sem vínculo.""",
  decisoes="- Nenhuma decisão nova.",
  papeis="- `platform.auditor` (nível 2): leitura de auditoria e relatórios de conformidade, com mascaramento padrão.\n- `platform.security`: investigação e alertas.\n- `platform.dpo`: consultas por CPF, leituras de cadastro civil e pedidos de titular.\n- Ninguém altera evento: correção é novo evento que referencia o original.",
  dados="- Esquema do evento do [29]({29-auditoria.md}), seção 2, que prevalece sobre os modelos da v1.",
  integracoes="- Exportação diária assinada para armazenamento de longo prazo ([29]({29-auditoria.md}), seção 3).\n- Alertas para o canal de segurança ([29]({29-auditoria.md}), seção 8).",
  pendencias="- Lacunas do [29]({29-auditoria.md}), seção 10."),
 dict(arquivo='desenvolvedor/seguranca-e-operacao/privacidade-dpo.md', v1=['spec_gestao_privacy_global_completo.md', 'spec-sub-sidebar-privacidade-lgpd.md'],
  titulo='Privacidade e encarregado (DPO) da plataforma', portal='Desenvolvedor (`desenvolvedor.`)', area='Segurança e operação', dominio=PLAT,
  objetivo='Cumprir a LGPD como controladora (dados da própria plataforma) e como operadora (dados das entidades): inventário, bases legais, consentimento, pedidos de titular, ROPA, incidentes e painel do DPO.',
  correcoes="""- **O [07]({07-privacidade-lgpd.md}) e o [32]({32-atendimento-privacidade-por-portal.md}), seções 3 a 5, prevalecem** ([19]({19-regras-modulos-3.md}), seção 2: privacidade global consolidada no 07; cookies e sessões no 06).
- **DPO da plataforma** (LGPD-07, [32]({32-atendimento-privacidade-por-portal.md}), seção 7): a empresa desenvolvedora, por encarregado indicado por ela, com painel no portal do desenvolvedor. Cada entidade designa o próprio DPO.
- **Painel do DPO** ([32]({32-atendimento-privacidade-por-portal.md}), seção 3.7); **pedido do titular** (seção 3.3); **ROPA** (seção 3.4); **incidentes e comunicação à ANPD** ([07]({07-privacidade-lgpd.md}), seção 8).
- **Operadora:** a plataforma não usa dado de entidade fora do contrato de tratamento ([07]({07-privacidade-lgpd.md}), seção 7).
- **Separação de funções:** o DPO não opera o módulo que audita ([22]({22-crm-canais-e-papeis.md}), seção 5).""",
  decisoes="- Nenhuma decisão nova.",
  papeis="- `platform.dpo` (papel **Encarregado** do [22]({22-crm-canais-e-papeis.md}), seção 5): relatório de impacto, relatório ao titular, aprovação de finalidade, painel do DPO.",
  dados="- Consentimentos, pedidos de titular, ROPA e incidentes da plataforma no master. Modelos da v1 (seção 13) só onde não contradizem o [07]({07-privacidade-lgpd.md}).",
  integracoes="- Atendimento: pedido de titular recebe protocolo (ATD-01).\n- Auditoria: consultas por CPF e leituras de cadastro civil ([29]({29-auditoria.md}), seção 5).",
  privacidade="- Métricas de privacidade conforme [07]({07-privacidade-lgpd.md}), seção 9.",
  pendencias="- Forma de designação e contato público do DPO (jurídico), no [32]({32-atendimento-privacidade-por-portal.md}), seção 7.\n- Lacunas do [07]({07-privacidade-lgpd.md}), seção 10."),
 dict(arquivo='desenvolvedor/seguranca-e-operacao/ti.md', v1='spec_gestao_ti_completa.md',
  titulo='TI da plataforma', portal='Desenvolvedor (`desenvolvedor.`)', area='Segurança e operação', dominio=PLAT,
  objetivo='Operar a infraestrutura da plataforma: backup e restauração, certificados, monitoramento, filas, cache, manutenção programada e segredos.',
  correcoes="""- **Dois assuntos com o mesmo nome** ([36]({36-tecnologia-da-informacao-por-portal.md}), seção 2): esta ficha é a TI **da plataforma** (seção 3 do 36). A TI **da entidade** (ativos, chamados, licenças da escola) fica no portal de gestão.
- **Recursos** ([36]({36-tecnologia-da-informacao-por-portal.md}), seção 3): backup e restauração ([24]({24-operacao-continuidade-qualidade.md}), seção 1), certificados com alerta a 14 dias ([10]({10-implantacao-operacao.md}), seção 7), monitoramento, filas e workers ([14]({14-integracao-modulos.md})), cache ([30]({30-cache.md})), manutenção programada ([24]({24-operacao-continuidade-qualidade.md}), seção 3), inventário de segredos ([05]({05-seguranca.md}), seção 2).
- **Toda ação de infraestrutura** é registrada na auditoria, categoria "processo", com `portal = desenvolvedor`.
- **Mudança sem plano de volta não é aprovada** ([36]({36-tecnologia-da-informacao-por-portal.md})).
- **`sub_sidebar_itsm.php`** da v1 é código de view com `onclick=` (ACH-01) e não faz parte desta ficha ([12]({12-catalogo-modulos.md}), seção 3).""",
  decisoes="- Nenhuma decisão nova. Escolha de provedor de nuvem, DNS e cluster segue o [10]({10-implantacao-operacao.md}).",
  papeis="- `platform.ops` (papel **TI / Operação** do [22]({22-crm-canais-e-papeis.md}), seção 5): operar serviços, filas, backup e certificados; sem acesso a dado pessoal de entidade.\n- `platform.developer`: aprovar mudança e manutenção programada (segundo papel).",
  dados="- Inventário de serviços, certificados e segredos no master; segredos só por referência ao cofre.",
  integracoes="- Monitoramento e erros, sem PII ([16]({16-integracoes-externas.md}), seção 2).\n- Backup externo cifrado, com chave fora do provedor.",
  pendencias="- Lacunas do [36]({36-tecnologia-da-informacao-por-portal.md}), seção 3: prazo de retenção de backup (G-12), dono de cada certificado, painel por serviço e escalonamento, limite de fila por entidade, dimensionamento do cache (CAC-01), janela de manutenção e aviso, provedor de nuvem."),
 dict(arquivo='desenvolvedor/seguranca-e-operacao/configuracoes-do-sistema.md', v1=['language_locale_selector_spec.md', '06-i18n-l10n.md'],
  titulo='Configurações do sistema', portal='Desenvolvedor (`desenvolvedor.`)', area='Segurança e operação', dominio=PLAT,
  objetivo='Manter as configurações globais da plataforma, agrupadas pelo documento do SDD que define cada regra, com mudança auditada e reversível.',
  correcoes="""- **Idiomas e locale:** o [09]({09-internacionalizacao.md}) prevalece; as especificações da v1 de idioma e seletor de locale estão consolidadas nele ([12]({12-catalogo-modulos.md})).
- **Grupos de configuração** (DP-04): idiomas e formatos ([09]({09-internacionalizacao.md})); senha, sessão e MFA ([06]({06-identidade-acesso.md})); limites de API ([04]({04-api.md})); e-mail e integrações ([16]({16-integracoes-externas.md})); cache ([30]({30-cache.md})); manutenção ([24]({24-operacao-continuidade-qualidade.md})); tokens e webhooks ([04]({04-api.md}), [16]({16-integracoes-externas.md})).
- **Valor fora do limite** do documento de origem é recusado (por exemplo, sessão mais longa que o máximo do 06).
- Configurações de entidade (feriados, fuso, campos personalizados) ficam no portal de gestão ([56]({56-configuracoes-e-relatorios-lacunas.md}), seção 2).""",
  decisoes="- **DP-04** ([80]({80-decisoes-por-padrao.md})): grupos pelo documento de origem; toda mudança com step-up, motivo, auditoria e versão com rollback.",
  papeis="- `platform.developer`: alterar configurações de segurança e de limites.\n- `platform.ops`: alterar configurações operacionais (cache, manutenção).\n- Toda mudança vista por `platform.auditor`.",
  dados="- Configurações versionadas no master: chave, valor, versão, autor, motivo, data.",
  integracoes="- Cache: invalidação na mudança de configuração ([30]({30-cache.md})).",
  pendencias="- Nenhuma além das do [09]({09-internacionalizacao.md})."),
 dict(arquivo='desenvolvedor/seguranca-e-operacao/integracoes-globais.md', v1='spec_complementar_integracoes_governanca.md',
  titulo='Integrações globais (plataforma)', portal='Desenvolvedor (`desenvolvedor.`)', area='Segurança e operação', dominio=PLAT,
  objetivo='Gerir as integrações contratadas e pagas pela plataforma e acompanhar, sem ver segredos, as integrações das entidades.',
  correcoes="""- **Dois níveis** ([16]({16-integracoes-externas.md}), seção 1): plataforma (credencial no cofre da plataforma, permissão `plataforma.integracao.*`) e tenant (cofre com chave por tenant).
- **Credencial de tenant** nunca visível em texto claro para a equipe da plataforma; ver o segredo exige step-up, motivo e alerta ao canal de segurança.
- **Catálogo da plataforma** ([16]({16-integracoes-externas.md}), seção 2): e-mail transacional (obrigatório), SMS (não é MFA, desligado por padrão), armazenamento de objetos, antivírus de upload, captcha, cobrança da assinatura do SaaS, backup externo, monitoramento sem PII, verificação de documento opcional.
- **Ciclo de vida, segurança das chamadas, auditoria e testes** ([16]({16-integracoes-externas.md}), seções 5, 7, 9 e 10); governança da v1 ligada ao [04]({04-api.md}), seção 7.""",
  decisoes="- Nenhuma decisão nova (D-04 a D-08 aprovadas no [16]({16-integracoes-externas.md}), seção 6).",
  papeis="- `platform.integration` (nível 6): configurar integrações de plataforma (`plataforma.integracao.*`).\n- `platform.security`: autorizar a visualização de segredo de tenant, com motivo.",
  dados="- Conexões e segredos por referência ao cofre; nunca em texto claro no banco.",
  integracoes="- Todas as do catálogo do [16]({16-integracoes-externas.md}), seção 2.",
  pendencias="- Escolha do provedor de captcha (ADR próprio, [16]({16-integracoes-externas.md}), seção 2)."),
 dict(arquivo='desenvolvedor/seguranca-e-operacao/painel-de-bancos-de-dados.md', v1=[],
  titulo='Painel de bancos de dados', portal='Desenvolvedor (`desenvolvedor.`)', area='Segurança e operação', dominio=PLAT,
  objetivo='Gerir todos os bancos da plataforma (master, bancos de unidade e bancos de identidade) sem expor o conteúdo deles. Substitui o módulo "Bancos" da v1, removido do escopo (PAG-03).',
  telas="""- **Inventário de bancos** (datatable): master, cada banco de unidade, cada banco de identidade; versão do esquema, tamanho e última restauração testada.
- **Migrações** (datatable por unidade e página de migração em lote com plano de volta e aprovação).
- **Backups** (datatable): estado e prazo de cada backup; pedido de restauração com dupla aprovação.
- **Acesso técnico de emergência** (página de pedido): motivo, chamado vinculado, tempo da sessão, leitura ou escrita.""",
  correcoes="""- **Regras do [34]({34-pagamentos-fiscal-bancos-por-portal.md}), seção 4 (PAG-03):**
  - Não existe console SQL no painel comum.
  - Migração em lote só com plano de volta e aprovação de segundo papel.
  - Restauração só por pedido com dupla aprovação, em ambiente isolado.
  - Acesso técnico direto só por procedimento de emergência: passkey, motivo e chamado vinculado, sessão de tempo limitado, leitura por padrão, escrita só com dupla aprovação; cada comando gravado e mascarado ([29]({29-auditoria.md})).
  - Consulta que atinja dado pessoal exige motivo e gera evento de auditoria.
  - Nenhum portal de entidade vê este painel.
- **Especificações "Bancos" da v1** (`spec_gestao_bancos.md` e `spec_gestao_bancos_completo.md`): fora do escopo e **não absorvidas**, porque expõem console SQL a todos os clientes ([03]({03-dominio-tenancy.md})).""",
  decisoes="- Nenhuma decisão nova (PAG-03 decidido em 03/11/2026).",
  papeis="- `platform.ops`: consultar inventário, acompanhar migrações e backups, pedir restauração e acesso de emergência.\n- `platform.developer`: aprovar migração em lote, restauração e escrita de emergência (segundo papel); a dupla aprovação exige duas pessoas diferentes de quem pediu.",
  dados="- Metadados dos bancos no master (`tenant_databases`, versão de esquema, backups). Nenhum dado de cliente é lido pelo painel.",
  integracoes="- Provisionamento ([provisionamento.md](../plataforma-e-clientes/provisionamento.md)): cria banco e registro.\n- Backup externo ([16]({16-integracoes-externas.md}), seção 2).",
  pendencias="- Prazo de retenção de backup (G-12, [36]({36-tecnologia-da-informacao-por-portal.md}), seção 3)."),
 dict(arquivo='transversal/exclusao-logica.md', v1='spec-soft-delete-totustuus.md',
  titulo='Exclusão lógica (soft delete)', portal='Todos', area='Transversal', dominio=TRANSV,
  objetivo='Regra única de exclusão lógica para toda tabela que aceita exclusão: colunas, validação prévia, unicidade, cascata lógica, restauração, expurgo e testes.',
  correcoes="""- **Exclusão é lógica por padrão** (`deleted_at`); física só pelo processo de retenção ou pedido do titular ([03]({03-dominio-tenancy.md}), seção 6).
- **Colunas** `deleted_at` e `deleted_by` em toda tabela que aceita exclusão ([19]({19-regras-modulos-3.md}), seção 14).
- **Exclusão bloqueada se houver dependente ativo**; a resposta lista só os tipos de dependentes, sem dados ([15]({15-validacoes.md}), seções 4 e 5). Motivo obrigatório para registros financeiros e de saúde.
- **Auditoria nunca é expurgada por soft delete** ([19]({19-regras-modulos-3.md}), seção 14; [29]({29-auditoria.md})).
- **IA não executa nem sugere exclusão** ([28]({28-cobertura-ia-todos-os-modulos.md})).""",
  decisoes="- Nenhuma decisão nova.",
  papeis="- Quem pode excluir é definido pela permissão `modulo.recurso.excluir` de cada módulo ([78]({78-permissoes-e-papeis.md})); restaurar exige a mesma permissão; expurgo só pelo job de retenção.",
  dados="- Índices de unicidade consideram `deleted_at` conforme a v1 (seção 13), sem permitir dois registros ativos iguais.",
  integracoes="- Busca e cache removem o registro excluído do índice ([21]({21-busca-e-armazenamento.md}), [30]({30-cache.md})).",
  pendencias="- Prazo de expurgo por tipo de dado: matriz de retenção ([26]({26-sdd-juridico-regulatorio.md}), seção 3)."),
 dict(arquivo='transversal/arquitetura-da-plataforma.md', v1='spec_education_saas_architecture.md',
  titulo='Arquitetura da plataforma educacional SaaS', portal='Todos', area='Transversal', dominio=TRANSV,
  objetivo='Visão de arquitetura da v1 (visão, princípios, áreas, tenant, identidade, portais, módulos, dados, banco, segurança e API), guardada integralmente e subordinada à arquitetura da v2.',
  correcoes="""- **Arquitetura, camadas, middleware e ADRs:** o [02]({02-arquitetura.md}) prevalece.
- **Tenant, unidade e bancos:** o [03]({03-dominio-tenancy.md}) prevalece (banco por unidade, master da plataforma, banco de identidade da entidade).
- **Identidade:** o [06]({06-identidade-acesso.md}) prevalece (conta global, vínculos e contexto, seção 12).
- **Portais e módulos:** a matriz [31]({31-matriz-portais-modulos.md}) prevalece; papéis no [78]({78-permissoes-e-papeis.md}).
- **API:** o [04]({04-api.md}) prevalece.""",
  decisoes="- Nenhuma decisão nova.", papeis="- Não se aplica (documento de arquitetura).",
  dados="- Domínios de dados conforme [03]({03-dominio-tenancy.md}) e DDL do [51]({51-ddl-modulos-novos.md}).",
  integracoes="- [14]({14-integracao-modulos.md}) e [16]({16-integracoes-externas.md}).",
  pendencias="- Riscos arquiteturais conhecidos ([02]({02-arquitetura.md}), seção 8)."),
 dict(arquivo='transversal/build-e-procedencia-slsa.md', v1='slsa-build-spec.md',
  titulo='Build, procedência e SLSA', portal='Todos', area='Transversal', dominio=TRANSV,
  objetivo='Pipeline de build com procedência verificável (SLSA), SBOM, assinatura de artefatos, gate de deploy, cofre de segredos e logs de build.',
  correcoes="""- **Pipeline e ambientes:** o [10]({10-implantacao-operacao.md}), seções 2 a 4, prevalece; gates de entrega no [11]({11-governanca-qualidade.md}), seção 3.
- **SBOM CycloneDX, assinatura e procedência SLSA** estão marcados como **[Planejado]** no [05]({05-seguranca.md}); esta ficha é o roteiro de implementação.
- **Segredos:** cofre e nenhum segredo em repositório ou log ([10]({10-implantacao-operacao.md}), seção 3; [05]({05-seguranca.md}), seção 2).
- **IA:** só explica falha de build; não aprova release ([28]({28-cobertura-ia-todos-os-modulos.md})).""",
  decisoes="- Nenhuma decisão nova.", papeis="- `platform.ops` opera o pipeline; `platform.developer` aprova release (segundo papel).",
  dados="- Atestados de procedência e SBOM guardados por versão publicada.", integracoes="- Cofre de segredos e armazenamento de artefatos ([16]({16-integracoes-externas.md}), seção 2).",
  pendencias="- Nível SLSA alvo e prazo (ADR, [11]({11-governanca-qualidade.md}), seção 4)."),
 dict(arquivo='transversal/teste-de-intrusao.md', v1='penetration-test-spec-v2.md',
  titulo='Teste de intrusão (pentest)', portal='Todos', area='Transversal', dominio=TRANSV,
  objetivo='Fases, responsabilidades e checklist do teste de intrusão externo e interno.',
  correcoes="""- **Estratégia de testes e pentest externo:** o [24]({24-operacao-continuidade-qualidade.md}), seção 5, prevalece; escopo definido por esta ficha.
- **Divulgação de vulnerabilidade:** [24]({24-operacao-continuidade-qualidade.md}), seção 6.
- **Testes de tenancy e de identidade** são critério de aceite obrigatório ([03]({03-dominio-tenancy.md}), seção 7; [06]({06-identidade-acesso.md}), seção 11).""",
  decisoes="- Nenhuma decisão nova.", papeis="- `platform.security` coordena; o pentest externo é contratado; achados viram chamados com SLA de correção.",
  dados="- Relatórios de pentest com acesso restrito a `platform.security` e `platform.developer`.", integracoes="- Não se aplica.",
  pendencias="- Periodicidade e fornecedor do pentest externo ([24]({24-operacao-continuidade-qualidade.md}), seção 9)."),
 dict(arquivo='transversal/navegacao-dos-portais.md', v1='12-portals-navigation-sidebar-pages-spec.md',
  titulo='Navegação dos portais (sidebars e páginas)', portal='Todos', area='Transversal', dominio=TRANSV,
  objetivo='Arquitetura de navegação dos seis portais (sidebar e sub-sidebar), matriz de páginas da v1, checklist de 21 itens de layout e governança de segurança da navegação.',
  correcoes="""- **Matriz de portais, áreas e módulos:** a [31]({31-matriz-portais-modulos.md}) prevalece; itens da v1 fora da matriz não entram no menu sem passar pela matriz.
- **Layout, componentes e acessibilidade:** o [08]({08-frontend-design-system.md}) prevalece; o checklist de 21 itens da v1 (seção 13) vale onde não contradiz o 08.
- **Menu por permissão:** item sem permissão não aparece e a rota responde 404 ou 403 (default-deny, [78]({78-permissoes-e-papeis.md}), seção 5).
- **Itens só citados na v1** (mural, materiais, tarefas) ganharam regra no DP-06 ([80]({80-decisoes-por-padrao.md})).
- **`sub_sidebar_itsm.php`** é código de view com `onclick=` (ACH-01) e não é especificação ([12]({12-catalogo-modulos.md}), seção 3).""",
  decisoes="- DP-06 ([80]({80-decisoes-por-padrao.md})).", papeis="- O menu de cada portal é montado pelos papéis do [78]({78-permissoes-e-papeis.md}).",
  dados="- Itens de menu publicados pelo Editor de portais ([editor-de-portais](../desenvolvedor/editor-de-portais/)).", integracoes="- Editor de portais (D-23).",
  pendencias="- Nenhuma."),
 dict(arquivo='transversal/plano-de-implementacao-v1.md', v1='TASKS_SPECS.md',
  titulo='Plano de implementação da v1 (fases e checklist)', portal='Todos', area='Transversal', dominio=TRANSV,
  objetivo='Plano de tarefas da v1 (fases 0 a 3, ordem de dependência e checklist de 18 itens por módulo), guardado integralmente como referência de ordem de construção.',
  correcoes="""- **Ordem de construção da v2:** fundações transversais (tenancy [03]({03-dominio-tenancy.md}), identidade [06]({06-identidade-acesso.md}), auditoria [29]({29-auditoria.md}), exclusão lógica, privacidade [07]({07-privacidade-lgpd.md})), depois o acadêmico na ordem do [55]({55-academico-verificacao-e-lacunas.md}), seção 3, e os demais módulos pela matriz [31]({31-matriz-portais-modulos.md}).
- **Definition of Done e gates:** [11]({11-governanca-qualidade.md}), seções 2 e 3.
- **Caminho `C:\\Xampp\\htdocs\\ttscdoc\\` e o progresso de 10/07/2026** são da v1 e não valem para a v2.""",
  decisoes="- Nenhuma decisão nova.", papeis="- Não se aplica.", dados="- Não se aplica.", integracoes="- Não se aplica.",
  pendencias="- Backlog priorizado: [11]({11-governanca-qualidade.md}), seção 8."),
]

for cfg in FICHAS:
    destino, n = monta(cfg)
    print(os.path.relpath(destino, ROOT), n, 'linhas')
