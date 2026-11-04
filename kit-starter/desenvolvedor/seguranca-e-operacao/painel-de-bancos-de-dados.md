# Painel de bancos de dados

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Segurança e operação
- Domínio: plataforma (banco master), instância separada do módulo das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Status: detalhado a partir do SDD v2 (sem especificação própria na v1)
- Fonte da v1: sem especificação própria (regras no SDD v2, seção 4 desta ficha)

## 1. Regra de leitura
Não há especificação própria na v1. Valem as regras do SDD v2 citadas nesta ficha.

## 2. Objetivo e escopo
Gerir todos os bancos da plataforma (master, bancos de unidade e bancos de identidade) sem expor o conteúdo deles. Substitui o módulo "Bancos" da v1, removido do escopo (PAG-03).

## 3. Telas
- **Inventário de bancos** (datatable): master, cada banco de unidade, cada banco de identidade; versão do esquema, tamanho e última restauração testada.
- **Migrações** (datatable por unidade e página de migração em lote com plano de volta e aprovação).
- **Backups** (datatable): estado e prazo de cada backup; pedido de restauração com dupla aprovação.
- **Acesso técnico de emergência** (página de pedido): motivo, chamado vinculado, tempo da sessão, leitura ou escrita.


## 4. Correções da v2 que prevalecem
- **Regras do [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 4 (PAG-03):**
  - Não existe console SQL no painel comum.
  - Migração em lote só com plano de volta e aprovação de segundo papel.
  - Restauração só por pedido com dupla aprovação, em ambiente isolado.
  - Acesso técnico direto só por procedimento de emergência: passkey, motivo e chamado vinculado, sessão de tempo limitado, leitura por padrão, escrita só com dupla aprovação; cada comando gravado e mascarado ([29](../../../docs/v2/29-auditoria.md)).
  - Consulta que atinja dado pessoal exige motivo e gera evento de auditoria.
  - Nenhum portal de entidade vê este painel.
- **Especificações "Bancos" da v1** (`spec_gestao_bancos.md` e `spec_gestao_bancos_completo.md`): fora do escopo e **não absorvidas**, porque expõem console SQL a todos os clientes ([03](../../../docs/v2/03-dominio-tenancy.md)).

## 5. Decisões por padrão aplicadas
- Nenhuma decisão nova (PAG-03 decidido em 03/11/2026).

## 6. Permissões e papéis
- `platform.ops`: consultar inventário, acompanhar migrações e backups, pedir restauração e acesso de emergência.
- `platform.developer`: aprovar migração em lote, restauração e escrita de emergência (segundo papel); a dupla aprovação exige duas pessoas diferentes de quem pediu.

## 7. Dados
- Metadados dos bancos no master (`tenant_databases`, versão de esquema, backups). Nenhum dado de cliente é lido pelo painel.

## 8. Integrações
- Provisionamento ([provisionamento.md](../plataforma-e-clientes/provisionamento.md)): cria banco e registro.
- Backup externo ([16](../../../docs/v2/16-integracoes-externas.md), seção 2).

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md).


## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- Prazo de retenção de backup (G-12, [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 3).

