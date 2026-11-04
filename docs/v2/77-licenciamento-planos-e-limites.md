# 77 — Licenciamento, planos, assinaturas e limites

> Parte do [SDD v2](00-README.md). Complementa [16](16-integracoes-externas.md) (cobrança da assinatura do SaaS) e [20](20-pagamentos-seguranca.md) (pagamentos). Permissões em [78](78-permissoes-e-papeis.md).
> **Status:** proposta do autor em 03/11/2026, para aprovação. Itens marcados **[Proposta]** entram no SDD quando aprovados.

---

## 1. Regras aprovadas pelo autor

| # | Regra | Origem |
|---|---|---|
| L-01 | Cada plano tem um **limite de alunos**, definido pelo desenvolvedor da plataforma. | Autor, 03/11/2026 |
| L-02 | Criar entidade e criar unidade é **exclusivo do papel de desenvolvedor** (`platform.developer`). Nenhum outro papel cria entidade ou unidade. | Autor, 03/11/2026 |

## 2. Modelo de plano

| Campo | Regra | Situação |
|---|---|---|
| Nome e código | Únicos na plataforma. | [Proposta] |
| Limite de alunos | Número inteiro, definido pelo desenvolvedor. Contabiliza **alunos com matrícula ativa** em qualquer unidade da entidade. | L-01 (aprovada) |
| Módulos incluídos | Lista de módulos licenciados para o plano. Entidade sem o módulo não vê o item no portal. | [Proposta] (ver [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 1) |
| Ciclo de cobrança | Mensal ou anual. | [Proposta] |
| Preço | Definido pelo desenvolvedor, em moeda única da plataforma. | [Proposta] |
| Situação | Ativo, descontinuado. Plano descontinuado não aceita novas assinaturas, e as existentes seguem até a renovação. | [Proposta] |

## 3. Assinatura da entidade

- Uma entidade tem **uma assinatura ativa** por vez, vinculada a um plano.
- Mudança de plano: efeito na data definida pelo desenvolvedor. Aumento de limite pode ser imediato; redução só vale na renovação, sem remover alunos já matriculados.
- Cobrança de assinatura: integrada ao provedor de pagamento, sem dado bancário no sistema ([16](16-integracoes-externas.md), seção 2.1).

### 3.1 Situações da assinatura [Proposta]

| Situação | Quando | Efeito |
|---|---|---|
| `ativa` | Pagamento em dia | Operação normal |
| `inadimplente` | Renovação não paga após o vencimento | Acesso de leitura por período de carência; novas matrículas bloqueadas |
| `suspensa` | Fim da carência sem pagamento, ou pedido do desenvolvedor | Somente leitura, como em [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 5 |
| `cancelada` | Cancelamento solicitado ou fim do processo de saída | Início do fluxo de saída de cliente |

Prazo de carência: **[Proposta] 15 dias**, a definir pelo desenvolvedor por plano.

## 4. Limite de alunos (L-01)

- **Contagem:** alunos com matrícula ativa, somados em todas as unidades da entidade. Matrícula cancelada, trancada ou concluída não conta.
- **Verificação:** a cada nova matrícula ativa e, em lote, uma vez por dia para conferência.
- **Ao atingir 90%:** aviso aos administradores da entidade e ao desenvolvedor.
- **Ao exceder o limite:** **[Proposta] bloqueio de novas matrículas ativas** até que o plano seja ampliado ou o número de alunos caia. Dados existentes não são alterados nem bloqueados.
- **Alternativa:** permitir o excedente por período de tolerância, com cobrança adicional. Não adotada no SDD sem decisão do autor.

## 5. Decisões pendentes

| # | Decisão | Proposta | Alternativa |
|---|---|---|---|
| D-27 | Comportamento ao exceder o limite de alunos | Bloquear novas matrículas ativas (seção 4) | Tolerância com cobrança adicional |
| D-28 | Prazo de carência por inadimplência | 15 dias, por plano | Prazo único para todos os planos |
| D-29 | Preço e ciclo por plano | Definidos pelo desenvolvedor, por plano | Preço único da plataforma |

## 6. Critérios de aceite

- [ ] Plano com limite de alunos obrigatório, definido pelo desenvolvedor.
- [ ] Contagem de alunos com matrícula ativa, somada por entidade, verificada na matrícula e em lote.
- [ ] Aviso a 90% e bloqueio de novas matrículas acima do limite (após D-27 aprovada).
- [ ] Mudança de plano com efeito na data definida, sem remover alunos.
- [ ] Situações da assinatura refletidas na navegação e nas ações (após D-28).
- [ ] Nenhum dado bancário no sistema (ver [16](16-integracoes-externas.md)).
