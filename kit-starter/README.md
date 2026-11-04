# Kit starter — sistema completo

Fichas de implementação de **todos os portais** do TotusTuus, geradas a partir do SDD v2 (`docs/v2/`) e da matriz de portais ([31](../docs/v2/31-matriz-portais-modulos.md), seção 2). Cada ficha é autossuficiente: quem implementa não precisa abrir a v1.

## Estrutura

| Pasta | Portal | Granularidade | Fichas |
|---|---|---|---|
| `desenvolvedor/<area>/<modulo>.md` | Desenvolvedor (`desenvolvedor.`), equipe da plataforma | Uma ficha por módulo | 38 |
| `gestao/<area>/<modulo>.md` | Gestão (`gestao.`), equipe administrativa da entidade | Uma ficha por módulo | 97 |
| `professor/<area>.md` | Professor (`portal-do-professor.`) | Uma ficha por área; os módulos da matriz são telas | 9 |
| `aluno/<area>.md` | Aluno (`portal-do-aluno.`) | Uma ficha por área | 10 |
| `responsaveis/<area>.md` | Pais e Responsáveis (`portal-dos-responsaveis.`) | Uma ficha por área | 6 |
| `terceiros/<area>.md` | Terceiros (`portal-de-terceiros.`) | Uma ficha por área | 7 |
| `transversal/*.md` | Todos | Regras que valem para todos os módulos | 6 |

## Como ler uma ficha

1. **Seções 1 a 12:** objetivo, telas (com os componentes do design system), permissões por portal extraídas do SDD, papéis do [78](../docs/v2/78-permissoes-e-papeis.md), regras essenciais, dados, integrações, exportação e auditoria, estados de interface, requisitos de frontend, aceite e pendências.
2. **Seção 13:** texto integral das seções do SDD v2 que regem o módulo, sem corte, com links ajustados. Em caso de dúvida, vale a seção 13.
3. **Seção 14** (fichas dos portais de entidade) ou **seção 13** (fichas do desenvolvedor e transversais): texto integral da especificação da v1 absorvida. Quando a v1 diz algo diferente, vale a v2.
4. Quando uma especificação da v1 serve a vários módulos, ela é copiada **uma vez** e as outras fichas apontam para ela (linha "Fonte da v1").

Decisões tomadas por padrão (sem pergunta ao autor, com o critério mais seguro e completo) estão no [80](../docs/v2/80-decisoes-por-padrao.md). A situação de cada arquivo da v1 está no [79](../docs/v2/79-rastreabilidade-v1-v2.md).

## Geradores

| Script | O que faz |
|---|---|
| `inventario/gera_inventario.py` | Lê a matriz (31, seção 2) e gera `inventario/inventario-paginas.md` |
| `kit-starter/gera_kit.py` | Cria esqueletos "pendente" para módulos novos; nunca sobrescreve ficha detalhada |
| `kit-starter/absorve_v1.py` | Fichas do desenvolvedor e transversais que absorvem especificações da v1 |
| `kit-starter/fichas_portais.py` | Fichas dos portais de entidade a partir de `dados_gestao.py`, `dados_professor.py`, `dados_aluno.py`, `dados_responsaveis.py` e `dados_terceiros.py` |
| `inventario/gera_rastreabilidade.py` | Regera o [79](../docs/v2/79-rastreabilidade-v1-v2.md) e reconhece as especificações absorvidas no kit |
| `inventario/gera_sdd_completo.py` | Regera `docs/v2/SDD-COMPLETO.md` |

Ordem ao mudar o SDD: matriz → `gera_inventario.py` → `gera_kit.py` → completar o arquivo `dados_*.py` ou `absorve_v1.py` → `fichas_portais.py` e `absorve_v1.py` → `gera_rastreabilidade.py` → `gera_sdd_completo.py`.

## Ordem de construção recomendada

1. Transversais: tenancy ([03](../docs/v2/03-dominio-tenancy.md)), identidade e acesso ([acesso](desenvolvedor/seguranca-e-operacao/acesso.md)), permissões ([78](../docs/v2/78-permissoes-e-papeis.md)), auditoria ([auditoria](desenvolvedor/seguranca-e-operacao/auditoria.md)), [exclusão lógica](transversal/exclusao-logica.md), privacidade.
2. Plataforma: [provisionamento](desenvolvedor/plataforma-e-clientes/provisionamento.md), licenciamento e limites ([77](../docs/v2/77-licenciamento-planos-e-limites.md)).
3. Acadêmico na ordem do [55](../docs/v2/55-academico-verificacao-e-lacunas.md), seção 3: estrutura, sistemas avaliativos, turmas e grade, diário, boletim e conselho, e os demais.
4. Secretaria, financeiro e os módulos de apoio da gestão; depois os portais do professor, aluno, responsáveis e terceiros.

O plano de fases da v1 está guardado em [plano-de-implementacao-v1](transversal/plano-de-implementacao-v1.md).

## Telas citadas fora da matriz

| Tela | Fonte | Ficha |
|---|---|---|
| Painel de bancos de dados (substitui o módulo "Bancos", PAG-03) | [34](../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 4 | [painel-de-bancos-de-dados](desenvolvedor/seguranca-e-operacao/painel-de-bancos-de-dados.md) |
| Taxas de split recebidas por entidade e período | [34](../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 3 | Financeiro da plataforma |

## Fora do SDD

- `sub_sidebar_itsm.php` da v1 é código de view com `onclick=` (ACH-01), não especificação; não é absorvido.
- A v1 cita especificações de páginas do aplicativo em `docs/portais/*-completo.md` e skills em `.agents/skills/` do repositório `jeffersongontijo765/totustuussoftcloud.academic`. Elas ficam naquele repositório; onde divergirem do kit, vale o SDD v2.
