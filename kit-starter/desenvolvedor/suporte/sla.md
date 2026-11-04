# SLA do suporte da plataforma

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Suporte
- Domínio: plataforma (banco master), instância separada do módulo das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Status: detalhado a partir do SDD v2 (sem especificação própria na v1)
- Fonte da v1: sem especificação própria (regras no SDD v2, seção 4 desta ficha)

## 1. Regra de leitura
Não há especificação própria na v1. Valem as regras do SDD v2 citadas nesta ficha.

## 2. Objetivo e escopo
Definir e acompanhar os prazos de atendimento dos chamados das entidades clientes.

## 3. Telas
- **Regras de SLA** (datatable): aplicação (entidade, cliente, fila, tipo, categoria, prioridade), tipo de prazo (primeira resposta, próxima resposta, resolução, fechamento) e valor. A regra mais específica vence.
- **Painel de SLA** (dashboard): chamados dentro do prazo, com 80% do prazo consumido e com prazo estourado, por fila e por prioridade; gráfico de cumprimento por período.
- **Calendário de dias úteis** (configuração): dias úteis e feriados usados na contagem.


## 4. Correções da v2 que prevalecem
- **Tipos de prazo** ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.3): primeira resposta, próxima resposta, resolução e fechamento.
- **Padrão aprovado** (ATD-02): urgente 1 h e 4 h; alta 4 h e 2 dias úteis; média 1 dia útil e 5 dias úteis; baixa 2 dias úteis e 10 dias úteis (primeira resposta e resolução). Ajustável por entidade dentro do limite do contrato.
- **Fechamento automático:** 3 dias úteis após `resolvido`, sem resposta do solicitante.
- **Pausa:** tempo em `aguardando_*` não conta.
- **Sem SLA:** sem valor definido, o chamado não recebe prazo e o painel mostra "sem SLA".
- **Alertas:** 80% do prazo consumido e prazo estourado; o estouro aparece no painel do gestor, não no portal do solicitante.

## 5. Decisões por padrão aplicadas
- Nenhuma decisão nova: valores e regras já aprovados (ATD-02).

## 6. Permissões e papéis
- `platform.manager`: configurar regras e calendário; ver o painel completo.
- `platform.operator`: ver o prazo dos próprios chamados.

## 7. Dados
- Regras de SLA e contagem no DDL do atendimento ([51](../../../docs/v2/51-ddl-modulos-novos.md), seção 1).

## 8. Integrações
- Chamados: prazo calculado na abertura e recalculado em cada mudança de estado.
- Notificações de alerta e de estouro ([57](../../../docs/v2/57-notificacoes-por-portal.md)).
- Contrato do cliente: limite de SLA contratado.

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md).


## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- Nenhuma além das do atendimento ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.10).

