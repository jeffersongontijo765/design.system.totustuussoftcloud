# 05 — Segurança

> Parte do [SDD v2](00-README.md). Identidade e acesso em [06](06-identidade-acesso.md); privacidade em [07](07-privacidade-lgpd.md).

---

## 1. Postura

A v1 declara risco **baixo** e zero achados abertos de severidade média ou superior (**[Declarado]**, auditorias de 10 e 11/07/2026). Essa afirmação não é usada como base de decisão nesta versão. A v2 exige que cada controle tenha teste ou evidência reproduzível. Os achados verificados contra o código estão em [13-achados-v1.md](13-achados-v1.md).

## 2. Controles

| Área | Requisito | Verificação |
|---|---|---|
| Senhas | Argon2id. Parâmetros mínimos do OWASP Password Storage Cheat Sheet: m = 19 MiB, t = 2, p = 1. **Parâmetros do produto (decisão do autor, 02/11/2026): m = 64 MiB, t = 4, p = 3.** Devem ser aceitos se o p95 de login, medido em hardware de produção, ficar abaixo de 500 ms. | **[Verificado]** `app/Security/Argon2idProfile.php` usa m = 64 MiB, t = 4, p = 2 (constante `THREADS`). **Pendente:** alinhar o código a p = 3. Teste de benchmark em CI. |
| Pepper de senha | Chave HMAC fora do banco, no cofre de segredos (ADR-05). Rotação com verificação dupla. | **[Planejado]** |
| Tokens | RS256 fixo. Rejeitar `alg` diferente, `none` e HS256. | **[Verificado parcial]**: `config/jwt.php` usa RS256 por padrão e bloqueia HS256 em produção, mas `JWT_SECRET` ainda é lido por código de proteção de ativos. Separar em segredo próprio por finalidade e não reutilizar o nome de JWT. |
| Sessão | Idle 30 min, absoluta 12 h, regeneração do ID após login e troca de privilégio. | Teste de integração. |
| Cookies | `HttpOnly`, `Secure`, `SameSite=Lax`, prefixo `__Host-` (ver [06](06-identidade-acesso.md), seção 7). | Teste de cabeçalho. |
| CSRF | Token sincronizador por sessão + validação de `Origin` ou `Sec-Fetch-Site`. Dupla submissão é aceita só para API de cookie. | Teste automatizado. |
| CSP | `default-src 'self'`; `script-src 'self' 'nonce-…'`; sem `unsafe-inline`; sem `on*=` em HTML (ADR-07). Trusted Types em modo report-only antes de forçar. | **[Verificado parcial]**: ver ACH-01 em [13](13-achados-v1.md). |
| Cabeçalhos | HSTS com `max-age` ≥ 1 ano em produção; `X-Content-Type-Options: nosniff`; `X-Frame-Options: DENY` ou `frame-ancestors 'none'`; `Referrer-Policy: strict-origin-when-cross-origin`; `Permissions-Policy` restritiva. | Teste de cabeçalho em CI. |
| Autorização | Default-deny. Toda rota com permissão ou rota pública explícita. | Teste que percorre o roteador e falha em rota sem regra. |
| Tenant | Ver [03](03-dominio-tenancy.md), seção 3. | Matriz de isolamento. |
| Rate limit | Por IP, por identificador (com atraso progressivo, não bloqueio total) e por tenant. | Teste de carga leve em CI. |
| Upload | Limite de tamanho; validação por assinatura do arquivo (magic bytes) e por lista branca de tipos; renomeação com UUID; antivírus quando disponível; servido por controller com `Content-Disposition` e `X-Content-Type-Options: nosniff`. Nunca dentro de diretório público. | Teste com arquivo renomeado (`.php` com conteúdo de imagem). |
| Imagens protegidas | Marca d'água e URL assinada com expiração para conteúdo restrito. | **[Planejado]** |
| SQL | Somente prepared statements. Ordenação e nomes de coluna em lista branca. | Análise estática (regra de SQL com interpolação). |
| Saída | Escapamento contextual em HTML, atributo, JavaScript e URL. | Teste de XSS automatizado. |
| Erros | `display_errors=0` em produção; resposta genérica; detalhe só no log interno. | Teste de configuração. |
| Logs | Sem senha, token, cookie, CPF, e-mail completo ou corpo de requisição sensível. Mascaramento na escrita. | Teste com dados sintéticos. |
| Criptografia em repouso | AES-256-GCM para dados sensíveis, chave derivada com HKDF e envelope com versão. | **[Declarado]**; teste de decifragem com rotação. |
| Biblioteca de cofre própria (D-02) | Primitivas de `libsodium` ou OpenSSL, sem algoritmo novo. Envelope cifrado com chave de dados; chave-mestra fora do host da aplicação e nunca no mesmo arquivo do envelope. Revisão externa de criptografia antes de produção. | **[Planejado]** |
| Criptografia em trânsito | TLS 1.2 mínimo, preferencialmente 1.3. | Teste externo com ferramenta de TLS, em homologação. |

## 3. Contas e ferramentas de desenvolvimento

- **Proibido em qualquer diretório implantado:** scripts que criam sessão para contas reais, que imprimem identificadores de sessão ou que desativam autenticação. A v1 inclui 162 arquivos em `scratch/` na raiz do código, entre eles scripts que criam sessão para a conta de desenvolvedor (ACH-06). Esses arquivos são removidos do repositório. Regra de CI proíbe qualquer script que crie sessão ou imprima identificador de sessão. IP de origem não é controle válido, porque é forjável atrás de proxy.
- Diretórios `uploads/`, `workspace/`, `storage/`, `node_modules/` e `vendor/` com dados de execução não entram no artefato de deploy. A exclusão é verificada no pipeline (ver [10](10-implantacao-operacao.md)).

## 4. Cadeia de suprimentos

| Controle | Regra |
|---|---|
| Versões | Pacotes com versão exata no lockfile. Nada de `latest`. |
| Instaladores de terceiros | Proibido executar em produção. Em desenvolvimento, versão fixada e checksum conferido antes da execução. |
| Auditoria | `composer audit` e `npm audit` em CI. Falha em alto ou crítico sem exceção registrada com prazo. |
| Segredos no código | `gitleaks` no pre-commit e no CI. Achado bloqueia merge. |
| SBOM | CycloneDX gerado por build: **[Planejado]**. Assinatura e procedência (SLSA) também são **[Planejado]**. |
| Ferramentas de IA e agentes | Versão fixada, revisão do código-fonte antes da instalação e sem permissão de escrita fora do repositório. Ver [11](11-governanca-qualidade.md). |

## 5. Modelo de ameaças (resumo STRIDE)

| Categoria | Ameaça | Controle principal |
|---|---|---|
| Spoofing | Login com credencial vazada; sessão roubada | Argon2id, MFA, breach-check, sessão com vínculo de dispositivo (D-03) |
| Tampering | Alteração de parâmetro de tenant ou preço | Tenant do contexto; validação no serviço; assinatura em webhook |
| Repudiation | Negar ação administrativa | Auditoria com ator, ação, alvo, antes/depois, IP e requisição |
| Information disclosure | Enumeração de IDs; vazamento de tenant; erro com SQL | UUID, 404 uniforme, erro genérico, filtro de campo |
| Denial of service | Bloqueio de conta por tentativas; exportação pesada; payload grande | Atraso progressivo; fila para exportação; limite de payload |
| Elevation of privilege | Acesso de professor a dados de outra unidade; conta master sem MFA | Default-deny; permissão de unidade; MFA obrigatória para conta de plataforma |

Ameaças adicionais que a v2 inclui: **SSRF** em webhooks e integrações (bloqueio de redes privadas), **CSV injection** em exportações (regra em [08](08-frontend-design-system.md), seção 3) e **open redirect** em telas de login. Também: **injeção de prompt** em recursos com IA (dados de aluno enviados a provedor externo sem minimização; saída do provedor tratada como dado não confiável), **mass assignment** (campos de papel e de tenant não são aceitos do corpo da requisição) e **path traversal** em download (o caminho nunca vem do cliente; só o ID do arquivo).

## 6. Resposta a incidentes

| Severidade | Início do tratamento | Contenção | Comunicação interna |
|---|---|---|---|
| Crítica | 1 h | 4 h | Imediata ao responsável e à diretoria |
| Alta | 4 h | 24 h | Em até 8 h |
| Média | 1 dia útil | 7 dias | Relatório semanal |
| Baixa | 3 dias úteis | Próxima entrega | Registro no backlog |

- Runbook e modelo de comunicação à ANPD: ver [07](07-privacidade-lgpd.md), seção 8.
- Exercício de mesa semestral com registro.

## 7. Critérios de aceite de segurança (para cada release)

- [ ] Nenhum achado aberto de severidade alta ou crítica sem exceção aprovada.
- [ ] Testes de isolamento de tenant e de autorização passando.
- [ ] Varredura de dependências sem vulnerabilidades altas ou críticas.
- [ ] Varredura de segredos sem achados.
- [ ] Varredura dinâmica (DAST) em homologação, sem achado médio ou superior não tratado.
- [ ] Revisão de mudança em autenticação, autorização, cripto ou upload por pessoa com perfil de segurança.
- [ ] Nenhum arquivo de desenvolvimento no artefato de deploy.
