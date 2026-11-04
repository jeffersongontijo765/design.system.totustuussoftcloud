# Contratos de aluno

- Portal: Gestão (`gestao.`)
- Área: Contratos
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [33](../../../docs/v2/33-contratos-por-portal.md), seção 2; [33](../../../docs/v2/33-contratos-por-portal.md), seção 5; [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 4; [53](../../../docs/v2/53-pacote-documentos-e-contratos.md) (integral)
- Fonte da v1: absorvida integralmente em [contratos-de-fornecedor.md](contratos-de-fornecedor.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Contrato de prestação de serviços educacionais gerado na matrícula e seus aditivos.

## 3. Telas

- **Contratos de aluno** (DataTable).
- **Modelos** (com aprovação jurídica).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `unit.secretary` e `unit.legal`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Assinatura no wizard (M-09, [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md)); cláusulas ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 4.1).

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

### 13.1 [33](../../../docs/v2/33-contratos-por-portal.md), seção 2

#### 2. Tipos de contrato e a quem pertencem

A v1 lista 13 tipos (seção 2.1). Eles não têm o mesmo dono. Cada um fica em um portal, com parte e papel definidos:

| Tipo | Parte A | Parte B | Dono | Portal de acesso |
|---|---|---|---|---|
| Contrato de cliente (SaaS) | Plataforma | Entidade | Plataforma | Desenvolvedor |
| Contrato de prestação de serviços educacionais (matrícula) | Entidade | Responsável legal e aluno | Entidade | Gestão; assinatura pelo Responsáveis |
| Contrato de trabalho e termos de pessoal | Entidade | Colaborador | Entidade (RH) | Gestão; ciência pelo Professor |
| Contrato de fornecedor e de serviço | Entidade | Fornecedor | Entidade (Compras) | Gestão; ciência pelo Terceiros |
| Contrato de manutenção, locação e parceria | Entidade | Fornecedor ou parceiro | Entidade | Gestão; ciência pelo Terceiros |
| Convênio e contrato institucional | Entidade | Órgão ou instituição | Entidade (Jurídico) | Gestão |
| Acordo de confidencialidade (NDA) | Plataforma ou entidade | Parte externa | Quem assina | Desenvolvedor ou Gestão |
| Acordo de processamento de dados (DPA) | Entidade ou plataforma | Operador | Jurídico | Gestão ou Desenvolvedor; ciência pelo Terceiros |
| Termo aditivo, distrato, renovação | Mesmas partes do contrato original | — | Dono do contrato original | Mesmo portal do original |
| Contrato guarda-chuva (master agreement) | Entidade | Fornecedor | Entidade (Compras) | Gestão |

**Regra:** o portal de origem é o do contrato original. Aditivo e distrato não mudam de portal.

**Pendência:** o contrato de matrícula (aluno ou responsável) e o contrato de cliente são contratos de consumo ou de prestação civil. A forma e as cláusulas dependem de **(jurídico)** ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 4). Não defino cláusula aqui.

### 13.2 [33](../../../docs/v2/33-contratos-por-portal.md), seção 5

#### 5. Assinatura

Estados (v1, seção 13.4): não iniciado, preparando envio, enviado, visualizado, parcialmente assinado, assinado, rejeitado, expirado, cancelado.

Regras:

- Assinatura eletrônica com validade jurídica depende do tipo de documento e do nível exigido **(jurídico)** ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 6, e Lei 14.063/2020).
- Assinatura de responsável em contrato de aluno: verificação de identidade do signatário antes do envio ([06](../../../docs/v2/06-identidade-acesso.md)).
- Envelope tem validade. Expirado não é reaberto; novo envelope é criado.
- Assinatura de terceiro: o portal de terceiros mostra só o próprio contrato.
- Documento assinado é guardado com hash e trilha ([21](../../../docs/v2/21-busca-e-armazenamento.md)).

### 13.3 [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 4

#### 4. Relação de consumo e cobrança

##### 4.1 Contrato e cláusulas

- Contrato de adesão deve ter redação clara e destaque para cláusulas que limitem direitos (CDC, art. 54, §4º) [A].
- Cláusula de rescisão, multa e reajuste devem estar no contrato e na área do cliente, com histórico [A].
- Prática abusiva é vedada (CDC, art. 39) [A]. Exemplo: exigir vantagem sem causa ou condicionar serviço a aceite de cobrança indevida.

##### 4.2 Direito de arrependimento em venda online

Quando a matrícula ou a assinatura é contratada fora do estabelecimento, o consumidor tem sete dias para desistir, sem custo (CDC, art. 49) [A]. O sistema:

- Mostra o prazo no fluxo de contratação.
- Registra a data da contratação e a data da desistência.
- Gera estorno integral dentro do prazo do meio de pagamento ([20](../../../docs/v2/20-pagamentos-seguranca.md), seção 11).

##### 4.3 Multa, juros e reajuste de mensalidade

- Multa moratória em relação de consumo tem limite de 2% (CDC, art. 52, §1º) [A].
- Anuidades e mensalidades escolares têm regras próprias de reajuste e de cobrança de encargos (Lei 9.870/1999) [V]. O sistema aplica os limites da norma como padrão, e o tenant não pode ultrapassá-los.
- Juros de mora e correção seguem a regra do contrato, dentro dos limites legais [V].

##### 4.4 Negativação e comunicação prévia

- A abertura de cadastro de inadimplente exige comunicação por escrito ao consumidor antes da inclusão (CDC, art. 43, §2º) [A].
- O sistema envia a comunicação e registra a data e o canal. A inclusão só ocorre depois do prazo de comunicação, que o jurídico confirma [V].
- Consulta a cadastro de inadimplentes sem finalidade legítima é vedada. Ver [21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6.8, para a regra de finalidade.

##### 4.5 Superendividamento e renegociação

- Antes de bloqueios e negativação, o sistema oferece renegociação com plano de pagamento (Lei 14.181/2021) [A para a existência; V para a aplicação à régua].
- Renegociação registra as condições, o consentimento do consumidor e o histórico.

##### 4.6 Bloqueio de serviço

- Bloqueio total do portal por inadimplência é vedado para serviço educacional essencial e para menor de idade. O sistema aplica bloqueio parcial: documentos obrigatórios, matrícula de rematrícula e comunicação com a família continuam acessíveis [P].
- Documentos escolares não são retidos como forma de cobrança sem previsão legal [V].

### 13.4 [53 — Pacote para Parecer Jurídico: Contratos, Declarações, Boletins e Demais Documentos](../../../docs/v2/53-pacote-documentos-e-contratos.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Pacote de consulta, complementar ao [50](../../../docs/v2/50-pacote-juridico-e-norma.md). Os tipos de contrato estão em [33](../../../docs/v2/33-contratos-por-portal.md). Os tipos de documento emitido estão em [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md). Acervo escolar em [17](../../../docs/v2/17-regras-modulos.md).
> **Natureza deste documento:** pacote de consulta. Não é parecer. As "posições propostas" são o que o SDD adota para desenhar o sistema. O jurídico confirma, corrige ou recusa cada uma.
> **Citações legais:** todas marcadas **a confirmar**. Não foram verificadas contra o texto vigente.
> **Códigos:** DC-01 a DC-28, em 6 blocos. Responde-se com o campo de resposta da seção 9.

---

#### 1. Escopo

O sistema produz e recebe documentos em quatro grupos:

| Grupo | Exemplos | Quem assina |
|---|---|---|
| Contratos | Matrícula, prestação de serviço a fornecedor, aditivo, parceria | Partes do contrato |
| Declarações e certidões | Declaração de matrícula, de frequência, de conclusão, de quitação, certidão de conclusão | Secretaria, com código de validação |
| Acervo escolar | Histórico, boletim, registro de classe, ata de resultados finais | Secretaria, com assinatura oficial |
| Outros | Termo de responsabilidade, requerimento, autorização, comunicado, certificado, ata de conselho | Conforme o tipo |

---

#### 2. Bloco A: contratos

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-01 | Contrato de matrícula: é contrato de adesão, e quais cláusulas são obrigatórias | Gerado no wizard de matrícula | Contrato de adesão, com cláusulas obrigatórias do sistema de ensino e destaque das cláusulas que limitam direitos | Contrato negociado por aluno | [33](../../../docs/v2/33-contratos-por-portal.md), CTR-05 |
| DC-02 | Contrato de matrícula com menor: quem assina e com que validade | Responsável assina por aluno menor | Responsável legal assina. Aluno maior assina o próprio contrato | Assinatura do aluno em qualquer idade | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), M-09 |
| DC-03 | Forma de assinatura por tipo de contrato | Matrícula, prestação e aditivo | Assinatura digital com certificado ICP-Brasil para matrícula e prestação. Assinatura simples para aditivo e termos internos **a confirmar** | ICP-Brasil para tudo | [33](../../../docs/v2/33-contratos-por-portal.md), CTR-04 |
| DC-04 | Contrato de prestação de serviço a fornecedor: cláusulas de proteção de dados | Fornecedor com acesso a dado pessoal | DPA (acordo de tratamento de dados) assinado antes do acesso. Exigência prevista em [33](../../../docs/v2/33-contratos-por-portal.md) | Contrato sem DPA | [33](../../../docs/v2/33-contratos-por-portal.md), seção 2 |
| DC-05 | Aditivo de contrato: quando exige nova assinatura | Mudança de valor, turma ou prazo | Aditivo assinado pelas mesmas partes. Mudança de valor exige aditivo, não edição | Edição direta com registro | [33](../../../docs/v2/33-contratos-por-portal.md), seção 3 |
| DC-06 | Renovação automática de contrato: aviso e direito de recusa | Contratos com renovação automática | Aviso de 60 dias antes. Direito de recusa expresso no contrato | Renovação sem aviso | [33](../../../docs/v2/33-contratos-por-portal.md), seção 6 |
| DC-07 | Contrato de matrícula e inadimplência: o contrato continua válido durante bloqueio parcial | Bloqueio parcial de portal | Contrato segue vigente. Bloqueio parcial não é rescisão | Rescisão automática | [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 3 |
| DC-08 | Guarda de contratos assinados: prazo | Arquivo de contratos | Prazo de cinco anos após o fim do contrato, salvo norma específica **a confirmar** | Prazo do sistema de ensino | [33](../../../docs/v2/33-contratos-por-portal.md), seção 7 |

---

#### 3. Bloco B: declarações e certidões

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-09 | Declaração de matrícula: validade e uso | Emitida para órgãos e empresas | Validade de 90 dias, por padrão, indicada no documento. Pode ser validada pelo código | Sem validade | [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), seção 3 |
| DC-10 | Declaração de frequência: base de dados | Frequência calculada de chamadas e de sala online | Frequência só com registro de chamada oficial. Presença online conta quando for a origem oficial | Presença online não conta para declaração | [17](../../../docs/v2/17-regras-modulos.md), seção 4 |
| DC-11 | Certidão de conclusão de curso: quando é emitida | Pós-EAD e cursos livres | Emitida após a conclusão registrada, com assinatura e registro | Emitida a pedido sem conclusão | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 5 |
| DC-12 | Declaração de quitação: quais parcelas considera | Quitação de mensalidades | Considera as parcelas vencidas até a data de emissão. Declara o período citado | Quitação total do contrato | [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md) |
| DC-13 | Validação pública de documento: quais dados aparecem | Código e QR no documento | Tipo, data, situação e entidade. Sem nome, CPF ou nota | Nome com data de nascimento | [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), seção 6 |
| DC-14 | Segunda via de documento: pode ter data nova | Reemissão | Segunda via indica que é reemissão e mantém a data de origem | Nova data sem indicação | [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md) |

---

#### 4. Bloco C: acervo escolar

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-15 | Histórico escolar: layout e conteúdo obrigatórios | Emissão de histórico | Conforme a norma do sistema de ensino da entidade, incluindo a referência legal no documento **a confirmar** | Layout próprio | [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), DOC-03 |
| DC-16 | Boletim: pode ser emitido antes do fechamento do período | Boletim parcial para família | Boletim parcial identificado como parcial. Não substitui o histórico | Boletim só após fechamento | [17](../../../docs/v2/17-regras-modulos.md) |
| DC-17 | Registro de classe e ata de resultados finais: guarda permanente ou por prazo | Acervo de turma | Prazo do sistema de ensino da entidade, com referência gravada **a confirmar** | Guarda permanente | [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 3 |
| DC-18 | Ata de conselho de classe: quem assina | Reunião de conselho | Presidente e secretário da reunião. Registro com data e pauta | Assinatura de todos os presentes | [17](../../../docs/v2/17-regras-modulos.md) |
| DC-19 | Certificado de participação em evento pastoral ou escolar: quando tem validade de documento oficial | Certificados de evento | Certificado de evento não é documento oficial. Não substitui histórico | Certificado com força de documento oficial | [43](../../../docs/v2/43-pastoral-por-portal.md), seção 3.4 |

---

#### 5. Bloco D: termos, autorizações e requerimentos

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-20 | Termo de responsabilidade de equipamento: texto e assinatura | Retirada de notebook, projetor, kit | Termo aceito no portal, com dados do equipamento e da pessoa. Assinatura simples | Assinatura física | [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md), AMB-06 |
| DC-21 | Autorização de saída de aluno menor: validade e forma | Retirada na portaria | Autorização do responsável com data e validade. Forma digital, por vínculo verificado | Autorização permanente | [35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md), seção 3.3 |
| DC-22 | Autorização de uso de imagem: quando é exigida | Fotos e vídeos em evento | Autorização específica, por escrito, com finalidade e prazo. Sem autorização não publica | Autorização geral na matrícula | [43](../../../docs/v2/43-pastoral-por-portal.md), seção 6 |
| DC-23 | Requerimento de segunda chamada, trancamento e transferência: prazo de resposta | Pedidos da secretaria | Prazo do serviço de atendimento ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md)). Negativa com motivo | Sem prazo | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) |

---

#### 6. Bloco E: documentos de terceiros e de cobrança

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-24 | Nota fiscal recebida de fornecedor: a plataforma só recebe e valida, não emite | Portal de terceiros | Recebe e valida. Emissão fica com o fornecedor. Decidido pelo autor em 03/11/2026 **a confirmar** a parte fiscal | Emissão pela plataforma | [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), PAG-06 |
| DC-25 | Boleto com instruções: texto obrigatório | Cobrança | Texto com instruções de pagamento e canal de contestação | Texto livre | [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md) |
| DC-26 | Comunicado institucional com dado pessoal: base e forma de envio | Comunicado a famílias | Comunicado com dado mínimo. Dado sensível nunca em comunicado em massa | Comunicado com dado completo | [07](../../../docs/v2/07-privacidade-lgpd.md) |

---

#### 7. Bloco F: atas, relatórios e dossiês

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-27 | Ata de reunião com participação de menor ou dado de saúde: guarda e acesso | Reunião com responsável e atendimento | Acesso restrito aos participantes e à direção. Dado sensível fora da ata | Ata aberta à comunidade | [40](../../../docs/v2/40-aulas-online-por-portal.md), seção 5 |
| DC-28 | Dossiê do aluno: quais documentos entram e quem acessa | Pasta digital do aluno | Acesso pelo papel da secretaria e pelo próprio aluno ou responsável. Sem dado de saúde para a secretaria | Acesso amplo da escola | [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), seção 3 |

---

#### 8. Itens que não são de jurídico

| Item | Responsável | Onde |
|---|---|---|
| Layout visual dos modelos | Gestão de documentos | [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), seção 5 |
| Teste de validação pública | Qualidade | [49](../../../docs/v2/49-logs-testes-por-portal.md) |

---

#### 9. Campo de resposta

| Código | Confirma | Corrige (posição correta e referência) | Recusa (motivo) | Responsável | Data |
|---|---|---|---|---|---|
| DC-01 a DC-28 | | | | | |

---

#### 10. Referências a confirmar

- Código Civil e Código de Defesa do Consumidor, sobre contrato de adesão e cláusulas de prestação de serviço **a confirmar**.
- LGPD, sobre acordo de tratamento com fornecedor **a confirmar**.
- Lei de Diretrizes e Bases e normas do sistema de ensino, sobre histórico, acervo e guarda **a confirmar**.
- Estrutura de ICP-Brasil e assinatura simples, para os contratos **a confirmar**.
- Regras fiscais de nota de fornecedor **a confirmar**.
