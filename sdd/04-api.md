# 04 — API REST

> Parte do [SDD v2](00-README.md). Controles de segurança detalhados em [05](05-seguranca.md).

---

## 1. Base e versionamento

- Base: `/api/v1/`. Mudança incompatível exige `/api/v2/` com controller próprio.
- Mudanças aditivas (campos novos opcionais, endpoints novos) são permitidas em v1.
- Remoção ou renomeação de campo exige período de depreciação de pelo menos 6 meses, com cabeçalho `Deprecation` e `Sunset` (RFC 9745 e RFC 8594).
- Documentação gerada a partir de anotações do código e publicada em `/api/docs` (**[Planejado]**: a v1 cita `docs/api-docs.php`, mas o arquivo não é verificado nesta versão).

## 2. Formato

- JSON em UTF-8. `Content-Type: application/json; charset=utf-8`.
- Limite de corpo: **1 MB** para JSON. Uploads têm rota própria com limite por tipo.
- Datas em ISO 8601 com fuso (`2026-11-02T14:00:00-03:00`) ou UTC (`Z`).

### Envelope

Sucesso:

```json
{ "success": true, "data": { }, "meta": { "request_id": "..." } }
```

Erro:

```json
{
  "success": false,
  "error": { "code": "validation_failed", "message": "Mensagem segura para exibir", "details": [ ] },
  "meta": { "request_id": "..." }
}
```

- `message` nunca contém SQL, stack trace, caminho de arquivo ou nome de tabela.
- `details` só aparece em `validation_failed`, com campo e regra.

## 3. Códigos HTTP

| Código | Uso |
|---|---|
| 200 / 201 / 204 | Sucesso (201 com `Location`) |
| 400 | Requisição malformada |
| 401 | Não autenticado |
| 403 | Autenticado, sem permissão |
| 404 | Não existe **ou** pertence a outro tenant (evita enumeração) |
| 409 | Conflito de estado ou idempotência |
| 413 | Payload acima do limite |
| 422 | Validação de domínio |
| 429 | Limite de taxa (com `Retry-After`) |
| 500 | Erro interno (sem detalhes ao cliente) |

Códigos de erro estáveis: `validation_failed`, `unauthorized`, `forbidden`, `not_found`, `rate_limited`, `conflict`, `payload_too_large`, `internal`.

Mapeamento: `validation_failed` com `422` (campo inválido) ou `400` (corpo malformado); `unauthorized` com `401`; `forbidden` com `403`; `not_found` com `404`; `rate_limited` com `429`; `conflict` com `409`; `payload_too_large` com `413`; `internal` com `500`. Campo de filtro ou ordenação fora da lista branca retorna `422` com `validation_failed`.

## 4. Autenticação de API

| Mecanismo | Uso | Regras |
|---|---|---|
| Sessão (cookie) | Frontend do próprio sistema | Cookie `HttpOnly`, `Secure`, `SameSite=Lax` (ver [06](06-identidade-acesso.md)). Requisições que mudam estado exigem CSRF. |
| Bearer JWT | Clientes técnicos registrados | Assinatura RS256; `exp` ≤ 15 min; `aud` e `iss` validados; `jti` consultado em lista de revogação; escopos explícitos. |
| HMAC (webhooks e integrações) | Entrega de eventos e chamadas de integração | Ver seção 7. |
| Chave de API | Integrações de baixo risco (somente leitura) | Armazenada como hash; exibida uma única vez; rotacionável; escopo e expiração obrigatórios. |

Nenhum token é aceito na query string. O endpoint de emissão de token e o grant OAuth2 para contas de serviço ainda não estão definidos: pendentes de ADR.

## 5. Autorização

1. `Auth` valida identidade.
2. `TenantContext` valida tenant e unidade.
3. `Authorize` exige permissão `modulo.recurso.acao`.
4. O serviço revalida o vínculo do recurso com o tenant (defesa em profundidade contra BOLA).
5. Campos sensíveis são filtrados por permissão de campo (BOPLA): o mesmo recurso pode ter visões diferentes.

## 6. Paginação, filtros e ordenação

- `?page=1&per_page=50`. `per_page` máximo **100**.
- Filtros no formato `filter[campo]=valor`. Campo fora de lista branca retorna `422`.
- Ordenação `sort=campo` ou `sort=-campo` somente em colunas da lista branca do recurso.
- Resposta paginada inclui `meta.page`, `meta.per_page` e `meta.total` (ou `meta.has_more` para listas grandes, sem contagem total).

## 7. Webhooks

Cabeçalhos de entrega:

- `X-Signature: sha256=<hex>` — HMAC-SHA256 do corpo bruto concatenado com timestamp (`{timestamp}.{corpo}`).
- `X-Timestamp` — epoch em segundos.
- `X-Nonce` — identificador único por entrega.
- `X-Event-Id` — idempotência no receptor.

Regras:

1. Receptor aceita timestamp com desvio de **até 300 s** e rejeita nonce já visto dentro dessa janela.
2. Comparação de assinatura com `hash_equals`.
3. Segredo por endpoint, com rotação que aceita dois segredos por até 24 h.
4. Entrega com retentativa exponencial e limite de tentativas; estado da entrega é consultável.
5. Endereço de destino só `https://`. Bloqueio de redes privadas e metadados de nuvem (anti-SSRF). Resolver o nome uma vez, conectar ao IP resolvido, validar esse IP contra redes privadas e não seguir redirecionamentos.

## 8. Idempotência

- Operações não idempotentes (criação de pagamento, envio de comunicação, matrícula) exigem `Idempotency-Key`.
- Chave armazenada com hash do método, caminho e corpo, por 24 h. Mesma chave com corpo diferente retorna `409`.

## 9. Limites de taxa

| Escopo | Limite inicial | Observação |
|---|---|---|
| API global por cliente | 60 req/min, rajada 10 | Valores de referência da v1; ajustar por medição |
| Login, MFA, recuperação | Atraso progressivo por identificador + limite por IP | Não bloquear conta inteira (ver [06](06-identidade-acesso.md)) |
| Operações pesadas (exportação) | 5/h por usuário | Fila assíncrona com link de download temporário |

## 10. Checklist de aceite de endpoint

- [ ] Autenticação declarada na rota (ou rota pública listada).
- [ ] Permissão granular definida e testada (permitido e negado).
- [ ] Escopo de tenant na consulta e teste de cross-tenant.
- [ ] Validação de entrada com schema; payload ≤ limite.
- [ ] Envelope de resposta e códigos de erro da seção 2 e 3.
- [ ] Limite de taxa aplicado.
- [ ] Idempotência quando aplicável.
- [ ] Teste automatizado para o caminho de sucesso e para os dois principais erros.
- [ ] Entrada em `docs` gerada a partir do código.
