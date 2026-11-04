# Estágio e TCC

- Portal: Gestão (`gestao.`)
- Área: Acadêmico
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [65](../../../docs/v2/65-estagio-e-tcc-por-portal.md) (integral)
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Gerir estágios (obrigatórios quando o curso exigir, ACA-03) com termo, seguro, supervisão e horas, e o TCC com orientação, prazos, banca, versão final e repositório.

## 3. Telas

- **Estágios** (DataTable): aluno, empresa concedente (CNPJ), tipo, supervisor, horas cumpridas, estado.
- **Estágio — cadastro** (página): campos da seção 13 (2.2), apólice de seguro com validade, termo de compromisso com assinatura.
- **Horas e supervisão** (lista de registros com validação).
- **TCC** (DataTable): aluno, orientador, tema, estado, prazo.
- **Banca de defesa** (página): membros (inclusive externos, seção 13, 6), data, ata e nota.
- **Repositório de TCC** (lista pública da entidade, conforme autorização do autor).

## 4. Permissões por portal (extraídas do SDD)

Do [65](../../../docs/v2/65-estagio-e-tcc-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver indicadores: estágios ativos, TCCs por status, prazos vencidos. Aprovar convênio com empresa concedente ([33](../../../docs/v2/33-contratos-por-portal.md)) | Avaliar aluno ou aprovar resultado | E |
| **Coordenação** | Aprovar estágio e TCC. Autorizar prorrogação. Montar banca. Ver todos da unidade | Lançar nota de avaliação de outro professor | E |
| **Secretaria** | Cadastrar estágio e TCC aprovados. Emitir declaração e termo. Guardar a versão final | Aprovar ou avaliar | E |

## 5. Papéis

- `unit.coordinator`: aprovar estágio e TCC, compor banca.
- `unit.secretary`: termos e documentos.
- `teacher`: orientar (portal do professor).
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Estados do estágio: `solicitado`, `ativo`, `concluido`, `cancelado` ([17](../../../docs/v2/17-regras-modulos.md), seção 4.3).
- Empresa concedente com CNPJ válido; apólice com validade durante todo o estágio ([17](../../../docs/v2/17-regras-modulos.md), seção 4.2).
- Pessoa de fora do sistema (banca externa, supervisor) entra por convite com escopo limitado (seção 13, 6).

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

### 13.1 [65 — Estágio e TCC, por Portal](../../../docs/v2/65-estagio-e-tcc-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Oitava lacuna da ordem de [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), seção 3. Depende da estrutura acadêmica ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), tipos de disciplina e carga horária). Decisão ACA-03: estágio obrigatório quando o curso exigir. TCC entra nesta versão (ACA-02, decidido em 03/11/2026). Campos de estágio já citados em [17](../../../docs/v2/17-regras-modulos.md), seção 4.2. Convênio com empresa concedente em [33](../../../docs/v2/33-contratos-por-portal.md). Motor de formulários para avaliação em [41](../../../docs/v2/41-formularios-e-pesquisas.md). Convidado externo com link de uso único em [40](../../../docs/v2/40-aulas-online-por-portal.md). Assinatura de termo e de ata em [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 5. Resultado no boletim em [62](../../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md). Campo de estágio da preceptoria, que é outra coisa, em [42](../../../docs/v2/42-preceptoria-por-portal.md). Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 8 do acadêmico. A v1 tem `internships` e `thesis_works` ([`spec_gestao_academica_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_academica_completo.md), seções 9 e 10). Pontos que dependem de norma ou de decisão do autor estão marcados.

---

#### 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Estágio tem regra? | **Parcial.** Campos e estados em [17](../../../docs/v2/17-regras-modulos.md) (CNPJ, apólice, `solicitado`, `ativo`, `concluido`, `cancelado`). Sem regra de horas, supervisão e avaliação |
| TCC tem regra? | **Não.** Só a entidade `thesis_works` da v1, sem regra de orientação, banca nem versão final |
| Banca de defesa? | **Não.** Só citada na v1, com composição e nota, sem regra |
| Termo e ata? | **Parcial.** Termo e ata são documentos de [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md). Falta regra de quem assina |

---

#### 2. Estágio

##### 2.1 Tipos

| Tipo | Regra |
|---|---|
| Obrigatório | Exigido pelo curso ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 2). Sem ele, o aluno não conclui. Decidido em ACA-03 |
| Não obrigatório | Opcional, acrescido à carga horária regular (Lei 11.788/2008, art. 2º, § 2º). Bolsa ou outra contraprestação e auxílio-transporte são obrigatórios (art. 12). Seguro contra acidentes pessoais é obrigatório em todo estágio (art. 9º, IV). No obrigatório, a instituição pode assumir o seguro (art. 9º, § 1º) |

##### 2.2 Cadastro

| Campo | Regra |
|---|---|
| Aluno e curso | Aluno com matrícula ativa. Curso que exige estágio tem carga horária obrigatória ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), disciplina do tipo estágio) |
| Empresa concedente | CNPJ válido, nome, endereço e contrato de convênio vigente ([33](../../../docs/v2/33-contratos-por-portal.md)). Regra de [17](../../../docs/v2/17-regras-modulos.md) |
| Supervisor da empresa | Pessoa da empresa concedente, com conta no portal de terceiros (seção 6) |
| Professor orientador | Professor habilitado na disciplina de estágio da turma |
| Período | Início, fim previsto e fim real. Dentro do período letivo ([58](../../../docs/v2/58-calendario-e-eventos-por-portal.md)) |
| Carga horária | Definida no projeto do curso (Lei 11.788/2008, art. 2º, § 1º) e combinada por semana. Limite: 4 h por dia e 20 h por semana na educação especial e nos anos finais do fundamental na EJA; 6 h por dia e 30 h por semana no superior, no médio e no técnico de nível médio; até 40 h por semana em período sem aula presencial, se o projeto do curso prever (art. 10). Em período de avaliação, cai pelo menos à metade (art. 10, § 2º). No mesmo concedente, até 2 anos, salvo pessoa com deficiência (art. 11). O sistema recusa termo acima desses limites |
| Termo de compromisso | Assinado por aluno, empresa e instituição. Gerado pelo sistema ([54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md)) |
| Apólice de seguro | Arquivo, com validade. Regra de [17](../../../docs/v2/17-regras-modulos.md) |

##### 2.3 Estados

`solicitado` → `ativo` → `concluido`, com `interrompido` e `cancelado`.

- `solicitado` para `ativo` só com termo assinado pelas três partes e apólice válida.
- `concluido` só com horas cumpridas, relatório final e avaliação do supervisor e do orientador.
- `interrompido` tem motivo registrado. Não conta como horas concluídas. Pode voltar a `ativo` por nova versão do termo.
- `cancelado` antes de `ativo`. Depois de `ativo`, é `interrompido`.

##### 2.4 Supervisão e horas

- O orientador registra visitas de supervisão, com data e observação.
- O aluno envia relatórios periódicos, com atividades desenvolvidas, em prazo não superior a 6 meses (Lei 11.788/2008, art. 7º, IV). Estágio de 1 ano ou mais dá direito a recesso de 30 dias, remunerado quando há bolsa (art. 13).
- Horas são registradas pelo aluno e confirmadas pelo supervisor da empresa.
- Alerta quando as horas do mês ficam 20% abaixo do previsto. Decidido em ETC-07. Alerta ao aluno e ao orientador ([57](../../../docs/v2/57-notificacoes-por-portal.md)).

##### 2.5 Avaliação e resultado

- Avaliação de estágio tem duas partes: supervisor da empresa e orientador. Cada uma é um formulário ([41](../../../docs/v2/41-formularios-e-pesquisas.md)).
- A nota final segue o método do sistema avaliativo ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 4). A v1 usa média das avaliações.
- Resultado `aprovado` ou `reprovado` entra no resultado do período ([62](../../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md)).
- Declaração de conclusão de estágio segue [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md). Não sai sem resultado registrado.

---

#### 3. TCC

##### 3.1 Tipos e escopo

Tipos: TCC, monografia, projeto final e artigo. Aplica-se a cursos que exigem trabalho final ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 2, graduação). Entra nesta versão: **decidido** em 03/11/2026 (ACA-02).

##### 3.2 Cadastro

| Campo | Regra |
|---|---|
| Aluno, curso e tipo | Aluno com matrícula ativa no curso |
| Título | Pode ser provisório. Muda com versão registrada |
| Orientador | Professor habilitado, da lista de professores do curso |
| Coorientador | Opcional. Mesma regra de habilitação |
| Linha de pesquisa | Lista configurável por curso |
| Datas | Início e entrega prevista. Entrega prevista é o prazo |
| Termo de orientação | Assinado pelo aluno e pelo orientador. Gerado pelo sistema |

##### 3.3 Estados

`em_orientacao` → `submetido` → `em_banca` → `aprovado` | `aprovado_com_ressalvas` | `reprovado`, com `reformulacao` a partir de `em_banca`.

- `reformulacao` volta a `submetido` depois da nova versão, com prazo definido pela banca.
- `aprovado_com_ressalvas` exige versão final com as correções. Sem ela, o trabalho não é encerrado.
- `reprovado` encerra o trabalho. Nova tentativa segue a regra do curso **(verificar)**.

##### 3.4 Prazo

- Aviso ao aluno e ao orientador 30 dias antes da entrega prevista, como a regra 17 da v1 ([`spec_gestao_academica_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_academica_completo.md), linha 1183).
- Entrega atrasada não muda o estado sozinha. A coordenação decide sobre a prorrogação, com justificativa.

##### 3.5 Banca de defesa

| Regra | Detalhe |
|---|---|
| Composição | Orientador e dois membros, internos ou externos. Coorientador não entra na nota |
| Membro externo | Cadastro com nome, titulação e instituição. Tem conta no portal de terceiros (seção 6) |
| Agendamento | Data, hora e local. Local é sala reservada ([44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)) ou link de sala online com convidado externo ([40](../../../docs/v2/40-aulas-online-por-portal.md)) |
| Avaliação | Cada membro lança nota e parecer, por formulário. Nota só é vista depois que todos lançaram |
| Nota final | Média ponderada, com pesos configurados pela escola |
| Resultado | Conforme seção 3.3 |
| Ata | Gerada do registro da defesa. Assinada pela banca ([54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md)) |

##### 3.6 Versão final e repositório

- Versão final em PDF e no formato que a escola definir.
- Publicação em repositório institucional depende de autorização do aluno e das regras de direito autoral **(jurídico)**. Sem autorização, o trabalho fica no acervo restrito.
- Trabalho com dado pessoal de pesquisa segue [07](../../../docs/v2/07-privacidade-lgpd.md).

---

#### 4. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelo de termo e de ata, sem dado | Ver estágio, TCC ou banca de entidade | P |
| **Gestão** | Ver indicadores: estágios ativos, TCCs por status, prazos vencidos. Aprovar convênio com empresa concedente ([33](../../../docs/v2/33-contratos-por-portal.md)) | Avaliar aluno ou aprovar resultado | E |
| **Coordenação** | Aprovar estágio e TCC. Autorizar prorrogação. Montar banca. Ver todos da unidade | Lançar nota de avaliação de outro professor | E |
| **Secretaria** | Cadastrar estágio e TCC aprovados. Emitir declaração e termo. Guardar a versão final | Aprovar ou avaliar | E |
| **Professor orientador** | Ver e acompanhar os próprios orientandos. Registrar visitas. Avaliar. Participar da banca | Ver orientando de outro professor | E |
| **Aluno** | Ver o próprio estágio ou TCC. Enviar relatórios e versões. Ver resultado | Ver avaliação de colega ou nota de banca | E |
| **Responsáveis** | Ver status e resultado do dependente, quando houver | Ver relatório ou avaliação | E, só dependentes com vínculo ativo |
| **Empresa concedente (supervisor)** | Pelo portal de terceiros: avaliar e confirmar horas do próprio estagiário | Ver outros estagiários. Ver a instituição | Terceiros |
| **Membro externo de banca** | Pelo portal de terceiros: lançar a avaliação da própria banca | Ver outras bancas ou a nota dos colegas antes do fim | Terceiros |
| **Terceiros** | Só os itens liberados pelo próprio vínculo | Qualquer outro item | E |

---

#### 5. Integrações

| Módulo | Relação |
|---|---|
| Estrutura ([59](../../../docs/v2/59-estrutura-academica-por-portal.md)) | Estágio e TCC são disciplinas do curso. Carga horária e tipos |
| Diário ([61](../../../docs/v2/61-diario-escolar-por-portal.md)) | Visitas e avaliações de orientação seguem o diário, quando houver |
| Boletim e resultado ([62](../../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md)) | Resultado do estágio e do TCC |
| Contratos ([33](../../../docs/v2/33-contratos-por-portal.md)) | Convênio com empresa concedente |
| Documentos ([48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md)) | Termo, ata, declaração de conclusão e histórico |
| Formulários ([41](../../../docs/v2/41-formularios-e-pesquisas.md)) | Avaliação do supervisor e do orientador, e da banca |
| Agendamento ([44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)) e aula online ([40](../../../docs/v2/40-aulas-online-por-portal.md)) | Defesa em sala ou por link |
| Notificações ([57](../../../docs/v2/57-notificacoes-por-portal.md)) | Prazo, horas abaixo do esperado, resultado |

---

#### 6. Pessoas de fora do sistema

Supervisor da empresa e membro externo de banca têm conta no portal de terceiros ([38](../../../docs/v2/38-portal-de-terceiros-prestadores.md)), com acesso só aos próprios itens. Não veem dados de outros estudantes nem de outras bancas. Decidido em ETC-04. A conta é criada pela secretaria, com verificação de e-mail ([06](../../../docs/v2/06-identidade-acesso.md)).

---

#### 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| ETC-01 | Limite semanal e total de jornada de estágio (seção 2.2) | **Conferido** em 03/11/2026: Lei 11.788/2008, arts. 10 e 11 |
| ETC-02 | Estágio não obrigatório: bolsa, auxílio e benefício (seção 2.1) | Texto da lei conferido em 03/11/2026 (Lei 11.788/2008, arts. 9º, 12 e 13) e registrado na seção 2.1. Parecer do (jurídico) pendente |
| ETC-03 | Carga horária mínima de estágio obrigatório por curso (seção 2.1) | **Conferido** em 03/11/2026: a lei não fixa horas e remete ao projeto do curso (Lei 11.788/2008, art. 2º, § 1º). O valor fica no curso, em [59](../../../docs/v2/59-estrutura-academica-por-portal.md) |
| ETC-04 | Supervisor de empresa e membro externo acessam (seção 6) | **Decidido** em 03/11/2026: conta no portal de terceiros |
| ETC-05 | Publicação de TCC em repositório: autorização do aluno e prazo de acesso (seção 3.6) | (jurídico) |
| ETC-06 | Verificação de similaridade (plágio) no TCC | **Decidido** em 03/11/2026: não nesta versão |
| ETC-07 | Percentual de horas mensais abaixo do esperado para alerta (seção 2.4) | **Decidido** em 03/11/2026: 20% abaixo do previsto |
| ETC-08 | Nova tentativa de TCC reprovado (seção 3.3) | (verificar) |
| ETC-09 | DDL das tabelas: estágio, horas, relatório, supervisão, TCC, versão, banca e avaliação | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.10. Revisão do owner pendente (DDL-01) |

---

#### 8. Critérios de aceite

- [ ] Estágio não vira `ativo` sem termo assinado pelas três partes e apólice válida (teste).
- [ ] Estágio `concluido` sem avaliação do supervisor e do orientador é recusado (teste).
- [ ] Supervisor de empresa não vê outro estagiário, e membro externo não vê outra banca (teste de isolamento).
- [ ] Nota da banca não aparece antes de todos os membros lançarem (teste).
- [ ] Versão final sem autorização do aluno não vai para o repositório público (teste).
- [ ] Declaração de conclusão não sai sem resultado registrado (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).
