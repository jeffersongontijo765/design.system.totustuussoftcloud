# Propostas

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Comercial da plataforma
- Domínio: plataforma (banco master, D-16)
- Escopo: Propostas comerciais do SaaS para instituições
- Status: detalhado (v1, com regras da v2)

## 1. Identificação
- Especificações: SDD 22 (CRM em dois contextos), v1 `spec_crm_funil_comercial.md`, SDD 78 (permissões).
- Regra de fonte: onde a v1 e a v2 divergem, vale a v2 ([22](../../../docs/v2/22-crm-canais-e-papeis.md)). A v1 ([spec_crm_funil_comercial.md](../../../docs/v2/anexo-v1/spec_crm_funil_comercial.md)) vale onde a v2 não trata do assunto.

## 2. Objetivo e escopo
Emitir, enviar e acompanhar as propostas comerciais da plataforma para as instituições.

- **Separação dos CRMs (D-16):** nenhum lead de tenant aparece aqui, e nenhum lead da plataforma aparece em tenant. A ligação entre os dois é só o contrato comercial (SDD 22, seção 1).

## 3. Telas
- **Propostas** (`/crm/proposals`, datatable): oportunidade, instituição, valor total, situação, enviada em, respondida em, ações.
- **Editor de proposta** (drawer ou página): itens (plano, módulos, quantidade de alunos do plano), valores, descontos e condições; modelo de PDF configurável (v1, seção 9).
- **Visualizar PDF** da proposta.

## 4. Dados
- `crm_proposals` (v1, seção 14), com `tenant_id` e `context` conforme SDD 22, seção 8.
- Situações (v1, seção 9): rascunho, enviada, visualizada, aceita, recusada, expirada.
- Itens da proposta usam os planos do licenciamento: limite de alunos (L-01), módulos (D-35), preço e ciclo (D-29) ([77](../../../docs/v2/77-licenciamento-planos-e-limites.md)).
- Aceite leva ao contrato (Contratos) e, com o contrato, ao provisionamento.

## 5. Campos e validações
- Desconto acima da alçada exige aprovação do gerente comercial (SDD 22, seção 4.1). Valor da alçada: lacuna L-23.
- Proposta aceita não é editada: mudança gera nova proposta.

## 6. Indicadores e gráficos
- Propostas por situação; valor em propostas enviadas; taxa de aceite.

## 7. Ações e confirmações
- Criar, enviar, reenviar, registrar aceite ou recusa, expirar. Assinatura eletrônica pelo módulo de Contratos (v1, seção 9).

## 8. Permissões e papéis
Papéis do CRM da plataforma (SDD 22, seção 4.1; códigos em SDD 78, seção 4.1):

| Papel | Pode | Não pode |
|---|---|---|
| Pré-vendas (SDR) | Qualificar, agendar demonstração, registrar interação | Fechar proposta, alterar preço, ver contrato |
| Vendedor (AE) | Criar proposta, avançar o funil até negociação (só os próprios) | Aprovar desconto acima da alçada, alterar contrato assinado |
| Gerente comercial | Atribuir leads, aprovar desconto dentro da alçada, ver funil da equipe | Aprovar a própria proposta |
| Operador de chatbot | Atender, transferir e registrar conversas da fila | Acessar carteira fora da fila |
| Sucesso do cliente | Acompanhar implantação e uso dos clientes ativos | Alterar cobrança |
- Quem cria a proposta não aprova o próprio desconto (SDD 78, seção 2.2).

## 9. Exportação e auditoria
- Auditoria de emissão, envio, aprovação de desconto, aceite e recusa. Exportação: CSV e XLSX; PDF da proposta individual.

## 10. Estados de interface
- Carregando, vazio, sem resultado, erro, acesso negado. Lead `sem_consentimento` mostrado com aviso de que não recebe marketing.

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
- Alçada de desconto (lacuna L-23 do SDD 22).
- Prazo padrão de validade da proposta: **[Sem detalhamento]**.
