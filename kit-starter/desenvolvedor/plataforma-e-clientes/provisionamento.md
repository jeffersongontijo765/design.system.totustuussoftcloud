# Provisionamento de entidade e unidade

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Plataforma e clientes
- Domínio: plataforma (banco master)
- Escopo: Criação de entidade e unidade em etapas retomáveis
- Status: detalhado

## 1. Identificação
- Especificações: `docs/v2/23-dominios-provisionamento-ciclo-de-vida.md` (§4); `docs/v2/03-dominio-tenancy.md`

## 2. Objetivo e escopo
Criar uma entidade ou unidade de forma segura: cada etapa é idempotente, a entidade só fica ativa ao final, e falhas deixam a entidade em `provisionando`.

## 3. Telas
- **Assistente de provisionamento** (8 etapas, SDD 23 §4): registro, banco da unidade, migrações, banco de identidade, carga inicial, canais e integrações, primeiro administrador por convite, ativação.
- **Fila de provisionamento** (datatable): entidade, etapa atual, situação, tentativas. Ações: retomar, cancelar.

## 4. Dados
- Registro no master; banco `tt_NNN` com registro em `tenant_databases`; banco de identidade da entidade, vazio e cifrado (D-19).
- Convite do primeiro administrador: validade de 72 h (SDD 06).

## 5. Campos e validações
- Código e domínio únicos (etapa 1).
- `schema_version` do banco igual à versão atual (etapa 3).
- Teste de conexão de canais, sem ativação automática (etapa 6).

## 6. Indicadores e gráficos
- Entidades em provisionamento, falhas por etapa.

## 7. Ações e confirmações
- Retomar: repete a etapa com falha, sem duplicar o que já foi criado.
- Cancelar: remove o banco criado e o registro (verificado). Confirmação digitando o código da entidade.

## 8. Permissões e papéis
- Só `platform.developer` cria entidade e unidade, na tela e na API (SDD 78, L-02 e §3).

## 9. Exportação e auditoria
- Cada etapa registrada na auditoria (SDD 29). Retomada e cancelamento com registro (SDD 23 §4).

## 10. Estados de interface
- Etapa em andamento, falha em etapa (com motivo), concluído, cancelado.

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
- Tempo limite de retomada: **[Sem detalhamento]**.
