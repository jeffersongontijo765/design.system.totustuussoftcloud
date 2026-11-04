# 53 — Pacote para Parecer Jurídico: Contratos, Declarações, Boletins e Demais Documentos

> Parte do [SDD v2](00-README.md). Pacote de consulta, complementar ao [50](50-pacote-juridico-e-norma.md). Os tipos de contrato estão em [33](33-contratos-por-portal.md). Os tipos de documento emitido estão em [48](48-gerador-de-documentos-por-portal.md). Acervo escolar em [17](17-regras-modulos.md).
> **Natureza deste documento:** pacote de consulta. Não é parecer. As "posições propostas" são o que o SDD adota para desenhar o sistema. O jurídico confirma, corrige ou recusa cada uma.
> **Citações legais:** todas marcadas **a confirmar**. Não foram verificadas contra o texto vigente.
> **Códigos:** DC-01 a DC-28, em 6 blocos. Responde-se com o campo de resposta da seção 9.

---

## 1. Escopo

O sistema produz e recebe documentos em quatro grupos:

| Grupo | Exemplos | Quem assina |
|---|---|---|
| Contratos | Matrícula, prestação de serviço a fornecedor, aditivo, parceria | Partes do contrato |
| Declarações e certidões | Declaração de matrícula, de frequência, de conclusão, de quitação, certidão de conclusão | Secretaria, com código de validação |
| Acervo escolar | Histórico, boletim, registro de classe, ata de resultados finais | Secretaria, com assinatura oficial |
| Outros | Termo de responsabilidade, requerimento, autorização, comunicado, certificado, ata de conselho | Conforme o tipo |

---

## 2. Bloco A: contratos

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-01 | Contrato de matrícula: é contrato de adesão, e quais cláusulas são obrigatórias | Gerado no wizard de matrícula | Contrato de adesão, com cláusulas obrigatórias do sistema de ensino e destaque das cláusulas que limitam direitos | Contrato negociado por aluno | [33](33-contratos-por-portal.md), CTR-05 |
| DC-02 | Contrato de matrícula com menor: quem assina e com que validade | Responsável assina por aluno menor | Responsável legal assina. Aluno maior assina o próprio contrato | Assinatura do aluno em qualquer idade | [46](46-matricula-e-rematricula-por-portal.md), M-09 |
| DC-03 | Forma de assinatura por tipo de contrato | Matrícula, prestação e aditivo | Assinatura digital com certificado ICP-Brasil para matrícula e prestação. Assinatura simples para aditivo e termos internos **a confirmar** | ICP-Brasil para tudo | [33](33-contratos-por-portal.md), CTR-04 |
| DC-04 | Contrato de prestação de serviço a fornecedor: cláusulas de proteção de dados | Fornecedor com acesso a dado pessoal | DPA (acordo de tratamento de dados) assinado antes do acesso. Exigência prevista em [33](33-contratos-por-portal.md) | Contrato sem DPA | [33](33-contratos-por-portal.md), seção 2 |
| DC-05 | Aditivo de contrato: quando exige nova assinatura | Mudança de valor, turma ou prazo | Aditivo assinado pelas mesmas partes. Mudança de valor exige aditivo, não edição | Edição direta com registro | [33](33-contratos-por-portal.md), seção 3 |
| DC-06 | Renovação automática de contrato: aviso e direito de recusa | Contratos com renovação automática | Aviso de 60 dias antes. Direito de recusa expresso no contrato | Renovação sem aviso | [33](33-contratos-por-portal.md), seção 6 |
| DC-07 | Contrato de matrícula e inadimplência: o contrato continua válido durante bloqueio parcial | Bloqueio parcial de portal | Contrato segue vigente. Bloqueio parcial não é rescisão | Rescisão automática | [26](26-sdd-juridico-regulatorio.md), seção 3 |
| DC-08 | Guarda de contratos assinados: prazo | Arquivo de contratos | Prazo de cinco anos após o fim do contrato, salvo norma específica **a confirmar** | Prazo do sistema de ensino | [33](33-contratos-por-portal.md), seção 7 |

---

## 3. Bloco B: declarações e certidões

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-09 | Declaração de matrícula: validade e uso | Emitida para órgãos e empresas | Validade de 90 dias, por padrão, indicada no documento. Pode ser validada pelo código | Sem validade | [48](48-gerador-de-documentos-por-portal.md), seção 3 |
| DC-10 | Declaração de frequência: base de dados | Frequência calculada de chamadas e de sala online | Frequência só com registro de chamada oficial. Presença online conta quando for a origem oficial | Presença online não conta para declaração | [17](17-regras-modulos.md), seção 4 |
| DC-11 | Certidão de conclusão de curso: quando é emitida | Pós-EAD e cursos livres | Emitida após a conclusão registrada, com assinatura e registro | Emitida a pedido sem conclusão | [46](46-matricula-e-rematricula-por-portal.md), seção 5 |
| DC-12 | Declaração de quitação: quais parcelas considera | Quitação de mensalidades | Considera as parcelas vencidas até a data de emissão. Declara o período citado | Quitação total do contrato | [34](34-pagamentos-fiscal-bancos-por-portal.md) |
| DC-13 | Validação pública de documento: quais dados aparecem | Código e QR no documento | Tipo, data, situação e entidade. Sem nome, CPF ou nota | Nome com data de nascimento | [48](48-gerador-de-documentos-por-portal.md), seção 6 |
| DC-14 | Segunda via de documento: pode ter data nova | Reemissão | Segunda via indica que é reemissão e mantém a data de origem | Nova data sem indicação | [48](48-gerador-de-documentos-por-portal.md) |

---

## 4. Bloco C: acervo escolar

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-15 | Histórico escolar: layout e conteúdo obrigatórios | Emissão de histórico | Conforme a norma do sistema de ensino da entidade, incluindo a referência legal no documento **a confirmar** | Layout próprio | [48](48-gerador-de-documentos-por-portal.md), DOC-03 |
| DC-16 | Boletim: pode ser emitido antes do fechamento do período | Boletim parcial para família | Boletim parcial identificado como parcial. Não substitui o histórico | Boletim só após fechamento | [17](17-regras-modulos.md) |
| DC-17 | Registro de classe e ata de resultados finais: guarda permanente ou por prazo | Acervo de turma | Prazo do sistema de ensino da entidade, com referência gravada **a confirmar** | Guarda permanente | [26](26-sdd-juridico-regulatorio.md), seção 3 |
| DC-18 | Ata de conselho de classe: quem assina | Reunião de conselho | Presidente e secretário da reunião. Registro com data e pauta | Assinatura de todos os presentes | [17](17-regras-modulos.md) |
| DC-19 | Certificado de participação em evento pastoral ou escolar: quando tem validade de documento oficial | Certificados de evento | Certificado de evento não é documento oficial. Não substitui histórico | Certificado com força de documento oficial | [43](43-pastoral-por-portal.md), seção 3.4 |

---

## 5. Bloco D: termos, autorizações e requerimentos

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-20 | Termo de responsabilidade de equipamento: texto e assinatura | Retirada de notebook, projetor, kit | Termo aceito no portal, com dados do equipamento e da pessoa. Assinatura simples | Assinatura física | [44](44-agendamento-ambientes-equipamentos.md), AMB-06 |
| DC-21 | Autorização de saída de aluno menor: validade e forma | Retirada na portaria | Autorização do responsável com data e validade. Forma digital, por vínculo verificado | Autorização permanente | [35](35-acesso-e-seguranca-fisica-por-portal.md), seção 3.3 |
| DC-22 | Autorização de uso de imagem: quando é exigida | Fotos e vídeos em evento | Autorização específica, por escrito, com finalidade e prazo. Sem autorização não publica | Autorização geral na matrícula | [43](43-pastoral-por-portal.md), seção 6 |
| DC-23 | Requerimento de segunda chamada, trancamento e transferência: prazo de resposta | Pedidos da secretaria | Prazo do serviço de atendimento ([32](32-atendimento-privacidade-por-portal.md)). Negativa com motivo | Sem prazo | [46](46-matricula-e-rematricula-por-portal.md) |

---

## 6. Bloco E: documentos de terceiros e de cobrança

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-24 | Nota fiscal recebida de fornecedor: a plataforma só recebe e valida, não emite | Portal de terceiros | Recebe e valida. Emissão fica com o fornecedor. Decidido pelo autor em 03/11/2026 **a confirmar** a parte fiscal | Emissão pela plataforma | [34](34-pagamentos-fiscal-bancos-por-portal.md), PAG-06 |
| DC-25 | Boleto com instruções: texto obrigatório | Cobrança | Texto com instruções de pagamento e canal de contestação | Texto livre | [34](34-pagamentos-fiscal-bancos-por-portal.md) |
| DC-26 | Comunicado institucional com dado pessoal: base e forma de envio | Comunicado a famílias | Comunicado com dado mínimo. Dado sensível nunca em comunicado em massa | Comunicado com dado completo | [07](07-privacidade-lgpd.md) |

---

## 7. Bloco F: atas, relatórios e dossiês

| Código | Pergunta | Contexto no sistema | Posição proposta | Alternativa | Onde |
|---|---|---|---|---|---|
| DC-27 | Ata de reunião com participação de menor ou dado de saúde: guarda e acesso | Reunião com responsável e atendimento | Acesso restrito aos participantes e à direção. Dado sensível fora da ata | Ata aberta à comunidade | [40](40-aulas-online-por-portal.md), seção 5 |
| DC-28 | Dossiê do aluno: quais documentos entram e quem acessa | Pasta digital do aluno | Acesso pelo papel da secretaria e pelo próprio aluno ou responsável. Sem dado de saúde para a secretaria | Acesso amplo da escola | [48](48-gerador-de-documentos-por-portal.md), seção 3 |

---

## 8. Itens que não são de jurídico

| Item | Responsável | Onde |
|---|---|---|
| Layout visual dos modelos | Gestão de documentos | [48](48-gerador-de-documentos-por-portal.md), seção 5 |
| Teste de validação pública | Qualidade | [49](49-logs-testes-por-portal.md) |

---

## 9. Campo de resposta

| Código | Confirma | Corrige (posição correta e referência) | Recusa (motivo) | Responsável | Data |
|---|---|---|---|---|---|
| DC-01 a DC-28 | | | | | |

---

## 10. Referências a confirmar

- Código Civil e Código de Defesa do Consumidor, sobre contrato de adesão e cláusulas de prestação de serviço **a confirmar**.
- LGPD, sobre acordo de tratamento com fornecedor **a confirmar**.
- Lei de Diretrizes e Bases e normas do sistema de ensino, sobre histórico, acervo e guarda **a confirmar**.
- Estrutura de ICP-Brasil e assinatura simples, para os contratos **a confirmar**.
- Regras fiscais de nota de fornecedor **a confirmar**.
