# ChecklistGrid

Grade de verificações de um processo (fechamento, início de semestre, auditoria) com estado por item, responsável e uma barra de conclusão no topo.

## Quando usar

- Fechamento mensal, abertura de período, checagens antes de publicar notas ou boletos.
- Quando cada item tem um dono e um estado, e o total de concluídos é o que a gestão acompanha.
- Para um processo linear com ordem obrigatória, use [Stepper](../Stepper/README.md).

## Anatomia

```
Concluídas                                     6 de 9
██████████████████████░░░░░░░░░░

[✓] Frequência lançada       [✓] Cobranças geradas
[⏱] Conciliação bancária     [○] Turmas sem chamada
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Cabeçalho de progresso | `.check-head` com `.check-track > i` (`--p`) | sim |
| Grade | `.checks` | sim |
| Item | `.check` com `.done`, `.wait` ou nenhum (pendente) | sim |
| Ícone de estado | `.check-ic` | sim |
| Título e responsável | `.check-title`, `.check-meta` | sim |

## Variantes / Estados

- **Concluído:** `.done`, ícone de check, tom verde.
- **Aguardando:** `.wait`, ícone de relógio, tom amarelo (depende de outra pessoa ou de dados).
- **Pendente:** sem classe, ícone de círculo.

## API

| Atributo | Efeito |
|---|---|
| `role="progressbar"` + `aria-valuenow` no trilho | progresso lido por leitores de tela |
| `--p` no `i` | largura da barra (concluídos / total × 100) |
| Classe de estado no `.check` | estado do item |

## Acessibilidade

- O estado aparece em texto ("Concluído por…", "Pendente: …") e no ícone com `aria-hidden`.
- O progresso tem `role="progressbar"` com valores e rótulo.

## Modelos

### HTML

```html
<div class="check-track" role="progressbar" aria-valuemin="0" aria-valuemax="9" aria-valuenow="6" aria-label="Itens concluídos: 6 de 9">
  <i style="--p:67"></i>
</div>
<div class="checks">
  <div class="check done">
    <span class="check-ic"><i class="fa-light fa-check" aria-hidden="true"></i></span>
    <div><div class="check-title">Frequência lançada</div><div class="check-meta">Concluído por Ana · 20/10</div></div>
  </div>
</div>
```

### CSS

Classes `.check*`. Os tons de estado usam `color-mix` com os tokens de sucesso e aviso.

### JS

```js
function atualizarProgresso(el, concluidos, total) {
  const pct = Math.round((concluidos / total) * 100);
  const trilho = el.querySelector('[role=progressbar]');
  trilho.setAttribute('aria-valuenow', concluidos);
  trilho.setAttribute('aria-valuemax', total);
  trilho.querySelector('i').style.setProperty('--p', pct);
}
```

### SQL

Turmas ativas sem chamada no dia (uma das verificações do exemplo):

```sql
SELECT COUNT(*) AS turmas_sem_chamada
FROM classes c
WHERE c.deleted_at IS NULL AND c.is_active = 1 AND c.period_uuid = ?
  AND NOT EXISTS (
    SELECT 1 FROM attendance a
    WHERE a.class_uuid = c.uuid AND a.lesson_date = CURDATE()
  );
```

## Faça / Não faça

- Faça: cada item com dono e prazo, visíveis no cartão.
- Faça: atualize o progresso a partir do estado real dos itens, não de um contador manual.
- Não faça: marcar como concluído um item que depende de outro sistema sem confirmação.
