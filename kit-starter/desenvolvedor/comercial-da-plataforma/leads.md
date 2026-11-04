# Leads

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Comercial da plataforma
- Domínio: plataforma (banco master, D-16)
- Escopo: Instituições e decisores interessados no SaaS, com consentimento e deduplicação
- Status: detalhado (SDD 22 e v1)

## 1. Identificação
- Especificações: SDD 22 (CRM em dois contextos), v1 `spec_crm_funil_comercial.md`, SDD 78 (permissões).
- Regra de fonte: onde a v1 e a v2 divergem, vale a v2 ([22](../../../docs/v2/22-crm-canais-e-papeis.md)). A v1 ([spec_crm_funil_comercial.md](../../../docs/v2/anexo-v1/spec_crm_funil_comercial.md)) vale onde a v2 não trata do assunto.

## 2. Objetivo e escopo
Registrar e qualificar os leads da plataforma vindos dos canais oficiais (site, WhatsApp, Telegram, Instagram, Messenger, telefone, presencial, indicação).

- **Separação dos CRMs (D-16):** nenhum lead de tenant aparece aqui, e nenhum lead da plataforma aparece em tenant. A ligação entre os dois é só o contrato comercial (SDD 22, seção 1).

## 3. Telas
- **Lista de leads** (`/crm/leads`, datatable). Colunas (v1, seção 6, ajustadas à v2): nome, telefone ou e-mail, canal de origem, campanha, produto ou plano de interesse, responsável, situação, data de criação, última interação, ações.
- **Ficha do lead** (`/crm/leads/:uuid`, página com linha do tempo de interações e consentimentos).
- **Drawer de lead** (criar e editar, v1 seção 6): contato, canal de origem, campanha, plano de interesse, responsável (manual ou por regra), pontuação de qualificação, linha do tempo, botão "Converter em oportunidade".
- **Alerta de possível duplicidade** na lista e na ficha.

## 4. Dados
- `crm_leads` (SDD 22, seção 8): `context = 'plataforma'`, `origin_channel`, `owner_uuid`, `status`, `lost_reason`, `email_hash` e `phone_hash` (HMAC com pepper), dados em claro cifrados.
- `crm_consents` (SDD 22, seção 8): finalidade, canal, versão do texto, data de aceite e de revogação. Consentimento nunca é apagado; revogação preenche `revoked_at`.
- Interações (mensagens, ligações, visitas) em tabela própria, com canal, direção e transcrição.

## 5. Campos e validações
- Nome: obrigatório (até 150). Telefone em E.164. E-mail válido.
- Captura só depois do aviso de finalidade; sem consentimento, o lead fica `sem_consentimento` e não recebe marketing (SDD 22, seção 2).
- Deduplicação: mesmo `email_hash` ou `phone_hash` no mesmo contexto gera alerta, sem fusão automática (SDD 22, seção 8).
- O bot não coleta dado de saúde, CPF completo, cartão, senha nem documento de imagem (SDD 22, seção 3).

## 6. Indicadores e gráficos
- Leads por situação e por canal; leads sem responsável; leads com consentimento revogado.

## 7. Ações e confirmações
- Criar, editar, atribuir, converter em oportunidade, descartar (desqualificado ou duplicado).
- Revogar consentimento: registro com data; efeito imediato sobre marketing.

## 8. Permissões e papéis
Papéis do CRM da plataforma (SDD 22, seção 4.1; códigos em SDD 78, seção 4.1):

| Papel | Pode | Não pode |
|---|---|---|
| Pré-vendas (SDR) | Qualificar, agendar demonstração, registrar interação | Fechar proposta, alterar preço, ver contrato |
| Vendedor (AE) | Criar proposta, avançar o funil até negociação (só os próprios) | Aprovar desconto acima da alçada, alterar contrato assinado |
| Gerente comercial | Atribuir leads, aprovar desconto dentro da alçada, ver funil da equipe | Aprovar a própria proposta |
| Operador de chatbot | Atender, transferir e registrar conversas da fila | Acessar carteira fora da fila |
| Sucesso do cliente | Acompanhar implantação e uso dos clientes ativos | Alterar cobrança |

## 9. Exportação e auditoria
- Exportação de leads exige permissão de exportação e step-up; CSV neutralizado. Auditoria de criação, atribuição, conversão e revogação de consentimento.

## 10. Estados de interface
- Carregando, vazio, sem resultado, erro, acesso negado. Lead `sem_consentimento` mostrado com aviso de que não recebe marketing.

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
- Texto de aceite de finalidade (lacuna L-21 do SDD 22).
- Critério da pontuação de qualificação (BANT ou próprio): **[Sem detalhamento]**.
