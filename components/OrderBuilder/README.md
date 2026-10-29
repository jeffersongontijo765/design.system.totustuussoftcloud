# OrderBuilder

Monta um pedido de venda em uma tela: catálogo pesquisável, carrinho com quantidades, desconto, forma de pagamento e total, com estados de carrinho vazio e pedido confirmado.

## Quando usar

Use o OrderBuilder quando a operação precisa escolher produtos de um catálogo curto e fechar um pedido na mesma tela — planos, módulos, implantação, treinamento e suporte vendidos pela equipe comercial. O componente resolve busca, filtro por categoria, quantidade, desconto comercial, forma de pagamento e conferência do total sem sair da página.

É o componente certo para:

- pedido de balcão ou telefone, com poucos itens e um cliente por vez;
- renovação de plano com desconto de 5% ou 10%;
- venda avulsa de módulos e serviços para uma escola já cadastrada;
- protótipo de orçamento, quando o pagamento é apenas uma intenção.

Não use quando:

- o cliente fecha a compra sozinho, com cadastro e pagamento online — use uma página de checkout;
- o pedido tem dezenas de linhas ou variações por unidade — use [DataTable](../DataTable/README.md) com edição em lote;
- o objetivo é acompanhar pedidos já criados — use [RecordsTable](../RecordsTable/README.md) ou [ApprovalQueue](../ApprovalQueue/README.md);
- a cobrança é recorrente e precisa de vigência, reajuste e faturamento automático — o pedido registra a contratação, mas a recorrência pertence ao módulo financeiro;
- o catálogo depende de tabela de preços por cliente e região — resolva o preço no servidor e envie o valor final, não replique a regra no navegador.

Componentes próximos: [EmptyState](../EmptyState/README.md) para o carrinho vazio, [Toast](../Toast/README.md) para confirmações fora do painel, [Input](../Input/README.md) e [Select](../Select/README.md) para os campos, [KpiView](../KpiView/README.md) para o resumo do pedido em outra página.

## Anatomia

```
┌ Novo pedido · #PED-2026-0187 ────────────── Cliente [Colégio Horizonte] ┐
│ Catálogo · 10 produtos          │ Carrinho · 2                          │
│ [ Buscar produto………………… ] [/]  │ Plano Profissional   R$ 549,00        │
│ (Todos) (Planos) (Módulos) …    │   [− 1 +]                     ×       │
│ [Plano Essencial] [Profissional]│ Módulo Financeiro    R$ 189,00        │
│ [Plano Enterprise] [Financeiro] │ Subtotal             R$ 738,00        │
│ …                               │ Desconto 5%         −R$ 36,90         │
│                                 │ Total                R$ 701,10        │
│                                 │ (Pix) (Boleto) (Cartão)               │
│                                 │ [ Finalizar pedido · R$ 701,10 ]      │
└─────────────────────────────────┴───────────────────────────────────────┘
```

| Parte | Classe ou atributo | Obrigatório | Função |
|---|---|---|---|
| Raiz | `.ob-card` + `data-ttsc-order-builder` | Sim | Delimita o componente e recebe o namespace JS. |
| Cabeçalho | `.ob-head`, `.ob-eyebrow`, `.ob-title`, `.ob-sub` | Sim | Identifica o pedido, o cliente e o número do rascunho. |
| Status | `.ob-draft` (`#ob-status`) | Sim | Mostra “Rascunho” ou “Confirmado”, com texto além da cor. |
| Cliente | `.ob-field` > `#ob-client` | Sim | Seletor de cliente; use `data-no-custom` quando quiser o select nativo. |
| Catálogo | `.ob-catalog` | Sim | Coluna de busca, filtros e produtos. |
| Busca | `.ob-search` > `input[type="search"]` | Sim | Filtra por nome, descrição e categoria. O atalho `/` foca o campo. |
| Categorias | `.chips` > `.chip[data-cat]` | Sim | Filtro exclusivo com `aria-pressed`; inclui “Todos”. |
| Produto | `button.prod[data-id]` | Sim | Cartão inteiro é o botão de adicionar; contém ícone, nome, descrição, preço e disponibilidade. |
| No pedido | `.prod-in` | Não | Contador textual do produto no carrinho; `aria-hidden` porque o `aria-label` do botão já informa. |
| Carrinho | `.ob-cart` | Sim | Painel rebaixado com itens, totais, pagamento e ação principal. |
| Item | `.ci` | Sim | Linha do pedido com nome, ciclo, preço unitário, quantidade, total e remover. |
| Quantidade | `.ci-qty` | Sim | Grupo acessível com “−”, valor e “+”; limites de 1 a 9. |
| Totais | `.cart-totals` (`dl`) | Sim | Subtotal, desconto e total em `dt`/`dd`. |
| Desconto | `#ob-discount` | Sim | Select de 0%, 5% ou 10%; o valor abatido aparece ao lado. |
| Pagamento | `.pay` (`fieldset`) | Sim | Rádios nativos em três opções; a nota abaixo explica o prazo. |
| Ação principal | `.btn-primary` > `#ob-finish` | Sim | “Finalizar pedido” com o total repetido no botão. |
| Vazio | `.cart-empty` | Sim | Substitui o conteúdo do carrinho quando não há itens. |
| Confirmado | `.cart-success` (`role="status"`) | Sim | Número do pedido, total, forma de pagamento e “Novo pedido”. |
| Anúncio | `#ob-announce` (`role="status"`) | Sim | Região `sr-only` que anuncia adicionar, remover, quantidade e desconto. |

O corpo usa `grid-template-columns: minmax(0,1fr) 384px`. A coluna do carrinho tem largura fixa de 384 px e as duas colunas se esticam para a mesma altura; abaixo de 900 px o grid vira uma coluna e o carrinho desce inteiro, sem rolagem interna.

## Variantes

| Variante | Como aplicar | Uso |
|---|---|---|
| Pedido de venda (padrão do preview) | Estrutura completa, 2 itens iniciais, Pix e 5% de desconto. | Balcão, telefone e renovação assistida. |
| Orçamento | `data-mode="quote"` na raiz; oculte `.pay` e `.pay-note`, troque o rótulo do botão para “Salvar proposta” e não envie `payment_method`. | Proposta enviada ao cliente antes da aprovação. |
| Assinatura | Use produtos com ciclo `monthly`; mostre a vigência em `.success-note` e mantenha o desconto como condição comercial. | Contratação de plano com cobrança recorrente no financeiro. |
| Pedido rápido | Esconda `.prod-desc` e `.cat-hint`; reduza o carrinho para 340 px. | Operação de balcão com catálogo conhecido e pressa. |
| Somente consulta | `pointer-events:none` no catálogo e no carrinho, com `aria-disabled="true"` no botão principal. | Conferência de um pedido já confirmado. |

O estado confirmado não é uma variante de layout: ele substitui o corpo do carrinho e mantém o catálogo para o próximo pedido. Ao adicionar um produto depois de confirmar, o componente inicia um novo rascunho e incrementa o número.

## Estados

| Estado | Como aparece | Regra |
|---|---|---|
| Rascunho | Cabeçalho com “Rascunho”, 2 itens, totais e pagamento visíveis. | Estado inicial do preview. |
| Adicionando | Contador `.prod-in`, animação curta no ícone e mensagem no `role="status"`. | O foco permanece no cartão do produto; não re-renderize o catálogo. |
| Sem resultados | `.cat-empty` com “Nenhum produto encontrado”, texto do filtro e “Limpar filtros”. | A busca e a categoria continuam preenchidas. |
| Vazio | `.cart-empty`, contador oculto, “Adicionar itens” leva ao catálogo. | O botão de finalizar não fica visível. |
| Limite | Quantidade máxima de 9; “+” desabilitado e anúncio “Limite de 9 unidades por item.”. | Nunca permita quantidade 0; para zerar, use remover. |
| Desconto | `0%`, `5%` ou `10%`; o valor abatido e a nota “x% de desconto aplicado” mudam juntos. | O desconto é comercial, não fiscal. |
| Pagamento | Pix, Boleto ou Cartão; a nota e a confirmação mudam por método. | Os rádios nativos preservam as setas do teclado. |
| Processando | Botão desabilitado com “Processando…” e `aria-busy="true"` na raiz. | Só durante a chamada de criação; mantenha os itens visíveis. |
| Confirmado | `.cart-success` com número, total e pagamento; cabeçalho “Confirmado”. | `role="status"` e foco no bloco; “Novo pedido” limpa e incrementa o número. |
| Erro | Faixa `role="alert"` acima dos totais, com “Tentar novamente”. | Não limpe o carrinho; o servidor é a fonte do total. |
| Desabilitado | `opacity:.5`, sem ponteiro, `aria-disabled="true"`. | Vale para o botão principal sem itens e para o seletor durante o envio. |

## Acessibilidade

- **Catálogo:** cada produto é um `<button>` com `aria-label` completo — nome, preço, ciclo e quantidade no pedido. Enter e Espaço adicionam; o foco não se perde e o contador é atualizado em texto.
- **Mensagens:** `#ob-announce` é `role="status"` e `aria-live="polite"`; a linha visível `.cart-live` é `aria-hidden="true"` para não duplicar o anúncio. O estado confirmado tem `role="status"` e recebe foco.
- **Quantidade:** cada grupo `.ci-qty` tem `aria-label="Quantidade de …"`; os botões dizem “Diminuir/Aumentar quantidade de …”; nos limites, o botão fica `disabled`.
- **Pagamento:** `fieldset` + `legend` “Forma de pagamento”; os rádios são nativos, com o rótulo “Pix”, “Boleto” ou “Cartão”. O anel de foco aparece no cartão visual.
- **Totais:** `dl` com `dt`/`dd`; o valor do desconto é precedido por “−” e o total aparece por extenso. O botão repete o total para quem não vê o resumo.
- **Busca:** `input[type="search"]` com `aria-label`; `/` foca o campo, Esc limpa; o botão de limpar tem 24×24 px e `aria-label`.
- **Filtros:** botões com `aria-pressed`; a contagem “3 de 10 produtos” é textual.
- **Disponibilidade:** ponto + palavra (“Disponível”, “Sob demanda”, “Últimas vagas”); nunca só a cor.
- **Foco:** contorno de 2 px em `--ttsc-accent` com offset de 2 px; campos com `:focus-within` reforçam com halo `--ttsc-accent-soft`.
- **Alvos:** ações do carrinho têm pelo menos 24×24 px; o cartão do produto inteiro é o alvo de adicionar.
- **Movimento:** as animações de “pop” e de entrada do estado são curtas e desligadas por `prefers-reduced-motion`.
- **Ordem de leitura:** cabeçalho → cliente → catálogo (busca, filtros, produtos) → carrinho (itens, totais, pagamento, ação). No mobile, o carrinho vem depois do catálogo; o botão “Adicionar itens” devolve o foco à busca.

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Calcule subtotal, desconto e total no servidor antes de gravar. | Confiar no total enviado pelo navegador. |
| Anuncie adicionar, remover, quantidade e desconto em uma única região `role="status"`. | Anunciar cada tecla digitada na busca. |
| Mantenha o foco no produto ou no botão de quantidade após a ação. | Re-renderizar o catálogo inteiro a cada clique e perder o foco. |
| Mostre a base do cálculo: subtotal, percentual e valor abatido. | Exibir só o total “com desconto” sem explicar o abatimento. |
| Use texto + ícone para disponibilidade e status. | Comunicar “esgotado” apenas com um ponto vermelho. |
| Desabilite o “+” no limite e o remover no último item. | Permitir quantidade 0 ou quantidade negativa. |
| Use “Finalizar pedido” quando há itens e “Novo pedido” depois de confirmar. | Reutilizar “Novo pedido” para cancelar um pedido já enviado. |
| Trate o ciclo `mensal`/`único` no rótulo do preço. | Somar planos mensais e serviços únicos como se fossem a mesma recorrência. |
| Mantenha o resumo visível ao revisar o pagamento. | Esconder os itens atrás de um modal no meio do fluxo. |
| Peça confirmação antes de descartar um rascunho com itens. | Limpar o carrinho ao trocar de cliente sem aviso. |

## API

Namespace global: `window.TTSCOrderBuilder`. O preview roda uma instância embutida com dados ilustrativos; o contrato abaixo é o do módulo em `assets/js/core/ttsc.order-builder.js`.

```js
const builder = TTSCOrderBuilder.init(el, {
  currency: 'BRL',
  locale: 'pt-BR',
  maxQty: 9,
  client: { selected: 'uuid-do-cliente', options: clientes },
  catalog: produtos,
  initialItems: [{ id: 'profissional', qty: 1 }],
  discount: 5,
  payment: 'pix',
  endpoint: '/developer/commercial/orders',
  onFinalize: async (payload) => { /* retorno do servidor */ }
});
```

| Opção | Tipo | Padrão | Função |
|---|---|---|---|
| `currency` | string | `'BRL'` | Moeda da formatação e do envio. |
| `locale` | string | `'pt-BR'` | Formatação de números e datas. |
| `maxQty` | number | `9` | Limite por item. |
| `catalog` | array | lido do DOM | `{id, name, description, price, cycle, category, icon, availability}`; `price` em centavos. |
| `initialItems` | array | `[]` | `{id, qty}` do rascunho. |
| `client` | object | `{}` | Cliente selecionado e opções do seletor. |
| `discount` | number | `0` | Percentual inicial: `0`, `5` ou `10`. |
| `payment` | string | `'pix'` | `pix`, `boleto` ou `cartao`. |
| `endpoint` | string | `null` | URL de criação; sem ela, o componente só simula o sucesso. |
| `onFinalize` | function | `null` | Recebe o payload e devolve a resposta; use para integrar sem `fetch` próprio. |

Métodos da instância:

| Método | Retorno | Função |
|---|---|---|
| `addItem(id, qty = 1)` | item | Adiciona ou incrementa; respeita `maxQty`. |
| `removeItem(id)` | boolean | Remove a linha e atualiza totais. |
| `setQuantity(id, qty)` | item | Ajusta entre 1 e `maxQty`; `0` remove. |
| `getTotals()` | objeto | `{count, subtotal, discount, total, items}`, em centavos. |
| `getState()` | objeto | Cópia do estado atual, incluindo cliente, pagamento e status. |
| `reset()` | void | Limpa o carrinho, zera desconto e abre um novo rascunho. |
| `destroy()` | void | Remove listeners e devolve o DOM ao estado inicial. |
| `on(event, handler)` | função | Assina eventos; devolve o cancelamento. |

Eventos: `order:add`, `order:remove`, `order:quantity`, `order:discount`, `order:payment`, `order:client`, `order:finalize`, `order:reset`, `catalog:filter`. O payload sempre traz `{orderId, item, totals}` quando aplicável.

Atributos `data-*` no HTML: `data-ttsc-order-builder`, `data-endpoint`, `data-currency`, `data-locale`, `data-max-qty`, `data-initial-items` (JSON), `data-client`, `data-discounts` (`0,5,10`). Não coloque preço, total ou token no atributo: o preço vem do catálogo do servidor e o total é recalculado na gravação.

## Modelos

### HTML

```html
<section class="ob-card" data-ttsc-order-builder
         data-endpoint="<?= $this->e($createUrl) ?>"
         data-currency="BRL" data-max-qty="9"
         data-discounts="0,5,10"
         aria-labelledby="pedido-titulo">
  <header class="ob-head">
    <div class="ob-id">
      <span class="ob-icon" aria-hidden="true"><i class="fa-light fa-cart-shopping"></i></span>
      <div>
        <p class="ob-eyebrow"><span class="dot" aria-hidden="true"></span>Pedido de venda · <span data-order-number>#<?= $this->e($draftNumber) ?></span></p>
        <h2 class="ob-title" id="pedido-titulo">Novo pedido</h2>
        <p class="ob-sub">Cliente: <strong data-client-name><?= $this->e($clientName) ?></strong> · Tabela de preços 2026</p>
      </div>
    </div>
    <div class="ob-head-actions">
      <div class="ob-field">
        <label for="pedido-cliente">Cliente</label>
        <div class="ob-select">
          <i class="fa-light fa-building lead" aria-hidden="true"></i>
          <select id="pedido-cliente" data-no-custom aria-label="Cliente do pedido">
            <?php foreach ($clients as $client): ?>
              <option value="<?= $this->e($client['uuid']) ?>" <?= $client['selected'] ? 'selected' : '' ?>>
                <?= $this->e($client['trade_name'] ?: $client['legal_name']) ?>
              </option>
            <?php endforeach; ?>
          </select>
          <i class="fa-light fa-chevron-down chev" aria-hidden="true"></i>
        </div>
      </div>
      <span class="ob-draft" id="pedido-status" aria-label="Pedido em rascunho">
        <i class="fa-light fa-pen" aria-hidden="true"></i><span>Rascunho</span>
      </span>
    </div>
  </header>

  <div class="ob-body">
    <section class="ob-catalog" aria-labelledby="pedido-catalogo">
      <div class="cat-head">
        <div class="cat-title"><h3 id="pedido-catalogo">Catálogo</h3><span class="cat-note" data-catalog-count><?= count($products) ?> produtos</span></div>
        <span class="cat-hint"><i class="fa-light fa-hand-pointer" aria-hidden="true"></i>Clique para adicionar</span>
      </div>

      <div class="ob-search" role="search">
        <i class="fa-light fa-magnifying-glass" aria-hidden="true"></i>
        <input type="search" placeholder="Buscar produto, módulo ou serviço..." aria-label="Buscar no catálogo" data-catalog-search>
        <button type="button" class="clear" data-catalog-clear aria-label="Limpar busca" hidden><i class="fa-light fa-circle-xmark" aria-hidden="true"></i></button>
        <kbd aria-hidden="true">/</kbd>
      </div>

      <div class="chips" role="group" aria-label="Filtrar o catálogo por categoria" data-catalog-chips>
        <button type="button" class="chip" data-cat="Todos" aria-pressed="true">Todos <span class="n"><?= count($products) ?></span></button>
        <?php foreach ($categories as $category): ?>
          <button type="button" class="chip" data-cat="<?= $this->e($category['name']) ?>" aria-pressed="false">
            <?= $this->e($category['name']) ?> <span class="n"><?= (int) $category['total'] ?></span>
          </button>
        <?php endforeach; ?>
      </div>

      <div class="prod-grid" data-catalog-grid>
        <?php foreach ($products as $product): ?>
          <button type="button" class="prod" data-id="<?= $this->e($product['uuid']) ?>"
                  data-price="<?= (int) round($product['unit_price'] * 100) ?>"
                  data-cycle="<?= $this->e($product['billing_cycle']) ?>"
                  data-category="<?= $this->e($product['category']) ?>"
                  aria-label="Adicionar <?= $this->e($product['name']) ?> por <?= $this->money($product['unit_price']) ?> ao pedido">
            <span class="prod-icon" aria-hidden="true"><i class="fa-light <?= $this->e($product['icon']) ?>"></i></span>
            <span class="prod-main">
              <span class="prod-name-row">
                <span class="prod-name"><?= $this->e($product['name']) ?></span>
                <span class="prod-in" aria-hidden="true"></span>
              </span>
              <span class="prod-desc"><?= $this->e($product['description']) ?></span>
              <span class="prod-foot">
                <span class="prod-price"><?= $this->money($product['unit_price']) ?><small><?= $this->e($product['suffix']) ?></small></span>
                <span class="avail <?= $this->e($product['tone']) ?>"><i class="fa-light fa-circle" aria-hidden="true"></i><?= $this->e($product['availability']) ?></span>
                <span class="prod-add" aria-hidden="true"><i class="fa-light fa-plus"></i></span>
              </span>
            </span>
          </button>
        <?php endforeach; ?>
      </div>

      <div class="cat-empty" data-catalog-empty hidden>
        <span class="ce-ico" aria-hidden="true"><i class="fa-light fa-magnifying-glass"></i></span>
        <p>Nenhum produto encontrado</p>
        <span>Ajuste a busca ou escolha outra categoria.</span>
        <button type="button" data-catalog-reset>Limpar filtros</button>
      </div>
    </section>

    <aside class="ob-cart" aria-labelledby="pedido-carrinho">
      <div class="cart-head" data-cart-head>
        <div class="cart-title">
          <span class="cart-ico" aria-hidden="true"><i class="fa-light fa-basket-shopping"></i></span>
          <h3 id="pedido-carrinho" tabindex="-1">Carrinho</h3>
          <span class="cart-count" data-cart-count aria-label="2 itens no pedido">2</span>
        </div>
        <button type="button" class="ghost-btn" data-cart-new><i class="fa-light fa-rotate-left" aria-hidden="true"></i><span>Novo pedido</span></button>
      </div>

      <p class="cart-live" data-cart-live aria-hidden="true"><i class="fa-light fa-circle-check"></i><span>2 itens no pedido. Revise antes de finalizar.</span></p>

      <div class="cart-core" data-cart-core>
        <ul class="cart-items" data-cart-items aria-label="Itens do pedido">
          <?php foreach ($items as $item): ?>
            <li class="ci" data-id="<?= $this->e($item['uuid']) ?>">
              <span class="ci-ico" aria-hidden="true"><i class="fa-light <?= $this->e($item['icon']) ?>"></i></span>
              <div class="ci-main">
                <p class="ci-name"><span><?= $this->e($item['name']) ?></span><small><?= $this->e($item['cycle']) ?></small></p>
                <p class="ci-unit"><?= $this->money($item['unit_price']) ?> cada</p>
              </div>
              <span class="ci-line"><?= $this->money($item['line_total']) ?></span>
              <div class="ci-qty" role="group" aria-label="Quantidade de <?= $this->e($item['name']) ?>">
                <button type="button" data-act="dec" data-id="<?= $this->e($item['uuid']) ?>" aria-label="Diminuir quantidade de <?= $this->e($item['name']) ?>" <?= $item['qty'] <= 1 ? 'disabled' : '' ?>><i class="fa-light fa-minus" aria-hidden="true"></i></button>
                <span class="n" aria-live="off"><?= (int) $item['qty'] ?></span>
                <button type="button" data-act="inc" data-id="<?= $this->e($item['uuid']) ?>" aria-label="Aumentar quantidade de <?= $this->e($item['name']) ?>" <?= $item['qty'] >= 9 ? 'disabled' : '' ?>><i class="fa-light fa-plus" aria-hidden="true"></i></button>
              </div>
              <button type="button" class="ci-remove" data-act="remove" data-id="<?= $this->e($item['uuid']) ?>" aria-label="Remover <?= $this->e($item['name']) ?> do pedido"><i class="fa-light fa-xmark" aria-hidden="true"></i></button>
            </li>
          <?php endforeach; ?>
        </ul>

        <dl class="cart-totals">
          <div class="trow"><dt>Subtotal</dt><dd data-subtotal><?= $this->money($totals['subtotal']) ?></dd></div>
          <div class="trow">
            <dt>Desconto</dt>
            <dd>
              <span class="disc-amt" data-discount-amount>−<?= $this->money($totals['discount']) ?></span>
              <span class="disc-sel">
                <select data-discount data-no-custom aria-label="Desconto do pedido">
                  <option value="0">0%</option>
                  <option value="5" <?= $totals['percent'] === 5 ? 'selected' : '' ?>>5%</option>
                  <option value="10" <?= $totals['percent'] === 10 ? 'selected' : '' ?>>10%</option>
                </select>
                <i class="fa-light fa-chevron-down" aria-hidden="true"></i>
              </span>
            </dd>
          </div>
          <div class="trow grand"><dt>Total</dt><dd data-total><?= $this->money($totals['total']) ?></dd></div>
        </dl>
        <p class="total-note" data-total-note><?= (int) $totals['count'] ?> itens · <?= $totals['percent'] ?>% de desconto aplicado</p>

        <fieldset class="pay">
          <legend>Forma de pagamento</legend>
          <div class="pay-opts">
            <label class="pay-opt"><input type="radio" name="pagamento" value="pix" checked><span class="pay-face"><i class="fa-light fa-qrcode" aria-hidden="true"></i>Pix</span></label>
            <label class="pay-opt"><input type="radio" name="pagamento" value="boleto"><span class="pay-face"><i class="fa-light fa-barcode" aria-hidden="true"></i>Boleto</span></label>
            <label class="pay-opt"><input type="radio" name="pagamento" value="cartao"><span class="pay-face"><i class="fa-light fa-credit-card" aria-hidden="true"></i>Cartão</span></label>
          </div>
        </fieldset>
        <p class="pay-note" data-pay-note><i class="fa-light fa-bolt" aria-hidden="true"></i><span>Aprovação imediata e sem taxas.</span></p>

        <button type="button" class="btn-primary" data-finish>
          <i class="fa-light fa-lock" aria-hidden="true"></i><span>Finalizar pedido</span><span class="amt" data-button-total><?= $this->money($totals['total']) ?></span>
        </button>
        <p class="cart-foot"><i class="fa-light fa-shield-check" aria-hidden="true"></i>Rascunho salvo · <?= $this->e($savedAt) ?></p>
      </div>

      <div class="cart-empty" data-cart-empty hidden>
        <span class="empty-ico" aria-hidden="true"><i class="fa-light fa-basket-shopping"></i></span>
        <p class="empty-title">Carrinho vazio</p>
        <p class="empty-text">Escolha produtos no catálogo para montar o pedido.</p>
        <button type="button" class="btn-ghost" data-cart-add-item><i class="fa-light fa-plus" aria-hidden="true"></i>Adicionar itens</button>
      </div>

      <div class="cart-success" data-cart-success role="status" tabindex="-1" hidden>
        <span class="success-ico" aria-hidden="true"><i class="fa-light fa-check"></i></span>
        <p class="success-eyebrow">Pedido confirmado</p>
        <p class="success-number" data-success-number>#<?= $this->e($draftNumber) ?></p>
        <p class="success-total"><span>Total</span><strong data-success-total><?= $this->money($totals['total']) ?></strong></p>
        <p class="success-note" data-success-note>Pix · pedido enviado para o financeiro.</p>
        <button type="button" class="btn-primary" data-cart-reset><i class="fa-light fa-rotate-left" aria-hidden="true"></i><span>Novo pedido</span></button>
        <p class="cart-foot"><i class="fa-light fa-envelope" aria-hidden="true"></i>Comprovante enviado para o cliente.</p>
      </div>
    </aside>
  </div>

  <p class="sr-only" data-announce role="status" aria-live="polite"></p>
</section>
```

### CSS

```css
/* Contrato visual do OrderBuilder. Os tokens vêm de tokens.css. */
.ob-card{background:var(--ttsc-surface);border:1px solid var(--ttsc-border);border-radius:var(--ttsc-radius-surface);box-shadow:var(--ttsc-shadow-sm);padding:var(--ttsc-space-4);min-width:0}
.ob-head{display:flex;align-items:flex-start;justify-content:space-between;gap:var(--ttsc-space-4);margin-bottom:var(--ttsc-widget-gap)}
.ob-title{margin:0;font-size:17px;line-height:24px;font-weight:600;letter-spacing:-.01em;color:var(--ttsc-text)}
.ob-sub{margin:2px 0 0;font-size:12px;line-height:16px;color:var(--ttsc-text-muted)}
.ob-icon,.cart-ico{display:grid;place-items:center;border:1px solid var(--ttsc-accent-border);background:var(--ttsc-accent-soft);color:var(--ttsc-accent-text);border-radius:11px}
.ob-body{display:grid;grid-template-columns:minmax(0,1fr) 384px;gap:var(--ttsc-widget-gap);align-items:stretch}
.ob-catalog{display:flex;flex-direction:column;gap:10px;min-width:0}
.ob-search{display:flex;align-items:center;gap:var(--ttsc-space-2);height:34px;padding:0 9px;border:1px solid var(--ttsc-border);border-radius:10px;background:var(--ttsc-canvas-2)}
.ob-search:focus-within{border-color:var(--ttsc-accent-border);background:var(--ttsc-surface);box-shadow:0 0 0 3px var(--ttsc-accent-soft)}
.ob-search input{flex:1;min-width:0;border:0;background:transparent;font:inherit;font-size:12px;color:var(--ttsc-text);outline:none}
.chips{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none}
.chip{height:26px;padding:0 10px;border:1px solid var(--ttsc-border);border-radius:var(--ttsc-radius-pill);background:var(--ttsc-surface);font-size:11px;color:var(--ttsc-text-2);cursor:pointer}
.chip[aria-pressed="true"]{background:var(--ttsc-accent-soft);border-color:var(--ttsc-accent-border);color:var(--ttsc-accent-text)}
.prod-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;min-width:0}
.prod{display:grid;grid-template-columns:32px minmax(0,1fr);gap:9px;padding:10px;border:1px solid var(--ttsc-border);border-radius:12px;background:var(--ttsc-surface);text-align:left;font:inherit;color:inherit;cursor:pointer}
.prod:hover{border-color:var(--ttsc-accent-border);background:color-mix(in srgb,var(--ttsc-accent) 4%,var(--ttsc-surface))}
.prod-name{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:12.5px;font-weight:600;color:var(--ttsc-text)}
.prod-desc{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-top:1px;font-size:10.5px;line-height:13.5px;color:var(--ttsc-text-muted)}
.prod-foot{display:flex;align-items:center;gap:6px;margin-top:6px}
.prod-price{font-size:12px;font-weight:600;color:var(--ttsc-text);font-variant-numeric:tabular-nums}
.avail{display:inline-flex;align-items:center;gap:3px;margin-left:auto;font-size:9px;color:var(--ttsc-text-muted)}
.avail.ok i{color:var(--ttsc-success)}.avail.warn i{color:var(--ttsc-warning)}.avail.info i{color:var(--ttsc-info)}
.ob-cart{display:flex;flex-direction:column;padding:14px;border:1px solid var(--ttsc-border-soft);border-radius:14px;background:var(--ttsc-canvas-2);background-image:linear-gradient(180deg,color-mix(in srgb,var(--ttsc-accent) 5%,transparent),transparent 130px);min-width:0}
.cart-head{display:flex;justify-content:space-between;align-items:center;gap:8px;padding-bottom:9px;border-bottom:1px dashed var(--ttsc-border-strong)}
.cart-items{list-style:none;margin:0;padding:0}
.ci{display:grid;grid-template-columns:28px minmax(0,1fr) auto;grid-template-rows:auto auto;gap:5px 8px;padding:9px 0;border-bottom:1px dashed var(--ttsc-border)}
.ci-qty{grid-column:2;grid-row:2;display:inline-flex;align-items:center;height:24px;border:1px solid var(--ttsc-border);border-radius:7px;background:var(--ttsc-surface)}
.ci-qty button{width:24px;height:100%;border:0;background:transparent;color:var(--ttsc-text-muted);cursor:pointer}
.ci-qty .n{width:24px;text-align:center;font-size:10.5px;font-weight:600;font-variant-numeric:tabular-nums}
.ci-line{grid-column:3;grid-row:1;font-size:11.5px;font-weight:600;font-variant-numeric:tabular-nums}
.ci-remove{grid-column:3;grid-row:2;width:24px;height:24px;border:0;background:transparent;color:var(--ttsc-text-muted);cursor:pointer}
.cart-totals .grand{border-top:1px solid var(--ttsc-border);margin-top:3px;padding-top:5px}
.cart-totals .grand dd{font-size:19px;font-weight:700;letter-spacing:-.02em}
.pay-opts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:5px}
.pay-opt{position:relative}
.ob-card .pay-opt>input[type="radio"]{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;margin:0!important;opacity:0;cursor:pointer;z-index:1}
.pay-face{display:flex;align-items:center;justify-content:center;gap:4px;height:29px;border:1px solid var(--ttsc-border);border-radius:8px;background:var(--ttsc-surface);font-size:10.5px;font-weight:600;color:var(--ttsc-text-muted)}
.pay-opt input:checked + .pay-face{background:var(--ttsc-accent-soft);border-color:var(--ttsc-accent-border);color:var(--ttsc-accent-text)}
.pay-opt input:focus-visible + .pay-face{outline:2px solid var(--ttsc-accent);outline-offset:2px}
.btn-primary{display:flex;align-items:center;gap:7px;width:100%;height:37px;margin-top:10px;padding:0 12px;border:0;border-radius:10px;background:linear-gradient(135deg,var(--ttsc-accent),var(--ttsc-accent-hover));color:var(--ttsc-accent-on);font:inherit;font-size:12.5px;font-weight:700;cursor:pointer}
.btn-primary .amt{margin-left:auto;padding-left:10px;border-left:1px solid color-mix(in srgb,var(--ttsc-accent-on) 24%,transparent);font-variant-numeric:tabular-nums}
.cart-empty,.cart-success{display:flex;flex:1;flex-direction:column;align-items:center;justify-content:center;gap:5px;text-align:center;padding:18px 10px}
.cart-empty[hidden],.cart-success[hidden]{display:none}
@media (max-width:900px){.ob-body{grid-template-columns:minmax(0,1fr)}}
@media (max-width:760px){.ob-head{flex-direction:column;align-items:stretch}}
@media (max-width:560px){.prod-grid{grid-template-columns:minmax(0,1fr)}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important}}
```

### JS

```js
// assets/js/core/ttsc.order-builder.js — sem dependências.
(function (window, document) {
  'use strict';

  var instances = new WeakMap();

  function money(cents) {
    return (cents / 100).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  }

  function OrderBuilder(el, options) {
    this.el = el;
    this.options = Object.assign({ maxQty: 9, discount: 0, payment: 'pix', catalog: [], items: [] }, options || {});
    this.state = { items: this.options.items.slice(), discount: this.options.discount, payment: this.options.payment, status: 'draft', orderId: null };
    this.bind();
    this.render();
  }

  OrderBuilder.prototype.byId = function (id) {
    return this.options.catalog.find(function (p) { return p.id === id; });
  };

  OrderBuilder.prototype.addItem = function (id, qty) {
    var product = this.byId(id);
    if (!product) return null;
    var row = this.state.items.find(function (i) { return i.id === id; });
    if (row) row.qty = Math.min(this.options.maxQty, row.qty + (qty || 1));
    else this.state.items.push({ id: id, qty: Math.min(this.options.maxQty, qty || 1) });
    this.emit('order:add', { item: product });
    this.render();
    return this.getState().items.find(function (i) { return i.id === id; });
  };

  OrderBuilder.prototype.removeItem = function (id) {
    this.state.items = this.state.items.filter(function (i) { return i.id !== id; });
    this.emit('order:remove', { id: id });
    this.render();
    return true;
  };

  OrderBuilder.prototype.setQuantity = function (id, qty) {
    if (qty <= 0) return this.removeItem(id);
    var row = this.state.items.find(function (i) { return i.id === id; });
    if (!row) return null;
    row.qty = Math.max(1, Math.min(this.options.maxQty, Number(qty) || 1));
    this.emit('order:quantity', { id: id, qty: row.qty });
    this.render();
    return row;
  };

  OrderBuilder.prototype.getTotals = function () {
    var items = this.state.items.map(function (row) {
      var p = this.byId(row.id);
      return { id: row.id, name: p.name, unitPrice: p.price, qty: row.qty, lineTotal: p.price * row.qty };
    }, this);
    var subtotal = items.reduce(function (sum, i) { return sum + i.lineTotal; }, 0);
    var discount = Math.round(subtotal * this.state.discount / 100);
    return { count: items.reduce(function (n, i) { return n + i.qty; }, 0), subtotal: subtotal, discount: discount, total: subtotal - discount, items: items };
  };

  OrderBuilder.prototype.reset = function () {
    this.state.items = [];
    this.state.discount = 0;
    this.state.payment = 'pix';
    this.state.status = 'draft';
    this.state.orderId = null;
    this.emit('order:reset');
    this.render();
    this.focus(this.el.querySelector('[data-cart-add-item]'));
  };

  OrderBuilder.prototype.destroy = function () {
    this.el.removeEventListener('click', this.onClick);
    this.el.removeEventListener('change', this.onChange);
    instances.delete(this.el);
  };

  OrderBuilder.prototype.emit = function (name, detail) {
    this.el.dispatchEvent(new CustomEvent(name, { bubbles: true, detail: Object.assign({ totals: this.getTotals() }, detail) }));
  };

  OrderBuilder.prototype.render = function () {
    var totals = this.getTotals();
    var isEmpty = totals.count === 0;
    this.el.querySelector('[data-cart-core]').hidden = isEmpty || this.state.status === 'success';
    this.el.querySelector('[data-cart-empty]').hidden = !isEmpty;
    this.el.querySelector('[data-cart-success]').hidden = this.state.status !== 'success';
    this.el.querySelector('[data-subtotal]').textContent = money(totals.subtotal);
    this.el.querySelector('[data-total]').textContent = money(totals.total);
    this.el.querySelector('[data-button-total]').textContent = money(totals.total);
    this.el.querySelector('[data-discount-amount]').textContent = totals.discount ? '−' + money(totals.discount) : money(0);
    var items = this.el.querySelector('[data-cart-items]');
    items.innerHTML = totals.items.map(function (i) { return this.itemHTML(i); }, this).join('');
    this.el.querySelector('[data-cart-count]').hidden = isEmpty || this.state.status === 'success';
    this.el.querySelector('[data-cart-count]').textContent = String(totals.count);
    this.el.querySelectorAll('.prod').forEach(function (card) {
      var row = totals.items.find(function (i) { return i.id === card.dataset.id; });
      card.classList.toggle('in-cart', Boolean(row));
      var badge = card.querySelector('.prod-in');
      if (badge) badge.textContent = row ? row.qty + ' no pedido' : '';
    }, this);
  };

  OrderBuilder.prototype.itemHTML = function (item) {
    return '<li class="ci" data-id="' + item.id + '"><div class="ci-main"><p class="ci-name"><span>' + item.name + '</span></p><p class="ci-unit">' + money(item.unitPrice) + ' cada</p></div>' +
      '<span class="ci-line">' + money(item.lineTotal) + '</span>' +
      '<div class="ci-qty" role="group" aria-label="Quantidade de ' + item.name + '">' +
      '<button type="button" data-act="dec" data-id="' + item.id + '" aria-label="Diminuir quantidade de ' + item.name + '"' + (item.qty <= 1 ? ' disabled' : '') + '>−</button>' +
      '<span class="n">' + item.qty + '</span>' +
      '<button type="button" data-act="inc" data-id="' + item.id + '" aria-label="Aumentar quantidade de ' + item.name + '"' + (item.qty >= this.options.maxQty ? ' disabled' : '') + '>+</button></div>' +
      '<button type="button" class="ci-remove" data-act="remove" data-id="' + item.id + '" aria-label="Remover ' + item.name + ' do pedido">×</button></li>';
  };

  OrderBuilder.prototype.announce = function (message) {
    var live = this.el.querySelector('[data-announce]');
    live.textContent = '';
    window.requestAnimationFrame(function () { live.textContent = message; });
  };

  OrderBuilder.prototype.focus = function (node) {
    if (node) node.focus({ preventScroll: true });
  };

  OrderBuilder.prototype.bind = function () {
    var self = this;
    this.onClick = function (event) {
      var product = event.target.closest('.prod');
      if (product) { self.addItem(product.dataset.id); self.announce('Item adicionado ao pedido.'); return; }
      var action = event.target.closest('[data-act]');
      if (action) {
        var id = action.dataset.id;
        if (action.dataset.act === 'remove') self.removeItem(id);
        else {
          var row = self.state.items.find(function (i) { return i.id === id; });
          self.setQuantity(id, row.qty + (action.dataset.act === 'inc' ? 1 : -1));
        }
        self.focus(self.el.querySelector('[data-act="' + action.dataset.act + '"][data-id="' + id + '"]'));
        return;
      }
      if (event.target.closest('[data-cart-add-item]')) self.el.querySelector('[data-catalog-search]').focus();
    };
    this.onChange = function (event) {
      if (event.target.matches('[data-discount]')) {
        self.state.discount = Number(event.target.value);
        self.render();
      }
      if (event.target.matches('input[name="pagamento"]')) self.state.payment = event.target.value;
    };
    this.el.addEventListener('click', this.onClick);
    this.el.addEventListener('change', this.onChange);
  };

  window.TTSCOrderBuilder = {
    init: function (el, options) {
      if (!el) return null;
      if (instances.has(el)) return instances.get(el);
      var instance = new OrderBuilder(el, options);
      instances.set(el, instance);
      return instance;
    }
  };
})(window, document);
```

O modelo acima é o esqueleto mínimo: a versão do preview acrescenta a busca, os chips, o estado confirmado, o anúncio por `role="status"` e a integração com `fetch`. Ao criar o pedido, envie apenas `client_uuid`, `items[{product_uuid, qty}]`, `discount_percent` e `payment_method`; o servidor recalcula os valores.

### SQL

As tabelas `clients` e `crm_products` existem no repositório. As tabelas `sales_orders`, `sales_order_items` e `sales_payments` são **DDL nova** deste modelo e precisam de migration. A coluna `billing_cycle` também é uma extensão sugerida para `crm_products`.

```sql
-- Extensão do catálogo (nova): ciclo de cobrança exibido no cartão.
ALTER TABLE crm_products
  ADD COLUMN billing_cycle ENUM('monthly', 'one_time', 'per_class') NOT NULL DEFAULT 'one_time' AFTER category;

-- DDL nova: pedido de venda.
CREATE TABLE sales_orders (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE,
  tenant_id CHAR(36) NOT NULL,
  client_uuid CHAR(36) NOT NULL,
  number VARCHAR(20) NOT NULL,
  status ENUM('draft', 'confirmed', 'invoiced', 'cancelled') NOT NULL DEFAULT 'draft',
  subtotal DECIMAL(15,2) NOT NULL DEFAULT 0.00,
  discount_percent DECIMAL(5,2) NOT NULL DEFAULT 0.00,
  discount_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00,
  total DECIMAL(15,2) NOT NULL DEFAULT 0.00,
  payment_method ENUM('pix', 'boleto', 'cartao') NOT NULL,
  notes VARCHAR(500) NULL,
  created_by_user_id BIGINT UNSIGNED NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  deleted_at DATETIME NULL,
  UNIQUE KEY uq_sales_orders_number (tenant_id, number),
  KEY idx_sales_orders_client (client_uuid, status),
  CONSTRAINT fk_sales_orders_client FOREIGN KEY (client_uuid) REFERENCES clients (uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE sales_order_items (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE,
  order_uuid CHAR(36) NOT NULL,
  product_uuid CHAR(36) NOT NULL,
  product_name VARCHAR(255) NOT NULL,
  billing_cycle ENUM('monthly', 'one_time', 'per_class') NOT NULL,
  unit_price DECIMAL(15,2) NOT NULL,
  quantity SMALLINT UNSIGNED NOT NULL,
  line_total DECIMAL(15,2) NOT NULL,
  created_at DATETIME NOT NULL,
  KEY idx_sales_items_order (order_uuid),
  CONSTRAINT fk_sales_items_order FOREIGN KEY (order_uuid) REFERENCES sales_orders (uuid) ON DELETE CASCADE,
  CONSTRAINT fk_sales_items_product FOREIGN KEY (product_uuid) REFERENCES crm_products (uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE sales_payments (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE,
  order_uuid CHAR(36) NOT NULL,
  method ENUM('pix', 'boleto', 'cartao') NOT NULL,
  status ENUM('pending', 'authorized', 'paid', 'failed', 'refunded') NOT NULL DEFAULT 'pending',
  amount DECIMAL(15,2) NOT NULL,
  due_date DATE NULL,
  paid_at DATETIME NULL,
  gateway_reference VARCHAR(120) NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  KEY idx_sales_payments_order (order_uuid, status),
  CONSTRAINT fk_sales_payments_order FOREIGN KEY (order_uuid) REFERENCES sales_orders (uuid) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 1. Clientes do seletor.
SELECT c.uuid, c.trade_name, c.legal_name
FROM clients c
WHERE c.deleted_at IS NULL AND c.status = 'active'
ORDER BY COALESCE(c.trade_name, c.legal_name);

-- 2. Catálogo do tenant (preço sempre do banco).
SELECT p.uuid, p.name, p.description, p.category, p.unit_price, p.billing_cycle
FROM crm_products p
WHERE p.tenant_id = :tenant_uuid
  AND p.is_active = 1
  AND p.deleted_at IS NULL
ORDER BY p.category, p.name;

-- 3. Criação do pedido em transação; o total é recalculado aqui, nunca recebido pronto.
START TRANSACTION;

INSERT INTO sales_orders
  (uuid, tenant_id, client_uuid, number, status, discount_percent, payment_method, created_at, updated_at)
VALUES
  (:order_uuid, :tenant_uuid, :client_uuid, :number, 'draft', :discount_percent, :payment_method, NOW(), NOW());

INSERT INTO sales_order_items
  (uuid, order_uuid, product_uuid, product_name, billing_cycle, unit_price, quantity, line_total, created_at)
SELECT
  :item_uuid, :order_uuid, p.uuid, p.name, p.billing_cycle,
  p.unit_price, :quantity, p.unit_price * :quantity, NOW()
FROM crm_products p
WHERE p.uuid = :product_uuid
  AND p.tenant_id = :tenant_uuid
  AND p.is_active = 1
  AND p.deleted_at IS NULL;

UPDATE sales_orders o
SET
  subtotal = (SELECT COALESCE(SUM(i.line_total), 0) FROM sales_order_items i WHERE i.order_uuid = o.uuid),
  discount_amount = ROUND((SELECT COALESCE(SUM(i.line_total), 0) FROM sales_order_items i WHERE i.order_uuid = o.uuid) * :discount_percent / 100, 2),
  total = (SELECT COALESCE(SUM(i.line_total), 0) FROM sales_order_items i WHERE i.order_uuid = o.uuid)
          - ROUND((SELECT COALESCE(SUM(i.line_total), 0) FROM sales_order_items i WHERE i.order_uuid = o.uuid) * :discount_percent / 100, 2),
  status = 'confirmed',
  updated_at = NOW()
WHERE o.uuid = :order_uuid AND o.status = 'draft' AND o.deleted_at IS NULL;

INSERT INTO sales_payments
  (uuid, order_uuid, method, status, amount, due_date, created_at, updated_at)
SELECT :payment_uuid, o.uuid, o.payment_method, 'pending', o.total,
       CASE WHEN o.payment_method = 'boleto' THEN DATE_ADD(CURDATE(), INTERVAL 5 DAY) ELSE NULL END,
       NOW(), NOW()
FROM sales_orders o
WHERE o.uuid = :order_uuid;

COMMIT;

-- 4. Leitura do pedido confirmado.
SELECT o.number, o.status, o.subtotal, o.discount_percent, o.discount_amount, o.total, o.payment_method,
       i.product_name, i.quantity, i.unit_price, i.line_total
FROM sales_orders o
JOIN sales_order_items i ON i.order_uuid = o.uuid
WHERE o.uuid = :order_uuid
  AND o.tenant_id = :tenant_uuid
  AND o.deleted_at IS NULL;
```

O desconto máximo deve ser validado no servidor (por exemplo, 10%), assim como a quantidade por item e o cliente ativo do tenant. O `number` é gerado na mesma transação para não repetir. Nenhum dado sensível do cliente entra no payload do componente.
