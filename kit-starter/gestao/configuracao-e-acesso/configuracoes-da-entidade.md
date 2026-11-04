# Configurações da entidade

- Portal: Gestão (`gestao.`)
- Área: Configuração e acesso
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 2; [03](../../../docs/v2/03-dominio-tenancy.md), seção 5; [09](../../../docs/v2/09-internacionalizacao.md) (integral)
- Fonte da v1: absorvida integralmente em [configuracoes-do-sistema.md](../../desenvolvedor/seguranca-e-operacao/configuracoes-do-sistema.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Configurações da entidade e da unidade: idioma, fuso, feriados locais, parâmetros acadêmicos e financeiros, identidade visual.

## 3. Telas

- **Configurações** (página com grupos, cada um ligado ao documento do SDD que o rege; mudança com motivo e auditoria).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `entity.admin` e `unit.manager`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Configurações ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 2); por tenant ([03](../../../docs/v2/03-dominio-tenancy.md), seção 5); idiomas ([09](../../../docs/v2/09-internacionalizacao.md)).

## 7. Dados

- Tabelas e campos conforme a seção 13 e o DDL do [51](../../../docs/v2/51-ddl-modulos-novos.md), quando o módulo estiver lá. Toda tabela tem `entidade_id`, `unidade_id`, `created_at`, `updated_at`, `created_by` e exclusão lógica com `deleted_at` e `deleted_by` ([03](../../../docs/v2/03-dominio-tenancy.md), seção 6; [15](../../../docs/v2/15-validacoes.md); [19](../../../docs/v2/19-regras-modulos-3.md), seção 14).

## 8. Integrações

- Ver a seção de integrações do documento de origem, na seção 13.

## 9. Exportação, auditoria e privacidade

- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Toda criação, alteração, aprovação, exclusão lógica, exportação e leitura de dado sensível gera evento de auditoria no banco da unidade ([29](../../../docs/v2/29-auditoria.md)).
- Dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md): mínimo necessário, mascaramento em listas, base legal registrada.

## 10. Estados de interface

- Carregando (skeleton), vazio com chamada para ação, sem resultado de filtro, erro com nova tentativa, acesso negado, registro bloqueado, fechado ou baixado (somente leitura), conflito de edição (versão).

## 11. Requisitos de frontend

- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`): página de lista com DataTable, KPIs, drawer de detalhe, formulário em página ou modal, kanban quando houver fluxo de estados.
- Seletor de unidade no topo quando o usuário tiver mais de uma; a troca reemite o token com o novo contexto ([06](../../../docs/v2/06-identidade-acesso.md), seção 12).

## 12. Critérios de aceite e pendências

- Critérios de aceite: os do documento de origem (seção 13) e os de [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 6.
- Testes de isolamento: usuário de outra unidade ou entidade recebe 404 em toda rota do módulo ([03](../../../docs/v2/03-dominio-tenancy.md)).
- As pendências do documento de origem estão na seção 13 e consolidadas no [45](../../../docs/v2/45-pendencias-consolidadas.md).

## 13. Regras da v2 (texto integral das fontes, sem corte)

### 13.1 [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 2

#### 2. Configurações

| Item | Situação | Onde |
|---|---|---|
| Painel do aluno e do professor | Parcial | [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2. Sem tela de configuração |
| Agenda iScholar | Lacuna | Não está claro o que é. **Definir** |
| Número de matrícula | Lacuna | Regra de numeração não especificada. Ver [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) |
| Financeiro (configurações gerais) | Parcial | [18](../../../docs/v2/18-regras-modulos-2.md), [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md) |
| Mensagens de carnê | Lacuna | Modelo de carnê não especificado. Ver [53](../../../docs/v2/53-pacote-documentos-e-contratos.md), DC-25 |
| Mensagens de NFS-e | Parcial | [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 5 |
| Gerenciar feriados | Coberto | [58](../../../docs/v2/58-calendario-e-eventos-por-portal.md), seções 3 e 4: dia não letivo (feriado, recesso, ponto facultativo) no calendário da unidade |
| Campos personalizados | Coberto | [72](../../../docs/v2/72-campos-personalizados-por-portal.md) (CFG-06) |
| Matrícula online | Coberto | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 3 |
| Gerenciar tokens | Coberto | [06](../../../docs/v2/06-identidade-acesso.md) e [04](../../../docs/v2/04-api.md) |
| Fuso horário | Parcial | Horários em UTC, com exibição no fuso da unidade ([44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)). Configuração por unidade não especificada |
| Webhooks | Coberto | [16](../../../docs/v2/16-integracoes-externas.md), [04](../../../docs/v2/04-api.md) |
| Gerenciar IES | Parcial | [03](../../../docs/v2/03-dominio-tenancy.md) cobre entidade e unidade. Cadastro de IES (credenciamento) não especificado |
| Preferências de comunicação | Parcial | Consentimento por finalidade em [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 3.2. Sem tela de canal preferido |
| Tipos de descontos | Parcial | [18](../../../docs/v2/18-regras-modulos-2.md), seção 2.6 (acumulação decidida). Tipos não listados |
| Catraca | Coberto | [35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md) |
| Tipos de justificativa de falta | Coberto | [61](../../../docs/v2/61-diario-escolar-por-portal.md), seção 4.2 |
| Integração de parceiros | Coberto | [16](../../../docs/v2/16-integracoes-externas.md) |
| Outras configurações | Não aplicável | Genérico |

### 13.2 [03](../../../docs/v2/03-dominio-tenancy.md), seção 5

#### 5. Configuração por tenant

| Configuração | Escopo | Observação |
|---|---|---|
| Marca (logo, cores, nome) | Entidade | Validação de imagem (ver [05](../../../docs/v2/05-seguranca.md)) |
| Locale padrão e moeda | Entidade | Moeda USD/BRL é **[Declarado]**; outras moedas dependem de requisito |
| Política de senha e MFA | Mantenedora ou entidade | Não pode ser menos restritiva que a política da plataforma |
| Retenção de dados | Entidade | Mínimo e máximo definidos pela plataforma ([07](../../../docs/v2/07-privacidade-lgpd.md)) |
| Limites de API | Tenant | Ver [04](../../../docs/v2/04-api.md) |

### 13.3 [09 — Internacionalização e Localização](../../../docs/v2/09-internacionalizacao.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md).

---

#### 1. Locales

| Código | Idioma | Situação |
|---|---|---|
| `en` | Inglês (canônico) | Fonte de todas as chaves |
| `pt-BR` | Português (Brasil) | Locale padrão do produto |
| `es`, `fr`, `de`, `it`, `zh`, `ja`, `ru`, `ar` | Demais idiomas | Tradução por fornecedor com revisão nativa |

A v1 declara 100% de chaves em dez locales, verificado em 04/08/2026 por testes. **[Declarado]**: a v2 exige que o teste seja executado em CI, e o número é gerado pelo teste, não digitado no SDD.

#### 2. Regras

1. Chave canônica em inglês, em `snake.case` com namespace por módulo: `academico.nota.salvar`.
2. Nenhum texto visível fixo no código ou em template.
3. Plural e gênero por ICU MessageFormat. Não concatenar fragmentos de frase.
4. Datas, horas, números e moeda por `Intl` do locale. Moeda do tenant é independente do idioma.
5. Fallback: idioma do usuário → idioma do tenant → `en`. Chave ausente em locale não canônico gera aviso em CI, não erro em produção.
6. Ordem de precedência do locale: preferência do usuário > parâmetro de locale do tenant > cabeçalho `Accept-Language` > padrão do produto.
7. Variável `APP_LOCALE` forçada (uso em instalação dedicada) desativa a troca pelo usuário e deve aparecer no painel de configuração.

#### 3. RTL (árabe)

- `dir="rtl"` no elemento `html` quando o locale é `ar`.
- Propriedades lógicas em CSS (`margin-inline-start`, `inline-end`) no lugar de esquerda e direita.
- Ícones direcionais (setas, avanço) espelhados; ícones de marca e de mídia não.
- Teste visual em RTL para cada tela nova.

#### 4. Governança de tradução

- Fornecedor de tradução com contrato de confidencialidade. Texto de tela não contém dado pessoal real.
- Glossário por idioma com termos do domínio educacional (matrícula, mantenedora, unidade etc.).
- Revisão nativa antes de publicar. Tradução automática não é publicada sem revisão.
- Mudança de texto em `en` gera tarefa de tradução para os demais locales com prazo.

#### 5. Critérios de aceite

- [ ] Teste de paridade: todas as chaves de `en` existem nos dez locales ou têm marca de pendência explícita.
- [ ] Teste de placeholders: mesmos parâmetros em todos os locales.
- [ ] Teste de layout em `ar` em telas de formulário e tabela.
- [ ] Nenhum texto fixo detectado por varredura do código de views.
