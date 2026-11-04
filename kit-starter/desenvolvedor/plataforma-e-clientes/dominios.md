# Domínios

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Plataforma e clientes
- Domínio: plataforma (banco master)
- Escopo: Domínios dos portais e domínios próprios das entidades
- Status: detalhado

## 1. Identificação
- Especificações: `docs/v2/23-dominios-provisionamento-ciclo-de-vida.md` (§1)

## 2. Objetivo e escopo
Gerir os domínios da plataforma e os domínios próprios das entidades, com verificação de posse.

## 3. Telas
- **Domínios ativos** (datatable): domínio, tipo (plataforma ou entidade), entidade, situação, certificado (validade).
- **Verificar domínio próprio** (página em etapas): registro DNS para comprovar a posse, emissão do certificado, ativação.
- **Alertas de certificado**: vencimento com alerta a 14 dias (SDD 23 §1, regra 3).

## 4. Dados
- Domínios da plataforma: `desenvolvedor.`, `gestao.`, `portal-do-professor.`, `portal-do-aluno.`, `portal-dos-responsaveis.`, `portal-de-terceiros.`, `autenticacao.`, `arquivos.` (SDD 23 §1).
- Domínio próprio de entidade: sem verificação de posse, não é ativado (SDD 23 §1, regra 4).

## 5. Campos e validações
- Formato do domínio: um único nível antes de `totustuussoftcloud.com.br` (SDD 23 §1).
- Host desconhecido recebe 404 (SDD 23 §1, regra 5).

## 6. Indicadores e gráficos
- Domínios por situação; certificados a vencer em 14 dias.

## 7. Ações e confirmações
- Adicionar domínio próprio, verificar, ativar, remover. Remoção de domínio ativo: confirmação digitando o nome do domínio.

## 8. Permissões e papéis
- Papel de plataforma: **[Sem detalhamento]**.

## 9. Exportação e auditoria
- Verificação, ativação e remoção auditadas (SDD 29).

## 10. Estados de interface
- Carregando, vazio, verificação pendente, certificado a vencer, erro de DNS, acesso negado.

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
- Cadastro da entidade para domínio próprio: endereço da entidade pendente em D-26 (SDD 23 §1).
