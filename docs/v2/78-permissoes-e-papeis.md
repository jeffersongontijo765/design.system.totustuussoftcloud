# 78 — Permissões, papéis e níveis de acesso por portal

> Parte do [SDD v2](00-README.md). Estende [06](06-identidade-acesso.md), seção 9 (RBAC com contexto) e a seção 10 (contas de plataforma). Escopo de portais em [23](23-dominios-provisionamento-ciclo-de-vida.md) e [31](31-matriz-portais-modulos.md).
> **Status:** aprovado pelo autor em 04/11/2026 (L-02, P-01, D-30 a D-33 e D-38 a D-43); D-44 e D-45 já estavam definidas nos documentos 31 e 22. Não há proposta em aberto neste documento.

---

## 1. Regras aprovadas pelo autor

| # | Regra | Origem |
|---|---|---|
| L-02 | Criar entidade e criar unidade é **exclusivo do papel `platform.developer`**. | Autor, 04/11/2026 |
| P-01 | O sistema de permissões é completo: papéis em níveis, com escopo, para todos os portais. | Autor, 04/11/2026 |

## 2. Modelo

- **Permissão:** `modulo.recurso.acao` (ex.: `academico.nota.lancar`), como em [06](06-identidade-acesso.md), seção 9.
- **Papel:** coleção de permissões, com **nível** e **escopo**.
- **Escopo:** `plataforma`, `entidade`, `unidade`, `turma` (para docentes), `proprio` (somente o próprio registro). Escopo mais estreito nunca amplia o papel.
- **Vínculo:** uma pessoa tem um ou mais vínculos (entidade, unidade, papel). Permissão efetiva é a união dos vínculos ativos, menos as negações.
- **Negação explícita** vence concessão ([06](06-identidade-acesso.md), seção 9).

### 2.1 Níveis de papel (D-38, aprovada)

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
- Papéis de nível 3 e acima, e todos os da plataforma, exigem **justificativa** e **revisão trimestral** ([06](06-identidade-acesso.md), seção 9).
- Papéis de nível 0 a 2 têm revisão anual.

### 2.2 Separação de funções (D-39, aprovada)

| Ação | Não pode ser feita pela mesma pessoa |
|---|---|
| Criar e aprovar mudança no Editor de portais: quem edita é `platform.builder` e quem aprova é `platform.developer` (D-33) | Sim ([23](23-dominios-provisionamento-ciclo-de-vida.md), seção 3) |
| Lançar nota e aprovar a nota | Sim |
| Cadastrar fornecedor e aprovar pagamento | Sim |
| Criar usuário e conceder papel de nível 3 ou acima | Sim |
| Criar plano e aplicar plano a entidade | Sim |

## 3. Criação de entidade e unidade (L-02)

| Ação | Papel exigido | Verificação |
|---|---|---|
| Criar entidade | `platform.developer` | Passkey e sessão curta ([06](06-identidade-acesso.md), seção 10) |
| Criar unidade | `platform.developer` | Idem |
| Editar dados de entidade ou unidade já criadas | Administrador da entidade (nível 4), exceto código e domínio, que são do desenvolvedor | Auditoria |
| Desativar ou encerrar entidade | `platform.developer`, por saída de cliente ([23](23-dominios-provisionamento-ciclo-de-vida.md), seção 5) | Confirmação digitando o nome |

Nenhum outro papel, inclusive de plataforma, cria ou remove entidade ou unidade. A regra vale também para API ([04](04-api.md)): o endpoint de criação exige o papel no servidor, não só na tela.

## 4. Papéis por portal

Papéis listados por portal, com o nível máximo previsto. Permissões detalhadas por módulo são definidas em cada ficha de módulo.

### 4.1 Portal do Desenvolvedor (plataforma)

| Papel | Nível | Escopo | Pode |
|---|---|---|---|
| `platform.developer` | 7 | plataforma | Criar entidade e unidade; planos, limites, licenças, Editor de portais |
| `platform.manager` | 6 | plataforma | Clientes, assinaturas, faturamento de clientes, domínios; sem criar entidade ou unidade |
| `platform.operator` | 5 | plataforma | Suporte e atendimento; consulta de cliente com motivo registrado |
| `platform.builder` | 7 | plataforma | Editor de portais, com passkey e sessão curta (mantido de [06](06-identidade-acesso.md), seção 9) |
| `platform.auditor` | 2 | plataforma | Leitura de auditoria e relatórios de conformidade |
| `platform.sales.sdr` | 1 | plataforma (leads) | Pré-vendas: qualificar, agendar demonstração, registrar interação (SDD 22, seção 4.1) |
| `platform.sales.ae` | 1 | plataforma (carteira própria) | Vendedor: criar proposta e avançar o funil até negociação (SDD 22, seção 4.1) |
| `platform.sales.manager` | 2 | plataforma (equipe comercial) | Gerente comercial: atribuir leads, aprovar desconto na alçada, ver funil da equipe (SDD 22, seção 4.1) |
| `platform.chatbot.operator` | 1 | plataforma (fila de conversas) | Atender, transferir e registrar conversas dos canais (SDD 22, seção 4.1) |
| `platform.customer_success` | 1 | plataforma (clientes ativos) | Acompanhar implantação e uso, sem alterar cobrança (SDD 22, seção 4.1) |
| `platform.finance` | 1 | plataforma (financeiro da empresa) | Papel **Financeiro** do [22](22-crm-canais-e-papeis.md), seção 5, na empresa desenvolvedora: operar contas, despesas, pagamentos e conciliação (D-43) |
| `platform.finance.manager` | 2 | plataforma (financeiro da empresa) | Aprovar despesas e orçamento; segundo aprovador acima de R$ 10.000 (D-43, aprovada) |
| `platform.accounting` | 1 | plataforma (contábil da empresa) | Papel **Contábil** do [22](22-crm-canais-e-papeis.md), seção 5: lançar, fechar período, exportar; não fecha período com lançamento que criou sem revisão (D-45) |
| `platform.fiscal` | 1 | plataforma (fiscal da empresa) | Papel **Fiscal** do [22](22-crm-canais-e-papeis.md), seção 5: emitir e cancelar NFS-e, apurar tributos; cancelamento exige aprovação do contábil (D-45) |
| `platform.assets` | 1 | plataforma (patrimônio da empresa) | Cadastrar e movimentar bens; manutenção, inventário e seguro (DP-03, [80](80-decisoes-por-padrao.md)) |
| `platform.assets.approver` | 2 | plataforma (patrimônio da empresa) | Aprovar transferência, descarte e manutenção acima do limite; não aprova o que registrou (DP-03) |
| `platform.fleet` | 1 | plataforma (frotas da empresa) | Veículos, motoristas, reservas, abastecimentos, viagens, multas e documentos (DP-03) |
| `platform.fleet.approver` | 2 | plataforma (frotas da empresa) | Aprovar reservas e ordens de manutenção; não aprova a própria reserva (DP-03) |
| `platform.purchasing` | 1 | plataforma (suprimentos da empresa) | Papel **Compras** do [22](22-crm-canais-e-papeis.md), seção 5: cotação, pedido, cadastro de fornecedor |
| `platform.warehouse` | 1 | plataforma (suprimentos da empresa) | Papel **Almoxarifado** do [22](22-crm-canais-e-papeis.md), seção 5: recebimento e movimento |
| `platform.purchasing.approver` | 2 | plataforma (suprimentos da empresa) | Papel **Aprovador de compras** do [22](22-crm-canais-e-papeis.md), seção 5: aprova requisição na alçada; não é o solicitante |
| `platform.people` | 1 | plataforma (HCM da empresa) | Pessoas (DP): cadastro funcional, férias, afastamentos, ponto com motivo, rescisão, benefícios ([39](39-departamento-pessoal-rh-medicina-por-portal.md), HCM-01 e HCM-10) |
| `platform.payroll` | 1 | plataforma (HCM da empresa) | Papel **Folha** do [22](22-crm-canais-e-papeis.md), seção 5: processar a folha; folha fechada não muda |
| `platform.payroll.approver` | 2 | plataforma (HCM da empresa) | Aprovar a folha; quem processa não aprova ([39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 7) |
| `platform.hr` | 1 | plataforma (HCM da empresa) | Papel **RH** do [22](22-crm-canais-e-papeis.md), seção 5, no escopo do HCM-01: recrutamento, onboarding, avaliação, clima, treinamento |
| `platform.sst.doctor` | 1 | plataforma (SST da empresa) | Médico do trabalho: ASO completo, prontuário, CID ([39](39-departamento-pessoal-rh-medicina-por-portal.md), HCM-06) |
| `platform.sst.technician` | 1 | plataforma (SST da empresa) | Técnico de SESMT: ocorrências, EPI, NR, PGR, CAT, sem diagnóstico ([39](39-departamento-pessoal-rh-medicina-por-portal.md), HCM-06) |
| `platform.security` | 5 | plataforma (segurança) | Papel **Segurança** do [22](22-crm-canais-e-papeis.md), seção 5: investigar, bloquear conta, política de MFA, autorizar visualização de segredo de tenant com motivo; não concede permissão a si mesmo |
| `platform.dpo` | 5 | plataforma (privacidade) | Papel **Encarregado** do [22](22-crm-canais-e-papeis.md), seção 5: relatório de impacto, pedidos de titular, ROPA, incidentes, painel do DPO (LGPD-07); não opera o módulo que audita |
| `platform.ops` | 5 | plataforma (infraestrutura) | Papel **TI / Operação** do [22](22-crm-canais-e-papeis.md), seção 5: serviços, filas, backup, certificados, inventário de bancos, pedido de restauração e de acesso de emergência ([34](34-pagamentos-fiscal-bancos-por-portal.md), seção 4); sem acesso a dado pessoal de entidade |
| `platform.integration` | 6 | plataforma (integrações) | Configurar integrações de plataforma (`plataforma.integracao.*`, [16](16-integracoes-externas.md), seção 1); nunca vê segredo de tenant em texto claro |

Aprovação técnica: migração em lote, restauração de backup e escrita em acesso de emergência exigem aprovação de `platform.developer` como segundo papel, por pessoa diferente de quem pediu ([34](34-pagamentos-fiscal-bancos-por-portal.md), seção 4).

### 4.2 Portal de Gestão (SaaS da entidade)

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

### 4.3 Portal do Professor

| Papel | Nível | Escopo | Pode |
|---|---|---|---|
| `teacher` | 1 | turma | Diário, materiais e avaliações **das próprias turmas**; nota só pelo docente da turma |
| `teacher.coordinator` | 2 | unidade | Aprova plano de aula e lançamentos de tarefa de nível 1 da unidade |

### 4.4 Portal do Aluno

| Papel | Nível | Escopo | Pode |
|---|---|---|---|
| `student` | 0 | proprio | Ver e usar apenas os próprios dados: boletim, materiais, financeiro, protocolos |

### 4.5 Portal dos Responsáveis

| Papel | Nível | Escopo | Pode |
|---|---|---|---|
| `guardian` | 0 | proprio (dependentes vinculados) | Ver e atuar pelos dependentes vinculados; dependente sem vínculo não aparece |

### 4.6 Portal de Terceiros

| Papel | Nível | Escopo | Pode |
|---|---|---|---|
| `thirdparty` | 0 | proprio (contrato vinculado) | Ver contratos, entregas, faturas e solicitações da própria organização |
| `thirdparty.manager` | 1 | entidade (contrato) | Gestão de entregas e faturas do contrato vinculado |

## 5. Regras transversais (D-40, aprovada)

1. **Default-deny:** rota ou ação sem papel explícito é negada, como em [03](03-dominio-tenancy.md).
2. **Escopo verificado no servidor:** o escopo `turma`, `unidade` ou `proprio` é conferido em cada consulta, não só na tela.
3. **Papel por portal:** papel de um portal não dá acesso a outro, mesmo com a mesma conta ([23](23-dominios-provisionamento-ciclo-de-vida.md), seção 2).
4. **Ações sensíveis com step-up:** exportação, alteração de papel e exclusão exigem autenticação recente ([06](06-identidade-acesso.md), seção 5).
5. **Revisão e expiração:** vínculo temporário tem data de fim. Vínculo vencido sai sozinho e gera auditoria.
6. **Auditoria:** toda concessão, revogação e mudança de papel gera registro com justificativa para níveis 3 e acima.

## 6. Decisões pendentes

| # | Decisão | Proposta | Alternativa |
|---|---|---|---|
| D-30 | Nomes e códigos dos papéis de gestão | Os códigos da seção 4. **Aprovada pelo autor em 04/11/2026.** | Nomes livres por entidade, mapeados para os níveis |
| D-31 | Papel de professor que também coordena | Dois papéis, um por portal. **Aprovada pelo autor em 04/11/2026.** | Um papel com acúmulo de escopo |
| D-32 | Papel do responsável com mais de um aluno | Escopo `proprio` com dependentes vinculados. **Aprovada pelo autor em 04/11/2026.** | Papel por aluno |
| D-33 | Papel que aprova a publicação no Editor de portais (diferente de quem editou) | `platform.developer` aprova o que o `platform.builder` edita. **Aprovada pelo autor em 04/11/2026.** | Papel de revisão separado, criado só para isso |
| D-38 | Níveis de papel | Oito níveis, de 0 (próprio) a 7 (desenvolvedor), com as regras da seção 2.1. **Aprovada pelo autor em 04/11/2026.** | Menos níveis, por exemplo 0, 1, 3, 4 e 7 |
| D-39 | Separação de funções | As cinco ações da seção 2.2. **Aprovada pelo autor em 04/11/2026.** | Lista definida por módulo |
| D-40 | Regras transversais | As seis regras da seção 5. **Aprovada pelo autor em 04/11/2026.** | Regras definidas por portal |
| D-41 | Códigos dos papéis comerciais da plataforma (SDD 22, seção 4.1) | Os cinco códigos `platform.sales.*`, `platform.chatbot.operator` e `platform.customer_success` da seção 4.1. **Aprovada pelo autor em 04/11/2026.** | Outros nomes, mantidos os níveis |
| D-42 | Cheques e caixa físico no financeiro da plataforma ([71](71-financeiro-completo-por-portal.md), seções 5 e 6) | Não se aplicam à empresa desenvolvedora, até haver necessidade. **Aprovada pelo autor em 04/11/2026.** | Aplicam-se, como nas entidades |
| D-43 | Papéis do financeiro da plataforma | `platform.finance` (opera) e `platform.finance.manager` (aprova). **Aprovada pelo autor em 04/11/2026.** | Usar `platform.manager` para aprovar |
| D-44 | Tributos e obrigações fiscais da empresa desenvolvedora | **Já definido** na [31](31-matriz-portais-modulos.md), seção 3.3 (aprovada em 03/11/2026). Confirmado pelo autor em 04/11/2026: módulo incluído na área Contábil da plataforma | — |
| D-45 | Papéis do contábil e do fiscal da plataforma | **Já definido** no [22](22-crm-canais-e-papeis.md), seção 5 (papéis Contábil e Fiscal, com segregação). Códigos: `platform.accounting` e `platform.fiscal` | — |

## 7. Critérios de aceite

- [ ] Somente `platform.developer` cria entidade e unidade, na tela e na API.
- [ ] Todo papel tem nível, escopo e lista de permissões.
- [ ] Papel de um portal não concede acesso a outro portal.
- [ ] Separação de funções aplicada nas ações da tabela 2.2.
- [ ] Revisão trimestral para níveis 3 e acima e para a plataforma; anual para os demais.
- [ ] Permissão validada no servidor, com teste de acesso negado por papel e por escopo.
