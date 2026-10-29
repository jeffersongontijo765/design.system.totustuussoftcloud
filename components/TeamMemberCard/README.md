# TeamMemberCard

Cartão de uma pessoa da equipe (professor, coordenador, atendente), com foto ou iniciais, nome, função, indicador de disponibilidade e contato. Usado em listas do corpo docente e da equipe.

## Quando usar

- Listar professores de uma etapa, coordenadores ou atendentes com o contato de cada um.
- Mostrar quem está disponível para atendimento e quem está em licença.
- Para a ficha completa de uma pessoa, use [ProfileHeader](../ProfileHeader/README.md).

## Anatomia

```
(RP)● Rafael Pereira
       Matemática · 12 turmas
✉ rafael.pereira@escola.com
🕒 Atendimento: seg e qua
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Cartão | `article.tm` | sim |
| Avatar e disponibilidade | `.tm-av` com `.av` e `.dot` (`role="img"` + `aria-label`) | sim |
| Nome e função | `.tm-name`, `.tm-role` | sim |
| Contato e horário | `.tm-meta` com `span` | recomendado |

## Variantes / Estados

- **Disponível:** `.dot` verde (padrão).
- **Ausente / em licença:** `.dot.off` cinza, com o motivo escrito em `.tm-meta` (não só a cor).
- **Grade:** colunas automáticas, de 210 px de largura mínima.

## API

| Atributo | Efeito |
|---|---|
| `role="img"` + `aria-label` no `.dot` | estado em texto para leitores de tela |
| `.off` no `.dot` | estado ausente |

## Acessibilidade

- O estado de disponibilidade tem `aria-label` ("Disponível", "Em licença").
- O e-mail é link `mailto:` quando estiver dentro de um `a`.
- A grade é lista semântica quando houver muitas pessoas (use `ul`/`li` no lugar de `div`).

## Modelos

### HTML

```html
<article class="tm">
  <div class="tm-top">
    <span class="tm-av">
      <span class="av" aria-hidden="true">RP</span>
      <span class="dot" role="img" aria-label="Disponível"></span>
    </span>
    <div><div class="tm-name">Rafael Pereira</div><div class="tm-role">Matemática · 12 turmas</div></div>
  </div>
  <div class="tm-meta"><span><i class="fa-light fa-envelope" aria-hidden="true"></i>rafael.pereira@escola.com</span></div>
</article>
```

### CSS

Classes `.tm*`. O indicador usa `--ttsc-success` e, ausente, `--ttsc-text-muted`.

### JS

Sem JavaScript próprio. A disponibilidade pode vir de um campo do cadastro ou do calendário de atendimento.

### SQL

Equipe do corpo docente ativa, com o número de turmas no período:

```sql
SELECT u.name AS nome, u.email, u.status,
       COUNT(DISTINCT c.id) AS turmas
FROM users u
LEFT JOIN class_subjects cs ON cs.teacher_uuid = u.uuid
LEFT JOIN classes c ON c.uuid = cs.class_uuid AND c.deleted_at IS NULL AND c.period_uuid = ?
WHERE u.tenant_id = ? AND u.deleted_at IS NULL
GROUP BY u.id, u.name, u.email, u.status
ORDER BY u.name;
```

## Faça / Não faça

- Faça: mostre o contato institucional, não o pessoal.
- Faça: escreva o motivo da ausência ("Em licença até 15/03").
- Não faça: colocar CPF, telefone pessoal ou endereço no cartão.
