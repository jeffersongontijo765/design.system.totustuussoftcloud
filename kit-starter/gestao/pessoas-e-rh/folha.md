# Folha

- Portal: Gestão (`gestao.`)
- Área: Pessoas e RH
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 3; [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 7
- Fonte da v1: absorvida integralmente em [departamento-pessoal.md](../../desenvolvedor/pessoas-da-plataforma/departamento-pessoal.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Processar e aprovar a folha de pagamento.

## 3. Telas

- **Competências** (lista).
- **Processamento** (assistente).
- **Aprovação** (fila; quem processa não aprova).
- **Holerites** (emissão).

## 4. Permissões por portal (extraídas do SDD)

Do [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md):

| Portal | Departamento pessoal | Recursos humanos | Medicina e SST |
|---|---|---|---|
| Gestão | Completo, por permissão ([17](../../../docs/v2/17-regras-modulos.md), seção 3) | Completo, por permissão | Apto, inapto, restrição, EPI, NR, CAT, afastamento. **Sem CID nem prontuário** |

## 5. Papéis

- `unit.payroll`: processar.
- `unit.payroll.approver`: aprovar.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Folha fechada não muda ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5).

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

### 13.1 [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 3

#### 3. Departamento pessoal

##### 3.1 Admissão

| Etapa | Regra |
|---|---|
| Cadastro | Dados civis no banco de identidade. Dados contratuais no banco da unidade |
| Documentos | Obrigatórios por cargo. Admissão bloqueada se faltar documento ([18](../../../docs/v2/18-regras-modulos-2.md), seção 3) |
| Exame admissional | Agendado pelo SST. Admissão só com ASO apto ([17](../../../docs/v2/17-regras-modulos.md), seção 5) |
| Registro | Evento de admissão para o eSocial (S-2200) **(verificar)** |

##### 3.2 Folha

**Estados (v2, já definidos):** `em_processamento`, `fechada`, `paga`. Folha fechada não é alterada; a correção é folha complementar ([17](../../../docs/v2/17-regras-modulos.md), seção 2).

**Lacunas:**

| # | Falta | Origem |
|---|---|---|
| DP-01 | Catálogo de verbas (proventos, descontos, informativos), com natureza e incidência de INSS, FGTS e IRRF | v1, seção 9.3 |
| DP-02 | Fórmulas de cálculo versionadas, com vigência. Tabela de INSS e IRRF por competência | **(verificar)** |
| DP-03 | Processamento por competência e unidade, com pendências bloqueando o fechamento | v1, seção 9.1 |
| DP-04 | Holerite: geração, envio e registro de visualização. Holerite só para o próprio colaborador | v1, seção 9.2; [17](../../../docs/v2/17-regras-modulos.md), seção 2 |
| DP-05 | Eventos eSocial de remuneração (S-1200) e de pagamento (S-1210) **(verificar)** | Ausente |

##### 3.3 Férias e afastamentos

- Período aquisitivo e concessivo com cálculo de direito. **(verificar)** art. 130 da CLT e fracionamento. Pendência L-12 de [18](../../../docs/v2/18-regras-modulos-2.md).
- Programação pelo colaborador ou gestor, com aprovação do RH.
- Afastamento com data fim não anterior ao início e sem sobreposição ([17](../../../docs/v2/17-regras-modulos.md), seção 5.2).

##### 3.4 Ponto e jornada

- Registro de ponto por unidade. Regras da CLT, com a redação da Lei 13.874/2019 (planalto.gov.br, Conferido em 03/11/2026):
  - O horário de trabalho é anotado em registro de empregados (art. 74, caput).
  - **Estabelecimento com mais de 20 trabalhadores:** anotação obrigatória de entrada e saída, em registro manual, mecânico ou eletrônico, conforme instruções do Ministério, com pré-assinalação do repouso permitida (art. 74, § 2º). O sistema conta os trabalhadores **por estabelecimento** e exige o registro acima de 20. Abaixo disso, o registro fica opcional por unidade.
  - Trabalho fora do estabelecimento: registro em poder do empregado (art. 74, § 3º), por exemplo no aplicativo.
  - **Ponto por exceção:** permitido por acordo individual escrito, convenção ou acordo coletivo (art. 74, § 4º). O sistema só ativa o modo por exceção com o documento do acordo anexado.
  - **Intervalos:** mínimo de 11 horas entre duas jornadas (art. 66). Intervalo de 1 a 2 horas em trabalho contínuo acima de 6 horas, salvo acordo ou contrato coletivo (art. 71, caput), e de 15 minutos quando passar de 4 horas e não exceder 6 (art. 71, § 1º). O sistema alerta a violação, não bloqueia o registro.
  - Requisitos técnicos do registro eletrônico (REP) são da Portaria MTP nº 671/2021 **(verificar)**. Regra do servidor público vem do estatuto do ente **(verificar)** por ente.
  - **Professor de escola particular** (CLT, arts. 317 a 323, texto compilado lido em 03/11/2026 no Planalto):
    - Pode dar aula em mais de um turno no mesmo estabelecimento, sem passar da jornada semanal legal, com intervalo para refeição assegurado e não contado (art. 318, Lei 13.415/2017). O sistema soma as aulas de todos os turnos do professor na unidade e alerta acima da jornada semanal do contrato.
    - Não dá aula nem trabalha em exame aos domingos (art. 319). A grade ([60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md)) recusa aula de professor no domingo.
    - **Remuneração por aulas semanais**, paga por mês de **quatro semanas e meia** (art. 320, § 1º). Falta desconta as aulas não dadas (§ 2º), salvo até 9 dias por casamento ou luto de cônjuge, pai, mãe ou filho (§ 3º). Aula acima do horário é paga no fim do mês (art. 321). A folha recebe do diário ([61](../../../docs/v2/61-diario-escolar-por-portal.md)) as aulas dadas e as excedentes de cada mês.
    - Em exames e férias escolares, recebe a mesma remuneração do período de aulas (art. 322). Em exames, no máximo 8 horas por dia, salvo pagamento de cada hora extra pelo valor de uma aula (§ 1º). Nas férias, só serviço de exame (§ 2º). Dispensa sem justa causa no fim do ano letivo ou nas férias garante essa remuneração (§ 3º).
- Ajuste manual só por RH, com motivo e evento de auditoria ([29](../../../docs/v2/29-auditoria.md)).
- Ponto fechado não é alterado sem ajuste rastreado.
- Entrada e saída pela catraca, quando houver, é fonte auxiliar, não única ([35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md), seção 3.4).

##### 3.5 Rescisão e desligamento

**Ausente na v2.** Proposta de estados: `solicitado` → `calculado` → `homologado` (se a regra exigir) → `pago` → `encerrado`.

- Cálculo com aviso prévio, férias proporcionais, 13.º e multa do FGTS **(verificar)**.
- Evento de desligamento para o eSocial (S-2299) **(verificar)**.
- Desligamento de quem tem afastamento ativo bloqueado até a regularização.

##### 3.6 Benefícios

Vale-transporte, vale-refeição e plano. Regra de desconto e de elegibilidade por cargo **(verificar)**. Benefício concedido gera evento de folha.

### 13.2 [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 7

#### 7. Permissões

A matriz da v1 (seção 20 de [`spec_gestao_pessoas_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_pessoas_completo.md)) é aproveitada, com estas correções:

| Permissão | v1 | Proposta |
|---|---|---|
| SST — Gerenciar | Por papel e portal que precisa (seção 11). RH e gestão não recebem essa permissão | SESMT e médico do trabalho, cada um com escopo próprio. RH e gestão só veem o resultado sem CID |
| Folha — Processar e aprovar | GE, GP, SA | Mantido. Quem processa não aprova ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5) |
| Ponto — Ajuste manual | RH e GP | Mantido, com motivo obrigatório |
| Audit Log | SA, GE, GP, AUD | Mantido. Leitura do audit log gera evento ([29](../../../docs/v2/29-auditoria.md), seção 5) |
| Holerite próprio | Todos | Mantido |
