# Publicação e rollback

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Editor de portais
- Domínio: plataforma (banco master)
- Escopo: Fluxo de rascunho, revisão, publicação por escopo e volta a versão anterior
- Status: parcialmente detalhado (regras do SDD v2; telas e campos **[Sem detalhamento]**)

## 1. Identificação
- Especificações: `docs/v2/23-dominios-provisionamento-ciclo-de-vida.md` (§3); `docs/v2/78-permissoes-e-papeis.md`; `docs/v2/29-auditoria.md`

## 2. Objetivo e escopo
Garantir que nenhuma mudança de portal chegue aos clientes sem revisão, com versão imutável e volta em um clique (SDD 23 §3).

## 3. Telas
- **Fila de revisão** (datatable): página ou layout, autor, data, escopo pretendido, situação.
- **Publicação** (página de confirmação): escopo (uma entidade, grupo ou todas), resumo das mudanças, resultado do teste de fumaça.
- **Versões** (linha do tempo imutável) com botão de volta a uma versão anterior.

## 4. Dados
- Versão imutável a cada publicação (SDD 23 §3).
- Escopo padrão: uma entidade; depois grupo (SDD 23 §3).
- Implantação separada do produto: falha do editor não afeta clientes (SDD 23 §3).

## 5. Campos e validações
- Revisão por segundo papel antes de publicar (SDD 23 §3).
- Teste de fumaça das telas afetadas antes de ir para produção (SDD 23 §3).
- Rollback registrado.

## 6. Indicadores e gráficos
- Publicações por período, rollbacks, mudanças aguardando revisão.

## 7. Ações e confirmações
- Enviar para revisão, aprovar, publicar, reverter. Publicar para todas as entidades: confirmação digitando o identificador do escopo.

## 8. Permissões e papéis
- Acesso: `platform.builder` (nível 7, escopo plataforma), com passkey e sessão de curta duração, e reautenticação antes de publicar (SDD 78, §4.1; SDD 31, seção 4).
- Editar e aprovar: não pode ser a mesma pessoa (SDD 78, §2.2).
- Quem aprova a revisão é um papel diferente do autor. **Papel exato não definido** (pendência D-33).

## 9. Exportação e auditoria
- Cada edição, aprovação, publicação e rollback gera registro (SDD 29; SDD 23 §3). Acesso ao editor é registrado.

## 10. Estados de interface
- Carregando, vazio, sem resultado, erro, acesso negado, rascunho, em revisão, publicado, com rollback feito.

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- O editor não aceita HTML, PHP ou JavaScript livre: só definições declarativas (SDD 23, seção 3).

## 12. Pendências e decisões
- Papel aprovador (D-33): **[Sem detalhamento]**. Proposta: `platform.developer` aprova o que o `platform.builder` edita.
- Tempo máximo de revisão e regra de rollback automático: **[Sem detalhamento]**.
