# 72 — Campos Personalizados, por Portal

> Parte do [SDD v2](00-README.md). Decisão CFG-06 em [56](56-configuracoes-e-relatorios-lacunas.md), seção 8: campos personalizados entram no escopo, definidos por entidade ou por unidade. Cada unidade tem seu próprio banco de dados ([03](03-dominio-tenancy.md), seção 1.1), por isso os valores ficam no banco da unidade. Minimização de dado em [07](07-privacidade-lgpd.md). Dado sensível e campos bloqueados em [18](18-regras-modulos-2.md), seção 3.3, e [38](38-portal-de-terceiros-prestadores.md). Campos usados em relatórios em [69](69-relatorios-e-censo-por-portal.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Não há especificação anterior. Itens **[Decisão do autor]** indicam o que ainda depende de resposta.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Campos personalizados entram? | **Sim**, por decisão de CFG-06 |
| Quem define? | Entidade, para todas as unidades. Ou unidade, para si mesma |
| Onde ficam os valores? | No banco da unidade. A definição da entidade é copiada para cada unidade |
| Podem mudar campo fixo? | **Não.** Só acrescentam informação |

---

## 2. Definição

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

## 3. Onde cabe

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
| Documento modelo | Não. Modelo tem campo próprio de [48](48-gerador-de-documentos-por-portal.md) |
| Dado de saúde, prontuário e ocorrência | **Não.** Esses têm estrutura fixa, com regra de [63](63-ocorrencias-disciplinares-por-portal.md) e [66](66-prontuario-e-portfolio-do-aluno-por-portal.md) |

Lista de objetos que podem ter campo: decidido em 03/11/2026 (CPF-01), como na tabela acima.

---

## 4. Regras

- **Só acrescenta.** Campo personalizado não substitui campo fixo, não muda chave, não altera regra de cálculo.
- **Dado pessoal exige classificação.** Campo `pessoal` ou `sensivel` não aparece em relatório comum nem em busca por texto ([21](21-busca-e-armazenamento.md)).
- **Campo sensível não é de texto livre.** Dado de saúde, religião e orientação só entra por campo com tipo e regra próprios, e com consentimento quando houver ([41](41-formularios-e-pesquisas.md), seção 3).
- **Valor fica no banco da unidade.** O cadastro da entidade guarda só a definição. A unidade grava o valor junto ao registro.
- **Mudança de definição é auditada.** Criar, alterar, inativar e remover valor geram evento ([29](29-auditoria.md)).
- **Remoção de definição não apaga valor.** Só inativa. Apagar o valor exige o mesmo prazo de guarda do dado (seção 7).

---

## 5. Relatórios e busca

- Campo personalizado entra em relatório só se o relatório o declarar, e só se a classificação permitir ([69](69-relatorios-e-censo-por-portal.md), seção 2.4).
- Busca só indexa campo `comum`. Pessoal e sensível ficam fora do índice ([21](21-busca-e-armazenamento.md)).
- Campo não entra no censo, nas declarações oficiais nem nos formatos regulatórios. Esses têm campos fixos.

---

## 6. Por portal

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

## 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| CPF-01 | Objetos que podem ter campo personalizado (seção 3) | **Decidido** em 03/11/2026: os da proposta. Saúde, prontuário e ocorrência ficam de fora |
| CPF-02 | Quem pode criar campo de unidade (seção 6) | **Decidido** em 03/11/2026: só a gestão |
| CPF-03 | Prazo de guarda de valor de campo removido (seção 4) | (jurídico) |
| CPF-04 | DDL: definição, opção de lista, valor por registro e evento de mudança | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.17. Revisão do owner pendente (DDL-01) |

---

## 8. Critérios de aceite

- [ ] Campo personalizado não substitui campo fixo (teste).
- [ ] Campo pessoal ou sensível não aparece em relatório comum nem na busca (teste de integração com [69](69-relatorios-e-censo-por-portal.md) e [21](21-busca-e-armazenamento.md)).
- [ ] Remover definição não apaga valor (teste).
- [ ] Valor de campo de unidade não sai do banco da unidade (teste de isolamento).
- [ ] Professor não vê campo pessoal ou sensível de aluno (teste de isolamento).
- [ ] Mudança de definição gera evento de auditoria (teste).
- [ ] Itens **[Decisão do autor]** e **(jurídico)** respondidos ou marcados como pendentes no [00](00-README.md).
