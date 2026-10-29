# GalleryGrid

Grade de fotos em mosaico, com tamanhos variados, legenda curta e um contador "+N" para as fotos que não cabem. Cada foto é um botão que abre a visualização.

## Quando usar

- Fotos de eventos, feiras, excursões e atividades da escola.
- Um conjunto de imagens que pede um resumo visual, com a opção de ver todas.
- Para uma foto só, ou para visualizar uma foto em tamanho grande, use [Lightbox](../Lightbox/README.md) ao abrir o item.

## Anatomia

```
[ foto larga            ] [ foto  ] [ foto alta ]
[                       ] [ foto  ] [           ]
[ foto ] [ foto ] [ +12 ]
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Grade | `.gg` com `role="list"` | sim |
| Foto | `button.gg-item` com `role="listitem"` e `aria-label` | sim |
| Tamanho | `.wide` (duas colunas), `.tall` (duas linhas) | não |
| Legenda | `.gg-cap` | recomendado |
| Contador | `.gg-more` (último item) | não |

## Variantes / Estados

- **Foto larga / alta:** `.wide` ou `.tall`, para dar ritmo ao mosaico. Não use mais de um destaque por linha.
- **Contador:** o último item mostra "+N" quando há mais fotos do que as visíveis.
- **Foco:** o contorno de foco aparece no botão.

## API

| Atributo | Efeito |
|---|---|
| `aria-label` em cada `.gg-item` | descrição da foto para leitores de tela |
| `.wide` / `.tall` | tamanho no mosaico |

## Acessibilidade

- Cada foto é um `button` com `aria-label` com o assunto da foto; o botão abre a visualização.
- A grade é `role="list"`, então o número de itens é anunciado.
- O contador "+N" tem `aria-label` com "Ver mais N fotos".
- As fotos reais precisam de texto alternativo; o gradiente de exemplo é decorativo.

## Modelos

### HTML

```html
<div class="gg" role="list">
  <button class="gg-item wide" type="button" role="listitem" aria-label="Abrir foto: estande de robótica">
    <span class="gg-art" style="background-image:url(...)"></span>
    <span class="gg-cap">Estande de robótica</span>
  </button>
  <button class="gg-item" type="button" role="listitem" aria-label="Ver mais 12 fotos">
    <span class="gg-art"></span><span class="gg-more">+12</span>
  </button>
</div>
```

### CSS

Classes `.gg*`. Quatro colunas, duas em telas pequenas, com linhas de 110 px.

### JS

```js
function abrirFoto(index, fotos) {
  // abre o visualizador (Lightbox) a partir da foto clicada
  document.dispatchEvent(new CustomEvent('gallery:open', { detail: { index, fotos } }));
}
```

### SQL

Fotos de um evento na biblioteca de arquivos, do mais recente ao mais antigo:

```sql
SELECT f.uuid, f.file_name AS nome, f.size_bytes, f.created_at
FROM storage_files f
WHERE f.tenant_id = ? AND f.mime_type LIKE 'image/%' AND f.is_deleted = 0
  AND f.origin_entity_type = 'event' AND f.origin_entity_uuid = ?
ORDER BY f.created_at DESC
LIMIT 12;
```

## Faça / Não faça

- Faça: mostre no máximo 7 fotos e o contador com o total.
- Faça: dê um texto alternativo para cada foto real.
- Não faça: publicar foto de criança sem autorização e sem cuidado com a identificação.
