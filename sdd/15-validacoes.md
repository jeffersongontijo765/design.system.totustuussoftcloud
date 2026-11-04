# 15 — Validações de Dados, Transações e Integrações

> Parte do [SDD v2](00-README.md). Autorização e tenant em [04](04-api.md) e [06](06-identidade-acesso.md). Modelo de integração entre módulos em [14](14-integracao-modulos.md). Integrações externas em [16](16-integracoes-externas.md).
> **Status:** padrão e catálogo de plataforma **definidos**. Regras de campo e de negócio dos módulos funcionais **pendentes** (seção 9).

---

## 1. Ordem de validação

Toda requisição que altera dados passa pelas camadas abaixo, nesta ordem. Falha em uma camada interrompe as seguintes.

| # | Camada | O que verifica | Erro |
|---|---|---|---|
| 0 | Identidade e tenant | Usuário autenticado; tenant e unidade do contexto; permissão do recurso | `401`, `403` ou `404` |
| 1 | Formato | JSON válido, tamanho dentro do limite, tipos de campo | `400` |
| 2 | Campo | Obrigatoriedade, tamanho, formato, faixa, enumeração, unicidade dentro do tenant | `422` com `details` |
| 3 | Regra de negócio | Relação entre campos e entre entidades (ex.: data fim ≥ data início) | `422` |
| 4 | Estado | A transição pedida é permitida a partir do estado atual | `409` |
| 5 | Concorrência | `version` enviada bate com a versão atual do registro | `409` |
| 6 | Idempotência | Chave de idempotência já usada com o mesmo corpo retorna o resultado anterior; com corpo diferente, `409` | `409` |
| 7 | Persistência | Restrições do banco (chaves únicas, `NOT NULL`, chaves estrangeiras) como última barreira | `409` ou `500` |

Regras:

- A validação de campo roda no servidor. Validação no navegador é conveniência, nunca a única barreira.
- Mensagens de erro mostram o campo e a regra violada, sem valor sensível e sem nome de tabela.
- Erro de validação não cria registro, não gera evento e não consome chave de idempotência.

## 2. Tipos de campo padrão

Cada tipo tem regra única, reutilizada por todos os módulos.

| Tipo | Regra | Armazenamento |
|---|---|---|
| Texto curto | Unicode NFC; sem espaço no início e no fim; sem caractere de controle; tamanho máximo declarado | `VARCHAR` com o tamanho declarado |
| Texto longo | Mesmas regras; sem HTML; quebra de linha permitida | `TEXT` |
| Nome de pessoa | Texto curto, 2 a 150 caracteres, letras e separadores; sem números | `VARCHAR(150)` |
| CPF | 11 dígitos com dígitos verificadores válidos. Aceita máscara na entrada e grava só dígitos. Rejeita sequência repetida (000…0). | Cifrado; hash HMAC com pepper para busca e unicidade |
| CNPJ | 14 dígitos com dígitos verificadores válidos | Cifrado; hash para busca |
| E-mail | RFC 5321 simplificado, até 254 caracteres; minúsculas; verificado por link (D-04) | `VARCHAR(254)`; hash para unicidade |
| Telefone | E.164 (`+55…`); validado pelo número de dígitos do país | `VARCHAR(20)` |
| CEP | 8 dígitos; consulta de logradouro é opcional | `CHAR(8)` |
| Data | ISO 8601 (`AAAA-MM-DD`); faixa declarada por campo | `DATE` |
| Data e hora | ISO 8601 com fuso; armazenada em UTC | `DATETIME(6)` |
| Valor monetário | Decimal com 2 casas, positivo ou zero salvo quando o campo permite negativo; moeda do tenant ou ISO 4217 declarada | `DECIMAL(14,2)` e coluna de moeda |
| Percentual | Decimal entre 0 e 100, com 2 casas | `DECIMAL(5,2)` |
| Quantidade | Inteiro não negativo ou decimal com unidade declarada | `INT` ou `DECIMAL(12,3)` |
| Enumeração | Lista fechada no código; valor fora da lista é `422` | `VARCHAR` com `CHECK` ou tabela de domínio |
| Identificador | UUID no formato canônico; existência verificada no tenant | `CHAR(36)` |
| URL | `https://` apenas; domínio em lista de permitidos quando for destino de envio | `VARCHAR(2048)` |
| Arquivo | Ver seção 4.3 | Fora do webroot |
| Booleano | `true` ou `false`; outros valores são `422` | `TINYINT(1)` |

## 3. Regras transversais de CRUD

| Regra | Descrição |
|---|---|
| Tenant obrigatório | `tenant_id` vem do contexto. Campo `tenant_id` no corpo é ignorado e, se diferente, rejeitado. |
| Sem atribuição em massa | Só campos declarados no contrato são aceitos. Campo desconhecido é `422`. |
| Campo por permissão | Campo sensível (salário, laudo, dado bancário) só é gravado por quem tem permissão do campo. |
| Versão | Atualização exige `version`. Diferença é `409` (controle otimista). |
| Exclusão lógica | `deleted_at` preenchido. Exclusão bloqueada se houver dependente ativo; a resposta lista os tipos de dependentes, sem dados. |
| Unicidade | Restrição de unicidade é sempre composta com `tenant_id`. |
| Auditoria | Criação, alteração e exclusão gravam antes e depois, ator, IP, user-agent e correlação. |
| Edição parcial | `PATCH` aceita só os campos enviados. `PUT` exige o contrato completo. |

## 4. Matriz por tipo de operação

| Operação | Validações específicas | Controles adicionais |
|---|---|---|
| **Criar** | Campos obrigatórios; unicidade no tenant; referências existentes no tenant | Idempotência obrigatória quando o recurso gera cobrança, convite, envio ou evento |
| **Ler** | Identificador válido; recurso do tenant e da unidade | Campo filtrado pela permissão. Recurso de outro tenant responde `404`. |
| **Listar** | `page` e `per_page` (máx. 100); filtros e ordenação em lista branca | Contagem total opcional; busca com limite de caracteres |
| **Alterar** | `version`; campos permitidos para o estado atual | Auditoria antes e depois |
| **Excluir** | Dependentes ativos; estado permite exclusão | Exclusão lógica; motivo obrigatório para registros financeiros e de saúde |
| **Exportar** | Permissão de exportação; formato da lista; limite de linhas por exportação | Step-up de autenticação (ver [06](06-identidade-acesso.md), seção 5); CSV neutralizado (ver [08](08-frontend-design-system.md), seção 3); assíncrona acima de 5.000 linhas |
| **Importar** | Tipo e tamanho do arquivo; cabeçalho esperado; validação linha a linha | Modo simulação antes de gravar; relatório de erros por linha; limite de linhas; idempotência por lote |
| **Transação financeira** | Valor e moeda; estado de origem; vínculo com o recurso de origem | Chave de idempotência obrigatória; sem gravação parcial (transação de banco); reconciliação diária |
| **Entrada de integração** | Assinatura do remetente; schema da mensagem; deduplicação por ID | Resposta rápida, processamento assíncrono; ver seção 6 |
| **Saída de integração** | Resposta do terceiro validada contra schema esperado | Timeout, retentativa só em operação idempotente; ver [16](16-integracoes-externas.md) |

### 4.1 Transição de estado

Toda entidade com estado declara a tabela de transições. Transição fora da tabela é `409`. A tabela é a única fonte: não há exceção por perfil de usuário sem registro de auditoria justificado.

Modelo de declaração:

| Estado atual | Transições permitidas | Quem pode | Efeito |
|---|---|---|---|
| `rascunho` | `aberto`, `cancelado` | permissão do módulo | nenhum |
| `aberto` | `fechado`, `cancelado` | permissão do módulo e MFA recente | gera evento |
| `fechado` | `reaberto` (com justificativa) | perfil administrativo e step-up | auditoria reforçada |
| `cancelado` | nenhuma | — | bloqueia alteração |

### 4.2 Transação financeira

- Valor sempre positivo na requisição; sinal é definido pelo tipo de movimento.
- Arredondamento de moeda com regra única por tenant, declarada na configuração. Valor final é recalculado pelo servidor e comparado com o enviado; diferença é `422`.
- Pagamento só baixa título com estado `emitido` ou `vencido`.
- Estorno gera movimento novo, nunca altera o original.
- Dois pagamentos com a mesma chave de idempotência geram um único movimento.

### 4.3 Upload

- Tamanho máximo por tipo de arquivo, declarado no contrato do campo.
- Tipo validado pela assinatura do arquivo (bytes iniciais), não pela extensão.
- Lista branca por campo (ex.: foto aceita JPEG e PNG; documento aceita PDF).
- Imagem reprocessada no servidor para remover metadados e validar a estrutura.
- PDF com JavaScript ou com estrutura inválida é recusado.
- Nome do arquivo guardado só como metadado; o nome de armazenamento é um UUID.
- Download sempre por controller, com permissão e `Content-Disposition: attachment` quando o tipo não é imagem de exibição.

## 5. Catálogo de entidades de plataforma

Regras de campo das entidades da plataforma. Módulos funcionais seguem o mesmo formato (seção 9).

| Entidade | Campo | Regra | Unicidade | Observação |
|---|---|---|---|---|
| Cliente (mantenedora) | `name` | texto curto, 3 a 200 | — | |
| | `document` | CNPJ válido | por plataforma | cifrado |
| | `status` | `ativo`, `suspenso`, `encerrado` | — | transição na tabela da seção 4.1 |
| Entidade | `name` | texto curto, 3 a 200 | por cliente | |
| | `legal_name` | texto curto, 3 a 200 | por cliente | |
| | `document` | CNPJ válido | por plataforma | cifrado |
| | `locale_default` | código de locale suportado ([09](09-internacionalizacao.md)) | — | |
| | `currency` | ISO 4217 suportada pela plataforma | — | |
| Unidade | `name` | texto curto, 3 a 150 | por entidade | |
| | `code` | `[A-Z0-9-]`, 2 a 20 | por entidade | código legível |
| | `address` | CEP válido; número; complemento opcional | — | |
| Usuário | `email` | e-mail verificado (D-04) | por plataforma | canal de recuperação obrigatório |
| | `name` | nome de pessoa | — | pode vir de `person_id` |
| | `password` | regra de senha de [06](06-identidade-acesso.md), seção 3 | — | nunca em log |
| | `mfa_methods` | TOTP, passkey ou certificado; SMS e e-mail não são fator | — | |
| Vínculo (`UserMembership`) | `role_id` | papel do tenant; papel de plataforma só em conta de plataforma | — | |
| | `unit_ids` | unidades da mesma entidade | — | escopo `full` cobre todas |
| Convite | `email` | e-mail válido | por tenant, em aberto | expira em 72 h |
| | `role_id` | papel permitido para quem convida | — | |
| Consentimento | `purpose` | finalidade de lista fechada ([07](07-privacidade-lgpd.md), seção 3) | — | registro imutável |
| | `granted_at`, `revoked_at` | data e hora em UTC | — | revogação não apaga o histórico |
| Credencial de integração | `provider` | lista de provedores de [16](16-integracoes-externas.md) | — | |
| | `secret` | nunca gravado em texto; só referência ao cofre | — | |
| | `environment` | `sandbox` ou `production` | — | não pode usar credencial de produção em sandbox |
| Upload | `file` | ver seção 4.3 | — | |

## 6. Validação de integração

### 6.1 Entrada (webhook e API de parceiro)

1. Assinatura HMAC válida ([04](04-api.md), seção 7).
2. Timestamp dentro de 300 s e nonce não visto.
3. Schema da mensagem; campo desconhecido é ignorado e registrado, não causa erro, salvo em campo de identidade.
4. Deduplicação pelo identificador do evento.
5. Resposta `202` após gravar na fila; processamento depois.

### 6.2 Saída (chamada a terceiro)

1. Resposta validada contra o schema esperado. Campo ausente obrigatório é erro de integração, não de dado.
2. Código HTTP mapeado para estado interno: `2xx` sucesso; `4xx` falha definitiva, sem retentativa; `5xx` e timeout são falha transitória.
3. Retentativa só em operação idempotente ou com chave de idempotência do provedor.
4. Resposta bruta não é salva com dado pessoal; salva-se o código, o identificador do provedor e um resumo.

## 7. Transações críticas por domínio

Regras que exigem confirmação do módulo dono antes de virarem definitivas.

| Domínio | Transação | Regra mínima | Confirmação |
|---|---|---|---|
| Acadêmico | Matrícula | Vaga disponível com bloqueio de concorrência; um vínculo ativo por aluno e turma; período aberto | Owner do módulo |
| Acadêmico | Lançamento de nota | Nota dentro da faixa do método de avaliação; período de lançamento aberto; professor vinculado à turma | Owner do módulo |
| Financeiro | Emissão de cobrança | Valor positivo; vencimento não anterior à data de emissão; chave de idempotência | Owner do módulo e DPO (dados bancários) |
| Financeiro | Baixa de pagamento | Título em estado emitido ou vencido; valor não excede saldo; reconciliação | Owner do módulo |
| Suprimentos | Movimento de estoque | Saldo não pode ficar negativo, salvo item marcado como consumo sob encomenda | Owner do módulo |
| Suprimentos | Pedido a fornecedor bloqueado | Não pode ser emitido; regra de bloqueio do módulo | Owner do módulo |
| RH | Afastamento | Data fim não anterior à data início; sobreposição com afastamento ativo é recusada | Owner do módulo |
| SMT | Exame ocupacional | Tipo de exame válido para a função; resultado só com profissional responsável | Owner do módulo |
| Contratos | Consumo de saldo | Saldo do contrato ou ata suficiente; contrato vigente | Owner do módulo |

## 8. Padrão de regra por módulo

Cada módulo funcional deve publicar, antes da implementação, uma tabela com este formato. Ela é a fonte da validação daquele módulo.

| Recurso | Campo | Tipo (seção 2) | Obrigatório | Limites | Regra de negócio | Estado | Permissão |
|---|---|---|---|---|---|---|---|

E uma tabela de transições (seção 4.1) para cada entidade com estado.

## 9. Situação dos módulos

| Estado | Módulos |
|---|---|
| Padrão de validação definido (este documento) | Todos |
| Entidades de plataforma definidas (seção 5) | Identidade, tenant, consentimento, credencial, upload |
| Regras por módulo | **Pendentes** para os 40+ módulos do [catálogo](12-catalogo-modulos.md) |

Prioridade proposta para o preenchimento: Financeiro, Pessoas (HCM), Acadêmico, SMT, Suprimentos, Contratos, Billing. A ordem é decisão do autor.

## 10. Testes obrigatórios

- Para cada campo do catálogo: teste de aceitação e de rejeição com valores de limite.
- Para CPF e CNPJ: vetores de teste com dígitos verificadores válidos e inválidos.
- Para cada transição de estado: teste de permitida e de bloqueada.
- Para transação financeira: teste de idempotência com chave repetida e corpo diferente.
- Para upload: arquivo com extensão falsa, arquivo com JavaScript embutido e arquivo acima do limite.
- Para exportação: campo com `=` no início e valor negativo.

## 11. Critérios de aceite

- [ ] Toda operação de escrita passa pela ordem da seção 1.
- [ ] Todo campo de entrada tem tipo da seção 2 ou regra declarada no módulo.
- [ ] Nenhum campo de plataforma aceito sem estar no catálogo da seção 5.
- [ ] Toda transição de estado está em tabela.
- [ ] Todo módulo listado no catálogo tem tabela de validação antes de entrar em implementação.
