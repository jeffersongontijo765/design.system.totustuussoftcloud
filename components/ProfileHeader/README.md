# ProfileHeader

Cabeçalho de perfil de uma pessoa: foto (ou iniciais), nome, papel e vínculo, etiquetas de situação e três indicadores. Usado na ficha do aluno, do professor ou do responsável.

## Quando usar

- Topo da ficha de um aluno, professor ou responsável, com o resumo antes das abas de detalhe.
- Quando a pessoa tem situação e indicadores que a secretaria confere logo ao abrir a ficha.
- Não use para listas de pessoas: para isso, use [TeamMemberCard](../TeamMemberCard/README.md).

## Anatomia

```
[ faixa de capa ]
(AS)  Ana Souza                          [Editar dados]
      Aluna · 2º ano B · Matrícula 2027
      [Matrícula ativa] [Turno da manhã]
─────────────────────────────────────────────
  92% Frequência │ 8,4 Média │ Em dia Mensalidades
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Contêiner | `section.ph` | sim |
| Capa | `.ph-cover` (decorativa, `aria-hidden`) | não |
| Avatar | `.ph-avatar` com iniciais ou `img` | sim |
| Nome e papel | `h2.ph-name`, `.ph-role` | sim |
| Situação | `.ph-tags` com `.pill` | recomendado |
| Indicadores | `.ph-stats > div` com `b` e `span` | recomendado |
| Ação | `.ph-acts` | não |

## Variantes / Estados

- **Com foto:** troque as iniciais por `<img>` com `alt` com o nome da pessoa.
- **Sem indicadores:** remova `.ph-stats`.
- **Pendência:** a etiqueta `pill-warn` mostra o que falta (documento, mensalidade).

## API

| Atributo | Efeito |
|---|---|
| `h2.ph-name` | nome da pessoa, usado como título da seção |

## Acessibilidade

- O nome é `h2` dentro de `section` com `aria-labelledby`.
- A capa e as iniciais decorativas são `aria-hidden`; o nome já está no texto.
- Os indicadores são `div` com número e rótulo; o rótulo precisa vir junto do número.

## Modelos

### HTML

```html
<section class="ph" aria-labelledby="ph-t">
  <div class="ph-cover" aria-hidden="true"></div>
  <div class="ph-body">
    <span class="ph-avatar" aria-hidden="true">AS</span>
    <div>
      <h2 id="ph-t" class="ph-name">Ana Souza</h2>
      <div class="ph-role">Aluna · 2º ano B</div>
      <div class="ph-tags"><span class="pill pill-ok">Matrícula ativa</span></div>
    </div>
  </div>
  <div class="ph-stats"><div><b>92%</b><span>Frequência</span></div></div>
</section>
```

### CSS

Classes `.ph*`. Em telas menores o avatar e o texto empilham.

### JS

Sem JavaScript próprio. Os dados vêm da ficha da pessoa (ver SQL).

### SQL

Ficha do aluno com a situação da matrícula e a frequência do período:

```sql
SELECT u.name AS nome, c.name AS curso, e.status AS situacao,
       ROUND(100 * SUM(a.status = 'present') / NULLIF(COUNT(a.id), 0), 1) AS frequencia
FROM users u
JOIN enrollments e ON e.student_uuid = u.uuid AND e.deleted_at IS NULL
JOIN courses c ON c.uuid = e.course_uuid
LEFT JOIN attendance a ON a.enrollment_uuid = e.uuid
WHERE u.uuid = ? AND u.tenant_id = ?
GROUP BY u.id, u.name, c.name, e.status;
```

## Faça / Não faça

- Faça: mostre a situação da matrícula logo abaixo do nome.
- Faça: use no máximo três indicadores.
- Não faça: mostrar dados sensíveis (CPF, saúde) no cabeçalho.
