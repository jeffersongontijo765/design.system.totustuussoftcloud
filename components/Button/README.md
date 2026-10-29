# Button

Botão de ação do chassi TotusTuus (`.ttsc-btn`), com seis variantes, três tamanhos, versão só-ícone e estado de carregamento.

> Também listado em: **Base › Buttons**.

## Quando usar

- Disparar uma ação na página: salvar, criar, exportar, abrir drawer/modal.
- Uma única ação **primary** por região (cabeçalho de página, rodapé de drawer, rodapé de modal).
- Para navegar para outra URL use [Link](../Link/README.md) (`<a class="ttsc-link">`), não um botão.

## Anatomia

```
[ ícone (opcional) ][ rótulo ]      .ttsc-btn + variante + tamanho
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Container | `button.ttsc-btn` ou `a.ttsc-btn` | sim |
| Variante | `ttsc-btn-primary` · `-secondary` · `-outline` · `-ghost` · `-destructive` · `-mono` · `-dim` | sim |
| Tamanho | `ttsc-btn-sm` · (padrão) · `ttsc-btn-lg` | não |
| Só ícone | `ttsc-btn-icon` + `aria-label` | não |
| Ícone | `<i class="fa-light fa-…">` antes do rótulo | não |

## Variantes

| Variante | Classe | Uso | Tokens |
|---|---|---|---|
| Primary | `ttsc-btn-primary` | Ação principal da região | fundo `ttsc-accent`, texto `ttsc-accent-on` (9,6:1), hover `ttsc-accent-hover` |
| Secondary | `ttsc-btn-secondary` | Ação alternativa | fundo `ttsc-surface-2`, texto `ttsc-text` |
| Outline | `ttsc-btn-outline` | Ações de toolbar (Exportar, Filtrar) | borda `ttsc-border`, fundo `ttsc-surface` |
| Ghost | `ttsc-btn-ghost` | Cancelar, ações terciárias, ícones em linhas de tabela | sem fundo; hover `ttsc-canvas-2` |
| Destructive | `ttsc-btn-destructive` | Excluir, revogar | fundo `ttsc-danger`, texto branco (4,8:1) |
| Mono | `ttsc-btn-mono` | Ênfase neutra (ex.: “Publicar” em telas de builder) | fundo `ttsc-text`, texto `ttsc-surface` |

## Estados

| Estado | Como aplicar |
|---|---|
| Hover / pressed | automático (CSS) |
| Foco | automático — contorno 2px `ttsc-accent` com offset 2px |
| Desabilitado | atributo `disabled` (em `<a>`, use `aria-disabled="true"` + `tabindex="-1"`) |
| Carregando | `disabled` + `aria-busy="true"` + troca do rótulo (ver JS) |

## API

Sem JavaScript obrigatório. Quando o botão abre outro componente, use o atributo do componente alvo:

| Atributo | Efeito |
|---|---|
| `data-ttsc-modal-toggle="#id"` | abre o [Modal](../Modal/README.md) |
| `data-ttsc-drawer-toggle="#id"` | abre o [Drawer](../Drawer/README.md) |
| `data-ttsc-dropdown-toggle="true"` | dentro de `[data-ttsc-dropdown]`, abre o [Dropdown](../Dropdown/README.md) |
| `data-ttsc-dismiss="#id"` | fecha/remove o alvo ([Dismiss](../Dismiss/README.md)) |

## Acessibilidade

- Use `<button type="button">` (ou `type="submit"` em formulários); nunca `<div onclick>`.
- Botão só-ícone **sempre** com `aria-label` (“Filtrar”, “Mais ações”).
- Rótulos são verbos no infinitivo, em pt-BR: “Salvar”, “Exportar”, “Nova matrícula”.
- Não use `ttsc-accent` como cor de texto em botões ghost/outline: fica em 2:1. Para texto verde use `ttsc-accent-text`.

## Modelos

### HTML

```html
<!-- Cabeçalho de página: uma primary + ações de toolbar -->
<div class="flex items-center gap-2">
  <button type="button" class="ttsc-btn ttsc-btn-outline">
    <i class="fa-light fa-arrow-down-to-line"></i> Exportar
  </button>
  <button type="button" class="ttsc-btn ttsc-btn-primary" data-ttsc-drawer-toggle="#drawer-enrollment">
    <i class="fa-light fa-plus"></i> Nova matrícula
  </button>
</div>

<!-- Só ícone em linha de tabela -->
<button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" aria-label="Editar matrícula">
  <i class="fa-light fa-pen"></i>
</button>

<!-- Rodapé de formulário -->
<div class="flex justify-end gap-2">
  <button type="button" class="ttsc-btn ttsc-btn-ghost" data-ttsc-drawer-dismiss="true">Cancelar</button>
  <button type="submit" class="ttsc-btn ttsc-btn-primary" data-loading-text="Salvando…">
    <i class="fa-light fa-floppy-disk"></i> <span>Salvar</span>
  </button>
</div>
```

### CSS

As classes vêm de `components/bundle.css` (runtime ttscui + ponte de tokens). Para customizar, altere **tokens**, nunca a classe:

```css
/* Ponte (já incluída em bundle.css): o botão primary lê --primary/--primary-foreground */
:root {
  --primary: var(--ttsc-accent);            /* #3ecf8e */
  --primary-foreground: var(--ttsc-accent-on); /* #0f0f0f */
}

/* Extensão do chassi: botão de largura total em drawers mobile */
.ttsc-btn-block { width: 100%; justify-content: center; }

/* Estado de carregamento com spinner Font Awesome */
.ttsc-btn[aria-busy="true"] i { animation: ttsc-spin 0.8s linear infinite; }
@keyframes ttsc-spin { to { transform: rotate(360deg); } }
```

### JS

```js
// assets/js/core/ttsc.button-loading.js — estado "carregando" para qualquer .ttsc-btn[data-loading-text]
export function setLoading(button, loading) {
  const label = button.querySelector('span') || button;
  if (loading) {
    button.dataset.originalText = label.textContent;
    label.textContent = button.dataset.loadingText || 'Processando…';
    button.disabled = true;
    button.setAttribute('aria-busy', 'true');
  } else {
    label.textContent = button.dataset.originalText || label.textContent;
    button.disabled = false;
    button.removeAttribute('aria-busy');
  }
}

// Formulário do CRUD genérico (DomainCrudController): trava o botão até a resposta
document.querySelectorAll('form[data-ttsc-crud]').forEach((form) => {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const submit = form.querySelector('[type="submit"]');
    setLoading(submit, true);
    try {
      const response = await fetch(form.action, {
        method: form.method || 'POST',
        body: new FormData(form),
        headers: { 'X-CSRF-Token': form.querySelector('[name="_token"]').value },
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
    } finally {
      setLoading(submit, false);
    }
  });
});
```

### SQL

O botão não guarda dados; ele **depende de permissão**. As ações de escrita do chassi seguem a cadeia `write_permission` → `.edit/.delete` → `.manage` → permissão da página. Para decidir se o botão “Nova matrícula” aparece:

```sql
-- O usuário logado tem a permissão de escrita da página? (MariaDB 10.11 / MySQL 8)
-- Mesma consulta do App\Security\AuthorizationGuard (catálogo RBAC no banco master).
SELECT COUNT(*) > 0 AS can_create
  FROM permissions p
  JOIN role_permission rp ON rp.permission_id = p.uuid
  JOIN user_role ur       ON ur.role_id = rp.role_id
 WHERE ur.user_id = :user_uuid
   AND p.slug = :write_permission;   -- ex.: 'admin.academic.admin'
```

Renderize o botão apenas quando `can_create = 1`; o servidor revalida no `DomainCrudController` (403 sem permissão ou sem `_token`). Superadmin (nível 10) passa sempre.

## Faça / Não faça

- **Faça:** uma primary por região; ícone à esquerda; rótulo curto com verbo.
- **Faça:** `ttsc-btn-sm` dentro de tabelas e cards densos.
- **Não faça:** duas primary lado a lado; botões verdes com texto branco (2:1); botão para navegação.
