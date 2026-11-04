# 24 — Operação, Continuidade, Qualidade e Lacunas do Projeto

> Parte do [SDD v2](00-README.md). Segurança geral em [05](05-seguranca.md). Implantação em [10](10-implantacao-operacao.md). Governança e Definition of Done em [11](11-governanca-qualidade.md). Domínios e ciclo de vida em [23](23-dominios-provisionamento-ciclo-de-vida.md).
> **Status:** proposta. Metas numéricas são valores iniciais para medir e ajustar em homologação, não garantias contratuais. Os valores de contrato dependem do autor.

---

## 1. Continuidade: backup e recuperação

Como cada unidade tem banco próprio ([03](03-dominio-tenancy.md), seção 1.1), a recuperação é feita unidade por unidade. Uma falha em uma unidade não exige restaurar as demais.

| Banco | RPO (perda máxima de dado) | RTO (tempo para voltar) | Retenção |
|---|---|---|---|
| Master | 15 min | 2 h | 35 dias de ponto de restauração; mensal por 12 meses |
| Banco de unidade | 15 min | 4 h | Mesma regra; cópia completa diária |
| Banco de identidade da entidade (D-19) | 15 min | 2 h | Mesma regra do master, com backup separado |
| Arquivos (armazenamento de objetos) | Versionamento habilitado, sem perda por substituição | 4 h | Conforme retenção de [21](21-busca-e-armazenamento.md) |
| Índice de busca | Reconstruível a partir do banco e dos arquivos | 24 h | Não é backup; é derivado |

Regras:

1. Backup é criptografado. A chave de backup fica fora do servidor de dados ([05](05-seguranca.md), seção 2).
2. Restauração de teste mensal, em ambiente isolado, com registro do tempo e do resultado. Falha de restauração é incidente.
3. Backup de cada banco de unidade é independente. Uma restauração de teste escolhe uma unidade ao acaso a cada mês.
4. Região secundária para o master e para os bancos de identidade. Falha da região principal aciona o plano de recuperação.
5. Expurgo por retenção ([07](07-privacidade-lgpd.md)) é aplicado também a backups quando o prazo de retenção de backup vence. O prazo de backup é **pendente** (ver [10](10-implantacao-operacao.md)).

## 2. Objetivos de serviço (SLO)

| Serviço | Meta inicial | Medição |
|---|---|---|
| Disponibilidade por entidade | 99,5% por mês | Requisições bem-sucedidas dentro do horário de atendimento da entidade |
| Login | 99,9% por mês | Autenticação concluída |
| Latência p95 de tela de lista | até 800 ms | Medição no servidor |
| Latência p95 de API | até 300 ms | Medição no servidor |
| Entrega de evento na fila | 99% em até 60 s | Tempo entre gravação na outbox e consumo |
| Envio de notificação | 99% em até 5 min | Entre enfileiramento e entrega ao provedor |

- Orçamento de erro: consumo acima de 50% do erro permitido no mês suspende novas mudanças de risco até a estabilização.
- Página de status pública para incidentes de disponibilidade.
- Alerta por entidade, não só global. Uma entidade pode estar fora enquanto as outras estão bem.

## 3. Severidade e suporte

| Severidade | Exemplo | Primeira resposta | Atualização | Solução ou contorno |
|---|---|---|---|---|
| 1 — crítica | Entidade inteira sem acesso; vazamento suspeito | 30 min, 24 × 7 | A cada 1 h | 4 h |
| 2 — alta | Módulo principal indisponível; cobrança parada | 2 h, horário comercial estendido | A cada 4 h | 1 dia útil |
| 3 — média | Função degradada, com contorno | 1 dia útil | Diária | Próxima versão |
| 4 — baixa | Dúvida, melhoria | 2 dias úteis | Sob demanda | Backlog |

- Vazamento de dado pessoal segue o runbook de [07](07-privacidade-lgpd.md), seção 8, independentemente da severidade.
- Atendimento de suporte não acessa dado de aluno sem vínculo e sem registro ([06](06-identidade-acesso.md), seção 10).

## 4. Releases e mudanças

- **Migrações compatíveis com a versão anterior** por pelo menos uma versão. Remoção de coluna em duas etapas, já definida em [15](15-validacoes.md), seção 1.
- **Feature flags por entidade.** Nova funcionalidade começa em uma entidade piloto, depois em grupo, depois em todas.
- **Canário:** a versão roda primeiro em um subconjunto de unidades. Métrica de erro acima do limite interrompe a propagação e reverte.
- **Rollback** testado em homologação a cada release de banco.
- **Janela de manutenção** comunicada às entidades com 72 h de antecedência, exceto correção de segurança.
- **Changelog por entidade**, com o que muda na tela e na API.

## 5. Estratégia de testes

| Tipo | Escopo | Quando roda | Responsável |
|---|---|---|---|
| Unidade | Regras de validação e cálculo | A cada commit | Desenvolvedor |
| Integração | Serviços com banco real de teste | A cada commit | Desenvolvedor |
| Contrato de evento | Payload de cada evento do catálogo ([14](14-integracao-modulos.md), seção 4) | A cada commit | Desenvolvedor |
| Isolamento | Matriz de entidades, unidades e papéis ([03](03-dominio-tenancy.md), seção 7) | A cada commit | Segurança |
| Ponta a ponta | Fluxos principais: matrícula, cobrança, login, troca de contexto | Antes de cada release | QA |
| Carga | Cenário de pico por entidade grande | Mensal e antes de mudança de infraestrutura | Operação |
| Segurança (DAST) | Varredura na homologação | Antes de cada release | Segurança |
| Pentest externo | Escopo definido em [penetration-test-spec-v2.md](anexo-v1/penetration-test-spec-v2.md) | Anual e após mudança de autenticação ou pagamento | Terceiro contratado |
| Restauração | Restauração de backup em ambiente isolado | Mensal (seção 1) | Operação |
| Exercício de incidente | Simulação de vazamento ou de indisponibilidade | Semestral | Segurança e DPO |

## 6. Divulgação de vulnerabilidade

- Canal público para relatório de vulnerabilidade, com endereço de contato de segurança publicado em `/.well-known/security.txt`.
- Resposta de confirmação em até 3 dias úteis. Correção de vulnerabilidade crítica em até 7 dias, alta em até 30 dias.
- Pesquisador de boa-fé não é processado por teste feito dentro do escopo publicado.
- Registro da vulnerabilidade e da correção, sem dado de cliente.

## 7. Acessibilidade e conteúdo

- Declaração de acessibilidade publicada, com o nível WCAG 2.2 AA e as pendências conhecidas.
- Teste com leitor de tela em telas principais a cada release.
- Conteúdo para o cidadão e para o aluno em linguagem simples. Textos de consentimento e de cobrança passam por revisão jurídica ([07](07-privacidade-lgpd.md)).

## 8. Contratos e termos

Documentos que a plataforma precisa ter e que não estão no SDD:

| Documento | Conteúdo mínimo | Dono |
|---|---|---|
| Termos de uso da plataforma | Responsabilidades, uso aceitável, suspensão | Jurídico |
| Contrato de cliente (entidade) | Escopo, SLA (seção 2), preço, saída ([23](23-dominios-provisionamento-ciclo-de-vida.md), seção 5) | Comercial e jurídico |
| Contrato de tratamento de dados (operador) | Quando a plataforma trata dado em nome da entidade ([07](07-privacidade-lgpd.md), seção 7) | DPO e jurídico |
| Política de privacidade (site e app) | Dados coletados por canal ([22](22-crm-canais-e-papeis.md)), finalidade e direitos | DPO |
| Política de cookies | Lista de cookies e finalidade, com consentimento | DPO |
| Política de segurança para fornecedores | Requisitos para terceiros que tocam dado de cliente ([16](16-integracoes-externas.md)) | Segurança |
| Plano de continuidade | Conteúdo da seção 1 em versão para o cliente | Operação |

## 9. Lacunas do projeto

Lista do que falta para o projeto estar completo. Cada item tem dono sugerido e prioridade.

| # | Lacuna | Prioridade | Dono sugerido | Onde |
|---|---|---|---|---|
| G-01 | Decisões D-22 a D-24: aprovadas em 02/11/2026 | Resolvido | Autor | [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 6 |
| G-02 | Retenção de 24 h da auditoria de consultas por CPF; possível conflito com o registro de acesso (Marco Civil, art. 15) e com o relatório ao titular | Alta | Jurídico e DPO | [21](21-busca-e-armazenamento.md), seção 6.8; análise em [25](25-dossie-juridico-e-lacunas.md), Q-01 |
| G-03 | Parecer da matriz de base legal | Alta | Jurídico | [07](07-privacidade-lgpd.md), seção 3; perguntas em [25](25-dossie-juridico-e-lacunas.md), Q-03 a Q-08 |
| G-04 | Piso máximo de aumento do limite de MFA por tenant | Alta | Autor | [20](20-pagamentos-seguranca.md), seção 19.2 |
| G-05 | Relatório de impacto (RIPD) da busca por CPF e do cadastro civil | Alta | DPO | [21](21-busca-e-armazenamento.md), [14](14-integracao-modulos.md) |
| G-06 | DDL de Documentos, Marketing, Atendimento, Simulados, Preceptoria, RH e Contábil/Fiscal | Alta | Owners dos módulos | [19](19-regras-modulos-3.md), [18](18-regras-modulos-2.md) |
| G-07 | Regras de validação de Pessoas, Acadêmico, Financeiro e demais módulos em nível campo a campo | Alta | Owners | [17](17-regras-modulos.md), [18](18-regras-modulos-2.md), [19](19-regras-modulos-3.md) |
| G-08 | Fronteira Armazenamento/Suprimentos (estoque duplicado) | Média | Produto | [19](19-regras-modulos-3.md), seção 2 |
| G-09 | Fronteira RH/Pessoas (HCM único ou dois módulos) | Média | Produto | [18](18-regras-modulos-2.md), seção 4.1 |
| G-10 | Módulo de atendimento único (SAC, chat e helpdesk) | Média | Produto | [19](19-regras-modulos-3.md), seção 7 |
| G-11 | Motor do OCR e ADR correspondente | Média | Responsável técnico | [21](21-busca-e-armazenamento.md), seção 3.10 |
| G-12 | Prazo de retenção de backups | Média | Jurídico e operação | Seção 1 |
| G-13 | Prazo de guarda para retenção legal na saída de cliente | Média | Jurídico | [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 5 |
| G-14 | Contrato de cliente, termos de uso, política de privacidade e de cookies, com revisão jurídica | Média | Jurídico | Seção 8 |
| G-15 | Metas de SLO e SLA de contrato, validadas em homologação | Média | Autor e operação | Seção 2 |
| G-16 | Matriz de isolamento automatizada para todas as entidades e papéis | Média | Segurança | [03](03-dominio-tenancy.md), seção 7 |
| G-17 | Plano de continuidade para o cliente | Baixa | Operação | Seção 1 |
| G-18 | Declaração de acessibilidade e teste com leitor de tela | Baixa | Frontend | Seção 7 |
| G-19 | Lista de jurisdições fora do Brasil, se houver cliente | Baixa | Jurídico | [19](19-regras-modulos-3.md), seção 4 |
| G-20 | Revisão de todas as regras marcadas **[Pendente]** nesta versão | Média | Owners | Todos os documentos 14 a 24 |

## 10. Critérios de aceite deste documento

- [ ] Metas de SLO, RPO e RTO aprovadas pelo autor.
- [ ] Restauração mensal executada e registrada em homologação.
- [ ] Estratégia de testes implantada em CI.
- [ ] Contratos da seção 8 revisados pelo jurídico.
- [ ] Lacunas G-01 a G-05 resolvidas antes de produção.
