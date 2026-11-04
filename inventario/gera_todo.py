"""Gera docs/TODO-IMPLEMENTACAO.md: o TODO completo para implementar o SDD, fase por fase.

Uso: python3 inventario/gera_todo.py
Fontes: kit-starter/**/*.md (módulos e telas), plano de implementação (parte 20 do SDD único),
documento 45 (pendências). Cada módulo vira uma lista de tarefas com as telas da ficha.
Não editar à mão: regere depois de mudar o kit ou o SDD. Marque o progresso numa cópia de trabalho
ou num gerenciador de tarefas a partir deste arquivo.
"""
import glob, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KIT = os.path.join(ROOT, 'kit-starter')
SAIDA = os.path.join(ROOT, 'docs', 'TODO-IMPLEMENTACAO.md')

FASES = [
    ('F0', 'Fundação', 'Tenancy, identidade, permissões, auditoria, cofre, exclusão lógica, privacidade base, internacionalização, design system, pipeline e observabilidade.'),
    ('F1', 'Plataforma SaaS', 'Provisionamento, domínios, licenciamento, Editor de portais, CRM e financeiro da plataforma, suporte e operação.'),
    ('F2', 'Acadêmico núcleo', 'Estrutura acadêmica, calendário, turmas e grade, matrícula e rematrícula, diário, boletim e conselho.'),
    ('F3', 'Secretaria e documentos', 'Protocolo, emissão de documentos, gestão de documentos, livros e arquivo morto.'),
    ('F4', 'Financeiro e fiscal da entidade', 'Mensalidades, títulos, cobrança, régua, conciliação, gateways e split, contas a pagar, caixa, DRE, contábil e fiscal, empenho.'),
    ('F5', 'Portais do professor, do aluno e dos responsáveis', 'Classe, diário do professor, planos, portais pessoais e notificações.'),
    ('F6', 'Gestão de apoio', 'Pessoas e SST, suprimentos, patrimônio e frotas, contratos, terceiros, biblioteca, simulados, atendimento, CRM do tenant e operações internas da plataforma.'),
    ('F7', 'Complementos', 'Aulas online, formulários, preceptoria, pastoral, agendamento, ocorrências, estágio e TCC, prontuário, relatórios e censo, importação, campos personalizados, integrações oficiais, acesso físico, TI da entidade e planejamento.'),
]

# prefixo do caminho da ficha (relativo a kit-starter/) -> fase; o primeiro que casar vale
REGRAS = [
    ('transversal/plano-de-implementacao-v1', 'F0'), ('transversal/', 'F0'),
    ('desenvolvedor/seguranca-e-operacao/ti', 'F1'), ('desenvolvedor/seguranca-e-operacao/integracoes-globais', 'F1'),
    ('desenvolvedor/seguranca-e-operacao/painel-de-bancos', 'F1'), ('desenvolvedor/seguranca-e-operacao/', 'F0'),
    ('gestao/configuracao-e-acesso/unidades', 'F0'), ('gestao/configuracao-e-acesso/usuarios', 'F0'),
    ('gestao/configuracao-e-acesso/vinculos', 'F0'), ('gestao/configuracao-e-acesso/privacidade', 'F0'),
    ('gestao/configuracao-e-acesso/configuracoes', 'F0'), ('gestao/configuracao-e-acesso/notificacoes', 'F5'),
    ('gestao/configuracao-e-acesso/', 'F7'),
    ('desenvolvedor/operacoes-internas', 'F6'), ('desenvolvedor/pessoas-da-plataforma', 'F6'), ('desenvolvedor/', 'F1'),
    ('gestao/academico/administracao', 'F2'), ('gestao/academico/calendario', 'F2'), ('gestao/academico/series', 'F2'),
    ('gestao/academico/regras-de-aprovacao', 'F2'), ('gestao/academico/pedagogico', 'F2'),
    ('gestao/academico/planos-de-aula', 'F5'), ('gestao/academico/livros', 'F3'), ('gestao/academico/', 'F7'),
    ('gestao/secretaria/protocolo', 'F3'), ('gestao/secretaria/emissao', 'F3'), ('gestao/secretaria/', 'F2'),
    ('gestao/gestao-de-documentos', 'F3'),
    ('gestao/financeiro', 'F4'), ('gestao/contabil', 'F4'), ('gestao/empenho', 'F4'),
    ('gestao/planejamento', 'F7'), ('gestao/relatorios', 'F7'), ('gestao/arquivos', 'F6'), ('gestao/', 'F6'),
    ('professor/', 'F5'), ('aluno/', 'F5'), ('responsaveis/', 'F5'), ('terceiros/', 'F6'),
]

PRE = """## Pré-requisitos (antes da F0)

- [ ] Nomear o responsável técnico e o owner de cada módulo (SDD, documento 11, seção 5). Sem owner, nenhuma revisão de DDL acontece.
- [ ] Escolher o provedor de nuvem; com ele, o KMS ou HSM da chave-mestra (DP-11), o CDN (CAC-03) e o Redis (CAC-01).
- [ ] Comparar o código atual (`jeffersongontijo765/totustuussoftcloud.academic`) com o SDD v2 e decidir, por módulo, reaproveitar, refatorar ou reescrever. Pontos de base que mudam na v2:
    - [ ] Banco master, banco de identidade por entidade e banco por unidade (documento 03, D-16, D-19).
    - [ ] Conta global, vínculos e contexto no token (documento 06, seção 12).
    - [ ] Login único com OIDC e PKCE (D-22) e sessão opaca no navegador (DP-10).
    - [ ] Permissões `modulo.recurso.acao`, níveis 0 a 7 e default-deny (documento 78).
    - [ ] Auditoria com cadeia de hash (documento 29).
    - [ ] Sem JavaScript inline nem `on*=` (ADR-07, ACH-01).
- [ ] Escrever o contrato OpenAPI de cada módulo antes da implementação, no padrão do documento 04 (versão, autenticação, schema, idempotência, erros).
- [ ] Montar o pipeline de CI na ordem do documento 10, seção 4: segredos, lint e análise estática, dependências, testes, build com SBOM, verificação do artefato, migrações com plano de volta, homologação, testes de fumaça.
- [ ] Criar o ambiente de homologação com MariaDB 10.11 ou MySQL 8 em `utf8mb4` e rodar `python3 inventario/valida_ddl.py --socket <socket>` (278 tabelas, 0 erros esperado) e `python3 inventario/lint_ddl.py`.
"""

F0_BASE = """### Infraestrutura da fundação

- [ ] Cadeia de middleware na ordem fixa (documento 02, seção 3): SecurityHeaders, RequestId, RateLimit por IP, Csrf, sessão e Auth, TenantContext, Authorize, Audit.
- [ ] Banco master e registro de bancos de unidade (`tenant_databases`); seleção de conexão pela unidade autorizada (documento 03, seção 1.1).
- [ ] Repositório base com filtro de tenant obrigatório; consulta sem filtro falha em teste (documento 02, seção 2).
- [ ] Exclusão lógica (`deleted_at`, `deleted_by`) e regra do DP-09 para tabela sem a coluna.
- [ ] Cofre `TotusTuus\\Vault` com envelope de chaves e chave-mestra no KMS (ADR-05, DP-11); `FileVault` só em desenvolvimento.
- [ ] Integração entre módulos por eventos, com outbox e idempotência (documento 14).
- [ ] Cache com chave por tenant (documento 30).
- [ ] Internacionalização: inglês canônico, `pt-BR` e os demais locales com teste de paridade (documento 09).
- [ ] Design system no app: tokens, `bundle.css` e componentes (documento 08; repositório `design.system.totustuussoftcloud`).
- [ ] Observabilidade sem dado pessoal nos logs; métricas e alertas (documento 10, seção 7).
- [ ] Backup e restauração testados (documento 24, seção 1).
"""

GATE = """## Portão de produção (por módulo)

Nenhum módulo vai para produção sem:

- [ ] Critérios de aceite do documento de origem marcados.
- [ ] Testes de isolamento de tenant e de autorização passando em CI (documentos 03, seção 7, e 06, seção 11).
- [ ] DDL revisado pelo owner e migração testada em homologação (documento 45, seção 7).
- [ ] Pendências jurídicas e de norma do módulo respondidas (documento 45, seções 3 e 4). Prazo marcado **[V]** ou **[P]** não entra em produção sem confirmação (documento 26, seção 3).
- [ ] Itens de homologação do módulo medidos (documento 45, seção 6).

Situação em 04/11/2026 (documento 45): 59 jurídicos sem decisão, 14 jurídicos já decididos pelo autor, 25 de conferência de norma, 12 de homologação e 44 de revisão do owner.
"""


def fase_de(rel):
    return next((f for pref, f in REGRAS if rel.startswith(pref)), 'F7')


def ler(caminho):
    t = open(caminho, encoding='utf8').read()
    titulo = re.search(r'^# (.+)$', t, re.M).group(1).strip()
    portal = re.search(r'^- Portal: (.+)$', t, re.M)
    portal = re.sub(r'\s*\(`[^`]*`\)', '', portal.group(1)).replace('`', '').strip() if portal else ''
    m = re.search(r'^## 3\. Telas[^\n]*\n(.*?)(?=^## )', t, re.S | re.M)
    telas = []
    if m:
        for linha in m.group(1).splitlines():
            mm = re.match(r'^- \*\*(.+?)\*\*', linha)
            if mm and mm.group(1) not in telas:
                telas.append(mm.group(1))
    v2 = re.search(r'^- Fonte da v2: (.+)$', t, re.M)
    fontes = re.findall(r'\[(\d\d)\]', v2.group(1)) if v2 else re.findall(r'\[(\d\d)\]\(', t.split('## 13.')[0])[:6]
    fontes = list(dict.fromkeys(fontes))
    return titulo, portal, telas, fontes


def main():
    fichas = {}
    for caminho in sorted(glob.glob(os.path.join(KIT, '**', '*.md'), recursive=True)):
        if re.match(r'^(README|MODELO)', os.path.basename(caminho)):
            continue
        rel = os.path.relpath(caminho, KIT).replace(os.sep, '/')
        fichas.setdefault(fase_de(rel), []).append((rel, *ler(caminho)))
    linhas = [
        '# TODO completo de implementação do SDD',
        '',
        'Gerado por `inventario/gera_todo.py` a partir das 173 fichas do kit-starter e do plano de implementação (SDD, parte 20). '
        'Não editar à mão: regere depois de mudar o kit ou o SDD.',
        '',
        '**Como usar:** siga as fases na ordem. Uma fase só começa quando as fases de que depende passaram no portão de passagem. '
        'Cada módulo tem a ficha de origem (`kit-starter/...`), os documentos do SDD que o regem e as telas pelo nome.',
        '',
        '```mermaid',
        'flowchart LR',
        '  P[Pré-requisitos] --> F0[F0 Fundação]',
        '  F0 --> F1[F1 Plataforma SaaS] --> F2[F2 Acadêmico núcleo]',
        '  F0 --> F2',
        '  F2 --> F3[F3 Secretaria e documentos]',
        '  F2 --> F4[F4 Financeiro e fiscal]',
        '  F3 --> F5[F5 Portais pessoais]',
        '  F4 --> F5',
        '  F0 --> F6[F6 Gestão de apoio]',
        '  F5 --> F7[F7 Complementos]',
        '  F6 --> F7',
        '```',
        '',
    ]
    total_mod = sum(len(v) for v in fichas.values())
    total_telas = sum(len(x[3]) for v in fichas.values() for x in v)
    linhas += ['| Fase | Módulos | Telas |', '|---|---|---|']
    for cod, nome, _ in FASES:
        mods = fichas.get(cod, [])
        linhas.append(f'| {cod} {nome} | {len(mods)} | {sum(len(x[3]) for x in mods)} |')
    linhas += [f'| **Total** | **{total_mod}** | **{total_telas}** |', '', PRE]
    for cod, nome, desc in FASES:
        mods = fichas.get(cod, [])
        linhas += ['---', '', f'## {cod} — {nome}', '', desc, '']
        if cod == 'F0':
            linhas.append(F0_BASE)
        linhas += ['### Portão de passagem da fase', '',
                   '- [ ] Critérios de aceite dos módulos da fase marcados.',
                   '- [ ] Testes de isolamento de tenant e de autorização passando em CI.',
                   '- [ ] Definition of Done do documento 11, seção 2, em cada módulo.',
                   '- [ ] DDL revisado pelo owner e migração testada em homologação.', '']
        for rel, titulo, portal, telas, fontes in mods:
            docs = ', '.join(fontes) if fontes else 'ver a ficha'
            linhas += [f'### {titulo}' + (f' — {portal}' if portal else ''), '',
                       f'Ficha: `kit-starter/{rel}` · SDD: documentos {docs}', '',
                       '- [ ] Ler a ficha e os documentos do SDD; confirmar com o owner as regras e as pendências do módulo.',
                       '- [ ] Migração das tabelas do módulo a partir do DDL do SDD, revisada pelo owner, com plano de volta.',
                       '- [ ] Repositório e serviço com filtro de tenant; regras de negócio e estados da ficha.',
                       '- [ ] Contrato OpenAPI e endpoints no padrão do documento 04, com validação no servidor (documento 15).',
                       '- [ ] Permissões `modulo.recurso.acao` e papéis do documento 78; default-deny; separação de funções.']
            if telas:
                linhas.append('- [ ] Telas com o design system (documento 08):')
                linhas += [f'    - [ ] {t}' for t in telas]
            linhas += ['- [ ] Auditoria das ações sensíveis (documento 29) e notificações, quando houver (documento 57).',
                       '- [ ] Textos por chave de internacionalização; acessibilidade WCAG 2.2 AA; 320 px sem rolagem horizontal.',
                       '- [ ] Testes: unitários, integração, isolamento de tenant, autorização e critérios de aceite do documento de origem.',
                       '']
    linhas += ['---', '', GATE]
    open(SAIDA, 'w', encoding='utf8').write('\n'.join(linhas))
    tarefas = sum(1 for l in linhas if re.match(r'^\s*- \[ \]', l))
    print('gerado:', os.path.relpath(SAIDA, ROOT), '|', total_mod, 'módulos |', total_telas, 'telas |', tarefas, 'tarefas |',
          len('\n'.join(linhas).encode()) // 1024, 'KB')


if __name__ == '__main__':
    main()
