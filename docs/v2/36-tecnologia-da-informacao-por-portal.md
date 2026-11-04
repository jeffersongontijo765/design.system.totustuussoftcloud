# 36 — Tecnologia da Informação (TI), por Portal

> Parte do [SDD v2](00-README.md). Operação da plataforma em [10](10-implantacao-operacao.md) e [24](24-operacao-continuidade-qualidade.md). Atendimento de chamados em [32](32-atendimento-privacidade-por-portal.md). Patrimônio em [19](19-regras-modulos-3.md), seção 8. Contratos em [33](33-contratos-por-portal.md). Achados da v1 em [13](13-achados-v1.md) (ACH-01, ACH-14).
> **Status:** aprovada pelo autor em 03/11/2026, com as propostas adotadas. Itens sem valor definido continuam pendentes, criada em 03/11/2026 a partir de [`spec_gestao_ti_completa.md`](anexo-v1/spec_gestao_ti_completa.md) (882 linhas, 18 seções) e da navegação da v1 ([12](anexo-v1/12-portals-navigation-sidebar-pages-spec.md), seção 4.1). Itens **[Decisão do autor]** dependem de resposta.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| O módulo de TI está completo? | **Não.** A v1 tem o escopo (18 domínios e 19 itens de menu), mas nenhuma regra de validação, estado, DDL ou critério de aceite. O catálogo o marca como "Revisar" ([12](12-catalogo-modulos.md)) |
| Está organizado por portal? | **Não.** A v1 mistura dois assuntos diferentes no mesmo módulo: a TI **da plataforma** e a TI **da entidade** |
| Há duplicidade com outros módulos? | **Sim.** Ativos × Patrimônio; Chamados × Atendimento; Contratos e SLA × Contratos; Fornecedores × Suprimentos |
| O código da view é aceitável? | **Não.** [`sub_sidebar_itsm.php`](anexo-v1/sub_sidebar_itsm.php) tem `onclick=`, o que viola a regra de zero JavaScript inline ([02](02-arquitetura.md), ADR-07). Achado ACH-01 em [13](13-achados-v1.md) |

---

## 2. Dois assuntos com o mesmo nome

| Assunto | Quem opera | Onde fica | Exemplos | Portal |
|---|---|---|---|---|
| **TI da plataforma** (operação do SaaS) | Equipe de operação da plataforma | Infraestrutura da plataforma | Clusters, DNS, certificados TLS, backups, filas, cache, monitoramento dos serviços | Desenvolvedor, "Gestão de TI" e "Configurações do Sistema" |
| **TI da entidade** (suporte de tecnologia da escola) | Equipe de TI da entidade | Dados da entidade, banco da unidade | Computadores, licenças de software, rede da escola, chamados de TI, inventário | Gestão |

**Regra:** a TI da plataforma **não é módulo de tenant**. Nenhum cliente acessa a infraestrutura da plataforma, nem como leitura. A TI da entidade **não acessa** a infraestrutura da plataforma.

Consequência: a tabela de recursos de infraestrutura da v1 (Kubernetes, DNS, backups) sai do módulo de TI de tenant. Ela fica nos documentos de operação ([10](10-implantacao-operacao.md), [24](24-operacao-continuidade-qualidade.md)), com acesso só pelo portal do desenvolvedor.

---

## 3. TI da plataforma (portal do desenvolvedor)

| Recurso | Estado na v2 | Onde está | Lacuna |
|---|---|---|---|
| Backup e restauração | Definido | [24](24-operacao-continuidade-qualidade.md), seção 1 | Prazo de retenção de backup (G-12) |
| Certificados TLS | Alerta a 14 dias | [10](10-implantacao-operacao.md), seção 7 | Inventário de certificados e dono de cada um |
| Monitoramento e alertas | Definido em partes | [10](10-implantacao-operacao.md), seção 7 | Painel por serviço e regra de escalonamento |
| Filas e workers | Parcial | [14](14-integracao-modulos.md) | Painel e limite de fila por entidade |
| Cache | Definido | [30](30-cache.md) | Dimensionamento (CAC-01) |
| Manutenção programada | Parcial | [24](24-operacao-continuidade-qualidade.md), seção 3 | Janela de manutenção e aviso aos clientes |
| Cluster, DNS, nuvem | Não definido | — | Escolha de provedor (ver [10](10-implantacao-operacao.md)) |
| Inventário de segredos | Definido | [05](05-seguranca.md), seção 2 | Rotação e dono por segredo |

**Regra:** toda ação de infraestrutura é registrada em [29](29-auditoria.md), categoria "processo", com `portal = desenvolvedor`.

---

## 4. TI da entidade (portal de gestão)

### 4.1 Recursos e donos

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
| Contratos, SLA e garantias de TI | Tipo de contrato em [33](33-contratos-por-portal.md). SLA do engine de [32](32-atendimento-privacidade-por-portal.md), seção 2.3 | Contratos |
| Fornecedores de TI | Cadastro de fornecedor em Suprimentos. Ver seção 5 | Suprimentos |
| Monitoramento de links e equipamentos da escola | Só se a entidade mantém equipamento monitorado. Ver seção 7 | TI da entidade |
| Base de conhecimento de TI | Artigos do atendimento ([32](32-atendimento-privacidade-por-portal.md), seção 2.7) | Atendimento |
| Automações e relatórios | Regra de disparo e painel do módulo | TI da entidade |

### 4.2 Estados de incidente e mudança

A v1 não define estado. Proposta, em linha com a prática de gestão de serviço de TI:

**Incidente:** `aberto` → `em_atendimento` → `resolvido` → `fechado`; `reaberto` a partir de `resolvido`. Severidade de 1 a 4 define o SLA.

**Problema:** `identificado` → `em_analise` → `solucao_definida` → `resolvido`. Liga a um ou mais incidentes.

**Mudança:** `solicitada` → `avaliada` → `aprovada` ou `recusada` → `agendada` → `implantada` → `verificada` → `fechada`. Mudança emergencial tem caminho próprio, com aprovação posterior registrada.

**Regras:**

- Mudança em ativo de produção (sistema que atende alunos) exige aprovação de um segundo papel. Quem solicita não aprova.
- Mudança sem plano de volta (rollback) não é aprovada.
- Incidente resolvido sem causa registrada fica em aberto para o problema, se for recorrente.

---

## 5. Duplicidades a resolver

| Duplicidade | Proposta | Decisão |
|---|---|---|
| **Ativos de TI × Patrimônio** (`spec_patrimonio_completo`, com QR, RFID e depreciação) | Patrimônio é o dono do bem. TI tem uma vista filtrada por categoria "tecnologia", com campos próprios (IP, MAC, serial, licença) guardados no registro do bem | **Decidido** em 03/11/2026: vista do patrimônio, sem cadastro próprio |
| **Chamados de TI × Atendimento** | Chamado de TI é um ticket de categoria TI. Não há fila separada. SLA, estados e portal são os de [32](32-atendimento-privacidade-por-portal.md) | Proposta registrada. Confirmar |
| **Contratos de TI × Contratos** | Contrato de licença, suporte e link é tipo de contrato em [33](33-contratos-por-portal.md). Sem repositório separado | Proposta registrada |
| **Fornecedores de TI × Suprimentos** | Fornecedor é cadastro único em Suprimentos | Proposta registrada |
| **SLA de TI × SLA de atendimento** | Motor único de SLA ([32](32-atendimento-privacidade-por-portal.md), seção 2.3) | Proposta registrada |
| **Segurança (menu de TI) × Segurança da v2** | Política de segurança e auditoria ficam em [05](05-seguranca.md) e [29](29-auditoria.md). TI só consome o resultado | Proposta registrada |

---

## 6. Permissões

| Papel | Pode | Não pode |
|---|---|---|
| Administrador de TI da entidade | Ativos, licenças, chamados de TI, mudanças | Aprovar a própria mudança |
| Técnico de TI | Atender chamados e incidentes, registrar resolução | Alterar contrato, excluir ativo |
| Aprovador de mudança (comitê) | Aprovar ou recusar mudança | Executar a mudança que aprovou |
| Auditor | Ler ativos, mudanças e registros de acesso | Alterar nada |
| Usuário comum (professor, aluno, funcionário) | Abrir chamado de TI pelo portal correspondente | Ver ativo, inventário, rede ou licença |

Segregação: quem executa mudança não aprova a própria mudança ([22](22-crm-canais-e-papeis.md), seção 5).

---

## 7. Monitoramento de equipamento da entidade

A v1 inclui monitoramento de servidores, links e equipamentos. Para a entidade, isso só vale se ela tiver equipamento próprio em rede monitorada. Regras:

- Coleta de métrica (uptime, latência, utilização) sem conteúdo de tráfego.
- Nenhuma credencial de equipamento no painel. Credencial de coleta fica no cofre ([05](05-seguranca.md), seção 2).
- Alerta por limite configurável por equipamento.
- Dado de monitoramento não identifica pessoa. Log de acesso de pessoa a equipamento segue [29](29-auditoria.md).

---

## 8. Por portal

| Portal | Recurso de TI | Escopo |
|---|---|---|
| Desenvolvedor | TI da plataforma (seção 3) | Plataforma apenas |
| Gestão | TI da entidade (seção 4): ativos, licenças, redes, chamados, incidentes, mudanças, contratos, fornecedores | Entidade e unidades, conforme permissão |
| Professor | Abrir chamado de TI (computador da sala, projetor, acesso a sistema) | Só o próprio chamado |
| Aluno | Abrir chamado de acesso (senha, conta) pelo portal do aluno | Só o próprio chamado. Redefinição de senha segue [06](06-identidade-acesso.md) |
| Responsáveis | Nenhum recurso de TI da entidade | — |
| Terceiros | Chamado de manutenção de equipamento de fornecedor, e acesso à rede da unidade quando contratado | Só o próprio chamado e o próprio acesso |

**Regra:** nenhum portal, exceto o de gestão e o do desenvolvedor, mostra inventário, topologia de rede, licença ou configuração de equipamento.

---

## 9. Lacunas

| # | Lacuna | Tipo |
|---|---|---|
| TI-01 | Inventário de certificados TLS e dono de cada um | **Escrito** na seção 11 |
| TI-02 | Painel de monitoramento da plataforma por serviço, com escalonamento | **Escrito** na seção 11 |
| TI-03 | Janela de manutenção programada e aviso aos clientes | **Escrito** na seção 11 |
| TI-04 | DDL de ativo de TI, licença, incidente, problema, mudança, CMDB | **Escrito** em [51](51-ddl-modulos-novos.md), seção 11. Revisão do owner pendente (DDL-01) |
| TI-05 | Remover [`sub_sidebar_itsm.php`](anexo-v1/sub_sidebar_itsm.php) do repositório de especificações e corrigir o `onclick=` no código (ACH-01) | Código. **Decidido** em 03/11/2026: remover e corrigir |
| TI-06 | Vista de ativo de TI sobre Patrimônio (seção 5) | **Decidido** em 03/11/2026: vista do patrimônio, sem cadastro próprio |
| TI-07 | Comitê de mudança: quem participa e com que quórum | **Decidido** em 03/11/2026: gestor de TI, segurança e um representante da direção. Quórum de 2 de 3 |
| TI-08 | Monitoramento de equipamento da entidade (seção 7) | **Decidido** em 03/11/2026: mantido, visível só à gestão de TI da entidade |
| TI-09 | Mudança emergencial: prazo para aprovação posterior | **Decidido** em 03/11/2026: 48 horas |

---

## 10. Critérios de aceite

- [ ] Nenhum cliente acessa infraestrutura da plataforma (teste de isolamento).
- [ ] Mudança em ativo de produção não é aprovada pelo próprio solicitante (teste).
- [ ] Mudança sem plano de volta é recusada (teste).
- [ ] Credencial de equipamento não aparece em painel, relatório ou log (varredura).
- [ ] Ativo de TI tem um único dono de dado (Patrimônio), sem cópia.
- [ ] [`sub_sidebar_itsm.php`](anexo-v1/sub_sidebar_itsm.php) sem `onclick=` ou removido do repositório de especificações.
- [ ] Itens **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).

---

## 11. Especificação dos itens TI-01 a TI-03

**TI-01: inventário de certificados TLS.** Cada certificado tem dono, domínio, emissor, data de validade e local de instalação. Alerta aos 30 dias e aos 14 dias antes do vencimento ([10](10-implantacao-operacao.md), seção 7). Certificado sem dono atribuído aparece no painel como pendência. Tabela e DDL na seção 11.1.

**TI-02: painel de monitoramento da plataforma.** Painel por serviço (API, sinalização, fila, banco de cada unidade, armazenamento de mídia), com estado, latência, taxa de erro e alertas. Escalonamento: alerta ao plantão em até 5 minutos para serviço parado; ao gestor de TI em até 30 minutos sem reconhecimento. Painel é do portal do desenvolvedor e não mostra dado de entidade.

**TI-03: janela de manutenção e aviso aos clientes.** Janela programada fora do horário de aula de cada unidade, com aviso às entidades com antecedência de 48 horas. Manutenção emergencial segue o comitê de mudança e a aprovação posterior de 48 horas (TI-07 e TI-09, decididos em 03/11/2026).

| Código | Regra de aceite |
|---|---|
| TI-01 | Certificado vencido sem alerta prévio é falha de teste |
| TI-02 | Serviço parado gera alerta em até 5 minutos (teste de alarme) |
| TI-03 | Manutenção fora da janela sem aprovação de emergência é recusada |

### 11.1 DDL (TI-04 e apoio a TI-01)

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

As demais tabelas de TI (ativo, licença, incidente, problema e mudança) estão em [51](51-ddl-modulos-novos.md), seção 11.
