# Gestão pastoral

- Portal: Gestão (`gestao.`)
- Área: Acadêmico
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [43](../../../docs/v2/43-pastoral-por-portal.md) (integral)
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Gerir agenda pastoral, escalas litúrgicas, intenções, eventos e celebrações, tradições religiosas (ecumênico) e ações sociais com beneficiários e doações, protegendo dados de alto risco.

## 3. Telas

- **Agenda pastoral** (calendário) e **escalas** (quadro por celebração).
- **Eventos e inscrições** (lista; autorização do responsável para menor).
- **Campanhas e ações sociais** (lista; beneficiários com acesso restrito; doações).
- **Relatório agregado** (dashboard para a gestão, sem identificação).

## 4. Permissões por portal (extraídas do SDD)

Do [43](../../../docs/v2/43-pastoral-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver agenda pastoral, aprovar evento, ver relatório agregado de ações e doações, gerenciar escalas | Ver intenção, anotação de acompanhamento, cadastro de beneficiário ou dado de doador identificado sem papel do módulo | E |

## 5. Papéis

- `unit.pastoral`: agenda, escala, evento, campanha e beneficiário dentro da campanha.
- `unit.manager`: aprovar evento, relatório agregado, gerenciar escalas.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Confissões: só horário público (seção 13, 2.1). Acompanhamento espiritual: restrito ao acompanhante (2.2).
- Beneficiário é dado de vulnerabilidade: exportação só com auditoria (2.3).
- Menores: regras da seção 13, 6.

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

### 13.1 [43 — Gestão Pastoral, por Portal (eventos, missas e celebrações, ações sociais)](../../../docs/v2/43-pastoral-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Matriz de portais em [31](../../../docs/v2/31-matriz-portais-modulos.md). Formulários de inscrição e pesquisa em [41](../../../docs/v2/41-formularios-e-pesquisas.md). Espaços e equipamentos em [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md). Eventos da escola em [17](../../../docs/v2/17-regras-modulos.md). Dado sensível em [07](../../../docs/v2/07-privacidade-lgpd.md) e [26](../../../docs/v2/26-sdd-juridico-regulatorio.md). Doações e receitas em [33](../../../docs/v2/33-contratos-por-portal.md) e [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md). Terceiros em [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md). Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** análise e especificação proposta, criada em 03/11/2026. A v1 tem a Gestão Pastoral só como lista de nomes na navegação ("Gestão Pastoral PRO", seção 4.2 de [`12-portals-navigation-sidebar-pages-spec.md`](../../../docs/v2/anexo-v1/12-portals-navigation-sidebar-pages-spec.md)), sem especificação. Missas e celebrações não aparecem na v1. Itens **[Decisão do autor]** e **(jurídico)** dependem de resposta ou parecer. Não é parecer.

---

#### 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| A gestão pastoral está especificada? | **Não.** Existe só a lista de nomes: Acompanhamento Espiritual, Encontros de Jovens, Ações Sociais, Confissões, Capelania Escolar |
| Eventos, missas e celebrações? | **Não.** A v1 tem "Festividades" em Gestão de Eventos, mas não tem agenda litúrgica, escala de celebrantes nem intenções |
| Ações sociais? | **Não.** O nome aparece, sem cadastro de beneficiário, campanha, entrega ou doação |
| Organizada por portal? | **Não.** Nenhum portal é definido |
| Há risco de privacidade? | **Sim, alto.** "Confissões" e "Acompanhamento Espiritual" tratam de convicção religiosa e de vida íntima. "Ações Sociais" trata de situação de vulnerabilidade |

---

#### 2. Itens de alto risco

##### 2.1 Confissões: mantido só como horário público

Confissão é sacramento. Um sistema que registra que alguém se confessou, com quem e quando, guarda dado sensível de convicção religiosa e uma informação que a própria instituição não deveria ter. Não há regra segura que torne isso aceitável.

**Decidido pelo autor em 03/11/2026: manter, com regra própria.** O sistema não registra confissão: não guarda quem se confessou, quando, nem presença, nem conteúdo. Não existe campo de pessoa nem de conteúdo ligado a confissão em nenhuma tabela. Na agenda de celebrações (seção 3), o horário de confissão aparece como horário público do local, sem vínculo com pessoa. Só aparece quando a tradição estiver habilitada (seção 3.5).

Pedido para registrar confissão, por qualquer portal, é recusado pelo sistema.

##### 2.2 Acompanhamento espiritual: restrito ao acompanhante

Anotação sobre vida espiritual, dúvidas de fé, luto ou crise pessoal é dado sensível (LGPD, art. 5º, II e art. 11). Regras:

- Adesão voluntária. O aluno ou o responsável (se menor) aceita por escrito, com finalidade e prazo.
- Só o acompanhante cadastrado vê as anotações. Coordenação, direção e RH não veem o conteúdo.
- Sem exportação, sem relatório com nome, sem envio a terceiro.
- Anotação pode ser retirada pelo titular, com exclusão do conteúdo e registro da exclusão sem o dado ([29](../../../docs/v2/29-auditoria.md)).
- Se houver risco à integridade do aluno, o acompanhante aciona o canal definido pela entidade ([35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md) e [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md)). A anotação em si não é repassada automaticamente.

##### 2.3 Ações sociais: beneficiário é dado de vulnerabilidade

Cadastro de família ou pessoa atendida, renda, moradia, situação de desemprego ou de saúde é dado sensível ou de alto risco. Regras na seção 5.

---

#### 3. Eventos e celebrações

##### 3.1 Agenda pastoral

| Tipo | Exemplo | Regra |
|---|---|---|
| Missa | Missa de domingo, missa de unidade, missa de formatura | Data, horário, local, celebrante |
| Celebração | Celebração da Palavra, bênção, ato ecumênico, oração | Mesmo modelo. Tipo define a escala litúrgica |
| Evento | Retiro, encontro de jovens, festa junina, feira solidária | Pode ter inscrição, capacidade, custo e certificado |
| Atividade de capelania | Atendimento de capelão, visita, reunião de pastoral | Agenda do capelão. Não é lançada como presença de aluno |

Local de celebração é reservado pelo módulo de [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md). Capela, auditório e pátio aparecem como ambiente.

##### 3.2 Escala litúrgica

| Função | Regra |
|---|---|
| Celebrante | Vinculado à agenda. Pessoa de fora da entidade é cadastrada como convidado, com documento só quando exigido pela norma do local |
| Leitor, ministro, coroinha, músico | Escala por celebração, com confirmação |
| Coroinha ou menor de idade | Só com consentimento do responsável, e sem imagem de criança publicada sem autorização expressa |
| Substituição | Troca registrada, com motivo. Substituto confirmado |

##### 3.3 Intenções de missa

Intenção é um pedido de oração por alguém. Costuma citar nome de pessoa, falecida ou doente.

| Regra | Detalhe |
|---|---|
| Campo | Texto livre limitado a nome e uma frase. Dado de saúde não é registrado, mesmo quando o pedido cita doença |
| Visibilidade | Só a equipe pastoral. Não aparece em portal de aluno, responsável ou terceiro |
| Retenção | Excluída após a celebração e um período fixo, a definir **(jurídico)** |
| Publicação | Lista de intenções só é impressa ou exibida com autorização de quem fez o pedido |

##### 3.4 Inscrição e presença em eventos

- Inscrição por formulário ([41](../../../docs/v2/41-formularios-e-pesquisas.md)), com capacidade e prazo.
- Presença em evento de pastoral não é presença acadêmica, a não ser que o evento seja marcado como atividade curricular pela entidade.
- Certificado de participação é emitido pelo módulo de documentos da secretaria ([17](../../../docs/v2/17-regras-modulos.md)).

---

##### 3.5 Tradições religiosas (ecumênico)

**Decidido pelo autor em 03/11/2026:** a pastoral é configurável por entidade, para atender escolas de qualquer tradição.

| Regra | Detalhe |
|---|---|
| Tradições habilitadas | A entidade escolhe as tradições que atende: católica, evangélica, espírita, judaica, islâmica, ortodoxa e outras. Pode escolher mais de uma |
| Modo ecumênico | Opção própria, para atividades que reúnem várias tradições: oração, bênção, ato inter-religioso. Não usa sacramento de uma tradição específica |
| Tipos por tradição | Cada tradição define os tipos de celebração e os papéis da escala. Ex.: confissão só aparece para a tradição que a pratica |
| Participação | Opcional para aluno. Não há obrigação de participar de celebração de tradição diferente da própria |
| Menor | Participação de menor em celebração segue a regra da seção 6 |
| Dado de convicção | A tradição do aluno não é coletada. Quando for necessária para uma escala ou atividade, é campo opcional, com consentimento, e visível só à equipe pastoral |

#### 4. Ações sociais

| Recurso | Regra |
|---|---|
| Campanha | Título, período, meta (ex.: arrecadar 200 cestas), responsável, prestação de contas |
| Doação | Valor, data, doador (identificado ou anônimo), destino. Lançada no financeiro como receita, com origem registrada ([34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md)). Doação anônima não grava identificador |
| Beneficiário | Cadastro mínimo: nome, responsável pelo núcleo familiar, contato, número de pessoas. Sem renda detalhada, salvo quando a campanha exige, com base legal |
| Entrega | Data, item, quantidade, quem recebeu. Sem dado de saúde |
| Triagem | Critério escrito por campanha. Decisão registrada com quem decidiu |
| Prestação de contas | Relatório agregado. Sem nome de beneficiário |

**Minimização:** campanha que não precisa de renda não a coleta. A regra é da campanha, não do sistema.

**Retenção:** cadastro de beneficiário tem prazo após o último atendimento, a definir **(jurídico)**. Enquanto não houver prazo, o cadastro não é expurgado automaticamente, e o registro fica marcado para revisão.

**Menor de idade:** ação com criança segue consentimento do responsável (seção 6).

---

#### 5. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Nada sobre o conteúdo. Modelos de escala e de campanha, sem dado | Ver qualquer dado pastoral de entidade | P |
| **Gestão** | Ver agenda pastoral, aprovar evento, ver relatório agregado de ações e doações, gerenciar escalas | Ver intenção, anotação de acompanhamento, cadastro de beneficiário ou dado de doador identificado sem papel do módulo | E |
| **Equipe pastoral** (capelão, coordenador, voluntário) | Gerenciar agenda, escala, evento, campanha e cadastro de beneficiário dentro da campanha | Ver anotação de acompanhamento que não é a sua. Exportar beneficiário sem auditoria | E |
| **Professor** | Ver agenda de celebração e evento da escola. Confirmar presença na própria escala, se for leitor ou convidado | Ver escala de outra pessoa, intenção ou beneficiário | E |
| **Aluno** | Ver agenda, inscrever-se em evento e em campanha, aceitar escala de leitura | Ver anotação de acompanhamento, intenção, beneficiário ou doação de colega | E |
| **Responsáveis** | Ver agenda, autorizar participação de dependente menor, inscrever-se em campanha como família | Ver anotação, intenção, escala de outro aluno ou cadastro de outra família | E, só dependentes com vínculo ativo |
| **Terceiros** | Fornecedor de evento (buffet, som, decoração) vê só a data, o local e a quantidade, pelo contrato em [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md). Pode ser cadastrado como tipo personalizado (TER-01) | Ver escala, intenção, beneficiário ou presença | E |

---

#### 6. Menores de idade

- Evento com participação de menor exige autorização do responsável, registrada, com validade.
- Encontro de jovens é atividade com menor. Decidido pelo autor em 03/11/2026: o contato de adulto com menor é só em grupo, com dois adultos presentes. Contato individual não é permitido, nem com aviso ao responsável.
- Imagem de menor em evento não é publicada sem autorização específica do responsável ([35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md), seção 6, e [26](../../../docs/v2/26-sdd-juridico-regulatorio.md)).

---

#### 7. Modelo de dados proposto

Tabelas no banco da unidade. Não é o DDL final.

| Tabela | Conteúdo | Sensibilidade |
|---|---|---|
| `pastoral_agenda` | Tipo, data, local, celebrante, estado | Normal |
| `pastoral_escala` | Função, pessoa, celebração, confirmação, substituição | Normal |
| `pastoral_intencao` | Nome e frase. Sem dado de saúde. Retenção curta | Sensível |
| `pastoral_acompanhamento` | Anotação. Acesso só do acompanhante. Sem exportação | Sensível |
| `pastoral_campanha` | Campanha, meta, período, responsável | Normal |
| `pastoral_beneficiario` | Cadastro mínimo, criptografado nos campos pessoais | Sensível |
| `pastoral_entrega` | Item, quantidade, data. Vínculo ao beneficiário | Pessoal |
| `pastoral_doacao` | Valor, data, doador ou anônimo. Vínculo ao financeiro | Pessoal |

Campos de `pastoral_acompanhamento` e `pastoral_beneficiario` são cifrados na aplicação, com chave do cofre ([05](../../../docs/v2/05-seguranca.md)).

---

#### 8. Pendências

| # | Pendência | Tipo |
|---|---|---|
| PAS-01 | Confissões: mantido só como horário público (seção 2.1) | **Decidido** em 03/11/2026 |
| PAS-02 | Acompanhamento espiritual: adesão voluntária e visibilidade só do acompanhante (seção 2.2) | **Decidido** em 03/11/2026. Parecer de (jurídico) pendente |
| PAS-03 | Retenção de intenção de missa (seção 3.3) | (jurídico) |
| PAS-04 | Retenção de cadastro de beneficiário (seção 4) | (jurídico) |
| PAS-05 | Consentimento de menor para evento, escala e imagem (seção 6) | (jurídico) |
| PAS-06 | Campanhas com renda: base legal de coleta (seção 4) | (jurídico) |
| PAS-07 | Contato adulto e menor em encontro de jovens: só em grupo, com dois adultos | **Decidido** em 03/11/2026 |
| PAS-08 | Tradições religiosas (seção 3.5) | **Decidido:** configurável por entidade, com modo ecumênico |
| PAS-09 | Aviso de risco ao aluno: coordenação pedagógica e psicólogo, sem o conteúdo da anotação (seção 2.2) | **Decidido** em 03/11/2026 |
| PAS-10 | DDL das tabelas da seção 7 | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 7. Revisão do owner pendente (DDL-01) |

---

#### 9. Critérios de aceite

- [ ] Não existe registro de confissão em nenhuma tela, tabela ou log (varredura).
- [ ] Anotação de acompanhamento não aparece para gestão, RH, responsável ou terceiro (teste de isolamento).
- [ ] Intenção não aparece fora da equipe pastoral (teste).
- [ ] Doação anônima não grava identificador (teste de banco).
- [ ] Menor não entra em evento sem autorização registrada e válida (teste).
- [ ] Relatório de ação social não traz nome de beneficiário (varredura).
- [ ] Exportação de beneficiário gera evento de auditoria com motivo (teste).
- [ ] Itens **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).
