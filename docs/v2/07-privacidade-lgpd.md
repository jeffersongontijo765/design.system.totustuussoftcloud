# 07 — Privacidade e LGPD

> Parte do [SDD v2](00-README.md). Este documento é técnico. Não substitui parecer jurídico. Pontos marcados **(jurídico)** precisam de confirmação antes do go-live.

---

## 1. Compromissos

1. Coletar apenas o dado necessário para uma finalidade declarada.
2. Informar o titular antes da coleta, em linguagem simples.
3. Responder às solicitações de direitos dentro do prazo legal.
4. Apagar ou anonimizar quando a finalidade acaba e não há obrigação legal de guarda.
5. Tratar dados de crianças e adolescentes com o melhor interesse, consentimento parental quando exigido e minimização reforçada. (Ecossistema educacional: **(jurídico)** confirmar bases por tipo de dado.)

## 2. Inventário de dados

Cada tabela com dado pessoal tem, no registro de dados (ROPA), os campos: finalidade, base legal, categoria do titular, categoria do dado, operador, prazo de retenção e medida de segurança.

| Categoria | Exemplos | Sensibilidade |
|---|---|---|
| Identificação | Nome, e-mail, telefone, documento (CPF, RG) | Alta. Documento de identificação tem acesso restrito por política; não é dado sensível no sentido do art. 5º, II, LGPD. |
| Família | Responsáveis, parentesco | Alta (menores) |
| Acadêmico | Notas, frequência, histórico | Média |
| Saúde | Laudos, deficiência, alergias | **Sensível** (art. 11 LGPD) |
| Financeiro | Cobrança, dados bancários | Alta |
| Acesso | Logs de sessão, IP, User-Agent | Média |

## 3. Bases legais

Matriz de base legal por finalidade. Status: **proposta, pendente de parecer jurídico**. Nenhuma linha é válida para produção antes da confirmação. Citações de artigos referem-se à LGPD (Lei 13.709/2018).

| Finalidade | Dado | Base proposta | Legislação setorial a confirmar | Confirmação |
|---|---|---|---|---|
| Matrícula e vínculo acadêmico | Identificação, responsáveis | Execução de contrato ou procedimentos preliminares (art. 7º, V); obrigação legal (art. 7º, II) | Normas de educação e de registro escolar | **(jurídico)** |
| Cobrança de mensalidades | Identificação, financeiro | Execução de contrato (art. 7º, V); exercício regular de direitos (art. 7º, VI) | Código de Defesa do Consumidor, quanto a cobrança e negativação | **(jurídico)** |
| Recursos humanos e folha | Identificação, salário, documentos trabalhistas | Obrigação legal (art. 7º, II) | CLT e normas do eSocial | **(jurídico)** |
| Segurança e medicina do trabalho | Dado de saúde ocupacional | Tutela da saúde (art. 11, II, f) ou obrigação legal (art. 11, II, a) | NRs do Ministério do Trabalho e Emprego | **(jurídico)** |
| Marketing | Contato | Consentimento (art. 7º, I), com revogação simples | Regras de envio de mensagens | **(jurídico)** |
| Segurança e logs | Acesso, IP, registro de ações | Legítimo interesse (art. 7º, IX), com teste de balanceamento documentado | Normas de segurança da informação | **(jurídico)** |
| Consulta por CPF ([21](21-busca-e-armazenamento.md), seção 6.8) | Identificação | Mesma base da finalidade declarada pelo tenant, sem base própria | Conforme a finalidade | **(jurídico)** |

**Escopo de legislação:** esta matriz cobre a legislação brasileira. Não afirma conformidade com outras jurisdições. A plataforma só atende outro país após revisão específica (lacuna LAC-15 em [19](19-regras-modulos-3.md)). "Atender toda a legislação" não é uma condição que este SDD possa certificar: é tarefa contínua do jurídico, com revisão a cada mudança normativa.

## 4. Direitos do titular

| Direito | Entrega | Prazo de referência |
|---|---|---|
| Confirmação e acesso | Exportação em formato legível e portável | 15 dias (art. 19 LGPD) |
| Correção | Edição com trilha de auditoria | Imediato quando possível |
| Anonimização, bloqueio ou eliminação | Processo de retenção | Conforme política e prazos legais |
| Portabilidade | JSON ou CSV | 15 dias |
| Revogação de consentimento | Efeito imediato nas finalidades dependentes | Imediato |
| Informação sobre compartilhamento | Lista de operadores e terceiros | 15 dias |

- Solicitação gera protocolo, registro e resposta por canal verificado.
- Exportação de dados pessoais exige step-up de autenticação (ver [06](06-identidade-acesso.md)).
- Fluxo de pedido de titular para o responsável legal de menor segue a mesma regra, com verificação de vínculo.

## 5. Retenção

- Prazo por categoria definido pela plataforma. A entidade pode reduzir, não estender além do que a lei permite. **(jurídico)** confirmar prazos de guarda de documentos escolares.
- Job diário de expurgo com relatório. Eliminação física registra data e tipo, sem guardar o dado eliminado.
- Backups seguem a mesma regra: retenção de backup é limitada e documentada, e restauração de backup reaplica expurgos já executados.

## 6. Minimização nos logs

- Sem senha, token, cookie, CPF, dado de saúde ou corpo completo de requisição em log.
- E-mail e telefone mascarados (`j***@d***.com`).
- Logs de auditoria mantêm identificador interno do ator, não o nome.

## 7. Transferência e operadores

- Lista de operadores (provedores de e-mail, SMS, pagamento, nuvem) com contrato de tratamento de dados.
- Transferência internacional só para países com nível adequado ou com cláusulas-padrão. **(jurídico)**
- Integrações enviam somente os campos necessários ao contrato com o terceiro.

## 8. Incidentes e comunicação à ANPD

A v1 cita prazo de **72 horas**. A v2 corrige para o texto vigente: a Resolução CD/ANPD nº 15/2024 fixa o prazo de comunicação de incidente com risco ou dano relevante em **três dias úteis** a partir do conhecimento do incidente, e o art. 48 da LGPD exige comunicação ao titular. **(jurídico)** confirmar o prazo vigente antes de publicar o runbook.

Passos do runbook:

1. Conter e preservar evidências (sem alterar logs).
2. Avaliar: tipo de dado, volume de titulares, risco aos direitos, medidas aplicadas.
3. Comunicar internamente conforme severidade ([05](05-seguranca.md), seção 6).
4. Comunicar à ANPD e aos titulares quando houver risco ou dano relevante, com conteúdo do modelo oficial.
5. Registrar o incidente, causa, ações e lições aprendidas.

## 9. Métricas de privacidade

| Métrica | Meta |
|---|---|
| Pedidos de titular atendidos no prazo | 100% |
| Dados com retenção vencida e não expurgados | 0 |
| Campos sensíveis em log (varredura) | 0 |
| Operadores sem contrato de tratamento | 0 |

## 10. Lacunas

Itens que a v1 listava como lacuna e que continuam abertos: ROPA completo por tabela, parecer de legítimo interesse, prazos de retenção aprovados, fluxo de consentimento para menores. Cada um tem dono e prazo no [backlog](11-governanca-qualidade.md).
