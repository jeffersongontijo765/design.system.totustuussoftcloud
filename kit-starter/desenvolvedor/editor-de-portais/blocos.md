# Blocos

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Editor de portais
- Domínio: plataforma (banco master)
- Escopo: Catálogo de blocos aprovados que as páginas e layouts podem usar
- Status: parcialmente detalhado (regras do SDD v2; telas e campos **[Sem detalhamento]**)

## 1. Identificação
- Especificações: `docs/v2/23` (§3); `docs/v2/08` (§4, componentes)

## 2. Objetivo e escopo
Manter o catálogo de blocos aprovados. Bloco fora do catálogo é recusado na publicação (SDD 23 §3). Os blocos são os componentes do design system (ver `kit-starter/README.md` e o índice de componentes).

## 3. Telas
- **Catálogo de blocos** (datatable): nome, componente do DS de origem, parâmetros, situação (aprovado, desativado).
- **Detalhe do bloco**: parâmetros aceitos, validação, exemplo. Campos **[Sem detalhamento]**.

## 4. Dados
- Bloco aponta para um componente do design system. Lista de componentes: índice em `docs/design-system/template/components/`.
- Catálogo inicial de blocos aprovados: **[Sem detalhamento]**.

## 5. Campos e validações
- Parâmetros de bloco validados por esquema antes da publicação (SDD 23 §3).
- Texto exibido passa pelo escape do sistema (SDD 23 §3).

## 6. Indicadores e gráficos
- Blocos por situação; blocos sem uso.

## 7. Ações e confirmações
- Aprovar novo bloco no catálogo, desativar bloco. Aprovação de bloco novo é decisão de plataforma: **[Sem detalhamento]** de quem aprova.

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
- Lista inicial de blocos e critérios de aprovação: **[Sem detalhamento]**.
