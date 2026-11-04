# Acompanhamento pedagógico

- Portal: Professor (`portal-do-professor.`)
- Área: Acompanhamento pedagógico
- Domínio: entidade: banco da unidade; o professor vê **só as turmas e disciplinas em que tem vínculo ativo** ([17](../../docs/v2/17-regras-modulos.md), seção 4.4; [06](../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [63](../../docs/v2/63-ocorrencias-disciplinares-por-portal.md), seção 8; [65](../../docs/v2/65-estagio-e-tcc-por-portal.md), seção 4; [42](../../docs/v2/42-preceptoria-por-portal.md), seção 5; [66](../../docs/v2/66-prontuario-e-portfolio-do-aluno-por-portal.md), seção 4; [41](../../docs/v2/41-formularios-e-pesquisas.md), seção 6; [43](../../docs/v2/43-pastoral-por-portal.md), seção 5
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Ocorrências da turma, orientação de estágio e TCC, preceptoria (quando o professor é preceptor), portfólio dos alunos, formulários e pastoral.

## 3. Telas

- **Ocorrências** (registrar ocorrência da própria turma).
- **Orientandos** (estágio e TCC: horas, versões, banca).
- **Preceptoria** (avaliar residentes vinculados, tutoria, metas, evidências).
- **Portfólio** (avaliar evidências dos alunos).
- **Formulários** (responder e, quando permitido, criar para a turma).
- **Pastoral** (confirmar presença na própria escala).

## 4. Permissões por portal (extraídas do SDD)

Do [63](../../docs/v2/63-ocorrencias-disciplinares-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Professor** | Registrar ocorrência das próprias turmas. Ver o próprio registro | Ver ocorrência de outra turma. Ver medida | E |

Do [65](../../docs/v2/65-estagio-e-tcc-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Professor orientador** | Ver e acompanhar os próprios orientandos. Registrar visitas. Avaliar. Participar da banca | Ver orientando de outro professor | E |

Do [42](../../docs/v2/42-preceptoria-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Preceptor** | Responder avaliação dos seus residentes. Registrar tutoria e metas dos seus tutorados. Validar evidência. Devolver ou aprovar | Ver residente sem vínculo ativo no programa. Ver avaliação de outro preceptor | E |

Do [66](../../docs/v2/66-prontuario-e-portfolio-do-aluno-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Professor** | Ver o portfólio da própria disciplina. Avaliar. Publicar material de aula | Ver prontuário. Ver portfólio de outra disciplina | E |

Do [41](../../docs/v2/41-formularios-e-pesquisas.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Professor** | Criar pesquisa para a própria turma (ex.: satisfação com a disciplina). Ver relatório da turma acima do mínimo | Pesquisa sobre colega ou ver resposta de outra turma | E |

Do [43](../../docs/v2/43-pastoral-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Professor** | Ver agenda de celebração e evento da escola. Confirmar presença na própria escala, se for leitor ou convidado | Ver escala de outra pessoa, intenção ou beneficiário | E |

## 5. Papéis

- `teacher` (nível 1, escopo turma): ações das próprias turmas.
- `teacher.coordinator` (nível 2, unidade): aprova planos e lançamentos de nível 1 da unidade ([78](../../docs/v2/78-permissoes-e-papeis.md), seção 4.3).
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Cada módulo só mostra alunos com vínculo à turma ou orientação do professor.

## 7. Dados

- Tabelas e campos conforme a seção 13 e o DDL do [51](../../docs/v2/51-ddl-modulos-novos.md), quando o módulo estiver lá. Toda tabela tem `entidade_id`, `unidade_id`, `created_at`, `updated_at`, `created_by` e exclusão lógica com `deleted_at` e `deleted_by` ([03](../../docs/v2/03-dominio-tenancy.md), seção 6; [15](../../docs/v2/15-validacoes.md); [19](../../docs/v2/19-regras-modulos-3.md), seção 14).

## 8. Integrações

- Ver a seção de integrações do documento de origem, na seção 13.

## 9. Exportação, auditoria e privacidade

- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../docs/v2/08-frontend-design-system.md), seção 3).
- Toda criação, alteração, aprovação, exclusão lógica, exportação e leitura de dado sensível gera evento de auditoria no banco da unidade ([29](../../docs/v2/29-auditoria.md)).
- Dados pessoais conforme [07](../../docs/v2/07-privacidade-lgpd.md): mínimo necessário, mascaramento em listas, base legal registrada.

## 10. Estados de interface

- Carregando (skeleton), vazio com chamada para ação, sem resultado de filtro, erro com nova tentativa, acesso negado, registro bloqueado, fechado ou baixado (somente leitura), conflito de edição (versão).

## 11. Requisitos de frontend

- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`): página de lista com DataTable, KPIs, drawer de detalhe, formulário em página ou modal, kanban quando houver fluxo de estados.
- Seletor de unidade no topo quando o usuário tiver mais de uma; a troca reemite o token com o novo contexto ([06](../../docs/v2/06-identidade-acesso.md), seção 12).

## 12. Critérios de aceite e pendências

- Critérios de aceite: os do documento de origem (seção 13) e os de [31](../../docs/v2/31-matriz-portais-modulos.md), seção 6.
- Testes de isolamento: usuário de outra unidade ou entidade recebe 404 em toda rota do módulo ([03](../../docs/v2/03-dominio-tenancy.md)).
- As pendências do documento de origem estão na seção 13 e consolidadas no [45](../../docs/v2/45-pendencias-consolidadas.md).

## 13. Regras da v2 (texto integral das fontes, sem corte)

### 13.1 [63](../../docs/v2/63-ocorrencias-disciplinares-por-portal.md), seção 8

#### 8. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar lista padrão de tipos e modelo de medida, sem dado | Ver ocorrência, relato ou medida de entidade | P |
| **Gestão** | Ver indicadores agregados: quantidade por tipo e gravidade, sem nome | Ver relato. Decidir medida disciplinar de aluno | E |
| **Direção** | Ver tudo. Decidir afastamento | Alterar relato de outro registro sem motivo | E |
| **Coordenação** | Ver tudo da unidade. Confirmar fato, aplicar medida, alterar gravidade com justificativa, decidir afastamento | Alterar relato de outro registro sem motivo | E |
| **Secretaria** | Ver o status e a comunicação enviada. Gerar documento autorizado | Ver relato. Registrar ocorrência | E |
| **Professor** | Registrar ocorrência das próprias turmas. Ver o próprio registro | Ver ocorrência de outra turma. Ver medida | E |
| **Aluno** | Ver a medida que lhe cabe. Enviar contestação por atendimento, se permitido | Ver relato ou ocorrência de colega | E |
| **Responsáveis** | Ver a comunicação, a medida e a própria contestação do dependente | Ver relato, nome de outro aluno ou registro de violência | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item de ocorrência | E |

### 13.2 [65](../../docs/v2/65-estagio-e-tcc-por-portal.md), seção 4

#### 4. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelo de termo e de ata, sem dado | Ver estágio, TCC ou banca de entidade | P |
| **Gestão** | Ver indicadores: estágios ativos, TCCs por status, prazos vencidos. Aprovar convênio com empresa concedente ([33](../../docs/v2/33-contratos-por-portal.md)) | Avaliar aluno ou aprovar resultado | E |
| **Coordenação** | Aprovar estágio e TCC. Autorizar prorrogação. Montar banca. Ver todos da unidade | Lançar nota de avaliação de outro professor | E |
| **Secretaria** | Cadastrar estágio e TCC aprovados. Emitir declaração e termo. Guardar a versão final | Aprovar ou avaliar | E |
| **Professor orientador** | Ver e acompanhar os próprios orientandos. Registrar visitas. Avaliar. Participar da banca | Ver orientando de outro professor | E |
| **Aluno** | Ver o próprio estágio ou TCC. Enviar relatórios e versões. Ver resultado | Ver avaliação de colega ou nota de banca | E |
| **Responsáveis** | Ver status e resultado do dependente, quando houver | Ver relatório ou avaliação | E, só dependentes com vínculo ativo |
| **Empresa concedente (supervisor)** | Pelo portal de terceiros: avaliar e confirmar horas do próprio estagiário | Ver outros estagiários. Ver a instituição | Terceiros |
| **Membro externo de banca** | Pelo portal de terceiros: lançar a avaliação da própria banca | Ver outras bancas ou a nota dos colegas antes do fim | Terceiros |
| **Terceiros** | Só os itens liberados pelo próprio vínculo | Qualquer outro item | E |

### 13.3 [42](../../docs/v2/42-preceptoria-por-portal.md), seção 5

#### 5. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos de instrumento, sem dado | Ver avaliação, PDI ou tutoria de qualquer entidade | P |
| **Gestão** | Criar instrumento, ciclo, programa e pesos. Ver relatório agregado. Gerenciar alertas de divergência. Aprovar devolução. Exportar com auditoria | Ver resposta individual de avaliação do preceptor. Ver anotação de tutoria. Ver PDI sem vínculo de coordenação | E |
| **Preceptor** | Responder avaliação dos seus residentes. Registrar tutoria e metas dos seus tutorados. Validar evidência. Devolver ou aprovar | Ver residente sem vínculo ativo no programa. Ver avaliação de outro preceptor | E |
| **Residente / aluno** | Responder autoavaliação. Ver a própria avaliação depois da conclusão. Ver PDI e metas. Enviar evidência | Ver avaliação de colega. Ver anotação de tutoria. Ver resposta de avaliação de preceptor, que é anônima | E |
| **Responsáveis** | Nada, por padrão. Residente é adulto | Ver avaliação, PDI, tutoria | E. Para aluno **menor** em preceptoria de tutoria, ver regra de consentimento abaixo |
| **Campo de estágio (terceiro)** | Os dados necessários para supervisionar cada estagiário do próprio campo: nome, frequência na prática, metas de prática, avaliação de desempenho na prática e ocorrências do campo | Tutoria, anotação, PDI, avaliação de outro campo e dado de saúde além de apto ou inapto para a prática | E, pelo contrato em [38](../../docs/v2/38-portal-de-terceiros-prestadores.md) |

**Menor de idade:** tutoria de aluno menor em preceptoria de tutoria (parte B) exige consentimento do responsável para o registro de tutoria com dado sensível. Sem consentimento, o registro fica limitado a dado de acompanhamento acadêmico ([26](../../docs/v2/26-sdd-juridico-regulatorio.md)) **(jurídico)**.

### 13.4 [66](../../docs/v2/66-prontuario-e-portfolio-do-aluno-por-portal.md), seção 4

#### 4. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelo de prontuário e de portfólio, sem dado | Ver prontuário, saúde ou portfólio de entidade | P |
| **Gestão** | Ver indicador: prontuários completos, documentos vencidos, portfólios publicados | Ver seção de saúde. Ver documento pessoal | E |
| **Coordenação** | Ver o prontuário, inclusive a seção de saúde com CID e diagnóstico. Ver portfólio da unidade | Editar histórico | E |
| **Secretaria** | Gerir documentos pessoais e acadêmicos, requerimentos e comunicações. Ver a seção de saúde, inclusive CID | Editar avaliação do portfólio | E |
| **Enfermagem e médico da escola** | Ver e registrar a seção de saúde e apoio | Ver histórico de notas ou ocorrência, sem necessidade | E |
| **Professor** | Ver o portfólio da própria disciplina. Avaliar. Publicar material de aula | Ver prontuário. Ver portfólio de outra disciplina | E |
| **Aluno** | Ver o próprio prontuário, exceto saúde restrita. Publicar e exportar o próprio portfólio. Ver a avaliação | Ver portfólio ou prontuário de colega | E |
| **Responsáveis** | Ver documentos e comunicações do dependente. Ver o portfólio do dependente menor sempre, e do maior se ele compartilhar | Ver CID ou diagnóstico. Ver portfólio de outro aluno | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item do prontuário ou do portfólio | E |

### 13.5 [41](../../docs/v2/41-formularios-e-pesquisas.md), seção 6

#### 6. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos globais, sem resposta. Ver uso agregado do motor | Ver resposta de qualquer entidade | P |
| **Gestão** | Criar, publicar, convidar, encerrar, ver relatório agregado, exportar com auditoria | Ver resposta nominal de formulário anônimo. Ver resposta de dado sensível sem papel do módulo de origem | E |
| **Professor** | Criar pesquisa para a própria turma (ex.: satisfação com a disciplina). Ver relatório da turma acima do mínimo | Pesquisa sobre colega ou ver resposta de outra turma | E |
| **Aluno** | Responder o que foi convidado. Ver a própria resposta enquanto o formulário não encerrar, quando não for anônimo | Ver resposta de colegas. Responder duas vezes em formulário de resposta única | E |
| **Responsáveis** | Responder pesquisa de família e avaliação de atendimento, por convite | Responder em nome de dependente maior de idade. Ver resposta de outra família | E |
| **Terceiros** | Nada, por padrão. Fornecedor só responde se o contrato prever pesquisa de avaliação de serviço | Ver resposta de qualquer outra pessoa | E, [38](../../docs/v2/38-portal-de-terceiros-prestadores.md) |
| **Convidado externo** | Responder com convite de uso único | Ver qualquer relatório | Fora dos seis portais, pela regra de [40](../../docs/v2/40-aulas-online-por-portal.md) |

### 13.6 [43](../../docs/v2/43-pastoral-por-portal.md), seção 5

#### 5. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Nada sobre o conteúdo. Modelos de escala e de campanha, sem dado | Ver qualquer dado pastoral de entidade | P |
| **Gestão** | Ver agenda pastoral, aprovar evento, ver relatório agregado de ações e doações, gerenciar escalas | Ver intenção, anotação de acompanhamento, cadastro de beneficiário ou dado de doador identificado sem papel do módulo | E |
| **Equipe pastoral** (capelão, coordenador, voluntário) | Gerenciar agenda, escala, evento, campanha e cadastro de beneficiário dentro da campanha | Ver anotação de acompanhamento que não é a sua. Exportar beneficiário sem auditoria | E |
| **Professor** | Ver agenda de celebração e evento da escola. Confirmar presença na própria escala, se for leitor ou convidado | Ver escala de outra pessoa, intenção ou beneficiário | E |
| **Aluno** | Ver agenda, inscrever-se em evento e em campanha, aceitar escala de leitura | Ver anotação de acompanhamento, intenção, beneficiário ou doação de colega | E |
| **Responsáveis** | Ver agenda, autorizar participação de dependente menor, inscrever-se em campanha como família | Ver anotação, intenção, escala de outro aluno ou cadastro de outra família | E, só dependentes com vínculo ativo |
| **Terceiros** | Fornecedor de evento (buffet, som, decoração) vê só a data, o local e a quantidade, pelo contrato em [38](../../docs/v2/38-portal-de-terceiros-prestadores.md). Pode ser cadastrado como tipo personalizado (TER-01) | Ver escala, intenção, beneficiário ou presença | E |
