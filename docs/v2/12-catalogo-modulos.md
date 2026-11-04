# 12 — Catálogo de Módulos

> Parte do [SDD v2](00-README.md). Status baseado na presença de especificação na pasta do SDD; implementação não foi verificada nesta versão.

---

## 1. Como usar

Cada módulo tem uma especificação de origem (v1). A v2 não reescreve todas as especificações de uma vez. Ela define o catálogo, o status e o caminho de consolidação. Ao tocar em um módulo, a especificação é revisada com o template dos documentos 01 a 11 antes da implementação.

Legenda de status: **Especificado** (há documento), **Revisar** (documento antigo ou duplicado), **Planejado** (sem documento).

## 2. Módulos

| Módulo | Especificação de origem (v1) | Status v2 | Observação |
|---|---|---|---|
| Acadêmico | [`spec_gestao_academica_completo.md`](anexo-v1/spec_gestao_academica_completo.md) | Especificado | Maior documento de módulo; quebrar por sub-domínio |
| Armazenamento | [`spec_gestao_armazenamento_completo.md`](anexo-v1/spec_gestao_armazenamento_completo.md), [`spec_object_storage_digital_assets.md`](anexo-v1/spec_object_storage_digital_assets.md) | Revisar | Dois documentos com escopo sobreposto |
| Auditoria | [`spec_gestao_auditoria_completo.md`](anexo-v1/spec_gestao_auditoria_completo.md) | Especificado | Ligar a [05](05-seguranca.md) e [07](07-privacidade-lgpd.md) |
| Autenticação | [`spec_gestao_autenticacao_completo.md`](anexo-v1/spec_gestao_autenticacao_completo.md) | Revisar | Substituído em parte por [06](06-identidade-acesso.md); manter só o que é específico do módulo |
| Bancos (administração de banco de dados) | [`spec_gestao_bancos.md`](anexo-v1/spec_gestao_bancos.md), [`spec_gestao_bancos_completo.md`](anexo-v1/spec_gestao_bancos_completo.md) | Removido do escopo | Não é módulo de dados bancários: é ferramenta de banco de dados com console SQL. Fora do produto. Ver [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 4 |
| Biblioteca acadêmica | [`spec_gestao_biblioteca_academica.md`](anexo-v1/spec_gestao_biblioteca_academica.md), [`spec_gestao_biblioteca_completo.md`](anexo-v1/spec_gestao_biblioteca_completo.md) | Revisar | Duplicado |
| Billing e cobrança | [`spec_gestao_billing_cobranca_mensalidades.md`](anexo-v1/spec_gestao_billing_cobranca_mensalidades.md) | Especificado | Adapters de pagamento: revisão de segurança por provedor |
| Chat rápido e SAC | [`spec_chat_rapido_sac.md`](anexo-v1/spec_chat_rapido_sac.md), [`SPEC-HELPDESK.md`](anexo-v1/SPEC-HELPDESK.md), [`spec_gestao_sac_base_conhecimento.md`](anexo-v1/spec_gestao_sac_base_conhecimento.md) | Revisar | Três documentos de atendimento |
| Client migration | [`client-migration-module-spec-completo.md`](anexo-v1/client-migration-module-spec-completo.md) | Especificado | Migração de dados entre tenants: exige revisão de isolamento |
| Contábil e fiscal | [`spec_gestao_contabil_fiscal_completo.md`](anexo-v1/spec_gestao_contabil_fiscal_completo.md) | Especificado | Conformidade fiscal: **(jurídico/contábil)** |
| Contratos | [`spec_gestao_contratos_completo.md`](anexo-v1/spec_gestao_contratos_completo.md) | Especificado | |
| Cookies e sessões | [`spec_gestao_cookies_sessions.md`](anexo-v1/spec_gestao_cookies_sessions.md) | Revisar | Conteúdo coberto por [06](06-identidade-acesso.md) |
| CRM e funil comercial | [`spec_crm_funil_comercial.md`](anexo-v1/spec_crm_funil_comercial.md) | Especificado | |
| Documentos | [`spec_gestao_documentos_completo.md`](anexo-v1/spec_gestao_documentos_completo.md), [`spec-builder-documentos-academicos.md`](anexo-v1/spec-builder-documentos-academicos.md) | Revisar | Duas especificações de documentos |
| Financeiro | [`spec_gestao_financeiro_completo.md`](anexo-v1/spec_gestao_financeiro_completo.md) | Especificado | |
| Frotas | [`spec_gestao_frotas_completo.md`](anexo-v1/spec_gestao_frotas_completo.md) | Especificado | Módulo de escopo diferente do produto educacional: confirmar se entra nesta versão |
| Governança de integrações | [`spec_complementar_integracoes_governanca.md`](anexo-v1/spec_complementar_integracoes_governanca.md) | Especificado | Ligar a [04](04-api.md) seção 7 |
| Interface de biblioteca (UI) | [`spec_gestao_biblioteca_completo.md`](anexo-v1/spec_gestao_biblioteca_completo.md) | Revisar | Título indica UI; separar da especificação de domínio |
| Layout de tickets | [`SPEC-LAYOUT-TICKET.md`](anexo-v1/SPEC-LAYOUT-TICKET.md) | Especificado | |
| Logger | [`spec_gestao_logger_completo.md`](anexo-v1/spec_gestao_logger_completo.md) | Revisar | Ler [10](10-implantacao-operacao.md) seção 7 antes; retirar dados de log da especificação |
| Marketing e redes sociais | [`spec_gestao_marketing_redes_sociais.md`](anexo-v1/spec_gestao_marketing_redes_sociais.md) | Especificado | Consentimento ([07](07-privacidade-lgpd.md)) |
| Notificações | [`spec_gestao_notificacoes.md`](anexo-v1/spec_gestao_notificacoes.md), [`spec_gestao_notificacoes_revisada.md`](anexo-v1/spec_gestao_notificacoes_revisada.md) | Revisar | Manter a revisada e arquivar a outra |
| Pessoas (HCM) | [`spec_gestao_pessoas_completo.md`](anexo-v1/spec_gestao_pessoas_completo.md) | Especificado | Dados de saúde e sensíveis: [07](07-privacidade-lgpd.md) seção 2 |
| Patrimônio | [`spec_patrimonio_completo.md`](anexo-v1/spec_patrimonio_completo.md) | Especificado | |
| Preceptoria e autoavaliação | [`spec-gestao-preceptoria-autoavaliacao.md`](anexo-v1/spec-gestao-preceptoria-autoavaliacao.md) e "Preceptoria PRO" da navegação | Especificação parcial, reclassificada | [42](42-preceptoria-por-portal.md). Nome em conflito (seção 2) |
| Formulários e pesquisas (motor) | Sem especificação própria na v1. Editores de avaliação e questionários feitos à parte | Especificado em v2 | [41](41-formularios-e-pesquisas.md). Usado por preceptoria, RH, pastoral e atendimento |
| Gestão pastoral PRO | Lista de nomes na navegação da v1, sem especificação | Especificado em v2 | [43](43-pastoral-por-portal.md). Confissões só como horário público, sem registro de pessoa |
| Agendamento de ambientes e equipamentos | "Agendamento Espaços PRO" na navegação da v1, sem especificação | Especificado em v2 | [44](44-agendamento-ambientes-equipamentos.md) |
| Aulas online e reuniões ao vivo | [`global_meeting_spec_v2_complete.md`](anexo-v1/global_meeting_spec_v2_complete.md) (v1, genérica) | Especificado em v2 | [40](40-aulas-online-por-portal.md). Mídia em [10](10-implantacao-operacao.md), seção 10 |
| Matrícula e rematrícula | [`spec_gestao_academica_completo.md`](anexo-v1/spec_gestao_academica_completo.md), seção 4 | Especificado em v2 | [46](46-matricula-e-rematricula-por-portal.md). Fecha M-01 a M-09 |
| Simulados e correção de redação | [`spec_gestao_simulados_ia.md`](anexo-v1/spec_gestao_simulados_ia.md) | Especificado em v2 | [47](47-simulados-por-portal.md). Nota da IA é sugestão |
| Gerador de documentos | [`spec-builder-documentos-academicos.md`](anexo-v1/spec-builder-documentos-academicos.md), [`spec_gestao_documentos_completo.md`](anexo-v1/spec_gestao_documentos_completo.md) | Especificado em v2 | [48](48-gerador-de-documentos-por-portal.md). Une as duas especificações da v1 |
| Logs, testes e acessibilidade | Sem especificação na v1 | Especificado em v2 | [49](49-logs-testes-por-portal.md) |
| Privacidade global | [`spec_gestao_privacy_global_completo.md`](anexo-v1/spec_gestao_privacy_global_completo.md), [`spec-sub-sidebar-privacidade-lgpd.md`](anexo-v1/spec-sub-sidebar-privacidade-lgpd.md) | Revisar | Consolidar com [07](07-privacidade-lgpd.md) |
| Recursos humanos | [`spec_gestao_rh_completo.md`](anexo-v1/spec_gestao_rh_completo.md) | Revisar | Sobrepõe-se a Pessoas (HCM); decidir fronteira |
| Segurança e medicina do trabalho | [`spec_gestao_seguranca_medicina_trabalho_completo.md`](anexo-v1/spec_gestao_seguranca_medicina_trabalho_completo.md) | Especificado | Dado de saúde ocupacional: sensível |
| Simulados com IA | [`spec_gestao_simulados_ia.md`](anexo-v1/spec_gestao_simulados_ia.md) | Especificado | Uso de IA: registrar provedor, dados enviados e retenção pelo provedor |
| Soft delete | [`spec-soft-delete-totustuus.md`](anexo-v1/spec-soft-delete-totustuus.md) | Especificado | Regra transversal; referenciada em [03](03-dominio-tenancy.md) |
| Suprimentos | [`spec_gestao_suprimentos_v3_consolidado.md`](anexo-v1/spec_gestao_suprimentos_v3_consolidado.md) | Especificado | Versão "consolidado" pode ter absorvido v1 e v2 |
| TI e ITSM | [`spec_gestao_ti_completa.md`](anexo-v1/spec_gestao_ti_completa.md), [`sub_sidebar_itsm.php`](anexo-v1/sub_sidebar_itsm.php) | Revisar | O arquivo `.php` é código de view, não especificação. Mover para o repositório de código. |
| Build e SLSA | [`slsa-build-spec.md`](anexo-v1/slsa-build-spec.md) | Especificado | Ligar a [10](10-implantacao-operacao.md) |
| Penetration test | [`penetration-test-spec-v2.md`](anexo-v1/penetration-test-spec-v2.md) | Especificado | Ligar a [05](05-seguranca.md) seção 7 |
| Ensino (arquitetura SaaS educação) | [`spec_education_saas_architecture.md`](anexo-v1/spec_education_saas_architecture.md) | Revisar | Parte de [02](02-arquitetura.md) e [03](03-dominio-tenancy.md) |
| Idiomas e seletor de locale | [`language_locale_selector_spec.md`](anexo-v1/language_locale_selector_spec.md), [`06-i18n-l10n.md`](anexo-v1/06-i18n-l10n.md) | Revisar | Consolidar em [09](09-internacionalizacao.md) |
| Chart builder | [`chart-builder-spec-complete.md`](anexo-v1/chart-builder-spec-complete.md) | Especificado | |
| Reunião global | [`global_meeting_spec_v2_complete.md`](anexo-v1/global_meeting_spec_v2_complete.md) | Especificação genérica da v1, não aderente aos portais | Aula online e sessões com menores em [40](40-aulas-online-por-portal.md) |
| Tarefas | [`TASKS_SPECS.md`](anexo-v1/TASKS_SPECS.md) | Revisar | Lista de tarefas, não especificação; converter em backlog |
| Tela de sidebar e navegação | [`12-portals-navigation-sidebar-pages-spec.md`](anexo-v1/12-portals-navigation-sidebar-pages-spec.md) | Revisar | Parte de [08](08-frontend-design-system.md) |

## 3. Arquivos que não são especificações

| Arquivo | Problema | Destino |
|---|---|---|
| `teste.html` | Página de teste com CDN | Remover ou mover para repositório de código como exemplo fora do build |
| [`sub_sidebar_itsm.php`](anexo-v1/sub_sidebar_itsm.php) | Código de view com `onclick=` | Repositório de código; ver ACH-01 em [13](13-achados-v1.md) |
| [`TASKS_SPECS.md`](anexo-v1/TASKS_SPECS.md) | Lista de tarefas | Backlog de [11](11-governanca-qualidade.md) |

## 4. Documentos da v1 substituídos pela v2

| Documento da v1 | Substituto na v2 |
|---|---|
| [`01-vision-scope.md`](anexo-v1/01-vision-scope.md) | [01](01-visao-escopo.md) |
| [`02-solution-architecture.md`](anexo-v1/02-solution-architecture.md) | [02](02-arquitetura.md) |
| [`03-domain-model.md`](anexo-v1/03-domain-model.md) | [03](03-dominio-tenancy.md) |
| [`04-api-standards.md`](anexo-v1/04-api-standards.md) | [04](04-api.md) |
| [`05-security-architecture.md`](anexo-v1/05-security-architecture.md) | [05](05-seguranca.md) |
| [`06-tenancy.md`](anexo-v1/06-tenancy.md) | [03](03-dominio-tenancy.md) |
| [`06-i18n-l10n.md`](anexo-v1/06-i18n-l10n.md) | [09](09-internacionalizacao.md) |
| [`07-identity-auth.md`](anexo-v1/07-identity-auth.md) | [06](06-identidade-acesso.md) |
| [`08-privacy-lgpd.md`](anexo-v1/08-privacy-lgpd.md) | [07](07-privacidade-lgpd.md) |
| [`09-deployment-ops.md`](anexo-v1/09-deployment-ops.md) | [10](10-implantacao-operacao.md) |
| [`10-governance-delivery.md`](anexo-v1/10-governance-delivery.md) | [11](11-governanca-qualidade.md) |
| [`11-frontend-design-system-master-model.md`](anexo-v1/11-frontend-design-system-master-model.md) | [08](08-frontend-design-system.md) |
| [`sdd-mestre-php8-mvc-saas.md`](anexo-v1/sdd-mestre-php8-mvc-saas.md) | [00](00-README.md) e [02](02-arquitetura.md) |
