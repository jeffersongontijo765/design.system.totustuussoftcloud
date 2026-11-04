# Layouts

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Editor de portais
- Domínio: plataforma (banco master)
- Escopo: Regiões de página dentro da casca do portal, sem alterar a casca
- Status: parcialmente detalhado (regras do SDD v2; telas e campos **[Sem detalhamento]**)

## 1. Identificação
- Especificações: `docs/v2/08-frontend-design-system.md` (§3 e §6); `docs/v2/23-dominios-provisionamento-ciclo-de-vida.md` (§3)

## 2. Objetivo e escopo
Definir como uma página se organiza em regiões, usando a casca do portal (cabeçalho, navegação, sub-sidebar, rodapé) que não muda numa tela de conteúdo (regra de layout do DS).

## 3. Telas
- **Lista de layouts** (datatable): nome, portal, regiões, situação.
- **Editor de layout**: regiões e ordem. Campos completos **[Sem detalhamento]**.
- **Pré-visualização** em 320 px, 375 px e 1280 px (SDD 08, seção 6).

## 4. Dados
- Layout pertence a um portal e é usado por páginas. A casca vem do layout do portal (SDD 08 e a navegação do DS).
- Regiões e blocos seguem o catálogo de `blocos.md`.

## 5. Campos e validações
- Região vazia, região duplicada: **[Sem detalhamento]** da regra.
- Página sem rolagem horizontal em 320 px (SDD 08, seção 6).

## 6. Indicadores e gráficos
- Layouts por portal. Layouts sem uso.

## 7. Ações e confirmações
- Criar, duplicar, arquivar layout. Trocar layout de página publicada passa por revisão (`publicacao-e-rollback.md`).

## 8. Permissões e papéis
- Acesso: `platform.builder` (nível 7, escopo plataforma), com passkey e sessão de curta duração, e reautenticação antes de publicar (SDD 78, §4.1; SDD 31, seção 4).
- Editar e aprovar: não pode ser a mesma pessoa (SDD 78, §2.2).

## 9. Exportação e auditoria
- Cada edição, aprovação, publicação e rollback gera registro (SDD 29; SDD 23 §3). Acesso ao editor é registrado.

## 10. Estados de interface
- Carregando, vazio, sem resultado, erro, acesso negado, rascunho, em revisão, publicado, com rollback feito.

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- O editor não aceita HTML, PHP ou JavaScript livre: só definições declarativas (SDD 23, seção 3).

## 12. Pendências e decisões
- Regiões padrão de cada portal e lista de layouts permitidos: **[Sem detalhamento]**.
