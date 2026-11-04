# 79 — Rastreabilidade v1 → v2

> Parte do [SDD v2](00-README.md). Gerado por `inventario/gera_rastreabilidade.py`. Não editar à mão: regere depois de mudar o catálogo ou um documento.
> **Objetivo:** mostrar, para cada arquivo da v1 (em [anexo-v1/](anexo-v1/)), para onde foi o conteúdo na v2 e o que ainda não foi absorvido. Nada da v1 fica sem destino declarado.

## 1. Como ler

- **Substituído:** o documento da v2 indicado cobre o assunto. A v1 fica só como histórico.
- **Absorvido em parte:** documentos da v2 citam e usam a especificação, mas não a reescreveram inteira. Ao implementar o módulo, ler a v1 no anexo e a v2 juntas; vale a v2 em caso de conflito.
- **Só catalogado:** o catálogo registra o arquivo, mas nenhum documento da v2 usa o conteúdo. **Ler no anexo antes de implementar** e trazer as regras para a v2.
- **Não é especificação:** arquivo de código ou de tarefas, com destino indicado.
- **Fora do escopo:** removido do produto por decisão registrada.
- **Absorvido integralmente no kit-starter:** o texto completo está dentro da ficha indicada, com as correções da v2 por cima.
- **Arquivo vazio:** placeholder sem conteúdo.
- **LACUNA:** não citado em lugar nenhum da v2. Precisa de decisão.

## 2. Resumo

| Situação | Arquivos |
|---|---|
| Absorvido integralmente no kit-starter | 20 |
| Absorvido em parte em | 20 |
| Substituído | 12 |
| Só catalogado | 7 |
| Fora do escopo do produto | 2 |
| Arquivo vazio (placeholder), sem conteúdo a absorver | 1 |

## 3. Arquivo por arquivo

| Arquivo da v1 | Linhas | Status no catálogo | Situação na v2 |
|---|---|---|---|
| [`01-vision-scope.md`](anexo-v1/01-vision-scope.md) | 62 | Substituído | Substituído por 01 |
| [`02-solution-architecture.md`](anexo-v1/02-solution-architecture.md) | 92 | Substituído | Substituído por 02 |
| [`03-domain-model.md`](anexo-v1/03-domain-model.md) | 55 | Substituído | Substituído por 03 |
| [`04-api-standards.md`](anexo-v1/04-api-standards.md) | 78 | Substituído | Substituído por 04 |
| [`05-security-architecture.md`](anexo-v1/05-security-architecture.md) | 69 | Substituído | Substituído por 05 |
| [`06-i18n-l10n.md`](anexo-v1/06-i18n-l10n.md) | 223 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/seguranca-e-operacao/configuracoes-do-sistema.md |
| [`06-tenancy.md`](anexo-v1/06-tenancy.md) | 95 | Substituído | Substituído por 03 |
| [`07-identity-auth.md`](anexo-v1/07-identity-auth.md) | 75 | Substituído | Substituído por 06 |
| [`08-privacy-lgpd.md`](anexo-v1/08-privacy-lgpd.md) | 66 | Substituído | Substituído por 07 |
| [`09-deployment-ops.md`](anexo-v1/09-deployment-ops.md) | 72 | Substituído | Substituído por 10 |
| [`10-governance-delivery.md`](anexo-v1/10-governance-delivery.md) | 75 | Substituído | Substituído por 11 |
| [`11-frontend-design-system-master-model.md`](anexo-v1/11-frontend-design-system-master-model.md) | 260 | Substituído | Substituído por 08 |
| [`12-portals-navigation-sidebar-pages-spec.md`](anexo-v1/12-portals-navigation-sidebar-pages-spec.md) | 279 | Revisar | Absorvido em parte em: 31, 34, 36, 40, 42, 43, 44 |
| [`chart-builder-spec-complete.md`](anexo-v1/chart-builder-spec-complete.md) | 1499 | Especificado | Absorvido em parte em: 31 |
| [`client-migration-module-spec-completo.md`](anexo-v1/client-migration-module-spec-completo.md) | 1207 | Especificado | Só catalogado: conteúdo ainda não absorvido na v2 (ler no anexo antes de implementar) |
| [`global_meeting_spec_v2_complete.md`](anexo-v1/global_meeting_spec_v2_complete.md) | 620 | Especificado em v2 | Absorvido em parte em: 31, 40 |
| [`language_locale_selector_spec.md`](anexo-v1/language_locale_selector_spec.md) | 387 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/seguranca-e-operacao/configuracoes-do-sistema.md |
| [`penetration-test-spec-v2.md`](anexo-v1/penetration-test-spec-v2.md) | 529 | Especificado | Absorvido em parte em: 24 |
| [`sdd-mestre-php8-mvc-saas.md`](anexo-v1/sdd-mestre-php8-mvc-saas.md) | 535 | Substituído | Substituído por 00 e 02 |
| [`slsa-build-spec.md`](anexo-v1/slsa-build-spec.md) | 356 | Especificado | Só catalogado: conteúdo ainda não absorvido na v2 (ler no anexo antes de implementar) |
| [`spec-builder-documentos-academicos.md`](anexo-v1/spec-builder-documentos-academicos.md) | 896 | Revisar | Absorvido em parte em: 31, 48 |
| [`spec-gestao-preceptoria-autoavaliacao.md`](anexo-v1/spec-gestao-preceptoria-autoavaliacao.md) | 409 | Especificação parcial, reclassificada | Absorvido em parte em: 42 |
| [`SPEC-HELPDESK.md`](anexo-v1/SPEC-HELPDESK.md) | 929 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/suporte/chamados-dos-clientes.md |
| [`SPEC-LAYOUT-TICKET.md`](anexo-v1/SPEC-LAYOUT-TICKET.md) | 350 | Especificado | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/suporte/chamados-dos-clientes.md |
| [`spec-soft-delete-totustuus.md`](anexo-v1/spec-soft-delete-totustuus.md) | 248 | Especificado | Só catalogado: conteúdo ainda não absorvido na v2 (ler no anexo antes de implementar) |
| [`spec-sub-sidebar-privacidade-lgpd.md`](anexo-v1/spec-sub-sidebar-privacidade-lgpd.md) | 321 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/seguranca-e-operacao/privacidade-dpo.md |
| [`spec_chat_rapido_sac.md`](anexo-v1/spec_chat_rapido_sac.md) | 294 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/suporte/chamados-dos-clientes.md |
| [`spec_complementar_integracoes_governanca.md`](anexo-v1/spec_complementar_integracoes_governanca.md) | 307 | Especificado | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/seguranca-e-operacao/integracoes-globais.md |
| [`spec_crm_funil_comercial.md`](anexo-v1/spec_crm_funil_comercial.md) | 244 | Especificado | Absorvido em parte em: 22 |
| [`spec_education_saas_architecture.md`](anexo-v1/spec_education_saas_architecture.md) | 729 | Revisar | Só catalogado: conteúdo ainda não absorvido na v2 (ler no anexo antes de implementar) |
| [`spec_gestao_academica_completo.md`](anexo-v1/spec_gestao_academica_completo.md) | 1382 | Especificado | Absorvido em parte em: 31, 40, 46, 55, 64, 65, 66, 67, 69, 70 |
| [`spec_gestao_armazenamento_completo.md`](anexo-v1/spec_gestao_armazenamento_completo.md) | 1380 | Revisar | Só catalogado: conteúdo ainda não absorvido na v2 (ler no anexo antes de implementar) |
| [`spec_gestao_auditoria_completo.md`](anexo-v1/spec_gestao_auditoria_completo.md) | 731 | Especificado | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/seguranca-e-operacao/auditoria.md |
| [`spec_gestao_autenticacao_completo.md`](anexo-v1/spec_gestao_autenticacao_completo.md) | 1001 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/seguranca-e-operacao/acesso.md |
| [`spec_gestao_bancos.md`](anexo-v1/spec_gestao_bancos.md) | 305 | Removido do escopo | Fora do escopo do produto |
| [`spec_gestao_bancos_completo.md`](anexo-v1/spec_gestao_bancos_completo.md) | 305 | Removido do escopo | Fora do escopo do produto |
| [`spec_gestao_biblioteca_academica.md`](anexo-v1/spec_gestao_biblioteca_academica.md) | 275 | Revisar | Absorvido em parte em: 68 |
| [`spec_gestao_biblioteca_completo.md`](anexo-v1/spec_gestao_biblioteca_completo.md) | 1182 | Revisar | Absorvido em parte em: 31, 68 |
| [`spec_gestao_billing_cobranca_mensalidades.md`](anexo-v1/spec_gestao_billing_cobranca_mensalidades.md) | 1433 | Especificado | Absorvido em parte em: 16, 18, 34 |
| [`spec_gestao_contabil_fiscal_completo.md`](anexo-v1/spec_gestao_contabil_fiscal_completo.md) | 294 | Especificado | Absorvido em parte em: 31 |
| [`spec_gestao_contratos_completo.md`](anexo-v1/spec_gestao_contratos_completo.md) | 1377 | Especificado | Absorvido em parte em: 33 |
| [`spec_gestao_cookies_sessions.md`](anexo-v1/spec_gestao_cookies_sessions.md) | 474 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/seguranca-e-operacao/acesso.md |
| [`spec_gestao_documentos_completo.md`](anexo-v1/spec_gestao_documentos_completo.md) | 546 | Revisar | Absorvido em parte em: 48 |
| [`spec_gestao_financeiro_completo.md`](anexo-v1/spec_gestao_financeiro_completo.md) | 1532 | Especificado | Absorvido em parte em: 71 |
| [`spec_gestao_frotas_completo.md`](anexo-v1/spec_gestao_frotas_completo.md) | 1558 | Especificado | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/operacoes-internas/frotas.md |
| [`spec_gestao_logger_completo.md`](anexo-v1/spec_gestao_logger_completo.md) | 1038 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/seguranca-e-operacao/auditoria.md |
| [`spec_gestao_marketing_redes_sociais.md`](anexo-v1/spec_gestao_marketing_redes_sociais.md) | 350 | Especificado | Só catalogado: conteúdo ainda não absorvido na v2 (ler no anexo antes de implementar) |
| [`spec_gestao_notificacoes.md`](anexo-v1/spec_gestao_notificacoes.md) | 378 | Revisar | Absorvido em parte em: 57 |
| [`spec_gestao_notificacoes_revisada.md`](anexo-v1/spec_gestao_notificacoes_revisada.md) | 642 | Revisar | Absorvido em parte em: 57 |
| [`spec_gestao_pessoas_completo.md`](anexo-v1/spec_gestao_pessoas_completo.md) | 1257 | Especificado | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/pessoas-da-plataforma/departamento-pessoal.md |
| [`spec_gestao_privacy_global_completo.md`](anexo-v1/spec_gestao_privacy_global_completo.md) | 345 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/seguranca-e-operacao/privacidade-dpo.md |
| [`spec_gestao_rh_completo.md`](anexo-v1/spec_gestao_rh_completo.md) | 1319 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/pessoas-da-plataforma/recursos-humanos.md |
| [`spec_gestao_sac_base_conhecimento.md`](anexo-v1/spec_gestao_sac_base_conhecimento.md) | 443 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/suporte/base-de-conhecimento.md |
| [`spec_gestao_seguranca_medicina_trabalho_completo.md`](anexo-v1/spec_gestao_seguranca_medicina_trabalho_completo.md) | 1581 | Especificado | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/pessoas-da-plataforma/medicina-e-seguranca-do-trabalho-da-empresa.md |
| [`spec_gestao_simulados_ia.md`](anexo-v1/spec_gestao_simulados_ia.md) | 683 | Especificado em v2 | Absorvido em parte em: 31, 47 |
| [`spec_gestao_suprimentos_v3_consolidado.md`](anexo-v1/spec_gestao_suprimentos_v3_consolidado.md) | 1271 | Especificado | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/operacoes-internas/suprimentos-da-empresa.md |
| [`spec_gestao_ti_completa.md`](anexo-v1/spec_gestao_ti_completa.md) | 882 | Revisar | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/seguranca-e-operacao/ti.md |
| [`spec_object_storage_digital_assets.md`](anexo-v1/spec_object_storage_digital_assets.md) | 237 | Revisar | Absorvido em parte em: 21 |
| [`spec_patrimonio_completo.md`](anexo-v1/spec_patrimonio_completo.md) | 1309 | Especificado | Absorvido integralmente no kit-starter: kit-starter/desenvolvedor/operacoes-internas/patrimonio.md |
| [`sub_sidebar_itsm.php`](anexo-v1/sub_sidebar_itsm.php) | 151 | Revisar | Absorvido em parte em: 36 |
| [`TASKS_SPECS.md`](anexo-v1/TASKS_SPECS.md) | 821 | Revisar | Só catalogado: conteúdo ainda não absorvido na v2 (ler no anexo antes de implementar) |
| [`teste`](anexo-v1/teste) | 1 | Vazio | Arquivo vazio (placeholder), sem conteúdo a absorver |
