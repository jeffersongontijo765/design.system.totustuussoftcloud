# Documentos administrativos (tramitação)

- Portal: Gestão (`gestao.`)
- Área: Gestão de documentos
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 1; [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 3; [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 6; [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 7
- Fonte da v1: absorvida integralmente em [servicos-comuns-assinatura-protocolo-e-armazenamento.md](servicos-comuns-assinatura-protocolo-e-armazenamento.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Contexto B: criar e tramitar documentos administrativos (ofícios, memorandos, processos internos) entre setores, com despacho, prazo e assinatura.

## 3. Telas

- **Caixa de entrada do setor** (DataTable).
- **Documento — tramitação** (página): linha do tempo de despachos, anexos, assinaturas, prazo.
- **Novo documento** (editor com modelo).

## 4. Permissões por portal (extraídas do SDD)

Do [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md):

| Portal | Contexto A (recebidos) | Contexto B (administrativos) | Contexto C (emitidos) |
|---|---|---|---|
| **Gestão** | Consulta o que foi aprovado, sem a imagem, salvo papel de validação | Cria, tramita, aprova e arquiva | Acompanha emissão e relatório |
| **Secretaria** | Valida, aprova ou recusa; vincula ao processo | Não tramita (salvo se for setor da própria secretaria) | Emite, assina e revoga com motivo |

## 5. Papéis

- Usuários do setor com permissão do contexto B; `unit.manager` vê todos da unidade.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Regras do contexto B ([54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 3).

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

### 13.1 [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 1

#### 1. Os três contextos

| Contexto | O que é | Quem origina | Quem cuida | Exemplos |
|---|---|---|---|---|
| **A. Documentos recebidos** | Arquivos enviados a instituição para análise e validação | Responsáveis, alunos, candidatos, fornecedores | Secretaria, RH, compras | Certidão de nascimento, RG do responsável, histórico de escola anterior, alvará do fornecedor |
| **B. Documentos administrativos** | Documentos internos de gestão, com tramitação e aprovação | Equipe da instituição | Gestão e administração | Ata de reunião de diretoria, ofício, circular, processo administrativo, política interna |
| **C. Documentos emitidos** | Documentos gerados pela instituição a partir de modelo, para uma pessoa ou uma organização | Secretaria | Secretaria | Declaração, histórico, boletim, certidão, contrato, termo |

Os três contextos não se misturam. Um documento pertence a um contexto, e o contexto define regras, estados, portal de acesso e prazo de guarda.

### 13.2 [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 3

#### 3. Contexto B: documentos administrativos

##### 3.1 O que o contexto faz

- Cria documento interno com modelo ou em formato livre.
- Tramita: envia para análise, aprovação e assinatura de quem deve aprovar.
- Mantém versões. Versão aprovada não muda.
- Arquiva ao fim da tramitação, com prazo de guarda.

##### 3.2 Estados

`rascunho` → `em_tramitacao` → `aprovado` → `arquivado`, com `reprovado` como saída de `em_tramitacao`.

- Quem cria não aprova o próprio documento. Regra verificada no banco, como em [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), seção 12.
- Documento aprovado pode ser assinado. A assinatura usa o serviço comum da seção 5.

##### 3.3 Regras

- Documento administrativo não é visível a alunos e responsáveis, salvo quando a gestão publica um comunicado, que é contexto C ou um comunicado específico ([53](../../../docs/v2/53-pacote-documentos-e-contratos.md), DC-26).
- Ata de conselho ou de diretoria com dado sensível tem acesso restrito aos participantes ([53](../../../docs/v2/53-pacote-documentos-e-contratos.md), DC-27).
- Documento de processo administrativo público segue a lei de processo do ente. Conferido em 03/11/2026 na Lei 9.784/1999 (planalto.gov.br), que vale para a administração federal (art. 1º). Ente estadual e municipal segue lei própria, configurada pela entidade **(verificar)** por ente. Regras da lei federal que o sistema aplica quando a entidade escolher esse regime:
  - **Forma:** ato escrito, em português, com data, local e assinatura da autoridade (art. 22, § 1º). Páginas numeradas em sequência e rubricadas (art. 22, § 4º): no processo digital, o sistema numera cada peça e guarda o hash.
  - **Prazos:** 5 dias quando não houver prazo próprio, prorrogável até o dobro com justificativa (art. 24). Decisão em até 30 dias após a instrução, prorrogável uma vez com motivo (art. 49). Recurso em 10 dias da ciência (art. 59), com reconsideração em 5 dias e no máximo três instâncias (arts. 56 e 57). Contagem exclui o dia do começo e inclui o do vencimento, que passa ao dia útil seguinte sem expediente (art. 66). O sistema calcula e mostra o vencimento.
  - **Intimação:** com antecedência mínima de 3 dias úteis e o conteúdo do art. 26, § 1º. Registro da ciência no processo.
  - **Motivação:** obrigatória quando o ato nega ou limita direito, impõe sanção, decide recurso ou anula ato (art. 50). O sistema exige o campo de motivação nesses tipos de decisão.

### 13.3 [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 6

#### 6. Por portal

| Portal | Contexto A (recebidos) | Contexto B (administrativos) | Contexto C (emitidos) |
|---|---|---|---|
| **Desenvolvedor** | Nada | Nada, salvo documentos da própria empresa | Publica modelos-padrão, sem dado |
| **Gestão** | Consulta o que foi aprovado, sem a imagem, salvo papel de validação | Cria, tramita, aprova e arquiva | Acompanha emissão e relatório |
| **Secretaria** | Valida, aprova ou recusa; vincula ao processo | Não tramita (salvo se for setor da própria secretaria) | Emite, assina e revoga com motivo |
| **Professor** | Nada | Lê documento de tramitação em que é parte | Solicita documento de sua turma |
| **Aluno maior e responsável** | Envia e acompanha o próprio documento e o de dependente com vínculo ativo | Nada | Solicita e baixa o próprio documento |
| **Fornecedor (terceiros)** | Envia documentos da empresa, com validade e alerta | Nada | Recebe documento emitido para ele, quando o contrato prevê |
| **Público** | Nada | Nada | Valida código, sem dado pessoal |

### 13.4 [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 7

#### 7. Como os contextos se encontram

Exemplo de fluxo completo, em matrícula:

1. **A:** responsável envia certidão de nascimento. A secretaria valida e aprova.
2. **Matrícula:** a aprovação libera o passo de documentos do wizard ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), M-08).
3. **C:** a secretaria emite o contrato de matrícula pelo modelo publicado.
4. **Assinatura:** o contrato passa pelo serviço comum de assinatura, com o responsável como signatário.
5. **Protocolo:** cada etapa recebe número de protocolo pelo serviço comum.
6. **Auditoria:** cada etapa grava o contexto e o portal.

Ata de conselho de classe (B) pode gerar declaração de encaminhamento (C), mas o vínculo é de referência: a ata não é copiada para dentro do documento emitido.
