# SDD Mestre — Plataforma SaaS Multi-Entity/Multi-Unit em PHP 8 MVC

## Visão do documento

Este documento define a Especificação de Design de Software (SDD) mestre para uma plataforma SaaS escalável, multi-entity, multi-unit e multi-user, construída em PHP 8 puro com arquitetura MVC, API RESTful, frontend progressivo com JavaScript `fetch`, design system com Tailwind 4.4 e estratégia de bibliotecas internas sem dependência de bibliotecas externas de runtime.[web:46][web:43][web:51]

O modelo de governança técnica deste projeto usa o `fable-method` como método principal de decisão, verificação e reporting; usa `oh-my-opencode-slim` como malha de agentes especialistas; usa `hallmark` para direção visual e prevenção de interfaces genéricas; usa `ag-kit` para workflows, memória e compressão de contexto; usa `agentic-awesome-skills` como catálogo complementar de skills; e integra `mantis` e skills dedicadas de segurança para auditoria contínua e validação das superfícies críticas do sistema.[attached_file:1][attached_file:2][attached_file:3][web:4][web:18]

## Política de pré-instalação e bootstrap de skills

Antes de qualquer uso operacional do SDD, o ambiente de agentes deve verificar se as skills, plugins e configurações mínimas estão presentes. Se não estiverem, o processo deve interromper a execução funcional e primeiro instalar, configurar e validar o stack de agentes necessário.[web:44][web:46][web:51][web:55]

### Regra obrigatória

Nenhum workflow do projeto pode assumir que `fable-method`, `oh-my-opencode-slim`, `ag-kit`, `hallmark`, `agentic-awesome-skills` ou integrações de segurança já estejam disponíveis. O processo deve sempre executar uma fase explícita de `agent environment bootstrap` antes da fase de planejamento, especificação ou implementação.[web:44][web:46][web:51]

### Ordem de bootstrap

1. Verificar OpenCode CLI.
2. Instalar e configurar `oh-my-opencode-slim`.
3. Instalar `ag-kit` no projeto ou por setup compartilhado.
4. Instalar `fable-method` no host compatível.
5. Registrar `hallmark`, `agentic-awesome-skills`, `mantis` e skills proprietárias de segurança.
6. Validar autenticação, modelos, skills e agentes.
7. Somente então iniciar o loop do `fable-method`.

### Checklist de verificação de ambiente

| Item | Verificação | Ação se ausente |
|---|---|---|
| OpenCode CLI | `opencode --version` responde | Instalar OpenCode CLI antes de prosseguir.[web:44][web:45] |
| oh-my-opencode-slim | Configuração presente e agentes respondem | Executar instalador e revalidar.[web:43][web:44][web:49] |
| AG Kit | `.agents/` ou setup equivalente presente | Rodar `npx @vudovn/ag-kit init`.[web:51][web:50] |
| fable-method | Plugin ou skills instalados | Instalar via plugin, script ou AGENTS.md.[web:46][web:47] |
| Model providers | `opencode auth login` concluído | Solicitar autenticação manual do usuário.[web:44][web:45] |
| Model registry | `opencode models --refresh` executado | Atualizar catálogo antes de uso.[web:43][web:44] |
| Agent health | `ping all agents` funciona | Corrigir config ou credenciais.[web:44][web:49][web:55] |
| Background subagents | flag experimental habilitada quando aplicável | Definir variável de ambiente apropriada.[web:43][web:55] |

## Instalação e configuração das skills obrigatórias

### 1. OpenCode CLI como pré-requisito

O `oh-my-opencode-slim` depende da presença do binário `opencode`, e a documentação de instalação recomenda verificar `opencode --version` antes de rodar o instalador.[web:44] Um guia de uso também destaca que mesmo quem usa OpenCode Desktop precisa do CLI instalado para que a instalação do plugin funcione corretamente.[web:45]

**Gate:** se `opencode --version` falhar, o processo deve parar e abrir uma tarefa de ambiente chamada `Install OpenCode CLI`.[web:44][web:45]

### 2. Instalação do oh-my-opencode-slim

A instalação recomendada do `oh-my-opencode-slim` usa `bunx oh-my-opencode-slim@latest install`, com opções não interativas como `--no-tui --skills=yes` quando o projeto exigir padronização automática de setup.[web:43][web:44] A configuração gerada fica em `~/.config/opencode/oh-my-opencode-slim.json`, onde os modelos dos agentes devem ser revisados e ajustados ao stack disponível.[web:43][web:44]

Comandos de referência:

```bash
opencode --version
bunx oh-my-opencode-slim@latest install --no-tui --skills=yes
opencode auth login
opencode models --refresh
opencode
# dentro da sessão
ping all agents
```

Se o projeto usar a orquestração de background da linha V2, a documentação técnica também cita a necessidade de habilitar `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS=1` ou variável equivalente persistida no shell profile.[web:43][web:55]

### 3. Instalação do AG Kit

O `ag-kit` pode ser inicializado no projeto com `npx @vudovn/ag-kit init`, o que injeta a pasta `.agents/` diretamente na base local do projeto.[web:51][web:50][web:54] Também existe opção de instalação global com `npm install -g @vudovn/ag-kit` seguida de `ag-kit init`, além de estratégia centralizada com symlink para reuso entre repositórios.[web:51]

Comandos de referência:

```bash
npx @vudovn/ag-kit init
# ou
npm install -g @vudovn/ag-kit
ag-kit init
```

**Gate:** se a pasta `.agents/` não existir após a execução, o ambiente deve ser considerado incompleto.[web:51][web:57]

### 4. Instalação do fable-method

O `fable-method` pode ser instalado como plugin recomendado em Claude Code com `/plugin marketplace add Sahir619/fable-method` seguido de `/plugin install fable@fable-method`, ou como skills standalone por `git clone` mais `install.sh` no Linux/macOS e `install.ps1` no PowerShell do Windows.[web:46][web:47]

Comandos de referência para setup standalone:

```bash
git clone https://github.com/Sahir619/fable-method && bash fable-method/install.sh
```

No Windows PowerShell:

```powershell
git clone https://github.com/Sahir619/fable-method; .\fable-method\install.ps1
```

Quando o host não suportar instalação nativa de skills, o repositório também informa que `AGENTS.md` pode ser usado como método equivalente para qualquer agente ou harness compatível.[web:46][web:47]

### 5. Registro do hallmark, agentic-awesome-skills e mantis

O `hallmark` entra como skill de direção visual e antítese de UI genérica.[web:18] O `agentic-awesome-skills` entra como catálogo amplo de skills reutilizáveis e deve ser conectado ao processo de seleção de capabilities por domínio.[web:4] O `mantis` e as skills proprietárias de segurança devem ser tratados como `security toolchain`, com localização, instalação e versionamento definidos pelo projeto em seu diretório de automação interna e validados no bootstrap antes do uso em auditorias.

Como nem todos esses componentes compartilham o mesmo método de instalação, o projeto deve manter um manifesto local chamado `docs/agent-stack/manifest.md` contendo:

- nome da skill ou plugin;
- origem;
- método de instalação;
- comando de atualização;
- versão/pino desejado;
- host compatível;
- critério de verificação pós-instalação.

## Script lógico de bootstrap recomendado

O projeto deve manter um workflow ou script de verificação com a seguinte lógica operacional:

```text
START
  -> check opencode cli
  -> if missing: stop and request installation
  -> check oh-my-opencode-slim config
  -> if missing: install plugin and configure
  -> check provider auth
  -> if missing: require interactive auth
  -> refresh models
  -> check .agents folder
  -> if missing: initialize ag-kit
  -> check fable-method availability
  -> if missing: install via plugin/script/AGENTS.md
  -> check hallmark / mantis / security skills registry
  -> if missing: install or register according to local manifest
  -> run health checks
  -> if all green: allow SDD workflows
END
```

## Política de configuração correta após instalação

Instalar não é suficiente; o ambiente precisa estar corretamente configurado antes de uso. O SDD passa a exigir as seguintes validações pós-instalação:

- `oh-my-opencode-slim` com preset escolhido e modelos compatíveis com orçamento e função de cada agente.[attached_file:2][web:43][web:52]
- autenticação de providers concluída por `opencode auth login`.[web:44][web:45]
- catálogo de modelos atualizado por `opencode models --refresh`.[web:43][web:44]
- agentes respondendo com `ping all agents`.[web:44][web:49][web:55]
- `ag-kit` presente no projeto e workflows reconhecidos.[web:51][web:54]
- `fable-method` acessível no host escolhido, seja por plugin, skills instaladas ou `AGENTS.md`.[web:46][web:47]
- skills de segurança registradas com owner técnico definido.


## Code intelligence layer

O projeto deve incluir uma camada explícita de inteligência estrutural de código para apoiar review, análise de impacto e navegação assistida pelos agents. O `code-review-graph` entra aqui como ferramenta essencial para produzir um grafo local do repositório, manter atualizações incrementais e expor contexto mínimo via MCP para que os agents leiam somente o que importa em cada tarefa.[web:62][web:60][web:70]

### Papel do code-review-graph

O `code-review-graph` deve ser tratado como dependência operacional do ecossistema de agents, não como utilitário opcional. Ele oferece visualização estrutural, blast-radius analysis, review context otimizado e ferramentas de busca/impacto que reduzem leitura inútil em codebases grandes.[web:62][web:66][web:70]

### Regras de uso

- Antes de revisar código, os agents devem consultar o grafo para obter contexto mínimo.
- Antes de alterações relevantes, os agents devem obter o impacto provável da mudança.
- Antes de refatorações, os agents devem identificar dependências, callers, testes afetados e hotspots arquiteturais.
- Após mudanças, o grafo deve ser atualizado incrementalmente.
- Em revisões de PR e debugging, o grafo deve ser a primeira fonte de orientação estrutural.

### Bootstrap obrigatório

Se o `code-review-graph` não estiver instalado, o pipeline de bootstrap deve instalá-lo e configurá-lo antes de habilitar qualquer workflow de review, refatoração ou análise estrutural.[web:58][web:62]

Comandos de referência:

```bash
pip install code-review-graph
code-review-graph install
code-review-graph build
code-review-graph status
```

Se o projeto usar suporte MCP, o SDD deve exigir a execução do instalador com a plataforma apropriada e a validação dos tools mínimos antes do uso pelos agents.[web:58][web:62]

### Fluxo operacional com agents

1. Orchestrator define a tarefa.
2. `code-review-graph` fornece contexto mínimo e impacto.
3. Librarian ou Explorer consultam o grafo para localizar arquivos relevantes.
4. Oracle decide a estratégia.
5. Fixer altera apenas o necessário.
6. Fable-method verifica por observação.
7. Mantis audita qualquer superfície sensível antes do merge.

## Objetivos do sistema

A plataforma deve servir como núcleo de um ecossistema educacional multi-tenant com capacidade de suportar múltiplas entidades, múltiplas unidades por entidade, múltiplos usuários por contexto e múltas camadas operacionais, incluindo Website, SaaS Admin e camada Developer.[attached_file:1][attached_file:2]

Os objetivos principais são:

- Permitir segregação forte de dados, configuração e branding por entidade.
- Permitir operação descentralizada por unidade, com controle contextual de usuários, permissões e fluxos.
- Expor API RESTful versionada para uso web, integrações e automações.
- Possibilitar frontends progressivos usando `fetch()` sobre contratos bem definidos.
- Garantir segurança, rastreabilidade, auditoria e escalabilidade horizontal desde a base da arquitetura.
- Padronizar internacionalização com inglês como idioma canônico e suporte a `en`, `pt-BR`, `es`, `fr`, `de`, `it`, `zh`, `ja`, `ru` e `ar`.[attached_file:2][attached_file:3]

## Escopo funcional

### Camadas do produto

#### 1. Website

Camada pública institucional e comercial, responsável por presença web, marketing, SEO, páginas públicas, onboarding, autenticação inicial, recuperação de acesso, central de ajuda e documentação pública do produto.

#### 2. SaaS Admin

Camada autenticada de operação do produto para superadministradores, administradores de entidade, gestores de unidade e usuários internos com funções específicas de negócio.

#### 3. Developer

Camada técnica voltada à administração avançada da plataforma, feature flags, API keys, webhooks, observabilidade, diagnósticos, jobs, integrações, trilhas de auditoria, inspeção de eventos e governança operacional do stack.

### Requisitos macro de domínio

O sistema deve suportar:

- Multi-entity.
- Multi-unit.
- Multi-user.
- RBAC e políticas contextuais.
- Múltiplos idiomas e contextos regionais.
- Módulos independentes e composáveis.
- API-first com web progressivo.
- Auditoria de segurança e de negócio.
- Escalabilidade por decomposição modular e isolamento de contexto.

## Princípios arquiteturais

### Fundamentos

A arquitetura base deve seguir estes princípios:

- **PHP 8 puro**, sem framework full-stack externo.
- **MVC próprio**, com fronteira clara entre Controller, Service, Domain, Repository e View.
- **REST first**, com contratos JSON estáveis e versionados.
- **Frontend progressivo**, server-rendered como baseline e `fetch()` para experiências assíncronas.
- **Bibliotecas internas próprias**, com contratos bem definidos, testáveis e substituíveis.
- **Security by design**, com verificações explícitas em cada fase de entrega.
- **Scalability by partitioning**, ou seja, escalabilidade por particionamento de módulos, contexto, filas, storage e boundaries de tenancy.
- **Observability by default**, com logs estruturados, métricas, traces e trilhas de auditoria.

### Estilo arquitetural

O sistema adota arquitetura modular monolítica no início, com boundaries rígidos entre domínios e contratos internos preparados para futura extração seletiva de serviços. Esse desenho reduz complexidade operacional precoce e ao mesmo tempo preserva evolução para cenários de alta escala.[attached_file:1][attached_file:2][attached_file:3]

### Estratégia de escalabilidade

A escalabilidade do projeto deve ser pensada em cinco dimensões:

1. **Escalabilidade organizacional**: separação por domínio, equipe, módulo e ownership.
2. **Escalabilidade de dados**: chaves de segregação por entity e unit, particionamento lógico e preparação para sharding futuro.
3. **Escalabilidade de tráfego**: cache, filas, workers, leitura otimizada e desacoplamento de jobs intensivos.
4. **Escalabilidade de produto**: camadas Website, Admin e Developer desacopladas no nível de UX, ACL e endpoints.
5. **Escalabilidade de mudança**: bibliotecas internas, contratos versionados, testes e governança por verificação.

## Governança por agentes e skills

### Papel do fable-method

O `fable-method` deve atuar como skill governante do ciclo completo de criação do sistema, porque seu fluxo prescreve classificar o pedido, definir o que significa pronto, reunir evidências, decidir uma única recomendação, alterar o menor conjunto correto de artefatos, verificar por observação e reportar com honestidade.[attached_file:1][web:46]

No contexto deste projeto, ele será o gerente lógico do programa e deve controlar:

- Sequenciamento de fases do SDD.
- Critérios de aceite por documento e por módulo.
- Checklist de verificação antes de cada avanço.
- Reação a falhas, inconsistências e retrabalho.
- Encerramento de etapa somente após evidência observável.

### Papel do oh-my-opencode-slim

O `oh-my-opencode-slim` deve ser usado como camada operacional de orquestração, delegando subtarefas a agentes como Orchestrator, Oracle, Librarian, Explorer, Designer, Fixer e, quando necessário, Council.[attached_file:2][web:43]

Distribuição recomendada:

| Agente | Responsabilidade |
|---|---|
| Orchestrator | Coordenar subtarefas, dependências, checkpoints e síntese final.[attached_file:2] |
| Oracle | Decisões arquiteturais, trade-offs, revisões críticas e debugging estratégico.[attached_file:2] |
| Librarian | Pesquisa externa, documentação, padrões, compliance, APIs e normas.[attached_file:2] |
| Explorer | Reconhecimento de codebase, inventário de módulos, dependências e superfícies.[attached_file:2] |
| Designer | UI/UX, design system, heurísticas visuais, layout e consistência.[attached_file:2] |
| Fixer | Implementações delimitadas, correções, testes e ajustes de baixo acoplamento.[attached_file:2] |
| Council | Revisões multiperspectiva para decisões caras e irreversíveis.[attached_file:2] |

### Papel do hallmark

O `hallmark` deve orientar a camada visual do sistema, especialmente para impedir UI genérica, repetitiva ou com estética típica de “AI slop”, reforçando intencionalidade visual e design mais autoral.[web:18]

### Papel do ag-kit

O `ag-kit` deve apoiar o programa com workflows como `/plan`, `/coordinate`, `/create`, `/verify` e `/test`, além de mecanismos de memória persistente e compressão de contexto para sessões longas de construção documental e implementação.[attached_file:3][web:51]

### Papel do agentic-awesome-skills

O `agentic-awesome-skills` deve ser usado como catálogo complementar para selecionar skills especializadas de API, testes, documentação, auditoria, design, engenharia de dados, DevOps e workflows auxiliares necessários ao projeto.[web:4]

### Papel do mantis e das skills de segurança

O `mantis`, junto com `totustuus-security-auditor` e `totustuus-security-auditor-v2`, deve compor a malha de segurança para secure review, threat modeling, surface analysis, hardening, auditoria de conformidade técnica e validação contínua de segurança ao longo do SDD e da implementação.[attached_file:1][attached_file:2]

## Como o fable-method gerencia o loop de erro

### Modelo de loop

O loop do `fable-method` não trata erro como exceção casual; ele trata erro como sinal de verificação falha, evidência incompleta, conflito de autoridade ou alteração acima do necessário. O método explicitamente define classificação inicial, verificação nomeada, coleta de evidência, decisão única, edição cirúrgica, verificação observável e relatório com caveats.[attached_file:1][web:46]

### Fluxo do loop de erro neste projeto

1. **Classificar a falha**
   - erro de escopo;
   - erro de entendimento do requisito;
   - erro de implementação;
   - erro de teste;
   - erro de evidência insuficiente;
   - erro de autoridade conflitante, como documentação versus teste.

2. **Reafirmar o critério de done**
   - antes de corrigir, a skill deve reabrir o critério de aceite que falhou;
   - se o critério estiver mal definido, a etapa volta ao estado “plan-first”.

3. **Recolher evidência adicional limitada**
   - o método impõe busca limitada e evidência primária antes de mexer;
   - se não houver evidência suficiente, a entrega deve parar e escalar dúvida, em vez de “inventar” correção.[attached_file:1]

4. **Escolher uma única hipótese de correção**
   - evitar múltiplas correções especulativas em paralelo na mesma thread principal;
   - preferir a menor alteração correta possível.[attached_file:1]

5. **Executar correção cirúrgica**
   - alterar apenas os artefatos necessários;
   - preservar contratos estáveis e rastreabilidade.

6. **Verificar por observação**
   - rodar testes, checar comportamento, validar logs, revisar diffs, confirmar contexto de tenancy e autorização;
   - sem observação concreta, a correção não pode ser reportada como concluída.[attached_file:1]

7. **Aplicar limite de retries**
   - o método define limites rígidos para ciclos fracassados de verify; ao atingir o limite, ele interrompe a automação e devolve o problema com caveats claros.[attached_file:1]

## Integração do mantis para auditoria de segurança

### Objetivo

O `mantis` deve ser integrado ao SDD como mecanismo permanente de auditoria técnica, não como etapa isolada no final do projeto. Segurança deve existir como trilha paralela ao desenvolvimento do sistema.[attached_file:1][attached_file:2]

### Pontos de integração

O SDD deve prever o `mantis` em quatro momentos:

1. **Durante arquitetura**
   - análise de superfícies de ataque;
   - threat modeling por módulo;
   - identificação de trust boundaries;
   - revisão de decisões críticas de autenticação, autorização, dados e integrações.

2. **Durante especificação**
   - revisão de requisitos de segurança por endpoint;
   - classificação de dados sensíveis;
   - matriz de controles por módulo;
   - exigências de logging e auditoria.

3. **Durante implementação**
   - secure review de controllers, services, auth, file handling, webhooks e admin tools;
   - validação de headers, sessões, tokens, input handling, rate limiting e segregação tenant-aware.

4. **Durante verificação e release**
   - auditoria de checklists de segurança;
   - análise de achados críticos, altos, médios e baixos;
   - bloqueio de release para achados críticos não mitigados.

### Security gates no SDD

Propõe-se a seguinte política de gates:

| Gate | Momento | Aprovador técnico |
|---|---|---|
| SG-01 | Fechamento da arquitetura base | Oracle + Security Auditor |
| SG-02 | Fechamento do domínio Auth/ACL/Tenancy | Mantis + Security Auditor V2 |
| SG-03 | Antes da implementação de módulos sensíveis | Orchestrator + Mantis |
| SG-04 | Antes de homologação | Mantis + Fable Judge |
| SG-05 | Antes de release | Security Council |

## Exemplo de fluxo entre Orchestrator e Designer

### Cenário

Objetivo: criar a UI base do SaaS Admin para gestão de entidades, unidades e usuários, mantendo escalabilidade, consistência visual e baixa dívida de design.

### Fluxo recomendado

1. **Orchestrator recebe a meta**
   - “Definir foundation UI do SaaS Admin para listas, formulários, dashboards, navegação contextual e estados vazios”.[attached_file:2]

2. **Orchestrator classifica a tarefa**
   - tarefa de produto webapp;
   - precisa design system, não só telas isoladas;
   - depende de regras de ACL, i18n e densidade informacional.

3. **Orchestrator aciona Designer**
   - entrega briefing contendo: público, camadas do sistema, módulos prioritários, padrão de densidade, acessibilidade, dark mode, RTL e necessidade anti-template.

4. **Designer usa hallmark + skills de webapp**
   - define design tokens;
   - estrutura side navigation, header, command surfaces, cards, tabelas, formulários, estados vazios e feedback patterns;
   - evita layout genérico repetitivo, usando linguagem visual consistente e funcional.[web:18]

5. **Designer retorna artefatos**
   - design principles;
   - token map;
   - component anatomy;
   - layout rules;
   - accessibility constraints;
   - guidelines para responsive e RTL.

6. **Orchestrator valida contra requisitos sistêmicos**
   - confere impacto em i18n;
   - confere aderência a módulos futuros;
   - confirma que a UI serve Website, Admin e Developer sem conflitar padrões essenciais.

7. **Oracle revisa trade-offs de arquitetura de front**
   - define limites entre renderização server-side e componentes assíncronos via `fetch`.

8. **Fixer implementa foundations delimitadas**
   - layout shell;
   - componentes base;
   - utilitários JS;
   - helpers de internacionalização visual.

9. **Mantis/Security revisa superfícies**
   - formulários, headers, upload widgets, feedback sensível, masking e ações privilegiadas.

10. **Fable-method verifica por observação**
    - renderização desktop/mobile;
    - consistência de tokens;
    - contraste;
    - comportamento em erro;
    - aderência a critérios de done.[attached_file:1]

## Requisitos não funcionais focados em escalabilidade

### Desempenho

- Tempo de resposta alvo para endpoints de leitura comuns: até 300 ms em p95 sob carga normal.
- Tempo de resposta alvo para endpoints autenticados críticos: até 500 ms em p95.
- Jobs pesados devem sair do request síncrono sempre que possível.
- Todas as listas grandes devem ser paginadas e filtráveis.
- Toda consulta multi-tenant deve usar predicados de segregação explícitos.

### Escalabilidade horizontal

- Aplicação stateless sempre que possível no layer web.
- Sessões prontas para backend compartilhado.
- Filas desacopladas para tarefas assíncronas.
- Cache de leitura por contexto, entidade e idioma.
- Storage preparado para externalização futura.

### Confiabilidade

- Logs estruturados por correlação.
- Retry policies delimitadas.
- Dead-letter queues para falhas assíncronas.
- Idempotência para endpoints de integração sensíveis.
- Health checks por camada.

### Operabilidade

- Feature flags.
- Configuração por ambiente.
- Diagnostics mode restrito.
- Painéis de jobs, falhas, eventos e auditoria.
- Ferramentas de suporte a troubleshooting multi-tenant.

## Modelo de domínio

### Entidades principais

| Entidade | Descrição |
|---|---|
| Platform | Contexto global da solução SaaS. |
| Entity | Organização cliente com branding, regras e dados isolados. |
| Unit | Subdivisão operacional da entidade. |
| User | Identidade humana ou técnica autenticável. |
| Membership | Vínculo do usuário com entity/unit/contexto. |
| Role | Agrupamento de permissões. |
| Permission | Capacidade atômica autorizável. |
| Session | Sessão autenticada web. |
| ApiClient | Cliente técnico com credenciais e scopes. |
| AuditEvent | Registro imutável de ação relevante. |
| LocalePack | Recurso de idioma por domínio textual. |
| FeatureFlag | Controle de ativação progressiva. |
| WebhookEndpoint | Destino de eventos externos. |
| Job | Unidade assíncrona de processamento. |

## Critérios de aceite adicionais do stack de skills

O SDD mestre só pode ser considerado operacional quando o ambiente de skills também estiver operacional. Isso exige:

- manifesto de stack mantido e versionado;
- bootstrap automatizado ou semiautomatizado documentado;
- health check de agentes executado com sucesso;
- fallback documentado para hosts alternativos;
- instruções de reinstalação e reset disponíveis.[web:44][web:49][web:51]

## Artefatos derivados obrigatórios

Este SDD mestre deve originar, no mínimo:

- `docs/sdd/01-vision-scope.md`
- `docs/sdd/02-solution-architecture.md`
- `docs/sdd/03-domain-model.md`
- `docs/sdd/04-api-standards.md`
- `docs/sdd/05-security-architecture.md`
- `docs/sdd/06-i18n-l10n.md`
- `docs/sdd/07-design-system.md`
- `docs/sdd/08-observability-audit.md`
- `docs/sdd/09-test-strategy.md`
- `docs/sdd/10-delivery-governance.md`
- `docs/security/threat-model.md`
- `docs/security/control-matrix.md`
- `docs/security/findings-register.md`
- `docs/agent-stack/manifest.md`
- `docs/agent-stack/bootstrap.md`
- `docs/agent-stack/verification.md`

## Encerramento operacional

O projeto deve ser conduzido como uma arquitetura modular governada por evidência, com escalabilidade planejada desde o modelo de domínio, dos contratos REST, da segregação tenant-aware, da observabilidade, da segurança e do próprio bootstrap do stack de agentes. O valor do conjunto de skills escolhido está justamente em combinar método explícito, orquestração multiagente, design intencional, workflows reusáveis, instalação verificável e auditoria contínua em vez de tratar cada entrega como geração isolada de código.[attached_file:1][attached_file:2][attached_file:3][web:4][web:18][web:44][web:46][web:51]
