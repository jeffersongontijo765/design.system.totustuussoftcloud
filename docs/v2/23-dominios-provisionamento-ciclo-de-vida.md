# 23 — Domínios, Editor de portais, Autenticação, Provisionamento e Ciclo de Vida

> Parte do [SDD v2](00-README.md). Identidade em [06](06-identidade-acesso.md), seção 12. Bancos em [03](03-dominio-tenancy.md), seção 1.1. Operação em [10](10-implantacao-operacao.md). Operação contínua, backup e testes em [24](24-operacao-continuidade-qualidade.md).
> **Status:** D-22, D-23 e D-24 aprovadas pelo autor em 02/11/2026. Esta seção cobre pontos que estavam no projeto sem registro: a arquitetura de subdomínios (Editor de portais e autenticação), o provisionamento de entidade e unidade e a saída de um cliente. Decisões D-22 a D-24 (seção 6) foram aprovadas em 02/11/2026.

---

## 1. Mapa de domínios

**Decisão D-25 (02/11/2026): seis portais.** Módulos não são subdomínios. Cada portal reúne os módulos que o usuário tem permissão de usar.

| Domínio | Portal | Quem acessa |
|---|---|---|
| `totustuussoftcloud.com.br` | Site institucional e CRM da plataforma. Não é portal de uso. | Público; equipe comercial |
| `desenvolvedor.totustuussoftcloud.com.br` | Portal do Desenvolvedor, com o Editor de portais como área restrita (papel `platform.builder`) | Equipe da plataforma |
| `gestao.totustuussoftcloud.com.br` | Portal SaaS de gestão: acadêmico, simulados, projetos, contábil, financeiro, biblioteca, arquivos, protocolo, suprimentos, frotas, pessoas, atendimento e acesso. Cada módulo aparece conforme o vínculo. | Usuários administrativos da entidade |
| `portal-do-professor.totustuussoftcloud.com.br` | Portal do Professor | Docentes |
| `portal-do-aluno.totustuussoftcloud.com.br` | Portal do Aluno | Estudantes |
| `portal-dos-responsaveis.totustuussoftcloud.com.br` | Portal dos Pais e Responsáveis | Responsáveis legais |
| `portal-de-terceiros.totustuussoftcloud.com.br` | Portal de Terceiros | Parceiros com acesso restrito |
| `autenticacao.totustuussoftcloud.com.br` | Serviço de login. Infraestrutura, não é portal. | Todos |
| `arquivos.totustuussoftcloud.com.br` | Serviço de arquivos sem tela, com origem separada. Infraestrutura. | Sistema |

Todos os endereços têm um único nível antes de `totustuussoftcloud.com.br`, para que o certificado curinga cubra todos. Por isso os portais usam hífen (`portal-do-aluno`), e não pontos.

**Fluxo de entrada (D-26, aprovada em 02/11/2026):**

1. A pessoa informa e-mail e senha no portal escolhido. A conta é a mesma em todos os portais.
2. Se a conta tiver um único vínculo ativo, com uma entidade e uma unidade, o sistema vai direto para a página principal do portal.
3. Se houver mais de uma entidade, a pessoa escolhe a entidade. Depois, se houver mais de uma unidade nela, escolhe a unidade.
4. Se a conta não tiver vínculo com o portal acessado, a tela mostra que não há acesso a esse portal, sem listar outras entidades ou unidades.
5. Trocar de entidade ou unidade depois do login emite novo token com o contexto escolhido (D-20). O endereço do portal não muda.

O subdomínio por entidade do D-24 é **superado** por D-25. O endereço da entidade fica pendente em D-26 ([00](00-README.md)).

Regras gerais:

1. Cada domínio tem cookie próprio. Nenhum cookie de sessão é compartilhado com domínio pai (ver seção 2).
2. Todo redirecionamento após login usa lista de destinos permitidos por conta. Destino fora da lista é recusado. Isso evita redirecionamento aberto.
3. Certificado curinga para `*.totustuussoftcloud.com.br`, com renovação automática e alerta a 14 dias do vencimento ([10](10-implantacao-operacao.md), seção 7).
4. Domínio próprio da entidade exige verificação de posse (registro DNS) e certificado emitido para ele. Sem verificação, o domínio não é ativado.
5. O host da requisição é validado contra a lista de domínios ativos. Host desconhecido recebe `404` ([03](03-dominio-tenancy.md), seção 3).

## 2. Sessão entre domínios

**Proposta (D-22):** OpenID Connect com código de autorização e PKCE.

- O login acontece só em `autenticacao.`.
- O domínio de destino recebe um código de uso único, troca por tokens e cria a própria sessão.
- Um domínio comprometido não acessa a sessão de outro.
- Logout propaga para todos os domínios com sessão ativa.

Alternativa: cookie compartilhado em `.totustuussoftcloud.com.br`. É mais simples, mas qualquer subdomínio comprometido recebe o cookie de todos. Não recomendado.

## 3. Editor de portais: a superfície mais sensível

O Editor de portais (chamado de "builder" na v1; nome decidido em MOD-12) altera páginas e rotas que valem para todas as entidades. O código do papel continua `platform.builder`, para não mudar as permissões já escritas em [06](06-identidade-acesso.md). Um erro ou um acesso indevido afeta todos os clientes. Por isso, ele tem regras próprias.

**Proposta (D-23):** o Editor de portais altera apenas definições declarativas: páginas, rotas, layout, blocos aprovados e configuração. Não aceita PHP, JavaScript ou HTML livre.

| Controle | Regra |
|---|---|
| Acesso | Papel `platform.builder`, passkey obrigatória ([06](06-identidade-acesso.md), seção 10) e sessão de curta duração. |
| Implantação | Sistema separado do produto, em outro grupo de servidores. Falha do Editor de portais não afeta os clientes. |
| Publicação | Rascunho → revisão por segundo papel → publicação. Quem edita não aprova a própria mudança. |
| Versão | Toda publicação gera versão imutável. Rollback volta a uma versão anterior em um clique, com registro. |
| Escopo | Mudança pode ser publicada para todas as entidades, para um grupo ou para uma entidade. Padrão: uma entidade, depois o grupo. |
| Validação | Definição é validada por esquema antes de publicar. Bloco fora do catálogo é recusado. |
| Conteúdo | Texto exibido passa pelo escape do sistema ([08](08-frontend-design-system.md)). Nenhum script é aceito. |
| Auditoria | Cada edição, aprovação e publicação gera registro ([18](18-regras-modulos-2.md), seção 4.2). |
| Teste | Publicação passa por teste de fumaça das telas afetadas antes de ir para produção. |

**Motivo do limite:** código livre no Editor de portais transforma uma conta comprometida em execução de código em todos os clientes. A versão declarativa mantém o mesmo ganho de produtividade com um teto de dano bem menor.

## 4. Provisionamento de entidade e unidade

Criar uma entidade ou unidade é uma operação de várias etapas. Cada etapa é idempotente e pode ser retomada. A entidade só fica ativa ao final.

| Ordem | Etapa | Verificação |
|---|---|---|
| 1 | Registro da entidade e das unidades no master | Código e domínio únicos |
| 2 | Criação do banco da unidade (`tt_NNN`) e registro em `tenant_databases` | Banco criado com o nome registrado |
| 3 | Aplicação das migrações ao banco da unidade | `schema_version` igual à versão atual |
| 4 | Criação do banco de identidade da entidade, se ainda não existir (D-19) | Vazio e cifrado com a chave da entidade |
| 5 | Carga inicial de catálogos (locales, papéis padrão, categorias) | Conferência por contagem |
| 6 | Configuração de canais e integrações, por credencial própria do tenant ([16](16-integracoes-externas.md)) | Teste de conexão, sem ativação automática |
| 7 | Criação do primeiro administrador da entidade, por convite | Convite com validade de 72 h ([06](06-identidade-acesso.md)) |
| 8 | Ativação do domínio e da entidade | Teste de fumaça no domínio |

Regras:

- Falha em qualquer etapa deixa a entidade em `provisionando`, sem acesso de usuário. Retomada ou cancelamento são ações com registro.
- Cancelamento antes da ativação remove o banco criado e o registro de bancos. A remoção é verificada.
- Provisionamento não copia dado de outra entidade. Modelos padrão são sementes independentes.

## 5. Saída de cliente (desprovisionamento)

Um cliente que sai da plataforma precisa de um fluxo próprio, com prazos e registro. Ele é também um direito do titular.

| Etapa | Ação | Prazo de referência |
|---|---|---|
| 1. Pedido | Registro do pedido pelo administrador da entidade, com confirmação de identidade (MFA recente) | Imediato |
| 2. Suspensão | Entidade fica somente leitura. Novos vínculos e cobranças são bloqueados. | Imediato |
| 3. Exportação | Pacote com dados de titulares e de operação, em formato legível e portável ([07](07-privacidade-lgpd.md), seção 4). Entrega cifrada, com link de validade curta. | Até 15 dias |
| 4. Retenção legal | Dados que a lei exige guardar ficam em banco de retenção, com acesso restrito e prazo registrado. | Conforme a finalidade ([07](07-privacidade-lgpd.md), seção 5) |
| 5. Encerramento | Vínculos revogados. Domínio desativado. Sessões encerradas. | Após a exportação |
| 6. Expurgo | Banco da unidade e banco de identidade removidos. Arquivos expurgados. Backups expiram no prazo de retenção de backup. | Conforme política |
| 7. Registro final | Certificado de encerramento com o que foi exportado, retido e expurgado | Imediato após o expurgo |

Pendência: o prazo de guarda para retenção legal depende do jurídico (matriz de retenção, [26](26-sdd-juridico-regulatorio.md), seção 3).

## 6. Decisões propostas

| # | Decisão | Proposta | Alternativa e condição de falha |
|---|---|---|---|
| D-22 | Sessão entre domínios | OIDC com código e PKCE (seção 2) | Cookie compartilhado: mais simples, mas um subdomínio comprometido expõe os demais |
| D-23 | Escopo do Editor de portais | Só definições declarativas, com publicação revisada e rollback (seção 3) | Código livre: mais poder, mas uma conta comprometida afeta todas as entidades |
| D-24 | Endereço do tenant | Subdomínio por entidade, mais domínio próprio opcional com verificação (seção 1) | Seleção de entidade na tela de login: mais simples, mas a marca fica menos separada |

Estas decisões foram aprovadas pelo autor em 02/11/2026, com as propostas indicadas.

## 7. Critérios de aceite

- [ ] Cada domínio tem cookie próprio, sem compartilhamento com o domínio pai.
- [ ] Redirecionamento após login passa pela lista de destinos da conta.
- [ ] Editor de portais publica somente definições validadas, com revisão de segundo papel e rollback.
- [ ] Provisionamento retomável; cancelamento remove o que foi criado.
- [ ] Saída de cliente com exportação, retenção legal, expurgo e certificado.
- [ ] D-22 a D-24 decididas e registradas.
