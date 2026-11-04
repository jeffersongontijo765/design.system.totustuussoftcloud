# Emissão de documentos (gerador de documentos)

- Portal: Gestão (`gestao.`)
- Área: Secretaria
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md) (integral)
- Fonte da v1: [spec-builder-documentos-academicos.md](../../../docs/v2/anexo-v1/spec-builder-documentos-academicos.md) (896 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Emitir declarações, históricos, certidões, boletins oficiais e diplomas a partir de modelos aprovados, com elegibilidade, emissão em lote, assinatura, validação pública por código e revogação.

## 3. Telas

- **Emitir documento** (assistente): tipo, aluno ou lote, verificação de elegibilidade, pré-visualização, assinatura.
- **Documentos emitidos** (DataTable): código de validação, tipo, aluno, estado (seção 13, ciclo de vida), revogação.
- **Modelos** (lista; editor de modelo com aprovação, seção 13, 5 e 12).
- **Painel de assinaturas** (seção 13, 19).
- **Validação pública** (página sem login pelo código).
- **Configuração de impressão** (seção 13, 17).

## 4. Permissões por portal (extraídas do SDD)

Do [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Criar e publicar modelo, cancelar documento com motivo, ver relatório de emissão | Emitir sem papel de secretaria | E |
| **Secretaria** | Solicitar, emitir, assinar (quando for o caso), reemitir, cancelar com motivo | Alterar modelo publicado | E |

## 5. Papéis

- `unit.secretary`: emitir e revogar com motivo.
- `unit.manager`: aprovar modelo.
- `platform.developer`: publicar modelos-base, sem dado.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Modelo só é usado depois de aprovado; documento emitido é imutável e só é revogado com motivo (seção 13, 12 e 15).
- Editor de modelos do gerador **não é** o Editor de portais ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.4).

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

### 13.1 [48 — Gerador de Documentos, por Portal](../../../docs/v2/48-gerador-de-documentos-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Emissão de documento oficial da secretaria em [17](../../../docs/v2/17-regras-modulos.md) e [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md). Assinatura digital em [33](../../../docs/v2/33-contratos-por-portal.md), seção 4, e decisão CTR-06. Biblioteca e acervo, separados, em [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3. Armazenamento e checksum em [21](../../../docs/v2/21-busca-e-armazenamento.md). Auditoria em [29](../../../docs/v2/29-auditoria.md). Consulta pública e dado mínimo em [07](../../../docs/v2/07-privacidade-lgpd.md).
> **Status:** especificação proposta, criada em 03/11/2026 e verificada contra a v1 no mesmo dia (seção 11). **Escopo:** apenas documentos emitidos pela secretaria (contexto C de [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md)). Documentos recebidos e administrativos têm regras próprias a partir de [`spec-builder-documentos-academicos.md`](../../../docs/v2/anexo-v1/spec-builder-documentos-academicos.md) (editor de modelos, chamado de builder na v1: layout, variáveis, condicionais) e [`spec_gestao_documentos_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_documentos_completo.md) (tipos, ciclo de vida, assinatura, permissões). Fecha MOD-07 da [31](../../../docs/v2/31-matriz-portais-modulos.md). Itens **(jurídico)**, **(verificar)** e **[Decisão do autor]** dependem de resposta.

---

#### 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| O gerador de documentos está especificado? | **Em parte.** O editor de modelos (layout, papel, margens, cabeçalho, rodapé, variáveis, condicionais) está bem descrito. Falta DDL, regra de emissão, validação pública e a separação entre gerador e gestão de documentos |
| Há duplicidade? | **Sim.** A v1 tem duas especificações de documentos, uma do editor de modelos (builder) e outra de gestão. Este documento une as duas |
| Está organizado por portal? | **Não.** A v1 não diz quem pode solicitar, quem emite e quem vê |
| Biblioteca e documentos se misturam? | **Não, por decisão.** A biblioteca tem acervo e empréstimo. Documento é emitido pela secretaria. Ver [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3 |

---

#### 2. Separação de responsabilidades

| Parte | Função | Dono |
|---|---|---|
| Editor de modelos | Desenha o modelo: papel, margens, cabeçalho, corpo, rodapé, variáveis, condicionais | Gestão de documentos |
| Catálogo de tipos | Declaração, histórico, certificado, termo, ata, comunicado, contrato e outros | Gestão de documentos |
| Emissão | Gera o arquivo final a partir de um modelo publicado e de dados do aluno, pessoa ou entidade | Secretaria ou módulo de origem |
| Assinatura | Assina o arquivo emitido | Serviço de assinatura ([33](../../../docs/v2/33-contratos-por-portal.md)) |
| Validação pública | Confirma autenticidade por código ou QR, sem dado pessoal além do mínimo | Gestão de documentos |

---

#### 3. Tipos de documento

Tipos da v1 mantidos: declaração de matrícula, declaração de frequência, declaração de conclusão, declaração de quitação, histórico escolar, certidão de conclusão, segunda via, aditivo e contrato.

Tipos previstos na v1 e mantidos como expansão: termo de responsabilidade, requerimento, autorização, boleto com instruções, comunicado institucional, certificado, ata, relatório acadêmico, ficha cadastral, dossiê do aluno e declaração personalizada.

Cada tipo tem:

- Modelo publicado e versionado.
- Lista de variáveis obrigatórias.
- Quem pode solicitar e quem pode emitir.
- Se exige assinatura e de quem.
- Prazo de validade, quando houver.

---

#### 4. Ciclo de vida do documento emitido

`solicitado` → `em_emissao` → `emitido` → `aguardando_assinatura` → `assinado` ou `expirado` ou `cancelado`.

- `solicitado`: pedido do aluno, responsável, professor ou da própria secretaria, com protocolo ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md)).
- `emitido` sem assinatura: disponível para download, com código de validação.
- `expirado`: quando o documento tem validade e ela venceu. Calculado por data ([18](../../../docs/v2/18-regras-modulos-2.md), T-04).
- `cancelado`: só com motivo e evento de auditoria. O arquivo continua guardado.

Documento emitido não é editado. Correção gera novo documento, e o anterior vai para `cancelado`.

---

#### 5. Editor de modelos: regras de modelo

| Regra | Detalhe |
|---|---|
| Papel | Presets A4 e ofício, com configuração de tamanho personalizado. Unidade em mm, cm ou pt |
| Margens e recuos | Por página, com recuo de primeira linha e de parágrafo |
| Cabeçalho e rodapé | Campos fixos da entidade (nome, CNPJ, endereço, logotipo) e paginação |
| Variáveis | Grupos mínimos: aluno, responsável, turma, curso, matrícula, entidade, unidade, data. Variável sem dado na emissão bloqueia a emissão e aponta o campo |
| Condicionais | Bloco aparece só se a condição for verdadeira. Ex.: bloco de bolsa só se houver bolsa |
| Repetições | Lista de disciplinas, de notas ou de parcelas, com cabeçalho repetido por página |
| Publicação | Modelo só é publicado depois de revisão. Publicado não muda ([41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 2.3) |

Modelo não contém código executável. Condicional e repetição são interpretadas por um motor de regras limitado.

---

#### 6. Validação pública

- Cada documento emitido tem código de validação e QR apontando para uma página pública.
- A página confirma: tipo, data de emissão, situação atual (válido, expirado, cancelado) e a entidade emissora.
- A página **não** mostra nome do aluno, CPF ou nota. Para confirmar a pessoa, o consultante informa o código e a data de nascimento, e a consulta é limitada por taxa ([23](../../../docs/v2/23-dominios-provisionamento-ciclo-de-vida.md)).
- Cada consulta gera evento de auditoria sem o dado consultado.

---

#### 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos-padrão, sem dado | Ver documento emitido de qualquer entidade | P |
| **Gestão** | Criar e publicar modelo, cancelar documento com motivo, ver relatório de emissão | Emitir sem papel de secretaria | E |
| **Secretaria** | Solicitar, emitir, assinar (quando for o caso), reemitir, cancelar com motivo | Alterar modelo publicado | E |
| **Professor** | Solicitar documento de sua turma, ex.: declaração de frequência de aluno da turma | Emitir histórico ou documento oficial. Ver documento de outro aluno | E |
| **Aluno maior** | Solicitar e baixar os próprios documentos, com código de validação | Ver documento de outro aluno. Cancelar documento emitido | E |
| **Responsável** | Solicitar e baixar documentos de dependente com vínculo ativo | Ver documento de dependente sem vínculo. Cancelar documento emitido | E |
| **Terceiros** | Ver um documento emitido para ele, quando o contrato prevê (ex.: cartório recebe certidão) | Ver outros documentos | E, [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md) |
| **Público (consulta)** | Validar código e situação | Ver dado pessoal, nota ou conteúdo | Fora dos portais, seção 6 |

---

#### 8. Assinatura

- Documento que exige assinatura passa por `aguardando_assinatura` até todos os signatários assinarem.
- Provedor de assinatura: decisão CTR-06, aceitar provedores de terceiros e ter assinatura digital própria.
- Assinatura de documento oficial depende de exigência de cada tipo. Conferido em 03/11/2026 na Lei 14.063/2020 (planalto.gov.br):
  - **Níveis:** simples (identifica o signatário), avançada (certificado fora da ICP-Brasil ou outro meio aceito pelas partes, ligado ao signatário de forma unívoca e que detecta alteração) e qualificada (certificado ICP-Brasil) (art. 4º). O modelo de documento guarda o **nível mínimo** exigido, e o sistema recusa assinatura abaixo dele.
  - **Âmbito:** a lei vale para interações com ente público e dentro dele (art. 2º). Não vale entre particulares (art. 2º, parágrafo único, II, a). Cada Poder e ente define o nível mínimo por ato próprio (art. 5º). Por isso, em escola pública o nível de cada tipo vem do ato do ente, configurado pela entidade.
  - **Qualificada obrigatória:** atos de chefes de Poder e de titulares de órgão autônomo, nota fiscal eletrônica (salvo pessoa física e MEI), transferência e registro de imóvel, e demais casos em lei (art. 5º, § 2º). Atestado médico eletrônico e receita de controle especial também (art. 13). Em conflito entre normas, prevalece a qualificada (art. 5º, § 5º).
  - A lei não trata de diploma nem de histórico. A regra do diploma e do histórico digital do superior (normas do MEC) **(verificar)**.
  - **Entre particulares** (MP 2.200-2/2001, art. 10, conferido em 03/11/2026): documento assinado com certificado ICP-Brasil presume-se verdadeiro em relação ao signatário (§ 1º). Outro meio de comprovação de autoria e integridade vale se admitido pelas partes ou aceito por quem recebe o documento (§ 2º). Por isso, contrato e termo entre a escola privada e a família podem usar assinatura avançada, com a aceitação registrada no próprio contrato.
- O arquivo assinado guarda o checksum do conteúdo emitido ([21](../../../docs/v2/21-busca-e-armazenamento.md)).

---

#### 9. Pendências

| # | Pendência | Tipo |
|---|---|---|
| DOC-01 | Quais tipos exigem assinatura com certificado ICP-Brasil (seção 8) | **Conferido** em parte em 03/11/2026: níveis e casos obrigatórios na Lei 14.063/2020, arts. 2º, 4º, 5º e 13. MP 2.200-2/2001, art. 10, conferida. Faltam as normas do MEC para diploma e histórico digital **(verificar)**. Lista final por tipo com o (jurídico) |
| DOC-02 | Prazo de guarda de cada tipo emitido (histórico, declaração, certidão) | (jurídico) |
| DOC-03 | Layout oficial do histórico escolar, conforme norma do sistema de ensino (Res. CNE/CEB, citada na v1) | (verificar) |
| DOC-04 | Validade de declaração, por tipo | **Decidido** em 03/11/2026: 90 dias quando o tipo não define prazo |
| DOC-05 | Limite de consultas públicas de validação por código, por minuto | **Decidido** em 03/11/2026: 10 por minuto por endereço |
| DOC-06 | DDL de tipo, modelo, versão, documento emitido, assinatura e validação | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 12. Revisão do owner pendente (DDL-01) |

---

#### 10. Critérios de aceite

- [ ] Modelo com variável sem dado não emite e aponta o campo (teste).
- [ ] Modelo publicado não muda, e correção gera novo documento (teste).
- [ ] Consulta pública não retorna nome, CPF ou nota (varredura).
- [ ] Responsável não baixa documento de dependente sem vínculo ativo (teste de isolamento).
- [ ] Cancelamento de documento exige motivo e gera evento de auditoria (teste).
- [ ] Itens **(jurídico)**, **(verificar)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).

---

#### 11. Verificação contra a v1 e lacunas fechadas

Verificado em 03/11/2026 contra [`spec-builder-documentos-academicos.md`](../../../docs/v2/anexo-v1/spec-builder-documentos-academicos.md) e [`spec_gestao_documentos_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_documentos_completo.md). A versão anterior deste documento cobria o núcleo (tipos, ciclo, editor de modelos, validação e portais), mas deixava de fora itens da v1. Os itens abaixo foram incluídos nas seções 12 a 19.

| Item da v1 | Situação antes | Onde agora |
|---|---|---|
| Aprovação de modelo, com revisor distinto de quem criou | Faltava | Seção 12 |
| Regras de elegibilidade com severidades | Faltava | Seção 13 |
| Emissão em lote | Faltava | Seção 14 |
| Revogação como ato separado do cancelamento | Faltava | Seção 15 |
| Biblioteca de componentes reutilizáveis | Faltava | Seção 16 |
| Configuração de impressão | Faltava | Seção 17 |
| Auditoria: lista completa de ações | Parcial | Seção 18 |
| Automações e painel de assinaturas | Faltava | Seção 19 |
| Interface da API e DDL | Faltava | Seções 20 e 21 |

---

#### 12. Aprovação de modelo

Estados do modelo: `rascunho` → `em_revisao` → `publicado` → `arquivado`.

- Quem cria o modelo não aprova o próprio modelo. A regra é verificada no banco, com a mesma técnica do `CHECK (created_by <> approved_by)` de [37](../../../docs/v2/37-planejamento-e-empenho.md).
- A revisão confere layout, variáveis e regras. Não confere o texto jurídico, que é responsabilidade do jurídico da entidade.
- Modelo publicado não muda. Mudança gera nova versão em `rascunho`.

---

#### 13. Elegibilidade para emissão

Cada tipo de documento tem regras de elegibilidade. A regra roda antes da geração.

| Tipo de regra | Exemplo | Severidade |
|---|---|---|
| Vínculo | Declaração de matrícula só para matrícula ativa | Bloqueante |
| Vigência | Aditivo só com contrato vigente | Bloqueante |
| Situação financeira | Declaração de quitação só sem parcela vencida | Bloqueante |
| Solicitação | Transferência só com pedido deferido | Bloqueante |
| Cadastro incompleto | Campo opcional do modelo vazio | Alerta |
| Dado desatualizado | Endereço com mais de um ano | Informativa |

Bloqueante impede a emissão e mostra o motivo. Alerta permite emitir com confirmação. Informativa só aparece no preview.

---

#### 14. Emissão em lote

- A secretaria seleciona um tipo e um conjunto de alunos, por turma, série ou filtro.
- O sistema roda a elegibilidade para cada aluno e separa: emitidos, bloqueados e com alerta.
- Lote gera um protocolo por documento, não um protocolo único.
- Falha em um aluno não cancela o lote. O relatório final lista o que falhou e o motivo.
- O lote tem limite de tamanho por execução, e roda em fila ([14](../../../docs/v2/14-integracao-modulos.md)).

---

#### 15. Revogação

Revogação é diferente de cancelamento:

- **Cancelamento:** o documento foi emitido por erro, antes de ser usado. Sai da validação com o motivo.
- **Revogação:** o documento foi emitido corretamente, mas a situação mudou (ex.: matrícula cancelada depois da declaração). A validação pública mostra "revogado" e a data.

Os dois exigem motivo e evento de auditoria. O arquivo nunca é apagado.

---

#### 16. Componentes reutilizáveis

Biblioteca por entidade, com componentes como cabeçalho institucional, rodapé de autenticação, bloco de assinatura da secretaria, tabela de disciplinas, caixa de LGPD e termo de ciência.

Cada componente tem nome, categoria, versão, estrutura, estilos, variáveis esperadas, dependências e escopo (entidade ou unidade). Alterar um componente gera nova versão. Os modelos que usam o componente escolhem a versão na publicação.

---

#### 17. Configuração de impressão

| Recurso | Regra |
|---|---|
| Margens espelhadas | Para documento frente e verso |
| Altura de cabeçalho e rodapé | Fixa em milímetros, por modelo |
| Quebra de página | Bloco não se divide entre páginas quando marcado |
| Fonte | Embutida no PDF. Fonte não embutida bloqueia a emissão |
| Assinatura visível | Campo de assinatura com área reservada, na última página |
| Número de página | Formato "página X de Y" em todas as páginas |

O PDF é gerado com a mesma versão do modelo que foi publicada na data da emissão.

---

#### 18. Auditoria: ações obrigatórias

Toda ação gera evento em [29](../../../docs/v2/29-auditoria.md), com os campos da seção 2 daquele documento e o campo `portal`:

criação de tipo · criação de modelo · edição de versão · envio para revisão · aprovação · publicação · preview · emissão · emissão em lote · reemissão · cancelamento · revogação · validação pública · download · alteração de regra · alteração de componente.

Validação pública registra a consulta sem o dado consultado ([29](../../../docs/v2/29-auditoria.md), seção 6).

---

#### 19. Automações e painel de assinaturas

- Documento aguardando assinatura há 3 dias: lembrete ao signatário.
- Documento expirado sem assinatura: aviso à secretaria, com opção de reenviar.
- Modelo em revisão há 5 dias úteis: lembrete ao revisor.
- Painel da secretaria: documentos aguardando assinatura, por signatário, e expirados. Gráfico de assinaturas concluídas por mês.

Prazos de lembrete são valores iniciais, ajustáveis pela entidade.

---

#### 20. Interface da API

| Método | Caminho | Função |
|---|---|---|
| GET, POST | `/documentos/tipos` | Listar e criar tipo |
| PUT | `/documentos/tipos/{uuid}` | Editar tipo |
| GET, POST | `/documentos/modelos` | Listar e criar modelo |
| POST | `/documentos/modelos/{uuid}/versoes` | Nova versão |
| POST | `/documentos/modelos/{uuid}/revisao` | Enviar para revisão |
| POST | `/documentos/modelos/{uuid}/publicacao` | Publicar (aprovador distinto do criador) |
| POST | `/documentos/emissoes` | Emitir um documento |
| POST | `/documentos/emissoes/lote` | Emitir em lote |
| POST | `/documentos/emissoes/{uuid}/cancelamento` | Cancelar, com motivo |
| POST | `/documentos/emissoes/{uuid}/revogacao` | Revogar, com motivo |
| GET | `/validar/{codigo}` | Validação pública, sem dado pessoal |

Todos os endpoints exigem permissão por ação e escopo. A validação pública tem limite de consultas (DOC-05).

---

#### 21. DDL

As tabelas do módulo estão em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 12 (tipos, modelos, versões, emissões, validação, revogação e componentes). Este documento não repete o DDL.

---

#### 22. Pendências desta verificação

| # | Pendência | Tipo |
|---|---|---|
| DOC-07 | Prazos de lembrete de assinatura e de revisão (seção 19) | Valor inicial, ajustável |
| DOC-08 | Limite de tamanho do lote (seção 14) | Operação, em homologação |

## 14. Conteúdo integral da v1 (absorvido)

### Especificação Completa — Gestão de Documentos Acadêmicos + Builder Universal de Documentos

Documento funcional e técnico para criação, configuração, versionamento, renderização, emissão e validação de qualquer documento acadêmico, administrativo, financeiro ou contratual, com suporte a builder visual, layout de impressão avançado, múltiplos tamanhos de papel, cabeçalho, rodapé, margens, identação, paginação e regras de negócio.

- Language Standard: Global English
Baseado na tela observada em **Secretaria > Modelos de documentos**, com filtros por período letivo, unidade, turma e aluno, e agrupamento por tipo documental como aditivo, contratos e declarações. [cite:1]

[image:1]

#### 1. Visão geral

O módulo deve permitir que a instituição crie, mantenha e emita documentos padronizados a partir de modelos reutilizáveis, parametrizados e versionados. A tela atual indica um catálogo de modelos por tipo documental com contexto acadêmico por período, unidade, turma e aluno, o que exige um motor de geração contextual e rastreável. [cite:1]

O objetivo não é apenas armazenar arquivos, mas prover uma plataforma de **Document Template Management + Document Builder + Rendering Engine + Issuance Workflow**, capaz de atender desde uma declaração simples até contratos complexos com assinatura, QR code, múltiplas páginas e requisitos formais de impressão.

#### 2. Objetivos do módulo

- Padronizar todos os documentos institucionais.
- Eliminar edição manual repetitiva em Word, LibreOffice ou editores externos.
- Permitir criação de modelos com baixa dependência técnica.
- Garantir versionamento, aprovação e trilha de auditoria.
- Possibilitar emissão individual ou em lote.
- Suportar layout profissional de impressão e PDF.
- Adaptar o mesmo builder para qualquer formato de papel.
- Atender cenários multiunidade, multicurso e multientidade.

#### 3. Escopo funcional

O módulo deve cobrir:

- Tipos documentais.
- Modelos documentais.
- Versionamento de modelos.
- Builder visual e técnico.
- Biblioteca de variáveis.
- Regras condicionais.
- Pré-visualização responsiva e de impressão.
- Emissão individual.
- Emissão em lote.
- Geração de PDF.
- Cabeçalho e rodapé configuráveis.
- Assinatura e autenticação.
- Validação pública.
- Revogação e reemissão.
- Auditoria completa.

#### 4. Tipos documentais suportados

A lista inicial deve incluir, no mínimo, os tipos mostrados na tela atual, como aditivo, contratos, declaração de conclusão de curso, declaração de frequência, declaração de matrícula, declaração de quitação, declaração de transferência e etiqueta do aluno. [cite:1]

Também deve aceitar expansão para:

- Termos de responsabilidade.
- Requerimentos.
- Autorizações.
- Boletos acompanhados de instruções.
- Comunicados institucionais.
- Certificados.
- Atas.
- Relatórios acadêmicos.
- Fichas cadastrais.
- Dossiês do aluno.
- Declarações personalizadas.

#### 5. Arquitetura conceitual

O módulo deve ser dividido em componentes independentes:

- **Document Type Service**: cadastro e política por tipo documental.
- **Template Catalog Service**: cadastro de modelos e escopos.
- **Template Version Service**: snapshots, histórico, rollback e comparação.
- **Document Builder Service**: edição visual/técnica do layout.
- **Rendering Engine**: interpretação do template e geração final.
- **Rule Engine**: validação de elegibilidade e lógica condicional.
- **Issuance Service**: emissão, protocolo e fila de processamento.
- **Signature Service**: integração com assinatura eletrônica/digital.
- **Validation Service**: consulta pública por QR/token/código.
- **Audit Service**: trilha completa de eventos.
- **Storage Service**: persistência dos arquivos gerados e seus checksums.

#### 6. Builder universal de documentos

O builder é o núcleo do módulo. Ele deve ser capaz de construir qualquer documento institucional sem depender de edição externa, usando composição visual por blocos e modo avançado por markup/template.

##### 6.1 Modos do builder

O builder deve possuir dois modos interoperáveis:

1. **Modo visual**
   - Edição por blocos.
   - Arrastar e soltar.
   - Painel de propriedades.
   - Guias visuais para margens e grid.
   - Preview imediato.

2. **Modo técnico**
   - HTML/CSS controlado.
   - DSL/template engine com variáveis.
   - Regras condicionais.
   - Estruturas de repetição.
   - CSS de impressão avançado.

3. **Modo híbrido**
   - Usuário monta no visual.
   - Usuário técnico refina no markup.
   - Sistema mantém estrutura sem perda de compatibilidade.

##### 6.2 Blocos base do builder

O builder deve oferecer blocos reutilizáveis:

- Título.
- Subtítulo.
- Parágrafo.
- Texto rico.
- Lista ordenada.
- Lista não ordenada.
- Tabela.
- Linha horizontal.
- Espaçador.
- Quebra de página.
- Imagem.
- Logo.
- QR code.
- Código de barras.
- Assinatura.
- Carimbo.
- Selo.
- Caixa de destaque.
- Campo variável.
- Grupo condicional.
- Repetidor.
- Colunas.
- Bloco de identificação institucional.
- Bloco de identificação do aluno.
- Rodapé institucional.
- Cabeçalho institucional.
- Bloco livre HTML.

##### 6.3 Áreas estruturais do documento

Cada documento deve ser composto por zonas independentes:

- Área da página.
- Cabeçalho.
- Corpo.
- Rodapé.
- Margem superior.
- Margem inferior.
- Margem esquerda.
- Margem direita.
- Área imprimível.
- Área de notas internas não impressas.

##### 6.4 Camadas do layout

O builder deve suportar camadas lógicas:

- Fundo.
- Conteúdo principal.
- Elementos fixos.
- Elementos repetidos por página.
- Marcas de segurança.
- Marca d’água.
- Overlay de preview.

#### 7. Suporte universal a tamanhos de papel

O builder deve permitir configurar qualquer formato de papel, com presets e modo customizado.

##### 7.1 Presets obrigatórios

- A0
- A1
- A2
- A3
- A4
- A5
- A6
- Carta (Letter)
- Ofício
- Legal
- Executivo
- Tabloide
- Envelope padrões institucionais
- Etiquetas personalizadas

##### 7.2 Configuração de papel

Campos obrigatórios:

- Nome do preset.
- Largura.
- Altura.
- Unidade de medida.
- Orientação: retrato ou paisagem.
- Sangria opcional.
- Área segura.
- Escala de renderização.
- DPI de preview.
- DPI de exportação.

##### 7.3 Unidades de medida aceitas

- mm
- cm
- in
- px
- pt

##### 7.4 Requisitos funcionais do motor de página

- Converter qualquer unidade para uma base interna padronizada.
- Preservar proporção e posicionamento no preview.
- Separar preview de tela do layout real de impressão.
- Permitir presets por modelo e por versão.
- Suportar documentos de página única e multipágina.

##### 7.5 Exemplo de configuração JSON

```json
{
  "page": {
    "size": "A4",
    "width": 210,
    "height": 297,
    "unit": "mm",
    "orientation": "portrait",
    "bleed": 0,
    "safeArea": 5,
    "dpiPreview": 96,
    "dpiExport": 300
  }
}
```

#### 8. Margens, recuos, alinhamento e identação

O builder deve permitir controle fino de composição tipográfica e de impressão.

##### 8.1 Configuração de margens da página

Campos:

- Margem superior.
- Margem inferior.
- Margem esquerda.
- Margem direita.
- Margem espelhada para frente e verso.
- Margem específica da primeira página.
- Margem específica de páginas pares/ímpares.

##### 8.2 Configuração de recuos e identação

Campos:

- Recuo do primeiro parágrafo.
- Recuo esquerdo do bloco.
- Recuo direito do bloco.
- Espaçamento antes.
- Espaçamento depois.
- Entrelinha.
- Alinhamento horizontal.
- Alinhamento vertical do bloco.
- Controle de hifenização.
- Justificado, esquerda, centro, direita.

##### 8.3 Regras tipográficas

- Permitir estilo por bloco e por classe.
- Permitir herança de estilo institucional.
- Permitir tabulações.
- Permitir grid de baseline opcional.
- Permitir controle de órfãs e viúvas em impressão.
- Permitir evitar quebra dentro de blocos críticos.

##### 8.4 Exemplo de estilo do corpo

```json
{
  "contentStyle": {
    "fontFamily": "Times New Roman",
    "fontSize": 12,
    "lineHeight": 1.5,
    "textAlign": "justify",
    "firstLineIndent": 1.25,
    "indentUnit": "cm",
    "spacingBefore": 0,
    "spacingAfter": 0.25,
    "spacingUnit": "cm"
  }
}
```

#### 9. Cabeçalho e rodapé

O sistema deve oferecer builder específico para cabeçalho e rodapé, desacoplado do corpo do documento.

##### 9.1 Capacidades do cabeçalho

- Logo institucional.
- Nome da instituição.
- CNPJ.
- Endereço.
- Unidade emissora.
- Linha decorativa.
- Título da seção.
- Número do documento.
- Data de emissão.
- Cabeçalho diferente na primeira página.
- Cabeçalho diferente em páginas pares/ímpares.

##### 9.2 Capacidades do rodapé

- Texto institucional.
- Endereço/contato.
- Autenticação e QR code.
- Número da página.
- Total de páginas.
- Código de validação.
- Rodapé legal.
- Assinatura institucional.
- Observação de validade.

##### 9.3 Campos configuráveis

- Altura do cabeçalho.
- Altura do rodapé.
- Distância da margem.
- Repetir em todas as páginas.
- Mostrar apenas na primeira página.
- Mostrar apenas na última página.
- Mostrar em páginas pares/ímpares.
- Sobrepor ou reservar área fixa.

##### 9.4 Placeholders de paginação

- `{{ page.number }}`
- `{{ page.total }}`
- `{{ document.validation_code }}`
- `{{ document.issue_date }}`

##### 9.5 Regras de layout

- Cabeçalho e rodapé devem reservar espaço real na área imprimível.
- O corpo não pode colidir com cabeçalho/rodapé.
- O preview deve mostrar claramente a caixa útil da página.

#### 10. Configuração avançada de impressão

O módulo precisa suportar impressão profissional e PDF confiável.

##### 10.1 Recursos obrigatórios

- CSS de impressão por template.
- `@page` configurável.
- Quebra de página manual e automática.
- Evitar quebra dentro de tabela ou assinatura.
- Repetição de cabeçalho de tabela.
- Marcas de corte opcionais.
- Escala de impressão controlada.
- Modo frente e verso.
- Margens espelhadas.
- Página inicial distinta.

##### 10.2 Propriedades a suportar

- `page-break-before`
- `page-break-after`
- `page-break-inside`
- `break-before`
- `break-after`
- `break-inside`
- `orphans`
- `widows`
- `@page`

##### 10.3 Exemplo conceitual

```css
@page {
  size: A4 portrait;
  margin: 20mm 15mm 25mm 20mm;
}

.section-no-break {
  break-inside: avoid;
}

.signature-block {
  page-break-inside: avoid;
}
```

#### 11. Biblioteca de variáveis e placeholders

O builder deve expor variáveis organizadas por domínio de negócio.

##### 11.1 Grupos mínimos

- Instituição.
- Mantenedora.
- Unidade.
- Curso.
- Turma.
- Período letivo.
- Aluno.
- Matrícula.
- Contrato.
- Financeiro.
- Responsável.
- Documento.
- Usuário emissor.
- Data/hora.
- Assinaturas.
- Configurações customizadas.

##### 11.2 Exemplos

- `{{ instituicao.nome }}`
- `{{ unidade.nome }}`
- `{{ aluno.nome_completo }}`
- `{{ aluno.cpf }}`
- `{{ matricula.numero }}`
- `{{ curso.nome }}`
- `{{ turma.nome }}`
- `{{ periodo_letivo.descricao }}`
- `{{ contrato.numero }}`
- `{{ financeiro.saldo_aberto }}`
- `{{ document.protocol }}`
- `{{ document.validation_code }}`
- `{{ issuer.nome }}`

##### 11.3 Requisitos

- Autocomplete por grupo.
- Descrição funcional da variável.
- Tipo da variável.
- Exemplo de valor.
- Indicação de campo sensível.
- Validação de placeholder inexistente.
- Aviso quando a variável não existir no contexto selecionado.

#### 12. Condicionais, repetições e lógica de template

O builder deve suportar lógica suficiente para compor documentos complexos.

##### 12.1 Condicionais

Exemplos:

```twig
{% if matricula.status == 'ATIVA' %}
<p>O aluno encontra-se regularmente matriculado.</p>
{% endif %}
```

##### 12.2 Repetições

```twig
{% for disciplina in historico.disciplinas %}
<tr>
  <td>{{ disciplina.nome }}</td>
  <td>{{ disciplina.carga_horaria }}</td>
  <td>{{ disciplina.nota_final }}</td>
</tr>
{% endfor %}
```

##### 12.3 Regras obrigatórias

- Comparações simples e compostas.
- Operadores lógicos.
- Formatação de datas, números e moeda.
- Funções auxiliares seguras.
- Blocos ocultos quando vazios.
- Fallbacks de valor.

#### 13. Componentes reutilizáveis

O sistema deve permitir biblioteca de componentes reutilizáveis por tenant.

##### Exemplos

- Cabeçalho institucional padrão.
- Rodapé de autenticação padrão.
- Bloco de assinatura da secretaria.
- Bloco de contrato financeiro.
- Tabela padrão de disciplinas.
- Caixa legal de LGPD.
- Termo padrão de ciência.

Cada componente deve ter:

- Nome.
- Categoria.
- Versão.
- HTML/estrutura.
- Estilos.
- Variáveis esperadas.
- Dependências.
- Escopo.

#### 14. Regras de negócio para emissão

Como a tela atual permite filtrar por período letivo, unidade, turma e aluno, a emissão precisa ser contextual e dirigida por dados acadêmicos antes da geração do documento. [cite:1]

##### Exemplos de elegibilidade

- Declaração de matrícula apenas para matrícula ativa.
- Declaração de frequência apenas com vínculo vigente.
- Declaração de quitação apenas sem débitos vencidos.
- Aditivo apenas com contrato vigente.
- Transferência apenas com solicitação deferida.
- Etiqueta do aluno apenas com vínculo válido ou cadastro ativo.

##### Severidades

- Bloqueante.
- Alerta.
- Informativa.

#### 15. Fluxos do usuário

##### 15.1 Criar tipo documental

1. Acessar Secretaria > Modelos de documentos. [cite:1]
2. Clicar em Cadastrar. [cite:1]
3. Informar nome, categoria, escopo e políticas.
4. Salvar o tipo.

##### 15.2 Criar modelo

1. Selecionar o tipo documental.
2. Criar novo modelo.
3. Definir escopo, vigência e formato de papel.
4. Abrir builder.
5. Montar cabeçalho, corpo e rodapé.
6. Inserir variáveis.
7. Configurar regras.
8. Salvar rascunho.

##### 15.3 Publicar modelo

1. Enviar para revisão.
2. Aprovador revisa layout e regras.
3. Publicar versão.
4. Modelo passa a ficar disponível para emissão.

##### 15.4 Emitir documento individual

1. Selecionar período, unidade, turma e aluno. [cite:1]
2. Selecionar o tipo documental desejado. [cite:1]
3. Sistema resolve o modelo aplicável.
4. Executa regras de elegibilidade.
5. Exibe preview.
6. Confirma emissão.
7. Gera PDF e protocolo.
8. Registra auditoria.

##### 15.5 Emitir em lote

1. Selecionar turma, unidade, curso ou filtro customizado.
2. Selecionar tipo documental.
3. Executar validações.
4. Enfileirar processamento.
5. Gerar resultado com sucessos e falhas.

#### 16. Estrutura da interface do builder

##### 16.1 Layout da tela

A interface deve conter:

- Barra superior com ações.
- Painel esquerdo de blocos.
- Área central de canvas/página.
- Painel direito de propriedades.
- Barra inferior de zoom, grade e páginas.
- Alternância entre preview tela e preview impressão.

##### 16.2 Barra superior

- Salvar.
- Salvar versão.
- Validar.
- Pré-visualizar.
- Testar com aluno.
- Aprovar.
- Publicar.
- Duplicar.
- Exportar definição.
- Importar definição.

##### 16.3 Painel esquerdo

- Blocos.
- Variáveis.
- Componentes reutilizáveis.
- Estrutura do documento.
- Páginas.

##### 16.4 Painel direito

Propriedades contextuais do elemento selecionado:

- Dimensões.
- Posição.
- Fonte.
- Cor.
- Borda.
- Margem.
- Padding.
- Recuo.
- Quebra.
- Visibilidade condicional.
- Fonte de dados.
- Repetição.

#### 17. Modelo de dados

##### 17.1 Entidades principais

- `document_types`
- `document_models`
- `document_model_versions`
- `document_layout_definitions`
- `document_layout_blocks`
- `document_layout_assets`
- `document_variables_catalog`
- `document_rules`
- `document_approvals`
- `document_issuances`
- `document_issuance_files`
- `document_validation_tokens`
- `document_revocations`
- `document_audit_logs`
- `document_components_library`

##### 17.2 Campos sugeridos para layout versionado

###### document_layout_definitions

- id
- model_version_id
- page_size
- page_width
- page_height
- unit
- orientation
- margin_top
- margin_right
- margin_bottom
- margin_left
- mirrored_margins
- header_height
- footer_height
- content_schema_json
- print_css
- preview_css
- builder_schema_json
- created_at

###### document_layout_blocks

- id
- layout_definition_id
- parent_block_id nullable
- block_type
- zone
- sort_order
- x
- y
- width
- height
- style_json
- content_json
- visibility_rule_json
- repeat_rule_json

#### 18. API sugerida

##### Tipos

- `GET /api/document-types`
- `POST /api/document-types`
- `PUT /api/document-types/{id}`

##### Modelos

- `GET /api/document-models`
- `POST /api/document-models`
- `GET /api/document-models/{id}`
- `PUT /api/document-models/{id}`
- `POST /api/document-models/{id}/version`
- `POST /api/document-models/{id}/publish`

##### Builder

- `GET /api/document-models/{id}/builder`
- `PUT /api/document-models/{id}/builder`
- `POST /api/document-models/{id}/validate-layout`
- `POST /api/document-models/{id}/preview`
- `POST /api/document-models/{id}/preview-print`

##### Emissão

- `POST /api/documents/issue`
- `POST /api/documents/issue-batch`
- `GET /api/documents/issuances`
- `GET /api/documents/issuances/{id}`
- `POST /api/documents/issuances/{id}/revoke`

##### Validação pública

- `GET /public/document-validation/{code}`

#### 19. Segurança, LGPD e governança

O módulo deve tratar documentos acadêmicos e cadastrais, o que exige governança forte sobre acesso, visualização e emissão, especialmente porque a tela atual é contextualizada por aluno e unidade. [cite:1]

##### Requisitos obrigatórios

- RBAC por ação e escopo.
- Separação por tenant.
- Restrição por unidade.
- Logs imutáveis.
- Hash do documento emitido.
- Máscara de dados sensíveis em telas públicas.
- Criptografia de dados sensíveis em repouso.
- Registro de base legal e finalidade, quando aplicável.
- Política de retenção e descarte.

#### 20. Auditoria

Toda ação deve ser registrada:

- criação de tipo;
- criação de modelo;
- edição de versão;
- aprovação;
- publicação;
- preview;
- emissão;
- reemissão;
- revogação;
- validação pública;
- download;
- alteração de regras.

Campos mínimos:

- entidade;
- id da entidade;
- ação;
- usuário;
- data/hora;
- IP;
- before/after;
- unidade;
- tenant;
- correlation id.

#### 21. Requisitos não funcionais

##### Performance

- Preview individual em até 2 segundos em cenários comuns.
- Geração síncrona simples em até 5 segundos.
- Emissão em lote assíncrona.
- Layout com paginação estável.

##### Confiabilidade

- Idempotência na emissão.
- Retry seguro em tarefas assíncronas.
- Não duplicar protocolo.
- Snapshot completo do payload usado na emissão.

##### Escalabilidade

- Filas para geração de lote.
- Storage desacoplado.
- Cache de variáveis institucionais.
- Render workers horizontais.

#### 22. Critérios de aceite do builder

O builder será considerado pronto quando:

- Permitir criar modelo sem ferramenta externa.
- Suportar A0, A1, A2, A3, A4, A5, Carta e formatos customizados.
- Permitir configurar orientação, margens e área imprimível.
- Permitir cabeçalho e rodapé independentes.
- Permitir identação, recuo, entrelinha e alinhamento por bloco.
- Permitir preview fiel do papel.
- Permitir quebras de página controladas.
- Permitir PDF multipágina estável.
- Permitir variáveis, condicionais e repetições.
- Permitir salvar e versionar layouts.
- Permitir emissão real por aluno/unidade/período.
- Permitir validação e auditoria completas.

#### 23. Roadmap recomendado

##### Fase 1

- Cadastro de tipos.
- Cadastro de modelos.
- Builder básico com A4/A3/Carta.
- Variáveis.
- Preview.
- Geração de PDF.
- Emissão individual.

##### Fase 2

- Versionamento avançado.
- Cabeçalho e rodapé por página.
- Condicionais e repetições.
- Emissão em lote.
- Validação pública.
- Revogação.

##### Fase 3

- Assinatura digital.
- Componentes reutilizáveis avançados.
- Editor técnico completo.
- Frentes e versos com margens espelhadas.
- Templates institucionais compartilhados entre unidades.

#### 24. Recomendação de implementação

Para um SaaS educacional multiunidade, a melhor abordagem é manter o documento emitido como artefato imutável, o template como ativo versionado e o builder como uma definição estruturada serializável em JSON, separada da renderização final.

A implementação recomendada é:

- Builder salvo em `builder_schema_json`.
- Estilo salvo em `style_json` por bloco.
- Template lógico salvo em `content_schema_json`.
- Exportação final em HTML de impressão + PDF.
- Render service isolado com fila para lote.
- Snapshot integral do payload da emissão.

#### 25. Exemplo de definição serializada do builder

```json
{
  "document": {
    "type": "DECLARACAO_MATRICULA",
    "version": "3.0.0"
  },
  "page": {
    "size": "A4",
    "orientation": "portrait",
    "unit": "mm",
    "width": 210,
    "height": 297,
    "margins": {
      "top": 20,
      "right": 15,
      "bottom": 25,
      "left": 20
    },
    "header": {
      "enabled": true,
      "height": 25,
      "repeatEveryPage": true
    },
    "footer": {
      "enabled": true,
      "height": 18,
      "repeatEveryPage": true
    }
  },
  "content": [
    {
      "type": "paragraph",
      "style": {
        "fontSize": 12,
        "textAlign": "justify",
        "firstLineIndent": 12.5,
        "lineHeight": 1.5
      },
      "value": "Declaramos que {{ aluno.nome_completo }} está regularmente matriculado(a)..."
    }
  ]
}
```

#### 26. Fechamento técnico

A tela observada já aponta corretamente para um catálogo de modelos documentais por tipo, mas a evolução ideal é transformar esse ponto em um subsistema completo de **gestão documental com builder universal**, suportando documentos simples, formais, extensos, multipágina e institucionalmente validados. [cite:1]

O grande diferencial do módulo deve ser unir três camadas no mesmo produto: governança do modelo, liberdade de composição visual e confiabilidade de emissão/impressão. Isso permite que a secretaria opere documentos do dia a dia, enquanto jurídico, financeiro e administração mantêm controle formal sobre versões, layout e validade.
