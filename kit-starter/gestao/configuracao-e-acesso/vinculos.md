# Vínculos

- Portal: Gestão (`gestao.`)
- Área: Configuração e acesso
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [06](../../../docs/v2/06-identidade-acesso.md), seção 12
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Gerir os vínculos da conta global com a entidade (aluno, responsável, professor, colaborador, terceiro) e o contexto de acesso.

## 3. Telas

- **Vínculos** (DataTable por tipo e estado).
- **Vínculo de responsabilidade** (responsável × dependente, com verificação).
- **Encerrar vínculo** (com motivo; acesso removido no próximo token).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `unit.secretary`: vínculos de aluno e responsável.
- `unit.hr`: colaboradores.
- `entity.admin`: todos.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Conta global, vínculos e contexto ([06](../../../docs/v2/06-identidade-acesso.md), seção 12).

## 7. Dados

- Tabelas e campos conforme a seção 13 e o DDL do [51](../../../docs/v2/51-ddl-modulos-novos.md), quando o módulo estiver lá. Toda tabela tem `entidade_id`, `unidade_id`, `created_at`, `updated_at`, `created_by` e exclusão lógica com `deleted_at` e `deleted_by` ([03](../../../docs/v2/03-dominio-tenancy.md), seção 6; [15](../../../docs/v2/15-validacoes.md); [19](../../../docs/v2/19-regras-modulos-3.md), seção 14).

## 8. Integrações

- Ver a seção de integrações do documento de origem, na seção 13.

## 9. Exportação, auditoria e privacidade

- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Toda criação, alteração, aprovação, exclusão lógica, exportação e leitura de dado sensível gera evento de auditoria no banco da unidade ([29](../../../docs/v2/29-auditoria.md)).
- Dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md): mínimo necessário, mascaramento em listas, base legal registrada.

## 10. Estados de interface

- Carregando (skeleton), vazio com chamada para ação, sem resultado de filtro, erro com nova tentativa, acesso negado, registro bloqueado, fechado ou baixado (somente leitura), conflito de edição (versão).

## 11. Requisitos de frontend

- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`): página de lista com DataTable, KPIs, drawer de detalhe, formulário em página ou modal, kanban quando houver fluxo de estados.
- Seletor de unidade no topo quando o usuário tiver mais de uma; a troca reemite o token com o novo contexto ([06](../../../docs/v2/06-identidade-acesso.md), seção 12).

## 12. Critérios de aceite e pendências

- Critérios de aceite: os do documento de origem (seção 13) e os de [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 6.
- Testes de isolamento: usuário de outra unidade ou entidade recebe 404 em toda rota do módulo ([03](../../../docs/v2/03-dominio-tenancy.md)).
- As pendências do documento de origem estão na seção 13 e consolidadas no [45](../../../docs/v2/45-pendencias-consolidadas.md).

## 13. Regras da v2 (texto integral das fontes, sem corte)

### 13.1 [06](../../../docs/v2/06-identidade-acesso.md), seção 12

#### 12. Conta global, vínculos e contexto de acesso

**Decisão do autor (02/11/2026):** uma pessoa pode estar em várias entidades e unidades, e o token de autenticação permite o acesso a elas. Esta seção define como isso funciona sem ampliar o que um token pode fazer.

**Status: D-19, D-20 e D-21 aprovadas pelo autor em 02/11/2026.**

##### 12.1 Três camadas

| Camada | Onde fica | Conteúdo |
|---|---|---|
| Conta | Master (`totustuus.matriz.bd`) | E-mail verificado, senha (Argon2id), fatores de MFA, sessões, tokens revogados |
| Vínculos | Master | Quais entidades e unidades a conta pode acessar, com qual papel |
| Pessoa | Banco de identidade da entidade, com cadastro civil cifrado (D-19, [14](../../../docs/v2/14-integracao-modulos.md), seção 3). O master guarda só `person_id` e e-mail verificado. O banco da unidade guarda só o `person_id`. | Nome, documento e contato civil (fora do master) |

Regra: o master guarda conta, vínculos e índice de pessoas. O cadastro civil fica no banco de identidade da entidade (D-19). Dados operacionais de unidade (notas, financeiro, matrícula) ficam no banco da unidade.

##### 12.2 Login

1. Usuário informa e-mail e senha. Se a conta existir, o sistema verifica MFA conforme a política do vínculo de maior exigência.
2. Após autenticar, o sistema lista os vínculos ativos da conta.
3. Se houver um único vínculo ativo (uma entidade e uma unidade), o contexto é esse e a pessoa vai direto para a página principal do portal. Se houver mais de um, a pessoa escolhe a entidade e depois a unidade (ver [23](../../../docs/v2/23-dominios-provisionamento-ciclo-de-vida.md), seção 1).
4. Um token é emitido para o contexto escolhido.

Sem vínculo ativo, a conta autentica mas não recebe contexto. A resposta é a mesma de conta sem acesso, sem revelar outras entidades.

##### 12.3 Conteúdo do token

| Claim | Conteúdo |
|---|---|
| `sub` | UUID da conta |
| `sid` | Identificador da sessão |
| `ctx_entity` | UUID da entidade ativa |
| `ctx_unit` | UUID da unidade ativa |
| `role` | Papel naquela unidade |
| `mv` | Versão dos vínculos no momento da emissão |
| `exp` | Até 15 min |
| `aud`, `iss` | Validados |

**Proposta (D-20):** o token leva apenas o contexto ativo, nunca a lista de vínculos. Motivos: tamanho do token, exposição de outras entidades a quem recebe o token e risco de token antigo manter acesso depois de um vínculo ser removido.

##### 12.4 Como o acesso é decidido em cada requisição

1. Valida assinatura, expiração, `aud` e `jti` não revogado.
2. Confere se `sid` está ativa.
3. Confere se o vínculo (`sub`, `ctx_entity`, `ctx_unit`) ainda existe e está ativo. A consulta usa cache de curta validade (até 30 s) e é invalidada na remoção do vínculo.
4. Se `mv` do token é anterior à versão atual dos vínculos, o papel é recalculado a partir do master, e não do token.
5. Seleciona o banco da unidade ([03](../../../docs/v2/03-dominio-tenancy.md), seção 1.1).

Consequência: remover um vínculo tira o acesso na próxima requisição, mesmo com token ainda válido.

##### 12.5 Troca de contexto

- Endpoint próprio: troca para outra unidade da mesma conta. Exige vínculo ativo na unidade pedida.
- Emite novo token com o novo contexto. O token anterior é revogado.
- Troca para unidade sem vínculo: recusada e registrada em auditoria ([18](../../../docs/v2/18-regras-modulos-2.md), seção 4.2).
- Troca de entidade pode exigir MFA recente, conforme a política da entidade destino.

##### 12.6 E-mail único

A conta é única por e-mail verificado em toda a plataforma. A mesma pessoa em duas entidades usa a mesma conta e a mesma senha. Duas pessoas diferentes não podem usar o mesmo e-mail verificado.

**Proposta (D-21):** conta global única. Alternativa: conta por entidade, com o mesmo e-mail em contas diferentes. Condição de falha da alternativa: a pessoa precisa de uma senha por entidade, e a recuperação de conta fica duplicada.

##### 12.7 Substitui regras anteriores

- A regra "login restrito ao tenant do identificador" ([03](../../../docs/v2/03-dominio-tenancy.md), seção 3, item 4) é substituída por esta seção. O risco que ela evitava, usar credencial de um tenant para entrar em outro, continua coberto: a conta só recebe contexto por vínculo.
- A seção 2 passo 1 não escolhe tenant antes do login.

##### 12.8 Testes

- Conta com vínculo na entidade A e sem vínculo na entidade B: não recebe contexto de B, mesmo com token de A.
- Token com `ctx_unit` de unidade sem vínculo ativo: recusado.
- Remoção de vínculo: acesso cortado na próxima requisição.
- Troca de contexto registrada em auditoria.
- E-mail já verificado em outra conta: cadastro recusado.
