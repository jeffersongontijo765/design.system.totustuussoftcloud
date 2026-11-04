# Modelo de ficha de módulo

Cada módulo do kit-starter usa esta ficha. Campos sem fonte no SDD ou nas especificações da v1 ficam como **[Sem detalhamento]**, nunca preenchidos por suposição.

## 1. Identificação
- Portal, área, módulo (do inventário) e domínio (plataforma ou entidade, conforme a matriz).
- Especificações de origem (v1) e regras aplicáveis (ex.: `17-regras-modulos.md`).

## 2. Objetivo e escopo
- Problema que resolve, quem usa e o que fica fora do módulo.

## 3. Telas
Para cada tela: nome, rota, tipo de arquétipo (dashboard, lista, formulário, detalhe, kanban, relatório, configurações) e componentes do design system usados.

## 4. Dados
- Entidades, dono do dado (plataforma ou entidade/unidade), tabelas, relações e isolamento por tenant.
- Estados do ciclo de vida e transições.

## 5. Campos e validações
- Tabela de campos: nome, tipo, obrigatório, validação, mensagem de erro (chave i18n).

## 6. Indicadores e gráficos
- KPIs com fórmula, fonte e período. Gráficos com tipo, eixos e filtros.

## 7. Ações e confirmações
- Ações da barra e por linha. Ações destrutivas com confirmação digitando o nome do objeto.

## 8. Permissões e papéis
- Quem vê, cria, edita, aprova e exporta. Validação no servidor.

## 9. Exportação e auditoria
- Formatos permitidos (CSV, XLSX, PDF, JSON). Eventos registrados na auditoria.

## 10. Estados de interface
- Carregando, vazio, sem resultado, erro, acesso negado, sucesso.

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.

## 12. Pendências e decisões
- Itens sem definição, com dono e critério de aceite.
