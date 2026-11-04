# Páginas

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Editor de portais
- Domínio: plataforma (banco master)
- Escopo: Definição declarativa de cada página dos portais, válida para todas as entidades (ou o escopo escolhido)
- Status: parcialmente detalhado (regras do SDD v2; telas e campos **[Sem detalhamento]**)

## 1. Identificação
- Especificações: `docs/v2/23-dominios-provisionamento-ciclo-de-vida.md` (§3); `docs/v2/78-permissoes-e-papeis.md`; `docs/v2/29-auditoria.md`

## 2. Objetivo e escopo
Criar e manter as páginas dos portais como definições declarativas, sem código livre (SDD 23, seção 3). Uma mudança de página vale para o escopo publicado.

## 3. Telas
- **Lista de páginas** (datatable): nome, portal, situação (rascunho, em revisão, publicada), última versão, responsável pela última edição.
- **Editor de página** (formulário declarativo): metadados, regiões, blocos da página, visibilidade por papel. Telas e campos completos **[Sem detalhamento]**.
- **Histórico de versões** da página (linha do tempo, ver `publicacao-e-rollback.md`).

## 4. Dados
- Página pertence a um portal. Sem HTML livre (SDD 23 §3).
- Estados: rascunho, em revisão, publicada, arquivada: transições **[Sem detalhamento]** além das regras de `publicacao-e-rollback.md`.

## 5. Campos e validações
- Nome e identificador da página: **[Sem detalhamento]**.
- Bloco fora do catálogo é recusado (SDD 23 §3, validação por esquema; ver `blocos.md`).

## 6. Indicadores e gráficos
- Páginas por portal e por situação. Métricas de uso de página: **[Sem detalhamento]**.

## 7. Ações e confirmações
- Criar, editar, enviar para revisão, arquivar. Excluir: **[Sem detalhamento]**; se existir, exige digitar o nome da página (SDD 08, seção 3).

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
- Regras de visibilidade por papel dentro da página: **[Sem detalhamento]**.
- Campos do editor declarativo: **[Sem detalhamento]**.
