# 69 — Relatórios, Exportações Regulatórias e Censo, por Portal

> Parte do [SDD v2](00-README.md). Décima segunda lacuna da ordem de [55](55-academico-verificacao-e-lacunas.md), seção 3. Regra geral de relatórios e lacunas do menu iScholar em [56](56-configuracoes-e-relatorios-lacunas.md), seções 3 a 7. Cada relatório depende do módulo que tem o dado, e por isso este documento só fecha o modelo comum e o catálogo. Documento oficial com código de validação em [48](48-gerador-de-documentos-por-portal.md), seção 6. Minimização em [07](07-privacidade-lgpd.md). Integração de envio em [16](16-integracoes-externas.md). Auditoria em [29](29-auditoria.md). Relatórios de estágio e TCC em [65](65-estagio-e-tcc-por-portal.md), e de conselho em [62](62-boletim-e-conselho-de-classe-por-portal.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 12 do acadêmico. A v1 tem relatórios de desempenho, frequência e regulatórios na API (`spec_gestao_academica_completo.md`, seção 15 e API). Pontos que dependem de norma ou de decisão do autor estão marcados.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Modelo comum de relatório? | **Parcial.** A regra geral está em [56](56-configuracoes-e-relatorios-lacunas.md), seção 3. Faltam ciclo de geração, arquivo e formatos |
| Catálogo por módulo? | **Parcial.** Seção 3 deste documento. Cada item depende do módulo de origem |
| Censo escolar? | **Não.** Não há especificação na v1 nem na v2 |
| Formatos oficiais (ficha SEE, recadastramento, SINAES)? | **Não.** Dependem de decisão CFG-05 e de ACA-02 |

---

## 2. Modelo comum

### 2.1 Tipos

| Tipo | Uso | Exemplo |
|---|---|---|
| Operacional | Lista do dia ou do período | Lista de presença, aniversariantes, empréstimos em atraso |
| Gerencial | Totais e indicadores | Desempenho por disciplina, frequência por turma, inadimplência |
| Regulatório | Formato exigido por órgão | Censo escolar, ficha SEE, relatório SINAES |

### 2.2 Ciclo

1. **Pedido.** O usuário escolhe o relatório e o filtro, dentro do próprio escopo ([56](56-configuracoes-e-relatorios-lacunas.md), regra 3).
2. **Geração.** Abaixo do limite de linhas, a geração é imediata. Acima dele, é fila, com aviso quando pronta ([57](57-notificacoes-por-portal.md)). Limite: REL-04.
3. **Arquivo.** O resultado é um arquivo com data, filtro, autor, hash e versão do layout.
4. **Download.** Só pelo autor do pedido, ou por quem tem o mesmo escopo, pelo período de validade.
5. **Expiração.** Arquivo expira e sai do armazenamento. O pedido e o filtro ficam no histórico.

### 2.3 Formatos

| Formato | Uso |
|---|---|
| Tela | Padrão. Sem arquivo |
| PDF | Para imprimir ou arquivar. Com cabeçalho da unidade e data |
| CSV e planilha | Para análise. Sem formatação |
| Layout oficial | Só para regulatório, na forma exigida pelo órgão |

### 2.4 Regras

- **Escopo da tela.** Relatório não mostra dado que a tela de origem não mostra ([56](56-configuracoes-e-relatorios-lacunas.md), regra 3).
- **Minimização.** Só os campos necessários. Aniversariantes usa mês e dia ([56](56-configuracoes-e-relatorios-lacunas.md), regra 4).
- **Grupo pequeno.** Indicador de grupo com menos de 2 pessoas não é mostrado, como em [41](41-formularios-e-pesquisas.md), seção 3.
- **Sem segredo.** Senha, token e link de uso único não aparecem em relatório. Ver [56](56-configuracoes-e-relatorios-lacunas.md), regra 7 e CFG-03.
- **Foto.** Relatório com foto só com consentimento específico ([56](56-configuracoes-e-relatorios-lacunas.md), CFG-02).
- **Auditoria.** Geração e download geram evento com o portal, o filtro e o número de linhas ([29](29-auditoria.md)).
- **Relatório programado.** O envio automático vai só para usuários com vínculo ativo na entidade. Não há envio a e-mail externo. **Decidido** em 03/11/2026 (REL-06).

---

## 3. Catálogo por módulo

| Módulo | Relatórios principais | Tipo | Documento de origem |
|---|---|---|---|
| Matrícula | Matrículas, matrículas ativas, comparação entre períodos, duplicidade de matrícula, vagas por turma | Gerencial e operacional | [46](46-matricula-e-rematricula-por-portal.md) |
| Estrutura | Grade curricular, sistema avaliativo, PPC vigente | Operacional | [59](59-estrutura-academica-por-portal.md) |
| Turmas | Total de alunos por turma e unidade, capa de pasta, ocupação | Operacional e gerencial | [60](60-turmas-e-grade-de-horarios-por-portal.md) |
| Grade | Horário da turma, do professor e da semana | Operacional | [60](60-turmas-e-grade-de-horarios-por-portal.md), seção 4.4 |
| Diário | Lista de presença, faltas consecutivas, justificadas, notas, planejado versus ministrado | Operacional e gerencial | [61](61-diario-escolar-por-portal.md) |
| Boletim | Abaixo da média, reprovados, ata de resultados finais | Gerencial e regulatório | [62](62-boletim-e-conselho-de-classe-por-portal.md) |
| Planos | Conteúdo não lançado, planejado versus ministrado | Gerencial | [64](64-planos-de-aula-e-de-ensino-por-portal.md) |
| Estágio e TCC | Estágios, horas, TCCs por status, defesas | Gerencial | [65](65-estagio-e-tcc-por-portal.md) |
| Ocorrências | Quantidade por tipo e gravidade, sem nome | Gerencial | [63](63-ocorrencias-disciplinares-por-portal.md) |
| Prontuário | Documentos vencidos, prontuários incompletos | Operacional | [66](66-prontuario-e-portfolio-do-aluno-por-portal.md) |
| Livros | Livros publicados, arquivo digitalizado e verificado | Gerencial | [67](67-livros-digitais-e-arquivo-morto-por-portal.md) |
| Biblioteca | Circulação, empréstimos em atraso, busca de bibliografia | Operacional e gerencial | [68](68-biblioteca-por-portal.md) |
| Financeiro | Recebimento, inadimplência, contas, caixa, DRE, fluxo de caixa | Gerencial e regulatório | [18](18-regras-modulos-2.md), [34](34-pagamentos-fiscal-bancos-por-portal.md) |
| Calendário e eventos | Calendário letivo, inscritos, certificados emitidos | Operacional | [58](58-calendario-e-eventos-por-portal.md) |
| Notificações | Entregas, falhas, leitura (sem corpo de mensagem) | Gerencial | [57](57-notificacoes-por-portal.md), NOT-08 |
| Salas | Ocupação e reservas | Gerencial | [44](44-agendamento-ambientes-equipamentos.md) |
| Avaliação institucional (CPA) | Resultados por dimensão do SINAES | Regulatório | [55](55-academico-verificacao-e-lacunas.md), ACA-02 (decidido: entra nesta versão) |

---

## 4. Censo escolar

### 4.1 O que é

Levantamento anual de dados da escola, com alunos, turmas, professores, unidade e infraestrutura, enviado ao órgão do sistema de ensino. O layout e o prazo mudam por ano e por esfera **(verificar)**.

### 4.2 Fonte

| Dado | Vem de |
|---|---|
| Alunos e matrículas | [46](46-matricula-e-rematricula-por-portal.md) |
| Turmas, turno e grade | [60](60-turmas-e-grade-de-horarios-por-portal.md) |
| Professores e vínculo | [39](39-departamento-pessoal-rh-medicina-por-portal.md) e [60](60-turmas-e-grade-de-horarios-por-portal.md) |
| Infraestrutura (salas) | [44](44-agendamento-ambientes-equipamentos.md) e [60](60-turmas-e-grade-de-horarios-por-portal.md), seção 2.2 |
| Estrutura do curso | [59](59-estrutura-academica-por-portal.md) |

### 4.3 Regras

- **Geração é da secretaria.** Gestão confere antes do envio. **Decidido** em 03/11/2026 (REL-03).
- **Conferência antes do envio.** O sistema lista inconsistências (aluno sem turma, turma sem professor, sala sem capacidade). Não corrige sozinho. A secretaria corrige no módulo de origem.
- **Versão enviada é registrada.** Ao enviar, o sistema grava o arquivo, o hash, a data e o layout usado. Reenvio gera nova versão.
- **Envio é ação da secretaria.** O sistema gera o arquivo no layout oficial do Educacenso. A secretaria confere, baixa e importa no sistema do INEP. A plataforma não acessa o sistema do INEP por conta própria. Ver [74](74-integracoes-educacionais-oficiais.md), seção 3.1.
- **Layout por ano.** Cada layout é uma versão. Relatório antigo não é regerado com layout novo sem aviso.

---

## 5. Formatos oficiais

| Formato | Quem exige | Situação |
|---|---|---|
| Censo escolar | Órgão federal, por esfera | Seção 4. Layout e prazo **(verificar)** |
| Ficha de matrícula SEE | Secretaria estadual | Formato **a confirmar** (CFG-05) |
| Ficha de recadastramento | Escola ou secretaria | Formato **a confirmar** (CFG-05) |
| Relatório SINAES e CPA | Ensino superior | Entra nesta versão (ACA-02, decidido em 03/11/2026) |
| Histórico escolar e livro de registro | Sistema de ensino | Já em [48](48-gerador-de-documentos-por-portal.md) e [67](67-livros-digitais-e-arquivo-morto-por-portal.md) |

---

## 6. Por portal

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

## 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| REL-01 | Layout e prazo do censo, por esfera e por ano (seção 4.1) | (verificar) |
| REL-02 | Prazo de guarda do arquivo gerado de relatório regulatório | (jurídico) |
| REL-03 | Quem envia o censo (seção 4.3) | **Decidido** em 03/11/2026: a secretaria envia, com conferência da gestão |
| REL-04 | Limite de linhas para geração imediata (seção 2.2) | Técnico. Proposta a validar em homologação |
| REL-05 | Formatos oficiais de cada unidade (seção 5) | **Decidido** em 03/11/2026 (CFG-05): censo, ficha SEE e SINAES. Ficha de recadastramento fica para configuração da unidade |
| REL-06 | Relatório programado: destinos (seção 2.4) | **Decidido** em 03/11/2026: só usuários com vínculo na entidade |
| REL-07 | DDL: modelo de relatório, pedido, execução, arquivo gerado, agendamento e envio regulatório | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.14. Revisão do owner pendente (DDL-01) |

---

## 8. Critérios de aceite

- [ ] Relatório não mostra dado que a tela de origem não mostra (teste de isolamento).
- [ ] Senha, token e link de uso único não aparecem em nenhum relatório (varredura).
- [ ] Exportação gera evento de auditoria com portal, filtro e número de linhas (teste).
- [ ] Censo não é enviado sem ação da secretaria (teste).
- [ ] Inconsistência do censo aparece como lista, sem correção automática (teste).
- [ ] Arquivo regulatório guarda layout, versão, hash e data do envio (teste).
- [ ] Arquivo expirado sai do armazenamento (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
