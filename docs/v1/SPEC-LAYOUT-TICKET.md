# SPEC-LAYOUT-TICKET.md

## 1. Objetivo

Este documento define a implementação da tela de detalhe de ticket inspirada no layout Movidesk da imagem de referência, usando Supabase como backend, autenticação, banco de dados, storage e controle de acesso. O objetivo é reproduzir a mesma densidade visual, organização dos campos e hierarquia de ações mostradas na interface [file:62].

## 2. Diretrizes de Layout

- Interface desktop-first.
- Sidebar fixa à esquerda.
- Topbar fixa no topo.
- Área principal dividida em coluna lateral de formulário e painel central de atendimento.
- Visual administrativo limpo, com fundo branco, bordas cinza claras e acento azul.
- Espaçamento compacto, típico de sistema de help desk profissional.

## 3. Estrutura Geral

### 3.1 Região 1 - Sidebar

- Largura fixa: 64px.
- Fundo: azul-acinzentado escuro.
- Ícones centralizados verticalmente.
- Estado ativo com contraste visual sutil.
- Conteúdo: navegação principal do sistema.

### 3.2 Região 2 - Topbar

- Altura fixa: 48px.
- Fundo branco.
- Linha inferior azul fina.
- À esquerda: identificação do ticket.
- À direita: ícones de busca, relógio, notificação, telefone, chat e avatar.
- Canto superior direito: menu de opções e status do ticket.

### 3.3 Região 3 - Conteúdo Principal

- Coluna esquerda: 340px aproximadamente.
- Painel central: restante da largura.
- O conteúdo deve ter rolagem vertical independente.

## 4. Coluna Esquerda

### 4.1 Bloco superior

- Tabs: Público e Interno.
- Link rápido: Colocar-me como solicitante.
- Campo: Solicitante.
- Campo: Serviço.
- Campo: Categoria.
- Campo: Urgência.
- Seção Ativos com radio buttons: Solicitante, Organização, Todos.

### 4.2 Bloco intermediário

- Campo: Previsão de solução.
- Campo: Responsável.
- Link rápido: Atribuir para mim.
- Campo: Tags.
- Campo: CC.

### 4.3 Regras visuais

- Labels acima dos inputs.
- Inputs com altura compacta.
- Bordas finas cinza claras.
- Largura total da coluna.
- Espaçamento vertical consistente.

## 5. Painel Central

### 5.1 Cabeçalho do ticket

- Campo largo: Assunto.
- Deve ocupar praticamente toda a largura útil do painel central.
- Posicionado imediatamente abaixo da topbar.

### 5.2 Editor de resposta

- Tabs: Ação pública e Ação interna.
- Ação pública ativa por padrão.
- Área de texto grande logo abaixo das tabs.
- Deve aceitar rich text futuramente.
- Deve suportar anexos, menções e macros.

### 5.3 Linha de ações e metadados

Campos na mesma linha:

- Data.
- Início.
- Fim.
- Tempo.
- Tipo.
- Tempo contabilizado.
- Atividade.
- Valor.
- Opções.

### 5.4 Botões

- Botão secundário: Aplicar macro.
- Botão de destaque: Nova ação.
- Botão final: Salvar.
- Menu Opções no canto direito da linha de status.

## 6. Componentes da Interface

### 6.1 Inputs

- Text input.
- Select com busca.
- Date picker.
- Time picker.
- Radio group.
- Textarea.
- Rich text editor.
- File uploader.

### 6.2 Navegação

- Sidebar icons.
- Tabs da esquerda.
- Tabs do editor.
- Menu de opções.

### 6.3 Feedback visual

- Badges de status.
- Hover sutil nos botões.
- Foco visível nos campos.
- Estado ativo em tabs e ícones.

## 7. Mapeamento de Dados Supabase

### 7.1 Tabelas principais

- tenants.
- users.
- user_profiles.
- customers.
- contacts.
- companies.
- units.
- departments.
- services.
- categories.
- queues.
- tickets.
- ticket_messages.
- ticket_activities.
- ticket_attachments.
- ticket_tags.
- sla_policies.
- macros.
- audit_logs.
- notifications.

### 7.2 Relações principais

- tickets.requester_id -> contacts.id.
- tickets.owner_user_id -> users.id.
- tickets.queue_id -> queues.id.
- tickets.category_id -> categories.id.
- tickets.service_id -> services.id.
- ticket_messages.ticket_id -> tickets.id.
- ticket_attachments.ticket_id -> tickets.id.
- ticket_tags.ticket_id -> tickets.id.

## 8. Regras de RLS

- Um usuário só acessa tickets do seu tenant.
- Cliente só acessa tickets próprios ou compartilhados.
- Agente só acessa filas autorizadas.
- Supervisores podem acessar tickets da unidade ou equipe sob responsabilidade.
- Todas as tabelas sensíveis devem ter RLS habilitado.

## 9. Interações da Tela

### 9.1 Abrir ticket

- Carregar ticket por id.
- Preencher colunas esquerda e central.
- Buscar mensagens, anexos e histórico.

### 9.2 Alterar solicitante

- Atualizar requester_id.
- Recalcular contexto do ticket.
- Registrar no audit log.

### 9.3 Alterar responsável

- Atualizar owner_user_id.
- Registrar timestamp da atribuição.
- Atualizar SLA se necessário.

### 9.4 Enviar ação pública

- Inserir mensagem pública na timeline.
- Notificar solicitante.
- Registrar evento.

### 9.5 Inserir ação interna

- Inserir nota interna apenas para agentes.
- Não notificar cliente.
- Registrar autor e data.

### 9.6 Aplicar macro

- Mostrar modal de seleção.
- Aplicar texto, tags, status e ações associadas.

## 10. Comportamento Responsivo

### 10.1 Desktop

- Layout completo conforme referência.

### 10.2 Tablet

- Sidebar colapsável.
- Coluna esquerda retrátil.
- Painel central priorizado.

### 10.3 Mobile

- Sidebar em drawer.
- Coluna esquerda vira seção expansível.
- Editor e metadados empilhados verticalmente.

## 11. Estados da Página

- Carregando.
- Ticket encontrado.
- Ticket não encontrado.
- Sem permissão.
- Erro de rede.
- Salvando.
- Salvo com sucesso.
- Alteração pendente.

## 12. Validações

- Assunto obrigatório.
- Solicitante obrigatório em ticket novo.
- Serviço obrigatório quando a fila exigir.
- Responsável obrigatório em status de atendimento, quando configurado.
- Mensagem pública não pode ser enviada vazia.
- Arquivos devem respeitar limite de tamanho e tipo.

## 13. Stack Sugerida

- Frontend: Next.js ou React.
- Estilo: Tailwind CSS.
- UI kit: componentes próprios ou shadcn/ui adaptado.
- Backend: Supabase.
- Auth: Supabase Auth.
- Banco: PostgreSQL do Supabase.
- Storage: Supabase Storage.
- Realtime: Supabase Realtime.

## 14. Componentes React Sugeridos

- TicketLayout.
- SidebarNav.
- TopBar.
- TicketHeader.
- TicketField.
- TicketTabs.
- PublicActionEditor.
- InternalActionEditor.
- MetadataRow.
- TicketMacroPicker.
- TicketStatusBadge.
- TicketAssigneePicker.
- TicketServicePicker.
- TicketCategoryPicker.
- TicketAttachments.
- TicketTimeline.

## 15. Estrutura de Pastas

```txt
app/
  tickets/
    [id]/
      page.tsx
components/
  ticket/
    SidebarNav.tsx
    TopBar.tsx
    TicketHeader.tsx
    TicketFields.tsx
    TicketEditor.tsx
    TicketMetaRow.tsx
    TicketActions.tsx
lib/
  supabase/
  auth/
  tickets/
  permissions/
  validations/
```

## 16. Tokens Visuais

- primary: #2F6FED
- sidebar: #3C4A57
- background: #F6F7FA
- surface: #FFFFFF
- border: #D9DEE6
- text: #2C2C2C
- text-muted: #6B7280
- success: #22C55E
- warning: #F59E0B
- danger: #EF4444

## 17. Regras de Auditoria

Registrar em audit_logs:

- criação do ticket.
- alteração de campo.
- troca de responsável.
- envio de mensagem.
- alteração de status.
- aplicação de macro.
- anexos adicionados.
- ações internas.
- fechamento.
- reabertura.

## 18. Critérios de Aceite

- A tela deve reproduzir fielmente a composição visual da referência.
- A hierarquia visual deve permitir leitura rápida e operação eficiente.
- O layout deve funcionar em desktop sem quebra de alinhamento.
- O ticket deve carregar e salvar dados via Supabase.
- Os campos devem ser consistentes com o modelo de dados do help desk.
- Todas as ações relevantes devem ser auditadas.

## 19. Próximos Entregáveis

- Wireframe detalhado por bloco.
- Schema SQL do Supabase.
- RLS policies.
- Componentes React base.
- Contrato de API para o ticket.
- Lista de validações front-end e back-end.
