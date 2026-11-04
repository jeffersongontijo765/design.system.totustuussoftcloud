# Empréstimos

- Portal: Gestão (`gestao.`)
- Área: Biblioteca
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [68](../../../docs/v2/68-biblioteca-por-portal.md), seção 4; [68](../../../docs/v2/68-biblioteca-por-portal.md), seção 5; [68](../../../docs/v2/68-biblioteca-por-portal.md), seção 10; [68](../../../docs/v2/68-biblioteca-por-portal.md), seção 11
- Fonte da v1: absorvida integralmente em [acervo.md](acervo.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Empréstimo, renovação e devolução de exemplares, inclusive entre unidades.

## 3. Telas

- **Balcão de circulação** (página: leitor, exemplar, empréstimo, devolução).
- **Empréstimos ativos e atrasados** (DataTable).
- **Empréstimo entre unidades** (fluxo).

## 4. Permissões por portal (extraídas do SDD)

Do [68](../../../docs/v2/68-biblioteca-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver indicadores e relatórios de circulação. Aprovar baixa e descarte | Emprestar, isentar multa ou editar acervo sem perfil de biblioteca | E |
| **Coordenação** | Ver relatórios de uso por curso e disciplina | Editar acervo ou empréstimo | E |

## 5. Papéis

- `unit.librarian`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Prazos por perfil ([68](../../../docs/v2/68-biblioteca-por-portal.md), seção 4); renovação bloqueada se houver reserva.

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

### 13.1 [68](../../../docs/v2/68-biblioteca-por-portal.md), seção 4

#### 4. Perfis e prazos

| Perfil | Empréstimos simultâneos | Prazo | Renovação |
|---|---|---|---|
| Aluno | 3 itens | 7 dias | Até 2 vezes, se não houver reserva de outro usuário |
| Professor | 5 itens | 30 dias | Mesma regra do aluno |
| Servidor | 5 itens | 30 dias | Mesma regra do aluno |

**Regra:** os valores da tabela são o ponto de partida de toda unidade nova. A escola altera por perfil e por categoria de item. **Decidido** em 03/11/2026 (BIB-04).

### 13.2 [68](../../../docs/v2/68-biblioteca-por-portal.md), seção 5

#### 5. Empréstimo, devolução e reserva

##### 5.1 Empréstimo

- Só com usuário com vínculo ativo: matrícula ativa para aluno, vínculo ativo para professor e servidor ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) e [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md)).
- Bloqueado com multa em aberto ou item atrasado.
- Retirada com busca por código de barras ou título. Confirmação de retirada pode ser assinada, se a escola exigir.

##### 5.2 Renovação

- Bloqueada se o item tiver reserva pendente de outro usuário.
- As renovações são contadas no empréstimo. Depois do limite, só devolução.

##### 5.3 Reserva

- Fila por item indisponível. Quando o exemplar volta, o próximo da fila é avisado ([57](../../../docs/v2/57-notificacoes-por-portal.md)).
- Reserva tem prazo de retirada. Expirado, passa ao próximo da fila.

##### 5.4 Devolução

- Devolução dentro da tolerância baixa a multa automaticamente.
- Exemplar devolvido em estado danificado vira `em_manutencao` até a avaliação do bibliotecário.

### 13.3 [68](../../../docs/v2/68-biblioteca-por-portal.md), seção 10

#### 10. Empréstimo entre unidades

- Unidades têm banco próprio ([03](../../../docs/v2/03-dominio-tenancy.md)). Empréstimo entre unidades exige transferência de registro, não consulta direta ao banco da outra unidade.
- **Decidido** em 03/11/2026 (BIB-01): o empréstimo é pedido pela unidade de destino e aprovado pela unidade de origem. Só o registro do exemplar e do usuário é transferido.

### 13.4 [68](../../../docs/v2/68-biblioteca-por-portal.md), seção 11

#### 11. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Ver métricas agregadas de uso, sem dado de acervo ou empréstimo | Ver acervo, empréstimo, multa ou histórico de leitura | P |
| **Gestão** | Ver indicadores e relatórios de circulação. Aprovar baixa e descarte | Emprestar, isentar multa ou editar acervo sem perfil de biblioteca | E |
| **Bibliotecário** (perfil da unidade) | Gerir acervo, empréstimo, multa, inventário, salas e biblioteca digital | Aprovar a própria isenção de multa | E |
| **Auxiliar de biblioteca** (perfil da unidade) | Emprestar e devolver. Lançar reserva | Gerir acervo. Isentar multa | E |
| **Coordenação** | Ver relatórios de uso por curso e disciplina | Editar acervo ou empréstimo | E |
| **Professor** | Consultar catálogo. Emprestar com prazo próprio. Reservar sala. Ver os próprios empréstimos | Ver empréstimo ou multa de outro usuário | E |
| **Aluno** | Consultar catálogo. Emprestar, reservar e renovar. Ver as próprias multas. Biblioteca digital | Ver empréstimo ou histórico de leitura de colega | E |
| **Responsáveis** | Ver empréstimos e multas do dependente, só leitura | Pagar, isentar ou ver título e histórico de leitura | E, só dependentes com vínculo ativo |
| **Responsável financeiro** (função dentro de responsáveis) | Ver valor e situação da multa do aluno sob sua responsabilidade, com link para quitar no financeiro | Ver título, categoria ou histórico | E |
| **Terceiros** | Nada por padrão. Acesso só por permissão explícita da entidade | Qualquer item sem permissão | E |
