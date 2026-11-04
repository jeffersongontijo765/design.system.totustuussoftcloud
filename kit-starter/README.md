# Kit starter — Portal do Desenvolvedor

Estrutura inicial do portal do desenvolvedor (equipe da plataforma), gerada a partir de `inventario/inventario-paginas.md` (seção 2.1 da matriz do SDD v2).

- `desenvolvedor/<area>/<modulo>.md`: um arquivo por módulo, com escopo, status e referências. Estado inicial: **pendente**.
- `gera_kit.py`: recria a estrutura quando o inventário muda. Não sobrescreve telas já aprovadas: revise antes de regerar.

Nenhuma tela foi criada ainda. Cada módulo tem sua seção "Telas" para ser detalhada e aprovada antes da implementação.

## Telas citadas fora da matriz

O inventário vem da seção 2 da matriz. Estas telas do portal do desenvolvedor estão em outros documentos do SDD e precisam entrar nas áreas indicadas:

| Tela | Fonte | Área do kit |
|---|---|---|
| Painel de bancos de dados (substitui o módulo "Bancos", PAG-03) | [34](../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 4 | Segurança e operação |
| Taxas de split recebidas por entidade e período | [34](../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 3 | Financeiro da plataforma (incluída) |
