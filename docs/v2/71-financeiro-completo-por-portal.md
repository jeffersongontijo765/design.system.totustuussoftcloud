# 71 — Financeiro Completo, por Portal: Pagamentos, Cheques, Caixa, Fluxo, DRE e Conciliação

> Parte do [SDD v2](00-README.md). Decisão CFG-04 em [56](56-configuracoes-e-relatorios-lacunas.md), seção 8: escopo financeiro completo, com cheques, caixa, DRE e fluxo de caixa. Este documento fecha o que faltava. Já especificado em outros documentos e só referenciado aqui: títulos, parcelas e descontos em [18](18-regras-modulos-2.md); cobrança e gateway em [20](20-pagamentos-seguranca.md); NFS-e, split e nota de fornecedor em [34](34-pagamentos-fiscal-bancos-por-portal.md); contratos em [33](33-contratos-por-portal.md); regras de conciliação e aprovação em [17](17-regras-modulos.md), seção 2. Financeiro da própria empresa desenvolvedora em [31](31-matriz-portais-modulos.md). Orçamento e empenho em [37](37-planejamento-e-empenho.md). Relatórios financeiros em [69](69-relatorios-e-censo-por-portal.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna financeira de [56](56-configuracoes-e-relatorios-lacunas.md), seções 6 e 8. A v1 tem [`spec_gestao_financeiro_completo.md`](anexo-v1/spec_gestao_financeiro_completo.md) com contas a pagar, fluxo de caixa, conciliação, centros de custo, orçamentos, DRE e inadimplência. Esta versão corrige o que a v1 deixa solto: regime do DRE, cheques e caixa.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Receitas de alunos (títulos, parcelas, cobrança)? | **Coberto** em [18](18-regras-modulos-2.md) e [20](20-pagamentos-seguranca.md) |
| Contas a pagar? | **Parcial.** Aprovação e rateio na v1 e em [17](17-regras-modulos.md), seção 2.4. Falta regra de pagamento em lote |
| Cheques (recebidos e emitidos)? | **Não.** Só como forma de pagamento na v1 |
| Caixa (físico e fechamento)? | **Não.** Só como tipo de conta bancária na v1 |
| Fluxo de caixa e DRE? | **Parcial.** Tela e fórmula na v1. Falta regime, linha de DRE e fechamento |
| Conciliação? | **Coberto** em [17](17-regras-modulos.md), seção 2.5, e [20](20-pagamentos-seguranca.md), seção 12 |

---

## 2. Divisão de dono

| Assunto | Dono | Documento |
|---|---|---|
| Título, parcela, desconto, cobrança de aluno | Financeiro da entidade | [18](18-regras-modulos-2.md) |
| Gateway, ledger, webhook, Pix, boleto | Financeiro da entidade, com provedor | [20](20-pagamentos-seguranca.md) |
| Conta a pagar, fornecedor, rateio | Financeiro da entidade | Este documento, seção 4 |
| Cheque | Financeiro da entidade | Este documento, seção 5 |
| Caixa físico | Financeiro da entidade, operado na unidade | Este documento, seção 6 |
| Fluxo de caixa e DRE | Financeiro da entidade | Este documento, seções 7 e 8 |
| Conciliação | Financeiro da entidade | [17](17-regras-modulos.md), seção 2.5 |
| NFS-e, split, nota de fornecedor | Financeiro e fiscal | [34](34-pagamentos-fiscal-bancos-por-portal.md) |
| Financeiro da empresa desenvolvedora | Plataforma | [31](31-matriz-portais-modulos.md) |

---

## 3. Contas e movimentação

- **Conta** é o lugar onde o dinheiro está: conta corrente, poupança, gateway, carteira digital (como método do gateway, [34](34-pagamentos-fiscal-bancos-por-portal.md)) ou caixa físico.
- Cada movimentação tem conta, data, valor, categoria financeira, centro de custo, origem e estado.
- Estados de movimentação: `previsto`, `lancado`, `conciliado`, `estornado`. Não há estado de atraso gravado: atraso é filtro calculado por data, como em [17](17-regras-modulos.md), seção 2.3 (T-04).
- Lançamento conciliado não é alterado. Correção é estorno e novo lançamento, com motivo.

---

## 4. Contas a pagar

### 4.1 Regras

- Despesa tem fornecedor, categoria, centro de custo, vencimento e valor.
- Rateio por centro de custo: a soma dos percentuais é 100%. Diferença bloqueia o lançamento.
- Aprovação: pendente bloqueia a baixa. Solicitante não aprova a própria despesa. Acima de R$ 10.000 exige segundo aprovador. Decidido em 03/11/2026, [17](17-regras-modulos.md), seção 2.4.
- Despesa com nota fiscal de fornecedor é recebida e validada pelo portal de terceiros ([38](38-portal-de-terceiros-prestadores.md)) e não é emitida aqui ([34](34-pagamentos-fiscal-bancos-por-portal.md)).

### 4.2 Pagamento

- Pagamento em lote: seleção de despesas aprovadas da mesma conta, com total conferido antes da confirmação.
- Pagamento tem chave de idempotência ([15](15-validacoes.md), seção 4). Reenvio não paga duas vezes.
- Pagamento por cheque segue a seção 5.

---

## 5. Cheques

- **Decidido** em 03/11/2026 (FIN-02): cheque é aceito como forma de pagamento de aluno, com limite por cheque configurado pela escola.

### 5.1 Cheque recebido

| Estado | Significado |
|---|---|
| `recebido` | Recebido na unidade, com dados conferidos |
| `custodiado` | Guardado para depósito |
| `depositado` | Enviado para compensação, em conta indicada |
| `compensado` | Dinheiro entrou. Gera movimentação |
| `devolvido` | Não compensado. Volta ao titular como título em aberto, com motivo |
| `substituido` | Trocado por outra forma, com registro |

### 5.2 Cheque emitido

| Estado | Significado |
|---|---|
| `emitido` | Preenchido e aprovado |
| `entregue` | Enviado ao favorecido |
| `compensado` | Pago. Gera movimentação |
| `cancelado` | Cancelado com motivo. Não reaproveita número |

### 5.3 Regras

- Número de cheque emitido é único por conta. Cancelado não é reaproveitado.
- Cheque recebido devolvido gera aviso ao responsável pela cobrança ([57](57-notificacoes-por-portal.md)). Não gera multa sem a regra de [18](18-regras-modulos-2.md).
- Custódia física: a guarda do cheque recebido segue regra própria **(jurídico)**. Ver FIN-06.

---

## 6. Caixa físico

- Cada caixa é uma conta do tipo caixa, com um operador por vez.
- **Abertura:** saldo inicial conferido pelo operador. Diferença é registrada.
- **Movimentação:** recebimentos em dinheiro, cheques e cartões. Sangria e suprimento exigem motivo e aprovação de quem a escola indicar.
- **Fechamento:** contagem pelo operador. Diferença entre o contado e o calculado vai para a coordenação do financeiro, com motivo. **Decidido** em 03/11/2026 (FIN-05): sem tolerância. Qualquer diferença vai para a coordenação.
- Caixa fechado não recebe lançamento. Reabertura exige justificativa e aprovação.
- Fechamento gera relatório de caixa, com recebimentos por forma.

---

## 7. Fluxo de caixa

- **Realizado:** movimentações lançadas e conciliadas, por conta e por data.
- **Projetado:** títulos a receber e contas a pagar em aberto, pela data de vencimento. Não grava nada: é consulta.
- **Diário:** entradas, saídas e saldo por dia, com a linha de saldo projetado.
- Projeção usa somente títulos com estado válido. Estorno e título cancelado saem da projeção.

---

## 8. DRE

### 8.1 Estrutura

- Cada categoria financeira aponta para uma linha da DRE. Categoria sem linha não entra no demonstrativo e aparece como pendência.
- Centro de custo é filtro, não linha.
- A DRE tem as linhas da v1 (receita bruta, deduções, receita líquida, custos, despesas, resultado), com o detalhamento que a entidade configurar.

### 8.2 Regime

- A DRE pode ser por **caixa** (pelo que foi pago e recebido) ou por **competência** (pelo período a que o valor se refere).
- **Decidido** em 03/11/2026 (FIN-01): a DRE é por competência. A escolha é por entidade e não muda no meio do exercício. Lançamento de caixa entra no período a que se refere.

---

### 8.3 Orçamento

**Decidido** em 03/11/2026 (FIN-07): o orçamento fica no financeiro.

- Orçamento é por centro de custo e categoria, por mês e por exercício. Estado: `rascunho`, `aprovado`, `encerrado`.
- Orçado versus realizado: o realizado vem dos lançamentos da seção 4 e da seção 3. Não é digitado.
- Desvio acima do limite configurado pela escola gera aviso à gestão. O aviso não bloqueia lançamento.
- Orçamento aprovado não muda. Ajuste é nova versão, com aprovação da gestão.

## 9. Conciliação

Regras já definidas em [17](17-regras-modulos.md), seção 2.5, e [20](20-pagamentos-seguranca.md), seção 12. Reforço:

- Tolerância de arredondamento é parâmetro da entidade, não constante ([17](17-regras-modulos.md), LAC-06).
- Conciliação não ajusta sozinha. Diferença vira item de conciliação e o ajuste é lançamento com motivo e aprovação.
- Extrato OFX é importado com hash por linha, para não duplicar.

---

## 10. Inadimplência e fiscal

- Inadimplência, régua e cadastro de inadimplente seguem [18](18-regras-modulos-2.md) e [26](26-sdd-juridico-regulatorio.md). Comunicação prévia por escrito antes de qualquer cadastro (CDC, art. 43, §2º) **(jurídico)**.
- Comprovante de IRPF do pagador: regra fiscal a confirmar (FIN-03).
- NFS-e de mensalidade e de serviço seguem [34](34-pagamentos-fiscal-bancos-por-portal.md).

---

## 11. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Ver e gerir o financeiro da própria empresa, separado da entidade | Ver financeiro de entidade | P |
| **Gestão** | Ver tudo: DRE, fluxo, inadimplência, caixa. Aprovar despesa e fechamento de caixa | Operar caixa. Lançar pagamento sem aprovação | E |
| **Financeiro** (perfil da unidade) | Operar contas, cheques, caixa, pagamentos, conciliação. Gerar relatório financeiro | Aprovar a própria despesa. Aprovar a própria diferença de caixa | E |
| **Coordenação** | Ver o financeiro da unidade, em leitura | Lançar ou aprovar lançamento | E |
| **Secretaria** | Receber pagamento de aluno na unidade, em caixa de atendimento. Emitir boleto e segunda via | Pagar despesa. Ver DRE | E |
| **Professor** | Nada | Qualquer item financeiro | E |
| **Aluno** | Ver e pagar os próprios títulos. Ver comprovantes e informe de pagamento | Ver título de colega | E |
| **Responsáveis** | Ver e pagar faturas dos dependentes. Ver comprovantes | Ver título de outra família | E, só dependentes com vínculo ativo |
| **Terceiros** (fornecedores) | Ver a própria conta a receber, enviar nota e acompanhar o pagamento | Ver outros fornecedores ou o caixa | E |

---

## 12. Pendências

| # | Pendência | Tipo |
|---|---|---|
| FIN-01 | DRE por caixa ou por competência (seção 8.2) | **Decidido** em 03/11/2026: competência |
| FIN-02 | Cheque como forma de pagamento de aluno (seção 5) | **Decidido** em 03/11/2026: aceito, com limite por cheque configurado pela escola |
| FIN-03 | Comprovante de IRPF do pagador: obrigação, formato e prazo (seção 10) | (verificar) |
| FIN-04 | "Parcelas de serviços financeiros" do menu iScholar (seção 1) | **Decidido** em 03/11/2026: não se aplica. Sai do escopo |
| FIN-05 | Tolerância de diferença de caixa (seção 6) | **Decidido** em 03/11/2026: sem tolerância |
| FIN-06 | Guarda física de cheque recebido e prazo (seção 5.3) | (jurídico) |
| FIN-07 | Orçamento orçado versus realizado (seção 8.3) | **Decidido** em 03/11/2026: no financeiro |
| FIN-08 | DDL: contas, movimentação, cheque, caixa, fechamento, rateio, categoria e linha de DRE | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.16. Revisão do owner pendente (DDL-01) |

---

## 13. Critérios de aceite

- [ ] Rateio de centro de custo com soma diferente de 100% é recusado (teste).
- [ ] Solicitante não aprova a própria despesa (teste).
- [ ] Pagamento repetido com a mesma chave não paga duas vezes (teste de idempotência).
- [ ] Cheque cancelado não reaproveita número (teste).
- [ ] Caixa fechado não recebe lançamento (teste).
- [ ] Projeção não grava nada (teste).
- [ ] Categoria sem linha de DRE aparece como pendência, não some (teste).
- [ ] Responsável não vê título de outra família (teste de isolamento).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
