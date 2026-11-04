# 45 — Pendências Consolidadas, por Responsável

> Parte do [SDD v2](00-README.md). Reúne em um lugar o que ainda não foi respondido, a partir das tabelas de pendências de cada documento. Decisões já tomadas ficam nas próprias tabelas, marcadas como **Decidido**.
> **Status:** lista de trabalho, refeita por auditoria completa em 03/11/2026. Cada item tem o código e o documento de origem. Quando um item é respondido, a resposta vai para o documento de origem, e a linha sai desta lista.

---

## 0. Como esta lista foi montada

Auditoria de 03/11/2026 nos documentos 00 a 76:

1. Leitura de toda linha de tabela com código (por exemplo `BOL-08`) nas seções de pendências, lacunas e decisões. Foram 337 linhas.
2. Linha com **Decidido**, **Feito**, **Escrito**, **Mantido** ou **Aceita**, sem parte pendente, conta como fechada: 168 linhas.
3. As demais foram separadas pelo responsável que precisa agir: autor, jurídico, norma, documento, homologação ou owner.
4. Pendência que outro documento já resolveu teve o status corrigido no documento de origem. A lista das correções está na seção 9.

A versão anterior desta lista tinha seções separadas para os docs 00 a 54 e 55 a 72. Agora há uma lista só.

---

## 1. Resumo

| Responsável | Itens | O que se espera |
|---|---|---|
| Autor | 0 | Decisão de produto ou confirmação de proposta (seção 2) |
| Jurídico, sem decisão | 58 | Parecer escrito, com data e nome do responsável (seção 3.1) |
| Jurídico, decidido pelo autor | 14 | Parecer sobre a regra já adotada (seção 3.2) |
| Conferência de norma | 25 | Confirmar o texto da norma antes da implementação (seção 4) |
| Documento a escrever | 0 | Especificação ou modelo de dados (seção 5) |
| Homologação e operação | 12 | Medir, dimensionar ou escolher produto antes da produção (seção 6) |
| Revisão do owner | 40 | Revisar o que já foi escrito e testar a migração (seção 7) |

Os pacotes para o jurídico ([50](50-pacote-juridico-e-norma.md), [53](53-pacote-documentos-e-contratos.md) e [73](73-resumo-juridico-academico.md)) agrupam as mesmas perguntas por tema. Não são itens a mais.

---

## 2. Autor (decisão de produto)

Nenhum item de tabela aberto. OCO-01, BIB-04, IA-01, IA-07 e NOT-01, e o prazo de 2 dias úteis da [63](63-ocorrencias-disciplinares-por-portal.md), seção 4.1, foram decididos em 03/11/2026 (seção 9.1).

**PLA-04** também foi decidido em 03/11/2026: BNCC obrigatória no plano de ensino e opcional no plano de aula ([64](64-planos-de-aula-e-de-ensino-por-portal.md), seção 4.1).

Continuam com o autor, no texto corrido: Frotas nesta versão e lista de jurisdições (seções 8.5 e 8.2).

**Licenciamento e permissões:** todas as propostas dos documentos [77](77-licenciamento-planos-e-limites.md) e [78](78-permissoes-e-papeis.md) foram aprovadas em 04/11/2026 (seção 9.1). Em aberto: **D-42** (cheques e caixa físico no financeiro da plataforma) e **D-43** (papéis do financeiro da plataforma), em [78](78-permissoes-e-papeis.md), seção 6.

---

### 2.1 Especificações da v1 ainda não absorvidas na v2

Dezessete arquivos de [anexo-v1/](anexo-v1/) estão no catálogo, mas nenhum documento da v2 usa o conteúdo deles (lista e situação em [79](79-rastreabilidade-v1-v2.md), seção 3, situação "Só catalogado"). **Antes de implementar o módulo correspondente, a especificação da v1 deve ser lida e as regras trazidas para a v2.** Responsável: owner de cada módulo. Ao absorver, regerar o [79](79-rastreabilidade-v1-v2.md).

---

## 3. Jurídico (parecer)

### 3.1 Sem decisão

| Código | Pendência | Documento |
|---|---|---|
| IA-02 | Provedores de modelo permitidos e região de processamento | [27](27-inteligencia-artificial-e-portais.md) |
| IA-03 | Contrato de tratamento com provedor de modelo | [27](27-inteligencia-artificial-e-portais.md) |
| IA-04 | Termo de uso de IA para entidade | [27](27-inteligencia-artificial-e-portais.md) |
| IA-05 | Relatório de impacto dos recursos de risco alto | [27](27-inteligencia-artificial-e-portais.md) |
| ATD-03 | Retenção de tickets e de transcrição | [32](32-atendimento-privacidade-por-portal.md) |
| LGPD-03 | Método de consentimento parental para menor de 13 anos | [32](32-atendimento-privacidade-por-portal.md) |
| LGPD-04 | Bases legais por tipo de dado escolar, incluindo menores | [32](32-atendimento-privacidade-por-portal.md) |
| LGPD-05 | Transferência internacional, se houver cliente fora do Brasil | [32](32-atendimento-privacidade-por-portal.md) |
| LGPD-06 | Painel do DPO e RIPD (G-05) | [32](32-atendimento-privacidade-por-portal.md) |
| LGPD-08 | Prazo de comunicação de incidente (três dias úteis, Resolução 15/2024) | [32](32-atendimento-privacidade-por-portal.md) |
| CTR-04 | Forma de assinatura por tipo de contrato | [33](33-contratos-por-portal.md) |
| CTR-05 | Cláusulas obrigatórias por tipo | [33](33-contratos-por-portal.md) |
| CTR-07 | Contrato de matrícula: forma, cláusulas e prazo de guarda | [33](33-contratos-por-portal.md) |
| PAG-04 | NFS-e Nacional, cancelamento, guarda de XML (seção 5.2) | [34](34-pagamentos-fiscal-bancos-por-portal.md) |
| PAG-05 | NFS-e da assinatura SaaS (plataforma) | [34](34-pagamentos-fiscal-bancos-por-portal.md) |
| PAG-07 | Open Finance e débito automático | [34](34-pagamentos-fiscal-bancos-por-portal.md) |
| ACC-04 | RIPD de biometria e de câmera | [35](35-acesso-e-seguranca-fisica-por-portal.md) |
| TER-03 | Base legal do transporte escolar e de restrição alimentar | [38](38-portal-de-terceiros-prestadores.md) |
| LIV-01 | Consentimento de responsável para gravação e para entrada de aluno menor sem gravação (seção 5). Pedido por cláusula do contrato com a instituição | [40](40-aulas-online-por-portal.md) |
| LIV-02 | Prazo de retenção de gravação e transcrição, padrão 30 dias (seção 5) | [40](40-aulas-online-por-portal.md) |
| FRM-03 | Base legal para coleta de dado sensível em formulário (seção 4) | [41](41-formularios-e-pesquisas.md) |
| FRM-06 | Prazo de guarda de resposta de formulário, por tipo | [41](41-formularios-e-pesquisas.md) |
| PRE-05 | Prazo de guarda de avaliação, tutoria e PDI | [42](42-preceptoria-por-portal.md) |
| PRE-06 | Consentimento para tutoria de aluno menor com dado sensível (seção 5) | [42](42-preceptoria-por-portal.md) |
| PAS-03 | Retenção de intenção de missa (seção 3.3) | [43](43-pastoral-por-portal.md) |
| PAS-04 | Retenção de cadastro de beneficiário (seção 4) | [43](43-pastoral-por-portal.md) |
| PAS-05 | Consentimento de menor para evento, escala e imagem (seção 6) | [43](43-pastoral-por-portal.md) |
| PAS-06 | Campanhas com renda: base legal de coleta (seção 4) | [43](43-pastoral-por-portal.md) |
| AMB-06 | Termo de responsabilidade de equipamento: texto e guarda | [44](44-agendamento-ambientes-equipamentos.md) |
| AMB-07 | Regra de uso de espaço esportivo por menor fora do horário escolar | [44](44-agendamento-ambientes-equipamentos.md) |
| MAT-01 | Lista de documentos obrigatórios por nível e se algum pode bloquear, não só condicionar (M-08) | [46](46-matricula-e-rematricula-por-portal.md) |
| SIM-01 | Prazo de guarda de redação original e de transcrição (seção 10) | [47](47-simulados-por-portal.md) |
| SIM-02 | Uso de nome de exame oficial (ENEM e outros) no perfil, e a permissão de uso | [47](47-simulados-por-portal.md) |
| DOC-02 | Prazo de guarda de cada tipo emitido (histórico, declaração, certidão) | [48](48-gerador-de-documentos-por-portal.md) |
| DDL-03 | Valores de domínio marcados (jurídico) no [50](50-pacote-juridico-e-norma.md) | [51](51-ddl-modulos-novos.md) |
| GD-02 | Prazo de guarda de documento recebido, por tipo (matrícula, fornecedor, candidato) | [54](54-gestao-de-documentos-tres-contextos.md) |
| NOT-04 | Prazo de retenção do corpo da mensagem (seção 3.7) | [57](57-notificacoes-por-portal.md) |
| CAL-04 | Certificado de evento: prazo de guarda | [58](58-calendario-e-eventos-por-portal.md) |
| EST-06 | Ato de autorização e reconhecimento do curso: formato e validade (seção 3.1) | [59](59-estrutura-academica-por-portal.md) |
| BOL-08 | Prazo de guarda de boletim e de ata | [62](62-boletim-e-conselho-de-classe-por-portal.md) |
| OCO-06 | Protocolo de violência: canal e prazo de encaminhamento (seção 6.3) | [63](63-ocorrencias-disciplinares-por-portal.md) |
| OCO-07 | Prazo de guarda de ocorrência e de medida | [63](63-ocorrencias-disciplinares-por-portal.md) |
| ETC-05 | Publicação de TCC em repositório: autorização do aluno e prazo de acesso (seção 3.6) | [65](65-estagio-e-tcc-por-portal.md) |
| PRT-07 | Revisão jurídica do acesso da secretaria e da coordenação ao CID (PRT-01), à luz da minimização de dado | [66](66-prontuario-e-portfolio-do-aluno-por-portal.md) |
| PRT-03 | Guarda do prontuário após saída do aluno (seção 2.4). Mesmo ponto de N-10 | [66](66-prontuario-e-portfolio-do-aluno-por-portal.md) |
| PRT-04 | Imagem de menor em portfólio: autorização e prazo (seção 3.1). Mesmo ponto de LIV-13 de [40](40-aulas-online-por-portal.md) | [66](66-prontuario-e-portfolio-do-aluno-por-portal.md) |
| ARQ-02 | Prazo de guarda por tipo de documento e de livro (seção 4.4). Mesmo ponto de N-10 e J-04 | [67](67-livros-digitais-e-arquivo-morto-por-portal.md) |
| ARQ-03 | O original em papel pode ser eliminado depois de digitalizado e verificado (seção 4.3) | [67](67-livros-digitais-e-arquivo-morto-por-portal.md) |
| ARQ-06 | Assinatura de ata: simples ou ICP-Brasil, por tipo de ata. Mesmo ponto de N-12 | [67](67-livros-digitais-e-arquivo-morto-por-portal.md) |
| BIB-05 | Marca d'água de leitura digital com identificação do leitor: base legal e licença do editor (seção 8) | [68](68-biblioteca-por-portal.md) |
| BIB-07 | Guarda de histórico de leitura e de empréstimo, e prazo de eliminação | [68](68-biblioteca-por-portal.md) |
| REL-02 | Prazo de guarda do arquivo gerado de relatório regulatório | [69](69-relatorios-e-censo-por-portal.md) |
| IMP-03 | Laudos e dados de saúde na importação: aceitar, ou bloquear e tratar na seção de saúde | [70](70-importacao-de-dados-por-portal.md) |
| IMP-04 | Prazo de retenção do arquivo de origem depois da gravação (seção 4, passo 8) | [70](70-importacao-de-dados-por-portal.md) |
| FIN-06 | Guarda física de cheque recebido e prazo (seção 5.3) | [71](71-financeiro-completo-por-portal.md) |
| CPF-03 | Prazo de guarda de valor de campo removido (seção 4) | [72](72-campos-personalizados-por-portal.md) |
| INT-04 | Termo de adesão à plataforma federal (SGP), e quem assina (seção 3.3) | [74](74-integracoes-educacionais-oficiais.md) |
| INT-05 | Dado de localização no arquivo do SIGEP (seção 3.2). Mesmo ponto de TER-02 | [74](74-integracoes-educacionais-oficiais.md) |

Itens do dossiê jurídico ([25](25-dossie-juridico-e-lacunas.md)) que continuam abertos: **Q-01 (G-02)**, retenção de consulta por CPF, com **prioridade máxima**; e **G-03**, base legal de legítimo interesse (Q-03 a Q-06).

### 3.2 Decidido pelo autor, falta o parecer

A regra já vale no SDD. O parecer confirma ou pede ajuste.

| Código | Pendência | Documento |
|---|---|---|
| SEG-01 | Regra de verificação do vínculo de responsabilidade legal | [31](31-matriz-portais-modulos.md) |
| ACC-02 | Biometria e reconhecimento facial: escopo (seção 5) | [35](35-acesso-e-seguranca-fisica-por-portal.md) |
| ACC-03 | Retenção de imagem de câmera (seção 6) | [35](35-acesso-e-seguranca-fisica-por-portal.md) |
| TER-02 | Prazo de guarda do rastro de localização do transporte escolar (seção 11) | [38](38-portal-de-terceiros-prestadores.md) |
| FRM-02 | Revisão humana de comentário livre antes de exibir (seção 3, item 5) | [41](41-formularios-e-pesquisas.md) |
| PAS-02 | Acompanhamento espiritual: adesão voluntária e visibilidade só do acompanhante (seção 2.2) | [43](43-pastoral-por-portal.md) |
| NOT-05 | Remetentes de aviso de saúde ou enfermagem (seção 4) | [57](57-notificacoes-por-portal.md) |
| CTR-06 | Provedor de assinatura eletrônica | [33](33-contratos-por-portal.md) |
| HCM-09 | Recrutamento: prazo de guarda de currículo de não contratado (seção 11) | [39](39-departamento-pessoal-rh-medicina-por-portal.md) |
| OCO-02 | Quem aplica afastamento (seção 5.3) | [63](63-ocorrencias-disciplinares-por-portal.md) |
| AUD-01 | Prazo de retenção de eventos de plataforma: **5 anos, aprovado pelo autor em 03/11/2026.** Registrar parecer jurídico quando houver ([25](25-dossie-juridico-e-lacunas.md), Q-01). | [29](29-auditoria.md) |
| IA-07 | Uso de dado de tenant para melhoria de produto: não usar sem consentimento específico | [27](27-inteligencia-artificial-e-portais.md) |
| ETC-02 | Bolsa, auxílio e seguro no estágio: texto da Lei 11.788/2008 conferido e registrado | [65](65-estagio-e-tcc-por-portal.md) |
| SST-05 | Guarda de documentos de SST: prontuário conferido (20 anos, NR-7, 7.6.1.1). Falta o parecer sobre os demais documentos | [52](52-medicina-do-trabalho-especificacao.md) |

---

## 4. Conferência de norma (verificar)

Itens que tratam do mesmo ponto: REL-01 e INT-02 (censo). Uma resposta vale para todos.

| Código | Pendência | Documento |
|---|---|---|
| PLN-01 | Obrigação de plano institucional e órgão colegiado aprovador, por tipo de entidade | [37](37-planejamento-e-empenho.md) |
| PLN-02 | Lei 4.320/1964 e normas do órgão de controle para o empenho (conferido em parte: Lei 4.320, arts. 36 e 58 a 65. Faltam as normas do tribunal de contas) | [37](37-planejamento-e-empenho.md) |
| TER-06 | Validade do selo do cartório digital por tipo de ato | [38](38-portal-de-terceiros-prestadores.md) |
| TER-07 | Documentos exigidos por tipo (alvará, seguro, certidões) | [38](38-portal-de-terceiros-prestadores.md) |
| HCM-02 | Catálogo de verbas e tabelas de INSS, IRRF e FGTS por competência | [39](39-departamento-pessoal-rh-medicina-por-portal.md) |
| HCM-03 | Regra de férias, 13.º e rescisão (L-12) | [39](39-departamento-pessoal-rh-medicina-por-portal.md) |
| HCM-04 | Eventos eSocial S-2200, S-1200, S-1210, S-2299 | [39](39-departamento-pessoal-rh-medicina-por-portal.md) |
| HCM-05 | Ponto e jornada: regra de registro e controle (conferido em parte: CLT, arts. 66, 71 e 74. Professor conferido. Faltam a Portaria MTP 671/2021 e o estatuto do servidor) | [39](39-departamento-pessoal-rh-medicina-por-portal.md) |
| PRE-04 | Regra de regulamento de residência e avaliação por programa | [42](42-preceptoria-por-portal.md) |
| DOC-01 | Quais tipos exigem assinatura com certificado ICP-Brasil (seção 8) (conferido em parte: Lei 14.063/2020. Faltam as normas do MEC para diploma e histórico) | [48](48-gerador-de-documentos-por-portal.md) |
| DOC-03 | Layout oficial do histórico escolar, conforme norma do sistema de ensino (Res. CNE/CEB, citada na v1) | [48](48-gerador-de-documentos-por-portal.md) |
| GD-06 | Documento administrativo de entidade pública: regra de processo administrativo (conferido em parte: Lei 9.784/1999 no federal. Falta a lei de cada ente) | [54](54-gestao-de-documentos-tres-contextos.md) |
| EST-02 | Carga horária mínima por nível, e regra de créditos no superior (seção 2) (conferido em parte: educação básica na LDB. Falta o superior, por curso) | [59](59-estrutura-academica-por-portal.md) |
| TUR-04 | Carga horária mínima de aula e de intervalo, por nível de ensino (conferido em parte: aula mínima na LDB. Falta o intervalo) | [60](60-turmas-e-grade-de-horarios-por-portal.md) |
| DIA-03 | Falta justificada conta ou não na frequência, por nível de ensino (seção 4.2) (conferido em parte: a LDB não abona. Faltam os regimes especiais) | [61](61-diario-escolar-por-portal.md) |
| DIA-09 | Lista de alunos para o Conselho Tutelar (LDB, art. 12, VIII): cálculo e periodicidade | [61](61-diario-escolar-por-portal.md) |
| BOL-02 | Regra de combinação do resultado do período (seção 3.1, último parágrafo) | [62](62-boletim-e-conselho-de-classe-por-portal.md) |
| OCO-08 | Efeito de afastamento na frequência (seção 5.3) | [63](63-ocorrencias-disciplinares-por-portal.md) |
| ETC-08 | Nova tentativa de TCC reprovado (seção 3.3) | [65](65-estagio-e-tcc-por-portal.md) |
| PRT-05 | Restrição alimentar e medicamento de uso escolar: documento e validade exigidos (seção 2.3) | [66](66-prontuario-e-portfolio-do-aluno-por-portal.md) |
| ARQ-04 | Formato e órgão de envio do livro de registro por tipo de sistema de ensino (seção 2.3) | [67](67-livros-digitais-e-arquivo-morto-por-portal.md) |
| REL-01 | Layout e prazo do censo, por esfera e por ano (seção 4.1) | [69](69-relatorios-e-censo-por-portal.md) |
| FIN-03 | Comprovante de IRPF do pagador: obrigação, formato e prazo (seção 10) | [71](71-financeiro-completo-por-portal.md) |
| INT-02 | Layout e prazo do Educacenso, por ano e por esfera (seção 3.1) (conferido em parte: obrigação no Decreto 6.425/2008. Layout e prazo vêm do ato anual, conferir a cada ciclo) | [74](74-integracoes-educacionais-oficiais.md) |
| INT-06 | Layout do SIGEP e se o monitor é pessoa do terceiro (seção 3.2) | [74](74-integracoes-educacionais-oficiais.md) |

---

## 5. Documento a escrever

Nenhum item aberto. Os oito itens desta seção foram escritos em 03/11/2026 (seção 9.2).

---

## 6. Homologação e operação

| Código | Pendência | Documento |
|---|---|---|
| AUD-02 | Armazenamento de longo prazo e ancoragem: **decidido pelo autor em 03/11/2026**, com a exportação diária assinada da seção 3. Escolha do produto concreto e teste de restauração ficam para homologação. | [29](29-auditoria.md) |
| CAC-01 | Dimensionamento do Redis por ambiente e entidade. **Decisão do autor (03/11/2026):** dimensionar em homologação antes de produção. | [30](30-cache.md) |
| CAC-02 | Validades medidas em homologação. **Decisão do autor (03/11/2026):** medir em homologação; os valores da seção 4 são o ponto de partida. | [30](30-cache.md) |
| CAC-03 | Escolha do provedor de CDN | [30](30-cache.md) |
| LIV-13 | Valores de capacidade: fragmento de 60 segundos (**decidido** em 03/11/2026), bitrate, salas por nó e limite de perda de pacote | [40](40-aulas-online-por-portal.md) |
| DOC-07 | Prazos de lembrete de assinatura e de revisão (seção 19) | [48](48-gerador-de-documentos-por-portal.md) |
| DOC-08 | Limite de tamanho do lote (seção 14) | [48](48-gerador-de-documentos-por-portal.md) |
| GD-04 | Formato e tamanho máximo de arquivo recebido, por contexto | [54](54-gestao-de-documentos-tres-contextos.md) |
| TST-04 | Ferramenta de varredura de acessibilidade, com versão fixada | [49](49-logs-testes-por-portal.md) |
| REL-04 | Limite de linhas para geração imediata (seção 2.2) | [69](69-relatorios-e-censo-por-portal.md) |
| AUD-03 | Central de segurança: escolha do produto e teste de envio (regra na seção 8.1) | [29](29-auditoria.md) |
| DDL-02 | Teste de migração em ambiente de homologação por banco de unidade ([10](10-implantacao-operacao.md), seção 5) | [51](51-ddl-modulos-novos.md) |

---

## 7. Revisão do owner

O texto ou o DDL já existe. Falta a revisão do owner do módulo e, no caso de DDL, o teste de migração (DDL-02).

| Código | Pendência | Documento |
|---|---|---|
| DDL-01 | Revisão de cada DDL pelo owner do módulo antes da migração | [51](51-ddl-modulos-novos.md) |
| GD-08 | Revisão do DDL pelo owner de cada contexto e teste de migração | [54](54-gestao-de-documentos-tres-contextos.md) |

Itens escritos que aguardam essa revisão: MOD-07, MOD-08, MOD-09, ATD-04, LGPD-01, LGPD-02, CTR-01, ACC-06, ACC-08, TI-04, HCM-07, LIV-10, FRM-05, PRE-08, PAS-10, AMB-08, MAT-07, DOC-06, NOT-07, CAL-05, EST-07, TUR-05, DIA-08, BOL-10, OCO-09, PLA-07, ETC-09, PRT-06, ARQ-07, BIB-08, REL-07, IMP-06, FIN-08, CPF-04, PER-07, SIM-07, INT-07, IMP-05.

---

## 8. Itens no texto corrido (regras com [Pendente] e marcadores de conferência)

Esta seção foi montada por varredura dos marcadores `[Pendente`, `Pendente:`, `(verificar)`, `a confirmar` e `[Decisão pendente]` nos docs 00 a 39. Os itens abaixo não estão nas tabelas de pendências, e cada um tem um dono sugerido. A seção 9 da [24](24-operacao-continuidade-qualidade.md) (G-20) já prevê a revisão dessas regras.

### 8.1 Valores que faltam (autor ou owner do módulo)

| Documento | Item | Dono sugerido |
|---|---|---|
| [17](17-regras-modulos.md) | Prazo máximo de trancamento, por regimento de cada curso | Acadêmico |
| [21](21-busca-e-armazenamento.md) | Prazo de backup que propaga o expurgo (35 dias proposto) | Operação |
| [06](06-identidade-acesso.md) | Versão vigente da NIST SP 800-63B-4, a confirmar antes do go-live | Segurança |

### 8.2 Regras que dependem de município, UF ou tipo de vínculo

| Documento | Item | Dono sugerido |
|---|---|---|
| [17](17-regras-modulos.md) | Formato de RG por UF | Pessoas (RH) |
| [18](18-regras-modulos-2.md) | Emissão de nota fiscal conforme política do município | Fiscal (verificar) |
| [19](19-regras-modulos-3.md) | Lista de jurisdições, só se houver cliente fora do Brasil | Autor |
| [19](19-regras-modulos-3.md) | Quem revisa o conteúdo gerado por IA antes de publicar (parcialmente resolvido por MOD-06 para simulado) | Acadêmico |

### 8.3 Itens de norma (verificar)

| Documento | Item | Dono sugerido |
|---|---|---|
| [17](17-regras-modulos.md) | Idade mínima para vínculo, por tipo | Jurídico |
| [17](17-regras-modulos.md) | Contrato de experiência: texto contraditório da v1 (L-03) | Jurídico |
| [18](18-regras-modulos-2.md) | Férias: período e fracionamento, CLT art. 130 | Jurídico e norma |
| [20](20-pagamentos-seguranca.md) | Prazo de resposta a chargeback, em 3 dias | Norma da bandeira (verificar) |
| [37](37-planejamento-e-empenho.md) | Plano institucional, colegiado e Lei 4.320 art. 61 e seguintes (também em PLN-01 e PLN-02) | Norma |
| [38](38-portal-de-terceiros-prestadores.md) | Validade jurídica do selo do cartório, por tipo de ato | Norma |
| [38](38-portal-de-terceiros-prestadores.md) | Verificação de CNPJ em base pública, e exigência de cadastro público de fornecedor | Norma |
| [39](39-departamento-pessoal-rh-medicina-por-portal.md) | Evento S-2200 de admissão, eSocial (também em HCM-04) | Norma |
| [39](39-departamento-pessoal-rh-medicina-por-portal.md) | Controle de jornada conforme legislação (também em HCM-05) | Norma |
| [39](39-departamento-pessoal-rh-medicina-por-portal.md) | Cálculo de aviso prévio, férias proporcionais, 13.º e multa do FGTS | Norma |
| [39](39-departamento-pessoal-rh-medicina-por-portal.md) | Regra de benefício e de elegibilidade por cargo | Norma e RH |
| [39](39-departamento-pessoal-rh-medicina-por-portal.md) | LTCAT, CAT ao INSS (canal e prazo), NR aplicáveis e validade de treinamento por NR | Norma e medicina do trabalho |

### 8.4 Jurídico (texto de lei e de contrato)

| Documento | Item | Dono sugerido |
|---|---|---|
| [07](07-privacidade-lgpd.md) | Base legal de cada finalidade, com setorial a confirmar | Jurídico |
| [07](07-privacidade-lgpd.md) | Prazo de guarda de documentos escolares | Jurídico |
| [21](21-busca-e-armazenamento.md) | Base legal por finalidade da busca por CPF | Jurídico |
| [25](25-dossie-juridico-e-lacunas.md) | Prazo de registro de acesso (seis meses, Marco Civil art. 15) | Jurídico |
| [25](25-dossie-juridico-e-lacunas.md) | Comunicação de inclusão de inadimplente (CDC art. 43, §2º) | Jurídico |
| [25](25-dossie-juridico-e-lacunas.md) | Superendividamento na régua de cobrança (Lei 14.181/2021) | Jurídico |
| [25](25-dossie-juridico-e-lacunas.md) | Base para SMS, WhatsApp e Telegram em cobrança e marketing | Jurídico |
| [25](25-dossie-juridico-e-lacunas.md) | Súmula 362 do TST para FGTS e documentos trabalhistas | Jurídico |
| [25](25-dossie-juridico-e-lacunas.md) | Forma de registro do consentimento de marketing | Jurídico |
| [32](32-atendimento-privacidade-por-portal.md) | DPO designado pela entidade, com contrato com a empresa desenvolvedora | Jurídico |

### 8.5 Pendências de produto e de licença

| Documento | Item | Dono sugerido |
|---|---|---|
| [05](05-seguranca.md) e [11](11-governanca-qualidade.md) | Confirmar uso de `JWT_SECRET` no código e remover HS256 (ACH-05) | Backend |
| [12](12-catalogo-modulos.md) | Frotas: confirmar se entra nesta versão, pois é de escopo diferente do educacional | Autor |
| [31](31-matriz-portais-modulos.md) | Atendimento consolidado: DDL pendente (T-02) | Documento |

---

## 9. Correções feitas nesta auditoria

Status atualizado no documento de origem, porque a pendência já tinha sido resolvida em outro documento:

| Itens | O que mudou |
|---|---|
| ATD-04, LGPD-01, LGPD-02, CTR-01, ACC-06, ACC-08, FRM-05, PRE-08, PAS-10, AMB-08, LIV-10, MAT-07, TI-04, DOC-06 | DDL escrito em [51](51-ddl-modulos-novos.md), seções 1 a 12 |
| NOT-07, CAL-05, EST-07, TUR-05, DIA-08, BOL-10, OCO-09, PLA-07, ETC-09, PRT-06, ARQ-07, BIB-08, REL-07, IMP-06, FIN-08, CPF-04 | DDL escrito em [51](51-ddl-modulos-novos.md), seção 15 |
| MOD-07, MOD-08, MOD-09 | Especificados em [48](48-gerador-de-documentos-por-portal.md), [47](47-simulados-por-portal.md) e [46](46-matricula-e-rematricula-por-portal.md) |
| MOD-10, MOD-11 | Escritos em [68](68-biblioteca-por-portal.md) e [32](32-atendimento-privacidade-por-portal.md) |
| LOG-01, LOG-02, TST-01, TST-02, TST-03 | Escritos em [49](49-logs-testes-por-portal.md). Na matriz de logs de [31](31-matriz-portais-modulos.md), integração e job deixam de aparecer como "sem especificação" |
| AUD-04 | Campo `portal` em [29](29-auditoria.md), seção 2 |
| TI-01, TI-02, TI-03 | Escritos em [36](36-tecnologia-da-informacao-por-portal.md), seção 11 |
| HCM-07 | Escrito em [52](52-medicina-do-trabalho-especificacao.md) |
| LIV-09 | Fechado por ACC-05 de [35](35-acesso-e-seguranca-fisica-por-portal.md) |
| PER-02, PER-03 | Fechados por PER-06 e PER-05 de [76](76-meu-perfil-por-portal.md) |
| SRC-01 a SRC-05, PER-04, PER-05 | Marca **[Decisão do autor]** retirada do texto de [75](75-busca-notificacoes-perfil-integracoes-por-escopo.md). A decisão já estava na tabela |
| Formulários | Em [41](41-formularios-e-pesquisas.md), seção 3, item 4, saiu "valor padrão proposto: 5", que contradizia a decisão de mínimo de 2 respostas |
| CFG-01 | Em [56](56-configuracoes-e-relatorios-lacunas.md), eventos deixam de ser lacuna, porque estão em [58](58-calendario-e-eventos-por-portal.md) |
| MOD-12 | Continua aberto. "Gerador de documentos" já é o nome usado. Falta "Editor de portais" em [23](23-dominios-provisionamento-ciclo-de-vida.md) |

### 9.1 Decisões do autor depois da auditoria

| Item | Decisão de 03/11/2026 |
|---|---|
| OCO-01 | Tipos de ocorrência: lista padrão da plataforma, que a escola ajusta ([63](63-ocorrencias-disciplinares-por-portal.md)) |
| Prazo de registro | Ocorrência com data anterior: motivo obrigatório depois de 2 dias úteis ([63](63-ocorrencias-disciplinares-por-portal.md), seção 4.1) |
| BIB-04 | Valor inicial da plataforma, que a escola ajusta: aluno 3 itens por 7 dias, professor e servidor 5 itens por 30 dias, até 2 renovações ([68](68-biblioteca-por-portal.md), seção 4) |
| IA-01 | IA dentro do plano, com a quota de IA-06. Excedente cobrado conforme o contrato ([27](27-inteligencia-artificial-e-portais.md)) |
| IA-07 | Não usar dado de cliente sem consentimento específico. Falta o parecer do jurídico (seção 3.2) |
| NOT-01 | As duas versões da v1 são unidas. Telas e painel da original em [57](57-notificacoes-por-portal.md), seções 3.8 e 3.9, que também fecham NOT-08 |
| L-01 | Cada plano tem limite de alunos, definido pelo desenvolvedor da plataforma. **Aprovada em 04/11/2026** ([77](77-licenciamento-planos-e-limites.md), seção 1) |
| L-02 | Criar entidade e criar unidade é exclusivo do papel `platform.developer`. **Aprovada em 04/11/2026** ([78](78-permissoes-e-papeis.md), seção 1) |
| P-01 | Sistema de permissões completo, com níveis de papel, para todos os portais. **Aprovada em 04/11/2026** ([78](78-permissoes-e-papeis.md)) |
| D-33 | Quem aprova a publicação no Editor de portais é `platform.developer`, diferente de quem edita (`platform.builder`). **Aprovada em 04/11/2026** ([78](78-permissoes-e-papeis.md), seção 6) |
| D-27 | Ao exceder o limite de alunos, bloquear novas matrículas ativas, sem alterar dados existentes. **Aprovada em 04/11/2026** ([77](77-licenciamento-planos-e-limites.md), seção 4) |
| D-28 | Carência de 15 dias na inadimplência, ajustável por plano. **Aprovada em 04/11/2026** ([77](77-licenciamento-planos-e-limites.md), seção 3.1) |
| D-29 | Preço e ciclo definidos pelo desenvolvedor, por plano. **Aprovada em 04/11/2026** ([77](77-licenciamento-planos-e-limites.md), seção 2) |
| D-30 | Códigos dos papéis de gestão como na seção 4 do [78](78-permissoes-e-papeis.md). **Aprovada em 04/11/2026** |
| D-31 | Professor que também coordena: dois papéis, um por portal. **Aprovada em 04/11/2026** ([78](78-permissoes-e-papeis.md)) |
| D-32 | Responsável com mais de um aluno: escopo `proprio` com dependentes vinculados. **Aprovada em 04/11/2026** ([78](78-permissoes-e-papeis.md)) |
| D-34 | Nome e código do plano únicos na plataforma. **Aprovada em 04/11/2026** ([77](77-licenciamento-planos-e-limites.md), seção 2) |
| D-35 | Cada plano tem uma lista de módulos; a entidade só vê no portal os módulos do plano. **Aprovada em 04/11/2026** ([77](77-licenciamento-planos-e-limites.md), seção 2) |
| D-36 | Plano ativo ou descontinuado; descontinuado não aceita novas assinaturas. **Aprovada em 04/11/2026** ([77](77-licenciamento-planos-e-limites.md), seção 2) |
| D-37 | Assinatura ativa, inadimplente, suspensa ou cancelada, com os efeitos da seção 3.1. **Aprovada em 04/11/2026** ([77](77-licenciamento-planos-e-limites.md)) |
| D-38 | Oito níveis de papel, de 0 (próprio) a 7 (desenvolvedor). **Aprovada em 04/11/2026** ([78](78-permissoes-e-papeis.md), seção 2.1) |
| D-39 | Separação de funções nas ações da seção 2.2. **Aprovada em 04/11/2026** ([78](78-permissoes-e-papeis.md)) |
| D-40 | Seis regras transversais de permissão. **Aprovada em 04/11/2026** ([78](78-permissoes-e-papeis.md), seção 5) |
| D-41 | Códigos dos papéis comerciais da plataforma: `platform.sales.sdr`, `platform.sales.ae`, `platform.sales.manager`, `platform.chatbot.operator` e `platform.customer_success`. **Aprovada em 04/11/2026** ([78](78-permissoes-e-papeis.md), seção 4.1) |

### 9.2 Documentos escritos depois da auditoria

| Item | Onde |
|---|---|
| SIM-07 | DDL de simulados e redação em [51](51-ddl-modulos-novos.md), seção 15.19 |
| INT-07 | DDL de integrações educacionais em [51](51-ddl-modulos-novos.md), seção 15.20 |
| PAG-01 | EFÍ e contingência de gateway por unidade em [34](34-pagamentos-fiscal-bancos-por-portal.md), seções 2.1 e 2.3. Lista de adapters corrigida em [16](16-integracoes-externas.md) |
| LOG-05 | Conectores com log em [49](49-logs-testes-por-portal.md), seção 2.1 |
| TST-05 | Geração do teste de isolamento a partir da matriz em [49](49-logs-testes-por-portal.md), seção 5.1 |
| IMP-05 | Modelos de arquivo de importação em [70](70-importacao-de-dados-por-portal.md), seção 4.1 |
| AUD-03 | Envio para central de segurança em [29](29-auditoria.md), seção 8.1. Produto fica para homologação |
| MOD-12 | "Editor de portais" em [23](23-dominios-provisionamento-ciclo-de-vida.md), [27](27-inteligencia-artificial-e-portais.md), [29](29-auditoria.md) e [31](31-matriz-portais-modulos.md). "Editor de modelos" em [48](48-gerador-de-documentos-por-portal.md). O código do papel `platform.builder` foi mantido |

### 9.3 Conferência de norma feita em 03/11/2026

Texto lido em planalto.gov.br: LDB (Lei 9.394/1996, com a redação da Lei 14.945/2024) e Lei do Estágio (Lei 11.788/2008, com a redação da Lei 14.913/2024). A conferência registra o que a lei diz. Não é parecer jurídico. O art. 47 da LDB (superior), lido antes em resumo, foi conferido no texto literal na seção 9.7.

| Item | Resultado |
|---|---|
| CAL-01 | Fechado. A LDB não fixa recesso. O calendário se adapta ao local, sem reduzir horas (art. 23, § 2º) |
| EST-01 e BOL-01 | 75% no fundamental e no médio (art. 24, VI). 60% na pré-escola (art. 31, IV). Falta o superior |
| EST-02 | 800 h no fundamental e 1.000 h no médio, em 200 dias (art. 24, I). Formação geral básica de 2.400 h (art. 35-C). Falta o superior |
| TUR-04 | 4 h diárias de aula no fundamental (art. 34). 4 h e 7 h na educação infantil (art. 31, III). Falta o intervalo |
| DIA-03 | A LDB não abona falta justificada. A exceção é o motivo religioso (art. 7º-A). Faltam os regimes especiais de lei própria |
| DIA-09 | Item novo: a escola notifica ao Conselho Tutelar os alunos acima de 30% do percentual de faltas permitido (art. 12, VIII) |
| PLA-04 | Fechado. Base nacional comum obrigatória no currículo (art. 26). Decidido: BNCC obrigatória no plano de ensino e opcional no plano de aula |
| ETC-01 | Fechado. 4 h e 20 h, ou 6 h e 30 h, por tipo de aluno. Até 40 h com alternância. Até 2 anos no mesmo concedente (arts. 10 e 11) |
| ETC-03 | Fechado. A lei remete ao projeto do curso (art. 2º, § 1º) |
| ETC-02 | Texto conferido: bolsa e auxílio-transporte obrigatórios no não obrigatório, seguro em todo estágio, recesso de 30 dias (arts. 9º, 12 e 13). Fica o parecer |

### 9.4 Conferência de norma de saúde e segurança do trabalho, em 03/11/2026

Texto lido nos PDFs oficiais do Ministério do Trabalho e Emprego (gov.br): NR-1 (atualizada em 2025, capítulo 1.5 em vigor desde 26/05/2026), NR-5 (Portaria MTP nº 4.219/2022) e NR-7 (atualizada em 2022). Lei 8.213/1991, art. 58, lida no Planalto. Registro do que a norma diz, não parecer.

| Item | Resultado |
|---|---|
| SST-01 | Fechado. Periódico anual para exposto a risco ou doente crônico, a cada dois anos para os demais. Retorno após 30 dias de ausência. Demissional em até 10 dias, dispensado se o último exame tiver menos de 135 ou 90 dias, por grau de risco (NR-7, 7.5.8 a 7.5.11) |
| SST-02 | Fechado. LTCAT sem prazo fixo, mantido atualizado. PPP atualizado e entregue na rescisão (Lei 8.213, art. 58). Fica para conferir a entrega do PPP pelo eSocial |
| SST-03 | Fechado. CIPA por estabelecimento, pelo Quadro I. Mandato de um ano com uma reeleição. Estabilidade até um ano após o mandato. Eleição convocada 60 dias antes. Reunião mensal. Treinamento de 8 a 20 horas (NR-5) |
| SST-04 | Fechado. Revisão do PGR a cada dois anos, ou três com certificação, e antes nos casos do item 1.5.4.4.6. Histórico do inventário por 20 anos (NR-1) |
| HCM-08 e SST-05 | Prontuário guardado por no mínimo 20 anos após o desligamento (NR-7, 7.6.1.1). SST-05 fica com o jurídico para os demais documentos |
| TER-05 | Fechado. O contrato com a clínica garante a guarda por 20 anos e a transferência do prontuário (NR-7, 7.6.1.2). Fica para conferir a regra do CFM para prontuário eletrônico |
| Novo no PGR | Riscos psicossociais relacionados ao trabalho entram no inventário (NR-1, Portaria MTE nº 1.419/2024) |
| Novo na CIPA | Nome atual: Comissão Interna de Prevenção de Acidentes e de Assédio |

### 9.5 Conferência de ponto, alimentação, censo e Pé-de-Meia, em 03/11/2026

Textos lidos: CLT (Decreto-Lei 5.452/1943, com a Lei 13.874/2019), Decreto 6.425/2008 e Lei 14.818/2024 no Planalto; RDC ANVISA nº 216/2004 na Biblioteca Virtual em Saúde. Registro do que a norma diz, não parecer.

| Item | Resultado |
|---|---|
| HCM-05 | Em parte. Registro de entrada e saída obrigatório acima de 20 trabalhadores por estabelecimento, ponto por exceção só com acordo, intervalos de 11 horas, de 1 a 2 horas e de 15 minutos (CLT, arts. 66, 71 e 74). Faltam a Portaria MTP nº 671/2021 e as regras do professor e do servidor |
| TER-04 | Fechado. Limites de temperatura, identificação e guarda de 30 dias pela RDC 216/2004, itens 4.8 a 4.11. Fica para conferir norma sanitária local e se há RDC posterior |
| INT-02 | Em parte. Obrigação de todo estabelecimento e responsáveis (Decreto 6.425/2008, arts. 2º a 6º). O decreto não fixa data, prazo nem layout: vêm do ato anual, guardado como versão por ano |
| INT-03 | Fechado. Ensino médio público e CadÚnico, frequência mínima de 80%, aportes pelo menos 9 vezes por ano, verificação federal (Lei 14.818/2024, arts. 1º, 3º, 4º e 5º). Decreto 11.901/2024 conferido na seção 9.7 |

### 9.6 Conferência de empenho, assinatura e processo administrativo, em 03/11/2026

Textos lidos no Planalto: Lei 4.320/1964, Lei 14.063/2020 e Lei 9.784/1999. Registro do que a lei diz, não parecer. Os três ficam em parte, porque dependem de norma de cada ente ou do MEC.

| Item | Resultado |
|---|---|
| PLN-02 | Modalidades por estimativa e global (art. 60), nota de empenho com campos fixos (art. 61), liquidação antes do pagamento (arts. 62 a 64), restos a pagar processados e não processados (art. 36), limite do duodécimo no último mês do mandato do prefeito (art. 59). Corrigido no [37](37-planejamento-e-empenho.md): restos a pagar incluem o empenho liquidado e não pago |
| DOC-01 | Três níveis de assinatura (art. 4º). A lei vale para interação com ente público, não entre particulares (art. 2º). Qualificada obrigatória nos casos do art. 5º, § 2º, e no atestado médico eletrônico (art. 13). Diploma e histórico não estão na lei |
| GD-06 | Lei federal: forma do ato, prazos de 5, 10 e 30 dias, intimação com 3 dias úteis, motivação obrigatória (arts. 22, 24, 26, 49, 50, 56 a 59 e 66). Estado e município seguem lei própria |

### 9.7 Conferência de curso, superior, Pé-de-Meia e assinatura entre particulares, em 03/11/2026

Textos lidos no Planalto: LDB (arts. 36 a 47, texto literal), Decreto 11.901/2024 e MP 2.200-2/2001. A CLT, arts. 317 a 324 (professor), foi lida depois no navegador, no texto compilado do Planalto.

| Item | Resultado |
|---|---|
| EST-01 | Fechado. No superior, a LDB só torna a frequência obrigatória, salvo EAD (art. 47, § 3º). O percentual é do regimento da instituição, configurado por curso |
| EST-03 | Fechado. Técnico integrado, concomitante e subsequente (arts. 36-B e 36-C), formação inicial e continuada, graduação tecnológica (art. 39), sequencial, graduação, pós e extensão (art. 44). Catálogos CNCT e CNCST como tabela de referência |
| Novo no [59](59-estrutura-academica-por-portal.md) | Página "Grade e Corpo Docente" do superior, publicada até um mês antes das aulas (art. 47, § 1º) |
| INT-03 | Regulamento conferido: 14 a 24 anos, matrícula em até dois meses, frequência por média ou mensal, valores anuais, termo de compromisso e responsabilidade da rede pela veracidade (Decreto 11.901/2024, arts. 3º a 7º). Fica o ato do MEC para canal e calendário |
| DOC-01 | Entre particulares, certificado ICP-Brasil presume veracidade e outro meio vale se aceito pelas partes (MP 2.200-2/2001, art. 10). Fica a norma do MEC para diploma e histórico |
| HCM-05 | Lei 15.371/2026 lida: trata de licença-paternidade e não altera os arts. 66, 71 e 74 da CLT. Professor: aula por mais de um turno sem passar da jornada semanal, sem aula no domingo, remuneração por aulas semanais em mês de 4,5 semanas, falta de casamento ou luto não descontada por 9 dias, exames com no máximo 8 horas por dia e férias escolares pagas (CLT, arts. 318 a 322). Registrado no [39](39-departamento-pessoal-rh-medicina-por-portal.md), seção 3.4 |

---

## 10. Critérios de aceite desta lista

- [ ] Cada item tem um documento de origem e um responsável.
- [ ] Cada item respondido sai desta lista e é marcado como **Decidido** ou **Escrito** no documento de origem.
- [ ] O parecer do jurídico (Q-01 e demais) fica registrado com data e nome do responsável.
- [ ] A próxima auditoria repete o método da seção 0 e compara as contagens.
