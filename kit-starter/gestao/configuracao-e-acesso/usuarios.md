# Usuários

- Portal: Gestão (`gestao.`)
- Área: Configuração e acesso
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 2; [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 4.2; [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 5; [06](../../../docs/v2/06-identidade-acesso.md), seção 2; [06](../../../docs/v2/06-identidade-acesso.md), seção 5; [06](../../../docs/v2/06-identidade-acesso.md), seção 7; [06](../../../docs/v2/06-identidade-acesso.md), seção 9
- Fonte da v1: absorvida integralmente em [acesso.md](../../desenvolvedor/seguranca-e-operacao/acesso.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Convidar, ativar, bloquear e revisar usuários da entidade e atribuir papéis até o nível 3, com revisão periódica.

## 3. Telas

- **Usuários** (DataTable: nome, e-mail, papéis, unidades, último acesso, MFA).
- **Convidar usuário** (e-mail, papel, unidade).
- **Usuário — detalhe** (papéis e escopos, sessões ativas, histórico).
- **Revisão de acesso** (campanha trimestral e anual com confirmação por gestor).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `entity.admin`: papéis até nível 3.
- `entity.security`: bloquear conta, política de MFA da entidade.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Níveis e atribuição ([78](../../../docs/v2/78-permissoes-e-papeis.md), seção 2.1); default-deny ([78](../../../docs/v2/78-permissoes-e-papeis.md), seção 5).

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

### 13.1 [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 2

#### 2. Modelo

- **Permissão:** `modulo.recurso.acao` (ex.: `academico.nota.lancar`), como em [06](../../../docs/v2/06-identidade-acesso.md), seção 9.
- **Papel:** coleção de permissões, com **nível** e **escopo**.
- **Escopo:** `plataforma`, `entidade`, `unidade`, `turma` (para docentes), `proprio` (somente o próprio registro). Escopo mais estreito nunca amplia o papel.
- **Vínculo:** uma pessoa tem um ou mais vínculos (entidade, unidade, papel). Permissão efetiva é a união dos vínculos ativos, menos as negações.
- **Negação explícita** vence concessão ([06](../../../docs/v2/06-identidade-acesso.md), seção 9).

##### 2.1 Níveis de papel (D-38, aprovada)

| Nível | Nome | O que faz | Exemplo |
|---|---|---|---|
| 0 | Próprio | Vê e atualiza só os próprios dados, quando permitido | Aluno, responsável, terceiro |
| 1 | Operador | Executa tarefas no escopo atribuído | Secretário, professor de turma |
| 2 | Coordenador | Gerencia tarefas de um conjunto de operadores e aprova o que é de nível 1 | Coordenador de turno |
| 3 | Gestor | Responde pela unidade inteira | Diretor de unidade |
| 4 | Administrador da entidade | Responde pela entidade: unidades, usuários e configurações, exceto criação de entidade ou unidade | Diretor geral |
| 5 | Operador da plataforma | Suporte, atendimento e operação, sem acesso a dado de entidade sem motivo registrado | Equipe de suporte |
| 6 | Gestor da plataforma | Operação da plataforma, planos e clientes, sem criar entidade ou unidade | Gerente de operação |
| 7 | Desenvolvedor | Criação de entidade e unidade (L-02), planos, limites, licenças e Editor de portais | `platform.developer` |

Regras de nível:
- Um papel só concede permissões do seu nível ou inferiores. Atribuir um papel de nível igual ou superior exige o aprovador de nível superior.
- Papéis de nível 3 e acima, e todos os da plataforma, exigem **justificativa** e **revisão trimestral** ([06](../../../docs/v2/06-identidade-acesso.md), seção 9).
- Papéis de nível 0 a 2 têm revisão anual.

##### 2.2 Separação de funções (D-39, aprovada)

| Ação | Não pode ser feita pela mesma pessoa |
|---|---|
| Criar e aprovar mudança no Editor de portais: quem edita é `platform.builder` e quem aprova é `platform.developer` (D-33) | Sim ([23](../../../docs/v2/23-dominios-provisionamento-ciclo-de-vida.md), seção 3) |
| Lançar nota e aprovar a nota | Sim |
| Cadastrar fornecedor e aprovar pagamento | Sim |
| Criar usuário e conceder papel de nível 3 ou acima | Sim |
| Criar plano e aplicar plano a entidade | Sim |

### 13.2 [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 4.2

##### 4.2 Portal de Gestão (SaaS da entidade)

| Papel | Nível | Escopo | Pode |
|---|---|---|---|
| `entity.admin` | 4 | entidade | Unidades, usuários, papéis até nível 3, configurações da entidade |
| `unit.manager` | 3 | unidade | Gestão da unidade: acadêmico, financeiro, pessoas, suprimentos |
| `unit.coordinator` | 2 | unidade | Coordenação de turno ou área; aprova tarefas de nível 1 |
| `unit.secretary` | 1 | unidade | Matrícula, documentos, protocolos |
| `unit.finance` | 1 | unidade | Títulos, cobrança, conciliação |
| `unit.hr` | 1 | unidade | Pessoas, folha, ponto |
| `unit.librarian` | 1 | unidade | Acervo, empréstimos |
| `unit.support` | 1 | unidade | Atendimento, SAC, tickets |
| `unit.auditor` | 2 | unidade | Leitura de auditoria da unidade |
| `unit.accounting` | 1 | unidade | Papel **Contábil** do [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5: lançar, fechar período, exportar; não fecha período com lançamento que criou sem revisão |
| `unit.fiscal` | 1 | unidade | Papel **Fiscal** do [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5: emitir e cancelar NFS-e, apurar tributos e retenções; cancelamento exige aprovação do contábil |
| `unit.finance.approver` | 2 | unidade | Aprovar despesa, estorno e baixa manual na alçada; não aprova o que lançou ([17](../../../docs/v2/17-regras-modulos.md), seção 2.4) |
| `unit.commercial` | 1 | unidade | Papel **Comercial** do [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5, no CRM do tenant (seção 4.2): captação, pré-cadastro, proposta; não aprova desconto acima da alçada |
| `unit.purchasing` | 1 | unidade | Papel **Compras**: cotação, pedido, cadastro de fornecedor; não aprova a própria requisição nem recebe a própria compra |
| `unit.warehouse` | 1 | unidade | Papel **Almoxarifado**: recebimento e movimento; ajuste de estoque só com motivo e aprovação |
| `unit.purchasing.approver` | 2 | unidade | Papel **Aprovador de compras**: aprova requisição na alçada; não é o solicitante |
| `unit.assets` | 1 | unidade | Patrimônio da entidade: cadastro, movimentação, inventário ([19](../../../docs/v2/19-regras-modulos-3.md), seção 8) |
| `unit.assets.approver` | 2 | unidade | Aprovar transferência, baixa e manutenção acima do limite; não aprova o que registrou (DP-05) |
| `unit.fleet` | 1 | unidade | Frotas e rotas da entidade ([19](../../../docs/v2/19-regras-modulos-3.md), seção 9) |
| `unit.fleet.approver` | 2 | unidade | Aprovar reserva e ordem de manutenção de veículo; não aprova a própria (DP-05) |
| `unit.payroll` | 1 | unidade | Papel **Folha**: processar a folha; folha fechada não muda |
| `unit.payroll.approver` | 2 | unidade | Aprovar a folha; quem processa não aprova ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 7) |
| `unit.sst.doctor` | 1 | unidade | Médico do trabalho: ASO, prontuário ocupacional, CID ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 7; [52](../../../docs/v2/52-medicina-do-trabalho-especificacao.md)) |
| `unit.sst.technician` | 1 | unidade | SESMT: CAT, EPI, NR, PGR, ocorrências; sem diagnóstico |
| `unit.legal` | 2 | entidade | Papel **Jurídico**: parecer, bloqueio legal; leitura de contratos, documentos e auditoria; não altera contrato assinado |
| `entity.dpo` | 2 | entidade | Papel **Encarregado (DPO)** da entidade ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 7): ROPA, pedidos de titular, incidentes, relatório de impacto; não opera o módulo que audita |
| `entity.security` | 3 | entidade | Papel **Segurança** da entidade: investigar, bloquear conta, política de MFA da entidade; não concede permissão a si mesmo |
| `unit.it.admin` | 2 | unidade | Administrador de TI da entidade ([36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 6): ativos, licenças, chamados e mudanças; não aprova a própria mudança |
| `unit.it.technician` | 1 | unidade | Técnico de TI: atender chamados e incidentes; não altera contrato nem exclui ativo |
| `unit.it.change_approver` | 2 | unidade | Comitê de mudança: aprova ou recusa; não executa a mudança que aprovou |
| `unit.preceptoria.manager` | 2 | unidade | Gestão de preceptoria ([42](../../../docs/v2/42-preceptoria-por-portal.md), seção 5): instrumentos, ciclos, programas, pesos, relatório agregado; não vê resposta individual nem anotação de tutoria |
| `unit.pastoral` | 1 | unidade | Equipe pastoral ([43](../../../docs/v2/43-pastoral-por-portal.md), seção 5): agenda, escala, evento, campanha e beneficiário da campanha; não vê anotação de acompanhamento alheia |
| `unit.reception` | 1 | unidade | Portaria e acesso físico ([35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md), seção 4): entradas e saídas, visitantes, autorizações de retirada |

Os papéis acima vêm dos papéis nomeados no [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5, e nos documentos por portal; os códigos seguem a convenção desta seção (DP-05, [80](../../../docs/v2/80-decisoes-por-padrao.md)). A coordenação pedagógica usa `unit.coordinator`; a secretaria, `unit.secretary`.

### 13.3 [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 5

#### 5. Regras transversais (D-40, aprovada)

1. **Default-deny:** rota ou ação sem papel explícito é negada, como em [03](../../../docs/v2/03-dominio-tenancy.md).
2. **Escopo verificado no servidor:** o escopo `turma`, `unidade` ou `proprio` é conferido em cada consulta, não só na tela.
3. **Papel por portal:** papel de um portal não dá acesso a outro, mesmo com a mesma conta ([23](../../../docs/v2/23-dominios-provisionamento-ciclo-de-vida.md), seção 2).
4. **Ações sensíveis com step-up:** exportação, alteração de papel e exclusão exigem autenticação recente ([06](../../../docs/v2/06-identidade-acesso.md), seção 5).
5. **Revisão e expiração:** vínculo temporário tem data de fim. Vínculo vencido sai sozinho e gera auditoria.
6. **Auditoria:** toda concessão, revogação e mudança de papel gera registro com justificativa para níveis 3 e acima.

### 13.4 [06](../../../docs/v2/06-identidade-acesso.md), seção 2

#### 2. Autenticação de usuário

Fluxo:

1. Recebe e-mail e senha na tela de entrada única da plataforma. A conta é global (seção 12). Não há tenant escolhido antes do login.
2. Aplica atraso progressivo por identificador e limite por IP (ver seção 6). Não bloqueia a conta.
3. Verifica senha com Argon2id (pepper quando ativo, ver [05](../../../docs/v2/05-seguranca.md), seção 2).
4. Se MFA é exigida pela política, pede segundo fator.
5. Cria sessão opaca no servidor. Regenera o ID de sessão.
6. Grava evento de login (sucesso ou falha) em auditoria, sem a senha.

Mensagem de falha é sempre a mesma para identificador inexistente e senha errada.

### 13.5 [06](../../../docs/v2/06-identidade-acesso.md), seção 5

#### 5. MFA

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

### 13.6 [06](../../../docs/v2/06-identidade-acesso.md), seção 7

#### 7. Sessão

| Controle | Valor |
|---|---|
| Idle | 30 min |
| Absoluta | 12 h (usuário); 4 h (conta de plataforma) |
| Sessões simultâneas | 3 por usuário; a mais antiga é encerrada |
| Vínculo | **Token de dispositivo (D-03, decidida):** cookie `__Host-` com ID aleatório de 256 bits, registrado em `DeviceTrust` e revogável pelo usuário e pelo administrador. A sessão só é aceita com token de dispositivo válido. Login em dispositivo novo exige MFA e notifica o usuário. Mudança de User-Agent ou de IP gera sinal de risco e step-up, sem bloqueio automático por IP (ACH-09). |
| Cookie | `__Host-` prefixo, `HttpOnly`, `Secure`, `SameSite=Lax` |
| Logout | Revoga a sessão atual; "sair de todos" revoga todas |
| Evento | Criação, rotação, término e revogação registrados em `UserSessionEvent` |

### 13.7 [06](../../../docs/v2/06-identidade-acesso.md), seção 9

#### 9. Autorização (RBAC com contexto)

- Permissão: `modulo.recurso.acao`, por exemplo `academico.nota.lancar`.
- Papéis são coleções de permissões. Permissões não são atribuídas diretamente ao usuário sem papel, exceto por exceção registrada com prazo.
- Escopo: tenant (obrigatório), unidade (quando aplicável), recurso (relação com o recurso, como turma do professor).
- Negação explícita tem precedência sobre concessão.
- Toda concessão e revogação de papel gera auditoria com justificativa obrigatória para papéis administrativos.
- Revisão de acesso: trimestral para papéis administrativos e de plataforma; anual para os demais.
