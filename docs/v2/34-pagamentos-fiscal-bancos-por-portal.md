# 34 — Pagamentos, Gateways, Split, Notas Fiscais, Bancos e Carteiras, por Portal

> Parte do [SDD v2](00-README.md). Segurança de pagamento em [20](20-pagamentos-seguranca.md). Integrações e credenciais em [16](16-integracoes-externas.md). Cobrança e NFS-e em [18](18-regras-modulos-2.md). Matriz de portais em [31](31-matriz-portais-modulos.md).
> **Status:** aprovada pelo autor em 03/11/2026, com as propostas adotadas. Itens sem valor definido continuam pendentes, criada em 03/11/2026. Itens **[Decisão do autor]** dependem de resposta. Itens **(jurídico)** dependem de parecer (arranjo de pagamento, nota fiscal, Open Finance). Não é parecer.

---

## 1. Resposta direta

| Assunto | Estado na v2 | Veredito |
|---|---|---|
| Gateways de pagamento | Lista de adapters em [16](16-integracoes-externas.md), seção 3. Segurança em [20](20-pagamentos-seguranca.md) | **Completa** desde 03/11/2026: EFÍ incluída, um gateway primário por unidade (SRC-05) e contingência na seção 2.3 (PAG-01). Fonte da lista: [`spec_gestao_billing_cobranca_mensalidades.md`](anexo-v1/spec_gestao_billing_cobranca_mensalidades.md), seção 17.1 |
| Split de pagamento | Opção (c) em [20](20-pagamentos-seguranca.md), seção 2. Não decidida | **Incompleta.** Sem decisão, sem modelo de subconta, sem regra de taxa |
| Emissão de nota fiscal | [16](16-integracoes-externas.md) (NFS-e por município) e [18](18-regras-modulos-2.md), seção 2.7 | **Incompleta.** Faltam NFS-e Nacional, cancelamento, XML e PDF, certificado, nota da plataforma e nota de terceiros |
| Bancos | Módulo "Bancos" tratado como dados bancários em [19](19-regras-modulos-3.md), seções 2 e 16 | **Errado.** Ver seção 4 |
| Carteiras digitais e débito automático | Não há especificação | **Ausente** |
| Open Finance | Não há especificação na v2. A v1 cita em [`spec_gestao_billing_cobranca_mensalidades.md`](anexo-v1/spec_gestao_billing_cobranca_mensalidades.md) | **Ausente** |

---

## 2. Gateways de pagamento

### 2.1 Lista consolidada

| Provedor | Métodos | Credencial (v1) | Origem |
|---|---|---|---|
| Asaas | Pix, boleto, cartão, carteira | Chave de API, identificador de carteira, URL de webhook | v1 billing, 17.1 |
| Mercado Pago | Pix, boleto, cartão | Access token, chave pública | v1 billing, 17.1 |
| PagSeguro | Boleto, cartão, Pix | Token, e-mail, modo sandbox | v1 billing, 17.1 |
| Gerencianet / EFÍ | Pix, boleto | Client ID, client secret, certificado Pix (.p12 ou .pem) | v1 billing, 17.1. Incluído na v2 em 03/11/2026 (PAG-01) |
| Stripe | Cartão | Chave secreta, chave pública, segredo de webhook | v1 billing, 17.1 |

**Regras que faltam na v2:**

- Certificado Pix (.p12 ou .pem) é segredo. Fica no cofre ([05](05-seguranca.md), seção 2), nunca no banco comum.
- Modo sandbox não pode ser ativado em produção. O sistema recusa a credencial de teste em ambiente de produção.
- Contingência: quando o gateway primário cai, o sistema não troca de provedor sozinho. Troca é decisão do financeiro, com registro. Regra completa na seção 2.3.
- Teste de conectividade com resultado imediato (v1, 17.1) é permitido, mas não grava o dado de teste.

### 2.2 Gateway por escala

| Escala | Quem configura | Conta de quem | Fonte |
|---|---|---|---|
| Entidade (cobrança de alunos) | Administrador da entidade, com MFA | Entidade | [20](20-pagamentos-seguranca.md), opção (a) |
| Plataforma (cobrança de clientes SaaS) | Financeiro da plataforma | Plataforma | [20](20-pagamentos-seguranca.md), seção 19.1 |

Gateway da plataforma que recebe por conta de entidade é custódia. Só existe se o parecer de [20](20-pagamentos-seguranca.md) for favorável.

### 2.3 Gateway por unidade e contingência (PAG-01)

Cada unidade tem **um gateway primário** (SRC-05). A unidade pode cadastrar **um gateway de contingência**, de outro provedor, com conta da própria entidade.

| Situação | Regra |
|---|---|
| Primário saudável | Toda cobrança nova sai pelo primário |
| Primário com falha | O monitor marca o provedor como degradado depois de 3 falhas seguidas de criação de cobrança ou de 5 minutos sem resposta ([20](20-pagamentos-seguranca.md), seção 16). O financeiro da unidade recebe aviso |
| Troca para contingência | Decisão do financeiro da unidade, com MFA e motivo. Vale só para cobrança nova. Fica na auditoria ([29](29-auditoria.md)) |
| Cobrança já emitida | Continua no gateway que a emitiu. Não é cancelada nem reemitida em outro provedor, para não haver dois boletos ou dois Pix válidos para o mesmo título |
| Webhook e conciliação | Cada gateway concilia as próprias cobranças. A conciliação diária roda para os dois enquanto houver cobrança aberta em algum deles ([20](20-pagamentos-seguranca.md), seção 12) |
| Volta ao primário | Decisão do financeiro, com registro, depois de teste de conectividade aprovado |
| Sem contingência cadastrada | A unidade aceita só os meios manuais ([71](71-financeiro-completo-por-portal.md): caixa e cheque) até o primário voltar |

**Regras gerais:**

- Os dois gateways da unidade não podem ser do mesmo provedor. Contingência no mesmo provedor não protege de queda do provedor.
- A credencial de cada gateway fica no cofre, separada por unidade ([05](05-seguranca.md), seção 2). Certificado Pix da EFÍ segue a mesma regra.
- Unidades da mesma entidade podem usar provedores diferentes. A troca numa unidade não afeta as outras.
- O provedor que emitiu cada título fica gravado no título. Relatório de recebimento mostra o provedor por título.

---

## 3. Split de pagamento

**Estado:** opção (c) em [20](20-pagamentos-seguranca.md), seção 2. Padrão desta versão é a opção (a): cada entidade tem a própria conta, sem custódia da plataforma.

**Se o split for adotado**, a especificação precisa de:

| Item | Regra proposta |
|---|---|
| Subconta | Cada entidade tem uma subconta no provedor, com identificador de carteira guardado. O identificador é dado de configuração, não segredo, mas fica vinculado à entidade. |
| Taxa | Percentual ou valor fixo da plataforma, por contrato. Gravado no momento da cobrança. Não muda retroativamente. |
| Divisão | Valor bruto, taxa, valor líquido da entidade e valor da plataforma gravados no lançamento do ledger ([20](20-pagamentos-seguranca.md), seção 4). |
| Estorno | Estorno devolve da subconta da entidade e da plataforma na proporção gravada. Taxa estornada só se o contrato permitir. |
| Conciliação | Diária por subconta, contra o extrato do provedor ([20](20-pagamentos-seguranca.md), seção 12). |
| Falha parcial | Se o provedor confirma uma parte, a diferença vira item de conciliação. Nunca é lançada automaticamente. |
| Contrato | Subcontas e taxa exigem contrato com o provedor e com a entidade. **(jurídico)** |

**Por portal:**

- Desenvolvedor: visão de taxas recebidas por entidade e por período.
- Gestão: visão do líquido recebido e do que foi retido como taxa.
- Responsáveis e aluno: aparecem só o valor pago e o estado. Taxa nunca aparece para o pagador.

**Decidido** em 03/11/2026: split em duas formas, automática e pelo gateway. Entidade sem fins lucrativos: mesmo split, com taxa da plataforma menor.

---

## 4. Módulo "Bancos": achado crítico

Os dois arquivos [`spec_gestao_bancos.md`](anexo-v1/spec_gestao_bancos.md) e [`spec_gestao_bancos_completo.md`](anexo-v1/spec_gestao_bancos_completo.md) têm 305 linhas cada e são **idênticos em conteúdo**. Não tratam de dados bancários de alunos, entidades ou fornecedores. Tratam de **gestão de bancos de dados**:

- inventário e descoberta de instâncias;
- console SQL com histórico, snippets e favoritos;
- migrações;
- backup e restauração;
- replicação e alta disponibilidade;
- visualizador de esquema;
- monitoramento.

A v2 classifica esse arquivo como "dados bancários" ([12](12-catalogo-modulos.md), linha 21; [19](19-regras-modulos-3.md), linha 25) e propõe que ele vire um conector de extrato. **Essa leitura está errada.**

**Risco:** um console SQL e uma ferramenta de migração expostos a usuários de entidade, em um SaaS multi-tenant, dão acesso direto ao banco de todos os clientes. Isso anula o isolamento de [03](03-dominio-tenancy.md).

**Decisão proposta:**

1. Remover o módulo "Bancos" do produto. Ele é ferramenta de operação e não entra no catálogo de módulos.
2. Se a equipe de operação precisar da ferramenta, ela roda fora do produto, com acesso restrito à rede de operação ([10](10-implantacao-operacao.md)), sem acesso pelos portais.
3. Dados bancários (conta de entidade, conta de fornecedor, conta para repasse) vivem no módulo **Financeiro**, com a regra de MFA para alteração ([31](31-matriz-portais-modulos.md), seção 4.3).

**Decidido** em 03/11/2026: módulo Bancos removido do escopo.

---

## 5. Nota fiscal

### 5.1 Quem emite, por escala e por portal

| Nota | Quem emite | Portal de origem | Estado |
|---|---|---|---|
| NFS-e de mensalidade e serviço educacional | Entidade, por município | Gestão | Parcial. Ver 5.2 |
| NFS-e da assinatura SaaS (plataforma cobra a entidade) | Plataforma | Desenvolvedor | **Ausente.** Precisa de especificação própria |
| NF-e de serviço de fornecedor (terceiros) | Fornecedor, no próprio sistema ou no município | Terceiros | Conflito. Ver 5.3 |
| NF-e de produto (SEFAZ) | — | Desenvolvedor (v1, "Gestão de integração") | **Fora de escopo.** Não há venda de produto no escopo. Confirmar |

### 5.2 Regras da NFS-e (entidade)

Já definido: emissão só para fatura paga ou parcial, conforme regra municipal; estados `pending`, `processing`, `issued`, `rejected`, `cancelled`; cancelamento transmitido ao município ([18](18-regras-modulos-2.md), seção 2.7).

Faltam:

- **NFS-e Nacional** (padrão ABRASF e nacional, citado na v1). Lista de municípios que usam cada padrão. **(jurídico)** e fiscal.
- **Certificado digital A1 ou A3** da entidade: guardado no cofre, nunca em arquivo ([16](16-integracoes-externas.md), seção 3).
- **Cancelamento:** prazo e justificativa exigidos pelo município. Cancelamento após o prazo exige processo fiscal, não ação do operador.
- **Reenvio** de nota rejeitada: só após correção do motivo. Nota rejeitada não é reemitida com o mesmo número.
- **Guarda:** XML e PDF guardados pelo prazo fiscal **(jurídico)**, com hash ([21](21-busca-e-armazenamento.md)).
- **Pagamento e nota:** emissão automática após pagamento é opcional. Se for automática, a nota tem o valor do pagamento confirmado, não o valor da fatura.
- **Tomador:** dado do responsável financeiro. Se o tomador tem dado pessoal, o campo segue a regra de [07](07-privacidade-lgpd.md).

### 5.3 Nota do fornecedor (terceiros)

A v1 ([`12-portals-navigation-sidebar-pages-spec.md`](anexo-v1/12-portals-navigation-sidebar-pages-spec.md), portal de terceiros, "Emissão e Upload de NF-e de Serviços") diz que o portal **emite** a nota. Isso não se sustenta: a nota é emitida pelo prestador, no município ou no seu sistema.

**Proposta:** o portal de terceiros **recebe e valida** a nota (XML, valor, tomador, competência), vincula à ordem de compra e ao pagamento, e não emite. Qualquer mudança de "emissão" para "envio" passa por revisão **(jurídico)** e fiscal.

**Decidido** em 03/11/2026: o portal de terceiros recebe e valida, sem emitir.

---

## 6. Bancos, Open Finance e débito automático

| Recurso | Quem usa | Regra proposta |
|---|---|---|
| Conta bancária da entidade | Financeiro da entidade | Cadastro no Financeiro. Alteração exige MFA e dupla aprovação |
| Conta bancária da plataforma | Financeiro da plataforma | Mesma regra, no portal do desenvolvedor |
| Dados bancários de fornecedor | Compras, terceiros | Terceiros cadastra. Compras aprova. Alteração gera alerta de possível fraude |
| Conciliação por extrato (OFX) | Financeiro | Já em [17](17-regras-modulos.md), seção 2.5 |
| Open Finance (leitura de extrato, consentimento) | Financeiro | Só com consentimento do titular da conta e regra do Open Finance. **(jurídico)**. Não especificado |
| Débito automático | Responsáveis | Autorização do pagador, revogável. Regra de cobrança em [18](18-regras-modulos-2.md). **(jurídico)** |

---

## 7. Carteiras digitais

**Estado:** ausente. Não há especificação de carteira digital (Apple Pay, Google Pay, carteira do provedor).

**Proposta mínima:** carteira digital é um **método de pagamento do gateway**, não módulo. O sistema não guarda token de carteira. Cada carteira aceita só o que o provedor suporta. Pagamento por carteira segue [20](20-pagamentos-seguranca.md), inclusive 3-D Secure.

**Decidido** em 03/11/2026: Pix e cartão pelo gateway da unidade, sem carteira própria.

---

## 8. Pagamento por portal

| Portal | Pagamento | Recurso |
|---|---|---|
| Desenvolvedor | Cobrança de clientes SaaS; recebimento da plataforma | Gateway da plataforma (com parecer), NFS-e da plataforma (ausente), taxas |
| Gestão | Cobrança de alunos e fornecedores; configuração do gateway | Gateway da entidade, split (se adotado), NFS-e da entidade, conciliação |
| Professor | Nenhum pagamento recebido. Holerite e pagamento de salário fora do escopo deste módulo | Só consulta do próprio holerite ([31](31-matriz-portais-modulos.md), seção 2.3) |
| Aluno | Pagar mensalidade: Pix, boleto, cartão | Cobrança, comprovante, segunda via |
| Responsáveis | Pagar fatura dos filhos; débito automático | Mesmos métodos, central financeira, débito automático (se aprovado) |
| Terceiros | Receber pagamento; enviar nota | Extrato, status da liquidação, envio de NF-e (seção 5.3), dados bancários com MFA |

**Regra:** nenhum portal, exceto Gestão e Desenvolvedor, mostra taxa, split ou conta de recebimento da entidade.

---

## 9. Pendências

| # | Pendência | Tipo |
|---|---|---|
| PAG-01 | Incluir EFÍ e regra de contingência entre gateways (seção 2) | **Escrito** em 03/11/2026: EFÍ na seção 2.1 e contingência na seção 2.3 |
| PAG-02 | Split: duas formas, automática e pelo gateway. Entidade sem fins lucrativos: mesmo split, com taxa da plataforma menor. Classificação da entidade (pública, particular, sem fins lucrativos) define só a taxa e a forma de cobrança (seção 3) | **Decidido** em 03/11/2026 |
| PAG-03 | Remover módulo "Bancos" de escopo e corrigir [12](12-catalogo-modulos.md) e [19](19-regras-modulos-3.md) (seção 4) | **Decidido** em 03/11/2026: removido. Correção de [12](12-catalogo-modulos.md) e [19](19-regras-modulos-3.md) é documento |
| PAG-04 | NFS-e Nacional, cancelamento, guarda de XML (seção 5.2) | (jurídico) e fiscal |
| PAG-05 | NFS-e da assinatura SaaS (plataforma) | Documento e (jurídico) |
| PAG-06 | Nota do fornecedor: recebe e valida, não emite (seção 5.3) | **Decidido** em 03/11/2026: só recebe e valida |
| PAG-07 | Open Finance e débito automático | (jurídico) |
| PAG-08 | Carteira digital: escopo e provedor (seção 7) | **Decidido** em 03/11/2026: Pix e cartão pelo gateway da entidade, sem carteira própria |
| PAG-09 | Corrigir a referência de fonte da lista de gateways: a lista vem de [`spec_gestao_billing_cobranca_mensalidades.md`](anexo-v1/spec_gestao_billing_cobranca_mensalidades.md) (v1), não de [01](01-visao-escopo.md) | **Feito** em 03/11/2026 na tabela de origem |

---

## 10. Critérios de aceite

- [ ] Todo gateway tem credencial no cofre e nenhuma em texto claro (teste de varredura, [20](20-pagamentos-seguranca.md)).
- [ ] Credencial de sandbox recusada em produção (teste).
- [ ] Nota emitida só para pagamento confirmado; nota rejeitada não é reemitida com o mesmo número.
- [ ] Módulo "Bancos" fora do catálogo de módulos e fora dos portais.
- [ ] Taxa e split, se adotados, gravados no lançamento e conciliados por subconta.
- [ ] Itens **[Decisão do autor]** e **(jurídico)** respondidos ou marcados como pendentes no [00](00-README.md).

## 11. Decisões de 03/11/2026

**PAG-02 (split): mantido na opção (a).** Mudanças necessárias se a opção (c) for adotada no futuro, listadas para análise:

| Documento | Mudança se (c) fosse adotado |
|---|---|
| [16](16-integracoes-externas.md), seção 3 | Gateway passa a ter subconta por entidade e identificador de carteira vinculado |
| [20](20-pagamentos-seguranca.md), seção 2 e seção 19 (D-10) | Opção (c) vira a decisão; padrão (a) é revogado; parecer deixa de ser condição |
| [20](20-pagamentos-seguranca.md), seção 4 | Lançamento grava valor bruto, taxa, valor líquido da entidade e valor da plataforma |
| [20](20-pagamentos-seguranca.md), seção 12 | Conciliação diária por subconta, além da conta de gateway |
| [18](18-regras-modulos-2.md), seção 2 | Baixa divide o pagamento; estorno devolve nas duas subcontas |
| [31](31-matriz-portais-modulos.md) e [23](23-dominios-provisionamento-ciclo-de-vida.md) | Portal do desenvolvedor passa a mostrar taxas recebidas por entidade |
| Jurídico | Contrato com o provedor para subconta; contrato de taxa com cada entidade |
| Operação | Teste de suporte do provedor a subcontas antes de qualquer contratação |

Enquanto (a) vigora, nenhuma dessas mudanças entra em produção.

**PAG-03 (módulo Bancos): removido do escopo de produto.** Substituição: painel de operação no portal do desenvolvedor, descrito abaixo. Não é módulo de tenant e não é console SQL aberto.

**Painel de bancos de dados (portal do desenvolvedor)**

| Recurso | Regra |
|---|---|
| Inventário | Lista dos bancos: master, cada banco de unidade, cada banco de identidade. Versão do esquema, tamanho e última restauração testada. |
| Migrações | Estado por unidade. Migração em lote só com plano de volta e aprovação de segundo papel. |
| Backup | Estado e prazo de cada backup. Restauração só por pedido com dupla aprovação, em ambiente isolado. |
| Consulta técnica | Não existe console SQL no painel comum. Acesso técnico direto só por procedimento de emergência: passkey, motivo e chamado vinculado, sessão de tempo limitado, leitura por padrão, escrita só com dupla aprovação. Cada comando é gravado e mascarado conforme [29](29-auditoria.md). |
| Dado pessoal | Qualquer consulta que atinja dado pessoal exige motivo e gera evento de auditoria. |
| Clientes | Nenhum portal de entidade vê este painel. |

Motivo: um console SQL acessível sem controle reduz o isolamento entre clientes a uma senha. O painel cobre a gestão de todos os bancos sem expor o conteúdo deles.
