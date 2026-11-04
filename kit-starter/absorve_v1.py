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


def rebaixa(texto, niveis=2):
    out, codigo = [], False
    for linha in texto.splitlines():
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
    v1 = os.path.join(V2, 'anexo-v1', cfg['v1'])
    texto_v1 = open(v1, encoding='utf8').read()
    r = lambda doc: rel(d, os.path.join(V2, doc))
    linha = lambda t: re.sub(r'\{(\d\d-[^}]+\.md)\}', lambda m: r(m.group(1)), t)
    corpo = f"""# {cfg['titulo']}

- Portal: {cfg['portal']}
- Área: {cfg['area']}
- Domínio: {linha(cfg['dominio'])}
- Status: detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)
- Fonte da v1: [{cfg['v1']}]({rel(d, v1)}) ({len(texto_v1.splitlines())} linhas)

## 1. Regra de leitura
As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.

## 2. Objetivo e escopo
{linha(cfg['objetivo'])}

## 3. Telas (índice da v1)
{telas(texto_v1)}

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
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([{{08}}]({r('08-frontend-design-system.md')}), seção 3).
- Auditoria conforme [29]({r('29-auditoria.md')}); dados pessoais conforme [07]({r('07-privacidade-lgpd.md')}).
{linha(cfg.get('privacidade', ''))}

## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08]({r('08-frontend-design-system.md')})).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
{linha(cfg['pendencias'])}

## 13. Conteúdo integral da v1 (absorvido)

{rebaixa(texto_v1)}
"""
    corpo = corpo.replace('[{08}]', '[08]')
    open(destino, 'w', encoding='utf8').write(corpo)
    return destino, len(corpo.splitlines())


PLAT = 'plataforma (banco master), instância separada do módulo das entidades ([31]({31-matriz-portais-modulos.md}), seção 2.1)'
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

]

for cfg in FICHAS:
    destino, n = monta(cfg)
    print(os.path.relpath(destino, ROOT), n, 'linhas')
