# Contratos de pessoal

- Portal: Gestão (`gestao.`)
- Área: Contratos
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [33](../../../docs/v2/33-contratos-por-portal.md), seção 2; [33](../../../docs/v2/33-contratos-por-portal.md), seção 3
- Fonte da v1: absorvida integralmente em [contratos-de-fornecedor.md](contratos-de-fornecedor.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Contratos de trabalho e aditivos dos colaboradores.

## 3. Telas

- **Contratos de pessoal** (DataTable).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `unit.hr` e `unit.legal`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Tipos de contrato e dono ([33](../../../docs/v2/33-contratos-por-portal.md), seção 2).

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

### 13.1 [33](../../../docs/v2/33-contratos-por-portal.md), seção 2

#### 2. Tipos de contrato e a quem pertencem

A v1 lista 13 tipos (seção 2.1). Eles não têm o mesmo dono. Cada um fica em um portal, com parte e papel definidos:

| Tipo | Parte A | Parte B | Dono | Portal de acesso |
|---|---|---|---|---|
| Contrato de cliente (SaaS) | Plataforma | Entidade | Plataforma | Desenvolvedor |
| Contrato de prestação de serviços educacionais (matrícula) | Entidade | Responsável legal e aluno | Entidade | Gestão; assinatura pelo Responsáveis |
| Contrato de trabalho e termos de pessoal | Entidade | Colaborador | Entidade (RH) | Gestão; ciência pelo Professor |
| Contrato de fornecedor e de serviço | Entidade | Fornecedor | Entidade (Compras) | Gestão; ciência pelo Terceiros |
| Contrato de manutenção, locação e parceria | Entidade | Fornecedor ou parceiro | Entidade | Gestão; ciência pelo Terceiros |
| Convênio e contrato institucional | Entidade | Órgão ou instituição | Entidade (Jurídico) | Gestão |
| Acordo de confidencialidade (NDA) | Plataforma ou entidade | Parte externa | Quem assina | Desenvolvedor ou Gestão |
| Acordo de processamento de dados (DPA) | Entidade ou plataforma | Operador | Jurídico | Gestão ou Desenvolvedor; ciência pelo Terceiros |
| Termo aditivo, distrato, renovação | Mesmas partes do contrato original | — | Dono do contrato original | Mesmo portal do original |
| Contrato guarda-chuva (master agreement) | Entidade | Fornecedor | Entidade (Compras) | Gestão |

**Regra:** o portal de origem é o do contrato original. Aditivo e distrato não mudam de portal.

**Pendência:** o contrato de matrícula (aluno ou responsável) e o contrato de cliente são contratos de consumo ou de prestação civil. A forma e as cláusulas dependem de **(jurídico)** ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 4). Não defino cláusula aqui.

### 13.2 [33](../../../docs/v2/33-contratos-por-portal.md), seção 3

#### 3. Ciclo de vida

Etapas da v1 (seção 2.2), com donos:

| Etapa | Dono | Saída |
|---|---|---|
| Solicitação | Quem precisa do contrato | Solicitação contratual |
| Triagem | Gestor de contratos | Aceita, devolvida ou recusada |
| Minuta | Gestor de contratos, com modelo | Minuta versionada |
| Revisão interna | Jurídico | Parecer |
| Negociação externa | Gestor de contratos | Versão negociada |
| Aprovação jurídica | Jurídico | Aprovado ou devolvido |
| Aprovação financeira | Financeiro | Aprovado ou devolvido, conforme faixa |
| Aprovação gestora | Gestor | Aprovado |
| Assinatura | Responsável pelo contrato | Assinado |
| Vigência | Sistema | Alerta de vencimento |
| Monitoramento de obrigações | Responsável pela obrigação | Entregas e SLA |
| Reajuste e renovação | Gestor de contratos, com financeiro | Aditivo |
| Encerramento e arquivamento | Gestor de contratos | Estado final |

**Estados do contrato** (já em [17](../../../docs/v2/17-regras-modulos.md), seção 7.3): `negociacao`, `aprovacao`, `assinado`, `vigente`, `em_renovacao`, `encerrado`, `cancelado`.

**Regras de transição:**

- Contrato `assinado` não é editado. Mudança vira aditivo ([17](../../../docs/v2/17-regras-modulos.md)).
- Ausência de cláusula obrigatória bloqueia envio para assinatura ([17](../../../docs/v2/17-regras-modulos.md), seção 7.2).
- Aprovação jurídica é obrigatória por tipo ([17](../../../docs/v2/17-regras-modulos.md)).
- Quem cria a minuta não aprova a própria minuta (segregação, [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5).
