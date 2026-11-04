# SDD v2 — TotusTuus SoftCloud

> **Versão:** 2.0.0 · **Data:** 02/11/2026 · **Status:** rascunho para revisão (aguarda aprovação do autor)
> **Substitui:** a coleção v1 (documentos `01` a `12`, `SPEC-*`, `spec_*`, `*_completo`). A v1 foi incorporada a esta pasta em `anexo-v1/`, sem alteração de conteúdo, para que a v2 seja autocontida. Índice do anexo na seção 5.
> **Método:** Elephant-Goldfish Model (EGM) — brief de conceito, rascunho com o contexto do projeto e revisão por leitores sem contexto (ver [11-governanca-qualidade.md](11-governanca-qualidade.md)).

---

## 1. Como ler este SDD

Cada requisito e afirmação de estado usa uma das etiquetas abaixo. Afirmações sem etiqueta são requisitos.

| Etiqueta | Significado |
|---|---|
| **[Verificado]** | Confirmado diretamente em código ou configuração, com caminho citado. |
| **[Declarado]** | Afirmação de estado vinda da v1 ou de auditorias externas, ainda não reproduzida neste repositório. Não deve ser usada como prova de conformidade. |
| **[Planejado]** | Ainda não implementado. Tem dono e critério de aceite. |

Regra: nenhum item sai de **[Declarado]** para **[Verificado]** sem teste, comando reproduzível ou link para o artefato de evidência.

## 2. Conteúdo

| Doc | Assunto |
|---|---|
| [01-visao-escopo.md](01-visao-escopo.md) | Produto, portais, escopo, fora de escopo, critérios de aceite |
| [02-arquitetura.md](02-arquitetura.md) | Arquitetura, camadas, ordem de middleware, ADRs, dependências |
| [03-dominio-tenancy.md](03-dominio-tenancy.md) | Modelo de domínio, hierarquia multi-tenant, isolamento |
| [04-api.md](04-api.md) | Contratos REST, autenticação de API, erros, paginação, webhooks |
| [05-seguranca.md](05-seguranca.md) | Modelo de ameaças, controles, critérios de aceite de segurança |
| [06-identidade-acesso.md](06-identidade-acesso.md) | Autenticação, MFA, sessões, RBAC, contas privilegiadas |
| [07-privacidade-lgpd.md](07-privacidade-lgpd.md) | Dados pessoais, bases legais, direitos do titular, incidentes |
| [08-frontend-design-system.md](08-frontend-design-system.md) | Frontend progressivo, CSP, design system, acessibilidade |
| [09-internacionalizacao.md](09-internacionalizacao.md) | i18n/l10n, locales, RTL |
| [10-implantacao-operacao.md](10-implantacao-operacao.md) | Ambientes, pipeline, segredos, backup, observabilidade, go-live |
| [11-governanca-qualidade.md](11-governanca-qualidade.md) | Processo de entrega, Definition of Done, gates, ADRs, revisão |
| [12-catalogo-modulos.md](12-catalogo-modulos.md) | Catálogo dos módulos funcionais e status das especificações |
| [13-achados-v1.md](13-achados-v1.md) | Registro dos problemas encontrados na v1 e como a v2 os trata |
| [14-integracao-modulos.md](14-integracao-modulos.md) | Integração entre módulos: donos de dados, eventos, outbox, contratos síncronos |
| [15-validacoes.md](15-validacoes.md) | Validações: ordem, tipos de campo, CRUD, transações, uploads, catálogo de plataforma |
| D-19 | Pessoa única entre unidades de uma entidade: cadastro civil no banco de identidade da entidade (opção a); o master guarda só conta, vínculos e índice de pessoas. Ver [14](14-integracao-modulos.md), seção 3. | **Adotada pela recomendação desta versão (02/11/2026). Mensagem anterior do autor, que colocava o cadastro civil no master, foi substituída. Confirmar.** |
| D-20 | Escopo do token: só o contexto ativo (entidade e unidade), nunca a lista de vínculos. Ver [06](06-identidade-acesso.md), seção 12.3. | **Aprovada pelo autor em 02/11/2026.** |
| D-21 | Conta global única por e-mail verificado em toda a plataforma, com vínculos. Ver [06](06-identidade-acesso.md), seção 12.6. | **Aprovada pelo autor em 02/11/2026.** |
| D-16 a D-18 | CRM: separação por banco (master para plataforma; banco de cada unidade para tenant, entidade + unidade); contas de canal oficiais da plataforma e do tenant; IA só com fonte cadastrada e opção de ticket sem IA. Ver [22](22-crm-canais-e-papeis.md), seção 9. | Decididas pelo autor em 02/11/2026. |
| [30-cache.md](30-cache.md) | Cache: camadas, chaves com entidade e unidade, classes e validade, invalidação, o que nunca é cacheado |
| [31-matriz-portais-modulos.md](31-matriz-portais-modulos.md) | Matriz de módulos por portal, fronteiras (biblioteca × documentos, protocolo × CRM, financeiro e contábil plataforma × entidade), matrícula, simulados, logs, testes, segurança e auditoria por portal |
| [32-atendimento-privacidade-por-portal.md](32-atendimento-privacidade-por-portal.md) | Help desk e SAC (estados, SLA, portal do cliente), privacidade, consentimento, pedido de titular, ROPA, DPO, por portal |
| [33-contratos-por-portal.md](33-contratos-por-portal.md) | Contratos: tipos e donos, ciclo de vida, alçadas, assinatura, obrigações, perfis e páginas por portal |
| [34-pagamentos-fiscal-bancos-por-portal.md](34-pagamentos-fiscal-bancos-por-portal.md) | Gateways, split, notas fiscais (NFS-e, fornecedor), bancos (módulo "Bancos" é ferramenta de banco de dados e sai do escopo), Open Finance, carteiras, por portal |
| [35-acesso-e-seguranca-fisica-por-portal.md](35-acesso-e-seguranca-fisica-por-portal.md) | Portaria, catracas, portas, visitantes, autorização de saída, biometria, câmeras (CFTV), por portal |
| [36-tecnologia-da-informacao-por-portal.md](36-tecnologia-da-informacao-por-portal.md) | TI da plataforma (desenvolvedor) e TI da entidade (gestão): ativos, chamados, mudanças, licenças, monitoramento, por portal |
| [29-auditoria.md](29-auditoria.md) | Auditoria: categorias, esquema do evento, integridade por cadeia de hash, acesso, mascaramento, retenção e alertas |
| [28-cobertura-ia-todos-os-modulos.md](28-cobertura-ia-todos-os-modulos.md) | Posição de IA para todos os módulos do catálogo: Sim, Restrita ou Não, com limite e decisão humana |
| [27-inteligencia-artificial-e-portais.md](27-inteligencia-artificial-e-portais.md) | IA por módulo e por portal: contratação por capacidade, gateway de IA, dados, limites por recurso, revisão humana, governança e testes. |
| [26-sdd-juridico-regulatorio.md](26-sdd-juridico-regulatorio.md) | SDD jurídico-regulatório: mapa de obrigações com grau de confiança, matriz de retenção, relação de consumo, consentimento por canal, educação, assinatura eletrônica, incidentes, acessibilidade, pagamentos, fiscal e SST. Não é parecer. |
| [25-dossie-juridico-e-lacunas.md](25-dossie-juridico-e-lacunas.md) | Dossiê para o jurídico: análise das lacunas, 13 perguntas com norma a verificar e riscos. Não é parecer. |
| [24-operacao-continuidade-qualidade.md](24-operacao-continuidade-qualidade.md) | Continuidade (RPO e RTO por banco), SLO, suporte, releases, testes, vulnerabilidade, contratos e lacunas do projeto (G-01 a G-20) |
| [23-dominios-provisionamento-ciclo-de-vida.md](23-dominios-provisionamento-ciclo-de-vida.md) | Domínios (seis portais, autenticação e arquivos), sessão entre domínios, Editor de portais declarativo, provisionamento e saída de cliente. D-22 e D-23 aprovadas. D-24 superada por D-25. |
| D-25 | **Aprovada pelo autor em 02/11/2026: seis portais.** Desenvolvedor, gestão (SaaS), professor, aluno, responsáveis e terceiros. Módulos são seções dentro dos portais, não subdomínios. Autenticação e arquivos são serviços de infraestrutura. Ver [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 1. | Aprovada. |
| D-26 | **Aprovada pelo autor em 02/11/2026.** Login único; depois seleção de entidade e unidade; atalho direto se houver um único vínculo. Portais em endereços próprios (`portal-do-aluno`, etc.). Ver [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 1. D-24 superada por D-25. Proposta: a entidade vem do contexto do token (D-20); domínio próprio opcional por entidade aponta para um dos portais. | Aguarda decisão do autor. |
| [22-crm-canais-e-papeis.md](22-crm-canais-e-papeis.md) | CRM em dois contextos (plataforma e tenant), canais de captação, papéis do CRM e papéis departamentais |
| [21-busca-e-armazenamento.md](21-busca-e-armazenamento.md) | Busca full-text e armazenamento de arquivos: layout, upload e download seguros, metadados corrigidos, quarentena, expurgo e índice com permissão |
| [20-pagamentos-seguranca.md](20-pagamentos-seguranca.md) | Pagamentos e recebimentos: escopo PCI, ledger, webhooks, Pix, boleto, estornos, conciliação e antifraude |
| [19-regras-modulos-3.md](19-regras-modulos-3.md) | Regras dos demais módulos do catálogo, duplicidades e lacunas |
| [18-regras-modulos-2.md](18-regras-modulos-2.md) | Regras de Cobrança, Notificações, Auditoria, RH e Contábil/Fiscal |
| [17-regras-modulos.md](17-regras-modulos.md) | Regras de validação, estados e defeitos dos módulos Financeiro, Pessoas, Acadêmico, SMT, Suprimentos e Contratos |
| [16-integracoes-externas.md](16-integracoes-externas.md) | Integrações externas de plataforma (master) e de tenant: catálogo, credenciais, ciclo de vida |

## 3. O que mudou em relação à v1

1. **Escopo de governança separado do produto.** A v1 misturava o produto com ferramentas de agentes de IA (`oh-my-opencode-slim`, `ag-kit`, `fable-method`, `mantis`) e instruções de instalação com `@latest`. A v2 mantém esses itens fora do SDD de produto. Ferramentas de desenvolvimento ficam em `11-governanca-qualidade.md`, com versão fixada.
2. **Sem dados pessoais nem identificadores operacionais.** A v1 listava e-mails reais de administradores e UUIDs da estrutura interna. A v2 remove esses dados; eles ficam no registro de seed privado.
3. **Referências verificáveis.** A v1 apontava para mais de 30 arquivos (`docs/security/…`, `docs/portais/…`, `.agents/skills/…`) que não estão nesta pasta. A v2 cita apenas caminhos que existem ou marca o item como externo.
4. **Afirmações de segurança com evidência.** Os números "0 críticos / 36 achados / 34 fixados" da v1 são **[Declarados]**. A v2 exige reprodução.
5. **Contradições corrigidas.** Ex.: "zero JavaScript inline" contra `onclick=` em [`sub_sidebar_itsm.php`](anexo-v1/sub_sidebar_itsm.php); "sem bibliotecas externas de runtime" contra CDN do Font Awesome. Detalhes em [13-achados-v1.md](13-achados-v1.md).
6. **Riscos de design corrigidos.** Ex.: rotação periódica de senha, bloqueio de conta por identificador (permite negação de serviço), vinculação rígida de sessão a IP, cookies `SameSite=Strict` em fluxos de navegação de primeira parte.

## 4. Princípios

1. **Default-deny.** Rota sem regra explícita é negada.
2. **Isolamento de tenant em toda consulta.** Filtro por tenant é obrigatório no repositório de dados, não só no controller.
3. **Segredos fora do código e fora do host da aplicação em produção.**
4. **Dados pessoais mínimos.** Coletar só o necessário; apagar ou anonimizar ao fim da retenção.
5. **Mudança rastreável.** Toda decisão relevante vira ADR; todo requisito tem critério de aceite testável.
6. **Português como idioma principal**, inglês como idioma canônico de chaves de código e i18n.

## 5. Decisões do autor (02/11/2026)

| # | Decisão | Opções | Onde |
|---|---|---|---|
| Busca por CPF | Permitida só com finalidade declarada por tenant, relatório de impacto, MFA recente, limites contra enumeração e auditoria de cada consulta. Ver [21](21-busca-e-armazenamento.md), seção 6.8. Prazo de retenção da auditoria: pendente (jurídico). | **Aprovada pelo autor em 02/11/2026.** |
| D-13 a D-15 | Busca e armazenamento: MySQL FULLTEXT inicialmente com interface isolada; um bucket por ambiente com prefixo por tenant; OCR nesta versão, com texto de bucket sensível fora do índice. Ver [21](21-busca-e-armazenamento.md), seção 9. | Decididas pelo autor em 02/11/2026. |
| D-10 a D-12 | Pagamentos: fluxo de recursos (conta do tenant; gateway da plataforma condicionado a parecer), centavos inteiros, MFA configurável com piso e limite padrão de R$ 1.000,00. Ver [20](20-pagamentos-seguranca.md), seção 19, e [06](06-identidade-acesso.md), seção 5. | Decidida pelo autor em 02/11/2026. |
| D-01 | Biblioteca de ícones. **Decidida: (a)**, self-host da licença Pro (ver [08](08-frontend-design-system.md)). | (a) self-host da licença Pro; (b) migrar para biblioteca open source; (c) manter CDN apenas com licença confirmada | [08](08-frontend-design-system.md) |
| D-02 | Cofre de segredos em produção. **Decidida: biblioteca própria** (`TotusTuus\Vault`), ver ADR-05. | (a) AWS KMS / Secrets Manager; (b) HashiCorp Vault; (c) provedor da nuvem contratada | [05](05-seguranca.md), [10](10-implantacao-operacao.md) |
| D-03 | Vínculo de sessão ao dispositivo. **Decidida: (b)**, token de dispositivo com revogação (ver [06](06-identidade-acesso.md), seção 7). | (a) só User-Agent + sinal de risco; (b) token de dispositivo (`DeviceTrust`) com revogação; (c) nenhum além de idle/absolute | [06](06-identidade-acesso.md) |
| D-04 | Recuperação de conta sem e-mail/SMS. **Decidida: e-mail verificado é obrigatório para cadastro e recuperação;** WhatsApp e Telegram ficam fora. | (a) códigos de recuperação de uso único; (b) passkey obrigatória para contas master; (c) suporte com verificação de identidade | [06](06-identidade-acesso.md) |

Cada opção tem trade-offs e condições de falha descritos no documento indicado. O SDD não escolhe por padrão.

## Decisões aprovadas em 03/11/2026 (documentos 31 a 36)

O autor aprovou as propostas adotadas nos documentos 31 a 36. Itens que pedem valor, nome ou parecer continuam pendentes e estão listados abaixo.

| Documento | Aprovado | Ainda pendente |
|---|---|---|
| [31](31-matriz-portais-modulos.md) | Biblioteca separada de Documentos; protocolo como serviço de atendimento, fora do CRM comercial; financeiro e contábil da plataforma e da entidade em bancos separados; matrícula, simulados e auditoria com `portal` | Planejamento acadêmico, institucional e de desenvolvimento; empenho; permanência dos módulos financeiro, contábil, patrimônio, frotas, suprimentos e pessoas da plataforma; gabarito óptico; plano PRO |
| [32](32-atendimento-privacidade-por-portal.md) | Ticket como tipo de protocolo; módulo único de atendimento; consentimento por finalidade; pedido de titular com estados e verificação de identidade; DPO com painel próprio, sem operar o módulo que audita | Valores padrão de SLA; regra de categoria sensível; nomes dos DPOs; retenção de tickets; consentimento de menor de 13 anos (jurídico) |
| [33](33-contratos-por-portal.md) | Tipos de contrato com dono e portal de origem; aditivo segue o portal do contrato original; contrato com dado pessoal exige DPA antes da assinatura | Faixas de alçada; antecedência de alerta; provedor de assinatura eletrônica; cláusulas obrigatórias e forma de assinatura (jurídico) |
| [34](34-pagamentos-fiscal-bancos-por-portal.md) | Módulo Bancos removido do escopo; split mantido na opção (a), sem custódia; nota de fornecedor recebida e validada, não emitida; carteira digital como método do gateway, sem guardar token | Open Finance e débito automático (jurídico); NFS-e Nacional, cancelamento e guarda de XML (fiscal e jurídico); NFS-e da assinatura SaaS |
| [35](35-acesso-e-seguranca-fisica-por-portal.md) | Biometria opcional, com alternativa sem biometria; template cifrado no banco da unidade; câmeras fora de áreas íntimas e com aviso; liberação de emergência sem rede | Prazo de retenção de imagem; escopo de biometria e reconhecimento facial (jurídico e RIPD); geolocalização na presença; fabricantes de catraca e porta |
| [36](36-tecnologia-da-informacao-por-portal.md) | TI da plataforma fora de qualquer portal de cliente; TI da entidade com ativo como vista do Patrimônio; chamados de TI no atendimento; mudança com aprovação de segundo papel; [`sub_sidebar_itsm.php`](anexo-v1/sub_sidebar_itsm.php) removido | Comitê de mudança e quórum; prazo de aprovação de mudança emergencial; manter ou remover monitoramento de equipamento da entidade |
| [37](37-planejamento-e-empenho.md) | Planejamento acadêmico, institucional e de desenvolvimento de pessoas; empenho para entidade pública. Análise, estados, regras, segregação, portais e estrutura de dados |
| [38](38-portal-de-terceiros-prestadores.md) | Portal de terceiros: prestadores por tipo (jurídico, contabilidade, cartório, alimentação, transporte escolar, transportadora, TI, limpeza, vigilância, uniformes, clínica de ASO, consultoria), com acesso limitado ao contrato |
| [39](39-departamento-pessoal-rh-medicina-por-portal.md) | Departamento pessoal, RH e medicina do trabalho: lacunas, separação de dado de saúde (RH sem CID), permissões corrigidas, por portal |
| [40](40-aulas-online-por-portal.md) | Aulas online e reuniões ao vivo: aula sem especificação na v1, menores (consentimento e gravação), presença, convidado externo, infraestrutura de mídia, por portal |
| [41](41-formularios-e-pesquisas.md) | Formulários e pesquisas: motor compartilhado, anonimato com tabelas separadas, dado sensível, relatórios por grupo com mínimo |
| [42](42-preceptoria-por-portal.md) | Preceptoria: avaliação e autoavaliação, tutoria, PDI, evidências; conflito de nome com a navegação da v1 |
| [43](43-pastoral-por-portal.md) | Gestão pastoral: eventos, missas e celebrações, escalas, intenções, ações sociais. Confissões só como horário público, sem registro de pessoa. Tradições configuráveis, com modo ecumênico |
| [44](44-agendamento-ambientes-equipamentos.md) | Agendamento de ambientes e equipamentos (acadêmico): conflito de horário, prioridade, grade como bloqueio fixo, equipamento como bem patrimonial |
| [45](45-pendencias-consolidadas.md) | Pendências consolidadas por responsável: autor, jurídico, norma, documento, homologação e owner. Refeita por auditoria completa dos docs 00 a 76 em 03/11/2026 |
| [46](46-matricula-e-rematricula-por-portal.md) | Matrícula e rematrícula: estados, janela, condicional com prazo, não rematriculada, trancamento por nível, vaga com bloqueio de concorrência, por portal |
| [47](47-simulados-por-portal.md) | Simulados e correção de redação: perfis, OCR com revisão, nota da IA só como sugestão confirmada pelo professor, ranking por opção da unidade |
| [48](48-gerador-de-documentos-por-portal.md) | Gerador de documentos: editor de modelos, tipos, ciclo de emissão, validação pública sem dado pessoal, assinatura, por portal |
| [49](49-logs-testes-por-portal.md) | Logs de integração e de job, testes por portal, teste de isolamento por par, acessibilidade |
| [51](51-ddl-modulos-novos.md) | DDL dos módulos novos e pendentes: atendimento, LGPD, contrato, acesso físico, formulários, preceptoria, pastoral, agendamento, sala de aula, matrícula e TI |
| [52](52-medicina-do-trabalho-especificacao.md) | Medicina do trabalho: PCMSO, PGR, LTCAT, CIPA e ergonomia, com DDL e quem vê o quê |
| [50](50-pacote-juridico-e-norma.md) | Pacote de 61 perguntas para jurídico e norma, com posição proposta por pergunta |
| [53](53-pacote-documentos-e-contratos.md) | Pacote para jurídico: contratos, declarações, certidões, acervo escolar, termos, autorizações, atas e dossiês. 28 perguntas (DC-01 a DC-28) |
| [54](54-gestao-de-documentos-tres-contextos.md) | Gestão de documentos em três contextos: recebidos (validação), administrativos (tramitação) e emitidos (secretaria), com serviços comuns de assinatura, protocolo e armazenamento |
| [55](55-academico-verificacao-e-lacunas.md) | Verificação do acadêmico contra o menu do iScholar: cobertura, 13 lacunas em ordem de dependência, 4 decisões de produto |
| [56](56-configuracoes-e-relatorios-lacunas.md) | Configurações e relatórios: menus do iScholar comparados com o SDD, lacunas por grupo |
| [57](57-notificacoes-por-portal.md) | Notificações por portal: canais, preferências, targeting, templates, provedores e lacunas do módulo |
| [58](58-calendario-e-eventos-por-portal.md) | Calendário escolar e eventos: período, dia não letivo, eventos, inscrição, capacidade, certificado, por portal |
| [59](59-estrutura-academica-por-portal.md) | Estrutura acadêmica: tipos de curso, disciplinas, grades e PPC versionados, equivalências, períodos e sistemas avaliativos, por portal |
| [60](60-turmas-e-grade-de-horarios-por-portal.md) | Turmas, cadastro de salas, enturmação, grupos de horários e grade de horários: conflitos de professor, turma e ambiente, publicação e consultas, por portal |
| [61](61-diario-escolar-por-portal.md) | Diário escolar: aula, chamada por três formas, faltas, justificativas com prazo e aprovação, notas com versão, fechamento e reabertura, por portal |
| [62](62-boletim-e-conselho-de-classe-por-portal.md) | Boletim parcial e oficial, regra de aprovação, recuperação paralela, conselho de classe com pauta, decisão e ata, por portal |
| [63](63-ocorrencias-disciplinares-por-portal.md) | Ocorrências disciplinares e de convivência: tipos, gravidade, fluxo, medidas, contestação, sigilo e denúncia de violência, por portal. Separada de SST, portaria e saúde |
| [64](64-planos-de-aula-e-de-ensino-por-portal.md) | Planos de ensino (disciplina, turma e período, com critérios que batem com o sistema avaliativo) e planos de aula (por aula ou semana), com revisão, IA com revisão humana e PPP fora do módulo, por portal |
| [65](65-estagio-e-tcc-por-portal.md) | Estágio (obrigatório ou não, termo, horas, supervisão, avaliação) e TCC (orientação, estados, banca, versão final e repositório), por portal. Supervisor externo e membro de banca com conta no portal de terceiros |
| [66](66-prontuario-e-portfolio-do-aluno-por-portal.md) | Prontuário como visão sobre os documentos (sem cópia), seção restrita de saúde e apoio, histórico após saída, portfólio com avaliação, compartilhamento e exportação, por portal |
| [67](67-livros-digitais-e-arquivo-morto-por-portal.md) | Livro de registro e livro de atas digitais com travamento, retificação e assinatura; arquivo morto com digitalização verificada por outra pessoa e eliminação só com termo, por portal |
| [68](68-biblioteca-por-portal.md) | Biblioteca separada de documentos: acervo e exemplares, perfis e prazos configurados pela escola, empréstimo, reserva, multa, inventário, biblioteca digital, salas via recursos e empréstimo entre unidades, por portal |
| [69](69-relatorios-e-censo-por-portal.md) | Relatórios: modelo comum (operacional, gerencial, regulatório), ciclo de geração e arquivo, catálogo por módulo, censo escolar com conferência e envio pela secretaria, formatos oficiais, por portal |
| [70](70-importacao-de-dados-por-portal.md) | Importação e carga inicial: ordem por dependência, simulação, lote desfazível, idempotência, histórico sem cobrança retroativa nem aviso em massa, por portal |
| [71](71-financeiro-completo-por-portal.md) | Financeiro completo (CFG-04): contas a pagar com rateio e aprovação, cheques recebidos e emitidos, caixa físico com fechamento, fluxo de caixa, DRE por regime escolhido, conciliação e por portal. Receita de aluno fica em 18 e 20 |
| [72](72-campos-personalizados-por-portal.md) | Campos personalizados (CFG-06): definidos por entidade ou por unidade, valores no banco da unidade, só acrescentam, com classificação de dado e fora de saúde, prontuário e ocorrência, por portal |
| [73](73-resumo-juridico-academico.md) | Resumo para o jurídico: 20 perguntas dos módulos acadêmicos e administrativos (docs 55 a 72), com posição proposta e documento de origem para cada uma |
| [74](74-integracoes-educacionais-oficiais.md) | Integrações educacionais oficiais: Educacenso (arquivo importado no INEP), SIGEP, SGP por API, sistema municipal (conflito em aberto) e Pé-de-Meia, com regra de canal oficial e de quem envia, por portal |
| [75](75-busca-notificacoes-perfil-integracoes-por-escopo.md) | Análise por escopo (plataforma, entidade, unidade, módulo, global): busca, notificações, perfil e integrações internas e externas, com lacunas e decisões pendentes |
| [76](76-meu-perfil-por-portal.md) | Meu perfil: uma tela em todos os portais, com dados, contato, endereço, segurança, preferências, consentimentos, histórico e pedido de titular. Regras de edição decididas em PER-04 e PER-05 |
| [77](77-licenciamento-planos-e-limites.md) | Licenciamento: planos com limite de alunos definido pelo desenvolvedor, situações da assinatura, carência e comportamento ao exceder o limite |
| [78](78-permissoes-e-papeis.md) | Permissões completas: níveis de papel (0 a 7), escopos, papéis por portal, criação de entidade e unidade só pelo desenvolvedor, separação de funções |
| [79](79-rastreabilidade-v1-v2.md) | Rastreabilidade v1 → v2: para cada um dos 62 arquivos da v1 (em `anexo-v1/`), o destino na v2 e o que ainda não foi absorvido. Gerado por `inventario/gera_rastreabilidade.py` |
| [80](80-decisoes-por-padrao.md) | Decisões tomadas por padrão, delegadas pelo autor em 04/11/2026 (melhor prática, mais segura, completa), com motivo e alternativa descartada |
| [81](81-classe-mural-materiais-tarefas.md) | Classe: mural de avisos, materiais de apoio e tarefas com entrega, por portal, com estados, regras, permissões e DDL (especifica o DP-06) |
| Decisões de configuração (CFG-01 a CFG-04) | Agenda iScholar fora do escopo. Foto com consentimento por aluno. Relatório de acesso do responsável com link de uso único. Financeiro completo, com cheques, caixa e DRE | [56](56-configuracoes-e-relatorios-lacunas.md), seção 8 |
| Notificações (NOT-02, NOT-03, NOT-05, NOT-06) | Silêncio 21h às 7h. Segunda aprovação acima de 500. Remetentes de saúde: secretaria, enfermagem, médico e coordenação. Push por aplicativo Android e iOS | [57](57-notificacoes-por-portal.md), seção 5 |
| Calendário e eventos escolares | Módulo próprio, nesta versão. Especificação pendente | [56](56-configuracoes-e-relatorios-lacunas.md), CFG-01 |

Correção aplicada: o módulo "Bancos" nos documentos [12](12-catalogo-modulos.md) e [19](19-regras-modulos-3.md) passa a ser ferramenta de banco de dados, fora do produto.

## Decisões de 03/11/2026, segunda rodada

| Decisão | Resposta | Documento |
|---|---|---|
| Módulo Bancos | Removido de produto. Painel de bancos de dados no portal do desenvolvedor, sem console SQL aberto | [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 11 |
| Split | Mantido em (a). Lista de mudanças para (c) registrada | [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 11 |
| Nota de fornecedor | Recebe e valida, sem emitir | [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 5.3 |
| Portaria & Acesso | Mantido no portal do desenvolvedor, para acesso físico da própria empresa | [35](35-acesso-e-seguranca-fisica-por-portal.md), seção 11 |
| Biometria, reconhecimento facial e câmeras | Escopo aprovado. Retenção de imagem: 30 dias, padrão inicial | [35](35-acesso-e-seguranca-fisica-por-portal.md), seção 11 |
| Ticket como protocolo | Aprovado em parte: pedido com responsável e prazo recebe protocolo | [32](32-atendimento-privacidade-por-portal.md), seção 7 |
| SLA padrão | Aprovado: 1 h a 10 dias úteis por prioridade, ajustável por entidade | [32](32-atendimento-privacidade-por-portal.md), seção 7 |
| Faixas de alçada | Aprovadas como padrão inicial: até R$ 10.000; até R$ 100.000; acima | [33](33-contratos-por-portal.md), seção 12 |
| DPO | Plataforma: empresa desenvolvedora. Entidade: designado pela entidade, podendo ser a empresa por contrato | [32](32-atendimento-privacidade-por-portal.md), seção 7 |
| Planejamento e empenho | Analisados e implementados como módulos de tenant. Empenho só para entidade pública | [37](37-planejamento-e-empenho.md) |

## Análises de 03/11/2026, terceiros e pessoal

- **Terceiros por tipo** ([38](38-portal-de-terceiros-prestadores.md)): cada prestador tem contrato, pessoas com vínculo ligado ao contrato, serviços do pacote do tipo e unidades listadas. O acesso é a interseção de contrato vigente, serviço, unidade e papel. Teste de isolamento entre prestadores.
- **Pessoal, RH e SST** ([39](39-departamento-pessoal-rh-medicina-por-portal.md)): análise mostrou lacunas em folha, rescisão, recrutamento, PCMSO, PGR, LTCAT e CIPA, e uma falha de privacidade na v1: RH e gestão podiam gerenciar SST e ver CID. Proposta: RH e gestão veem só o resultado do ASO.

## Decisões de 03/11/2026, terceiros e pessoal

| Tema | Decisão | Onde |
|---|---|---|
| RH e Pessoas (HCM-01) | Módulos separados, vínculo por referência à pessoa | [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 11 |
| Permissão "SST — Gerenciar" (HCM-06) | Por papel e portal que precisa. Não é concedida a RH nem a gestão por cargo | [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 11 |
| HCM da plataforma e dos clientes (HCM-10) | Dois usos do mesmo módulo, isolados: empresa desenvolvedora (master) e cada entidade | [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 11 |
| Currículo de não contratado (HCM-09) | Incluído. Prazo a fixar pelo (jurídico) | [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 11 |
| Tipos de prestador (TER-01) | Tipos personalizados a partir de modelo-base, só com serviços do catálogo, com aprovação e auditoria | [38](38-portal-de-terceiros-prestadores.md), seção 11 |
| Rastro de localização do transporte (TER-02) | Incluído. Guarda só durante a viagem e prazo fixo depois. 30 dias depois da viagem, decidido em 03/11/2026. Parecer do (jurídico) pendente | [38](38-portal-de-terceiros-prestadores.md), seção 11 |
| Acesso remoto de TI (TER-08) | Incluído. Só com chamado aberto, dentro de janela, sessão gravada | [38](38-portal-de-terceiros-prestadores.md), seção 11 |
| Infraestrutura de aula online (LIV-05) | Mídia própria, com as melhores tecnologias. Operação a especificar em [10](10-implantacao-operacao.md) | [40](40-aulas-online-por-portal.md), seção 8 |
| Transcrição de aula com menor por IA (LIV-03) | Sim, pelo gateway de IA. Desligada por padrão, habilitada por unidade | [40](40-aulas-online-por-portal.md), seção 5 |
| Presença em aula online (LIV-04) | 40 minutos de tempo conectado, configurável por entidade | [40](40-aulas-online-por-portal.md), seção 6 |
| Convidado externo e diretor (LIV-06, LIV-07) | Entidade habilita externos com token de uso único. Diretor tem passe livre na unidade, com auditoria. Coordenador em aberto | [40](40-aulas-online-por-portal.md), seção 7 |
| Visual da sala (LIV-08) | Template do portal, layout de reunião estilo Zoom. Especificado em [08](08-frontend-design-system.md), seção 9 | [40](40-aulas-online-por-portal.md), seção 4.4 |
| Operação de mídia (LIV-11) | Gravação em fragmentos cifrados de 60 s, com índice de fragmentos, manifesto e verificação de checksum | [10](10-implantacao-operacao.md), seção 10 |
| Coordenador em aula (LIV-07) | Pode observar aulas da unidade, com registro em auditoria | [40](40-aulas-online-por-portal.md), seção 7 |
| Consentimento de menor (LIV-01) | Pedido por cláusula do contrato com a instituição. Texto com o jurídico | [40](40-aulas-online-por-portal.md), seção 5 |


## 5. Anexo v1 (incorporado)

A coleção v1 está em [anexo-v1/](anexo-v1/) (62 arquivos, sem alteração de conteúdo). Cada arquivo tem um status em [12-catalogo-modulos.md](12-catalogo-modulos.md) (seções 2 a 4) e um destino na v2 em [79-rastreabilidade-v1-v2.md](79-rastreabilidade-v1-v2.md). O consolidado [SDD-COMPLETO.md](SDD-COMPLETO.md) é gerado por `inventario/gera_sdd_completo.py`. Não é preciso consultar a pasta original fora deste repositório.
