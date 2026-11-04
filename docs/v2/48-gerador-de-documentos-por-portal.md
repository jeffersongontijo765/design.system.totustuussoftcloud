# 48 — Gerador de Documentos, por Portal

> Parte do [SDD v2](00-README.md). Emissão de documento oficial da secretaria em [17](17-regras-modulos.md) e [46](46-matricula-e-rematricula-por-portal.md). Assinatura digital em [33](33-contratos-por-portal.md), seção 4, e decisão CTR-06. Biblioteca e acervo, separados, em [31](31-matriz-portais-modulos.md), seção 3. Armazenamento e checksum em [21](21-busca-e-armazenamento.md). Auditoria em [29](29-auditoria.md). Consulta pública e dado mínimo em [07](07-privacidade-lgpd.md).
> **Status:** especificação proposta, criada em 03/11/2026 e verificada contra a v1 no mesmo dia (seção 11). **Escopo:** apenas documentos emitidos pela secretaria (contexto C de [54](54-gestao-de-documentos-tres-contextos.md)). Documentos recebidos e administrativos têm regras próprias a partir de [`spec-builder-documentos-academicos.md`](anexo-v1/spec-builder-documentos-academicos.md) (editor de modelos, chamado de builder na v1: layout, variáveis, condicionais) e [`spec_gestao_documentos_completo.md`](anexo-v1/spec_gestao_documentos_completo.md) (tipos, ciclo de vida, assinatura, permissões). Fecha MOD-07 da [31](31-matriz-portais-modulos.md). Itens **(jurídico)**, **(verificar)** e **[Decisão do autor]** dependem de resposta.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| O gerador de documentos está especificado? | **Em parte.** O editor de modelos (layout, papel, margens, cabeçalho, rodapé, variáveis, condicionais) está bem descrito. Falta DDL, regra de emissão, validação pública e a separação entre gerador e gestão de documentos |
| Há duplicidade? | **Sim.** A v1 tem duas especificações de documentos, uma do editor de modelos (builder) e outra de gestão. Este documento une as duas |
| Está organizado por portal? | **Não.** A v1 não diz quem pode solicitar, quem emite e quem vê |
| Biblioteca e documentos se misturam? | **Não, por decisão.** A biblioteca tem acervo e empréstimo. Documento é emitido pela secretaria. Ver [31](31-matriz-portais-modulos.md), seção 3 |

---

## 2. Separação de responsabilidades

| Parte | Função | Dono |
|---|---|---|
| Editor de modelos | Desenha o modelo: papel, margens, cabeçalho, corpo, rodapé, variáveis, condicionais | Gestão de documentos |
| Catálogo de tipos | Declaração, histórico, certificado, termo, ata, comunicado, contrato e outros | Gestão de documentos |
| Emissão | Gera o arquivo final a partir de um modelo publicado e de dados do aluno, pessoa ou entidade | Secretaria ou módulo de origem |
| Assinatura | Assina o arquivo emitido | Serviço de assinatura ([33](33-contratos-por-portal.md)) |
| Validação pública | Confirma autenticidade por código ou QR, sem dado pessoal além do mínimo | Gestão de documentos |

---

## 3. Tipos de documento

Tipos da v1 mantidos: declaração de matrícula, declaração de frequência, declaração de conclusão, declaração de quitação, histórico escolar, certidão de conclusão, segunda via, aditivo e contrato.

Tipos previstos na v1 e mantidos como expansão: termo de responsabilidade, requerimento, autorização, boleto com instruções, comunicado institucional, certificado, ata, relatório acadêmico, ficha cadastral, dossiê do aluno e declaração personalizada.

Cada tipo tem:

- Modelo publicado e versionado.
- Lista de variáveis obrigatórias.
- Quem pode solicitar e quem pode emitir.
- Se exige assinatura e de quem.
- Prazo de validade, quando houver.

---

## 4. Ciclo de vida do documento emitido

`solicitado` → `em_emissao` → `emitido` → `aguardando_assinatura` → `assinado` ou `expirado` ou `cancelado`.

- `solicitado`: pedido do aluno, responsável, professor ou da própria secretaria, com protocolo ([32](32-atendimento-privacidade-por-portal.md)).
- `emitido` sem assinatura: disponível para download, com código de validação.
- `expirado`: quando o documento tem validade e ela venceu. Calculado por data ([18](18-regras-modulos-2.md), T-04).
- `cancelado`: só com motivo e evento de auditoria. O arquivo continua guardado.

Documento emitido não é editado. Correção gera novo documento, e o anterior vai para `cancelado`.

---

## 5. Editor de modelos: regras de modelo

| Regra | Detalhe |
|---|---|
| Papel | Presets A4 e ofício, com configuração de tamanho personalizado. Unidade em mm, cm ou pt |
| Margens e recuos | Por página, com recuo de primeira linha e de parágrafo |
| Cabeçalho e rodapé | Campos fixos da entidade (nome, CNPJ, endereço, logotipo) e paginação |
| Variáveis | Grupos mínimos: aluno, responsável, turma, curso, matrícula, entidade, unidade, data. Variável sem dado na emissão bloqueia a emissão e aponta o campo |
| Condicionais | Bloco aparece só se a condição for verdadeira. Ex.: bloco de bolsa só se houver bolsa |
| Repetições | Lista de disciplinas, de notas ou de parcelas, com cabeçalho repetido por página |
| Publicação | Modelo só é publicado depois de revisão. Publicado não muda ([41](41-formularios-e-pesquisas.md), seção 2.3) |

Modelo não contém código executável. Condicional e repetição são interpretadas por um motor de regras limitado.

---

## 6. Validação pública

- Cada documento emitido tem código de validação e QR apontando para uma página pública.
- A página confirma: tipo, data de emissão, situação atual (válido, expirado, cancelado) e a entidade emissora.
- A página **não** mostra nome do aluno, CPF ou nota. Para confirmar a pessoa, o consultante informa o código e a data de nascimento, e a consulta é limitada por taxa ([23](23-dominios-provisionamento-ciclo-de-vida.md)).
- Cada consulta gera evento de auditoria sem o dado consultado.

---

## 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos-padrão, sem dado | Ver documento emitido de qualquer entidade | P |
| **Gestão** | Criar e publicar modelo, cancelar documento com motivo, ver relatório de emissão | Emitir sem papel de secretaria | E |
| **Secretaria** | Solicitar, emitir, assinar (quando for o caso), reemitir, cancelar com motivo | Alterar modelo publicado | E |
| **Professor** | Solicitar documento de sua turma, ex.: declaração de frequência de aluno da turma | Emitir histórico ou documento oficial. Ver documento de outro aluno | E |
| **Aluno maior** | Solicitar e baixar os próprios documentos, com código de validação | Ver documento de outro aluno. Cancelar documento emitido | E |
| **Responsável** | Solicitar e baixar documentos de dependente com vínculo ativo | Ver documento de dependente sem vínculo. Cancelar documento emitido | E |
| **Terceiros** | Ver um documento emitido para ele, quando o contrato prevê (ex.: cartório recebe certidão) | Ver outros documentos | E, [38](38-portal-de-terceiros-prestadores.md) |
| **Público (consulta)** | Validar código e situação | Ver dado pessoal, nota ou conteúdo | Fora dos portais, seção 6 |

---

## 8. Assinatura

- Documento que exige assinatura passa por `aguardando_assinatura` até todos os signatários assinarem.
- Provedor de assinatura: decisão CTR-06, aceitar provedores de terceiros e ter assinatura digital própria.
- Assinatura de documento oficial depende de exigência de cada tipo. Conferido em 03/11/2026 na Lei 14.063/2020 (planalto.gov.br):
  - **Níveis:** simples (identifica o signatário), avançada (certificado fora da ICP-Brasil ou outro meio aceito pelas partes, ligado ao signatário de forma unívoca e que detecta alteração) e qualificada (certificado ICP-Brasil) (art. 4º). O modelo de documento guarda o **nível mínimo** exigido, e o sistema recusa assinatura abaixo dele.
  - **Âmbito:** a lei vale para interações com ente público e dentro dele (art. 2º). Não vale entre particulares (art. 2º, parágrafo único, II, a). Cada Poder e ente define o nível mínimo por ato próprio (art. 5º). Por isso, em escola pública o nível de cada tipo vem do ato do ente, configurado pela entidade.
  - **Qualificada obrigatória:** atos de chefes de Poder e de titulares de órgão autônomo, nota fiscal eletrônica (salvo pessoa física e MEI), transferência e registro de imóvel, e demais casos em lei (art. 5º, § 2º). Atestado médico eletrônico e receita de controle especial também (art. 13). Em conflito entre normas, prevalece a qualificada (art. 5º, § 5º).
  - A lei não trata de diploma nem de histórico. A regra do diploma e do histórico digital do superior (normas do MEC) **(verificar)**.
  - **Entre particulares** (MP 2.200-2/2001, art. 10, conferido em 03/11/2026): documento assinado com certificado ICP-Brasil presume-se verdadeiro em relação ao signatário (§ 1º). Outro meio de comprovação de autoria e integridade vale se admitido pelas partes ou aceito por quem recebe o documento (§ 2º). Por isso, contrato e termo entre a escola privada e a família podem usar assinatura avançada, com a aceitação registrada no próprio contrato.
- O arquivo assinado guarda o checksum do conteúdo emitido ([21](21-busca-e-armazenamento.md)).

---

## 9. Pendências

| # | Pendência | Tipo |
|---|---|---|
| DOC-01 | Quais tipos exigem assinatura com certificado ICP-Brasil (seção 8) | **Conferido** em parte em 03/11/2026: níveis e casos obrigatórios na Lei 14.063/2020, arts. 2º, 4º, 5º e 13. MP 2.200-2/2001, art. 10, conferida. Faltam as normas do MEC para diploma e histórico digital **(verificar)**. Lista final por tipo com o (jurídico) |
| DOC-02 | Prazo de guarda de cada tipo emitido (histórico, declaração, certidão) | (jurídico) |
| DOC-03 | Layout oficial do histórico escolar, conforme norma do sistema de ensino (Res. CNE/CEB, citada na v1) | (verificar) |
| DOC-04 | Validade de declaração, por tipo | **Decidido** em 03/11/2026: 90 dias quando o tipo não define prazo |
| DOC-05 | Limite de consultas públicas de validação por código, por minuto | **Decidido** em 03/11/2026: 10 por minuto por endereço |
| DOC-06 | DDL de tipo, modelo, versão, documento emitido, assinatura e validação | **Escrito** em [51](51-ddl-modulos-novos.md), seção 12. Revisão do owner pendente (DDL-01) |

---

## 10. Critérios de aceite

- [ ] Modelo com variável sem dado não emite e aponta o campo (teste).
- [ ] Modelo publicado não muda, e correção gera novo documento (teste).
- [ ] Consulta pública não retorna nome, CPF ou nota (varredura).
- [ ] Responsável não baixa documento de dependente sem vínculo ativo (teste de isolamento).
- [ ] Cancelamento de documento exige motivo e gera evento de auditoria (teste).
- [ ] Itens **(jurídico)**, **(verificar)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).

---

## 11. Verificação contra a v1 e lacunas fechadas

Verificado em 03/11/2026 contra [`spec-builder-documentos-academicos.md`](anexo-v1/spec-builder-documentos-academicos.md) e [`spec_gestao_documentos_completo.md`](anexo-v1/spec_gestao_documentos_completo.md). A versão anterior deste documento cobria o núcleo (tipos, ciclo, editor de modelos, validação e portais), mas deixava de fora itens da v1. Os itens abaixo foram incluídos nas seções 12 a 19.

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

## 12. Aprovação de modelo

Estados do modelo: `rascunho` → `em_revisao` → `publicado` → `arquivado`.

- Quem cria o modelo não aprova o próprio modelo. A regra é verificada no banco, com a mesma técnica do `CHECK (created_by <> approved_by)` de [37](37-planejamento-e-empenho.md).
- A revisão confere layout, variáveis e regras. Não confere o texto jurídico, que é responsabilidade do jurídico da entidade.
- Modelo publicado não muda. Mudança gera nova versão em `rascunho`.

---

## 13. Elegibilidade para emissão

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

## 14. Emissão em lote

- A secretaria seleciona um tipo e um conjunto de alunos, por turma, série ou filtro.
- O sistema roda a elegibilidade para cada aluno e separa: emitidos, bloqueados e com alerta.
- Lote gera um protocolo por documento, não um protocolo único.
- Falha em um aluno não cancela o lote. O relatório final lista o que falhou e o motivo.
- O lote tem limite de tamanho por execução, e roda em fila ([14](14-integracao-modulos.md)).

---

## 15. Revogação

Revogação é diferente de cancelamento:

- **Cancelamento:** o documento foi emitido por erro, antes de ser usado. Sai da validação com o motivo.
- **Revogação:** o documento foi emitido corretamente, mas a situação mudou (ex.: matrícula cancelada depois da declaração). A validação pública mostra "revogado" e a data.

Os dois exigem motivo e evento de auditoria. O arquivo nunca é apagado.

---

## 16. Componentes reutilizáveis

Biblioteca por entidade, com componentes como cabeçalho institucional, rodapé de autenticação, bloco de assinatura da secretaria, tabela de disciplinas, caixa de LGPD e termo de ciência.

Cada componente tem nome, categoria, versão, estrutura, estilos, variáveis esperadas, dependências e escopo (entidade ou unidade). Alterar um componente gera nova versão. Os modelos que usam o componente escolhem a versão na publicação.

---

## 17. Configuração de impressão

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

## 18. Auditoria: ações obrigatórias

Toda ação gera evento em [29](29-auditoria.md), com os campos da seção 2 daquele documento e o campo `portal`:

criação de tipo · criação de modelo · edição de versão · envio para revisão · aprovação · publicação · preview · emissão · emissão em lote · reemissão · cancelamento · revogação · validação pública · download · alteração de regra · alteração de componente.

Validação pública registra a consulta sem o dado consultado ([29](29-auditoria.md), seção 6).

---

## 19. Automações e painel de assinaturas

- Documento aguardando assinatura há 3 dias: lembrete ao signatário.
- Documento expirado sem assinatura: aviso à secretaria, com opção de reenviar.
- Modelo em revisão há 5 dias úteis: lembrete ao revisor.
- Painel da secretaria: documentos aguardando assinatura, por signatário, e expirados. Gráfico de assinaturas concluídas por mês.

Prazos de lembrete são valores iniciais, ajustáveis pela entidade.

---

## 20. Interface da API

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

## 21. DDL

As tabelas do módulo estão em [51](51-ddl-modulos-novos.md), seção 12 (tipos, modelos, versões, emissões, validação, revogação e componentes). Este documento não repete o DDL.

---

## 22. Pendências desta verificação

| # | Pendência | Tipo |
|---|---|---|
| DOC-07 | Prazos de lembrete de assinatura e de revisão (seção 19) | Valor inicial, ajustável |
| DOC-08 | Limite de tamanho do lote (seção 14) | Operação, em homologação |
