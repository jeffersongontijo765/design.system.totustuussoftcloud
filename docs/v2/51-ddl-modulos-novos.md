# 51 — DDL dos Módulos Novos e Pendentes

> Parte do [SDD v2](00-README.md). Fecha os DDL pendentes listados no [45](45-pendencias-consolidadas.md), seção 4. Convenções: MySQL 8 ou MariaDB 10.6, `utf8mb4`, horários em UTC (`DATETIME(3)`), chave interna `BIGINT UNSIGNED AUTO_INCREMENT` e `uuid CHAR(36)` para referência externa. Toda tabela de unidade tem `unidade_uuid` (regra de [03](03-dominio-tenancy.md), seção 1.1). Soft delete com `deleted_at` e `deleted_by` ([19](19-regras-modulos-3.md), seção 14). Tabelas de entidade ficam no banco da unidade. Tabelas de plataforma ficam no master.
> **Status:** DDL proposto, criado em 03/11/2026. Não foi executado. Antes de implementar, cada DDL passa por revisão do owner do módulo e por teste de migração ([10](10-implantacao-operacao.md), seção 5). Valores de domínio marcados com (jurídico) dependem do parecer ([50](50-pacote-juridico-e-norma.md)).

---

## 1. Atendimento (ATD-04)

```sql
CREATE TABLE atendimento_protocolos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  numero          VARCHAR(20) NOT NULL,
  tipo            ENUM('ticket','requerimento','reclamacao','sugestao','denuncia','pedido_titular') NOT NULL,
  canal           ENUM('site','formulario','whatsapp','telegram','instagram','messenger','telefone','presencial','portal') NOT NULL,
  prioridade      ENUM('baixa','media','alta','critica') NOT NULL,
  categoria_sensivel TINYINT(1) NOT NULL DEFAULT 0,
  estado          ENUM('novo','aberto','em_triagem','em_atendimento','aguardando_solicitante','aguardando_terceiro','resolvido','fechado','cancelado','reaberto','escalonado') NOT NULL,
  responsavel_uuid CHAR(36) NULL,
  solicitante_uuid CHAR(36) NULL,
  prazo_em        DATETIME(3) NULL,
  resolvido_em    DATETIME(3) NULL,
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at      DATETIME(3) NULL,
  deleted_by      CHAR(36) NULL,
  UNIQUE KEY ux_protocolo_numero (unidade_uuid, numero),
  INDEX ix_protocolo_fila (unidade_uuid, estado, prioridade, prazo_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE atendimento_eventos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  protocolo_id    BIGINT UNSIGNED NOT NULL,
  estado_anterior VARCHAR(30) NULL,
  estado_novo     VARCHAR(30) NOT NULL,
  ator_uuid       CHAR(36) NOT NULL,
  motivo          VARCHAR(500) NULL,
  criado_em       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_evento_protocolo FOREIGN KEY (protocolo_id) REFERENCES atendimento_protocolos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE atendimento_sla (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  unidade_uuid    CHAR(36) NOT NULL,
  prioridade      ENUM('baixa','media','alta','critica') NOT NULL,
  prazo_horas     INT UNSIGNED NOT NULL,
  UNIQUE KEY ux_sla_prioridade (unidade_uuid, prioridade)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Valores de SLA: 1 hora a 10 dias úteis por prioridade, ajustável por entidade ([32](32-atendimento-privacidade-por-portal.md), seção 7). Transcrição de chat fica em tabela própria com prazo de retenção **(jurídico)** ([50](50-pacote-juridico-e-norma.md), J-29).

---

## 2. Privacidade: ROPA (LGPD-01) e pedido de titular (LGPD-02)

```sql
-- Plataforma (master) e entidade (unidade): registro de atividades de tratamento
CREATE TABLE ropa_atividades (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  dominio         ENUM('plataforma','entidade') NOT NULL,
  unidade_uuid    CHAR(36) NULL,
  finalidade      VARCHAR(300) NOT NULL,
  base_legal      VARCHAR(60) NOT NULL,              -- código da matriz de [07](07-privacidade-lgpd.md), seção 3
  categorias_titular VARCHAR(200) NOT NULL,
  dados_tabela    VARCHAR(120) NULL,                 -- tabela de origem, quando houver
  sensivel        TINYINT(1) NOT NULL DEFAULT 0,
  retencao_codigo VARCHAR(60) NOT NULL,
  revisado_por    CHAR(36) NULL,
  revisado_em     DATETIME(3) NULL,
  deleted_at      DATETIME(3) NULL,
  INDEX ix_ropa_dominio (dominio, unidade_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Pedido de titular (acesso, correção, eliminação, portabilidade, revogação)
CREATE TABLE titular_pedidos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tipo            ENUM('acesso','correcao','eliminacao','portabilidade','revogacao','informacao') NOT NULL,
  solicitante_uuid CHAR(36) NOT NULL,                -- titular ou responsável legal com vínculo verificado
  verificacao     ENUM('pendente','verificado','recusado') NOT NULL,
  estado          ENUM('recebido','em_analise','atendido','parcial','recusado_com_motivo') NOT NULL,
  prazo_em        DATETIME(3) NOT NULL,
  motivo_recusa   VARCHAR(500) NULL,
  dpo_uuid        CHAR(36) NULL,
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  INDEX ix_titular_prazo (unidade_uuid, estado, prazo_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Prazo de resposta ao titular segue a LGPD (art. 19 e 18) **(verificar)**. Recusa sempre com motivo.

---

## 3. Contrato (CTR-01)

```sql
CREATE TABLE contratos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tipo            VARCHAR(40) NOT NULL,              -- tipos da [33](33-contratos-por-portal.md), seção 2
  portal_origem   ENUM('desenvolvedor','gestao','terceiros','aluno','responsaveis') NOT NULL,
  estado          ENUM('rascunho','em_negociacao','aguardando_assinatura','vigente','suspenso','vencido','encerrado','rescindido') NOT NULL,
  valor_centavos  BIGINT NULL,
  inicio_em       DATE NOT NULL,
  fim_em          DATE NULL,
  renovacao_auto  TINYINT(1) NOT NULL DEFAULT 0,
  aviso_renovacao_dias INT UNSIGNED NOT NULL DEFAULT 60,
  dpa_assinado    TINYINT(1) NOT NULL DEFAULT 0,      -- contrato com dado pessoal exige DPA antes da assinatura
  created_by      CHAR(36) NOT NULL,
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at      DATETIME(3) NULL,
  deleted_by      CHAR(36) NULL,
  INDEX ix_contrato_vencimento (unidade_uuid, estado, fim_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE contrato_partes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  contrato_id     BIGINT UNSIGNED NOT NULL,
  papel           ENUM('contratante','contratado','testemunha','interveniente') NOT NULL,
  documento_hash  CHAR(64) NOT NULL,                  -- CPF ou CNPJ em hash; o número fica no cadastro da parte
  CONSTRAINT fk_parte_contrato FOREIGN KEY (contrato_id) REFERENCES contratos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE contrato_assinaturas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  contrato_id     BIGINT UNSIGNED NOT NULL,
  parte_id        BIGINT UNSIGNED NOT NULL,
  provedor        VARCHAR(40) NOT NULL,              -- provedor de terceiros ou assinatura própria (CTR-06)
  tipo            ENUM('simples','avancada','qualificada_icp_brasil') NOT NULL,
  estado          ENUM('pendente','assinada','recusada','expirada') NOT NULL,
  evidencia_hash  CHAR(64) NULL,
  assinada_em     DATETIME(3) NULL,
  CONSTRAINT fk_assinatura_contrato FOREIGN KEY (contrato_id) REFERENCES contratos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Faixas de alçada e antecedência de alerta (60 e 30 dias) são regras de aplicação, não de tabela. Tipo de assinatura por contrato depende de J-19 ([50](50-pacote-juridico-e-norma.md)).

---

## 4. Acesso físico (ACC-06) e acesso aos dispositivos (ACC-08)

```sql
CREATE TABLE acesso_dispositivos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tipo            ENUM('catraca','porta','leitor_cracha','leitor_biometrico','camera') NOT NULL,
  conector        VARCHAR(40) NOT NULL,              -- protocolo aberto ou fabricante (decisão ACC-07)
  localizacao     VARCHAR(120) NOT NULL,
  modo_falha      ENUM('abre','fecha','mantem_estado') NOT NULL,
  lista_local_expira_em DATETIME(3) NULL,            -- lista de credenciais local no modo de falha (ACC-08)
  estado          ENUM('ativo','manutencao','inativo') NOT NULL,
  deleted_at      DATETIME(3) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE acesso_registros (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  unidade_uuid    CHAR(36) NOT NULL,
  dispositivo_id  BIGINT UNSIGNED NOT NULL,
  pessoa_uuid     CHAR(36) NULL,                     -- NULL para visitante sem cadastro
  visitante_id    BIGINT UNSIGNED NULL,
  direcao         ENUM('entrada','saida') NOT NULL,
  metodo          ENUM('cracha','biometria','facial','manual') NOT NULL,
  resultado       ENUM('permitido','negado','manual') NOT NULL,
  ocorrido_em     DATETIME(3) NOT NULL,
  INDEX ix_acesso_unidade (unidade_uuid, ocorrido_em),
  CONSTRAINT fk_acesso_dispositivo FOREIGN KEY (dispositivo_id) REFERENCES acesso_dispositivos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE acesso_autorizacoes_saida (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  unidade_uuid    CHAR(36) NOT NULL,
  aluno_uuid      CHAR(36) NOT NULL,
  responsavel_uuid CHAR(36) NOT NULL,                -- vínculo ativo verificado
  retirante_documento_hash CHAR(64) NOT NULL,
  valida_de       DATETIME(3) NOT NULL,
  valida_ate      DATETIME(3) NOT NULL,
  estado          ENUM('ativa','usada','expirada','revogada') NOT NULL,
  INDEX ix_autorizacao_aluno (unidade_uuid, aluno_uuid, valida_ate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE acesso_visitantes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  unidade_uuid    CHAR(36) NOT NULL,
  nome            VARCHAR(150) NOT NULL,
  documento_mascarado VARCHAR(20) NOT NULL,          -- sem número completo, sem imagem do documento
  motivo          VARCHAR(200) NOT NULL,
  autorizado_por_uuid CHAR(36) NOT NULL,
  valido_de       DATETIME(3) NOT NULL,
  valido_ate      DATETIME(3) NOT NULL,
  INDEX ix_visitante_unidade (unidade_uuid, valido_ate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

A lista local de credenciais de porta expira (campo `lista_local_expira_em`). Liberação de emergência (incêndio) não depende da rede e gera registro depois ([35](35-acesso-e-seguranca-fisica-por-portal.md), seção 7).

---

## 5. Formulários (FRM-05)

```sql
ALTER TABLE formulario_respostas
  ADD COLUMN substituida_por BIGINT UNSIGNED NULL,
  ADD COLUMN substituida_em DATETIME(3) NULL,
  ADD COLUMN motivo_substituicao VARCHAR(500) NULL,
  ADD CONSTRAINT fk_resposta_substituida FOREIGN KEY (substituida_por) REFERENCES formulario_respostas (id);
```

Resposta substituída não é apagada. Sai dos relatórios e fica no histórico ([41](41-formularios-e-pesquisas.md), seção 7).

---

## 6. Preceptoria (PRE-08)

```sql
CREATE TABLE preceptoria_instrumentos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  titulo          VARCHAR(200) NOT NULL,
  tipo            ENUM('autoavaliacao','avaliacao_preceptor','hibrido') NOT NULL,
  versao          INT UNSIGNED NOT NULL DEFAULT 1,
  estado          ENUM('rascunho','publicado','encerrado','arquivado') NOT NULL,
  formulario_id   BIGINT UNSIGNED NULL,              -- motor de [41](41-formularios-e-pesquisas.md)
  peso_autoavaliacao DECIMAL(5,2) NULL,              -- definido ao criar a autoavaliação
  peso_preceptor  DECIMAL(5,2) NULL,
  CHECK (peso_autoavaliacao IS NULL OR peso_preceptor IS NULL OR peso_autoavaliacao + peso_preceptor = 100),
  deleted_at      DATETIME(3) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE preceptoria_ciclos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  programa_uuid   CHAR(36) NOT NULL,
  inicio_em       DATE NOT NULL,
  fim_em          DATE NOT NULL,
  estado          ENUM('planejado','aberto','em_revisao','encerrado') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE preceptoria_avaliacoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  ciclo_id        BIGINT UNSIGNED NOT NULL,
  instrumento_id  BIGINT UNSIGNED NOT NULL,
  residente_uuid  CHAR(36) NOT NULL,
  preceptor_uuid  CHAR(36) NOT NULL,
  estado          ENUM('rascunho','enviada_pelo_residente','em_avaliacao_preceptor','em_revisao','devolvida','concluida') NOT NULL,
  nota_final      DECIMAL(6,2) NULL,
  concluida_em    DATETIME(3) NULL,
  CONSTRAINT fk_avaliacao_ciclo FOREIGN KEY (ciclo_id) REFERENCES preceptoria_ciclos (id),
  CONSTRAINT fk_avaliacao_instrumento FOREIGN KEY (instrumento_id) REFERENCES preceptoria_instrumentos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE preceptoria_tutoria (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tutorado_uuid   CHAR(36) NOT NULL,
  tutor_uuid      CHAR(36) NOT NULL,
  realizado_em    DATETIME(3) NOT NULL,
  duracao_min     SMALLINT UNSIGNED NOT NULL,
  anotacao_sensivel TINYINT(1) NOT NULL DEFAULT 0,
  anotacao_cifrada VARBINARY(4000) NULL,             -- cifrada na aplicação; chave do cofre
  INDEX ix_tutoria_tutorado (unidade_uuid, tutorado_uuid, realizado_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE preceptoria_metas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  pdi_id          BIGINT UNSIGNED NULL,
  tutorado_uuid   CHAR(36) NOT NULL,
  descricao       VARCHAR(500) NOT NULL,
  prazo_em        DATE NULL,
  estado          ENUM('planejada','em_andamento','atingida','nao_atingida','cancelada') NOT NULL,
  competencia_codigo VARCHAR(40) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE preceptoria_evidencias (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  avaliacao_id    BIGINT UNSIGNED NULL,
  meta_id         BIGINT UNSIGNED NULL,
  arquivo_uuid    CHAR(36) NULL,                     -- armazenamento de [21](21-busca-e-armazenamento.md)
  estado          ENUM('enviada','validada','recusada') NOT NULL,
  validada_por_uuid CHAR(36) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Regra de anonimato da avaliação de preceptor não está no DDL: ela é aplicada na consulta, com o mínimo de 2 respostas por grupo ([41](41-formularios-e-pesquisas.md), seção 3).

---

## 7. Pastoral (PAS-10)

```sql
CREATE TABLE pastoral_agenda (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tipo            ENUM('missa','celebracao','evento','atividade_capelania','confissao_horario') NOT NULL,
  tradicao        VARCHAR(30) NULL,                  -- NULL no modo ecumênico
  inicio_em       DATETIME(3) NOT NULL,
  fim_em          DATETIME(3) NOT NULL,
  local_reserva_uuid CHAR(36) NULL,                  -- ambiente de [44](44-agendamento-ambientes-equipamentos.md)
  estado          ENUM('agendada','realizada','cancelada') NOT NULL,
  INDEX ix_pastoral_agenda (unidade_uuid, inicio_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pastoral_escala (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  agenda_id       BIGINT UNSIGNED NOT NULL,
  funcao          VARCHAR(40) NOT NULL,              -- celebrante, leitor, ministro, músico, coroinha
  pessoa_uuid     CHAR(36) NOT NULL,
  confirmada_em   DATETIME(3) NULL,
  substituto_uuid CHAR(36) NULL,
  motivo_troca   VARCHAR(200) NULL,
  CONSTRAINT fk_escala_agenda FOREIGN KEY (agenda_id) REFERENCES pastoral_agenda (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pastoral_intencao (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  agenda_id       BIGINT UNSIGNED NOT NULL,
  nome_citado    VARCHAR(120) NOT NULL,
  frase           VARCHAR(200) NOT NULL,              -- sem dado de saúde
  excluir_apos_em DATETIME(3) NOT NULL,
  CONSTRAINT fk_intencao_agenda FOREIGN KEY (agenda_id) REFERENCES pastoral_agenda (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pastoral_acompanhamento (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  acompanhado_uuid CHAR(36) NOT NULL,
  acompanhante_uuid CHAR(36) NOT NULL,
  adesao_em       DATETIME(3) NOT NULL,               -- adesão voluntária registrada
  anotacao_cifrada VARBINARY(4000) NULL,             -- só o acompanhante lê
  estado          ENUM('ativo','encerrado','excluido') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pastoral_beneficiario (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  nome_cifrado    VARBINARY(500) NOT NULL,
  contato_cifrado VARBINARY(500) NULL,
  pessoas_no_nucleo SMALLINT UNSIGNED NOT NULL,
  ultimo_atendimento_em DATE NULL,
  revisao_em      DATE NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pastoral_campanha (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                  CHAR(36) NOT NULL UNIQUE,
  unidade_uuid          CHAR(36) NOT NULL,
  nome                  VARCHAR(120) NOT NULL,
  meta_valor_centavos   BIGINT UNSIGNED NULL,
  meta_itens            INT UNSIGNED NULL,
  inicio                DATE NOT NULL,
  fim                   DATE NOT NULL,
  responsavel_uuid      CHAR(36) NOT NULL,
  estado                ENUM('planejada','ativa','encerrada') NOT NULL DEFAULT 'planejada',
  CONSTRAINT ck_campanha_datas CHECK (fim >= inicio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pastoral_entrega (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  campanha_id       BIGINT UNSIGNED NULL,
  beneficiario_id   BIGINT UNSIGNED NOT NULL,
  item              VARCHAR(120) NOT NULL,
  quantidade        INT UNSIGNED NOT NULL,
  data_entrega      DATE NOT NULL,
  registrada_por    CHAR(36) NOT NULL,
  CONSTRAINT fk_entrega_campanha FOREIGN KEY (campanha_id) REFERENCES pastoral_campanha (id),
  CONSTRAINT fk_entrega_beneficiario FOREIGN KEY (beneficiario_id) REFERENCES pastoral_beneficiario (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pastoral_doacao (
  id                        BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                      CHAR(36) NOT NULL UNIQUE,
  unidade_uuid              CHAR(36) NOT NULL,
  campanha_id               BIGINT UNSIGNED NULL,
  doador_pessoa_uuid        CHAR(36) NULL,
  anonima                   TINYINT(1) NOT NULL DEFAULT 0,
  valor_centavos            BIGINT UNSIGNED NOT NULL,
  data_doacao               DATE NOT NULL,
  lancamento_financeiro_uuid CHAR(36) NULL,
  CONSTRAINT fk_doacao_campanha FOREIGN KEY (campanha_id) REFERENCES pastoral_campanha (id),
  CONSTRAINT ck_doacao_anonima CHECK (anonima = 0 OR doador_pessoa_uuid IS NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Confissão não tem tabela. O tipo `confissao_horario` em `pastoral_agenda` guarda só o horário público do local ([43](43-pastoral-por-portal.md), seção 2.1).

---

## 8. Agendamento de ambientes (AMB-08)

```sql
CREATE TABLE recursos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tipo            ENUM('ambiente','equipamento','kit') NOT NULL,
  nome            VARCHAR(150) NOT NULL,
  capacidade      INT UNSIGNED NULL,
  reservavel      TINYINT(1) NOT NULL DEFAULT 1,
  patrimonio_uuid CHAR(36) NULL,                     -- bem do patrimônio ([19](19-regras-modulos-3.md), seção 8)
  estado          ENUM('ativo','manutencao','inativo') NOT NULL,
  deleted_at      DATETIME(3) NULL,
  INDEX ix_recursos_unidade (unidade_uuid, tipo, estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE recurso_composicao (
  kit_id          BIGINT UNSIGNED NOT NULL,
  item_id         BIGINT UNSIGNED NOT NULL,
  quantidade      INT UNSIGNED NOT NULL,
  PRIMARY KEY (kit_id, item_id),
  CONSTRAINT fk_kit FOREIGN KEY (kit_id) REFERENCES recursos (id),
  CONSTRAINT fk_item FOREIGN KEY (item_id) REFERENCES recursos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE reservas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  recurso_id      BIGINT UNSIGNED NOT NULL,
  origem_tipo     ENUM('grade','prova','evento','pastoral','preceptoria','reuniao','avulsa') NOT NULL,
  origem_uuid     CHAR(36) NULL,
  solicitante_uuid CHAR(36) NOT NULL,
  inicio_utc      DATETIME(3) NOT NULL,
  fim_utc         DATETIME(3) NOT NULL,
  prioridade      TINYINT UNSIGNED NOT NULL,          -- 1 grade, 2 prova, 3 evento e pastoral, 4 preceptoria e reunião, 5 avulsa
  estado          ENUM('solicitada','aprovada','recusada','em_uso','concluida','cancelada','nao_utilizada') NOT NULL,
  checkin_em      DATETIME(3) NULL,
  motivo_cancelamento VARCHAR(300) NULL,
  INDEX ix_reserva_recurso (recurso_id, estado, inicio_utc),
  CONSTRAINT fk_reserva_recurso FOREIGN KEY (recurso_id) REFERENCES recursos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE reserva_recursos (
  reserva_id      BIGINT UNSIGNED NOT NULL,
  recurso_id      BIGINT UNSIGNED NOT NULL,
  quantidade      INT UNSIGNED NOT NULL DEFAULT 1,
  retirada_em     DATETIME(3) NULL,
  devolucao_em    DATETIME(3) NULL,
  estado_devolucao ENUM('ok','faltando_peca','danificado') NULL,
  PRIMARY KEY (reserva_id, recurso_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE recurso_bloqueios (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  recurso_id      BIGINT UNSIGNED NOT NULL,
  inicio_utc      DATETIME(3) NOT NULL,
  fim_utc         DATETIME(3) NOT NULL,
  motivo          ENUM('manutencao','feriado','uso_institucional','clima') NOT NULL,
  INDEX ix_bloqueio_recurso (recurso_id, inicio_utc, fim_utc)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Regra de conflito: checagem de `reservas` aprovadas e `recurso_bloqueios` sobrepostos, dentro de transação com `SELECT ... FOR UPDATE` no registro de `recursos`. Antecedência de 50 minutos e não-utilização de 15 minutos são regras de aplicação ([44](44-agendamento-ambientes-equipamentos.md), seção 3).

---

## 9. Sala de aula online (LIV-10)

O modelo de sala não usa tabelas `tenants` nem `users` no banco da unidade. A identidade fica no master ([03](03-dominio-tenancy.md), seção 1.1). A unidade guarda só referências.

```sql
CREATE TABLE sessoes_aula (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  turma_uuid      CHAR(36) NULL,
  tipo            ENUM('aula_turma','reuniao_responsavel','reuniao_equipe','convidado_externo') NOT NULL,
  agendada_inicio_utc DATETIME(3) NOT NULL,
  agendada_fim_utc   DATETIME(3) NOT NULL,
  estado          ENUM('agendada','aberta','em_andamento','encerrada','cancelada') NOT NULL,
  gravacao_permitida TINYINT(1) NOT NULL DEFAULT 0,
  transcricao_permitida TINYINT(1) NOT NULL DEFAULT 0,
  criada_por_uuid CHAR(36) NOT NULL,
  INDEX ix_sessao_unidade (unidade_uuid, agendada_inicio_utc)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sessao_participacoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  sessao_id       BIGINT UNSIGNED NOT NULL,
  pessoa_uuid     CHAR(36) NULL,                    -- NULL para convidado externo
  papel           ENUM('professor','aluno','responsavel','diretor','coordenador','convidado','moderador') NOT NULL,
  entrada_em      DATETIME(3) NULL,
  saida_em        DATETIME(3) NULL,
  tempo_conectado_s INT UNSIGNED NOT NULL DEFAULT 0,
  presenca_origem ENUM('automatica','confirmada_pelo_aluno','corrigida_pelo_professor') NULL,
  CONSTRAINT fk_participacao_sessao FOREIGN KEY (sessao_id) REFERENCES sessoes_aula (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Presença conta com 40 minutos de conexão, configurável por entidade ([40](40-aulas-online-por-portal.md), seção 6). A conta de cada pessoa está no master, e a participação guarda só o `pessoa_uuid`.

---

## 10. Matrícula (MAT-07)

```sql
CREATE TABLE matriculas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  aluno_uuid      CHAR(36) NOT NULL,
  turma_uuid      CHAR(36) NULL,
  periodo_letivo  VARCHAR(10) NOT NULL,
  tipo            ENUM('regular','especial','transferencia','condicional','ead') NOT NULL,
  estado          ENUM('lista_espera','solicitada','em_analise','condicional','ativa','trancada','transferida','concluida','cancelada','nao_rematriculada') NOT NULL,
  prazo_regularizacao_em DATETIME(3) NULL,
  solicitada_em   DATETIME(3) NULL,
  motivo_estado   VARCHAR(500) NULL,
  created_by      CHAR(36) NOT NULL,
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at      DATETIME(3) NULL,
  vinculo_ativo_chave VARCHAR(120) AS (CASE WHEN estado IN ('solicitada','em_analise','condicional','ativa','trancada') THEN CONCAT(aluno_uuid,'|',unidade_uuid,'|',periodo_letivo) ELSE NULL END) STORED,
  UNIQUE KEY ux_matricula_ativa (vinculo_ativo_chave)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE vagas_reserva (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  turma_uuid      CHAR(36) NOT NULL,
  matricula_uuid  CHAR(36) NOT NULL,
  reservada_em    DATETIME(3) NOT NULL,
  expira_em       DATETIME(3) NOT NULL,
  UNIQUE KEY ux_vaga_turma_matricula (turma_uuid, matricula_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE matricula_pendencias (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  matricula_uuid  CHAR(36) NOT NULL,
  tipo            ENUM('financeira','documental') NOT NULL,
  documento_tipo  VARCHAR(60) NULL,
  prazo_em        DATETIME(3) NULL,
  resolvida_em    DATETIME(3) NULL,
  INDEX ix_pendencia_matricula (unidade_uuid, matricula_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE janelas_rematricula (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                    CHAR(36) NOT NULL UNIQUE,
  unidade_uuid            CHAR(36) NOT NULL,
  serie                   VARCHAR(60) NULL,
  curso_uuid              CHAR(36) NULL,
  abre_em                 DATETIME(3) NOT NULL,
  fecha_em                DATETIME(3) NOT NULL,
  prazo_confirmacao_dias  TINYINT UNSIGNED NOT NULL,
  CONSTRAINT ck_janela_datas CHECK (fecha_em > abre_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE trancamentos (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                  CHAR(36) NOT NULL UNIQUE,
  unidade_uuid          CHAR(36) NOT NULL,
  matricula_uuid        CHAR(36) NOT NULL,
  motivo                ENUM('pessoal','financeiro','saude','militar','outro') NOT NULL,
  descricao             VARCHAR(1000) NULL,
  solicitado_em         DATETIME(3) NOT NULL,
  retorno_previsto_em   DATE NULL,
  estado                ENUM('solicitado','aprovado','recusado','ativo','encerrado') NOT NULL,
  protocolo_uuid        CHAR(36) NULL,
  CONSTRAINT ck_trancamento_descricao CHECK (motivo <> 'outro' OR descricao IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE transferencias (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                  CHAR(36) NOT NULL UNIQUE,
  unidade_uuid          CHAR(36) NOT NULL,
  matricula_origem_uuid CHAR(36) NOT NULL,
  matricula_destino_uuid CHAR(36) NULL,
  tipo                  ENUM('turma','curso','unidade') NOT NULL,
  solicitado_por        CHAR(36) NOT NULL,
  aprovado_por          CHAR(36) NULL,
  aprovado_em           DATETIME(3) NULL,
  CONSTRAINT ck_transf_aprovacao CHECK (aprovado_por IS NULL OR aprovado_por <> solicitado_por)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Transferência entre unidades usa pedido e aprovação da origem, sem consulta ao banco da outra unidade.

CREATE TABLE lista_espera (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  processo_uuid   CHAR(36) NOT NULL,
  candidato_uuid  CHAR(36) NOT NULL,
  prioridade      SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  estado          ENUM('aguardando','notificado','convertido','expirado','desistiu') NOT NULL,
  notificado_em   DATETIME(3) NULL,
  expira_em       DATETIME(3) NULL,
  UNIQUE KEY ux_espera (processo_uuid, candidato_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

A coluna gerada `vinculo_ativo_chave` só tem valor para matrícula em andamento ou ativa. A constraint `ux_matricula_ativa` impede dois vínculos desses no mesmo aluno, unidade e período. Matrículas canceladas ou concluídas não entram na chave. Concorrência de vaga é tratada na transação de confirmação, com bloqueio da turma ([46](46-matricula-e-rematricula-por-portal.md), seção 7).

---

## 11. TI (TI-04)

```sql
CREATE TABLE ti_ativos (
  patrimonio_uuid CHAR(36) NOT NULL PRIMARY KEY,     -- dono do dado é o patrimônio ([36](36-tecnologia-da-informacao-por-portal.md), seção 5)
  categoria_ti    VARCHAR(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ti_licencas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  software        VARCHAR(150) NOT NULL,
  quantidade      INT UNSIGNED NOT NULL,
  vencimento_em   DATE NULL,
  responsavel_uuid CHAR(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ti_incidentes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  atendimento_protocolo_uuid CHAR(36) NULL,          -- chamado é atendimento de categoria TI
  estado          ENUM('aberto','em_atendimento','resolvido','fechado') NOT NULL,
  problema_id     BIGINT UNSIGNED NULL,
  criado_em       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ti_problemas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  causa_raiz      VARCHAR(500) NULL,
  estado          ENUM('aberto','investigando','conhecido','resolvido') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ti_mudancas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tipo            ENUM('padrao','normal','emergencial') NOT NULL,
  estado          ENUM('solicitada','aprovada','em_execucao','concluida','revertida','recusada') NOT NULL,
  aprovacao_limite_em DATETIME(3) NULL,              -- emergencial: 48 horas para aprovação posterior
  comite_votos_favoraveis TINYINT UNSIGNED NULL,     -- quórum de 2 de 3 (TI-07)
  criada_por_uuid CHAR(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 12. Documentos emitidos (DOC-06)

```sql
CREATE TABLE doc_tipos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  codigo          VARCHAR(40) NOT NULL,
  nome            VARCHAR(150) NOT NULL,
  categoria       ENUM('contrato','declaracao','certidao','acervo','termo','ata','comunicado','outro') NOT NULL,
  validade_dias   INT UNSIGNED NULL,                 -- padrão de 90 quando nulo (DOC-04)
  exige_assinatura TINYINT(1) NOT NULL DEFAULT 0,
  deleted_at      DATETIME(3) NULL,
  UNIQUE KEY ux_doc_tipo_codigo (unidade_uuid, codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE doc_modelos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  tipo_id         BIGINT UNSIGNED NOT NULL,
  nome            VARCHAR(150) NOT NULL,
  estado          ENUM('rascunho','em_revisao','publicado','arquivado') NOT NULL,
  versao_publicada INT UNSIGNED NULL,
  criado_por_uuid CHAR(36) NOT NULL,
  aprovado_por_uuid CHAR(36) NULL,
  CHECK (aprovado_por_uuid IS NULL OR aprovado_por_uuid <> criado_por_uuid),
  deleted_at      DATETIME(3) NULL,
  CONSTRAINT fk_modelo_tipo FOREIGN KEY (tipo_id) REFERENCES doc_tipos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE doc_modelo_versoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  modelo_id       BIGINT UNSIGNED NOT NULL,
  versao          INT UNSIGNED NOT NULL,
  layout_json     JSON NOT NULL,                     -- papel, margens, blocos, variáveis, condicionais
  componentes_json JSON NULL,                        -- versões de componentes usadas (seção 16 de [48](48-gerador-de-documentos-por-portal.md))
  publicada_em    DATETIME(3) NULL,
  UNIQUE KEY ux_modelo_versao (modelo_id, versao),
  CONSTRAINT fk_versao_modelo FOREIGN KEY (modelo_id) REFERENCES doc_modelos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE doc_emissoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  modelo_versao_id BIGINT UNSIGNED NOT NULL,
  pessoa_uuid     CHAR(36) NOT NULL,
  protocolo       VARCHAR(30) NOT NULL,
  estado          ENUM('solicitado','em_emissao','emitido','aguardando_assinatura','assinado','expirado','cancelado','revogado') NOT NULL,
  emitido_em      DATETIME(3) NULL,
  valido_ate      DATE NULL,
  arquivo_uuid    CHAR(36) NULL,                     -- armazenamento de [21](21-busca-e-armazenamento.md)
  arquivo_sha256  CHAR(64) NULL,
  motivo_estado   VARCHAR(500) NULL,
  emitido_por_uuid CHAR(36) NOT NULL,
  UNIQUE KEY ux_emissao_protocolo (unidade_uuid, protocolo),
  INDEX ix_emissao_pessoa (unidade_uuid, pessoa_uuid),
  CONSTRAINT fk_emissao_versao FOREIGN KEY (modelo_versao_id) REFERENCES doc_modelo_versoes (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE doc_validacao (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  emissao_id      BIGINT UNSIGNED NOT NULL,
  codigo_hash     CHAR(64) NOT NULL UNIQUE,          -- hash do código de validação, nunca o código em texto
  criado_em       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_validacao_emissao FOREIGN KEY (emissao_id) REFERENCES doc_emissoes (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE doc_revogacoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  emissao_id      BIGINT UNSIGNED NOT NULL,
  motivo          VARCHAR(500) NOT NULL,
  revogado_por_uuid CHAR(36) NOT NULL,
  revogado_em     DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_revogacao_emissao FOREIGN KEY (emissao_id) REFERENCES doc_emissoes (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE doc_componentes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  nome            VARCHAR(150) NOT NULL,
  categoria       VARCHAR(60) NOT NULL,
  versao          INT UNSIGNED NOT NULL,
  estrutura_json  JSON NOT NULL,
  escopo          ENUM('entidade','unidade') NOT NULL,
  UNIQUE KEY ux_componente_versao (uuid, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`doc_validacao` guarda só o hash do código, para que um vazamento do banco não revele códigos válidos. A validação pública compara o hash da entrada.

---

## 13. Pendências deste documento

| # | Pendência | Tipo |
|---|---|---|
| DDL-01 | Revisão de cada DDL pelo owner do módulo antes da migração | Owner |
| DDL-02 | Teste de migração em ambiente de homologação por banco de unidade ([10](10-implantacao-operacao.md), seção 5) | Operação |
| DDL-03 | Valores de domínio marcados (jurídico) no [50](50-pacote-juridico-e-norma.md) | (jurídico) |

---

## 14. Critérios de aceite

- [ ] Toda tabela de unidade tem `unidade_uuid` (verificação de DDL).
- [ ] Tabela de pastoral não tem coluna de confissão (varredura de DDL).
- [ ] Coluna de anotação sensível é `VARBINARY`, cifrada na aplicação (verificação de DDL).
- [ ] `ux_matricula_ativa` impede duplicidade de vínculo (teste de constraint).
- [ ] Pesos de preceptoria somam 100 quando preenchidos (teste de CHECK).

---

## 15. DDL dos módulos 55 a 72 (primeira parte)

> Esta seção cobre notificações (NOT-07), calendário (CAL-05), estrutura acadêmica (EST-07), turmas e grade (TUR-05), diário (DIA-08) e boletim e conselho (BOL-10). Os demais módulos novos têm DDL nas seções 15.8 a 15.20. A tabela da seção 15.7 é o índice. Mesmas convenções da seção de abertura. Regras que o SQL não expressa, como pesos que somam 100 por período e a aprovação em duas pessoas, são validadas na aplicação e têm teste de aceite.

### 15.1 Notificações (NOT-07)

```sql
CREATE TABLE notif_templates (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  codigo          VARCHAR(60) NOT NULL,
  versao          INT UNSIGNED NOT NULL,
  idioma          CHAR(5) NOT NULL DEFAULT 'pt-BR',
  categoria       ENUM('academico','financeiro','pastoral','seguranca','saude') NOT NULL,
  corpo           TEXT NOT NULL,
  variaveis       JSON NOT NULL,
  aprovado_em     DATETIME(3) NULL,
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at      DATETIME(3) NULL,
  deleted_by      CHAR(36) NULL,
  UNIQUE KEY ux_template_versao (unidade_uuid, codigo, idioma, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE notif_notificacoes (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid        CHAR(36) NOT NULL,
  template_id         BIGINT UNSIGNED NOT NULL,
  publico_tipo        ENUM('turma','responsaveis_turma','unidade','entidade','plataforma') NOT NULL,
  publico_ref         CHAR(36) NULL,
  total_destinatarios INT UNSIGNED NOT NULL,
  criado_por          CHAR(36) NOT NULL,
  aprovado_por        CHAR(36) NULL,
  estado              ENUM('draft','in_review','scheduled','queued','processing','sent','cancelled','archived') NOT NULL,
  agendado_para       DATETIME(3) NULL,
  created_at          DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at          DATETIME(3) NULL,
  deleted_by          CHAR(36) NULL,
  CONSTRAINT fk_notif_template FOREIGN KEY (template_id) REFERENCES notif_templates (id),
  CONSTRAINT ck_notif_aprovacao CHECK (aprovado_por IS NULL OR aprovado_por <> criado_por),
  INDEX ix_notif_fila (unidade_uuid, estado, agendado_para)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE notif_entregas (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  notificacao_id    BIGINT UNSIGNED NOT NULL,
  destinatario_uuid CHAR(36) NOT NULL,
  canal             ENUM('app','email','sms','whatsapp') NOT NULL,
  provedor          VARCHAR(40) NULL,
  estado            ENUM('queued','processing','sent','delivered','read','failed') NOT NULL,
  tentativas        TINYINT UNSIGNED NOT NULL DEFAULT 0,
  enviado_em        DATETIME(3) NULL,
  lido_em           DATETIME(3) NULL,
  CONSTRAINT fk_entrega_notif FOREIGN KEY (notificacao_id) REFERENCES notif_notificacoes (id),
  UNIQUE KEY ux_entrega (notificacao_id, destinatario_uuid, canal),
  INDEX ix_entrega_estado (estado, enviado_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE notif_preferencias (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  pessoa_uuid     CHAR(36) NOT NULL,
  tipo_aviso      ENUM('academico','financeiro','comunicado') NOT NULL,
  canal           ENUM('app','email','sms','whatsapp') NOT NULL,
  ativo           TINYINT(1) NOT NULL DEFAULT 1,
  silencio_inicio TIME NOT NULL DEFAULT '21:00:00',
  silencio_fim    TIME NOT NULL DEFAULT '07:00:00',
  UNIQUE KEY ux_preferencia (pessoa_uuid, tipo_aviso, canal)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE notif_provedores (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  canal           ENUM('app','email','sms','whatsapp') NOT NULL,
  nome            VARCHAR(40) NOT NULL,
  primario        TINYINT(1) NOT NULL DEFAULT 0,
  saude           ENUM('ok','degradado','fora') NOT NULL DEFAULT 'ok',
  falhas_seguidas INT UNSIGNED NOT NULL DEFAULT 0,
  UNIQUE KEY ux_provedor (canal, nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Obrigatório: `notif_preferencias` não permite desligar aviso obrigatório (verificação, recuperação, MFA, saúde e segurança). A regra é checada na aplicação antes de gravar. Ver [57](57-notificacoes-por-portal.md), seção 3.3.

### 15.2 Calendário (CAL-05)

```sql
CREATE TABLE cal_calendarios (
  id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid          CHAR(36) NOT NULL UNIQUE,
  unidade_uuid  CHAR(36) NOT NULL,
  ano           SMALLINT UNSIGNED NOT NULL,
  estado        ENUM('rascunho','publicado','alterado') NOT NULL DEFAULT 'rascunho',
  created_at    DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at    DATETIME(3) NULL,
  deleted_by    CHAR(36) NULL,
  UNIQUE KEY ux_calendario_ano (unidade_uuid, ano)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cal_periodos (
  id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid          CHAR(36) NOT NULL UNIQUE,
  unidade_uuid  CHAR(36) NOT NULL,
  calendario_id BIGINT UNSIGNED NOT NULL,
  tipo          ENUM('bimestre','trimestre','semestre','modulo') NOT NULL,
  numero        TINYINT UNSIGNED NOT NULL,
  inicio        DATE NOT NULL,
  fim           DATE NOT NULL,
  estado        ENUM('planejado','aberto','em_fechamento','fechado','reaberto') NOT NULL DEFAULT 'planejado',
  CONSTRAINT fk_periodo_cal FOREIGN KEY (calendario_id) REFERENCES cal_calendarios (id),
  CONSTRAINT ck_periodo_datas CHECK (fim >= inicio),
  UNIQUE KEY ux_periodo_numero (calendario_id, tipo, numero)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cal_dias_nao_letivos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  calendario_id   BIGINT UNSIGNED NOT NULL,
  data            DATE NOT NULL,
  tipo            ENUM('feriado_nacional','feriado_estadual','feriado_municipal','recesso','ponto_facultativo','planejamento') NOT NULL,
  fonte           ENUM('secretaria','site_oficial','ia_confirmada') NOT NULL,
  fonte_ref       VARCHAR(500) NULL,
  confirmado_por  CHAR(36) NOT NULL,
  aplica_unidade  TINYINT(1) NOT NULL DEFAULT 1,
  CONSTRAINT fk_naoletivo_cal FOREIGN KEY (calendario_id) REFERENCES cal_calendarios (id),
  UNIQUE KEY ux_naoletivo (unidade_uuid, data, tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cal_alteracoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  calendario_id   BIGINT UNSIGNED NOT NULL,
  motivo          VARCHAR(500) NOT NULL,
  solicitado_por  CHAR(36) NOT NULL,
  aprovado_por    CHAR(36) NULL,
  estado          ENUM('pendente','aprovada','recusada') NOT NULL DEFAULT 'pendente',
  CONSTRAINT fk_alteracao_cal FOREIGN KEY (calendario_id) REFERENCES cal_calendarios (id),
  CONSTRAINT ck_alteracao_aprovacao CHECK (aprovado_por IS NULL OR aprovado_por <> solicitado_por)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cal_eventos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tipo            ENUM('festividade','feira','reuniao_coletiva','esportivo','formatura','pastoral') NOT NULL,
  titulo          VARCHAR(200) NOT NULL,
  inicio          DATETIME(3) NOT NULL,
  fim             DATETIME(3) NOT NULL,
  recurso_uuid    CHAR(36) NULL,
  publico_regra   JSON NOT NULL,
  capacidade      INT UNSIGNED NULL,
  custo_centavos  BIGINT UNSIGNED NULL,
  responsavel_uuid CHAR(36) NOT NULL,
  aprovado_por    CHAR(36) NULL,
  estado          ENUM('rascunho','publicado','em_andamento','encerrado','cancelado') NOT NULL DEFAULT 'rascunho',
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at      DATETIME(3) NULL,
  deleted_by      CHAR(36) NULL,
  CONSTRAINT ck_evento_datas CHECK (fim > inicio),
  INDEX ix_evento_data (unidade_uuid, inicio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cal_inscricoes (
  id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid          CHAR(36) NOT NULL UNIQUE,
  unidade_uuid  CHAR(36) NOT NULL,
  evento_id     BIGINT UNSIGNED NOT NULL,
  pessoa_uuid   CHAR(36) NOT NULL,
  estado        ENUM('inscrito','lista_espera','cancelado','presente','ausente') NOT NULL,
  criado_em     DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_inscricao_evento FOREIGN KEY (evento_id) REFERENCES cal_eventos (id),
  UNIQUE KEY ux_inscricao (evento_id, pessoa_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cal_certificados (
  id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid          CHAR(36) NOT NULL UNIQUE,
  unidade_uuid  CHAR(36) NOT NULL,
  evento_id     BIGINT UNSIGNED NOT NULL,
  pessoa_uuid   CHAR(36) NOT NULL,
  codigo_hash   CHAR(64) NOT NULL,
  emitido_em    DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_cert_evento FOREIGN KEY (evento_id) REFERENCES cal_eventos (id),
  UNIQUE KEY ux_certificado (evento_id, pessoa_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Certificado só existe com presença registrada ([58](58-calendario-e-eventos-por-portal.md), seção 9). O código de validação guarda só o hash ([54](54-gestao-de-documentos-tres-contextos.md)).

### 15.3 Estrutura acadêmica (EST-07)

```sql
CREATE TABLE est_cursos (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid        CHAR(36) NOT NULL,
  tipo                ENUM('infantil','fundamental','medio','tecnico','graduacao','pos_lato','livre') NOT NULL,
  codigo              VARCHAR(30) NOT NULL,
  nome                VARCHAR(200) NOT NULL,
  carga_horaria_total INT UNSIGNED NULL,
  situacao            ENUM('rascunho','ativo','suspenso','extinto') NOT NULL DEFAULT 'rascunho',
  created_at          DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at          DATETIME(3) NULL,
  deleted_by          CHAR(36) NULL,
  UNIQUE KEY ux_curso_codigo (unidade_uuid, codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE est_disciplinas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  codigo          VARCHAR(30) NOT NULL,
  nome            VARCHAR(200) NOT NULL,
  ementa          TEXT NULL,
  carga_horaria   INT UNSIGNED NOT NULL,
  tipo            ENUM('obrigatoria','optativa','eletiva','estagio','tcc','atividade_complementar') NOT NULL,
  situacao        ENUM('ativa','inativa') NOT NULL DEFAULT 'ativa',
  deleted_at      DATETIME(3) NULL,
  deleted_by      CHAR(36) NULL,
  UNIQUE KEY ux_disciplina_codigo (unidade_uuid, codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE est_grades (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  curso_id          BIGINT UNSIGNED NOT NULL,
  versao            INT UNSIGNED NOT NULL,
  vigencia_inicio   DATE NOT NULL,
  vigencia_fim      DATE NULL,
  estado            ENUM('rascunho','vigente','substituida') NOT NULL DEFAULT 'rascunho',
  CONSTRAINT fk_grade_curso FOREIGN KEY (curso_id) REFERENCES est_cursos (id),
  CONSTRAINT ck_grade_vigencia CHECK (vigencia_fim IS NULL OR vigencia_fim >= vigencia_inicio),
  UNIQUE KEY ux_grade_versao (curso_id, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE est_grade_itens (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  grade_id        BIGINT UNSIGNED NOT NULL,
  disciplina_id   BIGINT UNSIGNED NOT NULL,
  periodo_serie   TINYINT UNSIGNED NOT NULL,
  carga_horaria   INT UNSIGNED NOT NULL,
  obrigatoria     TINYINT(1) NOT NULL DEFAULT 1,
  CONSTRAINT fk_item_grade FOREIGN KEY (grade_id) REFERENCES est_grades (id),
  CONSTRAINT fk_item_disciplina FOREIGN KEY (disciplina_id) REFERENCES est_disciplinas (id),
  UNIQUE KEY ux_item_grade (grade_id, disciplina_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE est_pre_requisitos (
  grade_item_id          BIGINT UNSIGNED NOT NULL,
  requisito_disciplina_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (grade_item_id, requisito_disciplina_id),
  CONSTRAINT fk_prereq_item FOREIGN KEY (grade_item_id) REFERENCES est_grade_itens (id),
  CONSTRAINT fk_prereq_disc FOREIGN KEY (requisito_disciplina_id) REFERENCES est_disciplinas (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE est_ppc (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  curso_id          BIGINT UNSIGNED NOT NULL,
  versao            INT UNSIGNED NOT NULL,
  vigencia_inicio   DATE NOT NULL,
  vigencia_fim      DATE NULL,
  ata_colegiado_uuid CHAR(36) NULL,
  estado            ENUM('rascunho','aprovado','substituido') NOT NULL DEFAULT 'rascunho',
  CONSTRAINT fk_ppc_curso FOREIGN KEY (curso_id) REFERENCES est_cursos (id),
  UNIQUE KEY ux_ppc_versao (curso_id, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE est_equivalencias (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                    CHAR(36) NOT NULL UNIQUE,
  unidade_uuid            CHAR(36) NOT NULL,
  disciplina_origem_id    BIGINT UNSIGNED NOT NULL,
  disciplina_destino_id   BIGINT UNSIGNED NOT NULL,
  tipo                    ENUM('total','parcial','sem_equivalencia') NOT NULL,
  responsavel_uuid        CHAR(36) NOT NULL,
  aprovado_em             DATE NOT NULL,
  CONSTRAINT fk_equiv_origem FOREIGN KEY (disciplina_origem_id) REFERENCES est_disciplinas (id),
  CONSTRAINT fk_equiv_destino FOREIGN KEY (disciplina_destino_id) REFERENCES est_disciplinas (id),
  UNIQUE KEY ux_equivalencia (disciplina_origem_id, disciplina_destino_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE est_sistemas_avaliativos (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                  CHAR(36) NOT NULL UNIQUE,
  unidade_uuid          CHAR(36) NOT NULL,
  curso_id              BIGINT UNSIGNED NOT NULL,
  versao                INT UNSIGNED NOT NULL,
  escala                ENUM('numerica','conceitual','percentual') NOT NULL,
  nota_minima           DECIMAL(6,2) NOT NULL,
  piso_recuperacao      DECIMAL(6,2) NULL,
  metodo                ENUM('aritmetica','ponderada') NOT NULL,
  recuperacao           ENUM('paralela','final','ambas') NOT NULL,
  recuperacao_efeito    ENUM('substitui','compoe') NOT NULL,
  frequencia_minima_pct DECIMAL(5,2) NULL,
  casas_decimais        TINYINT UNSIGNED NOT NULL DEFAULT 1,
  vigencia_inicio       DATE NOT NULL,
  CONSTRAINT fk_sistema_curso FOREIGN KEY (curso_id) REFERENCES est_cursos (id),
  CONSTRAINT ck_sistema_freq CHECK (frequencia_minima_pct IS NULL OR frequencia_minima_pct BETWEEN 0 AND 100),
  UNIQUE KEY ux_sistema_versao (curso_id, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE est_sistema_pesos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  sistema_id      BIGINT UNSIGNED NOT NULL,
  tipo_avaliacao  ENUM('prova','trabalho','seminario','pratica','autoavaliacao','recuperacao') NOT NULL,
  peso_pct        DECIMAL(5,2) NOT NULL,
  CONSTRAINT fk_peso_sistema FOREIGN KEY (sistema_id) REFERENCES est_sistemas_avaliativos (id),
  CONSTRAINT ck_peso_faixa CHECK (peso_pct BETWEEN 0 AND 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Soma dos pesos de um período igual a 100 é regra de aplicação (EST-04 e [59](59-estrutura-academica-por-portal.md), seção 4).

### 15.4 Turmas e grade de horários (TUR-05)

```sql
CREATE TABLE tur_turmas (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                  CHAR(36) NOT NULL UNIQUE,
  unidade_uuid          CHAR(36) NOT NULL,
  codigo                VARCHAR(30) NOT NULL,
  curso_id              BIGINT UNSIGNED NOT NULL,
  grade_id              BIGINT UNSIGNED NOT NULL,
  periodo_id            BIGINT UNSIGNED NOT NULL,
  turno                 ENUM('manha','tarde','noite','integral','ead') NOT NULL,
  capacidade            INT UNSIGNED NOT NULL,
  recurso_referencia_uuid CHAR(36) NULL,
  professor_regente_uuid CHAR(36) NULL,
  estado                ENUM('planejada','aberta','em_andamento','encerrada','cancelada') NOT NULL DEFAULT 'planejada',
  deleted_at            DATETIME(3) NULL,
  deleted_by            CHAR(36) NULL,
  CONSTRAINT fk_turma_curso FOREIGN KEY (curso_id) REFERENCES est_cursos (id),
  CONSTRAINT fk_turma_grade FOREIGN KEY (grade_id) REFERENCES est_grades (id),
  UNIQUE KEY ux_turma_codigo (unidade_uuid, periodo_id, codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE tur_enturmacoes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  turma_id          BIGINT UNSIGNED NOT NULL,
  matricula_uuid    CHAR(36) NOT NULL,
  estado            ENUM('ativa','transferida','cancelada') NOT NULL,
  vinculo_ativo_chave VARCHAR(100) AS (CASE WHEN estado = 'ativa' THEN CONCAT(matricula_uuid, '|', turma_id) END) STORED,
  criado_em         DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_enturma_turma FOREIGN KEY (turma_id) REFERENCES tur_turmas (id),
  UNIQUE KEY ux_enturmacao_ativa (vinculo_ativo_chave)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE tur_grupos_horario (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  nome            VARCHAR(100) NOT NULL,
  turno           ENUM('manha','tarde','noite','integral','ead') NOT NULL,
  deleted_at      DATETIME(3) NULL,
  deleted_by      CHAR(36) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE tur_grupo_blocos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  grupo_id        BIGINT UNSIGNED NOT NULL,
  numero          TINYINT UNSIGNED NOT NULL,
  inicio          TIME NOT NULL,
  fim             TIME NOT NULL,
  intervalo_min   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  CONSTRAINT fk_bloco_grupo FOREIGN KEY (grupo_id) REFERENCES tur_grupos_horario (id),
  CONSTRAINT ck_bloco_horas CHECK (fim > inicio),
  UNIQUE KEY ux_bloco_numero (grupo_id, numero)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE tur_grades_horario (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  periodo_id      BIGINT UNSIGNED NOT NULL,
  versao          INT UNSIGNED NOT NULL,
  estado          ENUM('rascunho','vigente','substituida') NOT NULL DEFAULT 'rascunho',
  publicado_por   CHAR(36) NULL,
  publicado_em    DATETIME(3) NULL,
  UNIQUE KEY ux_grade_horario_versao (unidade_uuid, periodo_id, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE tur_aulas (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  grade_horario_id  BIGINT UNSIGNED NOT NULL,
  turma_id          BIGINT UNSIGNED NOT NULL,
  disciplina_id     BIGINT UNSIGNED NOT NULL,
  professor_uuid    CHAR(36) NOT NULL,
  bloco_id          BIGINT UNSIGNED NOT NULL,
  dia_semana        TINYINT UNSIGNED NOT NULL,
  recurso_uuid      CHAR(36) NULL,
  tipo              ENUM('presencial','online','hibrida','ead') NOT NULL,
  CONSTRAINT fk_aula_grade FOREIGN KEY (grade_horario_id) REFERENCES tur_grades_horario (id),
  CONSTRAINT fk_aula_turma FOREIGN KEY (turma_id) REFERENCES tur_turmas (id),
  CONSTRAINT fk_aula_bloco FOREIGN KEY (bloco_id) REFERENCES tur_grupo_blocos (id),
  CONSTRAINT ck_aula_dia CHECK (dia_semana BETWEEN 1 AND 7),
  UNIQUE KEY ux_aula_turma (grade_horario_id, turma_id, bloco_id, dia_semana),
  UNIQUE KEY ux_aula_professor (grade_horario_id, professor_uuid, bloco_id, dia_semana),
  UNIQUE KEY ux_aula_recurso (grade_horario_id, recurso_uuid, bloco_id, dia_semana)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE tur_substituicoes (
  id                        BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                      CHAR(36) NOT NULL UNIQUE,
  unidade_uuid              CHAR(36) NOT NULL,
  aula_id                   BIGINT UNSIGNED NOT NULL,
  professor_original_uuid   CHAR(36) NOT NULL,
  professor_substituto_uuid CHAR(36) NOT NULL,
  data                      DATE NOT NULL,
  motivo                    VARCHAR(500) NOT NULL,
  registrado_por            CHAR(36) NOT NULL,
  CONSTRAINT fk_subst_aula FOREIGN KEY (aula_id) REFERENCES tur_aulas (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Conflito de sala, professor e turma é impedido pelas chaves `ux_aula_*` com a grade de uma mesma versão ([60](60-turmas-e-grade-de-horarios-por-portal.md), seção 4.2). Sala `NULL` não conflita, por regra do MySQL: aula online sem sala ([60](60-turmas-e-grade-de-horarios-por-portal.md), seção 4.2).

### 15.5 Diário (DIA-08)

```sql
CREATE TABLE dia_aulas (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  aula_grade_id     BIGINT UNSIGNED NULL,
  turma_id          BIGINT UNSIGNED NOT NULL,
  disciplina_id     BIGINT UNSIGNED NOT NULL,
  professor_uuid    CHAR(36) NOT NULL,
  data              DATE NOT NULL,
  bloco_id          BIGINT UNSIGNED NOT NULL,
  estado            ENUM('planejada','realizada','cancelada','reposicao') NOT NULL,
  conteudo          TEXT NULL,
  motivo_cancelamento VARCHAR(500) NULL,
  plano_aula_id     BIGINT UNSIGNED NULL,
  CONSTRAINT fk_dia_aula_grade FOREIGN KEY (aula_grade_id) REFERENCES tur_aulas (id),
  CONSTRAINT ck_dia_aula_cancelada CHECK (estado <> 'cancelada' OR motivo_cancelamento IS NOT NULL),
  UNIQUE KEY ux_dia_aula (turma_id, disciplina_id, data, bloco_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dia_chamadas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  aula_id         BIGINT UNSIGNED NOT NULL,
  forma           ENUM('manual','qrcode','sala_online') NOT NULL,
  iniciada_em     DATETIME(3) NOT NULL,
  encerrada_em    DATETIME(3) NULL,
  prazo_correcao  DATETIME(3) NOT NULL,
  criada_por      CHAR(36) NOT NULL,
  CONSTRAINT fk_chamada_aula FOREIGN KEY (aula_id) REFERENCES dia_aulas (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dia_presencas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  chamada_id      BIGINT UNSIGNED NOT NULL,
  matricula_uuid  CHAR(36) NOT NULL,
  situacao        ENUM('presente','falta','justificada','pendente_qr') NOT NULL,
  CONSTRAINT fk_presenca_chamada FOREIGN KEY (chamada_id) REFERENCES dia_chamadas (id),
  UNIQUE KEY ux_presenca (chamada_id, matricula_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dia_justificativas (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  presenca_id       BIGINT UNSIGNED NOT NULL,
  tipo_codigo       VARCHAR(40) NOT NULL,
  prazo_ate         DATE NOT NULL,
  anexo_hash        CHAR(64) NULL,
  enviado_por       CHAR(36) NOT NULL,
  estado            ENUM('enviada','aprovada','recusada') NOT NULL,
  decidido_por      CHAR(36) NULL,
  decidido_em       DATETIME(3) NULL,
  motivo_recusa     VARCHAR(500) NULL,
  CONSTRAINT fk_just_presenca FOREIGN KEY (presenca_id) REFERENCES dia_presencas (id),
  CONSTRAINT ck_just_aprovacao CHECK (decidido_por IS NULL OR decidido_por <> enviado_por),
  CONSTRAINT ck_just_recusa CHECK (estado <> 'recusada' OR motivo_recusa IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dia_avaliacoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  turma_id        BIGINT UNSIGNED NOT NULL,
  disciplina_id   BIGINT UNSIGNED NOT NULL,
  periodo_id      BIGINT UNSIGNED NOT NULL,
  tipo            ENUM('prova','trabalho','seminario','pratica','autoavaliacao','recuperacao') NOT NULL,
  nome            VARCHAR(200) NOT NULL,
  peso_pct        DECIMAL(5,2) NOT NULL,
  data            DATE NULL,
  CONSTRAINT ck_avaliacao_peso CHECK (peso_pct BETWEEN 0 AND 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dia_notas_versoes (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid        CHAR(36) NOT NULL,
  avaliacao_id        BIGINT UNSIGNED NOT NULL,
  matricula_uuid      CHAR(36) NOT NULL,
  versao              INT UNSIGNED NOT NULL,
  valor               DECIMAL(6,2) NULL,
  lancado_por         CHAR(36) NOT NULL,
  lancado_em          DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  motivo_retificacao  VARCHAR(500) NULL,
  CONSTRAINT fk_nota_avaliacao FOREIGN KEY (avaliacao_id) REFERENCES dia_avaliacoes (id),
  CONSTRAINT ck_nota_retificacao CHECK (versao = 1 OR motivo_retificacao IS NOT NULL),
  UNIQUE KEY ux_nota_versao (avaliacao_id, matricula_uuid, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dia_fechamentos (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                    CHAR(36) NOT NULL UNIQUE,
  unidade_uuid            CHAR(36) NOT NULL,
  turma_id                BIGINT UNSIGNED NOT NULL,
  disciplina_id           BIGINT UNSIGNED NOT NULL,
  periodo_id              BIGINT UNSIGNED NOT NULL,
  estado                  ENUM('aberto','fechado','reaberto') NOT NULL DEFAULT 'aberto',
  pendencias              INT UNSIGNED NOT NULL DEFAULT 0,
  fechado_por             CHAR(36) NULL,
  fechado_em              DATETIME(3) NULL,
  justificativa_reabertura VARCHAR(500) NULL,
  autorizado_por          CHAR(36) NULL,
  CONSTRAINT ck_fechamento_reabertura CHECK (estado <> 'reaberto' OR (justificativa_reabertura IS NOT NULL AND autorizado_por IS NOT NULL)),
  UNIQUE KEY ux_fechamento (turma_id, disciplina_id, periodo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Nota corrigida é nova linha em `dia_notas_versoes`. A nota atual é a de maior `versao`. Período fechado não aceita linha nova em aula, chamada ou nota: regra de aplicação, com verificação de `dia_fechamentos` ([61](61-diario-escolar-por-portal.md), seções 5 e 6).

### 15.6 Boletim, recuperação e conselho (BOL-10)

```sql
CREATE TABLE bol_resultados (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  matricula_uuid    CHAR(36) NOT NULL,
  periodo_id        BIGINT UNSIGNED NOT NULL,
  disciplina_id     BIGINT UNSIGNED NULL,
  sistema_id        BIGINT UNSIGNED NOT NULL,
  media             DECIMAL(6,2) NULL,
  frequencia_pct    DECIMAL(5,2) NULL,
  situacao          ENUM('aprovado','recuperacao','reprovado_nota','reprovado_frequencia','aprovado_conselho','em_andamento','transferido','trancado') NOT NULL,
  versao            INT UNSIGNED NOT NULL,
  decidido_por      CHAR(36) NULL,
  justificativa     VARCHAR(1000) NULL,
  CONSTRAINT fk_resultado_sistema FOREIGN KEY (sistema_id) REFERENCES est_sistemas_avaliativos (id),
  CONSTRAINT ck_resultado_conselho CHECK (situacao <> 'aprovado_conselho' OR justificativa IS NOT NULL),
  UNIQUE KEY ux_resultado_versao (matricula_uuid, periodo_id, disciplina_id, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE bol_recuperacoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  resultado_id    BIGINT UNSIGNED NOT NULL,
  nota            DECIMAL(6,2) NOT NULL,
  data            DATE NOT NULL,
  efeito          ENUM('substitui','compoe') NOT NULL,
  registrada_por  CHAR(36) NOT NULL,
  CONSTRAINT fk_recuperacao_resultado FOREIGN KEY (resultado_id) REFERENCES bol_resultados (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE bol_conselhos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  turma_id        BIGINT UNSIGNED NOT NULL,
  periodo_id      BIGINT UNSIGNED NOT NULL,
  data_reuniao    DATETIME(3) NOT NULL,
  convocado_por   CHAR(36) NOT NULL,
  presidente_uuid CHAR(36) NOT NULL,
  secretario_uuid CHAR(36) NOT NULL,
  quorum_ok       TINYINT(1) NOT NULL DEFAULT 0,
  estado          ENUM('convocado','realizado','ata_assinada') NOT NULL DEFAULT 'convocado',
  UNIQUE KEY ux_conselho (turma_id, periodo_id, data_reuniao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE bol_conselho_pauta (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  conselho_id       BIGINT UNSIGNED NOT NULL,
  matricula_uuid    CHAR(36) NOT NULL,
  motivo            ENUM('media','frequencia','recuperacao','ocorrencia','outro') NOT NULL,
  incluido_por      CHAR(36) NOT NULL,
  retirado_motivo   VARCHAR(500) NULL,
  CONSTRAINT fk_pauta_conselho FOREIGN KEY (conselho_id) REFERENCES bol_conselhos (id),
  UNIQUE KEY ux_pauta (conselho_id, matricula_uuid, motivo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE bol_conselho_decisoes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  conselho_id       BIGINT UNSIGNED NOT NULL,
  matricula_uuid    CHAR(36) NOT NULL,
  disciplina_id     BIGINT UNSIGNED NULL,
  situacao          ENUM('aprovado','recuperacao','reprovado_nota','reprovado_frequencia','aprovado_conselho') NOT NULL,
  justificativa     VARCHAR(1000) NULL,
  decidido_por      CHAR(36) NOT NULL,
  decidido_em       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_decisao_conselho FOREIGN KEY (conselho_id) REFERENCES bol_conselhos (id),
  CONSTRAINT ck_decisao_justificativa CHECK (situacao <> 'aprovado_conselho' OR justificativa IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE bol_atas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  conselho_id     BIGINT UNSIGNED NOT NULL UNIQUE,
  numero          VARCHAR(30) NULL,
  texto_hash      CHAR(64) NOT NULL,
  estado          ENUM('rascunho','em_assinatura','assinada') NOT NULL DEFAULT 'rascunho',
  assinada_em     DATETIME(3) NULL,
  storage_path    VARCHAR(500) NULL,
  CONSTRAINT fk_ata_conselho FOREIGN KEY (conselho_id) REFERENCES bol_conselhos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Ata sem assinatura não gera resultado final ([62](62-boletim-e-conselho-de-classe-por-portal.md), seção 5.4). O texto da ata fica no armazenamento, e a tabela guarda só o hash. Dado sensível não entra na ata ([63](63-ocorrencias-disciplinares-por-portal.md), seção 6).

### 15.7 Índice dos módulos restantes

| Módulo | Código | Tabelas previstas | Situação |
|---|---|---|---|
| Ocorrências | OCO-09 | oco_ocorrencias, oco_versoes_relato, oco_envolvidos, oco_movimentacoes, oco_medidas, oco_comunicacoes, oco_contestacoes, oco_acessos_relato | Escrito, seções 15.8 a 15.17 |
| Planos | PLA-07 | pla_planos_ensino, pla_unidades, pla_avaliacoes_previstas, pla_planos_aula, pla_revisoes, pla_pendencias_planejamento | Escrito, seções 15.8 a 15.17 |
| Estágio e TCC | ETC-09 | etc_estagios, etc_termos, etc_estagio_horas, etc_estagio_relatorios, etc_estagio_avaliacoes, etc_tcc, etc_tcc_versoes, etc_repositorio, etc_bancas, etc_banca_membros, etc_banca_avaliacoes | Escrito, seções 15.8 a 15.17 |
| Prontuário e portfólio | PRT-06 | prt_secoes_saude, prt_acessos_saude, prt_documentos_vinculo, prt_portfolios, prt_evidencias, prt_avaliacoes, prt_exportacoes | Escrito, seções 15.8 a 15.17 |
| Arquivo e livros | ARQ-07 | arq_livros, arq_sequencias, arq_registros, arq_retificacoes, arq_atas, arq_ata_assinaturas, arq_itens_fisicos, arq_digitalizacoes, arq_emprestimos_fisicos, arq_eliminacoes | Escrito, seções 15.8 a 15.17 |
| Biblioteca | BIB-08 | lib_itens, lib_exemplares, lib_emprestimos, lib_reservas, lib_multas, lib_digital_licencas | Escrito, seção 15.13. Substitui os `lib_*` da v1 |
| Relatórios | REL-07 | rel_modelos, rel_pedidos, rel_arquivos, rel_agendamentos, rel_envios_regulatorios | Escrito, seções 15.8 a 15.17 |
| Importação | IMP-06 | imp_lotes, imp_linhas, imp_erros, imp_mapeamentos | Escrito, seções 15.8 a 15.17 |
| Financeiro | FIN-08 | fin_contas, fin_linhas_dre, fin_categorias, fin_centros_custo, fin_movimentacoes, fin_despesas, fin_rateios, fin_pagamentos, fin_cheques, fin_caixas, fin_fechamentos_caixa, fin_orcamentos, fin_orcamento_linhas | Escrito, seções 15.8 a 15.17 |
| Campos personalizados | CPF-04 | cpf_definicoes, cpf_opcoes, cpf_valores | Escrito, seções 15.8 a 15.17 |
| Meu perfil | PER-07 | per_pedidos_alteracao, per_historico | Escrito, seção 15.18 ([76](76-meu-perfil-por-portal.md)). Revisão do owner pendente |
| Simulados e redação | SIM-07 | sim_perfis, sim_rubrica_itens, sim_questoes, sim_alternativas, sim_simulados, sim_simulado_questoes, sim_respostas_objetivas, sim_redacoes, sim_redacao_paginas, sim_correcoes, sim_correcao_competencias, sim_redacao_eventos, sim_trilhas_reforco | Escrito, seção 15.19 ([47](47-simulados-por-portal.md)). Revisão do owner pendente |
| Integrações educacionais | INT-07 | int_conexoes, int_lotes, int_itens, int_rejeicoes, int_reconciliacoes | Escrito, seção 15.20 ([74](74-integracoes-educacionais-oficiais.md)). Revisão do owner pendente |

### 15.8 Ocorrências (OCO-09)

> Ocorrência não é excluída: sai de cena por `arquivada`, com motivo em `oco_movimentacoes`. O relato é cifrado na aplicação ([63](63-ocorrencias-disciplinares-por-portal.md), seção 6.4).

```sql
CREATE TABLE oco_ocorrencias (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid       CHAR(36) NOT NULL,
  tipo                ENUM('convivencia','conduta_aula','seguranca','integridade_academica','meio_digital','outro') NOT NULL,
  gravidade           ENUM('leve','media','grave','gravissima') NOT NULL,
  data_fato           DATETIME(3) NOT NULL,
  local_recurso_uuid  CHAR(36) NULL,
  registrada_por      CHAR(36) NOT NULL,
  estado              ENUM('registrada','em_analise','comunicada','com_medida','encerrada','arquivada') NOT NULL,
  violencia_protocolo TINYINT(1) NOT NULL DEFAULT 0,
  created_at          DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT ck_oco_violencia CHECK (violencia_protocolo = 0 OR tipo = 'outro'),
  INDEX ix_oco_unidade (unidade_uuid, estado, data_fato)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE oco_versoes_relato (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  ocorrencia_id   BIGINT UNSIGNED NOT NULL,
  versao          INT UNSIGNED NOT NULL,
  relato_cifrado  VARBINARY(8000) NOT NULL,
  alterado_por    CHAR(36) NOT NULL,
  alterado_em     DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  motivo          VARCHAR(500) NULL,
  CONSTRAINT fk_relato_oco FOREIGN KEY (ocorrencia_id) REFERENCES oco_ocorrencias (id),
  CONSTRAINT ck_relato_motivo CHECK (versao = 1 OR motivo IS NOT NULL),
  UNIQUE KEY ux_relato_versao (ocorrencia_id, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE oco_envolvidos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  ocorrencia_id   BIGINT UNSIGNED NOT NULL,
  matricula_uuid  CHAR(36) NULL,
  pessoa_uuid     CHAR(36) NULL,
  papel           ENUM('autor','vitima','testemunha','outro') NOT NULL,
  CONSTRAINT fk_envolvido_oco FOREIGN KEY (ocorrencia_id) REFERENCES oco_ocorrencias (id),
  CONSTRAINT ck_envolvido_pessoa CHECK (matricula_uuid IS NOT NULL OR pessoa_uuid IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE oco_movimentacoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  ocorrencia_id   BIGINT UNSIGNED NOT NULL,
  estado_anterior VARCHAR(30) NULL,
  estado_novo     VARCHAR(30) NOT NULL,
  ator_uuid       CHAR(36) NOT NULL,
  motivo          VARCHAR(500) NULL,
  criado_em       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_mov_oco FOREIGN KEY (ocorrencia_id) REFERENCES oco_ocorrencias (id),
  CONSTRAINT ck_mov_arquivada CHECK (estado_novo <> 'arquivada' OR motivo IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE oco_medidas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  ocorrencia_id   BIGINT UNSIGNED NOT NULL,
  tipo            ENUM('orientacao','conversa_responsavel','plano_convivencia','reparacao','acompanhamento','afastamento') NOT NULL,
  responsavel_uuid CHAR(36) NOT NULL,
  decidido_por    CHAR(36) NOT NULL,
  prazo           DATE NULL,
  resultado       VARCHAR(500) NULL,
  CONSTRAINT fk_medida_oco FOREIGN KEY (ocorrencia_id) REFERENCES oco_ocorrencias (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE oco_comunicacoes (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  ocorrencia_id       BIGINT UNSIGNED NOT NULL,
  destinatario_uuid   CHAR(36) NOT NULL,
  canal               ENUM('app','email','sms','whatsapp') NOT NULL,
  enviada_em          DATETIME(3) NOT NULL,
  notificacao_uuid    CHAR(36) NULL,
  CONSTRAINT fk_com_oco FOREIGN KEY (ocorrencia_id) REFERENCES oco_ocorrencias (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE oco_contestacoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  ocorrencia_id   BIGINT UNSIGNED NOT NULL,
  protocolo_uuid  CHAR(36) NOT NULL,
  prazo_ate       DATE NOT NULL,
  recebida_em     DATETIME(3) NOT NULL,
  decisao         ENUM('pendente','acolhida','mantida') NOT NULL DEFAULT 'pendente',
  resposta        VARCHAR(1000) NULL,
  respondida_por  CHAR(36) NULL,
  CONSTRAINT fk_contest_oco FOREIGN KEY (ocorrencia_id) REFERENCES oco_ocorrencias (id),
  CONSTRAINT ck_contest_resposta CHECK (decisao = 'pendente' OR respondida_por IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE oco_acessos_relato (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  ocorrencia_id   BIGINT UNSIGNED NOT NULL,
  acessado_por    CHAR(36) NOT NULL,
  motivo          VARCHAR(500) NOT NULL,
  acessado_em     DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_acesso_oco FOREIGN KEY (ocorrencia_id) REFERENCES oco_ocorrencias (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 15.9 Planos de ensino e de aula (PLA-07)

```sql
CREATE TABLE pla_planos_ensino (
  id                        BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                      CHAR(36) NOT NULL UNIQUE,
  unidade_uuid              CHAR(36) NOT NULL,
  disciplina_id             BIGINT UNSIGNED NOT NULL,
  turma_id                  BIGINT UNSIGNED NOT NULL,
  periodo_id                BIGINT UNSIGNED NOT NULL,
  professor_uuid            CHAR(36) NOT NULL,
  versao                    INT UNSIGNED NOT NULL,
  estado                    ENUM('rascunho','enviado','aprovado','devolvido') NOT NULL DEFAULT 'rascunho',
  objetivos                 TEXT NULL,
  metodologia               TEXT NULL,
  bibliografia_basica       TEXT NULL,
  bibliografia_complementar TEXT NULL,
  aprovado_por              CHAR(36) NULL,
  aprovado_em               DATETIME(3) NULL,
  CONSTRAINT fk_plano_disc FOREIGN KEY (disciplina_id) REFERENCES est_disciplinas (id),
  CONSTRAINT fk_plano_turma FOREIGN KEY (turma_id) REFERENCES tur_turmas (id),
  CONSTRAINT fk_plano_periodo FOREIGN KEY (periodo_id) REFERENCES cal_periodos (id),
  CONSTRAINT ck_plano_aprovacao CHECK (aprovado_por IS NULL OR aprovado_por <> professor_uuid),
  UNIQUE KEY ux_plano_versao (turma_id, disciplina_id, periodo_id, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pla_unidades (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  plano_id          BIGINT UNSIGNED NOT NULL,
  numero            TINYINT UNSIGNED NOT NULL,
  titulo            VARCHAR(200) NOT NULL,
  carga_prevista_h  DECIMAL(6,2) NOT NULL,
  aulas_previstas   SMALLINT UNSIGNED NOT NULL,
  CONSTRAINT fk_unid_plano FOREIGN KEY (plano_id) REFERENCES pla_planos_ensino (id),
  UNIQUE KEY ux_unidade_numero (plano_id, numero)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pla_avaliacoes_previstas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  plano_id        BIGINT UNSIGNED NOT NULL,
  tipo            ENUM('prova','trabalho','seminario','pratica','autoavaliacao','recuperacao') NOT NULL,
  peso_pct        DECIMAL(5,2) NOT NULL,
  data_prevista   DATE NULL,
  CONSTRAINT fk_avaliacao_plano FOREIGN KEY (plano_id) REFERENCES pla_planos_ensino (id),
  CONSTRAINT ck_avaliacao_peso CHECK (peso_pct BETWEEN 0 AND 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pla_planos_aula (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                    CHAR(36) NOT NULL UNIQUE,
  unidade_uuid            CHAR(36) NOT NULL,
  plano_ensino_id         BIGINT UNSIGNED NOT NULL,
  unidade_plano_id        BIGINT UNSIGNED NULL,
  dia_aula_id             BIGINT UNSIGNED NULL,
  data_prevista           DATE NOT NULL,
  objetivos               TEXT NULL,
  conteudo                TEXT NULL,
  metodologia             TEXT NULL,
  recursos                JSON NULL,
  estado                  ENUM('rascunho','enviado','aprovado','devolvido') NOT NULL DEFAULT 'rascunho',
  gerado_por_ia           TINYINT(1) NOT NULL DEFAULT 0,
  revisado_pelo_professor TINYINT(1) NOT NULL DEFAULT 0,
  enviado_em              DATETIME(3) NULL,
  aprovado_por            CHAR(36) NULL,
  CONSTRAINT fk_plano_aula_ensino FOREIGN KEY (plano_ensino_id) REFERENCES pla_planos_ensino (id),
  CONSTRAINT fk_plano_aula_unidade FOREIGN KEY (unidade_plano_id) REFERENCES pla_unidades (id),
  CONSTRAINT fk_plano_aula_dia FOREIGN KEY (dia_aula_id) REFERENCES dia_aulas (id),
  CONSTRAINT ck_plano_aula_ia CHECK (gerado_por_ia = 0 OR revisado_pelo_professor = 1 OR estado = 'rascunho'),
  INDEX ix_plano_aula_fila (unidade_uuid, estado, data_prevista)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pla_revisoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  plano_aula_id   BIGINT UNSIGNED NOT NULL,
  estado_anterior VARCHAR(20) NULL,
  estado_novo     VARCHAR(20) NOT NULL,
  ator_uuid       CHAR(36) NOT NULL,
  comentario      VARCHAR(1000) NULL,
  criado_em       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_revisao_aula FOREIGN KEY (plano_aula_id) REFERENCES pla_planos_aula (id),
  CONSTRAINT ck_revisao_devolucao CHECK (estado_novo <> 'devolvido' OR comentario IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pla_pendencias_planejamento (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  unidade_uuid    CHAR(36) NOT NULL,
  turma_id        BIGINT UNSIGNED NOT NULL,
  disciplina_id   BIGINT UNSIGNED NOT NULL,
  data_aula       DATE NOT NULL,
  motivo          ENUM('sem_plano_aprovado','conteudo_nao_ministrado') NOT NULL,
  criado_em       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  resolvido_em    DATETIME(3) NULL,
  INDEX ix_pendencia_turma (unidade_uuid, turma_id, resolvido_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Aula sem plano aprovado não é bloqueada: gera linha em `pla_pendencias_planejamento` ([64](64-planos-de-aula-e-de-ensino-por-portal.md), seção 4.2). Conteúdo não ministrado vira pendência, sem reagendamento automático (PLA-06).

### 15.10 Estágio e TCC (ETC-09)

```sql
CREATE TABLE etc_estagios (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                  CHAR(36) NOT NULL UNIQUE,
  unidade_uuid          CHAR(36) NOT NULL,
  matricula_uuid        CHAR(36) NOT NULL,
  curso_id              BIGINT UNSIGNED NOT NULL,
  disciplina_id         BIGINT UNSIGNED NULL,
  tipo                  ENUM('obrigatorio','nao_obrigatorio') NOT NULL,
  concedente_cnpj       CHAR(14) NOT NULL,
  concedente_nome       VARCHAR(200) NOT NULL,
  convenio_contrato_uuid CHAR(36) NULL,
  orientador_uuid       CHAR(36) NOT NULL,
  supervisor_pessoa_uuid CHAR(36) NULL,
  inicio                DATE NOT NULL,
  fim_previsto          DATE NOT NULL,
  fim_real              DATE NULL,
  carga_semanal_h       TINYINT UNSIGNED NOT NULL,
  carga_total_h         INT UNSIGNED NOT NULL,
  apolice_hash          CHAR(64) NULL,
  apolice_validade      DATE NULL,
  estado                ENUM('solicitado','ativo','concluido','interrompido','cancelado') NOT NULL,
  resultado             ENUM('aprovado','reprovado') NULL,
  motivo_interrupcao    VARCHAR(500) NULL,
  CONSTRAINT fk_estagio_curso FOREIGN KEY (curso_id) REFERENCES est_cursos (id),
  CONSTRAINT ck_estagio_datas CHECK (fim_previsto >= inicio),
  CONSTRAINT ck_estagio_interrupcao CHECK (estado <> 'interrompido' OR motivo_interrupcao IS NOT NULL),
  CONSTRAINT ck_estagio_resultado CHECK (estado <> 'concluido' OR resultado IS NOT NULL),
  CONSTRAINT ck_estagio_orientador CHECK (supervisor_pessoa_uuid IS NULL OR supervisor_pessoa_uuid <> orientador_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE etc_termos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  estagio_id      BIGINT UNSIGNED NOT NULL,
  versao          INT UNSIGNED NOT NULL,
  arquivo_hash    CHAR(64) NOT NULL,
  partes_assinadas TINYINT UNSIGNED NOT NULL DEFAULT 0,
  CONSTRAINT fk_termo_estagio FOREIGN KEY (estagio_id) REFERENCES etc_estagios (id),
  CONSTRAINT ck_termo_partes CHECK (partes_assinadas BETWEEN 0 AND 3),
  UNIQUE KEY ux_termo_versao (estagio_id, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE etc_estagio_horas (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  estagio_id              BIGINT UNSIGNED NOT NULL,
  mes                     CHAR(7) NOT NULL,
  horas_previstas         DECIMAL(6,2) NOT NULL,
  horas_cumpridas         DECIMAL(6,2) NOT NULL DEFAULT 0,
  confirmada_supervisor   TINYINT(1) NOT NULL DEFAULT 0,
  CONSTRAINT fk_horas_estagio FOREIGN KEY (estagio_id) REFERENCES etc_estagios (id),
  CONSTRAINT ck_horas_nao_negativas CHECK (horas_cumpridas >= 0),
  UNIQUE KEY ux_horas_mes (estagio_id, mes)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE etc_estagio_relatorios (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  estagio_id      BIGINT UNSIGNED NOT NULL,
  periodo_ref     CHAR(7) NOT NULL,
  arquivo_hash    CHAR(64) NOT NULL,
  descricao       TEXT NULL,
  enviado_em      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  avaliado_por    CHAR(36) NULL,
  CONSTRAINT fk_relatorio_estagio FOREIGN KEY (estagio_id) REFERENCES etc_estagios (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE etc_estagio_avaliacoes (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  estagio_id              BIGINT UNSIGNED NOT NULL,
  avaliador_tipo          ENUM('supervisor_empresa','orientador') NOT NULL,
  avaliador_uuid          CHAR(36) NOT NULL,
  nota                    DECIMAL(6,2) NOT NULL,
  formulario_resposta_uuid CHAR(36) NULL,
  CONSTRAINT fk_avaliacao_estagio FOREIGN KEY (estagio_id) REFERENCES etc_estagios (id),
  UNIQUE KEY ux_avaliacao_tipo (estagio_id, avaliador_tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE etc_tcc (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid        CHAR(36) NOT NULL,
  matricula_uuid      CHAR(36) NOT NULL,
  curso_id            BIGINT UNSIGNED NOT NULL,
  tipo                ENUM('tcc','monografia','projeto_final','artigo') NOT NULL,
  titulo              VARCHAR(300) NOT NULL,
  linha_pesquisa      VARCHAR(120) NULL,
  orientador_uuid     CHAR(36) NOT NULL,
  coorientador_uuid   CHAR(36) NULL,
  inicio              DATE NOT NULL,
  entrega_prevista    DATE NOT NULL,
  estado              ENUM('em_orientacao','submetido','em_banca','reformulacao','aprovado','aprovado_com_ressalvas','reprovado') NOT NULL,
  prorrogacao_ate     DATE NULL,
  prorrogacao_motivo  VARCHAR(500) NULL,
  termo_hash          CHAR(64) NULL,
  CONSTRAINT fk_tcc_curso FOREIGN KEY (curso_id) REFERENCES est_cursos (id),
  CONSTRAINT ck_tcc_coorientador CHECK (coorientador_uuid IS NULL OR coorientador_uuid <> orientador_uuid),
  CONSTRAINT ck_tcc_prorrogacao CHECK (prorrogacao_ate IS NULL OR prorrogacao_motivo IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE etc_tcc_versoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tcc_id          BIGINT UNSIGNED NOT NULL,
  versao          INT UNSIGNED NOT NULL,
  arquivo_hash    CHAR(64) NOT NULL,
  enviado_em      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_tcc_versao FOREIGN KEY (tcc_id) REFERENCES etc_tcc (id),
  UNIQUE KEY ux_tcc_versao (tcc_id, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE etc_repositorio (
  tcc_id              BIGINT UNSIGNED PRIMARY KEY,
  autorizacao_aluno   TINYINT(1) NOT NULL DEFAULT 0,
  acesso_publico      TINYINT(1) NOT NULL DEFAULT 0,
  CONSTRAINT fk_repo_tcc FOREIGN KEY (tcc_id) REFERENCES etc_tcc (id),
  CONSTRAINT ck_repo_publico CHECK (acesso_publico = 0 OR autorizacao_aluno = 1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE etc_bancas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tcc_id          BIGINT UNSIGNED NOT NULL UNIQUE,
  data_defesa     DATETIME(3) NOT NULL,
  local_recurso_uuid CHAR(36) NULL,
  link_sala       VARCHAR(500) NULL,
  peso_orientador DECIMAL(5,2) NOT NULL,
  peso_membros    DECIMAL(5,2) NOT NULL,
  nota_final      DECIMAL(6,2) NULL,
  resultado       ENUM('aprovado','aprovado_com_ressalvas','reprovado') NULL,
  ata_hash        CHAR(64) NULL,
  CONSTRAINT fk_banca_tcc FOREIGN KEY (tcc_id) REFERENCES etc_tcc (id),
  CONSTRAINT ck_banca_pesos CHECK (peso_orientador >= 0 AND peso_membros >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE etc_banca_membros (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  banca_id        BIGINT UNSIGNED NOT NULL,
  pessoa_uuid     CHAR(36) NOT NULL,
  papel           ENUM('orientador','membro_interno','membro_externo') NOT NULL,
  instituicao     VARCHAR(200) NULL,
  titulacao       VARCHAR(100) NULL,
  CONSTRAINT fk_membro_banca FOREIGN KEY (banca_id) REFERENCES etc_bancas (id),
  CONSTRAINT ck_membro_externo CHECK (papel <> 'membro_externo' OR instituicao IS NOT NULL),
  UNIQUE KEY ux_membro (banca_id, pessoa_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE etc_banca_avaliacoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  banca_id        BIGINT UNSIGNED NOT NULL,
  membro_id       BIGINT UNSIGNED NOT NULL,
  nota            DECIMAL(6,2) NOT NULL,
  parecer         VARCHAR(2000) NULL,
  lancado_em      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_avaliacao_banca FOREIGN KEY (banca_id) REFERENCES etc_bancas (id),
  CONSTRAINT fk_avaliacao_membro FOREIGN KEY (membro_id) REFERENCES etc_banca_membros (id),
  UNIQUE KEY ux_avaliacao_membro (banca_id, membro_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Estágio `ativo` só com `etc_termos.partes_assinadas = 3` e apólice válida, checado na aplicação ([65](65-estagio-e-tcc-por-portal.md), seção 2.3). Nota da banca só aparece quando todos os membros lançaram: regra de leitura, na aplicação.

### 15.11 Prontuário e portfólio (PRT-06)

```sql
CREATE TABLE prt_secoes_saude (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  matricula_uuid  CHAR(36) NOT NULL,
  tipo            ENUM('laudo_necessidade','plano_apoio','restricao_alimentar','medicamento','atendimento_enfermaria') NOT NULL,
  cid_cifrado     VARBINARY(255) NULL,
  descricao_cifrada VARBINARY(8000) NOT NULL,
  documento_uuid  CHAR(36) NULL,
  validade        DATE NULL,
  registrado_por  CHAR(36) NOT NULL,
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at      DATETIME(3) NULL,
  deleted_by      CHAR(36) NULL,
  CONSTRAINT ck_saude_medicamento CHECK (tipo <> 'medicamento' OR documento_uuid IS NOT NULL),
  INDEX ix_saude_aluno (unidade_uuid, matricula_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE prt_acessos_saude (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  secao_id        BIGINT UNSIGNED NOT NULL,
  acessado_por    CHAR(36) NOT NULL,
  motivo          VARCHAR(500) NOT NULL,
  acessado_em     DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_acesso_saude FOREIGN KEY (secao_id) REFERENCES prt_secoes_saude (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE prt_documentos_vinculo (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  unidade_uuid    CHAR(36) NOT NULL,
  matricula_uuid  CHAR(36) NOT NULL,
  documento_uuid  CHAR(36) NOT NULL UNIQUE,
  contexto        ENUM('A','B','C') NOT NULL,
  tipo_codigo     VARCHAR(60) NOT NULL,
  validade        DATE NULL,
  INDEX ix_vinculo_aluno (unidade_uuid, matricula_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE prt_portfolios (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                    CHAR(36) NOT NULL UNIQUE,
  unidade_uuid            CHAR(36) NOT NULL,
  matricula_uuid          CHAR(36) NOT NULL,
  disciplina_id           BIGINT UNSIGNED NOT NULL,
  periodo_id              BIGINT UNSIGNED NOT NULL,
  estado                  ENUM('rascunho','publicado','avaliado') NOT NULL DEFAULT 'rascunho',
  compartilhado_responsavel TINYINT(1) NOT NULL DEFAULT 0,
  CONSTRAINT fk_portfolio_disc FOREIGN KEY (disciplina_id) REFERENCES est_disciplinas (id),
  CONSTRAINT fk_portfolio_periodo FOREIGN KEY (periodo_id) REFERENCES cal_periodos (id),
  UNIQUE KEY ux_portfolio (matricula_uuid, disciplina_id, periodo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE prt_evidencias (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                    CHAR(36) NOT NULL UNIQUE,
  unidade_uuid            CHAR(36) NOT NULL,
  portfolio_id            BIGINT UNSIGNED NOT NULL,
  tipo                    ENUM('texto','imagem','arquivo','link','video') NOT NULL,
  conteudo_ref            VARCHAR(500) NULL,
  hash                    CHAR(64) NULL,
  dado_terceiro_verificado TINYINT(1) NOT NULL DEFAULT 0,
  publicado_em            DATETIME(3) NULL,
  CONSTRAINT fk_evidencia_portfolio FOREIGN KEY (portfolio_id) REFERENCES prt_portfolios (id),
  CONSTRAINT ck_evidencia_publicada CHECK (publicado_em IS NULL OR tipo <> 'imagem' OR dado_terceiro_verificado = 1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE prt_avaliacoes (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  portfolio_id        BIGINT UNSIGNED NOT NULL UNIQUE,
  professor_uuid      CHAR(36) NOT NULL,
  comentario          TEXT NULL,
  nota_qualitativa    ENUM('insuficiente','regular','bom','excelente') NOT NULL,
  publicado_em        DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_avaliacao_portfolio FOREIGN KEY (portfolio_id) REFERENCES prt_portfolios (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE prt_exportacoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  portfolio_id    BIGINT UNSIGNED NOT NULL,
  exportado_por   CHAR(36) NOT NULL,
  exportado_em    DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  arquivo_hash    CHAR(64) NOT NULL,
  CONSTRAINT fk_export_portfolio FOREIGN KEY (portfolio_id) REFERENCES prt_portfolios (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`prt_documentos_vinculo` aponta o documento de [54](54-gestao-de-documentos-tres-contextos.md) pelo `uuid`, sem copiar o arquivo. Um documento tem uma origem só, por causa do `UNIQUE` em `documento_uuid` ([66](66-prontuario-e-portfolio-do-aluno-por-portal.md), seção 2.1). Imagem de terceiro só é publicada depois de verificada: regra de checagem na aplicação e constraint acima.

### 15.12 Arquivo e livros (ARQ-07)

```sql
CREATE TABLE arq_livros (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tipo            ENUM('registro','atas') NOT NULL,
  ano             SMALLINT UNSIGNED NOT NULL,
  estado          ENUM('aberto','publicado') NOT NULL DEFAULT 'aberto',
  publicado_por   CHAR(36) NULL,
  publicado_em    DATETIME(3) NULL,
  UNIQUE KEY ux_livro (unidade_uuid, tipo, ano),
  CONSTRAINT ck_livro_publicacao CHECK (estado <> 'publicado' OR publicado_por IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE arq_sequencias (
  unidade_uuid    CHAR(36) NOT NULL,
  tipo            ENUM('registro','atas') NOT NULL,
  ano             SMALLINT UNSIGNED NOT NULL,
  ultimo_numero   INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (unidade_uuid, tipo, ano)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE arq_registros (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  livro_id        BIGINT UNSIGNED NOT NULL,
  numero_ordem    INT UNSIGNED NOT NULL,
  matricula_uuid  CHAR(36) NOT NULL,
  nome_aluno      VARCHAR(200) NOT NULL,
  cpf_cifrado     VARBINARY(255) NULL,
  curso           VARCHAR(200) NOT NULL,
  serie           VARCHAR(60) NULL,
  data_matricula  DATE NOT NULL,
  situacao        VARCHAR(40) NOT NULL,
  hash            CHAR(64) NOT NULL,
  hash_anterior   CHAR(64) NULL,
  CONSTRAINT fk_registro_livro FOREIGN KEY (livro_id) REFERENCES arq_livros (id),
  UNIQUE KEY ux_registro_ordem (livro_id, numero_ordem)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE arq_retificacoes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  registro_id       BIGINT UNSIGNED NOT NULL,
  motivo            VARCHAR(500) NOT NULL,
  autor_uuid        CHAR(36) NOT NULL,
  criado_em         DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  hash_anterior     CHAR(64) NOT NULL,
  hash_novo         CHAR(64) NOT NULL,
  CONSTRAINT fk_retificacao_registro FOREIGN KEY (registro_id) REFERENCES arq_registros (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE arq_atas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  tipo_ata        ENUM('conselho','reuniao','assembleia') NOT NULL,
  conselho_id     BIGINT UNSIGNED NULL,
  numero          INT UNSIGNED NULL,
  data_criacao    DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  estado          ENUM('rascunho','em_assinatura','assinado','publicado') NOT NULL DEFAULT 'rascunho',
  texto_hash      CHAR(64) NOT NULL,
  retifica_ata_id BIGINT UNSIGNED NULL,
  CONSTRAINT fk_ata_retifica FOREIGN KEY (retifica_ata_id) REFERENCES arq_atas (id),
  CONSTRAINT ck_ata_numero CHECK (estado <> 'publicado' OR numero IS NOT NULL),
  UNIQUE KEY ux_ata_numero (unidade_uuid, tipo_ata, numero)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE arq_ata_assinaturas (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  ata_id            BIGINT UNSIGNED NOT NULL,
  pessoa_uuid       CHAR(36) NOT NULL,
  tipo_assinatura   ENUM('simples','icp_brasil') NOT NULL,
  assinado_em       DATETIME(3) NOT NULL,
  hash_assinatura   CHAR(64) NOT NULL,
  CONSTRAINT fk_assinatura_ata FOREIGN KEY (ata_id) REFERENCES arq_atas (id),
  UNIQUE KEY ux_assinatura (ata_id, pessoa_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE arq_itens_fisicos (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid        CHAR(36) NOT NULL,
  codigo_localizacao  VARCHAR(60) NOT NULL,
  caixa               VARCHAR(30) NULL,
  pasta               VARCHAR(30) NULL,
  prateleira          VARCHAR(30) NULL,
  tipo_documento      VARCHAR(60) NOT NULL,
  matricula_uuid      CHAR(36) NULL,
  ano_letivo          SMALLINT UNSIGNED NULL,
  situacao            ENUM('apenas_fisico','digitalizado','digitalizado_verificado') NOT NULL DEFAULT 'apenas_fisico',
  UNIQUE KEY ux_localizacao (unidade_uuid, codigo_localizacao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE arq_digitalizacoes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  item_id           BIGINT UNSIGNED NOT NULL,
  arquivo_hash      CHAR(64) NOT NULL,
  digitalizado_por  CHAR(36) NOT NULL,
  digitalizado_em   DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  verificado_por    CHAR(36) NULL,
  verificado_em     DATETIME(3) NULL,
  CONSTRAINT fk_digit_item FOREIGN KEY (item_id) REFERENCES arq_itens_fisicos (id),
  CONSTRAINT ck_digit_verificador CHECK (verificado_por IS NULL OR verificado_por <> digitalizado_por)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE arq_emprestimos_fisicos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  item_id         BIGINT UNSIGNED NOT NULL,
  retirado_por    CHAR(36) NOT NULL,
  retirado_em     DATETIME(3) NOT NULL,
  prazo           DATE NOT NULL,
  devolvido_em    DATETIME(3) NULL,
  CONSTRAINT fk_emprest_item FOREIGN KEY (item_id) REFERENCES arq_itens_fisicos (id),
  CONSTRAINT ck_emprest_datas CHECK (devolvido_em IS NULL OR devolvido_em >= retirado_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE arq_eliminacoes (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid        CHAR(36) NOT NULL,
  data_eliminacao     DATE NOT NULL,
  responsavel_uuid    CHAR(36) NOT NULL,
  lista_hash          CHAR(64) NOT NULL,
  prazo_guarda_ok     TINYINT(1) NOT NULL,
  CONSTRAINT ck_eliminacao_prazo CHECK (prazo_guarda_ok = 1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Número de ordem vem de `arq_sequencias` e nunca é reaproveitado ([67](67-livros-digitais-e-arquivo-morto-por-portal.md), seção 2.2). CPF no livro é cifrado (ARQ-01). Termo de eliminação guarda só o hash da lista, nunca o conteúdo (seção 4.4).

### 15.13 Biblioteca (BIB-08)

> Substitui as tabelas `lib_*` da v1, que usam `entity_id` e `unit_id`. Corrige T-01 ([68](68-biblioteca-por-portal.md), seção 13).

```sql
CREATE TABLE lib_itens (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid        CHAR(36) NOT NULL,
  titulo              VARCHAR(300) NOT NULL,
  autores             JSON NOT NULL,
  isbn                VARCHAR(20) NULL,
  issn                VARCHAR(20) NULL,
  editora             VARCHAR(150) NULL,
  edicao              VARCHAR(50) NULL,
  ano                 SMALLINT UNSIGNED NULL,
  idioma              CHAR(5) NOT NULL DEFAULT 'pt-BR',
  categoria           VARCHAR(80) NULL,
  sinopse             TEXT NULL,
  digital             TINYINT(1) NOT NULL DEFAULT 0,
  licencas_simultaneas INT UNSIGNED NULL,
  created_at          DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  deleted_at          DATETIME(3) NULL,
  deleted_by          CHAR(36) NULL,
  INDEX ix_lib_titulo (unidade_uuid, titulo(100))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_exemplares (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                    CHAR(36) NOT NULL UNIQUE,
  unidade_uuid            CHAR(36) NOT NULL,
  item_id                 BIGINT UNSIGNED NOT NULL,
  codigo_tombamento       VARCHAR(40) NOT NULL,
  codigo_barras           VARCHAR(50) NOT NULL,
  localizacao             VARCHAR(100) NULL,
  conservacao             ENUM('otimo','bom','danificado','perdido') NOT NULL DEFAULT 'bom',
  situacao                ENUM('disponivel','emprestado','reservado','em_manutencao','baixado') NOT NULL DEFAULT 'disponivel',
  valor_aquisicao_centavos BIGINT UNSIGNED NULL,
  pedido_compra_uuid      CHAR(36) NULL,
  CONSTRAINT fk_exemplar_item FOREIGN KEY (item_id) REFERENCES lib_itens (id),
  UNIQUE KEY ux_tombamento (unidade_uuid, codigo_tombamento),
  UNIQUE KEY ux_codigo_barras (unidade_uuid, codigo_barras)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_emprestimos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  exemplar_id     BIGINT UNSIGNED NOT NULL,
  pessoa_uuid     CHAR(36) NOT NULL,
  perfil          ENUM('aluno','professor','servidor') NOT NULL,
  retirado_em     DATETIME(3) NOT NULL,
  prazo           DATE NOT NULL,
  devolvido_em    DATETIME(3) NULL,
  renovacoes      TINYINT UNSIGNED NOT NULL DEFAULT 0,
  estado          ENUM('ativo','atrasado','devolvido','perdido') NOT NULL DEFAULT 'ativo',
  ativo_chave     BIGINT UNSIGNED AS (CASE WHEN devolvido_em IS NULL THEN exemplar_id END) STORED,
  CONSTRAINT fk_emprestimo_exemplar FOREIGN KEY (exemplar_id) REFERENCES lib_exemplares (id),
  UNIQUE KEY ux_emprestimo_ativo (ativo_chave)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_reservas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  item_id         BIGINT UNSIGNED NOT NULL,
  pessoa_uuid     CHAR(36) NOT NULL,
  posicao         SMALLINT UNSIGNED NOT NULL,
  estado          ENUM('aguardando','pronta','expirada','atendida','cancelada') NOT NULL DEFAULT 'aguardando',
  disponivel_ate  DATETIME(3) NULL,
  CONSTRAINT fk_reserva_item FOREIGN KEY (item_id) REFERENCES lib_itens (id),
  UNIQUE KEY ux_reserva_posicao (item_id, posicao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_multas (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                  CHAR(36) NOT NULL UNIQUE,
  unidade_uuid          CHAR(36) NOT NULL,
  emprestimo_id         BIGINT UNSIGNED NOT NULL,
  pessoa_uuid           CHAR(36) NOT NULL,
  dias_atraso           INT UNSIGNED NOT NULL,
  valor_centavos        BIGINT UNSIGNED NOT NULL,
  estado                ENUM('pendente','paga','isenta') NOT NULL DEFAULT 'pendente',
  isenta_por            CHAR(36) NULL,
  justificativa_isencao VARCHAR(500) NULL,
  fatura_uuid           CHAR(36) NULL,
  CONSTRAINT fk_multa_emprestimo FOREIGN KEY (emprestimo_id) REFERENCES lib_emprestimos (id),
  CONSTRAINT ck_multa_isencao CHECK (estado <> 'isenta' OR (isenta_por IS NOT NULL AND justificativa_isencao IS NOT NULL)),
  CONSTRAINT ck_multa_auto_isencao CHECK (isenta_por IS NULL OR isenta_por <> pessoa_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_digital_licencas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  item_id         BIGINT UNSIGNED NOT NULL,
  pessoa_uuid     CHAR(36) NOT NULL,
  inicio          DATETIME(3) NOT NULL,
  expira_em       DATETIME(3) NOT NULL,
  CONSTRAINT fk_licenca_item FOREIGN KEY (item_id) REFERENCES lib_itens (id),
  CONSTRAINT ck_licenca_prazo CHECK (expira_em > inicio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Empréstimo ativo é único por exemplar pela coluna gerada `ativo_chave`. Sala de leitura não tem tabela aqui: usa `recursos` de [44](44-agendamento-ambientes-equipamentos.md).

### 15.14 Relatórios (REL-07)

```sql
CREATE TABLE rel_modelos (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NULL,
  codigo            VARCHAR(60) NOT NULL,
  versao            INT UNSIGNED NOT NULL,
  tipo              ENUM('operacional','gerencial','regulatorio') NOT NULL,
  modulo            VARCHAR(40) NOT NULL,
  layout_regulatorio ENUM('censo','see','sinaes','recadastramento') NULL,
  ativo             TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE KEY ux_modelo_versao (codigo, versao),
  CONSTRAINT ck_modelo_regulatorio CHECK (tipo <> 'regulatorio' OR layout_regulatorio IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE rel_pedidos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  modelo_id       BIGINT UNSIGNED NOT NULL,
  solicitado_por  CHAR(36) NOT NULL,
  portal          ENUM('desenvolvedor','gestao','coordenacao','secretaria','financeiro','professor','aluno','responsaveis','terceiros') NOT NULL,
  filtro          JSON NOT NULL,
  formato         ENUM('tela','pdf','csv','xlsx','layout_oficial') NOT NULL,
  linhas          INT UNSIGNED NULL,
  estado          ENUM('na_fila','processando','pronto','expirado','erro') NOT NULL DEFAULT 'na_fila',
  criado_em       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_pedido_modelo FOREIGN KEY (modelo_id) REFERENCES rel_modelos (id),
  INDEX ix_pedido_fila (unidade_uuid, estado, criado_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE rel_arquivos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  pedido_id       BIGINT UNSIGNED NOT NULL UNIQUE,
  storage_path    VARCHAR(500) NOT NULL,
  arquivo_hash    CHAR(64) NOT NULL,
  layout_versao   VARCHAR(20) NULL,
  expira_em       DATETIME(3) NOT NULL,
  CONSTRAINT fk_arquivo_pedido FOREIGN KEY (pedido_id) REFERENCES rel_pedidos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE rel_agendamentos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  modelo_id       BIGINT UNSIGNED NOT NULL,
  criado_por      CHAR(36) NOT NULL,
  frequencia      ENUM('diaria','semanal','mensal') NOT NULL,
  destinatarios   JSON NOT NULL,
  ativo           TINYINT(1) NOT NULL DEFAULT 1,
  CONSTRAINT fk_agendamento_modelo FOREIGN KEY (modelo_id) REFERENCES rel_modelos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE rel_envios_regulatorios (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  tipo              ENUM('censo','see','sinaes','recadastramento') NOT NULL,
  ano               SMALLINT UNSIGNED NOT NULL,
  versao_layout     VARCHAR(20) NOT NULL,
  arquivo_hash      CHAR(64) NOT NULL,
  gerado_por        CHAR(36) NOT NULL,
  conferido_por     CHAR(36) NULL,
  enviado_por       CHAR(36) NULL,
  enviado_em        DATETIME(3) NULL,
  protocolo_orgao   VARCHAR(100) NULL,
  CONSTRAINT ck_envio_conferencia CHECK (enviado_por IS NULL OR conferido_por IS NOT NULL),
  CONSTRAINT ck_envio_gerador CHECK (conferido_por IS NULL OR conferido_por <> gerado_por),
  UNIQUE KEY ux_envio_versao (unidade_uuid, tipo, ano, versao_layout)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Envio ao órgão só com conferência da gestão e ação da secretaria, pelo layout da versão ([69](69-relatorios-e-censo-por-portal.md), seção 4). Relatório programado só para pessoas com vínculo, na aplicação ([69](69-relatorios-e-censo-por-portal.md), seção 2.4).

### 15.15 Importação (IMP-06)

```sql
CREATE TABLE imp_lotes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  tipo              ENUM('pessoas','estrutura','calendario_salas','turmas','matriculas','historico','documentos','acervo','saldos') NOT NULL,
  arquivo_hash      CHAR(64) NOT NULL,
  origem_sistema    VARCHAR(100) NULL,
  estado            ENUM('simulado','gravando','gravado','parcial','desfeito','rejeitado') NOT NULL DEFAULT 'simulado',
  importado_por     CHAR(36) NOT NULL,
  confirmado_por    CHAR(36) NULL,
  linhas_total      INT UNSIGNED NOT NULL DEFAULT 0,
  linhas_ok         INT UNSIGNED NOT NULL DEFAULT 0,
  linhas_rejeitadas INT UNSIGNED NOT NULL DEFAULT 0,
  criado_em         DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  desfeito_em       DATETIME(3) NULL,
  CONSTRAINT ck_lote_confirmacao CHECK (confirmado_por IS NULL OR confirmado_por <> importado_por),
  CONSTRAINT ck_lote_contagem CHECK (linhas_ok + linhas_rejeitadas <= linhas_total)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE imp_linhas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  lote_id         BIGINT UNSIGNED NOT NULL,
  unidade_uuid    CHAR(36) NOT NULL,
  numero_linha    INT UNSIGNED NOT NULL,
  chave_externa   VARCHAR(120) NOT NULL,
  registro_tipo   VARCHAR(60) NOT NULL,
  registro_uuid   CHAR(36) NULL,
  estado          ENUM('ok','rejeitada','duplicada') NOT NULL,
  payload_cifrado VARBINARY(8000) NULL,
  CONSTRAINT fk_linha_lote FOREIGN KEY (lote_id) REFERENCES imp_lotes (id),
  UNIQUE KEY ux_linha_lote (lote_id, numero_linha),
  UNIQUE KEY ux_chave_externa (unidade_uuid, registro_tipo, chave_externa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE imp_erros (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  linha_id        BIGINT UNSIGNED NOT NULL,
  codigo          VARCHAR(60) NOT NULL,
  campo           VARCHAR(60) NULL,
  mensagem        VARCHAR(500) NOT NULL,
  CONSTRAINT fk_erro_linha FOREIGN KEY (linha_id) REFERENCES imp_linhas (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE imp_mapeamentos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  unidade_uuid    CHAR(36) NOT NULL,
  origem          VARCHAR(100) NOT NULL,
  campo_origem    VARCHAR(100) NOT NULL,
  campo_destino   VARCHAR(100) NOT NULL,
  UNIQUE KEY ux_mapeamento (unidade_uuid, origem, campo_origem)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`ux_chave_externa` faz a idempotência do reenvio ([70](70-importacao-de-dados-por-portal.md), seção 4). `payload_cifrado` é apagado depois da gravação (IMP-04).

### 15.16 Financeiro (FIN-08)

> Valores em centavos, em `BIGINT`. Convenção de [18](18-regras-modulos-2.md), seção 3.

```sql
CREATE TABLE fin_contas (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                    CHAR(36) NOT NULL UNIQUE,
  unidade_uuid            CHAR(36) NOT NULL,
  nome                    VARCHAR(120) NOT NULL,
  tipo                    ENUM('corrente','poupanca','caixa','gateway','carteira') NOT NULL,
  banco_codigo            VARCHAR(10) NULL,
  saldo_inicial_centavos  BIGINT NOT NULL DEFAULT 0,
  ativa                   TINYINT(1) NOT NULL DEFAULT 1,
  deleted_at              DATETIME(3) NULL,
  UNIQUE KEY ux_conta_nome (unidade_uuid, nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_linhas_dre (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  codigo          VARCHAR(20) NOT NULL,
  nome            VARCHAR(150) NOT NULL,
  ordem           SMALLINT UNSIGNED NOT NULL,
  pai_id          BIGINT UNSIGNED NULL,
  tipo            ENUM('receita','deducao','custo','despesa','resultado') NOT NULL,
  CONSTRAINT fk_dre_pai FOREIGN KEY (pai_id) REFERENCES fin_linhas_dre (id),
  UNIQUE KEY ux_dre_codigo (unidade_uuid, codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_categorias (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  nome            VARCHAR(120) NOT NULL,
  natureza        ENUM('receita','despesa') NOT NULL,
  linha_dre_id    BIGINT UNSIGNED NULL,
  CONSTRAINT fk_categoria_dre FOREIGN KEY (linha_dre_id) REFERENCES fin_linhas_dre (id),
  UNIQUE KEY ux_categoria_nome (unidade_uuid, nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_centros_custo (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  codigo          VARCHAR(30) NOT NULL,
  nome            VARCHAR(150) NOT NULL,
  UNIQUE KEY ux_centro_codigo (unidade_uuid, codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_movimentacoes (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid        CHAR(36) NOT NULL,
  conta_id            BIGINT UNSIGNED NOT NULL,
  data                DATE NOT NULL,
  competencia_mes     CHAR(7) NOT NULL,
  valor_centavos      BIGINT NOT NULL,
  categoria_id        BIGINT UNSIGNED NOT NULL,
  origem_tipo         ENUM('titulo','despesa','cheque','caixa','ajuste','estorno','tarifa') NOT NULL,
  origem_uuid         CHAR(36) NULL,
  estado              ENUM('previsto','lancado','conciliado','estornado') NOT NULL DEFAULT 'lancado',
  estorno_de_id       BIGINT UNSIGNED NULL,
  idempotencia_chave  VARCHAR(100) NULL UNIQUE,
  CONSTRAINT fk_mov_conta FOREIGN KEY (conta_id) REFERENCES fin_contas (id),
  CONSTRAINT fk_mov_categoria FOREIGN KEY (categoria_id) REFERENCES fin_categorias (id),
  CONSTRAINT fk_mov_estorno FOREIGN KEY (estorno_de_id) REFERENCES fin_movimentacoes (id),
  CONSTRAINT ck_mov_valor CHECK (valor_centavos <> 0),
  INDEX ix_mov_competencia (unidade_uuid, competencia_mes)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_despesas (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid        CHAR(36) NOT NULL,
  fornecedor_uuid     CHAR(36) NOT NULL,
  categoria_id        BIGINT UNSIGNED NOT NULL,
  vencimento          DATE NOT NULL,
  valor_centavos      BIGINT UNSIGNED NOT NULL,
  solicitado_por      CHAR(36) NOT NULL,
  aprovado_por        CHAR(36) NULL,
  estado              ENUM('pendente_aprovacao','aprovada','paga','cancelada') NOT NULL DEFAULT 'pendente_aprovacao',
  nota_recebida_uuid  CHAR(36) NULL,
  CONSTRAINT fk_despesa_categoria FOREIGN KEY (categoria_id) REFERENCES fin_categorias (id),
  CONSTRAINT ck_despesa_aprovacao CHECK (aprovado_por IS NULL OR aprovado_por <> solicitado_por)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_rateios (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  unidade_uuid    CHAR(36) NOT NULL,
  despesa_id      BIGINT UNSIGNED NOT NULL,
  centro_custo_id BIGINT UNSIGNED NOT NULL,
  percentual      DECIMAL(7,4) NOT NULL,
  CONSTRAINT fk_rateio_despesa FOREIGN KEY (despesa_id) REFERENCES fin_despesas (id),
  CONSTRAINT fk_rateio_centro FOREIGN KEY (centro_custo_id) REFERENCES fin_centros_custo (id),
  CONSTRAINT ck_rateio_faixa CHECK (percentual > 0 AND percentual <= 100),
  UNIQUE KEY ux_rateio (despesa_id, centro_custo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_pagamentos (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid        CHAR(36) NOT NULL,
  despesa_id          BIGINT UNSIGNED NOT NULL,
  conta_id            BIGINT UNSIGNED NOT NULL,
  valor_centavos      BIGINT UNSIGNED NOT NULL,
  pago_em             DATETIME(3) NOT NULL,
  idempotencia_chave  VARCHAR(100) NOT NULL UNIQUE,
  CONSTRAINT fk_pagamento_despesa FOREIGN KEY (despesa_id) REFERENCES fin_despesas (id),
  CONSTRAINT fk_pagamento_conta FOREIGN KEY (conta_id) REFERENCES fin_contas (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_cheques (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  unidade_uuid        CHAR(36) NOT NULL,
  direcao             ENUM('recebido','emitido') NOT NULL,
  numero              VARCHAR(20) NOT NULL,
  banco_codigo        VARCHAR(10) NOT NULL,
  agencia             VARCHAR(10) NOT NULL,
  conta_cifrada       VARBINARY(64) NULL,
  valor_centavos      BIGINT UNSIGNED NOT NULL,
  emitente_pessoa_uuid CHAR(36) NULL,
  data_emissao        DATE NOT NULL,
  data_bom_para       DATE NULL,
  conta_id            BIGINT UNSIGNED NULL,
  estado              ENUM('recebido','custodiado','depositado','compensado','devolvido','substituido','emitido','entregue','cancelado') NOT NULL,
  CONSTRAINT fk_cheque_conta FOREIGN KEY (conta_id) REFERENCES fin_contas (id),
  UNIQUE KEY ux_cheque (unidade_uuid, direcao, banco_codigo, agencia, numero)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_caixas (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                    CHAR(36) NOT NULL UNIQUE,
  unidade_uuid            CHAR(36) NOT NULL,
  conta_id                BIGINT UNSIGNED NOT NULL,
  operador_uuid           CHAR(36) NULL,
  estado                  ENUM('aberto','fechado') NOT NULL DEFAULT 'aberto',
  saldo_abertura_centavos BIGINT NOT NULL,
  aberto_em               DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  ativo_chave             BIGINT UNSIGNED AS (CASE WHEN estado = 'aberto' THEN conta_id END) STORED,
  CONSTRAINT fk_caixa_conta FOREIGN KEY (conta_id) REFERENCES fin_contas (id),
  UNIQUE KEY ux_caixa_aberto (ativo_chave)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_fechamentos_caixa (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                  CHAR(36) NOT NULL UNIQUE,
  unidade_uuid          CHAR(36) NOT NULL,
  caixa_id              BIGINT UNSIGNED NOT NULL,
  contado_centavos      BIGINT NOT NULL,
  calculado_centavos    BIGINT NOT NULL,
  diferenca_centavos    BIGINT AS (contado_centavos - calculado_centavos) STORED,
  motivo_diferenca      VARCHAR(500) NULL,
  fechado_por           CHAR(36) NOT NULL,
  fechado_em            DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  aprovado_por          CHAR(36) NULL,
  CONSTRAINT fk_fechamento_caixa FOREIGN KEY (caixa_id) REFERENCES fin_caixas (id),
  CONSTRAINT ck_fechamento_diferenca CHECK (diferenca_centavos = 0 OR motivo_diferenca IS NOT NULL),
  CONSTRAINT ck_fechamento_aprovacao CHECK (aprovado_por IS NULL OR aprovado_por <> fechado_por)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_orcamentos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  exercicio       SMALLINT UNSIGNED NOT NULL,
  versao          INT UNSIGNED NOT NULL,
  estado          ENUM('rascunho','aprovado','encerrado') NOT NULL DEFAULT 'rascunho',
  aprovado_por    CHAR(36) NULL,
  UNIQUE KEY ux_orcamento_versao (unidade_uuid, exercicio, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fin_orcamento_linhas (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  orcamento_id      BIGINT UNSIGNED NOT NULL,
  centro_custo_id   BIGINT UNSIGNED NOT NULL,
  categoria_id      BIGINT UNSIGNED NOT NULL,
  mes               CHAR(7) NOT NULL,
  valor_centavos    BIGINT UNSIGNED NOT NULL,
  CONSTRAINT fk_orc_linha_orc FOREIGN KEY (orcamento_id) REFERENCES fin_orcamentos (id),
  CONSTRAINT fk_orc_linha_centro FOREIGN KEY (centro_custo_id) REFERENCES fin_centros_custo (id),
  CONSTRAINT fk_orc_linha_categoria FOREIGN KEY (categoria_id) REFERENCES fin_categorias (id),
  UNIQUE KEY ux_orc_linha (orcamento_id, centro_custo_id, categoria_id, mes)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Soma de rateio igual a 100 e teto de caixa aberto por conta são regras de aplicação e de chave única, conforme o caso ([71](71-financeiro-completo-por-portal.md), seções 4 e 6). Cheque cancelado continua na chave única, então o número não volta a ser usado ([71](71-financeiro-completo-por-portal.md), seção 5.3).

### 15.17 Campos personalizados (CPF-04)

```sql
CREATE TABLE cpf_definicoes (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                  CHAR(36) NOT NULL UNIQUE,
  unidade_uuid          CHAR(36) NULL,
  unidade_chave         CHAR(36) AS (IFNULL(unidade_uuid, 'ENTIDADE')) STORED,
  escopo                ENUM('entidade','unidade') NOT NULL,
  objeto                ENUM('aluno','responsavel','turma','disciplina','recurso','fornecedor','contrato') NOT NULL,
  chave                 VARCHAR(60) NOT NULL,
  nome                  VARCHAR(120) NOT NULL,
  tipo                  ENUM('texto_curto','texto_longo','numero','data','lista','sim_nao') NOT NULL,
  obrigatorio_criacao   TINYINT(1) NOT NULL DEFAULT 0,
  regra_validacao       JSON NULL,
  classificacao         ENUM('comum','pessoal','sensivel') NOT NULL,
  estado                ENUM('ativo','inativo') NOT NULL DEFAULT 'ativo',
  criado_por            CHAR(36) NOT NULL,
  CONSTRAINT ck_definicao_escopo CHECK ((escopo = 'entidade' AND unidade_uuid IS NULL) OR (escopo = 'unidade' AND unidade_uuid IS NOT NULL)),
  UNIQUE KEY ux_definicao_chave (unidade_chave, objeto, chave)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cpf_opcoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  definicao_id    BIGINT UNSIGNED NOT NULL,
  valor           VARCHAR(120) NOT NULL,
  ordem           SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  CONSTRAINT fk_opcao_definicao FOREIGN KEY (definicao_id) REFERENCES cpf_definicoes (id),
  UNIQUE KEY ux_opcao (definicao_id, valor)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cpf_valores (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  definicao_id    BIGINT UNSIGNED NOT NULL,
  registro_uuid   CHAR(36) NOT NULL,
  valor_texto     VARCHAR(2000) NULL,
  valor_numero    DECIMAL(18,4) NULL,
  valor_data      DATE NULL,
  valor_bool      TINYINT(1) NULL,
  atualizado_por  CHAR(36) NOT NULL,
  atualizado_em   DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_valor_definicao FOREIGN KEY (definicao_id) REFERENCES cpf_definicoes (id),
  UNIQUE KEY ux_valor_registro (definicao_id, registro_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

O `ENUM` de `objeto` não tem saúde, prontuário nem ocorrência: a regra de CPF-01 vale no próprio banco ([72](72-campos-personalizados-por-portal.md), seção 3). Remover definição não apaga valor: a definição só muda de `estado` ([72](72-campos-personalizados-por-portal.md), seção 4).

### 15.18 Meu perfil (PER-07)

> Os dados civis continuam no cadastro de identidade ([06](06-identidade-acesso.md), seção 12). Aqui ficam só o pedido de alteração civil e o histórico que o usuário vê ([76](76-meu-perfil-por-portal.md)).

```sql
CREATE TABLE per_pedidos_alteracao (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  pessoa_uuid       CHAR(36) NOT NULL,
  campo             ENUM('nome','cpf','vinculo','nascimento','documento') NOT NULL,
  valor_atual_hash  CHAR(64) NOT NULL,
  valor_novo_cifrado VARBINARY(1000) NOT NULL,
  motivo            VARCHAR(500) NULL,
  estado            ENUM('pendente','aprovado','recusado') NOT NULL DEFAULT 'pendente',
  solicitado_em     DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  prazo_ate         DATE NOT NULL,
  decidido_por      CHAR(36) NULL,
  decidido_em       DATETIME(3) NULL,
  motivo_recusa     VARCHAR(500) NULL,
  CONSTRAINT ck_pedido_aprovacao CHECK (decidido_por IS NULL OR decidido_por <> pessoa_uuid),
  CONSTRAINT ck_pedido_recusa CHECK (estado <> 'recusado' OR motivo_recusa IS NOT NULL),
  INDEX ix_pedido_fila (unidade_uuid, estado, prazo_ate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE per_historico (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                  CHAR(36) NOT NULL UNIQUE,
  unidade_uuid          CHAR(36) NULL,
  pessoa_uuid           CHAR(36) NOT NULL,
  campo                 VARCHAR(60) NOT NULL,
  valor_anterior_mascarado VARCHAR(200) NULL,
  valor_novo_mascarado  VARCHAR(200) NULL,
  origem                ENUM('proprio_usuario','secretaria','sistema') NOT NULL,
  alterado_por          CHAR(36) NOT NULL,
  alterado_em           DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  INDEX ix_historico_pessoa (pessoa_uuid, alterado_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Valor de dado sensível não entra em `per_historico` em claro: o campo fica `NULL` e a aplicação grava a máscara ([76](76-meu-perfil-por-portal.md), seção 3). O novo valor de pedido é cifrado até a decisão.

### 15.19 Simulados e redação (SIM-07)

> Estados, perfis e regras de nota em [47](47-simulados-por-portal.md). A IA só grava **nota sugerida**. A nota que o aluno vê é a confirmada por pessoa (MOD-06). Perfil publicado não muda: mudança cria nova versão. Ranking é calculado na consulta, não gravado.

```sql
CREATE TABLE sim_perfis (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NULL,
  origem            ENUM('modelo_plataforma','entidade') NOT NULL,
  codigo            VARCHAR(40) NOT NULL,
  nome              VARCHAR(120) NOT NULL,
  tipo              ENUM('enem','mec','harvard','custom') NOT NULL,
  versao            SMALLINT UNSIGNED NOT NULL,
  estado            ENUM('rascunho','publicado','arquivado') NOT NULL DEFAULT 'rascunho',
  publicado_por     CHAR(36) NULL,
  publicado_em      DATETIME(3) NULL,
  unidade_chave     CHAR(36) AS (IFNULL(unidade_uuid, 'MODELO')) STORED,
  CONSTRAINT ck_perfil_origem CHECK ((origem = 'modelo_plataforma' AND unidade_uuid IS NULL) OR (origem = 'entidade' AND unidade_uuid IS NOT NULL)),
  CONSTRAINT ck_perfil_publicado CHECK (estado <> 'publicado' OR publicado_em IS NOT NULL),
  UNIQUE KEY ux_perfil_versao (unidade_chave, codigo, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_rubrica_itens (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  perfil_id         BIGINT UNSIGNED NOT NULL,
  codigo            VARCHAR(20) NOT NULL,
  competencia       VARCHAR(200) NOT NULL,
  nota_maxima       DECIMAL(6,2) NOT NULL,
  peso              DECIMAL(5,2) NOT NULL DEFAULT 1.00,
  ordem             SMALLINT UNSIGNED NOT NULL,
  CONSTRAINT fk_rubrica_perfil FOREIGN KEY (perfil_id) REFERENCES sim_perfis (id),
  CONSTRAINT ck_rubrica_nota CHECK (nota_maxima > 0 AND peso > 0),
  UNIQUE KEY ux_rubrica_codigo (perfil_id, codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_questoes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  disciplina_uuid   CHAR(36) NULL,
  tipo              ENUM('objetiva','discursiva','redacao') NOT NULL,
  enunciado         TEXT NOT NULL,
  dificuldade       ENUM('facil','media','dificil') NULL,
  origem            ENUM('autoria_propria','banco_licenciado','gerada_ia_aprovada') NOT NULL,
  autor_uuid        CHAR(36) NOT NULL,
  aprovada_por      CHAR(36) NULL,
  estado            ENUM('rascunho','ativa','inativa') NOT NULL DEFAULT 'rascunho',
  CONSTRAINT ck_questao_ia CHECK (origem <> 'gerada_ia_aprovada' OR aprovada_por IS NOT NULL),
  INDEX ix_questao_banco (unidade_uuid, disciplina_uuid, estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_alternativas (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  questao_id        BIGINT UNSIGNED NOT NULL,
  letra             CHAR(1) NOT NULL,
  texto             TEXT NOT NULL,
  correta           TINYINT(1) NOT NULL DEFAULT 0,
  CONSTRAINT fk_alternativa_questao FOREIGN KEY (questao_id) REFERENCES sim_questoes (id),
  UNIQUE KEY ux_alternativa (questao_id, letra)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_simulados (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  turma_uuid        CHAR(36) NOT NULL,
  titulo            VARCHAR(200) NOT NULL,
  perfil_id         BIGINT UNSIGNED NULL,
  modo_resposta     ENUM('online','gabarito_proprio','gabarito_terceiro') NOT NULL,
  estado            ENUM('rascunho','publicado','em_aplicacao','encerrado','arquivado') NOT NULL DEFAULT 'rascunho',
  abre_em           DATETIME(3) NOT NULL,
  fecha_em          DATETIME(3) NOT NULL,
  criado_por        CHAR(36) NOT NULL,
  publicado_por     CHAR(36) NULL,
  publicado_em      DATETIME(3) NULL,
  CONSTRAINT fk_simulado_perfil FOREIGN KEY (perfil_id) REFERENCES sim_perfis (id),
  CONSTRAINT ck_simulado_janela CHECK (fecha_em > abre_em),
  CONSTRAINT ck_simulado_publicacao CHECK (estado = 'rascunho' OR publicado_em IS NOT NULL),
  INDEX ix_simulado_turma (unidade_uuid, turma_uuid, estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_simulado_questoes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  simulado_id       BIGINT UNSIGNED NOT NULL,
  questao_id        BIGINT UNSIGNED NOT NULL,
  ordem             SMALLINT UNSIGNED NOT NULL,
  peso              DECIMAL(5,2) NOT NULL DEFAULT 1.00,
  CONSTRAINT fk_sq_simulado FOREIGN KEY (simulado_id) REFERENCES sim_simulados (id),
  CONSTRAINT fk_sq_questao FOREIGN KEY (questao_id) REFERENCES sim_questoes (id),
  UNIQUE KEY ux_sq_questao (simulado_id, questao_id),
  UNIQUE KEY ux_sq_ordem (simulado_id, ordem)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_respostas_objetivas (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  simulado_id       BIGINT UNSIGNED NOT NULL,
  aluno_uuid        CHAR(36) NOT NULL,
  questao_id        BIGINT UNSIGNED NOT NULL,
  alternativa_id    BIGINT UNSIGNED NULL,
  origem            ENUM('online','leitura_gabarito_proprio','importacao_gabarito_terceiro') NOT NULL,
  lote_leitura_uuid CHAR(36) NULL,
  respondida_em     DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_ro_simulado FOREIGN KEY (simulado_id) REFERENCES sim_simulados (id),
  CONSTRAINT fk_ro_questao FOREIGN KEY (questao_id) REFERENCES sim_questoes (id),
  CONSTRAINT fk_ro_alternativa FOREIGN KEY (alternativa_id) REFERENCES sim_alternativas (id),
  UNIQUE KEY ux_ro_resposta (simulado_id, aluno_uuid, questao_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_redacoes (
  id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                  CHAR(36) NOT NULL UNIQUE,
  unidade_uuid          CHAR(36) NOT NULL,
  simulado_id           BIGINT UNSIGNED NOT NULL,
  aluno_uuid            CHAR(36) NOT NULL,
  tentativa             SMALLINT UNSIGNED NOT NULL DEFAULT 1,
  forma_envio           ENUM('imagem','pdf_digitalizado','pdf_texto','texto_digitado') NOT NULL,
  estado                ENUM('enviada','ocr_em_andamento','ocr_concluido','revisao_ocr','em_correcao_ia','sugerida_pela_ia','em_revisao_professor','confirmada','devolvida') NOT NULL DEFAULT 'enviada',
  texto_transcrito      MEDIUMTEXT NULL,
  enviada_em            DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  nota_confirmada       DECIMAL(6,2) NULL,
  correcao_confirmada_id BIGINT UNSIGNED NULL,
  confirmada_por        CHAR(36) NULL,
  confirmada_em         DATETIME(3) NULL,
  CONSTRAINT fk_redacao_simulado FOREIGN KEY (simulado_id) REFERENCES sim_simulados (id),
  CONSTRAINT ck_redacao_confirmada CHECK (estado <> 'confirmada' OR (nota_confirmada IS NOT NULL AND confirmada_por IS NOT NULL AND confirmada_em IS NOT NULL)),
  CONSTRAINT ck_redacao_autor CHECK (confirmada_por IS NULL OR confirmada_por <> aluno_uuid),
  UNIQUE KEY ux_redacao_tentativa (simulado_id, aluno_uuid, tentativa),
  INDEX ix_redacao_fila (unidade_uuid, estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_redacao_paginas (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  redacao_id        BIGINT UNSIGNED NOT NULL,
  ordem             SMALLINT UNSIGNED NOT NULL,
  objeto_uuid       CHAR(36) NOT NULL,
  cabecalho_recortado TINYINT(1) NOT NULL DEFAULT 0,
  confianca_ocr     DECIMAL(5,2) NULL,
  versao_motor_ocr  VARCHAR(40) NULL,
  CONSTRAINT fk_pagina_redacao FOREIGN KEY (redacao_id) REFERENCES sim_redacoes (id),
  CONSTRAINT ck_pagina_confianca CHECK (confianca_ocr IS NULL OR (confianca_ocr >= 0 AND confianca_ocr <= 100)),
  UNIQUE KEY ux_pagina_ordem (redacao_id, ordem)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_correcoes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  redacao_id        BIGINT UNSIGNED NOT NULL,
  versao            SMALLINT UNSIGNED NOT NULL,
  autoria           ENUM('ia','professor','coordenacao') NOT NULL,
  autor_uuid        CHAR(36) NULL,
  modelo            VARCHAR(80) NULL,
  versao_prompt     VARCHAR(40) NULL,
  hash_entrada      CHAR(64) NULL,
  nota_total        DECIMAL(6,2) NOT NULL,
  alerta_fuga_tema  TINYINT(1) NOT NULL DEFAULT 0,
  alerta_incoerencia TINYINT(1) NOT NULL DEFAULT 0,
  criada_em         DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_correcao_redacao FOREIGN KEY (redacao_id) REFERENCES sim_redacoes (id),
  CONSTRAINT ck_correcao_ia CHECK (autoria <> 'ia' OR (modelo IS NOT NULL AND versao_prompt IS NOT NULL AND hash_entrada IS NOT NULL AND autor_uuid IS NULL)),
  CONSTRAINT ck_correcao_pessoa CHECK (autoria = 'ia' OR autor_uuid IS NOT NULL),
  UNIQUE KEY ux_correcao_versao (redacao_id, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_correcao_competencias (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  correcao_id       BIGINT UNSIGNED NOT NULL,
  rubrica_item_id   BIGINT UNSIGNED NOT NULL,
  nota              DECIMAL(6,2) NOT NULL,
  feedback          TEXT NULL,
  CONSTRAINT fk_cc_correcao FOREIGN KEY (correcao_id) REFERENCES sim_correcoes (id),
  CONSTRAINT fk_cc_rubrica FOREIGN KEY (rubrica_item_id) REFERENCES sim_rubrica_itens (id),
  UNIQUE KEY ux_cc_item (correcao_id, rubrica_item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_redacao_eventos (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  redacao_id        BIGINT UNSIGNED NOT NULL,
  estado_de         VARCHAR(30) NOT NULL,
  estado_para       VARCHAR(30) NOT NULL,
  motivo            VARCHAR(500) NULL,
  ator_uuid         CHAR(36) NULL,
  ocorrido_em       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_evento_redacao FOREIGN KEY (redacao_id) REFERENCES sim_redacoes (id),
  CONSTRAINT ck_evento_devolucao CHECK (estado_para <> 'devolvida' OR motivo IS NOT NULL),
  INDEX ix_evento_redacao (redacao_id, ocorrido_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sim_trilhas_reforco (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  redacao_id        BIGINT UNSIGNED NOT NULL,
  atividade         VARCHAR(500) NOT NULL,
  sugerida_por_ia   TINYINT(1) NOT NULL DEFAULT 0,
  estado            ENUM('sugerida','aprovada','recusada','concluida','vencida') NOT NULL DEFAULT 'sugerida',
  aprovada_por      CHAR(36) NULL,
  prazo_ate         DATE NULL,
  CONSTRAINT fk_trilha_redacao FOREIGN KEY (redacao_id) REFERENCES sim_redacoes (id),
  CONSTRAINT ck_trilha_aprovacao CHECK (estado IN ('sugerida','recusada') OR (aprovada_por IS NOT NULL AND prazo_ate IS NOT NULL))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

O texto enviado ao gateway de IA sai de `texto_transcrito` depois do recorte do cabeçalho, sem nome nem identificador do aluno ([47](47-simulados-por-portal.md), seção 6). `hash_entrada` guarda só o hash desse texto. A IA nunca preenche `nota_confirmada` nem `confirmada_por`: a coluna exige pessoa, e a confirmação é ação de professor ou de coordenação (MOD-06). Questão de simulado publicado não muda: a aplicação recusa alteração em `sim_simulado_questoes` quando o simulado sai de `rascunho`. O prazo de 15 dias da trilha (SIM-05) é o valor inicial, ajustável pela escola. `vencida` é calculado na consulta e gravado só no fechamento do ciclo.

### 15.20 Integrações educacionais oficiais (INT-07)

> Regras em [74](74-integracoes-educacionais-oficiais.md). O arquivo do Educacenso continua registrado em `rel_envios_regulatorios` (seção 15.14). As tabelas abaixo guardam a conexão, o lote, o item enviado, a rejeição do órgão e a reconciliação. Credencial fica no cofre ([05](05-seguranca.md)): aqui só a referência.

```sql
CREATE TABLE int_conexoes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  unidade_uuid      CHAR(36) NOT NULL,
  sistema           ENUM('educacenso','sigep','sgp','municipal','pe_de_meia') NOT NULL,
  canal             ENUM('arquivo','api') NOT NULL,
  versao_layout     VARCHAR(20) NULL,
  credencial_ref    VARCHAR(120) NULL,
  termo_adesao_uuid CHAR(36) NULL,
  estado            ENUM('em_configuracao','ativa','suspensa','encerrada') NOT NULL DEFAULT 'em_configuracao',
  ativada_por       CHAR(36) NULL,
  ativada_em        DATETIME(3) NULL,
  CONSTRAINT ck_conexao_api CHECK (canal <> 'api' OR estado <> 'ativa' OR credencial_ref IS NOT NULL),
  CONSTRAINT ck_conexao_canal CHECK (sistema NOT IN ('educacenso','sigep') OR canal = 'arquivo'),
  CONSTRAINT ck_conexao_sgp CHECK (sistema NOT IN ('sgp','pe_de_meia') OR canal = 'api'),
  UNIQUE KEY ux_conexao_sistema (unidade_uuid, sistema)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE int_lotes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  conexao_id        BIGINT UNSIGNED NOT NULL,
  direcao           ENUM('saida','entrada') NOT NULL,
  tipo              ENUM('arquivo','api_incremental','reconciliacao') NOT NULL,
  periodo_ref       VARCHAR(20) NULL,
  estado            ENUM('gerado','conferido','aprovado','enviado','aceito','aceito_parcial','rejeitado','cancelado') NOT NULL DEFAULT 'gerado',
  arquivo_hash      CHAR(64) NULL,
  envio_regulatorio_id BIGINT UNSIGNED NULL,
  gerado_por        CHAR(36) NULL,
  conferido_por     CHAR(36) NULL,
  aprovado_por      CHAR(36) NULL,
  enviado_por       CHAR(36) NULL,
  enviado_em        DATETIME(3) NULL,
  protocolo_orgao   VARCHAR(100) NULL,
  motivo_cancelamento VARCHAR(500) NULL,
  CONSTRAINT fk_lote_conexao FOREIGN KEY (conexao_id) REFERENCES int_conexoes (id),
  CONSTRAINT fk_lote_envio FOREIGN KEY (envio_regulatorio_id) REFERENCES rel_envios_regulatorios (id),
  CONSTRAINT ck_lote_arquivo CHECK (tipo <> 'arquivo' OR arquivo_hash IS NOT NULL),
  CONSTRAINT ck_lote_conferencia CHECK (conferido_por IS NULL OR conferido_por <> gerado_por),
  CONSTRAINT ck_lote_envio CHECK (tipo = 'api_incremental' OR direcao = 'entrada' OR enviado_em IS NULL OR aprovado_por IS NOT NULL),
  CONSTRAINT ck_lote_cancelado CHECK (estado <> 'cancelado' OR motivo_cancelamento IS NOT NULL),
  INDEX ix_lote_conexao (conexao_id, estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE int_itens (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  lote_id             BIGINT UNSIGNED NOT NULL,
  conexao_id          BIGINT UNSIGNED NOT NULL,
  registro_tipo       VARCHAR(40) NOT NULL,
  registro_uuid       CHAR(36) NOT NULL,
  chave_idempotencia  CHAR(64) NOT NULL,
  estado              ENUM('pendente','enviado','aceito','rejeitado') NOT NULL DEFAULT 'pendente',
  tentativas          SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  ultimo_envio_em     DATETIME(3) NULL,
  CONSTRAINT fk_item_lote FOREIGN KEY (lote_id) REFERENCES int_lotes (id),
  CONSTRAINT fk_item_conexao FOREIGN KEY (conexao_id) REFERENCES int_conexoes (id),
  UNIQUE KEY ux_item_idempotencia (conexao_id, chave_idempotencia),
  INDEX ix_item_registro (registro_tipo, registro_uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE int_rejeicoes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36) NOT NULL UNIQUE,
  lote_id           BIGINT UNSIGNED NOT NULL,
  item_id           BIGINT UNSIGNED NULL,
  codigo_orgao      VARCHAR(40) NOT NULL,
  mensagem          VARCHAR(1000) NOT NULL,
  campo             VARCHAR(80) NULL,
  modulo_origem     VARCHAR(40) NOT NULL,
  estado            ENUM('aberta','corrigida','descartada') NOT NULL DEFAULT 'aberta',
  tratada_por       CHAR(36) NULL,
  motivo_descarte   VARCHAR(500) NULL,
  CONSTRAINT fk_rejeicao_lote FOREIGN KEY (lote_id) REFERENCES int_lotes (id),
  CONSTRAINT fk_rejeicao_item FOREIGN KEY (item_id) REFERENCES int_itens (id),
  CONSTRAINT ck_rejeicao_descarte CHECK (estado <> 'descartada' OR (motivo_descarte IS NOT NULL AND tratada_por IS NOT NULL)),
  INDEX ix_rejeicao_fila (modulo_origem, estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE int_reconciliacoes (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  conexao_id        BIGINT UNSIGNED NOT NULL,
  data_ref          DATE NOT NULL,
  total_interno     INT UNSIGNED NOT NULL,
  total_externo     INT UNSIGNED NOT NULL,
  total_diferencas  INT UNSIGNED NOT NULL,
  estado            VARCHAR(15) AS (IF(total_diferencas = 0, 'ok', 'com_diferenca')) STORED,
  executada_em      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_reconciliacao_conexao FOREIGN KEY (conexao_id) REFERENCES int_conexoes (id),
  UNIQUE KEY ux_reconciliacao_dia (conexao_id, data_ref)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Os `CHECK` de `int_conexoes` gravam no banco os canais de [74](74-integracoes-educacionais-oficiais.md): Educacenso e SIGEP só por arquivo; SGP e Pé-de-Meia só por API. O sistema municipal aceita os dois (INT-01). Nenhuma coluna guarda endereço de banco de terceiro. Lote de arquivo enviado ao órgão exige aprovação da gestão e conferência por pessoa diferente de quem gerou. Envio incremental por API é aprovado uma vez, na ativação da conexão. Rejeição não é corrigida no lote: volta ao módulo de origem e só fecha como `corrigida` ou `descartada` com motivo (princípio 5 de [74](74-integracoes-educacionais-oficiais.md)). Diferença de reconciliação vira item para a secretaria, sem correção automática.
