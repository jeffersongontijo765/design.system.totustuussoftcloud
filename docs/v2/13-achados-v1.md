# 13 — Achados da v1

> Parte do [SDD v2](00-README.md). Registro dos problemas encontrados ao analisar a v1 (pasta `sdd.totustuussoftcloud/`, 37 mil linhas em cerca de 60 arquivos) e o código de referência em `totustuussoftcloud/`.

Severidade: **Alta** = risco de segurança ou de dado pessoal; **Média** = contradição que leva a implementação errada; **Baixa** = manutenção.

Evidência: **[Verificado]** = conferido com grep ou leitura neste ciclo. **[Declarado]** = afirmação da v1 não reproduzida.

| ID | Sev. | Achado | Evidência | Tratamento na v2 |
|---|---|---|---|---|
| ACH-01 | Alta | A v1 afirma "zero JavaScript inline" e CSP com nonce, mas há atributos `on*=` em 311 arquivos de `resources/` e `app/` (padrão `on(click\|submit\|change)=`). A CSP com nonce não funciona com eles. | **[Verificado]** por grep: `grep -rlE ' on(click\|submit\|change)=\"' resources app` retornou 311 arquivos. Contagem pelo padrão amplo `\bon\w+\s*=` ainda pendente. | ADR-07; critério de aceite em [08](08-frontend-design-system.md) |
| ACH-02 | Média | "Sem bibliotecas externas de runtime" contra Font Awesome por CDN e Tailwind "4.4". | **[Verificado]** em `teste.html` (CDN) | D-01 |
| ACH-03 | Alta | A v1 lista e-mails reais de administradores de plataforma e identificadores internos com UUID. O código também tem o e-mail de um administrador em `scripts/verify-portal-authorization.php` e `scratch/create_http_session.php`. | **[Verificado]** | Removido da v2; ver [03](03-dominio-tenancy.md) seção 2 |
| ACH-04 | Média | Mais de 30 referências a caminhos inexistentes na pasta do SDD (`docs/security/…`, `docs/portais/…`, `.agents/skills/…`). Os caminhos são do repositório de código, não desta pasta. | **[Verificado]** pela ausência na pasta | Referências internas da v2 só apontam para arquivos desta pasta |
| ACH-05 | Alta | `JWT_SECRET` existe no `.env` da aplicação, enquanto a v1 diz "HS256 bloqueado". Pode ser resíduo ou caminho ativo. | **[Verificado]** existência; uso **não verificado** | Confirmar uso e remover (ver [05](05-seguranca.md)) |
| ACH-06 | Alta | Pasta `scratch/` na raiz do código com 162 arquivos, incluindo script que cria sessão PHP real para a conta de desenvolvedor e imprime o ID de sessão. | **[Verificado]** | Fora do artefato e do repositório ou bloqueado por ambiente; [05](05-seguranca.md) seção 3 |
| ACH-07 | Média | Política de senha exige "rotatividade" periódica. | **[Declarado]** na v1 (doc 07) | Removido; [06](06-identidade-acesso.md) seção 3 |
| ACH-08 | Média | Bloqueio por identificador (5 falhas/hora) permite negação de serviço contra qualquer conta conhecida. | **[Declarado]** na v1 (doc 04 e 07) | Atraso progressivo; [06](06-identidade-acesso.md) seção 6 |
| ACH-09 | Média | Vínculo de sessão a IP "estrito" quebra usuários com IP trocado (rede móvel, CGNAT). | **[Declarado]** | Sinal de risco; D-03 |
| ACH-10 | Baixa | `SameSite=Strict` em cookie de sessão impede a sessão em navegação vinda de link externo (e-mail, portal de terceiros). | Análise de design | `SameSite=Lax`; [06](06-identidade-acesso.md) seção 7 |
| ACH-11 | Alta | Prazo de comunicação de incidente de "72 h" para ANPD. O texto vigente da Resolução CD/ANPD nº 15/2024 fala em três dias úteis. | Análise documental | Corrigido em [07](07-privacidade-lgpd.md) seção 8; confirmar com jurídico |
| ACH-12 | Alta | Cofre de arquivo (`FileVault`) como provedor de produção. Classes de KMS e HashiCorp existem, mas a produção depende de ativação. | **[Verificado]** existência das classes; **[Declarado]** uso em produção | ADR-05 (D-02: biblioteca própria); go-live bloqueado até a chave-mestra sair do host |
| ACH-13 | Alta | Pipeline e instruções com `npx @vudovn/ag-kit init`, `bunx oh-my-opencode-slim@latest install` e `git clone` de ferramenta de terceiros. Executa código de rede sem versão fixada. | **[Declarado]** na v1 (sdd-mestre) | Removido do fluxo de produção; [05](05-seguranca.md) seção 4 |
| ACH-14 | Média | [`sub_sidebar_itsm.php`](anexo-v1/sub_sidebar_itsm.php) e `teste.html` ficam na pasta de especificações. | **[Verificado]** | Movidos ou removidos; [12](12-catalogo-modulos.md) seção 3 |
| ACH-15 | Baixa | Marcadores de citação de ferramenta (`[web:46]`, `[attached_file:1]`) em 7 arquivos. | **[Verificado]** | Removidos |
| ACH-16 | Média | Documentos duplicados ou com escopo sobreposto: `06-i18n-l10n` e `06-tenancy` com mesmo número; `bancos` ×2; `notificacoes` ×2; `biblioteca` ×2 (academica/completo); `autenticacao` vs `07-identity-auth`; `privacy_global` vs `08-privacy-lgpd`; mais de 40 módulos sem índice. | **[Verificado]** por nome | [12](12-catalogo-modulos.md) |
| ACH-17 | Baixa | Datas inconsistentes: documentos dizem "04/08/2026" e o arquivo mais recente é de outubro. Métricas (controllers, rotas, testes) sem fonte. | **[Verificado]** pela leitura | Métricas geradas por CI ([01](01-visao-escopo.md) seção 7) |
| ACH-18 | Média | Política de "zero inline JS" e exceção por "bibliotecas internas" aparecem em documentos diferentes sem reconciliação. | **[Verificado]** pela leitura | Uma regra só em [08](08-frontend-design-system.md) |
| ACH-19 | Média | Arquivos de dados de execução (`uploads/`, `workspace/`, `storage/`, `node_modules/`, `vendor/`) estão na raiz do código. Sem garantia de exclusão do artefato. | **[Verificado]** presença; exclusão **não verificada** | Verificação no pipeline; [10](10-implantacao-operacao.md) seção 4 |
| ACH-21 | Alta | Tabela de fila de eventos da v1 (`sys_event_queue`) usa `entityid` e não tem `tenant_id`, violando o isolamento de [03](03-dominio-tenancy.md). | **[Verificado]** [`spec_complementar_integracoes_governanca.md`](anexo-v1/spec_complementar_integracoes_governanca.md), seção 8.1 | Modelo corrigido em [14](14-integracao-modulos.md), seção 9 |
| ACH-22 | Média | Eventos da v1 sem módulo no nome (`employee.created`), com colisão possível entre módulos. | **[Verificado]** seção 4.1 da mesma spec | Nome `modulo.entidade.fato` em [14](14-integracao-modulos.md), seção 4 |
| ACH-23 | Alta | A v1 não separa integrações de plataforma e de tenant; não há regra de credencial por tenant. | **[Verificado]** por leitura; a spec de integrações cita "master" uma vez | Definido em [16](16-integracoes-externas.md) |
| ACH-24 | Alta | Não havia validação por transação, CRUD ou integração na v2; só regras genéricas. | Análise de cobertura da v2 | Padrão em [15](15-validacoes.md); regras por módulo pendentes |
| ACH-25 | Alta | Nenhuma tabela de Financeiro e Acadêmico tem `tenant_id`; Pessoas e SMT usam `entityid`; Suprimentos isola por `entity_uuid`. | **[Verificado]** contagem de `tenant_id` nos DDL e nas queries | Correção T-01 em [17](17-regras-modulos.md), seção 1 |
| ACH-26 | Média | Financeiro armazena `overdue` como estado, que depende de data. | **[Verificado]** [`spec_gestao_financeiro_completo.md`](anexo-v1/spec_gestao_financeiro_completo.md), DDL de `financial_receivables` | Correção T-04 em [17](17-regras-modulos.md), seção 2.3 |
| ACH-27 | Média | Acadêmico diz "CPF único por tenant", mas o DDL não tem tenant. | **[Verificado]** | Correção T-05 em [17](17-regras-modulos.md) |
| ACH-28 | Média | Pessoas define contrato de experiência com texto contraditório: "máximo 90 dias (prorrogável 1× até 90 dias)". | **[Verificado]** [`spec_gestao_pessoas_completo.md`](anexo-v1/spec_gestao_pessoas_completo.md), linha 238 | Pendente jurídico, L-03 em [17](17-regras-modulos.md) |
| ACH-29 | Alta | Suprimentos e Contratos não têm DDL na v1. | **[Verificado]** zero `CREATE TABLE` | T-02 em [17](17-regras-modulos.md) |
| ACH-30 | Alta | Régua de cobrança prevê bloqueio do portal aos 90 dias de atraso, sem ressalva para menor de idade e documento obrigatório. | **[Verificado]** [`spec_gestao_billing_cobranca_mensalidades.md`](anexo-v1/spec_gestao_billing_cobranca_mensalidades.md), seção 11 | Bloqueio parcial e parecer jurídico em [18](18-regras-modulos-2.md), seção 2.6 |
| ACH-31 | Alta | Régua prevê negativação aos 30 dias e mensagens por SMS e WhatsApp sem base legal documentada. | **[Verificado]** mesma seção | Parecer em [18](18-regras-modulos-2.md), seção 2.6 (L-07) |
| ACH-32 | Média | Cobrança armazena `overdue` e `viewed` como estado. | **[Verificado]** DDL `billing_invoices` | T-04, [18](18-regras-modulos-2.md), seção 2.3 |
| ACH-33 | Média | RH e Pessoas descrevem o mesmo colaborador sem fronteira definida. | **[Verificado]** pelos índices das duas specs | T-07, [18](18-regras-modulos-2.md), seção 4.1 |
| ACH-34 | Média | Auditoria não define imutabilidade nem cadeia de integridade; prevê expurgo e edição de registro. | **[Verificado]** [`spec_gestao_auditoria_completo.md`](anexo-v1/spec_gestao_auditoria_completo.md), seção 4 | [18](18-regras-modulos-2.md), seção 4.2 |
| ACH-35 | Média | Quatro módulos da v1 descrevem o mesmo domínio: estoque em Armazenamento e Suprimentos; atendimento em três specs; Logger e Auditoria; Autenticação e 06. | **[Verificado]** pelo conteúdo | Seção 2 de [19](19-regras-modulos-3.md) |
| ACH-36 | Média | Módulos com DDL sem `tenant_id`: CRM, Patrimônio, Frotas, Biblioteca e Armazenamento. | **[Verificado]** contagem nos DDL | T-01, [19](19-regras-modulos-3.md), seção 1 |
| ACH-37 | Baixa | Privacidade global lista jurisdições fora do Brasil sem cliente que as justifique. | **[Verificado]** | L-15, [19](19-regras-modulos-3.md), seção 4 |
| ACH-38 | Alta | A v1 não define o escopo PCI nem proíbe armazenar PAN ou CVV. Não há ledger de partidas dobradas, e cobrança usa `DECIMAL` sem regra de centavos. | **[Verificado]** ausência nas specs de cobrança e financeiro | [20](20-pagamentos-seguranca.md), seções 3, 4 e 5 |
| ACH-39 | Alta | Webhook de pagamento sem regra de assinatura, deduplicação e consulta de confirmação na v1. | **[Verificado]** ausência em `04` e nas specs de cobrança | [20](20-pagamentos-seguranca.md), seção 7 |
| ACH-40 | Alta | Modelo de armazenamento da v1 sem `tenant_id`, com `visibility = public` permitido e UUID gerado por `UUID()` (versão 1). | **[Verificado]** [`spec_object_storage_digital_assets.md`](anexo-v1/spec_object_storage_digital_assets.md), seção 13 | Correções S-01 a S-10 em [21](21-busca-e-armazenamento.md), seção 4.1 |
| ACH-41 | Média | Busca full-text citada em módulos (Biblioteca) sem motor, escopo de permissão nem regra para dado sensível. | **[Verificado]** por busca de termo nas specs | [21](21-busca-e-armazenamento.md), seção 6 |
| ACH-20 | Média | `.rar` de backup de projeto e pastas de cópia estão na pasta de trabalho do repositório Git do usuário. | **[Verificado]** pelo `git status` | Mover para armazenamento de backup fora do repositório |

## Resumo

- **Alta:** ACH-01, 03, 05, 06, 11, 12, 13 — 7 itens.
- **Média:** ACH-02, 04, 07, 08, 09, 14, 16, 18, 19, 20 — 10 itens.
- **Baixa:** ACH-10, 15, 17 — 3 itens.

Nenhum item de severidade alta foi confirmado como explorado. A análise é de desenho e de configuração estática, não de teste dinâmico. Antes de tratar a v1 como "baixo risco", é preciso executar os testes de isolamento e uma varredura DAST.
