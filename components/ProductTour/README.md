# ProductTour

Cartão de passo a passo que aponta um elemento da tela e explica o que ele faz. Tem indicador de progresso, botões Voltar e Próximo e a saída "Pular tour".

## Quando usar

- Apresentar uma tela nova para secretaria, professores ou responsáveis no primeiro acesso.
- Explicar um fluxo de vários passos (matrícula, rematrícula) sem texto em excesso.
- Não use para mensagens de erro ou avisos: para isso, use [Toast](../Toast/README.md) ou [Alert](../Alert/README.md).

## Anatomia

```
[destaque na tela]
              ┌──────────────────────────┐
              │ Passo 2 de 4             │
              │ Filtre a fila por unidade│
              │ texto explicativo…       │
              │ ● ○ ○ ○                  │
              │ Pular tour   [Voltar][Próximo]│
              └──────────────────────────┘
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Destaque | `.tour-target` (o elemento real recebe o destaque) | sim |
| Cartão | `.tour` com `role="dialog"`, `aria-labelledby`, `aria-describedby` | sim |
| Progresso | `.tour-step` ("Passo 2 de 4") e `.tour-dots` | sim |
| Ações | `.tour-acts` com `.tour-btn` e `.tour-skip` | sim |

## Variantes / Estados

- **Primeiro passo:** sem "Voltar".
- **Último passo:** o botão "Próximo" vira "Concluir".
- **Pulado:** o tour fecha e não reaparece nessa conta.

## API

| Atributo | Efeito |
|---|---|
| `role="dialog"` + `aria-labelledby` / `aria-describedby` | nome e descrição do passo |
| `.on` em `.tour-dots i` | passo atual no indicador |

## Acessibilidade

- O cartão é um `dialog` nomeado; ao abrir, o foco vai para o primeiro botão.
- "Pular tour" é sempre visível e fica antes de "Próximo" na ordem de tabulação.
- O destaque visual não pode ser a única forma de saber qual elemento é; o texto do passo deve citá-lo.
- Respeite `prefers-reduced-motion` se houver animação de destaque.

## Modelos

### HTML

```html
<div class="tour" role="dialog" aria-labelledby="tr-h" aria-describedby="tr-p">
  <span class="tour-step">Passo 2 de 4</span>
  <h3 id="tr-h">Filtre a fila por unidade</h3>
  <p id="tr-p">Use o seletor de unidade para ver só os atendimentos da sua escola.</p>
  <div class="tour-acts">
    <button class="tour-skip" type="button">Pular tour</button>
    <div style="display:flex;gap:6px">
      <button class="tour-btn" type="button">Voltar</button>
      <button class="tour-btn primary" type="button">Próximo</button>
    </div>
  </div>
</div>
```

### CSS

Classes `.tour*`. O cartão usa `--ttsc-shadow-popover` e o destaque usa `--ttsc-accent`.

### JS

```js
const passos = [
  { alvo: '#filtro-unidade', titulo: 'Filtre a fila por unidade', texto: '...' },
];
let atual = 0;

function mostrarPasso(i) {
  const p = passos[i];
  document.querySelector('#tour-h').textContent = p.titulo;
  document.querySelector('#tour-p').textContent = p.texto;
  document.querySelector('#tour-passo').textContent = `Passo ${i + 1} de ${passos.length}`;
  document.querySelector(p.alvo)?.scrollIntoView({ block: 'center' });
}
```

### SQL

Sem consulta própria: o roteiro é configuração do módulo. Para saber quem já concluiu ou pulou o tour, guarde o estado no perfil do usuário (campo a definir no cadastro de preferências, não neste componente).

## Faça / Não faça

- Faça: no máximo cinco passos por tour.
- Faça: deixe sempre a saída "Pular tour".
- Não faça: bloquear a tela com o tour; o usuário precisa continuar usando o sistema.
