# Relatórios acadêmicos e censo

- Portal: Gestão (`gestao.`)
- Área: Acadêmico
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [69](../../../docs/v2/69-relatorios-e-censo-por-portal.md) (integral); [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 4; [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 5
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Emitir os relatórios acadêmicos pelo modelo comum (tipos, ciclo, formatos) e o censo escolar e formatos oficiais, inclusive CPA/SINAES (ACA-02).

## 3. Telas

- **Catálogo de relatórios** (lista por módulo, seção 13, 3): filtros, agendamento, formato.
- **Execuções** (DataTable): estado, autor, arquivo, validade do link.
- **Censo escolar** (assistente): fonte, validação, pendências, exportação no formato oficial.
- **CPA/SINAES** (página de ciclo de autoavaliação institucional).

## 4. Permissões por portal (extraídas do SDD)

Do [69](../../../docs/v2/69-relatorios-e-censo-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver gerenciais de toda a entidade. Conferir o censo e aprovar o envio | Gerar operacional de aluno. Ver arquivo de regulatório antes do envio | E |
| **Coordenação** | Ver relatórios gerenciais e operacionais da unidade, no escopo de pedagógico | Enviar censo. Ver relatório financeiro | E |
| **Secretaria** | Gerar operacionais e regulatórios da unidade. Gerar e enviar censo, com conferência da gestão | Gerar financeiro. Enviar sem conferência | E |

## 5. Papéis

- `unit.manager` e `unit.coordinator`: relatórios da unidade.
- `unit.secretary`: relatórios da secretaria e censo.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Relatório respeita o escopo de quem pede; dado pessoal só com permissão ([69](../../../docs/v2/69-relatorios-e-censo-por-portal.md), seção 2.4).
- Relatórios da secretaria, do diário, do financeiro e da biblioteca: [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seções 4 a 7.

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

### 13.1 [69 — Relatórios, Exportações Regulatórias e Censo, por Portal](../../../docs/v2/69-relatorios-e-censo-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Décima segunda lacuna da ordem de [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), seção 3. Regra geral de relatórios e lacunas do menu iScholar em [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seções 3 a 7. Cada relatório depende do módulo que tem o dado, e por isso este documento só fecha o modelo comum e o catálogo. Documento oficial com código de validação em [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), seção 6. Minimização em [07](../../../docs/v2/07-privacidade-lgpd.md). Integração de envio em [16](../../../docs/v2/16-integracoes-externas.md). Auditoria em [29](../../../docs/v2/29-auditoria.md). Relatórios de estágio e TCC em [65](../../../docs/v2/65-estagio-e-tcc-por-portal.md), e de conselho em [62](../../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 12 do acadêmico. A v1 tem relatórios de desempenho, frequência e regulatórios na API ([`spec_gestao_academica_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_academica_completo.md), seção 15 e API). Pontos que dependem de norma ou de decisão do autor estão marcados.

---

#### 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Modelo comum de relatório? | **Parcial.** A regra geral está em [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 3. Faltam ciclo de geração, arquivo e formatos |
| Catálogo por módulo? | **Parcial.** Seção 3 deste documento. Cada item depende do módulo de origem |
| Censo escolar? | **Não.** Não há especificação na v1 nem na v2 |
| Formatos oficiais (ficha SEE, recadastramento, SINAES)? | **Não.** Dependem de decisão CFG-05 e de ACA-02 |

---

#### 2. Modelo comum

##### 2.1 Tipos

| Tipo | Uso | Exemplo |
|---|---|---|
| Operacional | Lista do dia ou do período | Lista de presença, aniversariantes, empréstimos em atraso |
| Gerencial | Totais e indicadores | Desempenho por disciplina, frequência por turma, inadimplência |
| Regulatório | Formato exigido por órgão | Censo escolar, ficha SEE, relatório SINAES |

##### 2.2 Ciclo

1. **Pedido.** O usuário escolhe o relatório e o filtro, dentro do próprio escopo ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), regra 3).
2. **Geração.** Abaixo do limite de linhas, a geração é imediata. Acima dele, é fila, com aviso quando pronta ([57](../../../docs/v2/57-notificacoes-por-portal.md)). Limite: REL-04.
3. **Arquivo.** O resultado é um arquivo com data, filtro, autor, hash e versão do layout.
4. **Download.** Só pelo autor do pedido, ou por quem tem o mesmo escopo, pelo período de validade.
5. **Expiração.** Arquivo expira e sai do armazenamento. O pedido e o filtro ficam no histórico.

##### 2.3 Formatos

| Formato | Uso |
|---|---|
| Tela | Padrão. Sem arquivo |
| PDF | Para imprimir ou arquivar. Com cabeçalho da unidade e data |
| CSV e planilha | Para análise. Sem formatação |
| Layout oficial | Só para regulatório, na forma exigida pelo órgão |

##### 2.4 Regras

- **Escopo da tela.** Relatório não mostra dado que a tela de origem não mostra ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), regra 3).
- **Minimização.** Só os campos necessários. Aniversariantes usa mês e dia ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), regra 4).
- **Grupo pequeno.** Indicador de grupo com menos de 2 pessoas não é mostrado, como em [41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 3.
- **Sem segredo.** Senha, token e link de uso único não aparecem em relatório. Ver [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), regra 7 e CFG-03.
- **Foto.** Relatório com foto só com consentimento específico ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), CFG-02).
- **Auditoria.** Geração e download geram evento com o portal, o filtro e o número de linhas ([29](../../../docs/v2/29-auditoria.md)).
- **Relatório programado.** O envio automático vai só para usuários com vínculo ativo na entidade. Não há envio a e-mail externo. **Decidido** em 03/11/2026 (REL-06).

---

#### 3. Catálogo por módulo

| Módulo | Relatórios principais | Tipo | Documento de origem |
|---|---|---|---|
| Matrícula | Matrículas, matrículas ativas, comparação entre períodos, duplicidade de matrícula, vagas por turma | Gerencial e operacional | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) |
| Estrutura | Grade curricular, sistema avaliativo, PPC vigente | Operacional | [59](../../../docs/v2/59-estrutura-academica-por-portal.md) |
| Turmas | Total de alunos por turma e unidade, capa de pasta, ocupação | Operacional e gerencial | [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md) |
| Grade | Horário da turma, do professor e da semana | Operacional | [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), seção 4.4 |
| Diário | Lista de presença, faltas consecutivas, justificadas, notas, planejado versus ministrado | Operacional e gerencial | [61](../../../docs/v2/61-diario-escolar-por-portal.md) |
| Boletim | Abaixo da média, reprovados, ata de resultados finais | Gerencial e regulatório | [62](../../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md) |
| Planos | Conteúdo não lançado, planejado versus ministrado | Gerencial | [64](../../../docs/v2/64-planos-de-aula-e-de-ensino-por-portal.md) |
| Estágio e TCC | Estágios, horas, TCCs por status, defesas | Gerencial | [65](../../../docs/v2/65-estagio-e-tcc-por-portal.md) |
| Ocorrências | Quantidade por tipo e gravidade, sem nome | Gerencial | [63](../../../docs/v2/63-ocorrencias-disciplinares-por-portal.md) |
| Prontuário | Documentos vencidos, prontuários incompletos | Operacional | [66](../../../docs/v2/66-prontuario-e-portfolio-do-aluno-por-portal.md) |
| Livros | Livros publicados, arquivo digitalizado e verificado | Gerencial | [67](../../../docs/v2/67-livros-digitais-e-arquivo-morto-por-portal.md) |
| Biblioteca | Circulação, empréstimos em atraso, busca de bibliografia | Operacional e gerencial | [68](../../../docs/v2/68-biblioteca-por-portal.md) |
| Financeiro | Recebimento, inadimplência, contas, caixa, DRE, fluxo de caixa | Gerencial e regulatório | [18](../../../docs/v2/18-regras-modulos-2.md), [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md) |
| Calendário e eventos | Calendário letivo, inscritos, certificados emitidos | Operacional | [58](../../../docs/v2/58-calendario-e-eventos-por-portal.md) |
| Notificações | Entregas, falhas, leitura (sem corpo de mensagem) | Gerencial | [57](../../../docs/v2/57-notificacoes-por-portal.md), NOT-08 |
| Salas | Ocupação e reservas | Gerencial | [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md) |
| Avaliação institucional (CPA) | Resultados por dimensão do SINAES | Regulatório | [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), ACA-02 (decidido: entra nesta versão) |

---

#### 4. Censo escolar

##### 4.1 O que é

Levantamento anual de dados da escola, com alunos, turmas, professores, unidade e infraestrutura, enviado ao órgão do sistema de ensino. O layout e o prazo mudam por ano e por esfera **(verificar)**.

##### 4.2 Fonte

| Dado | Vem de |
|---|---|
| Alunos e matrículas | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) |
| Turmas, turno e grade | [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md) |
| Professores e vínculo | [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md) e [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md) |
| Infraestrutura (salas) | [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md) e [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), seção 2.2 |
| Estrutura do curso | [59](../../../docs/v2/59-estrutura-academica-por-portal.md) |

##### 4.3 Regras

- **Geração é da secretaria.** Gestão confere antes do envio. **Decidido** em 03/11/2026 (REL-03).
- **Conferência antes do envio.** O sistema lista inconsistências (aluno sem turma, turma sem professor, sala sem capacidade). Não corrige sozinho. A secretaria corrige no módulo de origem.
- **Versão enviada é registrada.** Ao enviar, o sistema grava o arquivo, o hash, a data e o layout usado. Reenvio gera nova versão.
- **Envio é ação da secretaria.** O sistema gera o arquivo no layout oficial do Educacenso. A secretaria confere, baixa e importa no sistema do INEP. A plataforma não acessa o sistema do INEP por conta própria. Ver [74](../../../docs/v2/74-integracoes-educacionais-oficiais.md), seção 3.1.
- **Layout por ano.** Cada layout é uma versão. Relatório antigo não é regerado com layout novo sem aviso.

---

#### 5. Formatos oficiais

| Formato | Quem exige | Situação |
|---|---|---|
| Censo escolar | Órgão federal, por esfera | Seção 4. Layout e prazo **(verificar)** |
| Ficha de matrícula SEE | Secretaria estadual | Formato **a confirmar** (CFG-05) |
| Ficha de recadastramento | Escola ou secretaria | Formato **a confirmar** (CFG-05) |
| Relatório SINAES e CPA | Ensino superior | Entra nesta versão (ACA-02, decidido em 03/11/2026) |
| Histórico escolar e livro de registro | Sistema de ensino | Já em [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md) e [67](../../../docs/v2/67-livros-digitais-e-arquivo-morto-por-portal.md) |

---

#### 6. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos de relatório e de layout, sem dado | Ver relatório ou arquivo de entidade | P |
| **Gestão** | Ver gerenciais de toda a entidade. Conferir o censo e aprovar o envio | Gerar operacional de aluno. Ver arquivo de regulatório antes do envio | E |
| **Coordenação** | Ver relatórios gerenciais e operacionais da unidade, no escopo de pedagógico | Enviar censo. Ver relatório financeiro | E |
| **Secretaria** | Gerar operacionais e regulatórios da unidade. Gerar e enviar censo, com conferência da gestão | Gerar financeiro. Enviar sem conferência | E |
| **Financeiro** (perfil da unidade) | Gerar relatórios financeiros, incluindo caixa e DRE | Ver dado pedagógico além do necessário | E |
| **Professor** | Ver lista de presença e de notas das próprias turmas | Relatório de outra turma ou unidade | E |
| **Aluno** | Ver o próprio histórico e boletim, quando a regra permitir | Relatório de turma ou de colega | E |
| **Responsáveis** | Ver o boletim e a frequência do dependente | Relatório de turma | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer relatório | E |

---

#### 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| REL-01 | Layout e prazo do censo, por esfera e por ano (seção 4.1) | (verificar) |
| REL-02 | Prazo de guarda do arquivo gerado de relatório regulatório | (jurídico) |
| REL-03 | Quem envia o censo (seção 4.3) | **Decidido** em 03/11/2026: a secretaria envia, com conferência da gestão |
| REL-04 | Limite de linhas para geração imediata (seção 2.2) | Técnico. Proposta a validar em homologação |
| REL-05 | Formatos oficiais de cada unidade (seção 5) | **Decidido** em 03/11/2026 (CFG-05): censo, ficha SEE e SINAES. Ficha de recadastramento fica para configuração da unidade |
| REL-06 | Relatório programado: destinos (seção 2.4) | **Decidido** em 03/11/2026: só usuários com vínculo na entidade |
| REL-07 | DDL: modelo de relatório, pedido, execução, arquivo gerado, agendamento e envio regulatório | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.14. Revisão do owner pendente (DDL-01) |

---

#### 8. Critérios de aceite

- [ ] Relatório não mostra dado que a tela de origem não mostra (teste de isolamento).
- [ ] Senha, token e link de uso único não aparecem em nenhum relatório (varredura).
- [ ] Exportação gera evento de auditoria com portal, filtro e número de linhas (teste).
- [ ] Censo não é enviado sem ação da secretaria (teste).
- [ ] Inconsistência do censo aparece como lista, sem correção automática (teste).
- [ ] Arquivo regulatório guarda layout, versão, hash e data do envio (teste).
- [ ] Arquivo expirado sai do armazenamento (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).

### 13.2 [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 4

#### 4. Relatórios da Secretaria

| Item | Situação | Dependência |
|---|---|---|
| Alunos com mais de uma matrícula | Lacuna | Regra de vínculo ativo, [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) |
| Alunos por transporte escolar | Parcial | [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md). Dado de localização, não entra no relatório |
| Aniversariantes | Lacuna | Minimização, regra 4 da seção 3 |
| Assinatura eletrônica | Parcial | [33](../../../docs/v2/33-contratos-por-portal.md), [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md) |
| Calendário por turma | Lacuna | Calendário escolar ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 1) |
| Capa de pasta por turma | Lacuna | Turma ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 3) |
| Carômetro | Lacuna | Foto, regra 8 da seção 3 |
| Compara matrículas entre períodos letivos | Lacuna | Período letivo |
| Declaração de transferência | Parcial | [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md) (tipo a incluir) |
| Declarações | Coberto | [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), [53](../../../docs/v2/53-pacote-documentos-e-contratos.md) |
| Documentos pendentes (Bilhete) | Parcial | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), M-08; [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md) |
| Ficha de matrícula SEE | Lacuna | Formato da Secretaria de Educação **a confirmar** |
| Ficha de recadastramento | Lacuna | Não especificado |
| Grade curricular | Lacuna | [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 1 |
| Histórico escolar e alunos | Parcial | [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), DOC-03 |
| Horário do professor por período | Lacuna | Grade de horários ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 3) |
| Horários da semana | Lacuna | Grade de horários |
| Horários da turma e dos professores | Lacuna | Grade de horários |
| Irmãos | Lacuna | Vínculo de família, [07](../../../docs/v2/07-privacidade-lgpd.md) |
| Lista de presença por disciplina e por turma | Lacuna | Diário ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 4) |
| Lista de professores | Parcial | [37](../../../docs/v2/37-planejamento-e-empenho.md), carga docente |
| Lista geral de alunos | Parcial | [17](../../../docs/v2/17-regras-modulos.md), seção 4.2 |
| Matrículas | Coberto | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) |
| Matrículas ativas | Coberto | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 2 |
| Matrículas e rematrículas | Coberto | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) |
| Ocorrências | Lacuna | [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 6 |
| Ocupação de sala | Coberto | [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md) |
| Reunião de pais | Parcial | [40](../../../docs/v2/40-aulas-online-por-portal.md), seção 4.1 (reunião 1:1). Reunião coletiva não especificada |
| Responsável por dois ou mais alunos | Lacuna | Vínculo de família |
| Senhas de acesso ao Painel | Parcial | Decidido: relatório de dados de acesso do responsável, só para o próprio responsável. Senha em texto não deve aparecer (regra 7 da seção 3) |
| Senhas do Painel do Professor | Parcial | Mesma regra do painel do responsável, para o professor, sem envio a aluno ou terceiro |
| Sistema avaliativo, detalhamento por disciplina | Lacuna | [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 2 |
| Telefones por tipo | Lacuna | Contato do titular, minimização |
| Total de alunos por turma e por unidade | Lacuna | Turma |
| Atividades complementares e de extensão | Coberto | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 5 |
| Ficha de matrícula e outros formatos oficiais | Lacuna | Formato oficial **a confirmar** |

Observação: a contagem por linha dá mais itens do que a tabela da seção 1, porque alguns itens do menu se repetem em grupos diferentes. A seção 1 usa a contagem do menu colado.

### 13.3 [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 5

#### 5. Relatórios do Diário escolar

| Grupo | Itens | Situação | Dependência |
|---|---|---|---|
| Diário eletrônico, capa e composição da turma | 3 | Lacuna | Diário, turma ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), itens 3 e 4) |
| Conteúdos curriculares não lançados e registro de conteúdos | 2 | Lacuna | Plano de aula ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 7) |
| Apuração de frequência, faltas consecutivas, fora do período, justificadas, por divisão, sintético | 7 | Lacuna | Frequência e justificativa ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 4) |
| Notas: abaixo da média, reprovados, ata de resultados finais, boletim | 4 | Lacuna | Boletim e aprovação ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 5) |
| Notas: recuperação, consulta por turma e professor, controle de lançamento, detalhamento, ficha individual, notas médias, notas por divisão, notas finais por curso | 11 | Lacuna | Sistema avaliativo ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 2) |
| Gráficos de desempenho, ranking, gráfico entre turmas | 3 | Parcial | Ranking tem regra em [47](../../../docs/v2/47-simulados-por-portal.md), seção 8, só para simulado |
| Planejamento de aulas: total planejado e ministrado, total de dias | 3 | Lacuna | Planos de aula ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 7) |
