# 35 — Acesso Físico e Segurança: Portaria, Catracas, Câmeras, Portas e Biometria, por Portal

> Parte do [SDD v2](00-README.md). Matriz de portais em [31](31-matriz-portais-modulos.md). Dado biométrico e de imagem em [07](07-privacidade-lgpd.md) e [26](26-sdd-juridico-regulatorio.md). Retenção e expurgo em [21](21-busca-e-armazenamento.md). Auditoria em [29](29-auditoria.md). Integração de hardware em [16](16-integracoes-externas.md).
> **Status:** aprovada pelo autor em 03/11/2026, com as propostas adotadas. Itens sem valor definido continuam pendentes, criada em 03/11/2026. A v1 cita o tema em navegação e em integração, sem especificação própria. Itens **[Decisão do autor]** e **(jurídico)** dependem de resposta ou parecer.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| O módulo de acesso físico está completo? | **Não.** Não há especificação. A v1 cita "Portaria & Acesso" (desenvolvedor), "Portaria Escolar" (gestão), "Entradas e Saídas" (aluno e responsáveis) e "Gestão de Integração: Catracas" (terceiros), sem regra, DDL, estados ou teste |
| Está organizado por portal? | **Não.** Os nomes se repetem com sentidos diferentes (ver seção 2) |
| Reconhecimento facial e biometria? | **Sem regra.** É dado sensível (LGPD, art. 11). Pendência jurídica |
| Câmeras (CFTV)? | **Sem regra.** A v1 não tem especificação de câmera nem de retenção de imagem |
| Portas eletrônicas? | **Sem regra.** Só aparece como item de navegação |

---

## 2. Confusão de nomes a resolver

| Nome na v1 | Onde está | O que é de fato | Ação |
|---|---|---|---|
| "Gestão de Acesso" | Portal do desenvolvedor, Segurança & Acesso | Usuários, papéis, MFA, sessões (acesso **lógico**) | Manter. É [06](06-identidade-acesso.md) |
| "Portaria & Acesso" | Portal do desenvolvedor | Catracas, visitantes, crachás, encomendas (acesso **físico**), da plataforma | **Decidido** em 03/11/2026: mantido, para a própria empresa, quando tiver instalações com controle |
| "Portaria Escolar" | Gestão (SAAS acadêmico) | Acesso físico da escola: catraca, reconhecimento facial, visitantes, autorização de saída de aluno | Manter. Este documento |
| "Entradas e Saídas" | Portal do aluno e dos responsáveis | Histórico do próprio acesso e notificação de entrada e saída | Manter. Só leitura do próprio dado |
| "Gestão de Auditoria" | Portal do desenvolvedor | Logs de sistema e de operação | É [29](29-auditoria.md). Não é acesso físico |

**Regra:** "acesso" sem qualificação não aparece em documento. Usar "acesso lógico" ou "acesso físico".

---

## 3. Recursos do acesso físico

### 3.1 Dispositivos

| Dispositivo | Função | Integração |
|---|---|---|
| Catraca | Registro de entrada e saída de pessoas | Driver do fabricante, por conector |
| Porta eletrônica | Liberação de porta com credencial | Driver do fabricante |
| Leitor de crachá (RFID ou código) | Identificação | Conector |
| Leitor biométrico ou facial | Identificação por biometria | Conector, **com regra da seção 5** |
| Câmera (CFTV) | Imagem do acesso e do ambiente | Stream ou gravador, **com regra da seção 6** |

Dispositivo é cadastrado por unidade. Um dispositivo não serve outra unidade, mesmo na mesma entidade.

### 3.2 Visitantes

- Cadastro de visitante com documento, motivo, destino e autorização de quem recebe.
- Documento do visitante: só número mascarado no registro de acesso. Imagem do documento não é guardada, salvo regra específica **(jurídico)**.
- Visitante de menor de idade na escola: regra de autorização do responsável, não do visitante ([07](07-privacidade-lgpd.md), seção 3).
- Validade: acesso temporário, com data e horário de fim.

### 3.3 Autorização de saída de aluno

Requisito da v1 (Portaria Escolar). Regra proposta:

- Saída de aluno menor só com autorização registrada do responsável, por canal verificado, com data e horário.
- Quem retira o aluno é identificado (nome e documento mascarado) e comparado com a lista autorizada.
- Saída sem autorização gera alerta imediato à coordenação e ao responsável.
- Autorização tem validade. Expirada, não vale.

### 3.4 Registro de entrada e saída

| Campo | Regra |
|---|---|
| Pessoa | Vínculo (aluno, professor, colaborador, visitante). Visitante não tem vínculo permanente. |
| Dispositivo | Identificador do dispositivo e da unidade |
| Direção | Entrada ou saída |
| Momento | Data e hora UTC ([29](29-auditoria.md), seção 2) |
| Método | Crachá, biometria, facial, manual |
| Resultado | Permitido, negado, manual |

Registro de entrada é dado de acesso. Retenção conforme seção 6.

---

## 4. Por portal

| Portal | Recurso | Escopo |
|---|---|---|
| Desenvolvedor | Acesso físico da própria plataforma, **se mantido** (seção 2) | Plataforma apenas |
| Gestão | Portaria completa: dispositivos, visitantes, autorização de saída, registros, câmeras, relatórios | Unidade, conforme permissão |
| Professor | Nenhum acesso físico próprio. Registro de entrada do próprio docente, se a unidade usa controle | Só o próprio registro |
| Aluno | Histórico de entradas e saídas, com horário. Notificação de atraso | Só o próprio histórico |
| Responsáveis | Entrada e saída dos dependentes em tempo real. Autorização de saída. Notificação | Só dependentes com vínculo ativo |
| Terceiros | Integração com fornecedor de catraca ou merenda (API). Sem acesso ao registro de pessoas | Só o contrato de integração ([16](16-integracoes-externas.md)) |

**Regra:** o responsável não vê o registro de outro aluno, nem imagem de câmera, nem de visitante.

---

## 5. Biometria e reconhecimento facial

**Problema:** biometria e reconhecimento facial são dado pessoal **sensível** (LGPD, art. 5º, II e art. 11). Em escola, envolvem principalmente menores.

**Proposta mínima, até parecer:**

1. Biometria é **opcional**. A unidade oferece crachá ou código como alternativa, sem penalizar quem recusa.
2. O consentimento é específico para biometria, por escrito, com finalidade e prazo. Revogável.
3. Template biométrico (não a imagem) é guardado cifrado, no banco da unidade, com chave do cofre ([05](05-seguranca.md)). Nunca sai da unidade.
4. Não há reconhecimento facial contra base de terceiros nem compartilhamento com outra unidade.
5. Exclusão do template na saída da pessoa ou na revogação. Registro da exclusão sem o dado ([29](29-auditoria.md)).
6. Relatório de impacto (RIPD) antes de ativar.

**(jurídico)** Base legal e exigências para menores. Lacuna LGPD-04 em [32](32-atendimento-privacidade-por-portal.md).

**Decidido** em 03/11/2026: biometria entra no escopo como opcional, com RIPD antes de ativar.

---

## 6. Câmeras (CFTV) e imagem

**Problema:** câmera registra imagem de menores, de visitantes e de funcionários. A v1 não define nada sobre câmera.

**Proposta:**

| Regra | Detalhe |
|---|---|
| Finalidade | Segurança patrimonial e de pessoas. Sem finalidade pedagógica nem de avaliação de docente. |
| Local | Áreas comuns e acessos. **Não** em banheiro, vestiário, sala de descanso ou área de amamentação. |
| Aviso | Placa de aviso no local. Sinalização visível. |
| Acesso à imagem | Só a função de segurança da unidade, com motivo registrado. Visualização ao vivo e exportação são eventos auditados ([29](29-auditoria.md)). |
| Retenção | Prazo curto e fixo de **30 dias**, decidido em 03/11/2026. Expurgo automático. Exportação de trecho fica em armazenamento com acesso restrito. |
| Reconhecimento facial em imagem | Mesma regra da seção 5. Desligado por padrão. |
| Terceiros | Câmera de terceiro não é acessada pelo portal de terceiros. |

**(jurídico)** Prazo de retenção de imagem e aviso exigido.

---

## 7. Portas e controle de acesso ao prédio

- Porta eletrônica tem regra de abertura por horário e por perfil, configurada na unidade.
- Liberação de emergência (incêndio) abre a porta sem depender da rede. Evento registrado depois.
- Falha de rede: a porta opera em modo local, com lista de credenciais sincronizada. Lista local expira.
- Alteração de regra de porta exige MFA e dupla aprovação, como outras configurações de segurança ([31](31-matriz-portais-modulos.md), seção 4.3).

---

## 8. Relação com os outros módulos

| Módulo | Relação |
|---|---|
| Acadêmico | Presença por QR Code e geolocalização (v1, `spec_gestao_academica_completo`, seção 8.3). **Atenção:** geolocalização do aluno é dado pessoal sensível de localização. Precisa de consentimento e de regra de minimização ([07](07-privacidade-lgpd.md)). Não há regra na v2 |
| Pessoas | Ponto eletrônico pode usar o registro de acesso. Não é fonte única |
| Patrimônio | QR e RFID são de bem, não de pessoa. Não usar a mesma tabela de acesso |
| Segurança do trabalho | Controle de acesso a área de risco. Fora deste documento |

---

## 9. Pendências

| # | Pendência | Tipo |
|---|---|---|
| ACC-01 | Portaria & Acesso da plataforma: manter ou retirar (seção 2) | **Decidido** em 03/11/2026: mantido, para a própria empresa (seção 11) |
| ACC-02 | Biometria e reconhecimento facial: escopo (seção 5) | **Decidido** em 03/11/2026 (seção 11). Parecer de (jurídico) pendente |
| ACC-03 | Retenção de imagem de câmera (seção 6) | **Decidido** em 03/11/2026: 30 dias. Parecer de (jurídico) pendente |
| ACC-04 | RIPD de biometria e de câmera | Documento e DPO |
| ACC-05 | Geolocalização em presença por QR Code | **Decidido** em 03/11/2026: a escola configura. Pode usar geolocalização ou outro método |
| ACC-06 | DDL de dispositivo, registro de acesso, autorização de saída e visitante | **Escrito** em [51](51-ddl-modulos-novos.md), seção 4. Revisão do owner pendente (DDL-01) |
| ACC-07 | Conectores de catraca e porta | **Decidido** em 03/11/2026: protocolo aberto primeiro, fabricantes depois, sob demanda |
| ACC-08 | Modo de falha da porta e lista local (seção 7) | **Escrito** em [51](51-ddl-modulos-novos.md), seção 4. Revisão do owner pendente (DDL-01) |

---

## 10. Critérios de aceite

- [ ] Dispositivo só atua na unidade à qual está cadastrado (teste de isolamento).
- [ ] Autorização de saída de menor sem registro gera bloqueio e alerta (teste).
- [ ] Biometria desligada por padrão; alternativa sem biometria disponível (teste).
- [ ] Nenhuma imagem de câmera aparece em portal de responsável, aluno ou terceiro (teste).
- [ ] Acesso à imagem gera evento de auditoria com motivo.
- [ ] Liberação de emergência funciona sem rede e gera evento depois.
- [ ] Itens **[Decisão do autor]** e **(jurídico)** respondidos ou marcados como pendentes no [00](00-README.md).

## 11. Decisões de 03/11/2026

**ACC-01 (Portaria & Acesso da plataforma): mantido no portal do desenvolvedor.** Função: gerir o acesso físico e a portaria da própria empresa desenvolvedora, quando ela tiver instalações com controle (catraca, porta eletrônica, crachá, visitantes, câmeras, encomendas). Regras:

- Dados em banco master, separado de qualquer entidade.
- Acesso restrito à equipe de segurança da empresa. Nenhum cliente vê esse módulo.
- Sem instalação, o módulo fica desativado.

**ACC-02 (escopo de biometria, reconhecimento facial e câmeras): aprovado.** Regras da seção 5 e da seção 6 valem como escopo: biometria opcional, template cifrado, RIPD antes de ativar, sem reconhecimento facial contra base de terceiros, câmera sem áreas íntimas e com aviso.

**ACC-03 (prazo de retenção de imagem): 30 dias, padrão inicial.** Expurgo automático ao fim do prazo. Trecho exportado para investigação fica em armazenamento restrito, com prazo próprio e registro. **(jurídico)** confirmar antes de produção.
