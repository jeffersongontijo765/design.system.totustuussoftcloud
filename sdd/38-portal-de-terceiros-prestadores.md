# 38 — Portal de Terceiros: Prestadores de Serviço, por Tipo, com Acesso Restrito ao Próprio Escopo

> Parte do [SDD v2](00-README.md). Portal em [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 1. Matriz em [31](31-matriz-portais-modulos.md), seção 2.6. Contratos em [33](33-contratos-por-portal.md). Identidade e vínculo em [06](06-identidade-acesso.md), seção 12. Nota fiscal em [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 5.3. Acesso físico em [35](35-acesso-e-seguranca-fisica-por-portal.md). Atendimento em [32](32-atendimento-privacidade-por-portal.md).
> **Status:** especificação proposta, criada em 03/11/2026. Itens **(verificar)** dependem de conferência de norma setorial. Itens **[Decisão do autor]** dependem de resposta.

---

## 1. Modelo

Um **prestador** é uma pessoa jurídica ou um MEI que a entidade contrata. O acesso não é dado à empresa como um todo. É dado a **pessoas** do prestador, e cada pessoa só enxerga o que o **contrato** dela cobre.

```
Prestador (CNPJ)
  └── Contrato (33), com vigência e status
        ├── Serviços habilitados (tipo de prestador, seção 3)
        ├── Unidades cobertas
        └── Pessoas do prestador (vínculo tipo "prestador")
              └── Papel dentro do serviço
```

O acesso de uma pessoa é a **interseção** de quatro filtros. Se algum falhar, a resposta é vazia:

| Filtro | Fonte |
|---|---|
| Contrato `vigente` | [33](33-contratos-por-portal.md), seção 3 |
| Serviço habilitado | Tipo de prestador (seção 3) |
| Unidade coberta | Contrato, seção 4 |
| Papel da pessoa no prestador | Vínculo, seção 2 |

**Regra de default:** nenhum dado é retornado sem filtro de contrato. Consulta sem contrato vigente é recusada na aplicação ([02](02-arquitetura.md), seção 2), não só na tela.

---

## 2. Pessoas e papéis do prestador

| Papel | Pode | Não pode |
|---|---|---|
| Responsável do prestador | Gerir as pessoas do próprio prestador, enviar documentos, acompanhar pedidos | Ver pessoas de outro prestador. Aprovar a própria nota |
| Operador | Executar as ações do serviço habilitado | Alterar contrato, ver faturamento |
| Financeiro do prestador | Ver pedidos e pagamentos do próprio contrato, enviar nota | Alterar dados bancários sem confirmação por MFA |
| Auditor do prestador | Ler o próprio histórico | Alterar qualquer registro |

Vínculo do prestador: conta global ([06](06-identidade-acesso.md), seção 12) com vínculo do tipo `prestador`, que guarda o `contrato_uuid`. Quando o contrato termina, o vínculo é revogado em até 30 s ([30](30-cache.md), seção 4).

---

## 3. Tipos de prestador

Cada tipo tem um **pacote fixo** de ações e de dados. A entidade habilita o pacote no contrato. Nenhum tipo recebe dado de outro tipo.

### 3.1 Jurídico (escritório de advocacia)

| Pode | Não pode |
|---|---|
| Ver contratos, pareceres e processos designados | Ver financeiro completo da entidade |
| Registrar parecer e minuta ([33](33-contratos-por-portal.md), seção 8, perfil JU) | Aprovar contrato como gestor |
| Ver dado de aluno apenas em processo designado, com motivo | Ver lista geral de alunos |

Sigilo profissional. Todo acesso a processo gera evento de auditoria com motivo ([29](29-auditoria.md)).

### 3.2 Contabilidade

| Pode | Não pode |
|---|---|
| Lançamentos, obrigações e tributos do escopo | Ver folha detalhada por colaborador. Recebe só totais |
| Propor fechamento, que o contador da entidade aprova | Fechar período sozinho |
| Exportar para o ERP do contador | Ver dado de saúde ou de aluno |

Lançamento proposto pelo prestador tem origem registrada. Aprovação é do contador da entidade ([22](22-crm-canais-e-papeis.md), seção 5).

### 3.3 Cartório (serviço notarial ou registral contratado)

| Pode | Não pode |
|---|---|
| Receber pedido de autenticação ou reconhecimento de documento indicado pela entidade | Ver outros documentos do titular |
| Devolver status e selo digital, quando o cartório emitir | Alterar o documento original |

Dado do titular aparece mascarado (CPF e e-mail, [29](29-auditoria.md), seção 6). Validade jurídica do selo **(verificar)** com o tipo de ato.

### 3.4 Alimentação escolar (lanchonete ou fornecedor de merenda)

| Pode | Não pode |
|---|---|
| Ver cardápio aprovado por nutricionista e quantidade de refeições por unidade e dia | Ver lista nominal de alunos sem restrição |
| Registrar entrega, temperatura e validade, conforme a RDC ANVISA nº 216/2004 (ver regra abaixo) | Ver histórico de compra da entidade com outro prestador |
| Receber lista de restrição alimentar, sem diagnóstico | Ver diagnóstico ou CID |

Regra de dado da alimentação, conferida em 03/11/2026 no texto da RDC ANVISA nº 216/2004 (bvsms.saude.gov.br). A RDC vale para cantinas e cozinhas institucionais (item 1.2). Leitura nossa: inclui cantina escolar e cozinha de merenda. A vigilância sanitária local pode complementar (art. 2º).

| Registro | Limite que o sistema confere |
|---|---|
| Cocção | Pelo menos 70 ºC em todas as partes do alimento (4.8.8) |
| Conservação a quente | Acima de 60 ºC por no máximo 6 horas (4.8.15) |
| Resfriamento | De 60 ºC a 10 ºC em até 2 horas, depois abaixo de 5 ºC ou a -18 ºC ou menos (4.8.16) |
| Preparado refrigerado | Até 5 dias a 4 ºC ou menos. Entre 4 ºC e 5 ºC, prazo menor, configurado pelo prestador (4.8.17) |
| Identificação | Designação, data de preparo e validade no preparado e no aguardando transporte. Data de abertura e nova validade no ingrediente aberto (4.8.6, 4.8.18 e 4.9.1) |
| Transporte e exposição | Temperatura monitorada e registrada (4.9.2 e 4.10.3) |
| Guarda | Registros mantidos por no mínimo 30 dias da data de preparo (4.11.3). O sistema guarda pelo prazo do contrato, nunca menos de 30 dias |

Valor fora do limite gera ocorrência para o responsável da entidade. O registro não é apagado nem corrigido sem rastro.

**Restrição alimentar** é dado de saúde ([07](07-privacidade-lgpd.md), seção 2). O prestador recebe apenas o aviso "restrição: sim" e o tipo de alimento a evitar, com consentimento do responsável **(jurídico)**. Não recebe a condição clínica.

### 3.5 Transporte escolar

| Pode | Não pode |
|---|---|
| Ver rotas, horários e pontos do contrato | Ver endereço completo do aluno |
| Ver lista de embarque por ponto, com nome e turma | Ver CPF, saúde ou notas |
| Registrar embarque e desembarque | Ver histórico de localização passado |
| Rastrear o veículo durante a viagem, sem identificar o aluno no mapa | Ver localização de aluno fora da viagem |

**Dado de menor com localização** é o caso de maior risco desta seção. Regras:

- A localização do veículo só é transmitida durante a viagem. Não há histórico além do necessário para a viagem, com prazo de 30 dias, decidido em 03/11/2026.
- Embarque só com autorização do responsável registrada ([35](35-acesso-e-seguranca-fisica-por-portal.md), seção 3.3).
- Alerta de desvio de rota vai para a coordenação e para o responsável, não para o prestador.
- Base legal e prazo de guarda **(jurídico)**.

### 3.6 Transportadora (carga e entrega de materiais)

| Pode | Não pode |
|---|---|
| Ver pedidos de compra e ordens de entrega do contrato | Ver dado pessoal de qualquer pessoa |
| Registrar coleta, entrega e comprovante | Ver rota de veículo de outro prestador |
| Rastrear a carga | Ver frota da entidade além das próprias cargas |

Rastreio é de carga, não de pessoa.

### 3.7 Tecnologia da informação (terceirizado de TI)

| Pode | Não pode |
|---|---|
| Atender chamados de TI do escopo ([36](36-tecnologia-da-informacao-por-portal.md)) | Ver banco de dados de pessoas |
| Ver a vista de ativos de TI do escopo | Alterar contrato ou configuração de segurança |
| Acesso remoto só com chamado aberto, passkey e sessão gravada | Acesso remoto permanente |

Acesso remoto de terceiro é o caminho de maior risco de TI. Exige chamado vinculado, janela de atendimento e registro da sessão ([36](36-tecnologia-da-informacao-por-portal.md), seção 6).

### 3.8 Limpeza e manutenção predial

| Pode | Não pode |
|---|---|
| Ver ordens de serviço, cronograma e áreas do contrato | Ver dado de aluno ou de colaborador |
| Solicitar crachá temporário pela portaria ([35](35-acesso-e-seguranca-fisica-por-portal.md)) | Ver registro de acesso de outras pessoas |
| Registrar execução e foto da área sem pessoa identificável | Ver câmera |

### 3.9 Vigilância e segurança patrimonial

| Pode | Não pode |
|---|---|
| Ver plantão, rondas e ocorrências do contrato | Ver câmera ao vivo fora de ocorrência aberta |
| Registrar ocorrência | Exportar imagem |
| Ver lista de visitantes autorizados do dia | Ver histórico de visitantes |

Acesso a imagem, quando permitido por ocorrência, gera evento de auditoria com motivo e tempo limitado ([35](35-acesso-e-seguranca-fisica-por-portal.md), seção 6).

### 3.10 Uniformes, material didático e livraria

| Pode | Não pode |
|---|---|
| Ver pedidos, catálogo e entregas do contrato | Ver lista nominal de alunos |
| Ver quantidades por série, tamanho e unidade | Ver dado pessoal além do destinatário da entrega, quando necessário |
| Emitir nota da venda ([34](34-pagamentos-fiscal-bancos-por-portal.md), seção 5.3) | Ver pagamento de outro prestador |

### 3.11 Saúde ocupacional terceirizada (clínica de ASO)

| Pode | Não pode |
|---|---|
| Receber agendamento de exame ocupacional: nome, função, tipo de exame | Ver histórico de exame de outro colaborador |
| Devolver resultado: apto, inapto ou apto com restrição, e o ASO | Ver CID, diagnóstico ou prontuário fora do ASO |
| Médico responsável com CRM válido | Acessar sistema da entidade além do agendamento |

Regra de dado: o prontuário fica sob responsabilidade do médico responsável pelo PCMSO, ou do médico que fez o exame quando a entidade é dispensada do PCMSO (NR-7, 7.6.1). A entidade é obrigada a manter o prontuário por no mínimo 20 anos após o desligamento (7.6.1.1). Por isso, o contrato com a clínica garante a guarda pelo prazo e a transferência formal dos prontuários quando o médico responsável ou a clínica mudar (7.6.1.2). A entidade recebe o resultado e o ASO, não o prontuário. Prontuário eletrônico segue o Conselho Federal de Medicina (7.6.1.3) **(verificar)**.

### 3.12 Consultoria pedagógica e treinamento

| Pode | Não pode |
|---|---|
| Ver turmas e conteúdo de formação do contrato | Ver notas ou dado de aluno |
| Registrar presença de participantes | Ver dado pessoal além de nome e função, para certificado |

---

## 4. Contrato e unidades

- Contrato de prestador segue [33](33-contratos-por-portal.md). Acesso só começa com contrato `vigente`.
- Unidade coberta é lista explícita. Contrato de uma unidade não dá acesso às outras, mesmo na mesma entidade ([03](03-dominio-tenancy.md)).
- Aditivo que inclui unidade ou serviço só passa a valer depois da aprovação, pela alçada de [33](33-contratos-por-portal.md), seção 12.

---

## 5. Habilitação e ciclo de vida

| Etapa | Regra |
|---|---|
| Cadastro | CNPJ válido e situação ativa. Verificação na base pública **(verificar)** |
| Documentos | Os exigidos pelo tipo: alvará, seguro, certidões trabalhistas e previdenciárias **(verificar)** |
| Contrato | Assinado ([33](33-contratos-por-portal.md), seção 5) |
| Convite | Cada pessoa é convidada pelo responsável do prestador. Convite com validade de 72 h ([06](06-identidade-acesso.md)) |
| Ativo | Documentos em dia e contrato vigente |
| Suspenso | Certidão vencida, contrato vencido ou irregularidade. Sem novo pedido |
| Encerrado | Vínculos revogados. Dados devolvidos ou expurgados conforme o contrato ([23](23-dominios-provisionamento-ciclo-de-vida.md), seção 5) |

**Alerta:** certidão vencendo em 30 dias.

---

## 6. Segregação e isolamento

1. Um prestador não vê outro prestador, nem o nome dele em lista de fornecedores, salvo cadastro público exigido por lei **(verificar)**.
2. Quem executa o serviço não aprova a própria nota ou o próprio pagamento.
3. Pessoa do prestador que sai do quadro do prestador perde o vínculo na mesma hora, pelo responsável do prestador.
4. Consulta que cruza dois prestadores é recusada e gera alerta.

---

## 7. Auditoria

Todo acesso de prestador grava evento com `portal = terceiros`, `prestador_uuid`, `contrato_uuid`, serviço e unidade ([29](29-auditoria.md), seção 2). Leitura de dado pessoal de titular é marcada como dado sensível.

---

## 8. Pendências

| # | Pendência | Tipo |
|---|---|---|
| TER-01 | Tipos personalizados: regra de criação (seção 11) | **Decidido** em 03/11/2026 |
| TER-02 | Prazo de guarda do rastro de localização do transporte escolar (seção 11) | **Decidido** em 03/11/2026: 30 dias depois da viagem. Parecer do (jurídico) pendente |
| TER-03 | Base legal do transporte escolar e de restrição alimentar | (jurídico) |
| TER-04 | Norma sanitária para registro de temperatura e validade na alimentação | **Conferido** em 03/11/2026: RDC ANVISA nº 216/2004, itens 4.8 a 4.11. Fica para conferir norma sanitária local e se há RDC posterior que a substitua |
| TER-05 | Guarda de prontuário pela clínica de ASO | **Conferido** em 03/11/2026: NR-7, 7.6.1 a 7.6.1.2. Contrato com a clínica garante 20 anos e transferência. Regra do CFM para prontuário eletrônico **(verificar)** |
| TER-06 | Validade do selo do cartório digital por tipo de ato | (verificar) |
| TER-07 | Documentos exigidos por tipo (alvará, seguro, certidões) | (verificar) |
| TER-08 | Acesso remoto de TI: janela e forma de gravação (seção 11) | **Incluído** em 03/11/2026 |

---

## 9. Critérios de aceite

- [ ] Pessoa de prestador A não obtém dado de prestador B (teste de isolamento por par).
- [ ] Pessoa com contrato encerrado perde acesso em até 30 s (teste).
- [ ] Prestador de tipo X não recebe campo fora do pacote do tipo (teste por tipo).
- [ ] Transporte escolar: nenhum endereço completo ou localização fora da viagem aparece para o prestador (teste).
- [ ] Restrição alimentar sem diagnóstico (teste de varredura de resposta).
- [ ] Acesso remoto de TI sem chamado aberto é recusado (teste).
- [ ] Itens **(verificar)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).

---

## 11. Decisões de 03/11/2026

**TER-01 (tipos personalizados): decidido.** Os doze tipos da seção 3 são modelos-base. A entidade cria um tipo próprio (por exemplo, "lanchonete com entrega própria") a partir de um modelo-base, com as regras:

- Escolhe serviços apenas do catálogo da plataforma. Não cria serviço fora dele.
- Pode retirar itens do pacote-base, mas não pode incluir campo bloqueado (dado de saúde, CID, diagnóstico, prontuário, gravação de câmera fora de finalidade).
- A criação e cada alteração de pacote exigem aprovação do responsável da entidade e ficam em auditoria ([29](29-auditoria.md)).
- Tipo personalizado só recebe os mesmos bloqueios dos tipos-base. Nenhum tipo personalizado ganha acesso que o modelo-base não tinha.

**TER-02 (guarda do rastro de localização do transporte escolar): incluído.** Regra: o rastro de localização do ônibus é guardado só durante a viagem e por um prazo fixo depois, para fins de segurança e de prestação de contas. Ao fim do prazo, o expurgo é automático. Nenhum prestador vê o rastro de um aluno fora da sua viagem. **Valor do prazo: (jurídico).** Até a definição, o sistema não grava o rastro por padrão.

**TER-08 (acesso remoto de TI): incluído.** Regra:

- Acesso remoto só dentro de um chamado aberto, com identificação do técnico e do ativo.
- Janela de acesso definida pela entidade. Padrão inicial: horário comercial da unidade. Fora da janela, o acesso é recusado.
- A sessão é gravada do início ao fim, com data, duração, técnico e ações. A gravação segue a retenção de auditoria ([29](29-auditoria.md)).
- Não há gravação de tela que capte dado pessoal sem aviso ao usuário da máquina.
