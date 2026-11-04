# Obrigações

- Portal: Gestão (`gestao.`)
- Área: Contábil e fiscal da entidade
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 1; [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 11
- Fonte da v1: absorvida integralmente em [plano-de-contas-da-entidade.md](plano-de-contas-da-entidade.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Calendário e entrega das obrigações acessórias da entidade.

## 3. Telas

- **Calendário de obrigações** (lista com prazos e responsável).
- **Entregas** (comprovantes).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `unit.fiscal` e `unit.accounting`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Mapa de obrigações ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 1).

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

### 13.1 [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 1

#### 1. Mapa de obrigações

| Área | Norma principal | Confiança | Controle no SDD | Documento |
|---|---|---|---|---|
| Proteção de dados pessoais | LGPD (Lei 13.709/2018) | [A] | Bases legais, direitos, incidentes, RIPD | [07](../../../docs/v2/07-privacidade-lgpd.md), [21](../../../docs/v2/21-busca-e-armazenamento.md), [25](../../../docs/v2/25-dossie-juridico-e-lacunas.md) |
| Dados de crianças e adolescentes | LGPD, art. 14; ECA | [A] para art. 14; [V] demais | Consentimento de responsável, minimização | [07](../../../docs/v2/07-privacidade-lgpd.md), seção 1 |
| Registro de acesso a aplicações | Marco Civil da Internet (Lei 12.965/2014), art. 15 | [A] para existência; [V] para o prazo | Registro de acesso separado | [21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6.8 |
| Relação de consumo (mensalidade, serviços) | CDC (Lei 8.078/1990) | [A] | Contrato, cobrança, multa, arrependimento | Este documento, seções 4 e 5 |
| Superendividamento | Lei 14.181/2021 | [A] para existência; [V] para aplicação à régua | Régua com análise de renegociação | [18](../../../docs/v2/18-regras-modulos-2.md), seção 2.6 |
| Anuidades e mensalidades escolares | Lei 9.870/1999 | [V] | Limites de reajuste, multa e juros | Este documento, seção 4 |
| Educação (matrícula, documentos) | LDB (Lei 9.394/1996) e normas do sistema de ensino | [V] | Guarda de registros escolares | Este documento, seção 6 |
| Trabalho e saúde ocupacional | CLT; NRs (NR-1, NR-7 e outras); eSocial | [V] | PCMSO, ASO, CAT, EPI | [17](../../../docs/v2/17-regras-modulos.md), seção 5 |
| Fiscal | LC 116/2003 (ISS); normas municipais; CTN | [A] para ISS; [V] para prazos | NFSe, retenção fiscal | [18](../../../docs/v2/18-regras-modulos-2.md), seção 2.7 |
| Pagamentos | Lei 12.865/2013; normas do Banco Central | [A] para a lei; [V] para as resoluções | Modelo de recebimento | [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 2 |
| Assinatura e contratos eletrônicos | MP 2.200-2/2001; Lei 14.063/2020 | [A] | Assinatura por nível | Este documento, seção 7 |
| Incidentes de segurança | LGPD, art. 48; Resolução CD/ANPD 15/2024 | [A] para o art. 48; [V] para o prazo | Runbook e comunicação | [07](../../../docs/v2/07-privacidade-lgpd.md), seção 8 |
| Acessibilidade | Lei 13.146/2015 (Estatuto da Pessoa com Deficiência) | [A] para existência; [V] para o alcance em sites privados | WCAG 2.2 AA | [08](../../../docs/v2/08-frontend-design-system.md), [24](../../../docs/v2/24-operacao-continuidade-qualidade.md), seção 7 |
| Comunicação por canais | LGPD; regras de uso das plataformas de mensagem | [A] para LGPD; [V] para regras de plataforma | Consentimento por canal | [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 3 |

### 13.2 [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 11

#### 11. Fiscal

- Nota fiscal de serviço segue o ISS do município (LC 116/2003) [A]. Cada município tem integração própria ([16](../../../docs/v2/16-integracoes-externas.md), seção 3).
- Guarda de documentos fiscais: 5 anos (CTN, art. 195) [V].
- Cancelamento de nota segue as regras do município e registra o motivo.
