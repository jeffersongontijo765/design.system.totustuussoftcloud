# Tributos e obrigações fiscais da empresa

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Contábil da plataforma
- Domínio: plataforma (banco master). Mesmo código do fiscal da entidade, com outro dono de dado ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3)
- Escopo: tributos, retenções, obrigações fiscais e notas da empresa desenvolvedora
- Status: detalhado (SDD 18, 22, 31, 34 e v1), com pendências já registradas no SDD

## 1. Identificação
- Especificações: [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3 (tributos da empresa); [18](../../../docs/v2/18-regras-modulos-2.md), seção 6 (estados da obrigação); [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5 (papel Fiscal); [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 5 (notas); v1 [spec_gestao_contabil_fiscal_completo.md](../../../docs/v2/anexo-v1/spec_gestao_contabil_fiscal_completo.md), seções 6.3 a 6.5, 7.3, 9 e 12.
- Regra de fonte: onde a v1 e a v2 divergem, vale a v2.

## 2. Objetivo e escopo
Controlar os tributos, as retenções e as obrigações fiscais da própria empresa desenvolvedora, e as notas que ela emite e recebe. Não trata os tributos de nenhuma entidade.

## 3. Telas
- **Obrigações fiscais** (datatable; v1 seção 6.3). Colunas: obrigação, período, tributo, vencimento, situação, responsável, competência, protocolo, ações.
- **Kanban de obrigações** (v1 seção 9.1), com os estados da v2 (seção 4).
- **Calendário fiscal** (gerenciamento; v1 seção 12.1): obrigações e vencimentos da empresa.
- **Retenções e tributos** (datatable; v1 seção 6.5). Colunas: tributo, base, alíquota, valor calculado, valor retido, diferença, competência, situação, ações.
- **Documentos fiscais** (datatable; v1 seção 6.4). Colunas: número, série, tipo, emitente, destinatário, data, valor, imposto, situação, XML, ações.
  - **Notas emitidas pela empresa**: NFS-e da assinatura do SaaS cobrada das entidades. **Ausente** no SDD (pendência PAG-05 do [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md)).
  - **Notas recebidas de fornecedores**: recebidas e validadas, não emitidas aqui ([34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 5.3).
- **Drawer de obrigação** e **drawer de documento fiscal** (v1 seção 8): identificação, dados fiscais, anexos e XML, histórico, correção com motivo.

## 4. Dados
- Estados da obrigação fiscal ([18](../../../docs/v2/18-regras-modulos-2.md), seção 6.2): `pendente`, `transmitida`, `paga`. `em_atraso` é **calculado por data**, não gravado.
- Notas, XML e anexos guardados conforme [21](../../../docs/v2/21-busca-e-armazenamento.md).

## 5. Campos e validações
- Competência e período fiscal válidos ([18](../../../docs/v2/18-regras-modulos-2.md), seção 6.1).
- Consistência entre documento, lançamento e obrigação (v1 seção 11.1).
- Cancelamento de nota exige aprovação do contábil ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5).

## 6. Indicadores e gráficos
- Widgets (v1 seções 5.1 e 7.3): obrigações vencendo em 7 dias, obrigações em atraso, obrigações entregues, com protocolo e em análise; valor apurado por tributo; documentos fiscais processados.
- Gráficos (v1 seção 5.2): tributos apurados por competência; rosca da situação das obrigações; documentos por tipo.

## 7. Ações e confirmações
- Registrar obrigação, transmitir, registrar pagamento e protocolo; apurar tributo; importar documento fiscal; cancelar nota (com aprovação do contábil).
- Alerta antes do vencimento (v1 seção 10.1).

## 8. Permissões e papéis
- `platform.fiscal` (papel Fiscal do [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5): emitir e cancelar NFS-e, apurar tributos. Cancelamento aprovado por `platform.accounting` (papel Contábil).
- Códigos no [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 4.1.

## 9. Exportação e auditoria
- Auditoria: transmissão, pagamento, cancelamento, reprocessamento de obrigação e ajuste manual de valor (v1 seção 14.1). Exportação CSV, XLSX e PDF; XML das notas.

## 10. Estados de interface
- Carregando, vazio, sem resultado, erro, acesso negado, obrigação vencida (destaque calculado por data).

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.

## 12. Pendências e decisões
- **NFS-e da assinatura do SaaS:** pendência **PAG-05**, já registrada no [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md) (documento a escrever e parecer jurídico).
- **NF-e de produto:** fora de escopo, sem venda de produto ([34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 5.1).
- Lista de tributos e obrigações da empresa e regime tributário: **[Sem detalhamento]** (dado do contador da empresa, não regra do sistema).
- **Divergência v1 × v2:** a v1 marca atraso por automação; na v2 o atraso é calculado por data.
