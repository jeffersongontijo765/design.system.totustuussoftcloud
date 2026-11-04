# Unidades

- Portal: Gestão (`gestao.`)
- Área: Configuração e acesso
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 3; [03](../../../docs/v2/03-dominio-tenancy.md), seção 1; [03](../../../docs/v2/03-dominio-tenancy.md), seção 4; [03](../../../docs/v2/03-dominio-tenancy.md), seção 5; [77](../../../docs/v2/77-licenciamento-planos-e-limites.md) (integral)
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Editar os dados das unidades existentes da entidade (endereço, contatos, fuso, identidade visual, dados oficiais). **Criar entidade ou unidade é exclusivo de `platform.developer`** (L-02); a gestão pede nova unidade por chamado.

## 3. Telas

- **Unidades** (lista, sem botão de criar).
- **Unidade — edição** (dados cadastrais, oficiais, fuso, identidade visual).
- **Pedir nova unidade** (abre chamado ao suporte da plataforma).
- **Consumo do plano** (alunos ativos × limite do plano, L-01, só leitura).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `entity.admin`: editar unidades.
- `unit.manager`: editar a própria unidade.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- L-02 ([78](../../../docs/v2/78-permissoes-e-papeis.md), seção 3); limite de alunos do plano ([77](../../../docs/v2/77-licenciamento-planos-e-limites.md)).

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

### 13.1 [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 3

#### 3. Criação de entidade e unidade (L-02)

| Ação | Papel exigido | Verificação |
|---|---|---|
| Criar entidade | `platform.developer` | Passkey e sessão curta ([06](../../../docs/v2/06-identidade-acesso.md), seção 10) |
| Criar unidade | `platform.developer` | Idem |
| Editar dados de entidade ou unidade já criadas | Administrador da entidade (nível 4), exceto código e domínio, que são do desenvolvedor | Auditoria |
| Desativar ou encerrar entidade | `platform.developer`, por saída de cliente ([23](../../../docs/v2/23-dominios-provisionamento-ciclo-de-vida.md), seção 5) | Confirmação digitando o nome |

Nenhum outro papel, inclusive de plataforma, cria ou remove entidade ou unidade. A regra vale também para API ([04](../../../docs/v2/04-api.md)): o endpoint de criação exige o papel no servidor, não só na tela.

### 13.2 [03](../../../docs/v2/03-dominio-tenancy.md), seção 1

#### 1. Hierarquia

```
Plataforma (host)
 └─ Mantenedora (client)          — contratante do SaaS
     └─ Entidade (entity)         — instituição / razão social
         └─ Unidade (unit)        — campus, filial, polo
             └─ Usuários, papéis e vínculos
```

- A **plataforma** é um tenant reservado, identificado por código de seed. Seus administradores são **contas de plataforma** (ver [06](../../../docs/v2/06-identidade-acesso.md), seção 10), não usuários comuns com flag.
- Cada nível herda configuração do nível superior e pode sobrescrevê-la onde a política permitir.

### 13.3 [03](../../../docs/v2/03-dominio-tenancy.md), seção 4

#### 4. Escopo de unidade

- `UserUnit` limita o usuário a unidades específicas. Acesso `full` cobre todas as unidades da entidade.
- Permissões de unidade são avaliadas junto com a permissão de módulo. Permissão de módulo sem vínculo de unidade não basta para dados daquela unidade.

### 13.4 [03](../../../docs/v2/03-dominio-tenancy.md), seção 5

#### 5. Configuração por tenant

| Configuração | Escopo | Observação |
|---|---|---|
| Marca (logo, cores, nome) | Entidade | Validação de imagem (ver [05](../../../docs/v2/05-seguranca.md)) |
| Locale padrão e moeda | Entidade | Moeda USD/BRL é **[Declarado]**; outras moedas dependem de requisito |
| Política de senha e MFA | Mantenedora ou entidade | Não pode ser menos restritiva que a política da plataforma |
| Retenção de dados | Entidade | Mínimo e máximo definidos pela plataforma ([07](../../../docs/v2/07-privacidade-lgpd.md)) |
| Limites de API | Tenant | Ver [04](../../../docs/v2/04-api.md) |

### 13.5 [77 — Licenciamento, planos, assinaturas e limites](../../../docs/v2/77-licenciamento-planos-e-limites.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Complementa [16](../../../docs/v2/16-integracoes-externas.md) (cobrança da assinatura do SaaS) e [20](../../../docs/v2/20-pagamentos-seguranca.md) (pagamentos). Permissões em [78](../../../docs/v2/78-permissoes-e-papeis.md).
> **Status:** aprovado pelo autor em 04/11/2026 (L-01 e D-27 a D-29, D-34 a D-37). Não há proposta em aberto neste documento.

---

#### 1. Regras aprovadas pelo autor

| # | Regra | Origem |
|---|---|---|
| L-01 | Cada plano tem um **limite de alunos**, definido pelo desenvolvedor da plataforma. | Autor, 04/11/2026 |
| L-02 | Criar entidade e criar unidade é **exclusivo do papel de desenvolvedor** (`platform.developer`). Nenhum outro papel cria entidade ou unidade. | Autor, 04/11/2026 |

#### 2. Modelo de plano

| Campo | Regra | Situação |
|---|---|---|
| Nome e código | Únicos na plataforma. | D-34 (aprovada) |
| Limite de alunos | Número inteiro, definido pelo desenvolvedor. Contabiliza **alunos com matrícula ativa** em qualquer unidade da entidade. | L-01 (aprovada) |
| Módulos incluídos | Lista de módulos licenciados para o plano. Entidade sem o módulo não vê o item no portal. | D-35 (aprovada) (ver [23](../../../docs/v2/23-dominios-provisionamento-ciclo-de-vida.md), seção 1) |
| Ciclo de cobrança | Mensal ou anual, definido por plano. | D-29 (aprovada) |
| Preço | Definido pelo desenvolvedor, por plano, em moeda única da plataforma. | D-29 (aprovada) |
| Situação | Ativo, descontinuado. Plano descontinuado não aceita novas assinaturas, e as existentes seguem até a renovação. | D-36 (aprovada) |

#### 3. Assinatura da entidade

- Uma entidade tem **uma assinatura ativa** por vez, vinculada a um plano.
- Mudança de plano: efeito na data definida pelo desenvolvedor. Aumento de limite pode ser imediato; redução só vale na renovação, sem remover alunos já matriculados.
- Cobrança de assinatura: integrada ao provedor de pagamento, sem dado bancário no sistema ([16](../../../docs/v2/16-integracoes-externas.md), seção 2.1).

##### 3.1 Situações da assinatura (D-37, aprovada)

| Situação | Quando | Efeito |
|---|---|---|
| `ativa` | Pagamento em dia | Operação normal |
| `inadimplente` | Renovação não paga após o vencimento | Acesso de leitura por período de carência; novas matrículas bloqueadas |
| `suspensa` | Fim da carência sem pagamento, ou pedido do desenvolvedor | Somente leitura, como em [23](../../../docs/v2/23-dominios-provisionamento-ciclo-de-vida.md), seção 5 |
| `cancelada` | Cancelamento solicitado ou fim do processo de saída | Início do fluxo de saída de cliente |

Prazo de carência: **15 dias**, ajustável pelo desenvolvedor por plano (D-28, aprovada).

#### 4. Limite de alunos (L-01)

- **Contagem:** alunos com matrícula ativa, somados em todas as unidades da entidade. Matrícula cancelada, trancada ou concluída não conta.
- **Verificação:** a cada nova matrícula ativa e, em lote, uma vez por dia para conferência.
- **Ao atingir 90%:** aviso aos administradores da entidade e ao desenvolvedor.
- **Ao exceder o limite:** **bloqueio de novas matrículas ativas** (D-27, aprovada) até que o plano seja ampliado ou o número de alunos caia. Dados existentes não são alterados nem bloqueados.
- **Alternativa:** permitir o excedente por período de tolerância, com cobrança adicional. Descartada pela D-27.

#### 5. Decisões pendentes

| # | Decisão | Proposta | Alternativa |
|---|---|---|---|
| D-27 | Comportamento ao exceder o limite de alunos | Bloquear novas matrículas ativas (seção 4). **Aprovada pelo autor em 04/11/2026.** | Tolerância com cobrança adicional |
| D-28 | Prazo de carência por inadimplência | 15 dias, por plano. **Aprovada pelo autor em 04/11/2026.** | Prazo único para todos os planos |
| D-29 | Preço e ciclo por plano | Definidos pelo desenvolvedor, por plano. **Aprovada pelo autor em 04/11/2026.** | Preço único da plataforma |
| D-34 | Nome e código do plano | Únicos na plataforma (seção 2). **Aprovada pelo autor em 04/11/2026.** | Únicos por grupo de planos |
| D-35 | Módulos incluídos no plano | Lista de módulos por plano; entidade sem o módulo não vê o item no portal (seção 2). **Aprovada pelo autor em 04/11/2026.** | Todos os módulos em todos os planos, com limite só de alunos |
| D-36 | Situação do plano | Ativo ou descontinuado; descontinuado não aceita novas assinaturas (seção 2). **Aprovada pelo autor em 04/11/2026.** | Plano pode ser excluído |
| D-37 | Situações da assinatura | Ativa, inadimplente, suspensa, cancelada, com os efeitos da seção 3.1. **Aprovada pelo autor em 04/11/2026.** | Só ativa e cancelada |

#### 6. Critérios de aceite

- [ ] Plano com limite de alunos obrigatório, definido pelo desenvolvedor.
- [ ] Contagem de alunos com matrícula ativa, somada por entidade, verificada na matrícula e em lote.
- [ ] Aviso a 90% e bloqueio de novas matrículas acima do limite (D-27).
- [ ] Mudança de plano com efeito na data definida, sem remover alunos.
- [ ] Situações da assinatura refletidas na navegação e nas ações (D-28 e D-37).
- [ ] Nenhum dado bancário no sistema (ver [16](../../../docs/v2/16-integracoes-externas.md)).
