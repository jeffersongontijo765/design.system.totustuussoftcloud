# ArticleCard

Cartão de notícia ou artigo: imagem de capa, categoria, título (link), resumo curto e data com o tempo de leitura. Usado em listas de notícias, comunicados e a central de ajuda.

## Quando usar

- Notícias da escola, comunicados e avisos publicados para famílias e alunos.
- Artigos de uma central de ajuda ou de uma base de conhecimento.
- Para um aviso urgente, prefira um [Alert](../Alert/README.md) no topo da página.

## Anatomia

```
┌───────────────────────┐
│ [imagem de capa]      │
│ Eventos               │
│ Título do artigo (link)│
│ resumo em 2 linhas…   │
│ Autor        20/11 · 4 min│
└───────────────────────┘
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Cartão | `article.ar` | sim |
| Capa | `.ar-img` (decorativa, `aria-hidden`) | não |
| Categoria | `.ar-cat` | recomendado |
| Título | `h3.ar-title` com `a` | sim |
| Resumo | `.ar-sum` | recomendado |
| Metadados | `.ar-meta` com `time datetime` | sim |

## Variantes / Estados

- **Com capa:** imagem no topo; a altura é fixa (120 px) para manter as linhas alinhadas.
- **Sem capa:** remova `.ar-img`; o título sobe.
- **Grade:** três colunas, duas em telas médias, uma em telas pequenas.

## API

| Atributo | Efeito |
|---|---|
| `time[datetime]` | data legível pelo leitor e pelo navegador |
| `a` dentro de `h3` | o título inteiro é o link |

## Acessibilidade

- O título é um link, e o foco visível usa o contorno de acento.
- A capa é `aria-hidden`; a imagem real precisa de `alt` se for informativa.
- A data usa `time` com `datetime` (formato ISO), para ser lida corretamente.

## Modelos

### HTML

```html
<article class="ar">
  <div class="ar-img" aria-hidden="true"></div>
  <div class="ar-body">
    <span class="ar-cat">Eventos</span>
    <h3 class="ar-title"><a href="/noticias/feira-2026">Feira de Ciências 2026 reúne 40 projetos</a></h3>
    <p class="ar-sum">Estudantes apresentaram trabalhos de robótica, química e biologia.</p>
    <div class="ar-meta"><span>Secretaria de Comunicação</span><time datetime="2026-11-20">20/11/2026 · 4 min</time></div>
  </div>
</article>
```

### CSS

Classes `.ar*`. Três colunas acima de 880 px, duas acima de 560 px, uma abaixo.

### JS

Sem JavaScript. Os artigos vêm da base de conhecimento ou do cadastro de notícias (ver SQL).

### SQL

Artigos publicados e visíveis, do mais recente ao mais antigo:

```sql
SELECT a.uuid, a.title AS titulo, a.summary AS resumo, a.published_at AS publicado_em,
       a.access_count AS acessos
FROM sac_knowledge_articles a
WHERE a.tenant_id = ? AND a.status = 'published' AND a.visibility = 'public'
ORDER BY a.published_at DESC
LIMIT 6;
```

## Faça / Não faça

- Faça: use título com menos de 70 caracteres e um resumo de até duas linhas.
- Faça: mostre a data de publicação e o tempo de leitura.
- Não faça: colocar capa com texto dentro da imagem; o texto some em telas pequenas.
