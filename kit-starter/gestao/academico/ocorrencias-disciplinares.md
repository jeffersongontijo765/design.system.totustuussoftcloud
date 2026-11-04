# Ocorrências disciplinares

- Portal: Gestão (`gestao.`)
- Área: Acadêmico
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [63](../../../docs/v2/63-ocorrencias-disciplinares-por-portal.md) (integral)
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Registrar ocorrências disciplinares com tipo e gravidade, fluxo de análise, medidas educativas, contestação, afastamento e notificação ao responsável, com sigilo do relato e proteção de dado de terceiro.

## 3. Telas

- **Ocorrências** (DataTable): aluno, turma, tipo, gravidade, estado, data; filtros; relato mascarado na lista.
- **Nova ocorrência** (formulário): campos da seção 13 (4.1), envolvidos, testemunhas, anexos; dado de terceiro marcado.
- **Ocorrência — detalhe** (página): linha do tempo do fluxo, medidas, contestação, notificação ao responsável, decisão.
- **Denúncia de violência** (fluxo restrito): canal sigiloso e encaminhamento obrigatório (seção 13, 6.3).
- **Painel** (dashboard agregado, sem identificação): ocorrências por tipo, gravidade e turma.

## 4. Permissões por portal (extraídas do SDD)

Do [63](../../../docs/v2/63-ocorrencias-disciplinares-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver indicadores agregados: quantidade por tipo e gravidade, sem nome | Ver relato. Decidir medida disciplinar de aluno | E |
| **Coordenação** | Ver tudo da unidade. Confirmar fato, aplicar medida, alterar gravidade com justificativa, decidir afastamento | Alterar relato de outro registro sem motivo | E |
| **Secretaria** | Ver o status e a comunicação enviada. Gerar documento autorizado | Ver relato. Registrar ocorrência | E |

## 5. Papéis

- `unit.coordinator`: registrar, analisar, aplicar medida, notificar responsável.
- `unit.manager`: afastamento e decisões de gravidade alta.
- `teacher`: registrar ocorrência da própria turma.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Relato visível só a quem a seção 13 (6.1) permite; nome de terceiro não aparece para o responsável do outro aluno.
- Contestação do responsável ou aluno tem prazo e decisão fundamentada.
- Denúncia de violência segue o encaminhamento legal descrito na seção 13.

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

### 13.1 [63 — Ocorrências Disciplinares e de Convivência, por Portal](../../../docs/v2/63-ocorrencias-disciplinares-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Sexta lacuna da ordem de [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), seção 3. Alimenta a pauta do conselho ([62](../../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md), seção 5.1). Aviso ao responsável em [57](../../../docs/v2/57-notificacoes-por-portal.md). Dado sensível e regra de saúde em [18](../../../docs/v2/18-regras-modulos-2.md), seção 3.3. Pedido de revisão pelo atendimento em [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md). Decisão disciplinar fora da IA em [27](../../../docs/v2/27-inteligencia-artificial-e-portais.md), seção 5.1. Ocorrência de segurança do trabalho, que é outra coisa, em [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md) e [52](../../../docs/v2/52-medicina-do-trabalho-especificacao.md). Ocorrência de portaria em [35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md). Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 6 do acadêmico. Pontos que dependem de norma ou de decisão do autor estão marcados.

---

#### 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Ocorrência disciplinar tem regra? | **Não.** Só aparece como lacuna em [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md) e em [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md) |
| Há ocorrência em outro contexto? | **Sim, em três.** Ocorrência de SST em [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md) e [52](../../../docs/v2/52-medicina-do-trabalho-especificacao.md). Ocorrência de portaria em [35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md). Ocorrência de frota em outro módulo. Nenhum deles é disciplinar |
| Pode ser misturada com esses? | **Não.** Cada tipo tem tabela, regra e permissão próprias |
| A v1 tem algo? | **Só o esqueleto:** entidade `occurrences`, timeline no perfil do aluno, API de registro, kanban de tratamento e aviso ao responsável para ocorrência grave |

---

#### 2. O que é e o que não é

**É:** registro de um fato observado, com data, local, pessoas envolvidas e relato objetivo, e o encaminhamento que a escola deu.

**Não é:**

- **Julgamento de caráter.** O relato descreve o fato. Não usa rótulo sobre a pessoa.
- **Registro de saúde.** Atendimento de enfermaria, de crise ou de lesão segue o registro de saúde do aluno, com restrição de acesso ([18](../../../docs/v2/18-regras-modulos-2.md), seção 3.3). Não entra aqui.
- **Denúncia de violência contra o aluno.** Esse caso segue a seção 6.3. Não é tratado como disciplina.
- **Saída ou atraso na portaria.** Segue [35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md).

---

#### 3. Tipos e gravidade

##### 3.1 Tipos

| Tipo | Exemplo |
|---|---|
| Convivência | Desrespeito entre alunos, briga, uso de linguagem ofensiva |
| Conduta em aula | Atrapalhar a aula, sair sem autorização, recusar atividade |
| Segurança | Brincadeira perigosa, objeto perigoso, acesso a área restrita |
| Integridade acadêmica | Fraude em avaliação, plágio, falsificação de documento |
| Uso de meio digital | Mensagem ofensiva, imagem sem autorização, perfil falso |
| Outro | Descrição livre, com justificativa |

**Decidido** em 03/11/2026 (OCO-01): lista padrão da plataforma, que a escola ajusta (inclui, renomeia ou desativa tipo). É o mesmo critério de DIA-01 em [61](../../../docs/v2/61-diario-escolar-por-portal.md).

##### 3.2 Gravidade

| Gravidade | Efeito |
|---|---|
| Leve | Registro e comunicação ao responsável pelo canal padrão |
| Média | Registro, comunicação e conversa com a coordenação |
| Grave | Aviso imediato ao responsável e à coordenação ([57](../../../docs/v2/57-notificacoes-por-portal.md)). Entra na pauta do conselho |
| Gravíssima | Aviso imediato à direção e à coordenação. Pode haver afastamento, decidido pela direção ou pela coordenação (seção 5.3) |

A gravidade é escolhida por quem registra e pode ser alterada pela coordenação com justificativa. A IA não sugere gravidade ([27](../../../docs/v2/27-inteligencia-artificial-e-portais.md), seção 5.1).

---

#### 4. Registro e fluxo

##### 4.1 Campos do registro

| Campo | Regra |
|---|---|
| Alunos envolvidos | Um ou mais, com vínculo ativo na turma ou na unidade |
| Data e hora do fato | Não pode ser futura. Pode ser anterior ao registro, com motivo se passar de 2 dias úteis. **Decidido** em 03/11/2026 |
| Local | Lista da unidade ([44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)) ou texto livre |
| Relato | Texto objetivo. Sem juízo sobre caráter. Sem dado de outro aluno além do necessário |
| Testemunhas | Opcional. Registradas como pessoa do cadastro, quando houver |
| Anexos | Fotos, prints ou documentos, com limite de tamanho. Imagem de outro aluno, que é menor, não é mostrada no aviso. Segue a regra de imagem de menor de [40](../../../docs/v2/40-aulas-online-por-portal.md) |
| Gravidade e tipo | Seção 3 |

##### 4.2 Estados

`registrada` → `em_analise` → `comunicada` → `com_medida` → `encerrada`, com `arquivada` quando o fato não procede.

- `registrada`: quem registrou ainda pode corrigir o relato. Depois de `comunicada`, correção vira nova versão.
- `em_analise`: a coordenação confirma o fato e pode ouvir o aluno e a testemunha.
- `comunicada`: o responsável recebe o aviso ([57](../../../docs/v2/57-notificacoes-por-portal.md)), sem o relato de terceiros (seção 6.2).
- `com_medida`: medida educativa registrada (seção 5).
- `encerrada`: medida cumprida ou sem medida.
- `arquivada`: fato não confirmado. Permanece no histórico, com motivo.

##### 4.3 Regras do fluxo

- Ocorrência não pode ser excluída. Só `arquivada`, com motivo.
- Toda mudança de estado gera evento de auditoria ([29](../../../docs/v2/29-auditoria.md)).
- Ocorrência grave vai direto para `comunicada`, sem esperar análise, para o responsável ser avisado a tempo.

---

#### 5. Medidas e contestação

##### 5.1 Medidas educativas

Medida educativa é a resposta pedagógica: conversa, orientação, plano de convivência, reparação, acompanhamento com a equipe pedagógica. Cada medida tem responsável, prazo e resultado.

##### 5.2 Contestação

- O responsável pode contestar a ocorrência pelo atendimento ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md)), dentro do prazo.
- Contestação não suspende a medida educativa, salvo decisão da direção.
- Resposta à contestação é registrada, com motivo, e a versão da ocorrência fica no histórico.
- Prazo de contestação: 5 dias úteis, como o prazo de justificativa de falta ([61](../../../docs/v2/61-diario-escolar-por-portal.md), DIA-02). **Decidido** em 03/11/2026.

##### 5.3 Afastamento

- Suspensão de aula ou afastamento de atividade é decisão da direção ou da coordenação, registrada com fundamento e prazo. **Decidido** em 03/11/2026.
- Antes de aplicar, a escola ouve o aluno e o responsável, e comunica por escrito.
- O regime de afastamento, o prazo máximo e a forma de comunicação dependem da legislação do sistema de ensino **(jurídico)**.
- Afastamento não gera falta para o aluno sem decisão da direção sobre o efeito na frequência **(verificar)**.

---

#### 6. Sigilo e dados

##### 6.1 Quem vê o relato

| Papel | Vê o relato | Vê a medida | Vê a contestação |
|---|---|---|---|
| Quem registrou | Sim, o próprio registro | Sim | Não |
| Coordenação | Sim | Sim | Sim |
| Direção | Sim | Sim | Sim |
| Secretaria | Não | Não | Não |
| Professor da turma | Só o que registrou | Não | Não |
| Aluno envolvido | Não | Sim, a medida que lhe cabe | Não |
| Responsável do aluno | Não | Sim, a medida e a comunicação | Sim, a própria contestação |

##### 6.2 Dado de terceiro

- O relato pode citar outros alunos. Ao aviso ao responsável, ele não é mostrado. Mostra-se só o tipo, a data e a medida.
- Relato com dado de saúde ou de conduta de outro aluno fica em campo restrito ([18](../../../docs/v2/18-regras-modulos-2.md), seção 3.3).

##### 6.3 Denúncia de violência

- Relato de violência, abuso, maus-tratos ou exploração contra o aluno **não entra como ocorrência disciplinar**.
- Abre protocolo próprio, com encaminhamento imediato à direção e ao canal que a legislação indicar **(jurídico)**. Ex.: conselho tutelar.
- O registro fica com acesso restrito à direção. Nenhum aviso automático é enviado ao suposto agressor.
- A IA não atua nesse caso ([27](../../../docs/v2/27-inteligencia-artificial-e-portais.md)).

##### 6.4 Armazenamento

- O relato sensível é cifrado na aplicação, como as anotações sensíveis de [51](../../../docs/v2/51-ddl-modulos-novos.md).
- Acesso ao relato gera evento de auditoria com motivo ([29](../../../docs/v2/29-auditoria.md)).

---

#### 7. Relação com outros módulos

| Módulo | Relação |
|---|---|
| Conselho de classe ([62](../../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md)) | Ocorrências do período entram na pauta. Ocorrência não decide resultado sozinha |
| Notificações ([57](../../../docs/v2/57-notificacoes-por-portal.md)) | Aviso ao responsável, com canal por gravidade |
| Atendimento ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md)) | Contestação por protocolo |
| Documentos ([48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md)) | Declaração de comportamento e transferência só se a escola configurar. Ver OCO-04 |
| Boletim ([62](../../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md)) | Ocorrência não entra no boletim, salvo decisão em OCO-04 |
| Matrícula ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md)) | Ocorrência não impede rematrícula. Medida de desligamento segue a norma **(jurídico)** |
| Pastoral ([43](../../../docs/v2/43-pastoral-por-portal.md)) | Confissão e acompanhamento espiritual não viram ocorrência |
| Preceptoria ([42](../../../docs/v2/42-preceptoria-por-portal.md)) | Não se aplica. Fica separada |

---

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

---

#### 9. Pendências

| # | Pendência | Tipo |
|---|---|---|
| OCO-01 | Lista padrão de tipos e gravidades (seção 3) | **Decidido** em 03/11/2026: lista padrão da plataforma, que a escola ajusta |
| OCO-02 | Quem aplica afastamento (seção 5.3) | **Decidido** em 03/11/2026: direção ou coordenação. Forma, prazo máximo e comunicação do afastamento seguem a legislação (jurídico), seção 5.3 |
| OCO-03 | Prazo de contestação do responsável (seção 5.2) | **Decidido** em 03/11/2026: 5 dias úteis |
| OCO-04 | Ocorrência aparece no boletim ou em declaração de comportamento? (seções 6 e 7) | **Decidido** em 03/11/2026: não |
| OCO-05 | Responsável vê relato ou só comunicação e medida (seção 6.1) | **Decidido** em 03/11/2026: só comunicação e medida |
| OCO-06 | Protocolo de violência: canal e prazo de encaminhamento (seção 6.3) | (jurídico) |
| OCO-07 | Prazo de guarda de ocorrência e de medida | (jurídico) |
| OCO-08 | Efeito de afastamento na frequência (seção 5.3) | (verificar) |
| OCO-09 | DDL das tabelas: ocorrência, versão do relato, envolvido, medida, contestação e evento de acesso ao relato | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.8. Revisão do owner pendente (DDL-01) |

---

#### 10. Critérios de aceite

- [ ] Ocorrência não é excluída, só arquivada com motivo (teste).
- [ ] Professor de outra turma não vê nem registra ocorrência (teste de isolamento).
- [ ] Responsável não vê relato nem nome de outro aluno no aviso (varredura do aviso e teste de isolamento).
- [ ] Ocorrência grave gera aviso imediato ao responsável e à coordenação (teste com [57](../../../docs/v2/57-notificacoes-por-portal.md)).
- [ ] Relato de violência não entra como ocorrência disciplinar e não gera aviso ao suposto agressor (teste).
- [ ] IA não sugere gravidade nem medida (teste de [27](../../../docs/v2/27-inteligencia-artificial-e-portais.md), seção 5.1).
- [ ] Acesso ao relato gera evento de auditoria (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).
