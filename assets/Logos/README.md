# Logos

Arquivos copiados de `assets/media/app/` do repositório, sem alteração.

| Arquivo | Uso | Fundo |
|---|---|---|
| `logo.svg` | Logotipo horizontal padrão (marca + “TotusTuus SOFTCLOUD”), igual a `brand-logos/totustuus-logo.svg`. | `ttsc-surface` claro |
| `logo-light.svg` | Logotipo para o tema claro (texto `#1e293b` / `#64748b`). | `ttsc-surface`, `ttsc-canvas` claros |
| `logo-dark.svg` | Logotipo para o tema escuro (texto `#f8fafc` / `#94a3b8`). | `ttsc-surface`, `ttsc-canvas` escuros |
| `logo-mark.svg` | Só o símbolo (também é o `favicon.svg`). Rail de 60px, avatar do sistema, splash. | qualquer |

- A marca é sempre `#10b981` (token `ttsc-logo`); não recolorir para `ttsc-accent`.
- O texto do logotipo é `<text>` em Inter 800/600: em `<img>` ele usa a Inter só se estiver instalada; para impressão, prefira `logo.png` do repositório.
- Área de respiro mínima: a altura do “T” ao redor. Altura mínima do logotipo horizontal: 24px; do símbolo: 16px.
- Nunca aplicar sombra, contorno, gradiente ou rotação; nunca colocar sobre `ttsc-accent`.
