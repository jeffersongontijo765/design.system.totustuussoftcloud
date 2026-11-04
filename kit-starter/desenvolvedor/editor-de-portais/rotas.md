# Rotas

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Editor de portais
- Domínio: plataforma (banco master)
- Escopo: Caminhos das páginas dentro de cada portal e domínio
- Status: parcialmente detalhado (regras do SDD v2; telas e campos **[Sem detalhamento]**)

## 1. Identificação
- Especificações: `docs/v2/23-dominios-provisionamento-ciclo-de-vida.md` (§3); `docs/v2/78-permissoes-e-papeis.md`; `docs/v2/29-auditoria.md`

## 2. Objetivo e escopo
Definir as rotas das páginas com validação de host e destino, para que nenhuma rota fique sem regra (SDD 23 §1; default-deny, SDD 03).

## 3. Telas
- **Lista de rotas** (datatable): caminho, portal, domínio, página associada, papel exigido, situação.
- **Editor de rota**: caminho, página, papéis permitidos (ver `paginas.md`). Campos completos **[Sem detalhamento]**.

## 4. Dados
- Rota pertence a um domínio dos seis portais e a uma página (SDD 23 §1).
- Destino de redirecionamento só da lista de destinos permitidos por conta (SDD 23 §1, regra 2).

## 5. Campos e validações
- Caminho com um único nível de host antes de `totustuussoftcloud.com.br` (SDD 23 §1).
- Host desconhecido recebe 404 (SDD 23 §1, regra 5).
- Rota sem regra explícita é negada (default-deny, SDD 03).

## 6. Indicadores e gráficos
- Rotas por portal; rotas sem página associada.

## 7. Ações e confirmações
- Criar, alterar caminho, remover. Remover rota ativa: confirmação digitando o caminho (SDD 08, seção 3).

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
- Formato exato do caminho e regras de parâmetro: **[Sem detalhamento]**.
