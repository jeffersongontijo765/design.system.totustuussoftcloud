# Formulários e pesquisas

- Portal: Gestão (`gestao.`)
- Área: Acadêmico
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [41](../../../docs/v2/41-formularios-e-pesquisas.md) (integral)
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Motor compartilhado de formulários e pesquisas (estilo Google Forms e Microsoft Forms) usado por todos os módulos, com anonimato real, dado sensível protegido e relatórios.

## 3. Telas

- **Formulários** (DataTable): título, módulo dono, público, estado, respostas.
- **Editor de formulário** (página): tipos de pergunta, lógica condicional, anonimato, público-alvo, prazo.
- **Respostas e relatórios** (dashboard com gráficos; exportação).

## 4. Permissões por portal (extraídas do SDD)

Do [41](../../../docs/v2/41-formularios-e-pesquisas.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Criar, publicar, convidar, encerrar, ver relatório agregado, exportar com auditoria | Ver resposta nominal de formulário anônimo. Ver resposta de dado sensível sem papel do módulo de origem | E |

## 5. Papéis

- `unit.manager` e `unit.coordinator`: criar e publicar no escopo da unidade.
- Módulo dono do formulário define quem vê as respostas ([41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 6).
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Pesquisa anônima não guarda vínculo com o respondente (seção 13, 3).
- Dado sensível segue a seção 13 (4) e o [07](../../../docs/v2/07-privacidade-lgpd.md).

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

### 13.1 [41 — Formulários e Pesquisas (motor compartilhado, estilo Google Forms e Microsoft Forms)](../../../docs/v2/41-formularios-e-pesquisas.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Consumidores: [42](../../../docs/v2/42-preceptoria-por-portal.md) (avaliações), [43](../../../docs/v2/43-pastoral-por-portal.md) (inscrições e pesquisas), [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md) (questionário de saída e clima), [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md) (CSAT do atendimento). Captura de lead continua em [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 7. Dado sensível em [07](../../../docs/v2/07-privacidade-lgpd.md). Auditoria em [29](../../../docs/v2/29-auditoria.md). Retenção em [21](../../../docs/v2/21-busca-e-armazenamento.md).
> **Status:** especificação proposta, criada em 03/11/2026. A v1 não tem motor de formulários próprio. Há "Gerador de autoavaliação" e "Editor de avaliação" na preceptoria, "formulário dinâmico por tipo" e "questionário de saída" no RH, e "Formulários e Jornadas" no System Builder. Cada um foi feito à parte. Itens **[Decisão do autor]** e **(jurídico)** dependem de resposta ou parecer.

---

#### 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Existe motor de formulários na v2? | **Não.** Cada módulo que precisa de formulário teria o seu. Isso duplica regra de anonimato, versão e relatório |
| Quem precisa? | Preceptoria, RH, pastoral, atendimento (CSAT), secretaria (pesquisa de satisfação) e professor (pesquisa de turma) |
| Captura de lead é o mesmo produto? | **Não.** Captura de lead é função do CRM ([22](../../../docs/v2/22-crm-canais-e-papeis.md)). O motor pode ser usado, mas a regra de origem permitida e de aceite continua a de 22 |
| Pode ser anônimo? | **Sim, com regra própria.** Resposta anônima não guarda identificador. Relatório por grupo só aparece acima de um mínimo de respostas |

**Decisão de desenho:** um motor único, com donos diferentes. O formulário pertence ao módulo que o criou (ex.: preceptoria). O motor fornece construção, publicação, convite, resposta, anonimato e relatório.

---

#### 2. Recursos

##### 2.1 Construção

| Recurso | Regra |
|---|---|
| Seções | Agrupam perguntas. Cada seção tem título e descrição |
| Tipos de pergunta | Texto curto, texto longo, escolha única, múltipla escolha, escala (1 a N, com rótulos nas pontas), data, hora, número, arquivo (com limite de tipo e tamanho, ver [21](../../../docs/v2/21-busca-e-armazenamento.md)), nota (estrelas), matriz (linhas × colunas) |
| Obrigatoriedade | Por pergunta |
| Lógica condicional | Mostra ou oculta pergunta ou seção conforme resposta anterior. Só para perguntas de escolha e escala. Ciclo de dependência é recusado ao publicar |
| Pontuação | Opcional. Cada opção tem valor. O cálculo é do módulo consumidor, não do motor |
| Modelos | Modelos globais publicados pela plataforma (sem dado) e modelos de cada entidade |
| Cópia | Duplicar formulário gera nova versão em rascunho |
| Pré-visualização | Sempre disponível, sem gravar resposta |

##### 2.2 Publicação e convite

| Forma | Quem responde | Regra |
|---|---|---|
| Convite nominal | Pessoa convidada, com vínculo ativo | Token de uso único, com validade. Identifica quem respondeu |
| Link aberto da unidade | Qualquer pessoa com vínculo do público-alvo | Exige login do portal. Sem login, não responde |
| Convite a convidado externo | Pessoa sem vínculo | Só se a entidade habilitar externos (decidido em [40](../../../docs/v2/40-aulas-online-por-portal.md), seção 7). Token de uso único, anônimo por padrão |

Regra geral: link aberto sem login não existe. Quem responde sem vínculo entra só por convite.

##### 2.3 Estados

`rascunho` → `publicado` → `encerrado` → `arquivado`. Formulário publicado não muda pergunta. Mudança exige nova versão. Respostas ficam ligadas à versão em que foram dadas.

`em_andamento` (prazo aberto) e `atrasado` (prazo vencido com convites sem resposta) são **calculados** a partir de data e de convites, sem coluna de estado ([18](../../../docs/v2/18-regras-modulos-2.md), T-04).

---

#### 3. Anonimato

Esta é a regra mais sensível do motor.

1. **Tabelas separadas.** `convites` guarda quem foi convidado e se respondeu (`respondido_em`). `respostas` guarda o conteúdo. Não há chave que une as duas em formulário anônimo.
2. **Token.** O convite tem token aleatório. Só o hash do token é gravado. O token não aparece em log.
3. **Sem metadado identificador.** Resposta anônima não grava IP, user agent nem `user_id`. O log de acesso registra só o evento de "resposta recebida", sem vínculo com a pessoa.
4. **Mínimo de respostas por grupo.** Relatório por grupo (turma, unidade, tópico) só aparece com **no mínimo 2 respostas** no grupo. Decidido pelo autor em 03/11/2026. Abaixo disso, o grupo é agregado com o grupo de nível superior ou fica oculto.
5. **Comentário livre.** Campo de texto livre em formulário anônimo é exibido só em lista sem vínculo com grupo pequeno. Antes de exibir, o sistema procura nomes próprios e números de telefone e mascara, com revisão humana antes de publicar o relatório.

**Atende:** LAC-16 em [19](../../../docs/v2/19-regras-modulos-3.md), seção 11 (anonimato na avaliação de preceptor).

---

#### 4. Dado sensível

Formulário pode coletar dado sensível (religião, saúde, orientação, origem étnica, filiação sindical). Regras:

- O formulário declara a categoria sensível **antes** de publicar. Sem a declaração, o campo não aceita tipo sensível.
- Coleta de dado sensível exige base legal: consentimento específico, registrado, ou outra base indicada pelo jurídico ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md)).
- Resposta com dado sensível tem acesso restrito ao papel que criou o formulário. Gestão vê só o agregado, nunca a resposta individual, salvo regra do módulo consumidor.
- Exportação de resposta com dado sensível gera evento de auditoria com motivo.
- Dado sensível não aparece em payload de evento ([14](../../../docs/v2/14-integracao-modulos.md), seção 8).

---

#### 5. Relatórios

| Relatório | Regra |
|---|---|
| Resumo por pergunta | Contagem e percentual. Escala com média. Gráfico de barras para escolha, linha para série temporal |
| Cruzamento por grupo | Só acima do mínimo da seção 3 |
| Comparação entre versões | Compara a mesma pergunta em versões diferentes, com aviso de mudança de texto |
| Exportação | CSV e PDF. Mesma regra de anonimato. Gera evento de auditoria |
| Painel | Taxa de resposta, atrasos e convites pendentes. Sem conteúdo |

---

#### 6. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos globais, sem resposta. Ver uso agregado do motor | Ver resposta de qualquer entidade | P |
| **Gestão** | Criar, publicar, convidar, encerrar, ver relatório agregado, exportar com auditoria | Ver resposta nominal de formulário anônimo. Ver resposta de dado sensível sem papel do módulo de origem | E |
| **Professor** | Criar pesquisa para a própria turma (ex.: satisfação com a disciplina). Ver relatório da turma acima do mínimo | Pesquisa sobre colega ou ver resposta de outra turma | E |
| **Aluno** | Responder o que foi convidado. Ver a própria resposta enquanto o formulário não encerrar, quando não for anônimo | Ver resposta de colegas. Responder duas vezes em formulário de resposta única | E |
| **Responsáveis** | Responder pesquisa de família e avaliação de atendimento, por convite | Responder em nome de dependente maior de idade. Ver resposta de outra família | E |
| **Terceiros** | Nada, por padrão. Fornecedor só responde se o contrato prever pesquisa de avaliação de serviço | Ver resposta de qualquer outra pessoa | E, [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md) |
| **Convidado externo** | Responder com convite de uso único | Ver qualquer relatório | Fora dos seis portais, pela regra de [40](../../../docs/v2/40-aulas-online-por-portal.md) |

---

#### 7. Modelo de dados proposto

Tabelas no banco da unidade. Horários em UTC. `utf8mb4`.

```sql
CREATE TABLE formularios (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  modulo_origem   VARCHAR(40) NOT NULL,        -- preceptoria, rh, pastoral, atendimento, ...
  titulo          VARCHAR(200) NOT NULL,
  unidade_uuid    CHAR(36) NOT NULL,
  anonimo         TINYINT(1) NOT NULL DEFAULT 0,
  categoria_sensivel TINYINT(1) NOT NULL DEFAULT 0,
  resposta_unica  TINYINT(1) NOT NULL DEFAULT 1,
  estado          ENUM('rascunho','publicado','encerrado','arquivado') NOT NULL,
  versao          INT UNSIGNED NOT NULL DEFAULT 1,
  abre_em         DATETIME(3) NULL,
  fecha_em        DATETIME(3) NULL,
  created_by      CHAR(36) NOT NULL,
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at      DATETIME(3) NULL,
  INDEX ix_form_unidade (unidade_uuid, estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE formulario_perguntas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  formulario_id   BIGINT UNSIGNED NOT NULL,
  versao          INT UNSIGNED NOT NULL,
  secao           VARCHAR(120) NULL,
  ordem           INT UNSIGNED NOT NULL,
  tipo            ENUM('texto_curto','texto_longo','escolha_unica','multipla','escala','data','hora','numero','arquivo','nota','matriz') NOT NULL,
  enunciado       TEXT NOT NULL,
  obrigatoria     TINYINT(1) NOT NULL DEFAULT 0,
  condicao        JSON NULL,                   -- {"pergunta_id": n, "valor": "..."}
  sensivel        TINYINT(1) NOT NULL DEFAULT 0,
  UNIQUE KEY ux_pergunta_ordem (formulario_id, versao, ordem),
  CONSTRAINT fk_pergunta_form FOREIGN KEY (formulario_id) REFERENCES formularios (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE formulario_convites (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  formulario_id   BIGINT UNSIGNED NOT NULL,
  token_hash      CHAR(64) NOT NULL UNIQUE,    -- SHA-256 do token. Nunca o token
  destinatario_uuid CHAR(36) NULL,             -- NULL em formulário anônimo
  expira_em       DATETIME(3) NOT NULL,
  respondido_em   DATETIME(3) NULL,
  CONSTRAINT fk_convite_form FOREIGN KEY (formulario_id) REFERENCES formularios (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE formulario_respostas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  formulario_id   BIGINT UNSIGNED NOT NULL,
  versao          INT UNSIGNED NOT NULL,
  respondido_em   DATETIME(3) NOT NULL,
  respondente_uuid CHAR(36) NULL,              -- NULL em formulário anônimo
  respostas       JSON NOT NULL,               -- {"pergunta_uuid": valor}
  CONSTRAINT fk_resposta_form FOREIGN KEY (formulario_id) REFERENCES formularios (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Regras do modelo:**

- Em formulário anônimo, `destinatario_uuid` e `respondente_uuid` ficam `NULL`. Não é preenchimento omitido, é regra. Teste de banco garante isso.
- Resposta é imutável. Correção gera nova resposta com motivo, e a anterior fica marcada como `substituida`. Essa coluna não está no DDL acima e entra na próxima revisão do modelo.
- `respostas` em JSON tem validação de schema contra a versão do formulário na gravação ([15](../../../docs/v2/15-validacoes.md), seção 4).

---

#### 8. Integração

| Consumidor | Uso | Dono do dado |
|---|---|---|
| Preceptoria ([42](../../../docs/v2/42-preceptoria-por-portal.md)) | Autoavaliação, avaliação do preceptor, comparação | Preceptoria |
| RH ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md)) | Questionário de saída, clima, avaliação de desempenho | RH |
| Pastoral ([43](../../../docs/v2/43-pastoral-por-portal.md)) | Inscrição em encontro, pesquisa de ação social | Pastoral |
| Atendimento ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md)) | CSAT ao fechar protocolo | Atendimento |
| CRM ([22](../../../docs/v2/22-crm-canais-e-papeis.md)) | Captura de lead. Regras de origem e aceite continuam de 22 | CRM |

Formulário não envia resposta a módulo consumidor. O consumidor lê a resposta por contrato, com permissão do próprio módulo.

---

#### 9. Pendências

| # | Pendência | Tipo |
|---|---|---|
| FRM-01 | Mínimo de respostas por grupo para relatório: 2 | **Decidido** em 03/11/2026 |
| FRM-02 | Revisão humana de comentário livre antes de exibir (seção 3, item 5) | **Decidido** em 03/11/2026: sempre revisado por pessoa. Parecer de (jurídico) pendente |
| FRM-03 | Base legal para coleta de dado sensível em formulário (seção 4) | (jurídico) |
| FRM-04 | Modelos globais iniciais: quem aprova | **Decidido** em 03/11/2026: a equipe da empresa desenvolvedora aprova antes de publicar |
| FRM-05 | Coluna `substituida` e demais detalhes do DDL (seção 7) | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 5. Revisão do owner pendente (DDL-01) |
| FRM-06 | Prazo de guarda de resposta de formulário, por tipo | (jurídico) |

---

#### 10. Critérios de aceite

- [ ] Formulário anônimo não grava `respondente_uuid` nem `destinatario_uuid` (teste de banco).
- [ ] Token de convite gravado só como hash (teste).
- [ ] Relatório de grupo abaixo do mínimo não aparece (teste).
- [ ] Formulário com dado sensível não publica sem a declaração de categoria (teste).
- [ ] Link aberto sem login não responde (teste).
- [ ] Resposta publicada não muda de versão (teste).
- [ ] Ciclo de condição é recusado ao publicar (teste).
- [ ] Itens **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).
