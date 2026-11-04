# 50 — Pacote para Parecer Jurídico e Conferência de Norma

> Parte do [SDD v2](00-README.md). Lista de trabalho em [45](45-pendencias-consolidadas.md). Base legal geral em [26](26-sdd-juridico-regulatorio.md) e [25](25-dossie-juridico-e-lacunas.md). Política de privacidade em [07](07-privacidade-lgpd.md).
> **Natureza deste documento:** pacote de consulta. Não é parecer, não é opinião jurídica e não substitui a análise de advogado habilitado. As "posições propostas" são o que o SDD adota hoje para que o sistema seja desenhado. O jurídico confirma, corrige ou recusa cada uma.
> **Citações legais:** as referências a leis, decretos, resoluções e normas regulamentadoras estão indicadas como **a confirmar**. Não foram verificadas contra o texto vigente na elaboração deste pacote.
> **Status:** versão 2, redigida em 03/11/2026. São 61 perguntas em 9 blocos.

---

## 1. Como responder

Cada pergunta tem um campo de resposta, na seção 11. O responsável marca uma das três opções:

- **Confirma:** a posição proposta pode ser adotada como está.
- **Corrige:** informar a posição correta e a referência legal que a sustenta.
- **Recusa:** a regra não pode ser adotada. Informar o motivo.

Resposta escrita, com data e nome do responsável, é o que fecha o item. A resposta vai para o documento de origem, e a linha sai da [45](45-pendencias-consolidadas.md).

---

## 2. Contexto para quem responde

**O que é a plataforma.** Sistema de gestão para instituições de ensino e outros serviços educacionais, com multi-tenancy: a empresa desenvolvedora opera a plataforma, e cada entidade cliente tem seu banco e suas unidades ([03](03-dominio-tenancy.md)).

**Quem são os titulares.** Alunos (muitos menores de idade), responsáveis legais, professores, funcionários, candidatos, residentes, prestadores de serviço, visitantes e doadores.

**Dados de risco no sistema.** Dados de saúde (ASO, atestados, CID), convicção religiosa (pastoral), dados de menor, imagem (câmeras e aulas gravadas), biometria opcional, localização de transporte escolar e dados de cobrança.

**Papéis.** A entidade é, em regra, a controladora dos dados dos seus alunos e funcionários. A empresa desenvolvedora atua como operadora, salvo onde o contrato diga outra coisa. Essa separação precisa de confirmação **(a confirmar)**, e alguns itens dependem dela.

---

## 3. Bloco A: dados de menores de idade e consentimento

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| J-01 | Consentimento do responsável para gravar aula com menor: forma, validade e revogação | Aula online pode ser gravada, com aviso visível | Consentimento específico e por escrito, pedido por cláusula do contrato com a instituição. Revogável | Consentimento por ato, a cada aula | [40](40-aulas-online-por-portal.md), seção 5 |
| J-02 | Menor de 13 anos: método de consentimento parental | Cadastro de aluno de educação infantil e fundamental | Consentimento do responsável, com verificação do vínculo, para qualquer tratamento que não seja essencial ao serviço (LGPD, art. 14 **a confirmar**) | Consentimento para todo tratamento | [32](32-atendimento-privacidade-por-portal.md) |
| J-03 | Tutoria de aluno menor com dado sensível: base legal | Registro de tutoria pode mencionar dificuldade pessoal | Consentimento do responsável para o registro com dado sensível. Sem consentimento, só dado de acompanhamento acadêmico | Vedar o registro sensível para menor | [42](42-preceptoria-por-portal.md), seção 5 |
| J-04 | Evento e escala pastoral com menor: autorização e imagem | Encontro de jovens, coroinha, festa escolar | Autorização do responsável, com validade. Imagem de menor só com autorização específica | Autorização geral na matrícula | [43](43-pastoral-por-portal.md), seção 6 |
| J-05 | Documentos obrigatórios por nível de ensino, e se algum pode bloquear a matrícula | Wizard de matrícula exige identidade, histórico anterior e outros | Identidade e histórico anterior condicionam a matrícula. Bloqueio só para o que a norma do sistema de ensino exige | Bloquear todo documento pendente | [46](46-matricula-e-rematricula-por-portal.md), M-08 |

---

## 4. Bloco B: dados sensíveis, biometria e imagem

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| J-06 | Biometria e reconhecimento facial de aluno: escopo, base legal e exigências para menor | Catraca com biometria opcional | Opcional, com alternativa sem biometria. Template cifrado, guardado na unidade. RIPD antes de ativar | Não usar biometria | [35](35-acesso-e-seguranca-fisica-por-portal.md), seção 5 |
| J-07 | Retenção de imagem de câmera | Câmeras de áreas comuns e de acesso | 30 dias, com expurgo automático. Aviso visível no local | Prazo maior, para investigação | [35](35-acesso-e-seguranca-fisica-por-portal.md), seção 6 |
| J-08 | Dado sensível em formulário: base legal | Pesquisa que pode perguntar saúde ou religião | Consentimento específico, declarado antes da publicação | Vedar dado sensível em formulário | [41](41-formularios-e-pesquisas.md), seção 4 |
| J-09 | Intenção de missa e cadastro de beneficiário: prazos de guarda | Pedido de oração e cadastro de família atendida | Intenção excluída após a celebração e prazo curto fixo. Beneficiário revisado periodicamente, sem expurgo automático até definição | Prazo único para os dois | [43](43-pastoral-por-portal.md), seções 3.3 e 4 |
| J-10 | Campanhas que coletam renda: base legal | Campanha de ação social pode pedir renda | Só quando a campanha precisar, com base escrita por campanha | Não coletar renda | [43](43-pastoral-por-portal.md), seção 4 |

---

## 5. Bloco C: cobrança, crédito e meios de pagamento

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| J-11 | Consulta por CPF: retenção da auditoria de 24 horas conflita com o relatório ao titular e com a guarda de acesso | Consulta de CPF é registrada para investigação | Prioridade máxima. Separar o registro de acesso (prazo legal) da auditoria de consulta. Parecer sobre o prazo da auditoria | Manter 24 horas e aceitar a limitação do relatório | [25](25-dossie-juridico-e-lacunas.md), Q-01 |
| J-12 | Registro de acesso a aplicação: prazo de seis meses | Login, IP e sessão | Confirma seis meses, se a lei aplicável for o Marco Civil da Internet, art. 15 **a confirmar** | Outro prazo, se a norma for outra | [25](25-dossie-juridico-e-lacunas.md) |
| J-13 | Negativação e comunicação prévia ao consumidor (CDC, art. 43, §2º **a confirmar**) | Régua de cobrança pode negativar | Comunicação por escrito antes da inclusão | Sem negativação automática | [25](25-dossie-juridico-e-lacunas.md) |
| J-14 | Superendividamento na régua de cobrança (Lei 14.181/2021 **a confirmar**) | Renegociação de mensalidades | Aplicar à régua, com proposta de renegociação antes de cobrança judicial | Régua sem tratamento específico | [25](25-dossie-juridico-e-lacunas.md) |
| J-15 | Mensagens por SMS, WhatsApp e Telegram em cobrança e marketing: base | Canais de comunicação de cobrança | Cobrança por execução de contrato. Marketing só com consentimento | Consentimento também para cobrança | [18](18-regras-modulos-2.md), seção 2.6 |
| J-16 | Open Finance e débito automático: base e autorização | Débito automático e leitura de extrato | Autorização específica, por escrito, revogável | Autorização junto ao contrato | [34](34-pagamentos-fiscal-bancos-por-portal.md), PAG-07 |
| J-17 | Bloqueio parcial por inadimplência: quais serviços continuam para menor | Bloqueio de portal por atraso | Documentos obrigatórios, rematrícula e comunicação com a família continuam | Bloqueio total após prazo | [26](26-sdd-juridico-regulatorio.md), seção 3 |
| J-18 | Chargeback: prazo de resposta | Contestação de cobrança no cartão | Resposta no prazo definido pela bandeira **a confirmar** | Prazo interno | [20](20-pagamentos-seguranca.md) |

---

## 6. Bloco D: contratos e assinatura

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| J-19 | Forma de assinatura por tipo de contrato | Contrato de matrícula, de prestação e de fornecedor | Assinatura digital com certificado ICP-Brasil para contrato de matrícula e de prestação. Assinatura simples para os demais, com validade conforme parecer | ICP-Brasil para todos | [33](33-contratos-por-portal.md), CTR-04 |
| J-20 | Assinatura digital própria: exigências para ser aceita | Decisão CTR-06: aceitar provedores de terceiros e ter assinatura própria | Credenciamento como autoridade certificadora, se a plataforma emitir certificado. Caso contrário, usar provedor credenciado | Só provedor de terceiros | [33](33-contratos-por-portal.md), CTR-06 |
| J-21 | Cláusulas obrigatórias por tipo de contrato | Modelos de contrato do sistema | Lista por tipo, a ser entregue pelo jurídico | Modelo padrão único | [33](33-contratos-por-portal.md), CTR-05 |
| J-22 | Contrato de matrícula: forma, cláusulas e prazo de guarda | Gerado no wizard de matrícula | Forma escrita e assinada. Guarda pelo prazo do sistema de ensino | Guarda por prazo fixo | [33](33-contratos-por-portal.md), CTR-07 |
| J-23 | Contrato de experiência de trabalho: texto da v1 é contraditório | Admissão no módulo de RH | Regra da CLT **a confirmar**. Não usar o texto da v1 | Sem contrato de experiência no sistema | [17](17-regras-modulos.md), seção 3 |

---

## 7. Bloco E: trabalhista, previdenciário e saúde

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| N-01 | Férias: período aquisitivo, fracionamento e cálculo de direito (CLT, art. 130 **a confirmar**) | Módulo de férias | Regra da CLT, com fracionamento conforme a lei | Regra interna mais simples | [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 3 |
| N-02 | Rescisão: aviso prévio, férias proporcionais, 13.º e multa do FGTS | Cálculo de desligamento | Cálculo conforme a CLT, com tabela por competência | Cálculo manual pela contabilidade | [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 4 |
| N-03 | Eventos eSocial de admissão, remuneração, pagamento e desligamento (S-2200, S-1200, S-1210, S-2299 **a confirmar** com o layout vigente) | Transmissão ao eSocial | Os quatro eventos, com layout vigente | Só os eventos de SST | [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 8 |
| N-04 | Tabelas de INSS, IRRF e FGTS por competência | Cálculo de folha | Tabela oficial da competência, versionada | Tabela fixa do ano | [39](39-departamento-pessoal-rh-medicina-por-portal.md), DP-02 |
| N-05 | Controle de jornada e registro de ponto | Ponto eletrônico | Conforme a CLT e a portaria aplicável **a confirmar** | Espelho de ponto simples | [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 3 |
| N-06 | Prontuário de medicina do trabalho e ASO: prazo de guarda | Guarda de ASO e prontuário | Prazo previsto nas normas de saúde ocupacional e no regulamento do conselho **a confirmar** | Prazo único de 20 anos | [39](39-departamento-pessoal-rh-medicina-por-portal.md), HCM-08 |
| N-07 | CAT ao INSS: canal e prazo | Registro de acidente de trabalho | Canal e prazo vigentes **a confirmar** | Envio manual | [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 5 |
| N-08 | NRs aplicáveis, validade de treinamento e CIPA | PCMSO, PGR, CIPA e treinamentos | NR-1 (gestão de riscos), NR-5 (CIPA), NR-7 (PCMSO), NR-17 (ergonomia) e NRs específicas, **a confirmar** | Lista reduzida | [52](52-medicina-do-trabalho-especificacao.md) |
| N-09 | Quem emite CID e quem pode vê-lo | Atestado e afastamento | Médico emite e vê. Gestão e RH não recebem CID | Gestão vê o motivo resumido | [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 5.1 |

---

## 8. Bloco F: educação, documentos e estágio

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| N-10 | Prazo de guarda de documentos escolares: histórico, declaração e registro de classe | Acervo escolar | Prazo do sistema de ensino da entidade, com a referência gravada no sistema | Prazo único do sistema | [26](26-sdd-juridico-regulatorio.md), seção 3 |
| N-11 | Layout do histórico escolar | Emissão de histórico | Conforme a norma do sistema de ensino **a confirmar** | Layout próprio | [48](48-gerador-de-documentos-por-portal.md), DOC-03 |
| N-12 | Assinatura de documento oficial: exigência de ICP-Brasil por tipo | Emissão de documento com assinatura | Lista por tipo, entregue pelo jurídico | Assinatura simples para todos | [48](48-gerador-de-documentos-por-portal.md), DOC-01 |
| N-13 | Plano institucional e órgão colegiado aprovador, por tipo de entidade | Planejamento institucional | Aprovação pelo órgão colegiado, com ata registrada | Aprovação pela direção | [37](37-planejamento-e-empenho.md), PLN-01 |
| N-14 | Lei 4.320/1964 e as fases da despesa pública (empenho, liquidação e pagamento) | Módulo de empenho, só para entidade pública | Modalidades ordinária, estimativa e global, com as fases da lei **a confirmar** | Empenho sem fases | [37](37-planejamento-e-empenho.md), PLN-02 |
| N-15 | Tempo de guarda de currículo de candidato não contratado | Banco de candidatos | Prazo fixo, com aviso no envio | Guarda indefinida | [39](39-departamento-pessoal-rh-medicina-por-portal.md), HCM-09 |
| N-16 | Residência médica: regulamento e avaliação por programa | Preceptoria de residentes | Conforme o regulamento da Comissão Nacional de Residência Médica e do programa **a confirmar** | Regra única | [42](42-preceptoria-por-portal.md), PRE-04 |

---

## 9. Bloco G: prestadores de serviço

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| N-17 | Transporte escolar: base legal de trajeto e de restrição alimentar | Motorista e restrição alimentar do aluno | Trajeto só durante a viagem. Restrição alimentar sem diagnóstico | Restrição com diagnóstico | [38](38-portal-de-terceiros-prestadores.md), TER-03 |
| N-18 | Rastro de localização do ônibus: prazo de guarda | Localização durante a viagem | 30 dias depois da viagem, decidido pelo autor em 03/11/2026. Confirmar | Sem guarda | [38](38-portal-de-terceiros-prestadores.md), TER-02 |
| N-19 | Norma sanitária: registro de temperatura e validade na alimentação | Fornecedor de merenda | Registro por lote, conforme a norma da vigilância sanitária **a confirmar** | Sem registro | [38](38-portal-de-terceiros-prestadores.md), TER-04 |
| N-20 | Prontuário pela clínica de ASO: guarda | Clínica contratada para exames | Quem faz o exame guarda o prontuário | Empresa guarda | [38](38-portal-de-terceiros-prestadores.md), TER-05 |
| N-21 | Cartório digital: validade do selo por tipo de ato | Fornecedor de cartório | Validade conforme a lei do tipo de ato **a confirmar** | Validade única | [38](38-portal-de-terceiros-prestadores.md), TER-06 |
| N-22 | Documentos exigidos por tipo de prestador | Cadastro de fornecedor | Lista por tipo, entregue pelo jurídico | Lista única | [38](38-portal-de-terceiros-prestadores.md), TER-07 |
| N-23 | Nome do fornecedor visível a outros fornecedores | Lista de prestadores | Não visível, salvo cadastro público exigido por lei **a confirmar** | Visível a todos | [38](38-portal-de-terceiros-prestadores.md), seção 9 |

---

## 10. Bloco H: privacidade, incidente e governança

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| J-24 | Prazo de comunicação de incidente à ANPD (Resolução CD/ANPD 15/2024 **a confirmar**) | Plano de resposta a incidente | Três dias úteis, após confirmar a vigência | Outro prazo | [07](07-privacidade-lgpd.md), seção 8 |
| J-25 | Bases legais por finalidade de tratamento escolar | Matriz de finalidades | Matriz de [07](07-privacidade-lgpd.md), seção 3, revisada | Matriz nova | [07](07-privacidade-lgpd.md) |
| J-26 | Transferência internacional de dado, se houver cliente fora do Brasil | Hospedagem e fornecedores | Só com cliente fora do Brasil. Sem cliente, não se aplica | Verificar caso a caso | [19](19-regras-modulos-3.md), seção 4 |
| J-27 | Vínculo de responsabilidade legal: quem pode solicitar em nome de outra pessoa | Acesso de responsável a dados do aluno | Verificação por documento e vínculo cadastrado pela escola. Decidido pelo autor em 03/11/2026. Confirmar | Autodeclaração com código | [31](31-matriz-portais-modulos.md), SEG-01 |
| J-28 | Revisão humana de comentário livre em relatório anônimo | Formulário anônimo com comentário | Sempre revisado por pessoa, decidido pelo autor. Confirmar se a revisão basta | Mascaramento automático | [41](41-formularios-e-pesquisas.md), FRM-02 |
| J-29 | Retenção de tickets de atendimento e de transcrição de chat | Atendimento e chat | Prazo fixo, definido pelo jurídico | Prazo por tipo | [32](32-atendimento-privacidade-por-portal.md), ATD-03 |
| J-30 | Prazo de guarda de cada tipo de documento emitido | Emissão de documentos | Prazo por tipo, conforme norma | Prazo único | [48](48-gerador-de-documentos-por-portal.md), DOC-02 |
| J-31 | Uso de nome de exame oficial em perfil de simulado | Perfis ENEM e outros | Permitido só com autorização do titular do nome | Uso livre como referência | [47](47-simulados-por-portal.md), SIM-02 |
| J-32 | Retenção de redação original e de transcrição de simulado | Redações digitalizadas | Prazo do sistema de ensino | Prazo fixo | [47](47-simulados-por-portal.md), SIM-01 |
| J-33 | Prazos de retenção de avaliação, tutoria e PDI | Preceptoria | Prazo do programa e do sistema de ensino | Prazo único | [42](42-preceptoria-por-portal.md), PRE-05 |
| J-34 | Retenção de gravação e transcrição de aula | Aula online gravada | 30 dias, padrão proposto | Prazo menor | [40](40-aulas-online-por-portal.md), LIV-02 |
| J-35 | Retenção de respostas de formulário, por tipo | Pesquisas e avaliações | Prazo por tipo, a definir | Prazo único | [41](41-formularios-e-pesquisas.md), FRM-06 |
| J-36 | Gateway de IA e transcrição de aula com menor: base e contrato com o provedor | Transcrição de aula por IA, decidido pelo autor | Permitido pelo gateway, com contrato de tratamento com o provedor | Vedar transcrição de menor | [27](27-inteligencia-artificial-e-portais.md), IA-02 a IA-04 |
| J-37 | Relatório de impacto (RIPD) de biometria, câmera e busca por CPF | Tratamentos de alto risco | Elaborar antes de ativar, com o DPO | Sem RIPD | [35](35-acesso-e-seguranca-fisica-por-portal.md), ACC-04 |
| J-38 | Termo de responsabilidade de equipamento e uso de espaço por menor | Empréstimo de equipamento e uso de quadra | Termo aceito no portal, com guarda pelo prazo da entidade | Sem termo | [44](44-agendamento-ambientes-equipamentos.md), AMB-06 e AMB-07 |

---

## 11. Campo de resposta

Use uma linha por código. O responsável preenche as colunas e devolve o pacote assinado.

| Código | Confirma | Corrige (posição correta e referência) | Recusa (motivo) | Responsável | Data |
|---|---|---|---|---|---|
| J-01 a J-38 | | | | | |
| N-01 a N-23 | | | | | |

---

## 12. Itens que não são de jurídico nem de norma

| Item | Responsável | Onde |
|---|---|---|
| Medição de capacidade de mídia, validade de cache e dimensionamento de Redis | Operação, em homologação | [10](10-implantacao-operacao.md), [30](30-cache.md) |
| Escolha do produto de armazenamento de longo prazo de auditoria | Operação | [29](29-auditoria.md), AUD-02 |
| Escolha de CDN | Operação | [30](30-cache.md), CAC-03 |
| Revisão dos DDL de todos os módulos novos | Owner de cada módulo | [51](51-ddl-modulos-novos.md) |

---

## 13. Referências a confirmar

Todas as citações marcadas **a confirmar** neste pacote precisam ser conferidas contra o texto vigente pelo jurídico. A lista está aqui para facilitar a conferência:

- LGPD (Lei 13.709/2018): arts. 11, 14, 18 e 19 **a confirmar**.
- Resolução CD/ANPD 15/2024, prazo de incidente **a confirmar**.
- Marco Civil da Internet (Lei 12.965/2014), art. 15 **a confirmar**.
- CDC, art. 43, §2º, e Lei 14.181/2021 **a confirmar**.
- CLT, art. 130 e demais regras de férias, rescisão e experiência **a confirmar**.
- Normas regulamentadoras NR-1, NR-5, NR-7 e NR-17 **a confirmar**.
- Lei 4.320/1964, empenho e fases da despesa **a confirmar**.
- Estrutura de ICP-Brasil para assinatura **a confirmar**.
