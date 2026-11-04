"""Estrutura do SDD unificado: partes, documentos de cada parte e texto de abertura de cada parte.

Usado por inventario/gera_sdd_unificado.py. O texto de abertura é autoral e resume a parte;
o texto integral dos documentos da v2 e das especificações da v1 vem logo depois, sem corte.
Referências `#doc-NN` apontam para o documento NN dentro do próprio SDD unificado.
"""

# Fichas do kit-starter que absorveram especificações da v1: em qual parte o texto da v1 entra.
KIT_PARTE = [
    ('desenvolvedor/seguranca-e-operacao/acesso', 3), ('desenvolvedor/seguranca-e-operacao/mfa', 3),
    ('desenvolvedor/seguranca-e-operacao/ti', 17), ('desenvolvedor/seguranca-e-operacao/painel-de-bancos', 17),
    ('desenvolvedor/seguranca-e-operacao/integracoes-globais', 14),
    ('desenvolvedor/seguranca-e-operacao/configuracoes-do-sistema', 16),
    ('desenvolvedor/seguranca-e-operacao', 4),
    ('desenvolvedor/operacoes-internas', 12), ('desenvolvedor/pessoas-da-plataforma', 11),
    ('desenvolvedor/suporte', 13), ('desenvolvedor/', 6),
    ('gestao/academico', 8), ('gestao/simulados', 8), ('gestao/biblioteca', 8), ('gestao/planejamento', 8),
    ('gestao/secretaria', 9), ('gestao/gestao-de-documentos', 9),
    ('gestao/financeiro', 10), ('gestao/contabil', 10), ('gestao/empenho', 10),
    ('gestao/comercial', 6), ('gestao/pessoas', 11),
    ('gestao/suprimentos', 12), ('gestao/patrimonio', 12), ('gestao/contratos', 12),
    ('gestao/atendimento', 13), ('gestao/arquivos', 16), ('gestao/relatorios', 16), ('gestao/configuracao', 3),
    ('transversal/exclusao-logica', 16), ('transversal/arquitetura', 2), ('transversal/navegacao', 5),
    ('transversal/', 17),
    ('professor/', 5), ('aluno/', 5), ('responsaveis/', 5), ('terceiros/', 12),
]

PARTES = [
 dict(n=1, titulo='Visão e escopo', docs=['00', '01', '12', '13'], abertura="""
O TotusTuus SoftCloud é uma plataforma SaaS multi-tenant para escolas e instituições de ensino: mantenedoras, entidades e unidades. Ela tem seis portais e um site público, e uma API REST versionada ([01](#doc-01)).

```mermaid
flowchart LR
  site[Site público] --> auth[Login único]
  auth --> dev[Portal do Desenvolvedor<br/>equipe da plataforma]
  auth --> ges[Portal de Gestão<br/>equipe da entidade]
  auth --> pro[Portal do Professor]
  auth --> alu[Portal do Aluno]
  auth --> res[Portal dos Responsáveis]
  auth --> ter[Portal de Terceiros]
  api[API REST v1] --- ges
  api --- dev
```

**Regras principais**
- Escopo: web responsiva, sem aplicativo nativo. Gateways de pagamento existem como integração; a ativação em produção depende de contrato ([01](#doc-01), seção 5).
- Os módulos e a situação de cada um estão no catálogo ([12](#doc-12)). Os defeitos da v1 que não podem se repetir estão nos achados ([13](#doc-13)).
- Quando a v1 e a v2 divergem, vale a v2 ([00](#doc-00)).
"""),
 dict(n=2, titulo='Arquitetura e tenancy', docs=['02', '03', '04', '14', '30'], abertura="""
Monólito modular em PHP 8, com um banco master da plataforma, um banco de identidade por entidade e um banco por unidade ([02](#doc-02), ADR-08; [03](#doc-03)).

```mermaid
flowchart TB
  P[Plataforma] --> M[Mantenedora]
  M --> E[Entidade]
  E --> U1[Unidade A]
  E --> U2[Unidade B]
  subgraph Bancos
    BM[(Banco master<br/>catálogo, contas de plataforma, CRM da plataforma)]
    BI[(Banco de identidade<br/>da entidade: cadastro civil)]
    BU1[(Banco da unidade A<br/>notas, financeiro, matrícula, folha)]
    BU2[(Banco da unidade B)]
  end
  E -.-> BI
  U1 -.-> BU1
  U2 -.-> BU2
  P -.-> BM
```

```mermaid
sequenceDiagram
  participant N as Navegador
  participant F as Front controller
  participant MW as Middleware
  participant C as Controller
  participant S as Serviço
  participant R as Repositório
  N->>F: requisição
  F->>MW: SecurityHeaders, RequestId, RateLimit por IP, Csrf
  MW->>MW: Sessão e Auth, TenantContext, Authorize, Audit
  MW->>C: contexto (usuário, entidade, unidade, locale)
  C->>S: chama o serviço
  S->>R: consulta com filtro de tenant
  R-->>S: dados da unidade autorizada
  S-->>C: resultado
  C-->>N: resposta
```

**Regras principais**
- Controller não executa SQL; serviço recebe o contexto e não lê `$_SESSION`; repositório filtra por tenant em toda consulta ([02](#doc-02), seção 2).
- A ordem da cadeia de middleware é fixa e só muda por ADR ([02](#doc-02), seção 3).
- A API é versionada, com autenticação por token, schema de entrada e idempotência ([04](#doc-04)).
- Os módulos se integram por eventos, sem acesso direto ao banco do outro ([14](#doc-14)). O cache tem chave por tenant ([30](#doc-30)).
"""),
 dict(n=3, titulo='Identidade, acesso e permissões', docs=['06', '78', '35'], abertura="""
Cada pessoa tem uma conta global, ligada à entidade e à unidade por vínculos. O token leva só o contexto ativo, e o acesso é reavaliado a cada requisição ([06](#doc-06), seção 12).

```mermaid
sequenceDiagram
  participant P as Pessoa
  participant A as autenticacao.
  participant M as Master
  participant D as Portal
  P->>A: e-mail, senha e MFA
  A->>M: lista os vínculos ativos
  alt um vínculo
    A-->>P: contexto definido
  else vários vínculos
    P->>A: escolhe entidade e unidade
  end
  A->>D: código de uso único (OIDC + PKCE)
  D->>M: troca por token com ctx_entity, ctx_unit, role, mv
  Note over D,M: a cada requisição: assinatura, sessão ativa,<br/>vínculo ainda existe, papel recalculado se mv mudou
```

**Regras principais**
- Login só no domínio de autenticação; os portais recebem um código de uso único ([06](#doc-06); D-22).
- Permissões no formato `modulo.recurso.acao`, com default-deny. Os níveis vão de 0 (próprio) a 7 (desenvolvedor) ([78](#doc-78), seção 2.1).
- Separação de funções: quem cria não aprova o mesmo objeto financeiro, de compra ou de consentimento ([78](#doc-78), seção 2.2).
- Só `platform.developer` cria entidade e unidade (L-02, [78](#doc-78), seção 3).
- Acesso físico (portaria, catracas, biometria) é tratado no [35](#doc-35).
"""),
 dict(n=4, titulo='Segurança, privacidade e auditoria', docs=['05', '07', '29', '32'], abertura="""
Segurança e privacidade fazem parte do desenho desde o início: segredos no cofre, dados pessoais mínimos e uma trilha de auditoria imutável ([05](#doc-05), [07](#doc-07), [29](#doc-29)).

```mermaid
flowchart LR
  A[Ação no sistema] --> E[Evento de auditoria]
  E --> H["hash = SHA-256(evento + prev_hash)"]
  H --> B[(Banco da unidade<br/>só INSERT e SELECT)]
  B --> V[Verificação a cada hora]
  V -->|quebra| AL[Alerta de segurança]
  B --> D[Ancoragem diária<br/>hash assinado fora do servidor]
```

**Regras principais**
- Nenhum segredo em texto claro; chave-mestra do cofre fora do host da aplicação ([05](#doc-05); ADR-05).
- LGPD: base legal registrada, minimização, direitos do titular com prazo, incidentes comunicados à ANPD ([07](#doc-07)).
- Auditoria com cadeia de hash, leitura que também gera evento e exportação com MFA ([29](#doc-29)).
- Atendimento (helpdesk e SAC) e privacidade por portal, com o DPO de cada entidade ([32](#doc-32)).
"""),
 dict(n=5, titulo='Portais, navegação e interface', docs=['31', '08', '09', '75', '76'], abertura="""
A matriz de portais define o que cada portal tem, quem é dono de cada dado e onde cada módulo aparece ([31](#doc-31)). A interface segue o design system ([08](#doc-08)).

```mermaid
flowchart TB
  M[Matriz de portais e módulos] --> D[Desenvolvedor: plataforma, clientes, operação]
  M --> G[Gestão: acadêmico, secretaria, financeiro, pessoas, suprimentos]
  M --> P[Professor: classe, diário, simulados]
  M --> A[Aluno: classe, boletim, financeiro próprio]
  M --> R[Responsáveis: dependentes com vínculo ativo]
  M --> T[Terceiros: só o próprio contrato]
```

**Regras principais**
- Sem JavaScript inline nem atributos `on*=`; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](#doc-08)).
- Inglês canônico e dez locales, com teste de paridade de chaves ([09](#doc-09)).
- Busca, notificações e perfil respeitam o escopo de cada portal ([75](#doc-75), [76](#doc-76)).
- O portal de terceiros nunca mostra financeiro interno, contábil, folha ou dado de aluno ([31](#doc-31), seção 2.6).
"""),
 dict(n=6, titulo='Plataforma SaaS: clientes, domínios, licenças e CRM', docs=['23', '77', '22'], abertura="""
A plataforma cria entidades e unidades em etapas idempotentes, controla planos com limite de alunos e mantém um CRM próprio, separado do CRM de cada entidade ([23](#doc-23), [77](#doc-77), [22](#doc-22)).

```mermaid
flowchart LR
  r[1 - Registro no master] --> b[2 - Banco da unidade] --> mg[3 - Migrações] --> id[4 - Banco de identidade]
  id --> cat[5 - Catálogos iniciais] --> can[6 - Canais e integrações] --> adm[7 - Convite do administrador] --> at[8 - Ativação do domínio]
```

```mermaid
stateDiagram-v2
  [*] --> ativa
  ativa --> inadimplente: renovação não paga
  inadimplente --> ativa: pagamento
  inadimplente --> suspensa: fim da carência (15 dias)
  suspensa --> ativa: regularização
  ativa --> cancelada
  suspensa --> cancelada
  cancelada --> [*]
```

**Regras principais**
- Falha em qualquer etapa deixa a entidade em `provisionando`, sem acesso; a retomada é registrada ([23](#doc-23), seção 4).
- A saída do cliente tem sete etapas: pedido, suspensão, exportação, retenção legal, encerramento, expurgo e certificado ([23](#doc-23), seção 5).
- Cada plano tem limite de alunos; acima do limite, novas matrículas ativas são bloqueadas ([77](#doc-77)).
- São dois CRMs: o da plataforma (vender o SaaS) e o do tenant (captar alunos). Nenhum lead cruza de um para o outro ([22](#doc-22), seção 1).
"""),
 dict(n=7, titulo='Regras gerais dos módulos de gestão', docs=['17', '18', '19'], abertura="""
Estes documentos trazem as regras de base de financeiro, pessoas, acadêmico, segurança do trabalho, suprimentos, contratos, cobrança, notificações, auditoria e dos módulos que vieram da v1 ([17](#doc-17), [18](#doc-18), [19](#doc-19)). As partes seguintes detalham cada área.

```mermaid
stateDiagram-v2
  [*] --> open: título emitido
  open --> partial: baixa menor que o saldo
  open --> paid: baixas = líquido
  partial --> paid: baixas = líquido
  open --> cancelled: sem baixa
  partial --> cancelled: só por estorno
  paid --> [*]
  cancelled --> [*]
```

**Regras principais**
- "Atrasado" não é estado: é filtro calculado sobre `open` e `partial` com vencimento passado ([17](#doc-17), seção 2.3).
- Despesa acima de R$ 10.000 exige segundo aprovador; o solicitante não aprova a própria ([17](#doc-17), seção 2.4).
- Duplicidades da v1 resolvidas: suprimentos é dono do estoque; auditoria é dona da trilha; autenticação consolidada no [06](#doc-06); um único módulo de atendimento ([19](#doc-19), seção 2).
"""),
 dict(n=8, titulo='Acadêmico', docs=['55', '59', '58', '60', '61', '81', '62', '63', '64', '65', '66', '67', '68', '69', '40', '41', '42', '43', '44', '47', '37'], abertura="""
O acadêmico é especificado em ordem de dependência: estrutura, sistemas avaliativos, turmas e grade, diário, boletim e conselho, e os demais módulos ([55](#doc-55), seção 3).

```mermaid
flowchart LR
  est[1 - Estrutura acadêmica<br/>doc 59] --> ava[2 - Sistemas avaliativos<br/>doc 59 seção 4]
  est --> tur[3 - Turmas e grade<br/>doc 60]
  ava --> dia[4 - Diário<br/>doc 61]
  tur --> dia
  dia --> bol[5 - Boletim e conselho<br/>doc 62]
  oco[6 - Ocorrências<br/>doc 63]
  est --> pla[7 - Planos de aula e ensino<br/>doc 64]
  tur --> pla
  est --> tcc[8 - Estágio e TCC<br/>doc 65]
  dia --> pro[9 - Prontuário e portfólio<br/>doc 66]
  bol --> pro
  liv[10 - Livros e arquivo morto<br/>doc 67]
  bib[11 - Biblioteca<br/>doc 68]
  bol --> rel[12 - Relatórios e censo<br/>doc 69]
  cal[Calendário<br/>doc 58] --> tur
```

```mermaid
stateDiagram-v2
  [*] --> registrada
  registrada --> em_analise
  em_analise --> comunicada
  em_analise --> arquivada: fato não procede
  comunicada --> com_medida
  comunicada --> encerrada
  com_medida --> encerrada
```

**Regras principais**
- Os três níveis de ensino estão no escopo: básico, técnico e superior, com TCC e CPA/SINAES (ACA-01, ACA-02).
- Grade publicada só muda por nova versão; turma aponta para curso, grade e versão ([59](#doc-59), [60](#doc-60)).
- Nota só pelo professor da turma; diário fechado só reabre pela coordenação, com motivo ([61](#doc-61)).
- Ocorrência tem relato sigiloso e dado de terceiro protegido ([63](#doc-63)).
- A Classe (mural, materiais e tarefas) tem nota de tarefa no diário só quando a tarefa é avaliação ([81](#doc-81)).
- Aulas online, formulários, preceptoria, pastoral, agendamento, simulados e planejamento estão nos documentos [40](#doc-40) a [44](#doc-44), [47](#doc-47) e [37](#doc-37).
"""),
 dict(n=9, titulo='Secretaria, matrícula e documentos', docs=['46', '48', '54'], abertura="""
A secretaria conduz a matrícula do pedido à efetivação, emite documentos a partir de modelos aprovados e gere os documentos em três contextos: recebidos, administrativos e emitidos ([46](#doc-46), [48](#doc-48), [54](#doc-54)).

```mermaid
stateDiagram-v2
  [*] --> solicitada
  [*] --> lista_espera: sem vaga
  lista_espera --> solicitada: vaga liberada
  solicitada --> em_analise
  em_analise --> ativa
  em_analise --> condicional: pendência com prazo
  em_analise --> cancelada
  condicional --> ativa: regularizada
  condicional --> cancelada: prazo vencido (job)
  ativa --> trancada
  ativa --> transferida
  ativa --> concluida
  ativa --> cancelada
  ativa --> nao_rematriculada: fim da janela + 30 dias
```

```mermaid
stateDiagram-v2
  [*] --> solicitado
  solicitado --> em_emissao
  em_emissao --> emitido
  emitido --> aguardando_assinatura
  aguardando_assinatura --> assinado
  aguardando_assinatura --> expirado
  emitido --> cancelado: só com motivo
```

**Regras principais**
- Vaga reservada na transação de confirmação; empate na última vaga gera uma matrícula e uma lista de espera ([46](#doc-46), M-03).
- Sem contrato e termo de LGPD assinados, a matrícula não passa de `em_analise` ([46](#doc-46), M-08).
- Documento emitido não é editado; correção gera documento novo e o anterior é cancelado ([48](#doc-48), seção 4).
"""),
 dict(n=10, titulo='Financeiro, pagamentos e fiscal', docs=['20', '34', '71'], abertura="""
Todo movimento financeiro passa por um ledger, com valores em centavos inteiros, e cada pagamento tem um ciclo de vida com transições validadas ([20](#doc-20)).

```mermaid
stateDiagram-v2
  [*] --> criada
  criada --> autorizacao_pendente
  autorizacao_pendente --> autorizada
  autorizacao_pendente --> recusada
  autorizada --> capturada
  autorizada --> cancelada
  criada --> expirada: Pix ou boleto vencido
  capturada --> estornada_parcial
  capturada --> estornada_total
  estornada_parcial --> estornada_total
  capturada --> em_contestacao
  autorizacao_pendente --> pendente_conciliacao: sem confirmação no prazo
```

**Regras principais**
- `capturada` nunca volta para `autorizada`; só estorno ou chargeback ([20](#doc-20), seção 6.2).
- O sistema fica fora do escopo PCI: cartão só pelo provedor ([20](#doc-20), seção 3).
- Gateway e contingência por unidade; split quando adotado; NFS-e da entidade e da plataforma ([34](#doc-34)).
- Contas a pagar, cheques, caixa físico, fluxo de caixa, DRE e conciliação ([71](#doc-71)).
- Valores legais e tributários são parâmetros obrigatórios; sem eles, a apuração fica bloqueada ([80](#doc-80)).
"""),
 dict(n=11, titulo='Pessoas, departamento pessoal e SST', docs=['39', '52'], abertura="""
O HCM tem três submódulos: departamento pessoal, recursos humanos e medicina e segurança do trabalho. O da plataforma e o da entidade são instâncias separadas ([39](#doc-39), HCM-01 e HCM-10).

```mermaid
stateDiagram-v2
  state Colaborador {
    [*] --> ativo
    ativo --> afastado
    afastado --> ativo
    ativo --> desligado
  }
  state Folha {
    [*] --> em_processamento
    em_processamento --> fechada: aprovada por outra pessoa
    fechada --> paga
  }
```

**Regras principais**
- Folha fechada não é alterada; correção é folha complementar ([17](#doc-17), seção 3.3).
- Quem processa a folha não a aprova ([39](#doc-39), seção 7).
- ASO, CID e prontuário só pelo médico do trabalho; RH e gestão veem apto ou inapto ([39](#doc-39), [52](#doc-52)).
"""),
 dict(n=12, titulo='Suprimentos, patrimônio, frotas, contratos e terceiros', docs=['33', '53', '38'], abertura="""
Compras seguem requisição, cotação, pedido e recebimento, com separação de funções. Contratos têm ciclo de vida com alçadas, e os prestadores usam o portal de terceiros ([17](#doc-17), seção 6; [33](#doc-33); [38](#doc-38)).

```mermaid
flowchart LR
  rq[Requisição] -->|aprovada por outra pessoa| ct[Cotação] --> pd[Pedido] -->|recebido por outra pessoa| rc[Recebimento] --> es[Estoque]
```

```mermaid
stateDiagram-v2
  [*] --> negociacao
  negociacao --> aprovacao
  aprovacao --> assinado
  assinado --> vigente
  vigente --> em_renovacao
  em_renovacao --> vigente: aditivo
  vigente --> encerrado
  negociacao --> cancelado
  aprovacao --> cancelado
```

**Regras principais**
- Quem pede não aprova a própria requisição e não recebe a própria compra ([22](#doc-22), seção 5).
- Contrato assinado não é editado: mudança vira aditivo; quem cria a minuta não a aprova ([33](#doc-33), seção 3).
- Patrimônio com depreciação por categoria aprovada pelo contador; categoria sem regra não deprecia (DP-02, [80](#doc-80)).
- Pacote de documentos e contratos para o jurídico ([53](#doc-53)).
"""),
 dict(n=13, titulo='Atendimento e notificações', docs=['57'], abertura="""
Atendimento usa um modelo único de ticket para SAC, helpdesk, chat e chamados ([32](#doc-32), seção 2). Notificações têm estados, preferências e horário de silêncio ([57](#doc-57)).

```mermaid
stateDiagram-v2
  [*] --> novo
  novo --> aberto
  novo --> em_triagem
  aberto --> em_triagem
  aberto --> em_atendimento
  em_triagem --> em_atendimento
  em_triagem --> escalonado
  em_atendimento --> aguardando: cliente, terceiro ou aprovação
  aguardando --> em_atendimento
  em_atendimento --> resolvido
  escalonado --> em_atendimento
  resolvido --> fechado
  resolvido --> reaberto
  fechado --> reaberto: dentro da janela
  reaberto --> em_atendimento
  novo --> cancelado
```

**Regras principais**
- Estado de espera pausa o contador de SLA ([32](#doc-32), seção 2.3).
- Aviso obrigatório (verificação, recuperação de conta, MFA, saúde e segurança) não pode ser desligado ([57](#doc-57), seção 3.3).
- Horário de silêncio de 21h às 7h, exceto aviso obrigatório ([57](#doc-57)).
- `read` só é gravado quando o destinatário abre o aviso ([57](#doc-57), seção 3.2).
"""),
 dict(n=14, titulo='Integrações e importação', docs=['16', '74', '70'], abertura="""
Integrações existem em dois níveis, plataforma e tenant, com credenciais no cofre e um ciclo de vida próprio ([16](#doc-16)). Integrações educacionais oficiais estão no [74](#doc-74) e a importação de dados de sistema anterior, no [70](#doc-70).

```mermaid
stateDiagram-v2
  [*] --> rascunho
  rascunho --> testando
  testando --> ativa: teste ok e confirmação
  testando --> rascunho: falha
  ativa --> suspensa
  suspensa --> ativa
  suspensa --> revogada
  ativa --> expirada: credencial vencida
```

**Regras principais**
- Credencial gravada no cofre antes de qualquer teste; teste só com operação de leitura ([16](#doc-16), seção 5.1).
- Ativar conexão de produção exige permissão própria e step-up; conexão de plataforma exige dupla aprovação ([16](#doc-16), seção 5.2).
- SMS não é fator de MFA ([16](#doc-16), seção 2).
"""),
 dict(n=15, titulo='Inteligência artificial', docs=['27', '28'], abertura="""
A IA sugere e a pessoa decide. Nenhuma decisão sobre direito, nota, matrícula, crédito, emprego ou saúde é tomada só pela IA ([27](#doc-27), princípio 2).

```mermaid
flowchart LR
  p[Pedido de uso de IA] --> c{Recurso contratado?}
  c -->|não| x[Recurso não aparece; API recusa]
  c -->|sim| m[Dado mínimo, identificadores redigidos]
  m --> g[Modelo]
  g --> s[Sugestão identificada como IA]
  s --> h[Revisão humana registrada]
  h --> a[(Auditoria: finalidade, dados, resposta, modelo, versão, quem pediu)]
```

**Regras principais**
- Dado de cliente não treina modelo de terceiros sem consentimento e contrato ([27](#doc-27), princípio 4).
- Cobertura de IA módulo a módulo, com os módulos que ficam sem IA por decisão ([28](#doc-28)).
"""),
 dict(n=16, titulo='Dados, validações, configurações e armazenamento', docs=['51', '15', '56', '72', '21'], abertura="""
Os modelos de dados (DDL) dos módulos novos estão no [51](#doc-51); validações comuns no [15](#doc-15); configurações e relatórios no [56](#doc-56); campos personalizados no [72](#doc-72); arquivos e busca no [21](#doc-21).

```mermaid
flowchart LR
  in[Entrada] --> v[Validação no servidor<br/>doc 15] --> s[Serviço] --> r[(Banco da unidade)]
  s --> f[(Armazenamento de objetos<br/>doc 21)]
  r --> idx[Índice de busca<br/>com isolamento por tenant]
  r --> del[Exclusão lógica<br/>deleted_at e deleted_by]
```

**Regras principais**
- Exclusão é lógica por padrão; bloqueada se houver dependente ativo; auditoria nunca é expurgada ([03](#doc-03), seção 6; [15](#doc-15); [19](#doc-19), seção 14).
- Arquivos com versão, hash, antivírus, retenção e bloqueio legal ([21](#doc-21), seção 3).
- Busca por CPF exige motivo e gera auditoria ([21](#doc-21), seção 6.8).
"""),
 dict(n=17, titulo='Operação, qualidade, testes e TI', docs=['10', '11', '24', '49', '36'], abertura="""
Toda entrega passa por um pipeline fixo, com bloqueio em segredo exposto, dependência vulnerável e teste de isolamento de tenant ([10](#doc-10), seção 4).

```mermaid
flowchart LR
  s1[1 - Segredos] --> s2[2 - Lint e análise estática] --> s3[3 - Dependências] --> s4[4 - Testes<br/>inclui isolamento e autorização]
  s4 --> s5[5 - Build com SBOM] --> s6[6 - Verificação do artefato] --> s7[7 - Migrações com plano de volta]
  s7 --> s8[8 - Homologação e produção] --> s9[9 - Testes de fumaça]
```

**Regras principais**
- Sem `npx`, `bunx` ou instalador remoto no pipeline; ferramentas com versão fixada ([10](#doc-10), seção 4).
- Definition of Done, gates e ADRs ([11](#doc-11)). Continuidade, SLO, releases e testes ([24](#doc-24)).
- Logs sem dado pessoal e testes por portal ([49](#doc-49)). TI da plataforma e da entidade são assuntos diferentes ([36](#doc-36)).
"""),
 dict(n=18, titulo='Jurídico e regulatório', docs=['25', '26', '50', '73'], abertura="""
As obrigações legais e as perguntas para o jurídico estão agrupadas por tema. Nenhuma regra jurídica é inventada: o que depende de parecer fica marcado como pendência ([25](#doc-25), [26](#doc-26), [50](#doc-50), [73](#doc-73)).

```mermaid
flowchart LR
  q[Pergunta jurídica no texto] --> pk[Pacote para o jurídico<br/>docs 50, 53, 73]
  pk --> pa[Parecer escrito<br/>com data e responsável]
  pa --> d[Regra registrada no 45 ou no 80]
  d --> t[Texto do módulo atualizado]
```

**Regras principais**
- Matriz de retenção, relação de consumo, cobrança, negativação e bloqueio de serviço ([26](#doc-26)).
- Inadimplente mantém acesso à rematrícula, à documentação e à comunicação com a família ([26](#doc-26), seção 3).
"""),
 dict(n=19, titulo='Pendências, decisões e rastreabilidade', docs=['45', '80', '79'], abertura="""
Toda pendência do SDD tem um responsável: autor, jurídico, conferência de norma, homologação ou owner do módulo ([45](#doc-45)). As decisões tomadas por padrão estão no [80](#doc-80), e a situação de cada arquivo da v1 está no [79](#doc-79).

```mermaid
flowchart LR
  p[Pendência no texto] --> q{Quem decide?}
  q -->|produto| a[Autor]
  q -->|lei| j[Jurídico]
  q -->|norma| n[Conferência de norma]
  q -->|medida ou produto| h[Homologação]
  q -->|revisão de DDL| o[Owner do módulo]
  q -->|padrão seguro| dp[Decisão por padrão no 80]
```

**Situação em aberto** ([45](#doc-45), seção 1): 59 itens jurídicos sem decisão, 14 jurídicos já decididos pelo autor, 25 de conferência de norma, 2 documentos a escrever (DDL de RH e contábil e de marketing), 12 de homologação e 42 de revisão do owner. Nenhum item de decisão de produto está em aberto. As lacunas LAC-01 a LAC-25 têm a situação de cada uma nos documentos 17, 18, 19 e 22.
"""),
]

GLOSSARIO = """
| Termo | Significado |
|---|---|
| Plataforma | A empresa que opera o SaaS. Tenant reservado, com contas de plataforma ([03](#doc-03), seção 1) |
| Mantenedora | Cliente que contrata o SaaS; agrupa entidades |
| Entidade | Instituição (razão social). Tem um banco de identidade com o cadastro civil |
| Unidade | Campus, filial ou polo da entidade. Tem um banco próprio com os dados operacionais |
| Tenant | Nível de isolamento de dados: entidade e unidade. Toda consulta filtra pelo tenant do contexto |
| Banco master | Banco da plataforma: catálogo de entidades e unidades, contas de plataforma, CRM da plataforma, índice de pessoas |
| Conta global | Conta única da pessoa, por e-mail verificado, válida em todas as entidades ([06](#doc-06), seção 12) |
| Vínculo | Ligação da conta com uma entidade e uma unidade, com um papel (aluno, responsável, professor, colaborador, terceiro) |
| Contexto | Entidade e unidade ativas na sessão; o token leva só o contexto ativo |
| Papel | Conjunto de permissões com nível de 0 a 7 ([78](#doc-78)) |
| Permissão | Ação autorizada no formato `modulo.recurso.acao`; sem permissão explícita, a ação é negada (default-deny) |
| Step-up | Nova autenticação recente exigida antes de uma ação sensível |
| Break-glass | Credencial de emergência guardada offline em dois cofres ([06](#doc-06), seção 10) |
| Separação de funções | Quem cria um objeto financeiro, de compra ou de consentimento não o aprova ([78](#doc-78), seção 2.2) |
| Portal | Superfície do produto para um público: desenvolvedor, gestão, professor, aluno, responsáveis, terceiros |
| Área e módulo | Área agrupa módulos dentro de um portal ([31](#doc-31), seção 2) |
| Protocolo | Número de acompanhamento de requerimento ou solicitação, consultável por número e CPF |
| Matrícula condicional | Matrícula aceita com pendência e prazo; vencido o prazo, é cancelada por job ([46](#doc-46), M-04) |
| Diário | Registro de aula, chamada, conteúdo e notas da turma ([61](#doc-61)) |
| Sistema avaliativo | Escala, média, recuperação e regra de aprovação de uma turma ([59](#doc-59), seção 4) |
| Ledger | Registro financeiro em partidas dobradas de todo movimento ([20](#doc-20), seção 5) |
| Split | Divisão do pagamento entre recebedores no gateway ([34](#doc-34), seção 3) |
| NFS-e | Nota fiscal de serviço eletrônica ([34](#doc-34), seção 5) |
| DPO (encarregado) | Pessoa indicada para responder pela proteção de dados; a plataforma e cada entidade têm o seu |
| ROPA | Registro das operações de tratamento de dados pessoais |
| ANPD | Autoridade Nacional de Proteção de Dados |
| SLA | Prazo de atendimento com contagem pausada nos estados de espera ([32](#doc-32), seção 2.3) |
| DDL | Definição das tabelas do banco ([51](#doc-51)) |
| ADR | Registro de decisão de arquitetura ([02](#doc-02), seção 6) |
| SBOM e SLSA | Lista de componentes do build e procedência verificável do artefato ([05](#doc-05), [10](#doc-10)) |
| D-xx, L-xx, DP-xx | Decisão do autor, regra de licenciamento ou permissão aprovada, e decisão tomada por padrão ([80](#doc-80)) |
| [Declarado] e [Planejado] | Afirmação da v1 ainda não reproduzida; item ainda não implementado, com dono e critério de aceite ([00](#doc-00)) |
| [A], [V] e [P] | Norma consolidada; norma a verificar; ponto que depende de parecer ([26](#doc-26)) |
"""

PARTES.append(dict(n=20, titulo='Plano de implementação', docs=[], abertura="""
O sistema é construído em oito fases. Cada fase só começa quando as fases de que ela depende passaram pelo critério de passagem. As fases seguem a ordem de dependência do acadêmico ([55](#doc-55), seção 3) e o pipeline de entrega ([10](#doc-10), seção 4).

```mermaid
flowchart LR
  F0[F0 Fundação] --> F1[F1 Plataforma SaaS]
  F0 --> F2[F2 Acadêmico núcleo]
  F1 --> F2
  F2 --> F3[F3 Secretaria e documentos]
  F2 --> F4[F4 Financeiro e fiscal]
  F3 --> F5[F5 Portais do professor, aluno e responsáveis]
  F4 --> F5
  F0 --> F6[F6 Pessoas, suprimentos, patrimônio, contratos, terceiros, atendimento]
  F5 --> F7[F7 Complementos acadêmicos, relatórios, importação e IA]
  F6 --> F7
```

| Fase | O que entra | Documentos |
|---|---|---|
| F0 Fundação | Tenancy e bancos, identidade e login único, permissões e papéis, auditoria, exclusão lógica, privacidade base, internacionalização, design system, pipeline e observabilidade | [03](#doc-03), [06](#doc-06), [78](#doc-78), [29](#doc-29), [15](#doc-15), [07](#doc-07), [09](#doc-09), [08](#doc-08), [10](#doc-10) |
| F1 Plataforma SaaS | Provisionamento, domínios e OIDC, licenciamento e limites, Editor de portais, CRM da plataforma, cobrança do SaaS, suporte | [23](#doc-23), [77](#doc-77), [22](#doc-22), [34](#doc-34), [32](#doc-32) |
| F2 Acadêmico núcleo | Estrutura acadêmica, calendário, turmas e grade, matrícula e rematrícula, diário, boletim e conselho | [59](#doc-59), [58](#doc-58), [60](#doc-60), [46](#doc-46), [61](#doc-61), [62](#doc-62) |
| F3 Secretaria e documentos | Protocolo, gerador de documentos, gestão de documentos, livros e arquivo morto | [31](#doc-31), seção 3.2; [48](#doc-48), [54](#doc-54), [67](#doc-67) |
| F4 Financeiro e fiscal | Títulos, cobrança, régua, gateways e split, financeiro completo, contábil e fiscal da entidade | [17](#doc-17), [18](#doc-18), [20](#doc-20), [34](#doc-34), [71](#doc-71) |
| F5 Portais pessoais | Professor (classe, diário, planos), aluno, responsáveis, notificações | [81](#doc-81), [64](#doc-64), [57](#doc-57), [76](#doc-76) |
| F6 Gestão de apoio | Pessoas e SST, suprimentos, patrimônio e frotas, contratos, terceiros, biblioteca, simulados, atendimento | [39](#doc-39), [52](#doc-52), [19](#doc-19), [33](#doc-33), [38](#doc-38), [68](#doc-68), [47](#doc-47) |
| F7 Complementos | Aulas online, formulários, preceptoria, pastoral, agendamento, ocorrências, estágio e TCC, prontuário, relatórios e censo, importação, campos personalizados, integrações oficiais, IA, planejamento e empenho | [40](#doc-40) a [44](#doc-44), [63](#doc-63), [65](#doc-65), [66](#doc-66), [69](#doc-69), [70](#doc-70), [72](#doc-72), [74](#doc-74), [27](#doc-27), [28](#doc-28), [37](#doc-37) |

**Critério de passagem de cada fase**
1. Critérios de aceite dos documentos da fase atendidos e marcados.
2. Testes de isolamento de tenant e de autorização passando em CI ([03](#doc-03), seção 7; [06](#doc-06), seção 11).
3. Definition of Done do [11](#doc-11), seção 2, em cada módulo.
4. DDL revisado pelo owner e migração testada em homologação ([45](#doc-45), seção 7).

**Antes de produção, por módulo**
- As pendências jurídicas e de norma do módulo ([45](#doc-45), seções 3 e 4) estão respondidas. Um prazo marcado **[V]** ou **[P]** não entra em produção sem confirmação ([26](#doc-26), seção 3).
- Os itens de homologação do módulo ([45](#doc-45), seção 6) foram medidos.
"""))
