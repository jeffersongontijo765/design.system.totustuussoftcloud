# Campos personalizados

- Portal: Gestão (`gestao.`)
- Área: Configuração e acesso
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [72](../../../docs/v2/72-campos-personalizados-por-portal.md) (integral)
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Definir campos personalizados por entidade nos cadastros permitidos.

## 3. Telas

- **Campos** (lista por cadastro).
- **Campo — formulário** (tipo, obrigatoriedade, validação, visibilidade por portal).

## 4. Permissões por portal (extraídas do SDD)

Do [72](../../../docs/v2/72-campos-personalizados-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Criar e inativar campos de entidade e de unidade. Definir visibilidade | Ver campo sensível de aluno sem o papel próprio | E |
| **Coordenação** | Editar valor de aluno da unidade, nos campos que permitir | Criar campo de unidade ou de entidade. Ver campo sensível | E |
| **Secretaria** | Preencher valor de campo comum e pessoal da unidade | Criar ou inativar campo. Ver campo sensível | E |

## 5. Papéis

- `entity.admin`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- [72](../../../docs/v2/72-campos-personalizados-por-portal.md).

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

### 13.1 [72 — Campos Personalizados, por Portal](../../../docs/v2/72-campos-personalizados-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Decisão CFG-06 em [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 8: campos personalizados entram no escopo, definidos por entidade ou por unidade. Cada unidade tem seu próprio banco de dados ([03](../../../docs/v2/03-dominio-tenancy.md), seção 1.1), por isso os valores ficam no banco da unidade. Minimização de dado em [07](../../../docs/v2/07-privacidade-lgpd.md). Dado sensível e campos bloqueados em [18](../../../docs/v2/18-regras-modulos-2.md), seção 3.3, e [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md). Campos usados em relatórios em [69](../../../docs/v2/69-relatorios-e-censo-por-portal.md). Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Não há especificação anterior. Itens **[Decisão do autor]** indicam o que ainda depende de resposta.

---

#### 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Campos personalizados entram? | **Sim**, por decisão de CFG-06 |
| Quem define? | Entidade, para todas as unidades. Ou unidade, para si mesma |
| Onde ficam os valores? | No banco da unidade. A definição da entidade é copiada para cada unidade |
| Podem mudar campo fixo? | **Não.** Só acrescentam informação |

---

#### 2. Definição

Um campo personalizado tem:

| Atributo | Regra |
|---|---|
| Nome e chave | Nome visível e chave interna estável, que não muda |
| Objeto | A que cadastro pertence (seção 3) |
| Tipo | Texto curto, texto longo, número, data, lista de valores, sim ou não |
| Obrigatório | Sim ou não. Obrigatório só em criação, para não travar cadastro antigo |
| Validação | Tamanho, faixa, formato ou lista. Regra da própria definição |
| Escopo | `entidade` (vale para todas as unidades) ou `unidade` (vale só para a unidade) |
| Visibilidade | Quais portais veem e quais editam (seção 6) |
| Classificação | Comum, pessoal, sensível. Define regras de acesso e de relatório |
| Estado | `ativo`, `inativo`. Inativo não aparece em tela nova, mas o valor fica |

---

#### 3. Onde cabe

Campo personalizado só vale para objetos listados aqui. Os objetos são:

| Objeto | Pode ter campo personalizado |
|---|---|
| Aluno | Sim, com classificação |
| Responsável | Sim, com classificação |
| Turma | Sim |
| Disciplina | Sim |
| Recurso (sala, equipamento) | Sim |
| Fornecedor | Sim |
| Contrato | Sim |
| Documento modelo | Não. Modelo tem campo próprio de [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md) |
| Dado de saúde, prontuário e ocorrência | **Não.** Esses têm estrutura fixa, com regra de [63](../../../docs/v2/63-ocorrencias-disciplinares-por-portal.md) e [66](../../../docs/v2/66-prontuario-e-portfolio-do-aluno-por-portal.md) |

Lista de objetos que podem ter campo: decidido em 03/11/2026 (CPF-01), como na tabela acima.

---

#### 4. Regras

- **Só acrescenta.** Campo personalizado não substitui campo fixo, não muda chave, não altera regra de cálculo.
- **Dado pessoal exige classificação.** Campo `pessoal` ou `sensivel` não aparece em relatório comum nem em busca por texto ([21](../../../docs/v2/21-busca-e-armazenamento.md)).
- **Campo sensível não é de texto livre.** Dado de saúde, religião e orientação só entra por campo com tipo e regra próprios, e com consentimento quando houver ([41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 3).
- **Valor fica no banco da unidade.** O cadastro da entidade guarda só a definição. A unidade grava o valor junto ao registro.
- **Mudança de definição é auditada.** Criar, alterar, inativar e remover valor geram evento ([29](../../../docs/v2/29-auditoria.md)).
- **Remoção de definição não apaga valor.** Só inativa. Apagar o valor exige o mesmo prazo de guarda do dado (seção 7).

---

#### 5. Relatórios e busca

- Campo personalizado entra em relatório só se o relatório o declarar, e só se a classificação permitir ([69](../../../docs/v2/69-relatorios-e-censo-por-portal.md), seção 2.4).
- Busca só indexa campo `comum`. Pessoal e sensível ficam fora do índice ([21](../../../docs/v2/21-busca-e-armazenamento.md)).
- Campo não entra no censo, nas declarações oficiais nem nos formatos regulatórios. Esses têm campos fixos.

---

#### 6. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelo de campos padrão, sem dado | Criar campo de entidade. Ver valor | P |
| **Gestão** | Criar e inativar campos de entidade e de unidade. Definir visibilidade | Ver campo sensível de aluno sem o papel próprio | E |
| **Coordenação** | Editar valor de aluno da unidade, nos campos que permitir | Criar campo de unidade ou de entidade. Ver campo sensível | E |
| **Secretaria** | Preencher valor de campo comum e pessoal da unidade | Criar ou inativar campo. Ver campo sensível | E |
| **Professor** | Preencher campo de turma e disciplina, quando a gestão permitir | Ver campo pessoal ou sensível de aluno | E |
| **Aluno** | Preencher campo próprio, quando o campo permitir | Ver campo de colega | E |
| **Responsáveis** | Preencher e ver campo do dependente, quando o campo permitir | Ver campo sensível que não lhe caiba | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer campo | E |

---

#### 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| CPF-01 | Objetos que podem ter campo personalizado (seção 3) | **Decidido** em 03/11/2026: os da proposta. Saúde, prontuário e ocorrência ficam de fora |
| CPF-02 | Quem pode criar campo de unidade (seção 6) | **Decidido** em 03/11/2026: só a gestão |
| CPF-03 | Prazo de guarda de valor de campo removido (seção 4) | (jurídico) |
| CPF-04 | DDL: definição, opção de lista, valor por registro e evento de mudança | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.17. Revisão do owner pendente (DDL-01) |

---

#### 8. Critérios de aceite

- [ ] Campo personalizado não substitui campo fixo (teste).
- [ ] Campo pessoal ou sensível não aparece em relatório comum nem na busca (teste de integração com [69](../../../docs/v2/69-relatorios-e-censo-por-portal.md) e [21](../../../docs/v2/21-busca-e-armazenamento.md)).
- [ ] Remover definição não apaga valor (teste).
- [ ] Valor de campo de unidade não sai do banco da unidade (teste de isolamento).
- [ ] Professor não vê campo pessoal ou sensível de aluno (teste de isolamento).
- [ ] Mudança de definição gera evento de auditoria (teste).
- [ ] Itens **[Decisão do autor]** e **(jurídico)** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).
