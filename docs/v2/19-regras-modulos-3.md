# 19 — Regras de Validação: Demais Módulos do Catálogo

> Parte do [SDD v2](00-README.md). Continua [17](17-regras-modulos.md) e [18](18-regras-modulos-2.md). Padrão em [15](15-validacoes.md). Catálogo em [12](12-catalogo-modulos.md).
> **Escopo deste documento:** módulos restantes com regras de validação identificadas na v1. Onde a v1 não define DDL, a seção do módulo lista as regras encontradas e o que falta. Não é uma especificação campo a campo.

---

## 1. Defeitos transversais

| ID | Defeito | Módulos afetados | Correção |
|---|---|---|---|
| T-01 | Sem `tenant_id` nos DDL. Contagem: CRM (5 tabelas), Patrimônio (12), Frotas (13), Biblioteca (5), Armazenamento (17). | Esses módulos | `tenant_id` NOT NULL e índice composto ([03](03-dominio-tenancy.md)). |
| T-02 | Sem DDL: Documentos, Marketing, SAC/Helpdesk, Simulados IA, Preceptoria, Privacidade global. | Esses módulos | DDL antes da implementação. |
| T-04 | Valor derivado armazenado como valor atual. Ex.: Patrimônio guarda `current_value`, que depende de depreciação. | Patrimônio | Armazenar o último cálculo com data e método. Recalcular, não sobrescrever. |
| T-07 | Duplicidade. Ver seção 2. | Vários | Uma especificação por domínio. |

## 2. Duplicidades a resolver

| Módulo A | Módulo B | Sobreposição | Proposta |
|---|---|---|---|
| Armazenamento (estoque, 17 tabelas) | Suprimentos (almoxarifado) | Saldo, movimento, estoque mínimo, rastreabilidade por lote | Suprimentos é dono de estoque e movimento. Armazenamento é renomeado para sistema de arquivos e documentos, sem estoque. **Decidido** em 03/11/2026. |
| Logger | Auditoria | Registro de eventos, bloqueio de IP, alertas de segurança | Auditoria é dona de trilha de negócio e de segurança ([18](18-regras-modulos-2.md), seção 4). Logger técnico fica em [10](10-implantacao-operacao.md), seção 7. |
| Autenticação (v1, 1.001 linhas) | 06 e 07 | Login, sessão, MFA, senha | Consolidar em [06](06-identidade-acesso.md). A especificação de módulo perde o conteúdo que duplica 06. |
| Privacidade global | 07 e Cookies e sessões | Direitos do titular, consentimento, cookies | Consolidar em [07](07-privacidade-lgpd.md). Cookies e sessões fica em 06. |
| Bancos (administração de banco de dados, 305 linhas) | Financeiro (contas bancárias) | Nenhuma: são assuntos diferentes | Bancos sai do escopo. Dados bancários ficam no Financeiro. Ver [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 4. |
| SAC, Chat rápido, Helpdesk | Entre si | Atendimento e tickets | Um único módulo de atendimento. Helpdesk é a base. Proposta na seção 7. |
| Biblioteca acadêmica e Biblioteca completo | Entre si | Acervo, empréstimo, multa | Uma especificação. Escolher a mais recente como base. |

## 3. Documentos

| Regra | Detalhe |
|---|---|
| Edição após assinatura | Bloqueada. Só nova versão autorizada (v1, linhas 255 e 380). |
| Download restrito | Bloqueado para documento marcado como restrito (v1, linha 298). |
| Rejeição | Exige motivo obrigatório (v1, linha 386). |
| Versão | Cada versão guarda hash SHA-256 do arquivo e autor. |
| Retenção | Por política, com expurgo registrado ([07](07-privacidade-lgpd.md)). |
| Arquivo | Validação de tipo e tamanho por campo ([15](15-validacoes.md), seção 4.3). |

**Pendente:** DDL (T-02). Lista de tipos de documento e prazo de retenção por tipo.

## 4. Privacidade global

A v1 descreve modelo tenant-aware e unit-aware (linha 8) e cobre direitos do titular, consentimento parental e múltiplas jurisdições. As regras já estão em [07](07-privacidade-lgpd.md). Pontos que faltam:

| Regra | Detalhe |
|---|---|
| Menor de 13 anos | Consentimento parental verificável antes de coletar (v1, linha 39). Verificação do responsável por canal verificado. **(jurídico)** para validar o método. |
| Jurisdições | A v1 cita Singapura, Tailândia e outras. **[Pendente]** A plataforma opera no Brasil; a lista de jurisdições só entra se houver cliente fora do Brasil. |
| Exclusão | Respeita retenção legal e necessidade de preservação probatória (v1, linha 28). Registro de exceção com motivo. |

**Defeito:** a v1 é uma lista de princípios, sem DDL nem campos. Não é possível validar. Proposta: reduzir a [07](07-privacidade-lgpd.md) e tirar a lista de jurisdições do escopo desta versão.

## 5. Armazenamento (estoque)

Este módulo é tratado como estoque, por causa do conteúdo. Ver seção 2.

| Regra | Detalhe |
|---|---|
| Saldo | Nunca negativo, bloqueio na API (linha 54). |
| Rastreabilidade | Lote, série ou validade obrigatório para item controlado (linha 57). |
| Bloqueio de item | Status `Bloqueado` impede movimento. Motivo registrado. |
| Movimento | Quantidade obrigatória e maior que zero. |

**Pendente:** os 17 DDL precisam da fronteira com Suprimentos (seção 2) antes de validar.

## 6. CRM e funil comercial

| Entidade | Estados (DDL) | Regra |
|---|---|---|
| Lead | `new`, `contacted`, `qualified`, `disqualified`, `converted` | Conversão cria oportunidade. |
| Oportunidade | `open`, `won`, `lost` | `estimated_value DECIMAL(12,2)`, maior ou igual a zero. |
| Atividade | — | Vínculo obrigatório a lead ou oportunidade (linha 106). |

- "Fechado perdido" exige motivo obrigatório (linha 97): preço, concorrência, sem orçamento, timing ou outro.
- Lead convertido não volta a `new`.
- **Defeito:** sem `tenant_id` (T-01). Lead contém dado pessoal de terceiro. Base legal de contato comercial precisa de parecer ([07](07-privacidade-lgpd.md)).

## 7. Atendimento (SAC, Chat rápido, Helpdesk)

Três especificações descrevem o mesmo tipo de solicitação. A v1 do Helpdesk cita tenant 23 vezes e define obrigatoriedade dinâmica por tipo (linhas 142 e 340).

Regras do Helpdesk:

| Regra | Detalhe |
|---|---|
| Campos obrigatórios | Variam por tipo de solicitação (linha 142). |
| Campos padrão | Lista fixa para todo tipo (seção 8.1). |
| Retenção | Política e expurgo (linha 791). |
| Canais | Obrigatórios por tipo (seção 6.1). |

**Proposta:** um módulo de atendimento. Helpdesk como base. SAC e Chat rápido viram canais ou tipos de solicitação.

**Pendente:** DDL (T-02).

## 8. Patrimônio

### 8.1 Entidades com DDL (12 tabelas)

Categorias de ativo, ativos e demais. Valores em `DECIMAL(15,2)` e taxa em `DECIMAL(8,4)`. Os tipos estão adequados.

### 8.2 Regras

| Campo | Regra |
|---|---|
| `acquisition_value` | Maior que zero. Não altera após a aquisição, salvo correção com motivo. |
| `residual_value` | Não negativo; não maior que `acquisition_value`. |
| `dep_method` | Lista fechada: `linear`, `accelerated`, `degressive`, `unit`. |
| `dep_rate` | Entre 0 e 100%, conforme método. |
| `current_value` | Calculado. Não é campo editável. Ver T-04. |
| Baixa | Ativo baixado não recebe depreciação nem movimento. |

**Pendente:** regra de depreciação por categoria, aprovada pela contabilidade.

## 9. Frotas

| Regra | Detalhe |
|---|---|
| CNH do motorista | Vencida bloqueia a reserva e exibe alerta (linha 422). |
| Conflito de horário | Bloqueia a reserva do veículo (linha 421). |
| Veículo em manutenção | Bloqueia; sugere veículo alternativo (linha 423). |
| Tacógrafo | Validade obrigatória quando aplicável (linha 240). |
| Consumo | Calculado a partir de litros e quilometragem. Não editável (linha 580). |
| Abastecimento | Litros obrigatório e maior que zero (linha 612). |

**Defeito:** 13 DDL sem `tenant_id` (T-01). Consumo "calculado" aparece como campo de entrada em outra tela (linha 215). Padronizar como calculado.

## 10. Biblioteca acadêmica

| Regra | Detalhe |
|---|---|
| Multa | Multa em aberto ou item atrasado bloqueia novo empréstimo (linhas 39 e 109). |
| Renovação | Bloqueada se o item tiver reserva pendente (linha 164). |
| Reserva | Check-in obrigatório para validar a reserva (linha 151). |
| Responsável | Vê empréstimos e multas do filho vinculado, somente leitura (linha 28). |
| Status do item | `active`, `archived`, `lost`. |

**Defeito:** 5 DDL sem `tenant_id` (T-01).

## 11. Preceptoria e autoavaliação

| Regra | Detalhe |
|---|---|
| Pergunta | Tipo, peso e obrigatoriedade configuráveis (linha 38). |
| Condicional | Pergunta pode depender de outra (linha 260). |
| Avaliação fechada | Não pode ser editada (linha 263). |
| Anonimato | **[Pendente]** Avaliação de preceptor deve ser anônima para o avaliado, com regra de mínimo de respostas por grupo para não identificar a pessoa. |

**Pendente:** DDL (T-02).

## 12. Simulados com IA

| Regra | Detalhe |
|---|---|
| Auditoria | Obrigatória em notas e revisões (linha 610). |
| Conteúdo gerado | Revisão humana antes de publicar **[Pendente: regra de quem revisa]**. |
| Dados enviados ao provedor | Só o conteúdo do simulado, sem dado pessoal do aluno. Registrar o provedor e a retenção dele ([16](16-integracoes-externas.md)). |

**Defeito:** sem DDL (T-02). Sem definição de como o aluno é identificado nas respostas enviadas à IA.

## 13. Client migration

| Regra | Detalhe |
|---|---|
| Checksum | Hash de cada arquivo enviado (linha 316). Divergência é erro (linha 353). |
| Segredos | Credenciais não são migradas em texto. Hash ou recadastro (linha 553). |
| Idempotência | Token por execução de job (linha 687) e chave por registro (linha 869). |
| Isolamento | Migração de dados entre tenants exige revisão de isolamento ([17](17-regras-modulos.md), seção 1). |

**Defeito:** sem DDL (T-02).

## 14. Soft delete

| Regra | Detalhe |
|---|---|
| Colunas | `deleted_at`, `deleted_by` em toda tabela soft-deletable (seção 3.1). |
| Validação pré-exclusão | Obrigatória. Ex.: aluno com matrícula ativa não pode ser excluído (linha 111). |
| Expurgo | Hard delete após N dias configurados por entidade, por job (linha 56). |
| Testes | Restauração e expurgo testados (seção 4.2). |

**Conflito:** o expurgo do soft delete precisa respeitar a imutabilidade da auditoria ([18](18-regras-modulos-2.md), seção 4.2). Registro de auditoria não é expurgado por soft delete.

## 15. Marketing e redes sociais

| Regra | Detalhe |
|---|---|
| Publicação | Campos de título, texto, rede, data e aprovação obrigatórios (linha 126). |
| Aprovação | Publicação só após aprovação de quem tem permissão (fluxo de aprovação). |
| Datas críticas | Bloqueadas para publicação (linha 214). |
| Palavras bloqueadas | Lista de termos que impede publicação (linha 282). |
| Contato | Bloquear, silenciar ou priorizar contato respeita consentimento ([07](07-privacidade-lgpd.md)). |

**Defeito:** sem DDL (T-02). Sem tenant. **Resolvido em 04/11/2026:** DDL com `unidade_uuid` em [51](51-ddl-modulos-novos.md), seção 19.

## 16. Bancos

Removido do escopo ([34](34-pagamentos-fiscal-bancos-por-portal.md), seção 4). As regras da v1 (alteração por pipeline, backup, TLS) valem para a ferramenta de operação, que fica fora do produto.

## 17. Autenticação (módulo de origem)

A especificação v1 (1.001 linhas) já exige Argon2id e refresh token armazenado com hash (linhas 267, 272 e 329). Está alinhada com [06](06-identidade-acesso.md). Não há regra nova a acrescentar. O módulo deve ser consolidado em 06 (seção 2).

## 18. Lacunas

| # | Lacuna | Dono sugerido | Situação em 04/11/2026 |
|---|---|---|---|
| LAC-14 | Fronteira Armazenamento/Suprimentos (seção 2) | Produto | Resolvida ([19](19-regras-modulos-3.md), seção 2) |
| LAC-15 | Lista de jurisdições da privacidade (seção 4) | Jurídico | Resolvida: só legislação brasileira ([07](07-privacidade-lgpd.md), seção 3) |
| LAC-16 | Anonimato na avaliação de preceptor (seção 11) | Acadêmico | Resolvida: anônima, mínimo de 2 respostas por grupo ([42](42-preceptoria-por-portal.md), PRE-03) |
| LAC-17 | Regra de revisão humana de conteúdo gerado por IA (seção 12) | Acadêmico, Jurídico | Resolvida: a IA sugere e a pessoa decide ([27](27-inteligencia-artificial-e-portais.md), princípio 2) |
| LAC-18 | Regra de depreciação por categoria (seção 8) | Contabilidade | Resolvida por padrão: DP-02 ([80](80-decisoes-por-padrao.md)) |
| LAC-19 | Módulo de atendimento único (seção 7) | Produto | Resolvida: modelo único de ticket ([32](32-atendimento-privacidade-por-portal.md), seção 2.1) |
| LAC-20 | DDL de Documentos, Marketing, Atendimento, Simulados, Preceptoria, Privacidade | Owners | Resolvida: DDL de documentos ([51](51-ddl-modulos-novos.md), seção 12; [54](54-gestao-de-documentos-tres-contextos.md), seção 10), atendimento ([51](51-ddl-modulos-novos.md), seção 1), privacidade ([51](51-ddl-modulos-novos.md), seção 2), preceptoria ([51](51-ddl-modulos-novos.md), seção 6), simulados ([51](51-ddl-modulos-novos.md), seção 15) e marketing ([51](51-ddl-modulos-novos.md), seção 19). Aguarda revisão do owner |

## 19. Critérios de aceite

- [ ] Cada módulo do catálogo tem uma seção aqui ou em 17 e 18, ou está marcado como duplicado.
- [ ] Duplicidades da seção 2 têm decisão registrada.
- [ ] Todo DDL tem `tenant_id NOT NULL` (T-01).
- [ ] Valor derivado não é campo editável (T-04).
