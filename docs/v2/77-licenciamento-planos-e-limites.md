# 77 — Licenciamento, planos, assinaturas e limites

> Parte do [SDD v2](00-README.md). Complementa [16](16-integracoes-externas.md) (cobrança da assinatura do SaaS) e [20](20-pagamentos-seguranca.md) (pagamentos). Permissões em [78](78-permissoes-e-papeis.md).
> **Status:** L-01 e D-27 a D-29 aprovadas pelo autor em 04/11/2026. Itens ainda marcados **[Proposta]** estão numerados de D-34 a D-37 (seção 5) e aguardam o autor.

---

## 1. Regras aprovadas pelo autor

| # | Regra | Origem |
|---|---|---|
| L-01 | Cada plano tem um **limite de alunos**, definido pelo desenvolvedor da plataforma. | Autor, 03/11/2026 |
| L-02 | Criar entidade e criar unidade é **exclusivo do papel de desenvolvedor** (`platform.developer`). Nenhum outro papel cria entidade ou unidade. | Autor, 03/11/2026 |

## 2. Modelo de plano

| Campo | Regra | Situação |
|---|---|---|
| Nome e código | Únicos na plataforma. | [Proposta] D-34 |
| Limite de alunos | Número inteiro, definido pelo desenvolvedor. Contabiliza **alunos com matrícula ativa** em qualquer unidade da entidade. | L-01 (aprovada) |
| Módulos incluídos | Lista de módulos licenciados para o plano. Entidade sem o módulo não vê o item no portal. | [Proposta] D-35 (ver [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 1) |
| Ciclo de cobrança | Mensal ou anual, definido por plano. | D-29 (aprovada) |
| Preço | Definido pelo desenvolvedor, por plano, em moeda única da plataforma. | D-29 (aprovada) |
| Situação | Ativo, descontinuado. Plano descontinuado não aceita novas assinaturas, e as existentes seguem até a renovação. | [Proposta] D-36 |

## 3. Assinatura da entidade

- Uma entidade tem **uma assinatura ativa** por vez, vinculada a um plano.
- Mudança de plano: efeito na data definida pelo desenvolvedor. Aumento de limite pode ser imediato; redução só vale na renovação, sem remover alunos já matriculados.
- Cobrança de assinatura: integrada ao provedor de pagamento, sem dado bancário no sistema ([16](16-integracoes-externas.md), seção 2.1).

### 3.1 Situações da assinatura [Proposta] D-37

| Situação | Quando | Efeito |
|---|---|---|
| `ativa` | Pagamento em dia | Operação normal |
| `inadimplente` | Renovação não paga após o vencimento | Acesso de leitura por período de carência; novas matrículas bloqueadas |
| `suspensa` | Fim da carência sem pagamento, ou pedido do desenvolvedor | Somente leitura, como em [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 5 |
| `cancelada` | Cancelamento solicitado ou fim do processo de saída | Início do fluxo de saída de cliente |

Prazo de carência: **15 dias**, ajustável pelo desenvolvedor por plano (D-28, aprovada).

## 4. Limite de alunos (L-01)

- **Contagem:** alunos com matrícula ativa, somados em todas as unidades da entidade. Matrícula cancelada, trancada ou concluída não conta.
- **Verificação:** a cada nova matrícula ativa e, em lote, uma vez por dia para conferência.
- **Ao atingir 90%:** aviso aos administradores da entidade e ao desenvolvedor.
- **Ao exceder o limite:** **bloqueio de novas matrículas ativas** (D-27, aprovada) até que o plano seja ampliado ou o número de alunos caia. Dados existentes não são alterados nem bloqueados.
- **Alternativa:** permitir o excedente por período de tolerância, com cobrança adicional. Descartada pela D-27.

## 5. Decisões pendentes

| # | Decisão | Proposta | Alternativa |
|---|---|---|---|
| D-27 | Comportamento ao exceder o limite de alunos | Bloquear novas matrículas ativas (seção 4). **Aprovada pelo autor em 04/11/2026.** | Tolerância com cobrança adicional |
| D-28 | Prazo de carência por inadimplência | 15 dias, por plano. **Aprovada pelo autor em 04/11/2026.** | Prazo único para todos os planos |
| D-29 | Preço e ciclo por plano | Definidos pelo desenvolvedor, por plano. **Aprovada pelo autor em 04/11/2026.** | Preço único da plataforma |
| D-34 | Nome e código do plano | Únicos na plataforma (seção 2) | Únicos por grupo de planos |
| D-35 | Módulos incluídos no plano | Lista de módulos por plano; entidade sem o módulo não vê o item no portal (seção 2) | Todos os módulos em todos os planos, com limite só de alunos |
| D-36 | Situação do plano | Ativo ou descontinuado; descontinuado não aceita novas assinaturas (seção 2) | Plano pode ser excluído |
| D-37 | Situações da assinatura | Ativa, inadimplente, suspensa, cancelada, com os efeitos da seção 3.1 | Só ativa e cancelada |

## 6. Critérios de aceite

- [ ] Plano com limite de alunos obrigatório, definido pelo desenvolvedor.
- [ ] Contagem de alunos com matrícula ativa, somada por entidade, verificada na matrícula e em lote.
- [ ] Aviso a 90% e bloqueio de novas matrículas acima do limite (D-27).
- [ ] Mudança de plano com efeito na data definida, sem remover alunos.
- [ ] Situações da assinatura refletidas na navegação e nas ações (D-28 e D-37).
- [ ] Nenhum dado bancário no sistema (ver [16](16-integracoes-externas.md)).
