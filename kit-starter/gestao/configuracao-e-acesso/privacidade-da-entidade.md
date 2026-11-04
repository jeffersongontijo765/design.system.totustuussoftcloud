# Privacidade da entidade

- Portal: Gestão (`gestao.`)
- Área: Configuração e acesso
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 3; [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 4; [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 5; [07](../../../docs/v2/07-privacidade-lgpd.md) (integral)
- Fonte da v1: absorvida integralmente em [privacidade-dpo.md](../../desenvolvedor/seguranca-e-operacao/privacidade-dpo.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

LGPD da entidade como controladora: consentimentos, pedidos de titular, ROPA, incidentes e painel do DPO da entidade.

## 3. Telas

- **Painel do DPO** (dashboard).
- **Pedidos do titular** (fila com prazo).
- **Consentimentos** (lista por finalidade e canal).
- **ROPA** (registro de tratamento).
- **Incidentes** (registro e comunicação).

## 4. Permissões por portal (extraídas do SDD)

Do [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md):

| Portal | Quem abre | Onde é atendido | Visibilidade |
|---|---|---|---|
| Gestão | Equipe da entidade e atendentes | Fila da categoria e da unidade | Conforme permissão da fila |

Do [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md):

| Portal | Recurso de privacidade | Escopo |
|---|---|---|
| Gestão | DPO da entidade, ROPA da entidade, pedidos de titular, consentimentos, termos de imagem, proteção de menores | Entidade e unidades conforme permissão |

## 5. Papéis

- `entity.dpo`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- [07](../../../docs/v2/07-privacidade-lgpd.md) e [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seções 3 a 5.

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

### 13.1 [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 3

#### 3. Privacidade e LGPD

##### 3.1 Princípio de organização

A privacidade tem **duas escalas**:

- **Plataforma:** governança da própria empresa como controladora (ROPA, RIPD, incidentes, DPO, contratos com clientes).
- **Entidade:** governança do tenant como controlador. A plataforma é operadora. Cada entidade tem o próprio DPO, o próprio registro de tratamento e os próprios pedidos de titular.

Essa separação segue [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 1, e [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.

##### 3.2 Consentimento

Cada consentimento registra: finalidade, canal, versão do texto, data de concessão, data de revogação e evidência. Já definido em `crm_consents` ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 8). Falta generalizar:

| Regra | Detalhe |
|---|---|
| Finalidade separada | Cada finalidade tem consentimento próprio. Marketing não é condição de matrícula. |
| Revogação simples | Mesmo canal de concessão, sem barreira extra. Efeito imediato. |
| Consentimento não apagado | Revogação preenche `revoked_at`. Histórico fica. |
| Menor de 13 anos | Consentimento parental verificável antes da coleta. Método **(jurídico)**. |
| Menor de 18 e maior de 13 | Regra de [07](../../../docs/v2/07-privacidade-lgpd.md), seção 3. Confirmar base por tipo de dado **(jurídico)**. |
| Termo de imagem | Consentimento específico por finalidade (site, redes, mural). Revogável. |

##### 3.3 Solicitação do titular

Fluxo, com estados e prazo (base em [07](../../../docs/v2/07-privacidade-lgpd.md), seção 4):

| Estado | Ação |
|---|---|
| `recebida` | Protocolo gerado; prazo começa no recebimento |
| `identidade_pendente` | Verificação por canal verificado. Sem verificação, não há resposta. |
| `em_analise` | Atribuída a responsável. Avalia exceção legal. |
| `aguardando_dpo` | Pedido sensível ou com exceção: aprovação do DPO |
| `atendida` | Resposta entregue pelo canal verificado |
| `negada_com_motivo` | Recusa fundamentada, com a exceção legal citada **(jurídico)** |
| `encerrada` | Estado final |

Regras:

- Prazo de referência: 15 dias para confirmação e acesso, conforme [07](../../../docs/v2/07-privacidade-lgpd.md), seção 4 **(jurídico)**. O sistema calcula o prazo e alerta com antecedência.
- Pedido de titular que é menor passa pelo responsável legal, com verificação de vínculo ([07](../../../docs/v2/07-privacidade-lgpd.md), seção 4).
- Pedido recebido por atendimento vira ticket e protocolo (seção 2), com categoria `privacidade`.
- Exclusão respeita retenção legal e preservação probatória. Exceção é registrada com motivo ([31](../../../docs/v2/31-matriz-portais-modulos.md)).

##### 3.4 Registro de tratamento (ROPA)

Cada tratamento tem: finalidade, base legal, categoria de titular, categoria de dado, operador, prazo de retenção, medida de segurança e local de armazenamento. [07](../../../docs/v2/07-privacidade-lgpd.md), seção 2, exige o registro, mas não define a tabela.

**Pendência:** DDL do ROPA por escala (plataforma e entidade). Documento a criar.

##### 3.5 Incidentes

Já definido em [07](../../../docs/v2/07-privacidade-lgpd.md), seção 8, com prazo de três dias úteis **(jurídico)**. Falta o registro estruturado: tipo de dado, volume de titulares, risco, comunicação à ANPD e aos titulares, medidas e lições. Esse é o modelo de [18](../../../docs/v2/18-regras-modulos-2.md), seção 4.

##### 3.6 Transferência e operadores

Lista de operadores e contrato de tratamento: [07](../../../docs/v2/07-privacidade-lgpd.md), seção 7. Transferência internacional: **(jurídico)**. A v1 lista jurisdições de vários países ([`spec_gestao_privacy_global_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_privacy_global_completo.md), seção 4); a v2 limita ao Brasil, conforme [07](../../../docs/v2/07-privacidade-lgpd.md), seção 3, até haver cliente fora do país.

##### 3.7 Painel do DPO

O DPO precisa de:

- fila de pedidos de titular e de aprovação;
- prazos e alertas;
- incidentes em aberto;
- RIPD em andamento (lacuna G-05 em [25](../../../docs/v2/25-dossie-juridico-e-lacunas.md));
- trilha de decisão.

O DPO **não opera** o módulo que audita ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5). Ele vê o resultado, não altera o dado.

### 13.2 [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 4

#### 4. Privacidade por portal

| Portal | Recurso de privacidade | Escopo |
|---|---|---|
| Desenvolvedor | ROPA da plataforma, incidentes da plataforma, DPO da plataforma, contratos de operador com clientes | Plataforma apenas |
| Gestão | DPO da entidade, ROPA da entidade, pedidos de titular, consentimentos, termos de imagem, proteção de menores | Entidade e unidades conforme permissão |
| Professor | Próprias configurações de privacidade, consentimento de uso de imagem de turma | Só o próprio dado |
| Aluno | Dados cadastrais, solicitação LGPD, revogação de consentimento | Só o próprio dado |
| Responsáveis | Consentimento de imagem dos filhos, dados dos filhos, solicitação LGPD pelos dependentes | Só dependentes com vínculo ativo |
| Terceiros | Acordo de tratamento de dados (DPA), termo de confidencialidade | Só a própria empresa |

**Regra:** pedido de titular nunca é atendido por outro portal que não o do próprio titular ou do responsável verificado.

### 13.3 [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 5

#### 5. Pendências de privacidade e LGPD

| # | Pendência | Tipo |
|---|---|---|
| LGPD-01 | DDL do ROPA (plataforma e entidade) | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 2. Revisão do owner pendente (DDL-01) |
| LGPD-02 | DDL do pedido de titular e seus estados (seção 3.3) | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 2. Revisão do owner pendente (DDL-01) |
| LGPD-03 | Método de consentimento parental para menor de 13 anos | (jurídico) |
| LGPD-04 | Bases legais por tipo de dado escolar, incluindo menores | (jurídico), lacuna Q-03 a Q-08 em [25](../../../docs/v2/25-dossie-juridico-e-lacunas.md) |
| LGPD-05 | Transferência internacional, se houver cliente fora do Brasil | (jurídico) |
| LGPD-06 | Painel do DPO e RIPD (G-05) | Documento e (jurídico) |
| LGPD-07 | Quem é o DPO da plataforma e o de cada entidade | **Decidido** em 03/11/2026: plataforma é a empresa desenvolvedora. Entidade designa o seu, podendo contratar a empresa. Nomes a informar |
| LGPD-08 | Prazo de comunicação de incidente (três dias úteis, Resolução 15/2024) | (jurídico) confirmar vigência |

### 13.4 [07 — Privacidade e LGPD](../../../docs/v2/07-privacidade-lgpd.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Este documento é técnico. Não substitui parecer jurídico. Pontos marcados **(jurídico)** precisam de confirmação antes do go-live.

---

#### 1. Compromissos

1. Coletar apenas o dado necessário para uma finalidade declarada.
2. Informar o titular antes da coleta, em linguagem simples.
3. Responder às solicitações de direitos dentro do prazo legal.
4. Apagar ou anonimizar quando a finalidade acaba e não há obrigação legal de guarda.
5. Tratar dados de crianças e adolescentes com o melhor interesse, consentimento parental quando exigido e minimização reforçada. (Ecossistema educacional: **(jurídico)** confirmar bases por tipo de dado.)

#### 2. Inventário de dados

Cada tabela com dado pessoal tem, no registro de dados (ROPA), os campos: finalidade, base legal, categoria do titular, categoria do dado, operador, prazo de retenção e medida de segurança.

| Categoria | Exemplos | Sensibilidade |
|---|---|---|
| Identificação | Nome, e-mail, telefone, documento (CPF, RG) | Alta. Documento de identificação tem acesso restrito por política; não é dado sensível no sentido do art. 5º, II, LGPD. |
| Família | Responsáveis, parentesco | Alta (menores) |
| Acadêmico | Notas, frequência, histórico | Média |
| Saúde | Laudos, deficiência, alergias | **Sensível** (art. 11 LGPD) |
| Financeiro | Cobrança, dados bancários | Alta |
| Acesso | Logs de sessão, IP, User-Agent | Média |

#### 3. Bases legais

Matriz de base legal por finalidade. Status: **proposta, pendente de parecer jurídico**. Nenhuma linha é válida para produção antes da confirmação. Citações de artigos referem-se à LGPD (Lei 13.709/2018).

| Finalidade | Dado | Base proposta | Legislação setorial a confirmar | Confirmação |
|---|---|---|---|---|
| Matrícula e vínculo acadêmico | Identificação, responsáveis | Execução de contrato ou procedimentos preliminares (art. 7º, V); obrigação legal (art. 7º, II) | Normas de educação e de registro escolar | **(jurídico)** |
| Cobrança de mensalidades | Identificação, financeiro | Execução de contrato (art. 7º, V); exercício regular de direitos (art. 7º, VI) | Código de Defesa do Consumidor, quanto a cobrança e negativação | **(jurídico)** |
| Recursos humanos e folha | Identificação, salário, documentos trabalhistas | Obrigação legal (art. 7º, II) | CLT e normas do eSocial | **(jurídico)** |
| Segurança e medicina do trabalho | Dado de saúde ocupacional | Tutela da saúde (art. 11, II, f) ou obrigação legal (art. 11, II, a) | NRs do Ministério do Trabalho e Emprego | **(jurídico)** |
| Marketing | Contato | Consentimento (art. 7º, I), com revogação simples | Regras de envio de mensagens | **(jurídico)** |
| Segurança e logs | Acesso, IP, registro de ações | Legítimo interesse (art. 7º, IX), com teste de balanceamento documentado | Normas de segurança da informação | **(jurídico)** |
| Consulta por CPF ([21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6.8) | Identificação | Mesma base da finalidade declarada pelo tenant, sem base própria | Conforme a finalidade | **(jurídico)** |

**Escopo de legislação:** esta matriz cobre a legislação brasileira. Não afirma conformidade com outras jurisdições. A plataforma só atende outro país após revisão específica (lacuna LAC-15 em [19](../../../docs/v2/19-regras-modulos-3.md)). "Atender toda a legislação" não é uma condição que este SDD possa certificar: é tarefa contínua do jurídico, com revisão a cada mudança normativa.

#### 4. Direitos do titular

| Direito | Entrega | Prazo de referência |
|---|---|---|
| Confirmação e acesso | Exportação em formato legível e portável | 15 dias (art. 19 LGPD) |
| Correção | Edição com trilha de auditoria | Imediato quando possível |
| Anonimização, bloqueio ou eliminação | Processo de retenção | Conforme política e prazos legais |
| Portabilidade | JSON ou CSV | 15 dias |
| Revogação de consentimento | Efeito imediato nas finalidades dependentes | Imediato |
| Informação sobre compartilhamento | Lista de operadores e terceiros | 15 dias |

- Solicitação gera protocolo, registro e resposta por canal verificado.
- Exportação de dados pessoais exige step-up de autenticação (ver [06](../../../docs/v2/06-identidade-acesso.md)).
- Fluxo de pedido de titular para o responsável legal de menor segue a mesma regra, com verificação de vínculo.

#### 5. Retenção

- Prazo por categoria definido pela plataforma. A entidade pode reduzir, não estender além do que a lei permite. **(jurídico)** confirmar prazos de guarda de documentos escolares.
- Job diário de expurgo com relatório. Eliminação física registra data e tipo, sem guardar o dado eliminado.
- Backups seguem a mesma regra: retenção de backup é limitada e documentada, e restauração de backup reaplica expurgos já executados.

#### 6. Minimização nos logs

- Sem senha, token, cookie, CPF, dado de saúde ou corpo completo de requisição em log.
- E-mail e telefone mascarados (`j***@d***.com`).
- Logs de auditoria mantêm identificador interno do ator, não o nome.

#### 7. Transferência e operadores

- Lista de operadores (provedores de e-mail, SMS, pagamento, nuvem) com contrato de tratamento de dados.
- Transferência internacional só para países com nível adequado ou com cláusulas-padrão. **(jurídico)**
- Integrações enviam somente os campos necessários ao contrato com o terceiro.

#### 8. Incidentes e comunicação à ANPD

A v1 cita prazo de **72 horas**. A v2 corrige para o texto vigente: a Resolução CD/ANPD nº 15/2024 fixa o prazo de comunicação de incidente com risco ou dano relevante em **três dias úteis** a partir do conhecimento do incidente, e o art. 48 da LGPD exige comunicação ao titular. **(jurídico)** confirmar o prazo vigente antes de publicar o runbook.

Passos do runbook:

1. Conter e preservar evidências (sem alterar logs).
2. Avaliar: tipo de dado, volume de titulares, risco aos direitos, medidas aplicadas.
3. Comunicar internamente conforme severidade ([05](../../../docs/v2/05-seguranca.md), seção 6).
4. Comunicar à ANPD e aos titulares quando houver risco ou dano relevante, com conteúdo do modelo oficial.
5. Registrar o incidente, causa, ações e lições aprendidas.

#### 9. Métricas de privacidade

| Métrica | Meta |
|---|---|
| Pedidos de titular atendidos no prazo | 100% |
| Dados com retenção vencida e não expurgados | 0 |
| Campos sensíveis em log (varredura) | 0 |
| Operadores sem contrato de tratamento | 0 |

#### 10. Lacunas

Itens que a v1 listava como lacuna e que continuam abertos: ROPA completo por tabela, parecer de legítimo interesse, prazos de retenção aprovados, fluxo de consentimento para menores. Cada um tem dono e prazo no [backlog](../../../docs/v2/11-governanca-qualidade.md).
