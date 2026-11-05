# Arquitetura de JavaScript — componentes vs. páginas

> Regra que evita o problema nº 1 deste sistema: **um renderizador único para
> todas as páginas**. Foi assim que 574 de 576 telas passaram a ser o mesmo
> documento com dados trocados.

## O erro a não repetir

O padrão atual do repositório:

```html
<main data-model="page" data-model-tab="table"> … </main>
<script src="components/bundle.js"></script>
```

`TTSCModelKit.render(ficha)` lê `models/<modulo>.json` e **constrói a página
inteira**. Consequências medidas:

- 574/576 páginas com `data-model-*`;
- 92% de similaridade estrutural média entre páginas;
- 165 KB por página (o mesmo HTML gerado, com dados diferentes);
- 966 KB de JavaScript carregados em toda tela;
- qualquer variação de layout exige mexer no renderizador — então ninguém varia.

## O modelo correto

### 1. Componente = comportamento reutilizável

Um módulo por comportamento, sem conhecer a página:

```js
// components/Modal/modal.js
export function openModal(el) { … }
export function closeModal(el) { … }
```

- Não lê `models/*.json`.
- Não decide layout: recebe o elemento já no DOM.
- Pode ser carregado sob demanda (`import()`), conforme o componente aparece.

### 2. Página = template próprio

O HTML da página é escrito para **aquela** tela (server-rendered). O layout vem
das classes `ttsc-*` e dos primitivos, não de um renderizador genérico.

Proibido em página nova: `data-model`, `data-model-api`, `data-model-view`,
`data-model-tab`, `data-model-refresh` — são marcadores do renderizador.

### 3. Controller = o que só aquela página faz

```js
// paginas/referencia/assets/registros.js
import { initTable } from "../../../components/Table/table.js";
import { initDrawer } from "../../../components/Drawer/drawer.js";

initTable(document.querySelector("[data-table]"));
initDrawer(document.querySelector("#drawer-filtros"));
```

Orçamento: **≤ 8 KB por controller**. Se passar, o comportamento pertence a um
componente, não à página.

## Regras verificáveis

| ID | Regra |
|---|---|
| R16 | Página não pode conter atributos `data-model*` (renderizador genérico). |
| R17 | Página não pode ter `<script>` inline com código. |
| R18 | Script de página deve ser `type="module"` e externo. |
| R19 | Controller de página ≤ 8 KB. |

## Quando a ficha de dados pode existir

Ficha (`models/*.json`) serve para **conteúdo**: rótulos, campos, valores de
exemplo, configuração de colunas. Nunca para:

- escolher o arquétipo da página;
- decidir quais blocos aparecem;
- montar o HTML.

Se a ficha decide o layout, você recriou o renderizador único com outro nome.

## Migração das 576 páginas existentes

1. Escolher um módulo piloto (ex.: `academico/matriculas`).
2. Escrever o template à mão, com `page-spec`, usando os blocos aprovados.
3. Mover o comportamento para controllers pequenos.
4. Comparar com a versão gerada; só então substituir as demais telas do módulo.
5. Remover `data-model-*` do módulo migrado e rodar `npm run ds:check`.
