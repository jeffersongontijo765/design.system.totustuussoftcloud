# Pedagógico (coordenação e diário)

- Portal: Gestão (`gestao.`)
- Área: Acadêmico
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [61](../../../docs/v2/61-diario-escolar-por-portal.md) (integral)
- Fonte da v1: absorvida integralmente em [administracao-escolar-estrutura-academica.md](administracao-escolar-estrutura-academica.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Acompanhar e supervisionar o diário escolar de todas as turmas da unidade: aulas, chamada, faltas e justificativas, notas, médias e fechamento do diário. O lançamento é do professor (portal do professor); a coordenação acompanha, cobra pendências, aprova justificativas e reabre o diário com motivo.

## 3. Telas

- **Painel pedagógico** (dashboard): diários pendentes por turma e professor, aulas sem conteúdo, chamadas pendentes, notas fora do prazo, alunos com frequência abaixo do mínimo.
- **Diários da unidade** (DataTable): turma, disciplina, professor, período, estado (`aberto`, `fechado`, `reaberto`), % de chamada e de conteúdo; drawer com o diário em leitura.
- **Justificativas de falta** (fila com aprovação): documento anexado, período, decisão com motivo.
- **Reabrir diário** (modal): motivo obrigatório, prazo de reabertura, aviso ao professor; gera evento de auditoria.
- **Alunos em risco** (lista): frequência e média abaixo do limite, com encaminhamento à coordenação ou ao responsável.

## 4. Permissões por portal (extraídas do SDD)

Do [61](../../../docs/v2/61-diario-escolar-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver relatórios do diário e indicadores de frequência | Lançar nota ou chamada. Autorizar reabertura, que é da coordenação | E |
| **Coordenação** | Aprovar justificativa. Autorizar lançamento fora do prazo e reabertura. Ver diário de todas as turmas da unidade | Lançar nota pelo professor | E |
| **Secretaria** | Consultar diário. Emitir relatórios. Cadastrar tipos de justificativa | Lançar nota ou aprovar justificativa | E |

## 5. Papéis

- `unit.coordinator`: acompanhar, aprovar justificativa, reabrir diário com motivo.
- `unit.manager`: leitura e relatórios.
- `teacher` (portal do professor): lança chamada, conteúdo e nota **só das turmas vinculadas**; nota só pelo professor da turma ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5).
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Estados do diário: `aberto`, `fechado`, `reaberto` (com justificativa) ([17](../../../docs/v2/17-regras-modulos.md), seção 4.3).
- Presença por QR Code válida por 5 minutos por padrão; geolocalização só com consentimento ([17](../../../docs/v2/17-regras-modulos.md), seção 4.2).
- A coordenação **não altera** nota nem chamada do professor; corrige por reabertura do diário, e o professor relança.

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

### 13.1 [61 — Diário Escolar, por Portal: Chamada, Faltas, Justificativas, Notas e Conteúdo](../../../docs/v2/61-diario-escolar-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Quarta lacuna da ordem de [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), seção 3. Turma, aula e grade em [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md). Sistema avaliativo e frequência mínima em [59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 4. Chamada por QR Code e sala online em [17](../../../docs/v2/17-regras-modulos.md), seção 4, e [40](../../../docs/v2/40-aulas-online-por-portal.md). Períodos em [59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 3.6. Aviso ao responsável em [57](../../../docs/v2/57-notificacoes-por-portal.md). Relatórios do diário em [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 5. Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna do diário. Pontos que dependem de norma ou de decisão do autor estão marcados.

---

#### 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Chamada tem regra? | **Parcial.** QR Code e manual em [17](../../../docs/v2/17-regras-modulos.md). Falta regra de registro por aula |
| Faltas e justificativas? | **Não.** Só o nome "faltas" e "justificadas" no menu de referência |
| Lançamento de nota? | **Parcial.** Regra de faixa e de período aberto em [17](../../../docs/v2/17-regras-modulos.md) |
| Conteúdo da aula? | **Não.** Só citado como plano de aula em [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md) |
| Fechamento e reabertura? | **Parcial.** Estados `aberto`, `fechado`, `reaberto` em [17](../../../docs/v2/17-regras-modulos.md) |

---

#### 2. Aula

Cada aula da grade ([60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), seção 4) gera uma **aula realizada** no diário. A aula tem:

- Turma, disciplina, professor, data e bloco.
- Conteúdo ministrado, com texto livre e referência ao plano de aula.
- Estado: `planejada`, `realizada`, `cancelada`, `reposicao`.

**Regras:**

- Só o professor da disciplina na turma registra a aula.
- Aula cancelada não conta na frequência. Exige motivo.
- Aula de reposição é aula nova, com data própria. Não substitui a original.
- Conteúdo não lançado até o fim do período aparece no relatório de pendências ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 5).

---

#### 3. Chamada

##### 3.1 Formas de registro

| Forma | Quando | Regra |
|---|---|---|
| Manual | Padrão | Presente, falta, ou justificada, por aluno |
| QR Code | Presencial | Código válido pelo tempo configurado (5 minutos por padrão, decidido em 03/11/2026). Presença sem QR vira pendência |
| Sala online | Aula online | Presença pelo tempo conectado e confirmação, conforme [40](../../../docs/v2/40-aulas-online-por-portal.md), seção 6 |

**Regra geral:** a chamada é lançada na aula, com correção até o fim do dia útil seguinte. **Decidido** em 03/11/2026 (DIA-05). Lançamento fora do prazo exige justificativa da coordenação.

##### 3.2 Presença pendente

Aluno sem registro, em aula que usou QR ou sala online, fica como **pendência de chamada**. Não vira falta sem revisão do professor.

---

#### 4. Faltas e justificativas

##### 4.1 Falta

- Falta é registrada por aluno, por aula. Não por dia.
- Falta é contada por disciplina, e por período no total de frequência.

##### 4.2 Justificativa

| Regra | Detalhe |
|---|---|
| Tipos | Lista padrão da plataforma, ajustável pela escola. Decidido em 03/11/2026 |
| Prazo | 5 dias úteis após a falta, ajustável pela escola. Decidido em 03/11/2026 |
| Documento | Anexo quando o tipo exigir. Armazenado como documento recebido ([54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), contexto A) |
| Quem aprova | Coordenação. Professor não aprova justificativa de própria aula |
| Efeito | A LDB não prevê abono geral de falta: a falta justificada continua contando para o mínimo de 75% (art. 24, VI). A exceção da LDB é a falta por motivo religioso com atividade alternativa, que regulariza a frequência (art. 7º-A, § 2º). Regimes especiais de lei própria, como exercícios domiciliares, entram como exceção configurada **(verificar)** |
| Negativa | Sempre com motivo. Aluno ou responsável recebe o aviso ([57](../../../docs/v2/57-notificacoes-por-portal.md)) |

##### 4.3 Aviso de falta

- Falta acima do limite de alerta da escola gera aviso ao responsável ([57](../../../docs/v2/57-notificacoes-por-portal.md)).
- O aviso informa a disciplina e a quantidade de faltas. Não informa motivo clínico.
- Falta de saúde justificada por atestado não aparece com diagnóstico no aviso ([57](../../../docs/v2/57-notificacoes-por-portal.md), seção 3.5).
- **Conselho Tutelar:** a escola notifica ao Conselho Tutelar do município a relação dos alunos com faltas acima de 30% do percentual permitido em lei (LDB, art. 12, VIII). O sistema gera a lista por período para a secretaria enviar. A forma de cálculo e a periodicidade ficam em DIA-09 **(verificar)**.

---

#### 5. Notas

##### 5.1 Lançamento

- Nota é lançada por avaliação, na escala e com o peso do sistema avaliativo ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 4).
- Só o professor da disciplina na turma lança nota.
- Nota fora da escala é recusada.
- Nota lançada é `lançada`. Correção gera nova versão com motivo, e a anterior fica no histórico.

##### 5.2 Média e recuperação

- Média por disciplina e por período, pelo método do sistema avaliativo.
- Aluno abaixo da média entra em recuperação conforme a regra do sistema. A nota de recuperação aplica-se conforme o sistema.
- Recuperação paralela e conselho de classe seguem [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 5.

##### 5.3 Período

Lançamento de nota e de chamada só com período `aberto` ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 3.6). Reabertura exige justificativa e autorização da coordenação pedagógica (DIA-04).

---

#### 6. Fechamento do diário

- Diário fecha por turma e disciplina, ao fim do período.
- Diário fechado não aceita chamada, nota ou conteúdo.
- Reabertura exige justificativa e autorização da coordenação pedagógica. Fica em auditoria ([29](../../../docs/v2/29-auditoria.md)).
- Fechamento sem todas as notas gera pendência, não bloqueio. **Decidido** em 03/11/2026 (DIA-07).

---

#### 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Nada sobre diário de entidade | Ver diário, nota, falta ou conteúdo | P |
| **Gestão** | Ver relatórios do diário e indicadores de frequência | Lançar nota ou chamada. Autorizar reabertura, que é da coordenação | E |
| **Coordenação** | Aprovar justificativa. Autorizar lançamento fora do prazo e reabertura. Ver diário de todas as turmas da unidade | Lançar nota pelo professor | E |
| **Secretaria** | Consultar diário. Emitir relatórios. Cadastrar tipos de justificativa | Lançar nota ou aprovar justificativa | E |
| **Professor** | Fazer chamada, lançar nota e conteúdo das próprias turmas. Ver o diário das próprias turmas | Lançar em turma em que não leciona. Aprovar justificativa da própria aula | E |
| **Aluno** | Ver as próprias notas, faltas e justificativas. Enviar justificativa com anexo | Ver nota ou falta de colega | E |
| **Responsáveis** | Ver as notas e faltas do dependente. Enviar justificativa | Ver diário de outra turma | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item do diário | E |

---

#### 8. Pendências

| # | Pendência | Tipo |
|---|---|---|
| DIA-01 | Tipos de justificativa de falta | **Decidido** em 03/11/2026: lista padrão da plataforma (atestado médico, motivo familiar, luto, convocação oficial, atividade escolar, outro), que a escola ajusta |
| DIA-02 | Prazo para apresentar justificativa | **Decidido** em 03/11/2026: 5 dias úteis, ajustável pela escola |
| DIA-03 | Falta justificada conta ou não na frequência, por nível de ensino (seção 4.2) | **Conferido** em parte em 03/11/2026: a LDB não prevê abono geral (art. 24, VI). A exceção é o art. 7º-A. Regimes especiais de lei própria **(verificar)** |
| DIA-04 | Quem autoriza reabertura de diário e lançamento fora do prazo | **Decidido** em 03/11/2026: coordenação pedagógica, com justificativa e registro. A secretaria executa |
| DIA-05 | Prazo de correção da chamada após a aula (seção 3.1) | **Decidido** em 03/11/2026: até o fim do dia útil seguinte |
| DIA-06 | Limite de falta que gera aviso ao responsável (seção 4.3) | **Decidido** em 03/11/2026: a cada 5 faltas na disciplina |
| DIA-07 | Fechamento sem todas as notas: pendência ou bloqueio (seção 6) | **Decidido** em 03/11/2026: pendência, sem bloqueio |
| DIA-08 | DDL: aula, chamada, falta, justificativa, lançamento de nota e conteúdo | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.5. Revisão do owner pendente (DDL-01) |
| DIA-09 | Lista de alunos para o Conselho Tutelar (LDB, art. 12, VIII): base do cálculo de "30% do percentual permitido" e periodicidade do envio (seção 4.3) | (verificar) |

---

#### 9. Critérios de aceite

- [ ] Professor de outra turma não lança chamada nem nota (teste de isolamento).
- [ ] Presença pendente de QR não vira falta sem revisão (teste).
- [ ] Nota fora da escala é recusada (teste).
- [ ] Correção de nota gera nova versão com motivo (teste).
- [ ] Diário fechado não aceita lançamento, e reabertura fica em auditoria (teste).
- [ ] Aviso de falta não traz diagnóstico (varredura).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).
