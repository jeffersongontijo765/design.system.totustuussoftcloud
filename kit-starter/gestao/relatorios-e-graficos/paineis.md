# Painéis

- Portal: Gestão (`gestao.`)
- Área: Relatórios e gráficos
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.8; [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 3; [69](../../../docs/v2/69-relatorios-e-censo-por-portal.md), seção 2
- Fonte da v1: absorvida integralmente em [graficos-salvos.md](graficos-salvos.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Painéis da unidade com widgets e gráficos salvos.

## 3. Telas

- **Painéis** (lista e editor de grade).

## 4. Permissões por portal (extraídas do SDD)

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Teste de isolamento | Teste de permissão | Teste de fluxo principal | Teste de acessibilidade |
|---|---|---|---|---|
| Gestão | Cross-tenant e cross-unidade | Papel sem permissão não vê o módulo | Matrícula, cobrança, emissão de documento | Telas principais |

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Autenticação | Sessão | Dados e restrições especiais |
|---|---|---|---|
| Gestão | Senha e MFA conforme política da entidade ([06](../../../docs/v2/06-identidade-acesso.md), seção 5) | Padrão | Consulta por CPF com finalidade ([21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6.8) |

Do [69](../../../docs/v2/69-relatorios-e-censo-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver gerenciais de toda a entidade. Conferir o censo e aprovar o envio | Gerar operacional de aluno. Ver arquivo de regulatório antes do envio | E |
| **Coordenação** | Ver relatórios gerenciais e operacionais da unidade, no escopo de pedagógico | Enviar censo. Ver relatório financeiro | E |
| **Secretaria** | Gerar operacionais e regulatórios da unidade. Gerar e enviar censo, com conferência da gestão | Gerar financeiro. Enviar sem conferência | E |

## 5. Papéis

- Quem cria o painel e quem recebe compartilhamento; dados respeitam o escopo de quem vê.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Gráficos e painéis ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.8).

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

### 13.1 [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.8

##### 3.8 Gráficos e painéis

[`chart-builder-spec-complete.md`](../../../docs/v2/anexo-v1/chart-builder-spec-complete.md) (16 seções: consulta, renderização, painéis, API, segurança, exportação, tempo real) está marcado como "Especificado" no catálogo, mas a v2 não tem regra para ele.

**Proposta:**

- O construtor de gráfico é **componente compartilhado** ([08](../../../docs/v2/08-frontend-design-system.md)), não módulo de domínio.
- Cada gráfico salvo pertence a um portal e a um contexto (plataforma, entidade ou unidade). Nenhum gráfico mostra dado fora do escopo de quem o abriu.
- Consulta passa pela mesma camada de permissão das telas. A consulta não tem acesso direto ao banco.
- Gráfico de dado sensível (CPF, saúde, salário) não é exportável sem motivo e sem auditoria ([29](../../../docs/v2/29-auditoria.md)).
- Painel com dado pessoal entra no cache só com a regra de [30](../../../docs/v2/30-cache.md), seção 4.

### 13.2 [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 3

#### 3. Relatórios: regra geral que falta

Nenhum documento define como um relatório é gerado. Proposta, para ser validada:

1. **Relatório pertence ao módulo que tem o dado.** Não existe "relatório central". Cada módulo expõe os seus relatórios, com a mesma regra de acesso.
2. **Três tipos:** operacional (lista do dia), gerencial (totais e indicadores) e regulatório (formato exigido por órgão, como o censo e a ficha SEE).
3. **Permissão por escopo.** O relatório respeita o mesmo filtro de portal, unidade e turma que a tela. Relatório não é atalho para dado que a tela não mostra.
4. **Minimização.** Relatório com dado pessoal sai só com os campos necessários. Aniversariantes usa mês e dia, não a data completa de nascimento.
5. **Exportação é evento de auditoria** ([29](../../../docs/v2/29-auditoria.md)), com o campo `portal` e o filtro usado.
6. **Agregado com mínimo de grupo**, como em [41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 3, quando o relatório for sobre grupo pequeno.
7. **Senha e segredo nunca aparecem em relatório.** Exceção decidida pelo autor em 03/11/2026: a secretaria gera relatório com os dados de acesso do responsável (usuário e link de acesso). O relatório só pode ser enviado ao próprio responsável, nunca a aluno nem a terceiro, e segue a LGPD. **Decidido pelo autor em 03/11/2026:** a senha não aparece em texto. O relatório traz o usuário e um link de primeiro acesso, de uso único e com validade curta. O responsável cria a própria senha ao acessar.
8. **Foto em relatório** (carômetro) só com consentimento específico ([35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md), seção 6).

### 13.3 [69](../../../docs/v2/69-relatorios-e-censo-por-portal.md), seção 2

#### 2. Modelo comum

##### 2.1 Tipos

| Tipo | Uso | Exemplo |
|---|---|---|
| Operacional | Lista do dia ou do período | Lista de presença, aniversariantes, empréstimos em atraso |
| Gerencial | Totais e indicadores | Desempenho por disciplina, frequência por turma, inadimplência |
| Regulatório | Formato exigido por órgão | Censo escolar, ficha SEE, relatório SINAES |

##### 2.2 Ciclo

1. **Pedido.** O usuário escolhe o relatório e o filtro, dentro do próprio escopo ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), regra 3).
2. **Geração.** Abaixo do limite de linhas, a geração é imediata. Acima dele, é fila, com aviso quando pronta ([57](../../../docs/v2/57-notificacoes-por-portal.md)). Limite: REL-04.
3. **Arquivo.** O resultado é um arquivo com data, filtro, autor, hash e versão do layout.
4. **Download.** Só pelo autor do pedido, ou por quem tem o mesmo escopo, pelo período de validade.
5. **Expiração.** Arquivo expira e sai do armazenamento. O pedido e o filtro ficam no histórico.

##### 2.3 Formatos

| Formato | Uso |
|---|---|
| Tela | Padrão. Sem arquivo |
| PDF | Para imprimir ou arquivar. Com cabeçalho da unidade e data |
| CSV e planilha | Para análise. Sem formatação |
| Layout oficial | Só para regulatório, na forma exigida pelo órgão |

##### 2.4 Regras

- **Escopo da tela.** Relatório não mostra dado que a tela de origem não mostra ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), regra 3).
- **Minimização.** Só os campos necessários. Aniversariantes usa mês e dia ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), regra 4).
- **Grupo pequeno.** Indicador de grupo com menos de 2 pessoas não é mostrado, como em [41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 3.
- **Sem segredo.** Senha, token e link de uso único não aparecem em relatório. Ver [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), regra 7 e CFG-03.
- **Foto.** Relatório com foto só com consentimento específico ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), CFG-02).
- **Auditoria.** Geração e download geram evento com o portal, o filtro e o número de linhas ([29](../../../docs/v2/29-auditoria.md)).
- **Relatório programado.** O envio automático vai só para usuários com vínculo ativo na entidade. Não há envio a e-mail externo. **Decidido** em 03/11/2026 (REL-06).
