# UnitGrid

Grade de unidades (salas, mesas, leitos, docas) em que cada célula mostra o nome, o estado e um detalhe, com cor por estado. Dá uma visão de ocupação de uma só vez.

## Quando usar

- Salas e laboratórios por turno, auditórios por dia, veículos ou docas em uma operação.
- Quando o estado de cada unidade importa e a quantidade cabe em uma tela (até cerca de 60 células).
- Para a planta real de um prédio, use uma imagem com marcadores; esta grade é para listas.

## Anatomia

```
┌────────────┐ ┌────────────┐ ┌────────────┐
│ Sala 101   │ │ Sala 102   │ │ Lab. 1     │
│ Ocupada    │ │ Livre      │ │ Livre      │
└────────────┘ └────────────┘ └────────────┘
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Grade | `.units` com `role="list"` | sim |
| Célula | `.unit` com `role="listitem"` e `aria-label` | sim |
| Estado | `.unit-free`, `.unit-busy`, `.unit-res`, `.unit-maint` | sim |
| Nome e detalhe | `b` e `small` | sim |
| Legenda | `.legend` | recomendado |

## Variantes / Estados

- **Livre:** verde.
- **Ocupada:** vermelho.
- **Reservada:** amarelo, com o horário da reserva no detalhe.
- **Em manutenção:** borda tracejada e texto apagado. Não conta como ocupada nem livre.

## API

| Atributo | Efeito |
|---|---|
| Classe de estado no `.unit` | cor e significado |
| `aria-label` no `.unit` | texto completo da célula para leitores de tela |

## Acessibilidade

- O estado está escrito em texto ("Livre", "Ocupada"), não só na cor.
- Cada célula tem `aria-label` com nome, estado e capacidade.
- A legenda é `aria-hidden` porque o texto de cada célula já diz o estado.

## Modelos

### HTML

```html
<div class="units" role="list">
  <div class="unit unit-busy" role="listitem" aria-label="Sala 101, ocupada, 32 lugares">
    <b>Sala 101</b><small>Ocupada · 32 lugares</small>
  </div>
  <div class="unit unit-free" role="listitem" aria-label="Sala 102, livre, 32 lugares">
    <b>Sala 102</b><small>Livre · 32 lugares</small>
  </div>
</div>
```

### CSS

Classes `.units`, `.unit`, `.unit-*`. As cores usam `color-mix` com os tokens de estado, então funcionam no escuro.

### JS

```js
const ESTADO = { livre: 'unit-free', ocupada: 'unit-busy', reservada: 'unit-res', manutencao: 'unit-maint' };

function renderUnits(el, unidades) {
  el.replaceChildren(...unidades.map((u) => {
    const div = document.createElement('div');
    div.className = 'unit ' + ESTADO[u.estado];
    div.setAttribute('role', 'listitem');
    div.setAttribute('aria-label', `${u.nome}, ${u.rotuloEstado}, ${u.capacidade} lugares`);
    div.innerHTML = '<b></b><small></small>';
    div.querySelector('b').textContent = u.nome;
    div.querySelector('small').textContent = `${u.rotuloEstado} · ${u.capacidade} lugares`;
    return div;
  }));
}
```

### SQL

Turmas ativas por turno e situação no período (para a visão de salas, use a tabela de reservas quando houver):

```sql
SELECT
  c.name AS turma,
  c.shift AS turno,
  c.max_students AS capacidade,
  CASE WHEN c.is_active = 1 THEN 'ativa' ELSE 'inativa' END AS situacao
FROM classes c
WHERE c.deleted_at IS NULL AND c.period_uuid = ?
ORDER BY c.shift, c.name;
```

## Faça / Não faça

- Faça: ordene por turno ou por andar e mantenha a mesma ordem em toda a tela.
- Faça: marque manutenção como estado próprio, não como ocupada.
- Não faça: usar mais de quatro estados; a legenda deixa de caber.
