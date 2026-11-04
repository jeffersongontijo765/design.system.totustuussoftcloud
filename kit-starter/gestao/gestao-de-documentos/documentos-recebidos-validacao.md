# Documentos recebidos (validação)

- Portal: Gestão (`gestao.`)
- Área: Gestão de documentos
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 1; [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 2; [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 6; [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 7
- Fonte da v1: absorvida integralmente em [servicos-comuns-assinatura-protocolo-e-armazenamento.md](servicos-comuns-assinatura-protocolo-e-armazenamento.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Contexto A: receber, conferir e validar os documentos enviados por alunos, responsáveis, candidatos, colaboradores e terceiros, com pendências e prazos.

## 3. Telas

- **Fila de validação** (DataTable): documento, dono, tipo, enviado em, estado; filtros por tipo e prazo.
- **Validar documento** (página lado a lado: visualizador e checklist): aprovar, recusar com motivo, pedir novo envio.
- **Pendências por pessoa** (lista).

## 4. Permissões por portal (extraídas do SDD)

Do [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md):

| Portal | Contexto A (recebidos) | Contexto B (administrativos) | Contexto C (emitidos) |
|---|---|---|---|
| **Gestão** | Consulta o que foi aprovado, sem a imagem, salvo papel de validação | Cria, tramita, aprova e arquiva | Acompanha emissão e relatório |
| **Secretaria** | Valida, aprova ou recusa; vincula ao processo | Não tramita (salvo se for setor da própria secretaria) | Emite, assina e revoga com motivo |

## 5. Papéis

- `unit.secretary` e o setor dono do tipo de documento.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Regras do contexto A ([54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 2); documento sensível com acesso restrito ([07](../../../docs/v2/07-privacidade-lgpd.md)).

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

### 13.2 [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 2

#### 2. Contexto A: documentos recebidos

##### 2.1 O que o contexto faz

- Recebe arquivo enviado pelo portal (responsável, aluno, candidato ou fornecedor).
- Confere o arquivo: formato, tamanho, legibilidade e tipo declarado.
- Valida o conteúdo por pessoa habilitada. A validação registra quem validou, quando e o resultado.
- Vincula o arquivo a um cadastro ou a um processo: matrícula, cadastro de fornecedor, candidatura.
- Controla vencimento, quando o documento tem validade (ex.: alvará, seguro, certidão).

##### 2.2 Estados

`enviado` → `em_analise` → `aprovado` ou `recusado` ou `pendente_correcao`.

- `recusado` exige motivo. O remetente recebe o motivo e pode reenviar.
- `pendente_correcao` tem prazo. Vencido o prazo, o processo vinculado é tratado conforme a regra do processo (ex.: matrícula condicional, em [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md)).
- `vencido` é calculado por data ([18](../../../docs/v2/18-regras-modulos-2.md), T-04), não gravado.

##### 2.3 Regras

- Documento de menor é enviado pelo responsável com vínculo ativo.
- Imagem de documento de identidade é guardada cifrada, com acesso restrito à validação. Número completo aparece mascarado nas telas ([07](../../../docs/v2/07-privacidade-lgpd.md)).
- Documento recebido não é emitido. Nunca gera código de validação pública.
- Validação não é automática por padrão. Automação de leitura (OCR) só sugere, e a pessoa confirma ([21](../../../docs/v2/21-busca-e-armazenamento.md), seção 3.10).

##### 2.4 Retenção

Prazo por tipo de documento, vinculado ao processo que originou o envio. Documento de matrícula segue o prazo de guarda escolar **(jurídico, [50](../../../docs/v2/50-pacote-juridico-e-norma.md), J-05 e N-10)**. Documento de fornecedor segue o prazo do contrato.

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
