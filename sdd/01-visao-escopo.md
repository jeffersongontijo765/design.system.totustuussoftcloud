# 01 — Visão e Escopo

> Parte do [SDD v2](00-README.md).

---

## 1. Visão

Plataforma SaaS multi-tenant para o ecossistema educacional: mantenedoras (grupos educacionais), instituições (entities) e unidades físicas (units), com usuários de cada nível. Entrega uma aplicação web responsiva e uma API REST versionada.

## 2. Superfícies do produto

| Superfície | Público | Conteúdo |
|---|---|---|
| **Site público** | Visitantes, contratantes | Institucional, SEO, onboarding, central de ajuda, SAC |
| **Portal administrativo SaaS** | Administradores de entidade e unidade | Gestão acadêmica, pessoas, financeiro e módulos funcionais |
| **Portal do desenvolvedor** | Equipe da plataforma (master) | Operação global, feature flags, chaves de API, webhooks, auditoria, jobs |
| **Portal do professor** | Docentes | Turmas, notas, frequência, materiais |
| **Portal do aluno** | Estudantes | Notas, agenda, documentos |
| **Portal dos pais e responsáveis** | Responsáveis legais | Acompanhamento, financeiro do aluno, comunicação |
| **Portal de terceiros** | Parceiros com acesso delegado | Acesso restrito por contrato e escopo |
| **API REST v1** | Integrações e clientes técnicos | Ver [04-api.md](04-api.md) |

Número de portais: **6** (developer, SaaS acadêmico, professor, aluno, pais/responsáveis, terceiros), mais o site público.

## 3. Objetivos

1. Isolamento forte de dados, configuração e marca entre tenants.
2. Operação descentralizada por unidade, com permissões no contexto da unidade.
3. API versionada para o frontend, integrações e automações.
4. Segurança, rastreabilidade e privacidade desde o início, não como etapa posterior.
5. Internacionalização com inglês canônico e dez locales (ver [09](09-internacionalizacao.md)).

## 4. Escopo desta versão

| Item | Situação |
|---|---|
| Site público, SaaS administrativo, portais, API v1 | **[Declarado]** na v1 como implementados em grande parte; percentuais por área não foram reproduzidos. |
| Módulos funcionais | Catálogo e status em [12-catalogo-modulos.md](12-catalogo-modulos.md). |
| Autenticação, MFA, RBAC, sessões | Ver [06](06-identidade-acesso.md). |
| LGPD e direitos do titular | Ver [07](07-privacidade-lgpd.md). |

## 5. Fora de escopo

- Aplicativos nativos iOS e Android. Só web responsiva.
- Ativação de gateways de pagamento em produção. Adapters existem como integração; ativação depende de contrato e de revisão de segurança específica por provedor. A API expõe a criação de pagamento como contrato ([04](04-api.md)); o que fica fora é a ativação do provedor.
- Escolha de provedor de nuvem. Ver [10](10-implantacao-operacao.md).
- Ferramentas de agentes de IA usadas pela equipe de desenvolvimento. Ficam em [11](11-governanca-qualidade.md) como ferramentas de processo, não como requisito do produto.

## 6. Critérios de aceite de escopo

- [ ] Toda rota da aplicação aponta para um controller existente (verificação automatizada).
- [ ] Views renderizam sem aviso com dados vazios.
- [ ] Nenhum endpoint sem regra de autorização explícita (default-deny, ver [05](05-seguranca.md)).
- [ ] Testes de isolamento de tenant passam em CI.
- [ ] Chaves de `en` e `pt-BR` completas; demais locales seguem o teste de paridade de [09](09-internacionalizacao.md).

## 7. Métricas

As métricas da v1 (número de controllers, rotas, models, testes) **[Declaradas]** serão recalculadas por script em CI e publicadas como saída do pipeline, não como texto fixo no SDD.
