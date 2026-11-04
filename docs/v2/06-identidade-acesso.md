# 06 — Identidade, Autenticação e Autorização

> Parte do [SDD v2](00-README.md). Controles gerais em [05](05-seguranca.md).

---

## 1. Tipos de identidade

| Identidade | Credencial | Observação |
|---|---|---|
| Conta de pessoa (global) | E-mail verificado + senha + MFA conforme política | Uma conta por pessoa, no master. Pode ter vínculos com várias entidades e unidades (seção 12). |
| Vínculo (`UserMembership`) | Não é credencial | Liga a conta a uma entidade, unidade e papel. Fica no master. |
| Conta de plataforma | Senha + **passkey obrigatória** (ver seção 10) | Não é um usuário comum com flag. Papel `platform.*` separado. |
| Conta de serviço | Credencial de cliente (OAuth2 client credentials) ou chave de API | Dona de escopos mínimos; sem login interativo |
| Convidado | Token de convite de uso único | Expira em 72 h; aceite registra consentimento |
| Dispositivo confiável | Token de dispositivo (D-03) | Revogável por usuário e por administrador |

## 2. Autenticação de usuário

Fluxo:

1. Recebe e-mail e senha na tela de entrada única da plataforma. A conta é global (seção 12). Não há tenant escolhido antes do login.
2. Aplica atraso progressivo por identificador e limite por IP (ver seção 6). Não bloqueia a conta.
3. Verifica senha com Argon2id (pepper quando ativo, ver [05](05-seguranca.md), seção 2).
4. Se MFA é exigida pela política, pede segundo fator.
5. Cria sessão opaca no servidor. Regenera o ID de sessão.
6. Grava evento de login (sucesso ou falha) em auditoria, sem a senha.

Mensagem de falha é sempre a mesma para identificador inexistente e senha errada.

## 3. Senhas

| Regra | Requisito | Base |
|---|---|---|
| Tamanho mínimo | 15 caracteres se a senha for o único fator; 8 se houver MFA | NIST SP 800-63B-4 (confirmar versão vigente antes do go-live) |
| Tamanho máximo | Pelo menos 64 caracteres aceitos | NIST SP 800-63B |
| Composição | Sem exigência de símbolos ou maiúsculas | NIST SP 800-63B |
| Rotação periódica | **Não exigida.** Trocar só com suspeita de comprometimento. | NIST SP 800-63B. A v1 exigia "rotatividade" (ACH-07) |
| Verificação de vazamento | Verificar contra lista de senhas vazadas (lista local ou API por prefixo de hash, sem enviar a senha) | NIST SP 800-63B |
| Armazenamento | Argon2id + pepper (ver [05](05-seguranca.md)) | OWASP |
| Redefinição | Token de uso único, expira em 30 min, invalida sessões ativas | — |

## 4. Recuperação de conta

E-mail verificado é o único canal de cadastro e de recuperação (decisão D-04, 02/11/2026). Sem e-mail verificado, o cadastro não é concluído. WhatsApp e Telegram não são canais de recuperação nem de MFA.

Regras:

- Recuperação não revela se a conta existe.
- Ao concluir recuperação, todas as sessões e tokens anteriores são revogados.
- Recuperação de **conta de plataforma** exige passkey registrada e aprovação de dois responsáveis de segurança, registrada em auditoria (ver seção 10).
- Perda de MFA: recuperação por e-mail verificado, com espera de 24 h e notificação em todos os canais cadastrados. Durante a espera, a conta não aceita troca de MFA. Para contas de plataforma, vale a seção 10.
- Usuário sem e-mail verificado não tem conta ativa (D-04).

## 5. MFA

| Método | Uso |
|---|---|
| TOTP | Aceito para usuários de tenant |
| Passkey / WebAuthn | Aceito para todos; **obrigatório** para conta de plataforma |
| Certificado de cliente (PKI) | Aceito para integrações e cenários institucionais |
| Código por e-mail, SMS, WhatsApp ou Telegram | **Configurável pelo tenant (D-12, decidida pelo autor em 02/11/2026), com piso obrigatório.** Ver quadro abaixo. |

**Política de MFA configurável (D-12):**

| Ação | Métodos aceitos | Observação |
|---|---|---|
| Login comum de usuário de tenant | TOTP, passkey, certificado, e-mail, SMS, WhatsApp ou Telegram, conforme configuração do tenant | Pelo menos um método. Recomendado: TOTP ou passkey. |
| Aprovação de estorno, baixa manual ou pagamento acima do limite | TOTP, passkey ou certificado | Canais de mensagem não são aceitos. |
| Conta de plataforma | Passkey obrigatória | Sem alteração pelo tenant. |
| Alteração de método de MFA | Fator forte já cadastrado, ou espera de 24 h com notificação em todos os canais | Impede troca de método por quem só tem acesso ao canal. |
| Recuperação de conta | E-mail verificado (D-04) | Inalterado. |

Riscos aceitos pela configuração: troca de chip (SIM swap) e phishing em tempo real para SMS e WhatsApp; sequestro de conta de mensagem para Telegram e WhatsApp. Por isso esses canais não aprovam operação financeira. Cada tenant que habilitar esses canais assume o risco por escrito no cadastro de política.

Histórico: a versão anterior desta seção proibia SMS e e-mail como fator. A decisão D-12 do autor substitui essa proibição por configuração com piso. NIST SP 800-63B classifica SMS como método restrito; o piso desta seção mantém canais de mensagem fora de operações financeiras e de contas privilegiadas.

Step-up: exige MFA recente (até 5 min) para exportação de dados pessoais, alteração de papel, alteração de MFA, alteração de dados bancários e ações sobre o tenant.

## 6. Limites de tentativa

- Por identificador: atraso progressivo (1 s, 2 s, 4 s … até 60 s) após 5 falhas em 15 min.
- Por IP: limite de 20 tentativas por 15 min com resposta `429`.
- Por dispositivo: sinal de risco, sem bloqueio automático.
- CAPTCHA a partir da 10ª falha por IP. Provedor escolhido em ADR próprio.
- **Sem bloqueio total de conta por falha de senha.** Bloqueio por identificador permite negação de serviço contra qualquer conta conhecida (ACH-08). Conta de plataforma recebe o mesmo atraso progressivo, com alerta em tempo real ao canal de segurança. Não há bloqueio.

## 7. Sessão

| Controle | Valor |
|---|---|
| Idle | 30 min |
| Absoluta | 12 h (usuário); 4 h (conta de plataforma) |
| Sessões simultâneas | 3 por usuário; a mais antiga é encerrada |
| Vínculo | **Token de dispositivo (D-03, decidida):** cookie `__Host-` com ID aleatório de 256 bits, registrado em `DeviceTrust` e revogável pelo usuário e pelo administrador. A sessão só é aceita com token de dispositivo válido. Login em dispositivo novo exige MFA e notifica o usuário. Mudança de User-Agent ou de IP gera sinal de risco e step-up, sem bloqueio automático por IP (ACH-09). |
| Cookie | `__Host-` prefixo, `HttpOnly`, `Secure`, `SameSite=Lax` |
| Logout | Revoga a sessão atual; "sair de todos" revoga todas |
| Evento | Criação, rotação, término e revogação registrados em `UserSessionEvent` |

## 8. Tokens de API

- Access token JWT RS256, `exp` ≤ 15 min. Claims e regras na seção 12.
- Refresh token somente para clientes técnicos. Rotação a cada uso; reutilização de refresh revogado encerra a família de tokens. Endpoint de emissão e grant ainda não definidos: pendentes de ADR.
- Revogação por `jti` em lista com TTL igual ao `exp`.
- Navegador não recebe JWT (ADR-03, aceita por padrão no DP-10 do [80](80-decisoes-por-padrao.md)).

## 9. Autorização (RBAC com contexto)

- Permissão: `modulo.recurso.acao`, por exemplo `academico.nota.lancar`.
- Papéis são coleções de permissões. Permissões não são atribuídas diretamente ao usuário sem papel, exceto por exceção registrada com prazo.
- Escopo: tenant (obrigatório), unidade (quando aplicável), recurso (relação com o recurso, como turma do professor).
- Negação explícita tem precedência sobre concessão.
- Toda concessão e revogação de papel gera auditoria com justificativa obrigatória para papéis administrativos.
- Revisão de acesso: trimestral para papéis administrativos e de plataforma; anual para os demais.

## 10. Contas de plataforma (break-glass)

- Máximo de 5 contas de plataforma ativas.
- Passkey obrigatória. Conta sem passkey é desativada ao primeiro login após a migração.
- Uso de conta de plataforma gera alerta em tempo real para o canal de segurança.
- Conta de emergência (break-glass): credencial guardada offline em dois cofres físicos sob controle de duas pessoas; uso exige ticket e revisão em 24 h.
- Nenhum acesso de plataforma a dados de tenant sem registro de motivo e sem auditoria marcada.

## 11. Testes de identidade (critério de aceite)

- [ ] Conta autenticada sem vínculo com a unidade pedida não acessa dado dessa unidade, mesmo com token válido.
- [ ] Troca de contexto para unidade sem vínculo é recusada e registrada.
- [ ] Remoção de vínculo passa a valer na próxima requisição, sem esperar a expiração do token.
- [ ] Mensagem de erro idêntica para usuário inexistente e senha errada (diferença média de tempo menor que 20 ms em 200 amostras, mesmo ambiente).
- [ ] Sessão expira em idle e em absoluta.
- [ ] Regeneração de ID após login e após elevação.
- [ ] Token revogado é rejeitado.
- [ ] Refresh reutilizado encerra a família.
- [ ] Step-up exigido nas ações da seção 5.
- [ ] Conta de plataforma não entra sem passkey.

## 12. Conta global, vínculos e contexto de acesso

**Decisão do autor (02/11/2026):** uma pessoa pode estar em várias entidades e unidades, e o token de autenticação permite o acesso a elas. Esta seção define como isso funciona sem ampliar o que um token pode fazer.

**Status: D-19, D-20 e D-21 aprovadas pelo autor em 02/11/2026.**

### 12.1 Três camadas

| Camada | Onde fica | Conteúdo |
|---|---|---|
| Conta | Master (`totustuus.matriz.bd`) | E-mail verificado, senha (Argon2id), fatores de MFA, sessões, tokens revogados |
| Vínculos | Master | Quais entidades e unidades a conta pode acessar, com qual papel |
| Pessoa | Banco de identidade da entidade, com cadastro civil cifrado (D-19, [14](14-integracao-modulos.md), seção 3). O master guarda só `person_id` e e-mail verificado. O banco da unidade guarda só o `person_id`. | Nome, documento e contato civil (fora do master) |

Regra: o master guarda conta, vínculos e índice de pessoas. O cadastro civil fica no banco de identidade da entidade (D-19). Dados operacionais de unidade (notas, financeiro, matrícula) ficam no banco da unidade.

### 12.2 Login

1. Usuário informa e-mail e senha. Se a conta existir, o sistema verifica MFA conforme a política do vínculo de maior exigência.
2. Após autenticar, o sistema lista os vínculos ativos da conta.
3. Se houver um único vínculo ativo (uma entidade e uma unidade), o contexto é esse e a pessoa vai direto para a página principal do portal. Se houver mais de um, a pessoa escolhe a entidade e depois a unidade (ver [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 1).
4. Um token é emitido para o contexto escolhido.

Sem vínculo ativo, a conta autentica mas não recebe contexto. A resposta é a mesma de conta sem acesso, sem revelar outras entidades.

### 12.3 Conteúdo do token

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

### 12.4 Como o acesso é decidido em cada requisição

1. Valida assinatura, expiração, `aud` e `jti` não revogado.
2. Confere se `sid` está ativa.
3. Confere se o vínculo (`sub`, `ctx_entity`, `ctx_unit`) ainda existe e está ativo. A consulta usa cache de curta validade (até 30 s) e é invalidada na remoção do vínculo.
4. Se `mv` do token é anterior à versão atual dos vínculos, o papel é recalculado a partir do master, e não do token.
5. Seleciona o banco da unidade ([03](03-dominio-tenancy.md), seção 1.1).

Consequência: remover um vínculo tira o acesso na próxima requisição, mesmo com token ainda válido.

### 12.5 Troca de contexto

- Endpoint próprio: troca para outra unidade da mesma conta. Exige vínculo ativo na unidade pedida.
- Emite novo token com o novo contexto. O token anterior é revogado.
- Troca para unidade sem vínculo: recusada e registrada em auditoria ([18](18-regras-modulos-2.md), seção 4.2).
- Troca de entidade pode exigir MFA recente, conforme a política da entidade destino.

### 12.6 E-mail único

A conta é única por e-mail verificado em toda a plataforma. A mesma pessoa em duas entidades usa a mesma conta e a mesma senha. Duas pessoas diferentes não podem usar o mesmo e-mail verificado.

**Proposta (D-21):** conta global única. Alternativa: conta por entidade, com o mesmo e-mail em contas diferentes. Condição de falha da alternativa: a pessoa precisa de uma senha por entidade, e a recuperação de conta fica duplicada.

### 12.7 Substitui regras anteriores

- A regra "login restrito ao tenant do identificador" ([03](03-dominio-tenancy.md), seção 3, item 4) é substituída por esta seção. O risco que ela evitava, usar credencial de um tenant para entrar em outro, continua coberto: a conta só recebe contexto por vínculo.
- A seção 2 passo 1 não escolhe tenant antes do login.

### 12.8 Testes

- Conta com vínculo na entidade A e sem vínculo na entidade B: não recebe contexto de B, mesmo com token de A.
- Token com `ctx_unit` de unidade sem vínculo ativo: recusado.
- Remoção de vínculo: acesso cortado na próxima requisição.
- Troca de contexto registrada em auditoria.
- E-mail já verificado em outra conta: cadastro recusado.
