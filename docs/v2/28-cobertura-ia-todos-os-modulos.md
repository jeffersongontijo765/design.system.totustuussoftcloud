# 28 — Cobertura de IA em Todos os Módulos

> Parte do [SDD v2](00-README.md). Regras gerais, contratação e governança de IA em [27](27-inteligencia-artificial-e-portais.md). Catálogo de módulos em [12](12-catalogo-modulos.md). Regras de validação em [17](17-regras-modulos.md), [18](18-regras-modulos-2.md) e [19](19-regras-modulos-3.md).
> **Objetivo:** todo módulo do catálogo tem uma posição de IA, mesmo quando a posição é "não". A [27](27-inteligencia-artificial-e-portais.md), seções 5 e 6, detalha os módulos de maior uso. Esta seção fecha a cobertura.

---

## 1. Legenda

| Posição | Significado |
|---|---|
| **Sim** | Recurso completo, com revisão humana onde há decisão |
| **Restrita** | Recurso parcial. A IA apenas sugere. Nenhuma ação é executada por ela. |
| **Não** | A IA não entra no módulo, pelo motivo indicado |

Regras comuns:

1. IA não executa ação destrutiva, de pagamento, de publicação ou de bloqueio sem confirmação humana.
2. IA não decide sobre direito, nota, matrícula, crédito, emprego ou saúde. Quando sugere, o registro mostra quem decidiu.
3. Módulos marcados como **Não** não recebem chamada ao gateway de IA. Essa regra é testada.
4. Todo recurso `ai.*` segue a contratação e os testes da [27](27-inteligencia-artificial-e-portais.md), seções 3 e 9.

---

## 2. Cobertura por módulo

| Módulo do catálogo | Posição | Recurso (capacidade) | Limite e decisão humana |
|---|---|---|---|
| Acadêmico | Sim | `ai.academico`: planos, resumos, dúvidas, questões | Nota, aprovação e decisão disciplinar são humanas ([27](27-inteligencia-artificial-e-portais.md), seção 5.1) |
| Armazenamento (arquivos e busca) | Sim | `ai.documentos`: busca semântica, OCR assistido | Não expõe texto de bucket sensível fora do escopo ([21](21-busca-e-armazenamento.md)) |
| Auditoria | Sim | `ai.auditoria`: linha do tempo, consulta em linguagem natural | Não encerra incidente. Não retorna dado fora do escopo do auditor. |
| Autenticação | Restrita | Sinal de risco de login, sem bloqueio | Bloqueio é regra determinística ([06](06-identidade-acesso.md)). IA apenas registra sinal para análise. |
| Bancos (extratos) | Restrita | Classificação de lançamento de extrato | Não movimenta conta. Conciliação exige confirmação humana. |
| Biblioteca acadêmica | Sim | `ai.operacao`: recomendação de leitura | Não usa dado pessoal sensível. Não aplica multa. |
| Billing e cobrança | Sim | `ai.financeiro`: explicação de fatura, renegociação | Não decide cobrança, negativação nem bloqueio ([27](27-inteligencia-artificial-e-portais.md), seção 5.2) |
| Chat rápido e SAC | Sim | `ai.chat`: captação e atendimento com fonte | Fora da fonte, vai para humano (D-18, [22](22-crm-canais-e-papeis.md)) |
| Client migration | Restrita | `ai.plataforma.migracao`: sugestão de mapeamento de colunas | Não grava dado. Mapeamento é validado por pessoa. Credencial de origem não é enviada ao modelo. |
| Contábil e fiscal | Restrita | `ai.financeiro`: sugestão de classificação contábil e de inconsistência | Não apura tributo, não fecha período e não emite nota. Contador decide. |
| Contratos | Sim | `ai.contratos`: análise de cláusulas e prazos | Não emite parecer jurídico ([27](27-inteligencia-artificial-e-portais.md), seção 5.5) |
| Cookies e sessões | Não | — | Controle de sessão e de cookie é determinístico e de segurança. IA não participa. |
| CRM | Sim | `ai.crm` e `ai.chat` | Não envia mensagem sem aprovação ([27](27-inteligencia-artificial-e-portais.md), seção 5.6) |
| Documentos | Sim | `ai.documentos` | Não responde sobre documento de outro titular |
| Financeiro | Sim | `ai.financeiro` | Ver [27](27-inteligencia-artificial-e-portais.md), seção 5.2 |
| Frotas | Restrita | `ai.operacao`: previsão de manutenção, sugestão de rota | Regra de CNH vencida e de conflito de horário é determinística. IA não bloqueia motorista. |
| Governança de integrações | Sim | `ai.platform.ops`: diagnóstico de falha de integração | Não altera credencial nem reenvia evento sem ação humana ([16](16-integracoes-externas.md)) |
| Interface de biblioteca (UI) | Não | — | Componente visual. Não há decisão a apoiar. |
| Layout de tickets | Restrita | Sugestão de campos a partir do tipo de chamado | Campos obrigatórios seguem a regra cadastrada |
| Logger | Restrita | `ai.platform.ops`: agrupamento de erros, causa provável | Não altera configuração nem reinicia serviço |
| Marketing e redes sociais | Sim | `ai.marketing` | Não publica. Não envia a lead sem consentimento ([27](27-inteligencia-artificial-e-portais.md), seção 5.9) |
| Notificações | Restrita | Redação de mensagem | Não decide envio. Regra de consentimento e de horário é determinística. |
| Pessoas (HCM) | Sim | `ai.rh`, com apoio a ponto e folha | Não altera folha. Inconsistência de ponto é sugestão ao RH ([27](27-inteligencia-artificial-e-portais.md), seção 5.3) |
| Privacidade global | Restrita | `ai.auditoria`: classificação de dado pessoal em texto, rascunho de resposta ao titular | DPO decide e envia. Não confirma exclusão de dado. |
| Recursos humanos | Sim | `ai.rh` | Ver [27](27-inteligencia-artificial-e-portais.md), seção 5.3 |
| Segurança e medicina do trabalho | Sim | `ai.smt` | Não faz diagnóstico nem parecer de aptidão ([27](27-inteligencia-artificial-e-portais.md), seção 5.4) |
| Simulados com IA | Sim | `ai.simulados` | Questão exige revisão de professor. Nota final é humana. |
| Soft delete | Não | — | Exclusão e expurgo são ações destrutivas. IA não executa nem sugere exclusão automática. |
| Suprimentos | Sim | `ai.suprimentos` | Não adjudica fornecedor nem emite pedido ([27](27-inteligencia-artificial-e-portais.md), seção 5.5) |
| TI e ITSM | Sim | `ai.helpdesk` e `ai.platform.ops` | Não fecha chamado nem altera ambiente |
| Build e SLSA | Restrita | Explicação de falha de build | Não aprova release |
| Penetration test | Restrita | `ai.platform.seguranca`: triagem de achados | Severidade final e divulgação são do responsável de segurança |
| Ensino (arquitetura SaaS) | Não | — | Documento de arquitetura. Não é módulo de uso. |
| Idiomas e seletor de locale | Sim | `ai.platform.traducao`: tradução assistida de chaves | Tradução entra como pendente e só é publicada após revisão nativa ([09](09-internacionalizacao.md)) |
| Chart builder | Sim | Sugestão de gráfico a partir da pergunta | Usuário escolhe e salva |
| Reunião global | Sim | Ata e resumo de reunião | Não registra decisão como fato sem confirmação |
| Tarefas | Sim | Sugestão de prioridade e de responsável | Gestor confirma |
| Sidebar e navegação | Restrita | Assistente de navegação: encontra a tela pelo nome | Só leva a telas que o usuário tem permissão de abrir |
| Patrimônio | Sim | `ai.operacao` | Depreciação é cálculo do sistema, não da IA ([19](19-regras-modulos-3.md), seção 8) |
| Preceptoria e autoavaliação | Restrita | Resumo agregado de autoavaliação | Não avalia pessoa. Resumo só com número mínimo de respondentes. |
| Helpdesk | Sim | `ai.helpdesk` | Ver [27](27-inteligencia-artificial-e-portais.md), seção 5.7 |
| Jurídico (apoio) | Restrita | Pesquisa de norma e revisão de contrato | Não emite parecer. Qualquer uso exige advogado habilitado ([26](26-sdd-juridico-regulatorio.md)) |
| Portal do aluno, professor, pais e terceiros | Sim | Assistente de consulta e de tarefa, dentro da permissão do portal | Não mostra dado de outro titular. Não decide nota, cobrança ou acesso. |

---

## 3. Resumo da cobertura

| Posição | Quantidade de módulos |
|---|---|
| Sim | 25 |
| Restrita | 14 |
| Não | 4 |

Os quatro módulos sem IA são cookies e sessões, interface de biblioteca, soft delete e arquitetura de ensino. Não são lacunas: a ausência é uma decisão de segurança ou de escopo.

---

## 4. Critérios de aceite

- [ ] Todo módulo do catálogo ([12](12-catalogo-modulos.md)) aparece nesta tabela com posição definida.
- [ ] Módulos marcados como **Não** não chamam o gateway de IA (teste automatizado).
- [ ] Cada recurso `ai.*` tem chave de capacidade, quota e limite registrados.
- [ ] Cada recurso **Restrito** tem registro de que nenhuma ação é executada pela IA.

---

## 5. Cobertura de IA dos módulos adicionados em 03/11/2026

| Módulo | Uso de IA | Regra |
|---|---|---|
| Aulas online ([40](40-aulas-online-por-portal.md)) | Transcrição de aula, **decidido: sim**, pelo gateway | Só com gravação permitida e consentimento. Desligada por padrão |
| Formulários ([41](41-formularios-e-pesquisas.md)) | Não usa IA | Nenhum conteúdo de formulário é enviado a modelo |
| Preceptoria ([42](42-preceptoria-por-portal.md)) | Não usa IA | Avaliação e tutoria não são enviadas a modelo |
| Gestão pastoral ([43](43-pastoral-por-portal.md)) | Não usa IA | Anotação de acompanhamento e intenção não são enviadas a modelo |
| Agendamento ([44](44-agendamento-ambientes-equipamentos.md)) | Não usa IA | Sem uso |
| Matrícula ([46](46-matricula-e-rematricula-por-portal.md)) | Não usa IA | Sem uso |
| Simulados ([47](47-simulados-por-portal.md)) | **Sim**: correção de redação e nota sugerida | Nota só vale depois de confirmada pelo professor (MOD-06). Texto sem nome do aluno |
| Gerador de documentos ([48](48-gerador-de-documentos-por-portal.md)) | Não usa IA | Sem uso |
| Logs e testes ([49](49-logs-testes-por-portal.md)) | Não usa IA | Logs não levam conteúdo a modelo |
| Medicina do trabalho ([52](52-medicina-do-trabalho-especificacao.md)) | Não usa IA | Dado de saúde não sai do sistema ([27](27-inteligencia-artificial-e-portais.md)) |

Regra de [28](28-cobertura-ia-todos-os-modulos.md), item 3: módulos marcados como "Não" não recebem chamada ao gateway de IA. Essa regra é testada.
