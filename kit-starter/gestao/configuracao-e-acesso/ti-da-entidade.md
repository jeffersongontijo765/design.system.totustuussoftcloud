# TI da entidade

- Portal: Gestão (`gestao.`)
- Área: Configuração e acesso
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 2; [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 4; [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 5; [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 6; [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 7; [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 8; [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 9; [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 11
- Fonte da v1: absorvida integralmente em [ti.md](../../desenvolvedor/seguranca-e-operacao/ti.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

TI da entidade: ativos, licenças, chamados de TI, mudanças e monitoramento de equipamentos.

## 3. Telas

- **Ativos de TI** (DataTable).
- **Licenças** (vencimentos).
- **Chamados de TI** (fila).
- **Mudanças** (fluxo com aprovação por comitê).

## 4. Permissões por portal (extraídas do SDD)

Do [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md):

| Portal | Recurso de TI | Escopo |
|---|---|---|
| Gestão | TI da entidade (seção 4): ativos, licenças, redes, chamados, incidentes, mudanças, contratos, fornecedores | Entidade e unidades, conforme permissão |

## 5. Papéis

- `unit.it.admin`, `unit.it.technician`, `unit.it.change_approver`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seções 4 a 11.

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

### 13.1 [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 2

#### 2. Dois assuntos com o mesmo nome

| Assunto | Quem opera | Onde fica | Exemplos | Portal |
|---|---|---|---|---|
| **TI da plataforma** (operação do SaaS) | Equipe de operação da plataforma | Infraestrutura da plataforma | Clusters, DNS, certificados TLS, backups, filas, cache, monitoramento dos serviços | Desenvolvedor, "Gestão de TI" e "Configurações do Sistema" |
| **TI da entidade** (suporte de tecnologia da escola) | Equipe de TI da entidade | Dados da entidade, banco da unidade | Computadores, licenças de software, rede da escola, chamados de TI, inventário | Gestão |

**Regra:** a TI da plataforma **não é módulo de tenant**. Nenhum cliente acessa a infraestrutura da plataforma, nem como leitura. A TI da entidade **não acessa** a infraestrutura da plataforma.

Consequência: a tabela de recursos de infraestrutura da v1 (Kubernetes, DNS, backups) sai do módulo de TI de tenant. Ela fica nos documentos de operação ([10](../../../docs/v2/10-implantacao-operacao.md), [24](../../../docs/v2/24-operacao-continuidade-qualidade.md)), com acesso só pelo portal do desenvolvedor.

### 13.2 [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 4

#### 4. TI da entidade (portal de gestão)

##### 4.1 Recursos e donos

| Recurso da v1 | Proposta na v2 | Dono de dado |
|---|---|---|
| Hardware (computador, servidor local, impressora) | Ativo de TI com ciclo de vida | TI da entidade |
| Software e licenças | Licença com número de assentos, validade e contrato ligado | TI da entidade |
| Redes e links | Circuito e equipamento de rede. Nunca guarda senha de equipamento em texto | TI da entidade |
| Ativos (inventário) | Vista sobre o Patrimônio, para bens de TI. Ver seção 5 | Patrimônio |
| CMDB (relações entre ativos, serviços e contratos) | Modelo de relação. Restrito a ativos da própria entidade | TI da entidade |
| Chamados de TI | Categoria "TI" do módulo de atendimento. Ver seção 5 | Atendimento |
| Incidentes | Chamado de tipo incidente, com severidade e impacto | Atendimento |
| Problemas (causa raiz) | Registro ligado a incidentes recorrentes | TI da entidade |
| Mudanças | Solicitação com aprovação por comitê, ver seção 6 | TI da entidade |
| Contratos, SLA e garantias de TI | Tipo de contrato em [33](../../../docs/v2/33-contratos-por-portal.md). SLA do engine de [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.3 | Contratos |
| Fornecedores de TI | Cadastro de fornecedor em Suprimentos. Ver seção 5 | Suprimentos |
| Monitoramento de links e equipamentos da escola | Só se a entidade mantém equipamento monitorado. Ver seção 7 | TI da entidade |
| Base de conhecimento de TI | Artigos do atendimento ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.7) | Atendimento |
| Automações e relatórios | Regra de disparo e painel do módulo | TI da entidade |

##### 4.2 Estados de incidente e mudança

A v1 não define estado. Proposta, em linha com a prática de gestão de serviço de TI:

**Incidente:** `aberto` → `em_atendimento` → `resolvido` → `fechado`; `reaberto` a partir de `resolvido`. Severidade de 1 a 4 define o SLA.

**Problema:** `identificado` → `em_analise` → `solucao_definida` → `resolvido`. Liga a um ou mais incidentes.

**Mudança:** `solicitada` → `avaliada` → `aprovada` ou `recusada` → `agendada` → `implantada` → `verificada` → `fechada`. Mudança emergencial tem caminho próprio, com aprovação posterior registrada.

**Regras:**

- Mudança em ativo de produção (sistema que atende alunos) exige aprovação de um segundo papel. Quem solicita não aprova.
- Mudança sem plano de volta (rollback) não é aprovada.
- Incidente resolvido sem causa registrada fica em aberto para o problema, se for recorrente.

### 13.3 [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 5

#### 5. Duplicidades a resolver

| Duplicidade | Proposta | Decisão |
|---|---|---|
| **Ativos de TI × Patrimônio** (`spec_patrimonio_completo`, com QR, RFID e depreciação) | Patrimônio é o dono do bem. TI tem uma vista filtrada por categoria "tecnologia", com campos próprios (IP, MAC, serial, licença) guardados no registro do bem | **Decidido** em 03/11/2026: vista do patrimônio, sem cadastro próprio |
| **Chamados de TI × Atendimento** | Chamado de TI é um ticket de categoria TI. Não há fila separada. SLA, estados e portal são os de [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md) | Proposta registrada. Confirmar |
| **Contratos de TI × Contratos** | Contrato de licença, suporte e link é tipo de contrato em [33](../../../docs/v2/33-contratos-por-portal.md). Sem repositório separado | Proposta registrada |
| **Fornecedores de TI × Suprimentos** | Fornecedor é cadastro único em Suprimentos | Proposta registrada |
| **SLA de TI × SLA de atendimento** | Motor único de SLA ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.3) | Proposta registrada |
| **Segurança (menu de TI) × Segurança da v2** | Política de segurança e auditoria ficam em [05](../../../docs/v2/05-seguranca.md) e [29](../../../docs/v2/29-auditoria.md). TI só consome o resultado | Proposta registrada |

### 13.4 [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 6

#### 6. Permissões

| Papel | Pode | Não pode |
|---|---|---|
| Administrador de TI da entidade | Ativos, licenças, chamados de TI, mudanças | Aprovar a própria mudança |
| Técnico de TI | Atender chamados e incidentes, registrar resolução | Alterar contrato, excluir ativo |
| Aprovador de mudança (comitê) | Aprovar ou recusar mudança | Executar a mudança que aprovou |
| Auditor | Ler ativos, mudanças e registros de acesso | Alterar nada |
| Usuário comum (professor, aluno, funcionário) | Abrir chamado de TI pelo portal correspondente | Ver ativo, inventário, rede ou licença |

Segregação: quem executa mudança não aprova a própria mudança ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5).

### 13.5 [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 7

#### 7. Monitoramento de equipamento da entidade

A v1 inclui monitoramento de servidores, links e equipamentos. Para a entidade, isso só vale se ela tiver equipamento próprio em rede monitorada. Regras:

- Coleta de métrica (uptime, latência, utilização) sem conteúdo de tráfego.
- Nenhuma credencial de equipamento no painel. Credencial de coleta fica no cofre ([05](../../../docs/v2/05-seguranca.md), seção 2).
- Alerta por limite configurável por equipamento.
- Dado de monitoramento não identifica pessoa. Log de acesso de pessoa a equipamento segue [29](../../../docs/v2/29-auditoria.md).

### 13.6 [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 8

#### 8. Por portal

| Portal | Recurso de TI | Escopo |
|---|---|---|
| Desenvolvedor | TI da plataforma (seção 3) | Plataforma apenas |
| Gestão | TI da entidade (seção 4): ativos, licenças, redes, chamados, incidentes, mudanças, contratos, fornecedores | Entidade e unidades, conforme permissão |
| Professor | Abrir chamado de TI (computador da sala, projetor, acesso a sistema) | Só o próprio chamado |
| Aluno | Abrir chamado de acesso (senha, conta) pelo portal do aluno | Só o próprio chamado. Redefinição de senha segue [06](../../../docs/v2/06-identidade-acesso.md) |
| Responsáveis | Nenhum recurso de TI da entidade | — |
| Terceiros | Chamado de manutenção de equipamento de fornecedor, e acesso à rede da unidade quando contratado | Só o próprio chamado e o próprio acesso |

**Regra:** nenhum portal, exceto o de gestão e o do desenvolvedor, mostra inventário, topologia de rede, licença ou configuração de equipamento.

### 13.7 [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 9

#### 9. Lacunas

| # | Lacuna | Tipo |
|---|---|---|
| TI-01 | Inventário de certificados TLS e dono de cada um | **Escrito** na seção 11 |
| TI-02 | Painel de monitoramento da plataforma por serviço, com escalonamento | **Escrito** na seção 11 |
| TI-03 | Janela de manutenção programada e aviso aos clientes | **Escrito** na seção 11 |
| TI-04 | DDL de ativo de TI, licença, incidente, problema, mudança, CMDB | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 11. Revisão do owner pendente (DDL-01) |
| TI-05 | Remover [`sub_sidebar_itsm.php`](../../../docs/v2/anexo-v1/sub_sidebar_itsm.php) do repositório de especificações e corrigir o `onclick=` no código (ACH-01) | Código. **Decidido** em 03/11/2026: remover e corrigir |
| TI-06 | Vista de ativo de TI sobre Patrimônio (seção 5) | **Decidido** em 03/11/2026: vista do patrimônio, sem cadastro próprio |
| TI-07 | Comitê de mudança: quem participa e com que quórum | **Decidido** em 03/11/2026: gestor de TI, segurança e um representante da direção. Quórum de 2 de 3 |
| TI-08 | Monitoramento de equipamento da entidade (seção 7) | **Decidido** em 03/11/2026: mantido, visível só à gestão de TI da entidade |
| TI-09 | Mudança emergencial: prazo para aprovação posterior | **Decidido** em 03/11/2026: 48 horas |

### 13.8 [36](../../../docs/v2/36-tecnologia-da-informacao-por-portal.md), seção 11

#### 11. Especificação dos itens TI-01 a TI-03

**TI-01: inventário de certificados TLS.** Cada certificado tem dono, domínio, emissor, data de validade e local de instalação. Alerta aos 30 dias e aos 14 dias antes do vencimento ([10](../../../docs/v2/10-implantacao-operacao.md), seção 7). Certificado sem dono atribuído aparece no painel como pendência. Tabela e DDL na seção 11.1.

**TI-02: painel de monitoramento da plataforma.** Painel por serviço (API, sinalização, fila, banco de cada unidade, armazenamento de mídia), com estado, latência, taxa de erro e alertas. Escalonamento: alerta ao plantão em até 5 minutos para serviço parado; ao gestor de TI em até 30 minutos sem reconhecimento. Painel é do portal do desenvolvedor e não mostra dado de entidade.

**TI-03: janela de manutenção e aviso aos clientes.** Janela programada fora do horário de aula de cada unidade, com aviso às entidades com antecedência de 48 horas. Manutenção emergencial segue o comitê de mudança e a aprovação posterior de 48 horas (TI-07 e TI-09, decididos em 03/11/2026).

| Código | Regra de aceite |
|---|---|
| TI-01 | Certificado vencido sem alerta prévio é falha de teste |
| TI-02 | Serviço parado gera alerta em até 5 minutos (teste de alarme) |
| TI-03 | Manutenção fora da janela sem aprovação de emergência é recusada |

##### 11.1 DDL (TI-04 e apoio a TI-01)

```sql
CREATE TABLE ti_certificados (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  dominio         VARCHAR(255) NOT NULL,
  emissor         VARCHAR(120) NOT NULL,
  instalado_em    VARCHAR(120) NOT NULL,
  valido_ate      DATE NOT NULL,
  dono_uuid       CHAR(36) NULL,
  INDEX ix_cert_validade (valido_ate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

As demais tabelas de TI (ativo, licença, incidente, problema e mudança) estão em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 11.
