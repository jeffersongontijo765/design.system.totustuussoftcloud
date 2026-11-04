# 78 — Permissões, papéis e níveis de acesso por portal

> Parte do [SDD v2](00-README.md). Estende [06](06-identidade-acesso.md), seção 9 (RBAC com contexto) e a seção 10 (contas de plataforma). Escopo de portais em [23](23-dominios-provisionamento-ciclo-de-vida.md) e [31](31-matriz-portais-modulos.md).
> **Status:** aprovado pelo autor em 04/11/2026 (L-02, P-01, D-30 a D-33 e D-38 a D-41). Não há proposta em aberto neste documento.

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

## 7. Critérios de aceite

- [ ] Somente `platform.developer` cria entidade e unidade, na tela e na API.
- [ ] Todo papel tem nível, escopo e lista de permissões.
- [ ] Papel de um portal não concede acesso a outro portal.
- [ ] Separação de funções aplicada nas ações da tabela 2.2.
- [ ] Revisão trimestral para níveis 3 e acima e para a plataforma; anual para os demais.
- [ ] Permissão validada no servidor, com teste de acesso negado por papel e por escopo.
