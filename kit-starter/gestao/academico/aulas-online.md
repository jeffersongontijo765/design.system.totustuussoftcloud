# Aulas online e reuniões ao vivo

- Portal: Gestão (`gestao.`)
- Área: Acadêmico
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [40](../../../docs/v2/40-aulas-online-por-portal.md) (integral)
- Fonte da v1: [global_meeting_spec_v2_complete.md](../../../docs/v2/anexo-v1/global_meeting_spec_v2_complete.md) (620 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Configurar e acompanhar aulas online e reuniões (tipos de sessão, entrada, interface da sala, gravação com consentimento, transcrição, presença online) na unidade.

## 3. Telas

- **Sessões** (DataTable): tipo, turma, professor, data, estado, gravação.
- **Configuração** (página): provedor de mídia, política de gravação e retenção, consentimento.
- **Gravações** (lista com acesso controlado e prazo de retenção).
- **Presença online** (relatório por sessão, integra o diário).

## 4. Permissões por portal (extraídas do SDD)

Do [40](../../../docs/v2/40-aulas-online-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Agendar sessões da unidade, criar e encerrar sala, ver presença consolidada, gerenciar permissão de gravação, ver relatórios e auditoria. **Diretor da unidade** entra em qualquer sessão da unidade, com passe livre. **Coordenador** entra para observar aulas da unidade. Ambos com registro em auditoria | Entrar em sala de aula sem ser moderador, convidado, diretor ou coordenador da unidade. Baixar gravação sem evento de auditoria | E |

## 5. Papéis

- `unit.manager`: política de gravação e retenção.
- `unit.coordinator`: acompanhar sessões e presença.
- `teacher`: criar e conduzir sessões (portal do professor).
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Gravação só com aviso e consentimento conforme a seção 13 (5).
- Presença online segue a regra da seção 13 (6) e alimenta o diário ([61](../../../docs/v2/61-diario-escolar-por-portal.md)).

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

### 13.1 [40 — Aulas Online e Reuniões ao Vivo, por Portal](../../../docs/v2/40-aulas-online-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Matriz de portais em [31](../../../docs/v2/31-matriz-portais-modulos.md). Portais e domínios em [23](../../../docs/v2/23-dominios-provisionamento-ciclo-de-vida.md). Presença e frequência em [17](../../../docs/v2/17-regras-modulos.md). Dado de menor, consentimento e gravação em [07](../../../docs/v2/07-privacidade-lgpd.md) e [26](../../../docs/v2/26-sdd-juridico-regulatorio.md). Gateway de IA em [27](../../../docs/v2/27-inteligencia-artificial-e-portais.md). Auditoria em [29](../../../docs/v2/29-auditoria.md). Retenção em [21](../../../docs/v2/21-busca-e-armazenamento.md). Pendências de acesso físico e geolocalização em [35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md), seção 9.
> **Status:** análise e especificação proposta, criada em 03/11/2026 a partir de [`global_meeting_spec_v2_complete.md`](../../../docs/v2/anexo-v1/global_meeting_spec_v2_complete.md) (620 linhas, v1) e das partes de chamada e EAD de [`spec_gestao_academica_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_academica_completo.md) (seção 8.3 e linhas 596–612). Itens **[Decisão do autor]** e **(jurídico)** dependem de resposta ou parecer. Não é parecer.

---

#### 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Aula online está especificada como módulo? | **Não.** A v1 não tem módulo de aula online. O único texto é a especificação genérica de reunião ao vivo, com um caso de uso "Live class" (seção 5.2) |
| Está organizada por portal? | **Não.** A especificação de reunião não conhece os seis portais. Usa papéis genéricos (`teacher`, `student`, `parent_guardian`, `guest`) e não diz o que cada um vê |
| Trata de menores? | **Não.** Aluno é tratado como adulto. Não há consentimento de responsável, nem bloqueio de gravação, nem limite de câmera |
| Gravação e transcrição têm regra de privacidade? | **Parcial.** Diz "sob permissão explícita" e "conforme política do tenant", sem padrão nem base legal |
| Presença em aula online é regra? | **Não.** Tem registro de entrada e saída, sem regra de frequência válida nem correção pelo professor |
| Infraestrutura de mídia é definida? | **Não na v2.** A v1 cita WebRTC, SFU, serviço de gravação e armazenamento de mídia, sem decisão de construir ou contratar |
| A v2 cita o módulo como especificado? | **Corrigir.** O catálogo ([12](../../../docs/v2/12-catalogo-modulos.md)) marca "Reunião global" como "Especificado", mas o arquivo é da v1 e não foi adaptado. Status correto: **especificação genérica, não aderente** |

---

#### 2. O que existe na v1

| Fonte | O que diz | Limite |
|---|---|---|
| [`global_meeting_spec_v2_complete.md`](../../../docs/v2/anexo-v1/global_meeting_spec_v2_complete.md) | Reunião, sala, chat, sala de espera, presença, gravação, transcrição, relatórios, auditoria, RBAC por tenant e unidade | Genérica. Não separa aula de reunião de pais, de reunião pedagógica e de reunião administrativa como regras diferentes |
| Mesmo arquivo, seção 5.2 | "Live class": professor abre sessão para um grupo de alunos, com controle de áudio, vídeo, chat e ordem de fala | Não diz quem pode entrar além da turma, nem o que acontece com aluno fora da turma |
| [`spec_gestao_academica_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_academica_completo.md), seção 8.3 | Chamada por QR Code, por geolocalização no modo EAD e por IP e horário de acesso ao "LMS" | Cita um LMS que não tem especificação. Geolocalização já está pendente em [35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md) (ACC-05) |
| [`spec_gestao_academica_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_academica_completo.md), Conselho de Classe | Campo `meeting_link` na reunião do conselho | Sem regra de acesso nem de gravação |
| [`12-portals-navigation-sidebar-pages-spec.md`](../../../docs/v2/anexo-v1/12-portals-navigation-sidebar-pages-spec.md) (v1) | "Calendário de Aulas" (professor), "Aulas e Conteúdos" (aluno), "Aulas de Hoje" (dashboard do professor) | Não há item de sala ao vivo na navegação. A aula é tratada como calendário e conteúdo |

**Conclusão:** a v1 tem a sala ao vivo (genérica) e o calendário de aulas, mas não liga os dois. Não há um lugar onde a aula online se encontre com a turma, a presença e o portal do aluno.

---

#### 3. Problemas encontrados

1. **Aluno tratado como adulto.** A v1 não exige consentimento do responsável para aula com menor, nem para gravação ou transcrição ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md): consentimento específico e em destaque, LGPD art. 14).
2. **Gravação por padrão do tenant.** A política de retenção é "por tenant", sem valor padrão. Uma escola sem configuração gravaria sem prazo.
3. **Transcrição sem freio.** A v1 gera transcrição "de áudio ao vivo, se habilitado". Não diz se a transcrição de aula com menores sai para um provedor de IA. Pela regra da v2 ([27](../../../docs/v2/27-inteligencia-artificial-e-portais.md)), dado de menor não sai do sistema sem finalidade e base definidas.
4. **Convidado sem regra de portal.** O papel `guest` existe na v1 (acesso por token assinado e expirável), mas não há portal para ele. Não se sabe quem é, o que vê nem por quanto tempo.
5. **Responsável sem limite.** O responsável entra em reunião 1:1 com o professor. Não há regra que impeça o acesso a sala de aula de outros alunos ou a gravação da turma.
6. **Presença por conexão.** A v1 registra tempo conectado e marca presença "manual ou automática". Tempo conectado não prova que o aluno assistiu.
7. **Câmera de aluno menor.** A v1 dá controle de vídeo ao professor, sem padrão de câmera desligada para alunos nem regra de exposição de imagem de menor a outros alunos.
8. **Dois sistemas de presença sem ponte.** A chamada presencial (QR, geolocalização) e a presença em aula online usam tabelas diferentes na v1. Não há regra de qual vale para a frequência oficial.
9. **Infraestrutura sem decisão.** SFU, serviço de gravação e armazenamento de mídia são descritos como unidades de implantação, sem dizer se a entidade contrata um provedor de vídeo ou se a plataforma opera a sua própria. Essa escolha muda o papel LGPD (operador) e o custo.
10. **Modelo de dados conflita com [03].** A v1 cria tabelas `tenants` e `users` no mesmo esquema da sala. Pela v2, cada entidade e unidade tem o seu banco, e a identidade fica no master ([03](../../../docs/v2/03-dominio-tenancy.md), seção 1.1). Essas tabelas devem sair do banco da unidade.
11. **Padrão visual não adotado.** A v1 pede interface escura estilo Supabase com verde-esmeralda. A v2 não define esse padrão em [08](../../../docs/v2/08-frontend-design-system.md). Decidir se a sala segue o padrão do portal ou um próprio.

---

#### 4. Modelo proposto

##### 4.1 Tipos de sessão

Cada sessão tem um tipo. O tipo define quem pode entrar, se pode gravar e se gera presença.

| Tipo | Quem entra | Gravação | Gera presença | Gera transcrição |
|---|---|---|---|---|
| Aula da turma | Professor e alunos da turma, com vínculo ativo | Desligada por padrão. Só com permissão da entidade e consentimento (seção 5) | Sim, pela regra da seção 6 | Desligada por padrão |
| Reunião professor e responsável | Professor e o responsável com vínculo ao aluno | Desligada por padrão. Só com consentimento do próprio responsável | Não | Desligada |
| Reunião pedagógica ou administrativa | Membros convidados da equipe | Só com permissão da gestão | Não | Só com aviso a todos |
| Convidado externo (palestra, banca) | Convidado com token de uso único, para uma só sessão | Só com aviso e permissão da gestão | Não | Não |

##### 4.2 Estados da sessão

`agendada` → `aberta` (sala liberada) → `em_andamento` → `encerrada`, com `cancelada` a partir de `agendada`. Sessão `encerrada` não reabre. Uma nova sessão é criada se a aula voltar.

##### 4.3 Entrada

- Entrada só com autenticação do portal, exceto o convidado externo, que entra com token.
- Sala de espera obrigatória para convidado e responsável. Aluno entra direto se estiver na lista da turma.
- Token de entrada assinado e com validade curta. Link de sessão não serve para outra sessão.
- Tentativa de entrada fora da turma ou do vínculo gera evento de segurança e é recusada.

---

##### 4.4 Interface da sala

**Decidido pelo autor em 03/11/2026.** A sala usa o template do portal, com a mesma identidade visual, e layout de reunião estilo Zoom:

- Grade de vídeo no centro, com destaque para quem fala.
- Painel lateral com participantes e chat, alternável.
- Barra superior de ação: microfone, câmera, compartilhar tela, levantar a mão, gravação e sair.
- Indicador visível de gravação e de sessão em andamento.

O estilo escuro com verde-esmeralda da v1 não é obrigatório. O template e os componentes da sala estão em [08](../../../docs/v2/08-frontend-design-system.md), seção 9.

---

#### 5. Gravação, transcrição e consentimento

**Regra padrão:** nenhuma sessão com aluno é gravada por padrão.

| Regra | Detalhe |
|---|---|
| Permissão | A entidade habilita a gravação por unidade. O professor inicia a gravação por sessão, com aviso visível na sala |
| Consentimento | Para aluno menor, consentimento do responsável, específico e registrado, antes da gravação ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md)). Sem consentimento, o aluno entra na aula sem ser gravado, ou não entra, conforme a regra da entidade **(jurídico)** |
| Aviso | Todos veem o aviso de gravação ao entrar, e o aviso fica visível enquanto ela durar |
| Acesso à gravação | Só a gestão e o professor da turma. Responsável vê só a gravação da própria sessão de reunião 1:1. Aluno não vê gravação de aula dos colegas |
| Download | Bloqueado por padrão. Quando habilitado, gera evento de auditoria ([29](../../../docs/v2/29-auditoria.md)) |
| Transcrição | Desligada por padrão. Pode ser enviada a provedor de IA, **decidido pelo autor em 03/11/2026**, sempre pelo gateway de IA ([27](../../../docs/v2/27-inteligencia-artificial-e-portais.md)), com registro da chamada. A entidade habilita por unidade. Só existe se a sessão tiver gravação permitida, conforme o consentimento da regra acima |
| Retenção | Padrão proposto: **30 dias** para gravação e transcrição, com expurgo automático. Valor a confirmar **(jurídico)** |
| Exclusão a pedido | Gravação e transcrição apagadas a pedido do titular ou do responsável, quando a lei permitir. Registro da exclusão sem o dado |

---

#### 6. Presença em aula online

A regra de presença precisa de três pontos: quem conta, quanto tempo conta e quem corrige.

| Regra | Proposta |
|---|---|
| Base | Presença conta com **40 minutos** de tempo conectado. O valor é configurável por entidade, com 40 minutos como padrão. Decidido pelo autor em 03/11/2026 |
| Interação | Além do tempo, o aluno registra presença ativa por uma das formas: resposta a pergunta de checagem, ou confirmação por código mostrado pelo professor. Sem interação, o sistema marca **presença pendente** |
| Presença pendente | Vira falta só após revisão do professor |
| Correção | O professor corrige com motivo. A correção vai para auditoria com antes e depois |
| Frequência oficial | A frequência oficial é o registro da chamada em [17](../../../docs/v2/17-regras-modulos.md), com a presença online como uma das origens. Origem fica registrada no registro de frequência |
| Geolocalização | Não usada para aula online. A v1 propõe GPS para EAD. Pendente em [35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md), ACC-05 |
| Câmera | Aluno entra com câmera desligada por padrão. O professor não obriga câmera ligada, por ser dado de imagem de menor sem finalidade pedagógica |

---

#### 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Ver saúde técnica da plataforma: uso de sala, falhas de conexão, filas de gravação, sem identidade nem conteúdo | Entrar em sala, ver gravação, ver transcrição, ver nome de participante | P |
| **Gestão** | Agendar sessões da unidade, criar e encerrar sala, ver presença consolidada, gerenciar permissão de gravação, ver relatórios e auditoria. **Diretor da unidade** entra em qualquer sessão da unidade, com passe livre. **Coordenador** entra para observar aulas da unidade. Ambos com registro em auditoria | Entrar em sala de aula sem ser moderador, convidado, diretor ou coordenador da unidade. Baixar gravação sem evento de auditoria | E |
| **Professor** | Criar e conduzir aula da própria turma, controlar microfone, câmera e chat, admitir da sala de espera, iniciar gravação com permissão, corrigir presença com motivo | Criar sessão para turma que não leciona, ver aula de outra turma, baixar gravação sem permissão | E |
| **Aluno** | Entrar na aula da própria turma no horário, ver a própria presença, ver a gravação quando liberada pela entidade | Entrar em turma sem vínculo, ver lista de participantes além do próprio nome, ver gravação de colegas, gravar, baixar | E |
| **Responsáveis** | Entrar na reunião 1:1 com o professor do próprio dependente, ver a própria gravação de reunião, receber aviso de sessão | Entrar em aula de turma, ver presença da turma, ver dado de outro aluno, entrar sem sala de espera | E, só dependentes com vínculo ativo |
| **Terceiros** | Ver integração técnica com o provedor de vídeo, se a entidade contratar um, sem conteúdo de sessão | Ver sessão, participante, gravação ou transcrição | E, pelo contrato de integração ([38](../../../docs/v2/38-portal-de-terceiros-prestadores.md)) |
| **Convidado externo** | Entrar em uma sessão com token de uso único, se a entidade habilitar a opção de externos | Ver outras sessões, o portal da entidade, ou dados de participantes | Fora dos seis portais. Decidido pelo autor em 03/11/2026: a entidade pode habilitar externos |

**Regra de isolamento:** um portal nunca recebe dado de sessão de outra turma, de outra unidade ou de outra entidade. Teste de varredura de resposta por papel.

---

#### 8. Infraestrutura de mídia

| Opção | Descrição | Efeito |
|---|---|---|
| A. Provedor de vídeo contratado | A entidade ou a plataforma contrata um provedor de vídeo, com contrato de operador | Menos operação. Exige contrato de operador com cláusulas de dado de menor e de localização dos dados **(jurídico)** |
| B. Própria mídia | Plataforma opera SFU e gravação próprios | Mais controle. Exige operação de mídia, monitoramento e custo de infraestrutura, que a v2 ainda não especifica ([10](../../../docs/v2/10-implantacao-operacao.md)) |

**Decidido pelo autor em 03/11/2026: opção B, mídia própria, com as melhores tecnologias disponíveis.** A plataforma opera a sua própria SFU, o serviço de gravação e o armazenamento de mídia. A escolha de cada componente open source é feita em homologação, com critério de maturidade, segurança e desempenho, e registrada em [10](../../../docs/v2/10-implantacao-operacao.md). Consequências:

- A plataforma passa a ser a operadora direta do dado de sessão. Cifração em trânsito e em repouso, isolamento de mídia por entidade e unidade, e registro de acesso são obrigatórios desde o primeiro lançamento ([05](../../../docs/v2/05-seguranca.md)).
- Operação de mídia (SFU, gravação em fragmentos, armazenamento, capacidade e monitoramento) está especificada em [10](../../../docs/v2/10-implantacao-operacao.md), seção 10.
- As integrações de mídia saem de [16](../../../docs/v2/16-integracoes-externas.md) e passam a ser componentes internos. Cabe um contrato de operador só se algum componente de terceiro for usado.
- Gravação fica sob a mesma guarda de [21](../../../docs/v2/21-busca-e-armazenamento.md) para arquivos. O expurgo automático da seção 5 precisa rodar no armazenamento de mídia.

---

#### 9. Correções nos documentos

Correções abaixo. A de [12](../../../docs/v2/12-catalogo-modulos.md) já foi aplicada. As demais são propostas e dependem da aprovação do autor.

| Onde | Correção |
|---|---|
| [12](../../../docs/v2/12-catalogo-modulos.md), linha "Reunião global" | Trocar "Especificado" por "Especificação genérica da v1. Aderente só após [40](../../../docs/v2/40-aulas-online-por-portal.md)" |
| [31](../../../docs/v2/31-matriz-portais-modulos.md), matriz por portal | Incluir a aula online como módulo de entidade (E), ligado à turma e não ao módulo de comunicação |
| [28](../../../docs/v2/28-cobertura-ia-todos-os-modulos.md) | Marcar aula online e reunião como **Não** para transcrição e resumo de sessão com menor, até parecer |
| [`global_meeting_spec_v2_complete.md`](../../../docs/v2/anexo-v1/global_meeting_spec_v2_complete.md) (v1) | Não editar. Este documento substitui a parte de aula. A parte de reunião administrativa segue a v1 com as regras da seção 4 |

---

#### 10. Pendências

| # | Pendência | Tipo |
|---|---|---|
| LIV-01 | Consentimento de responsável para gravação e para entrada de aluno menor sem gravação (seção 5). Pedido por cláusula do contrato com a instituição | (jurídico). Texto da cláusula a cargo do jurídico |
| LIV-02 | Prazo de retenção de gravação e transcrição, padrão 30 dias (seção 5) | (jurídico). Padrão de 30 dias até parecer |
| LIV-03 | Transcrição de aula com menor pode sair para provedor de IA (seção 5) | **Decidido: sim**, pelo gateway de IA. Consentimento (LIV-01) continua valendo |
| LIV-04 | Tempo conectado para presença (seção 6) | **Decidido: 40 minutos**, configurável por entidade |
| LIV-05 | Infraestrutura de mídia (seção 8) | **Decidido: mídia própria**, com as melhores tecnologias |
| LIV-11 | Operação de mídia: SFU, gravação em fragmentos, armazenamento e mapeamento | **Feito:** [10](../../../docs/v2/10-implantacao-operacao.md), seção 10 |
| LIV-06 | Convidado externo (seção 7) | **Decidido:** a entidade habilita a opção. Quem entra usa token de uso único |
| LIV-07 | Coordenador entra em aula para observar (seção 7) | **Decidido:** sim, com registro em auditoria |
| LIV-08 | Padrão visual da sala (seção 4.4) | **Decidido:** template do portal, layout de reunião |
| LIV-12 | Template e componentes da sala | **Feito:** [08](../../../docs/v2/08-frontend-design-system.md), seção 9 |
| LIV-13 | Valores de capacidade: fragmento de 60 segundos (**decidido** em 03/11/2026), bitrate, salas por nó e limite de perda de pacote | Medir em homologação e registrar em [10](../../../docs/v2/10-implantacao-operacao.md), seção 10 |
| LIV-09 | Geolocalização em EAD (seção 6) | **Decidido** em 03/11/2026 por ACC-05 de [35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md): a escola configura |
| LIV-10 | Modelo de dados da sala, sem tabelas `tenants` e `users` no banco da unidade | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 9. Revisão do owner pendente (DDL-01) |

---

#### 11. Critérios de aceite

- [ ] Aluno de turma A não entra em sessão da turma B (teste de isolamento).
- [ ] Sessão com aluno menor não grava sem consentimento registrado (teste).
- [ ] Transcrição desligada por padrão; sessão com menor não envia dado a provedor de IA sem parecer (teste).
- [ ] Câmera do aluno começa desligada (teste).
- [ ] Responsável não entra em aula de turma e não vê presença de outros alunos (teste de varredura).
- [ ] Gravação baixada gera evento de auditoria com motivo (teste).
- [ ] Presença pendente não vira falta sem revisão do professor (teste).
- [ ] Token de convidado expira e não serve para outra sessão (teste).
- [ ] Itens **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).

## 14. Conteúdo integral da v1 (absorvido)

### SPEC v2 — Global Meeting & Live Streaming Platform

**Product:** TotusTuusSoftCloud  
**Template:** Supabase-style UI/UX  
**Language:** Global English  
**Version:** 2.0.0  
**Status:** Complete technical specification

#### 1. Executive Summary

This module delivers a secure, scalable, global real-time meeting and live streaming platform for education and institutional communication. It supports teacher-parent meetings, live classes, pedagogical meetings, internal administrative sessions, one-to-one conversations, webinars, and hybrid events.

The specification assumes an enterprise SaaS environment with multi-tenant isolation, per-unit access control, strict auditability, and international naming standards. All technical artifacts must follow English naming, `snake_case` database conventions, and Supabase-inspired UI patterns.

#### 2. Product Principles

- Global English first.
- Security by default.
- Privacy by design.
- Multi-tenant isolation.
- Scalable real-time architecture.
- Education-friendly UX.
- Auditability for every sensitive action.
- Open standards and vendor-neutral design.

#### 3. Scope

##### 3.1 Included

- Meeting creation and scheduling.
- Instant and recurring sessions.
- Live audio and video.
- Screen sharing.
- Chat and attachments.
- Waiting room and host moderation.
- Presence and attendance tracking.
- Recording and transcript generation.
- Reports and audit logs.
- Notifications and reminders.
- Admin policies and retention controls.

##### 3.2 Excluded in this version

- Native mobile apps.
- Advanced AI meeting agent.
- External marketplace integrations.
- Full white-label domain routing.
- Hardware room system integration.

#### 4. Roles and Actors

- `system_admin`
- `tenant_admin`
- `unit_admin`
- `coordinator`
- `teacher`
- `student`
- `parent_guardian`
- `moderator`
- `guest`

#### 5. Business Use Cases

##### 5.1 Teacher and parent meeting

A teacher schedules a one-to-one meeting with a parent or guardian, shares a secure access link, and controls entry through a waiting room. The system records attendance, duration, and optional notes.

##### 5.2 Live class

A teacher opens a class session for a specific group of students. Students join with role-based permissions, and the teacher controls audio, video, chat, screen sharing, and participation order.

##### 5.3 Pedagogical session

A coordinator schedules a meeting with multiple teachers to discuss planning, student performance, or institutional topics. Notes, files, and outcomes can be attached to the session record.

##### 5.4 Internal meeting

An internal meeting supports administrative work, policy discussion, operational planning, and sensitive coordination inside the institution.

#### 6. Functional Requirements

##### 6.1 Meeting management

- Create, edit, cancel, restore, and duplicate meetings.
- Support one-time and recurring meetings.
- Support meeting templates.
- Support meeting categories and tags.
- Allow host, co-host, moderator, and participant roles.
- Support default rules by tenant and unit.

##### 6.2 Access control

- Require authentication for internal users.
- Allow external access only with signed, expiring tokens.
- Support manual approval from waiting room.
- Block unauthorized reuse of join links.
- Prevent cross-tenant access.
- Apply unit-level restrictions when configured.

##### 6.3 Live communication

- Audio streaming.
- Video streaming.
- Adaptive quality switching.
- Screen sharing.
- File sharing.
- Public and private chat.
- Reactions.
- Raise hand.
- Presenter spotlight.
- Host controls.

##### 6.4 Attendance and participation

- Track join time, leave time, and total connected time.
- Mark attendance manually or automatically.
- Distinguish viewer, speaker, and presenter participation.
- Export attendance reports.
- Record participation events for compliance.

##### 6.5 Recording and transcript

- Start and stop recording under explicit permission.
- Store recordings securely.
- Generate transcript from recorded or live audio if enabled.
- Link transcript to the meeting record.
- Support retention and deletion policies.

##### 6.6 Notifications

- Meeting invitation email.
- Reminder before start.
- Join confirmation.
- Meeting started notice.
- Meeting ended notice.
- Recording available notice.
- Transcript ready notice.

#### 7. Non-Functional Requirements

- Low latency in real-time communication.
- Horizontal scalability.
- High availability.
- Graceful reconnection.
- Browser compatibility.
- Mobile responsive web support.
- Secure media transport.
- Strong observability.
- International time zone support.
- Operational resilience under load.

#### 8. UI/UX Requirements

##### 8.1 Visual system

- Supabase-style dark-first interface.
- Emerald accent color.
- Minimal cards and clean tables.
- Collapsible navigation groups.
- Strong empty states.
- Compact action bars.
- Consistent status badges.

##### 8.2 Screen structure

- Dashboard.
- Meetings list.
- Calendar view.
- Create meeting.
- Meeting details.
- Live meeting room.
- Participants panel.
- Recordings library.
- Transcript page.
- Reports page.
- Settings and policies.
- Audit logs.

##### 8.3 Live room layout

- Main video grid.
- Active speaker focus.
- Side panel for chat and participants.
- Top action bar.
- Status indicators.
- Responsive mobile fallback.

#### 9. System Architecture

##### 9.1 High-level layers

- Presentation layer.
- Application layer.
- API layer.
- Realtime signaling layer.
- Media layer.
- Recording pipeline.
- Notification pipeline.
- Storage layer.
- Audit and analytics layer.

##### 9.2 Media architecture

- WebRTC for media transport.
- SFU for group sessions.
- Optional P2P for very small sessions.
- Signaling over secure WebSocket or equivalent.
- Recording as asynchronous media job.
- Separate storage for artifacts and metadata.

##### 9.3 Suggested deployment units

- API service.
- Realtime signaling service.
- Media gateway service.
- Recording worker service.
- Notification worker service.
- Audit/logging service.
- Database cluster.
- Object storage for media.

#### 10. Domain Model

##### 10.1 Core entities

- `tenants`
- `units`
- `users`
- `user_memberships`
- `meetings`
- `meeting_templates`
- `meeting_rules`
- `meeting_invites`
- `meeting_participants`
- `meeting_rooms`
- `meeting_sessions`
- `meeting_presence`
- `meeting_chat_messages`
- `meeting_attachments`
- `meeting_reactions`
- `meeting_polls`
- `meeting_whiteboards`
- `meeting_recordings`
- `meeting_transcripts`
- `meeting_audit_logs`
- `meeting_exports`

##### 10.2 Identifier strategy

- `id`: internal technical primary key.
- `uuid`: public external identifier.
- `code`: human-readable business code.

##### 10.3 Core meeting fields

- `id`
- `uuid`
- `code`
- `tenant_id`
- `unit_id`
- `created_by_user_id`
- `host_user_id`
- `meeting_type`
- `title`
- `description`
- `scheduled_start_at`
- `scheduled_end_at`
- `actual_start_at`
- `actual_end_at`
- `timezone`
- `status`
- `visibility`
- `access_policy`
- `waiting_room_enabled`
- `chat_enabled`
- `screen_share_enabled`
- `recording_enabled`
- `transcript_enabled`
- `max_participants`
- `created_at`
- `updated_at`
- `deleted_at`

#### 11. Database Design

##### 11.1 Recommended schema rules

- Use English names only.
- Use `snake_case` consistently.
- Add indexes for tenant scope, status, scheduled time, and public UUID.
- Use soft delete where operationally useful.
- Use timestamps in UTC.
- Keep audit tables append-only.

##### 11.2 Example tables

###### `meetings`

- `id` bigint unsigned primary key.
- `uuid` char(36) unique.
- `code` varchar(50) unique.
- `tenant_id` bigint unsigned indexed.
- `unit_id` bigint unsigned nullable indexed.
- `created_by_user_id` bigint unsigned.
- `host_user_id` bigint unsigned.
- `meeting_type` varchar(50).
- `title` varchar(255).
- `description` text.
- `scheduled_start_at` datetime.
- `scheduled_end_at` datetime.
- `actual_start_at` datetime nullable.
- `actual_end_at` datetime nullable.
- `timezone` varchar(64).
- `status` varchar(30).
- `visibility` varchar(30).
- `access_policy` varchar(30).
- `waiting_room_enabled` tinyint(1).
- `chat_enabled` tinyint(1).
- `screen_share_enabled` tinyint(1).
- `recording_enabled` tinyint(1).
- `transcript_enabled` tinyint(1).
- `max_participants` int unsigned.
- `created_at` datetime.
- `updated_at` datetime.
- `deleted_at` datetime nullable.

###### `meeting_participants`

- `id` bigint unsigned primary key.
- `uuid` char(36) unique.
- `meeting_id` bigint unsigned indexed.
- `user_id` bigint unsigned nullable.
- `display_name` varchar(255).
- `email` varchar(255) nullable.
- `role` varchar(30).
- `join_status` varchar(30).
- `joined_at` datetime nullable.
- `left_at` datetime nullable.
- `mute_state` varchar(30).
- `camera_state` varchar(30).
- `hand_raised` tinyint(1).
- `attendance_state` varchar(30).
- `created_at` datetime.
- `updated_at` datetime.

###### `meeting_recordings`

- `id` bigint unsigned primary key.
- `uuid` char(36) unique.
- `meeting_id` bigint unsigned indexed.
- `storage_provider` varchar(50).
- `storage_path` varchar(500).
- `file_name` varchar(255).
- `mime_type` varchar(100).
- `file_size` bigint unsigned.
- `duration_seconds` int unsigned.
- `status` varchar(30).
- `created_at` datetime.
- `updated_at` datetime.

###### `meeting_audit_logs`

- `id` bigint unsigned primary key.
- `uuid` char(36) unique.
- `tenant_id` bigint unsigned indexed.
- `meeting_id` bigint unsigned nullable indexed.
- `actor_user_id` bigint unsigned nullable indexed.
- `event_type` varchar(100).
- `event_name` varchar(100).
- `event_payload` json.
- `ip_address` varchar(45).
- `user_agent` varchar(255).
- `created_at` datetime.

#### 12. API Specification

##### 12.1 Meetings

- `POST /api/v1/meetings`
- `GET /api/v1/meetings`
- `GET /api/v1/meetings/{uuid}`
- `PATCH /api/v1/meetings/{uuid}`
- `DELETE /api/v1/meetings/{uuid}`
- `POST /api/v1/meetings/{uuid}/duplicate`
- `POST /api/v1/meetings/{uuid}/start`
- `POST /api/v1/meetings/{uuid}/end`
- `POST /api/v1/meetings/{uuid}/cancel`

##### 12.2 Participation

- `POST /api/v1/meetings/{uuid}/join-token`
- `POST /api/v1/meetings/{uuid}/join`
- `POST /api/v1/meetings/{uuid}/leave`
- `GET /api/v1/meetings/{uuid}/participants`
- `PATCH /api/v1/meetings/{uuid}/participants/{participant_uuid}`
- `DELETE /api/v1/meetings/{uuid}/participants/{participant_uuid}`

##### 12.3 Realtime collaboration

- `POST /api/v1/meetings/{uuid}/chat/messages`
- `GET /api/v1/meetings/{uuid}/chat/messages`
- `POST /api/v1/meetings/{uuid}/screen-share/start`
- `POST /api/v1/meetings/{uuid}/screen-share/stop`
- `POST /api/v1/meetings/{uuid}/reactions`
- `POST /api/v1/meetings/{uuid}/polls`

##### 12.4 Recording and transcript

- `POST /api/v1/meetings/{uuid}/recordings/start`
- `POST /api/v1/meetings/{uuid}/recordings/stop`
- `GET /api/v1/meetings/{uuid}/recordings`
- `GET /api/v1/meetings/{uuid}/transcript`
- `POST /api/v1/meetings/{uuid}/transcript/generate`

##### 12.5 Reports and audit

- `GET /api/v1/meetings/{uuid}/report`
- `GET /api/v1/meetings/{uuid}/presence`
- `GET /api/v1/meetings/{uuid}/audit-logs`
- `GET /api/v1/meetings/{uuid}/exports`

#### 13. Realtime Event Contract

##### 13.1 Event channels

- `meeting.joined`
- `meeting.left`
- `meeting.started`
- `meeting.ended`
- `meeting.chat_message.created`
- `meeting.participant.muted`
- `meeting.participant.kicked`
- `meeting.reaction.created`
- `meeting.hand_raised`
- `meeting.recording.started`
- `meeting.recording.stopped`
- `meeting.transcript.ready`

##### 13.2 Payload standards

- Use JSON.
- Include `tenant_uuid`, `meeting_uuid`, `actor_uuid`, `event_name`, `created_at`.
- Keep payloads minimal and versioned.
- Never expose internal secrets in events.

#### 14. Security Specification

##### 14.1 Authentication

- Use secure token-based auth.
- Support MFA for privileged roles.
- Session hardening for internal users.
- Optional SSO integration.

##### 14.2 Authorization

- Enforce RBAC and tenant scope.
- Support policy checks by role and context.
- Protect all admin and moderation actions.

##### 14.3 Media security

- Encrypt media transport.
- Sign room join tokens.
- Limit token lifetime.
- Restrict access to recordings.
- Control download permissions.

##### 14.4 Abuse prevention

- Rate limiting.
- Bot protection on public joins.
- Chat moderation and profanity filtering if enabled.
- Suspicious activity logs.

#### 15. Privacy and Compliance

- Consent-based recording policies.
- Data retention policies by tenant.
- Right-to-access support.
- Right-to-delete support where legally allowed.
- Audit trails for sensitive actions.
- Configurable regional policy packs.

#### 16. Storage and Retention

##### 16.1 Storage types

- Metadata in relational database.
- Media files in object storage.
- Logs in append-only audit store.
- Transcripts in searchable text storage.

##### 16.2 Retention defaults

- Meeting metadata: per tenant policy.
- Recordings: per tenant policy.
- Transcripts: per tenant policy.
- Audit logs: long-term retention.

#### 17. Error Handling

- Invalid token.
- Expired join link.
- Meeting not found.
- Meeting not started.
- Room full.
- User not authorized.
- Recording unavailable.
- Network interruption.
- Media negotiation failure.

All errors must return structured English messages and machine-readable codes.

#### 18. Observability

- Application logs.
- Security logs.
- Audit logs.
- Metrics for join success, video quality, participant counts, and recording status.
- Alerting for downtime or session failures.

#### 19. Testing Requirements

- Unit tests for domain rules.
- Integration tests for APIs.
- Realtime event tests.
- Authorization tests.
- Load tests for concurrent sessions.
- Browser compatibility tests.
- Recovery tests for disconnection and reconnection.
- Security validation tests.

#### 20. Deployment Requirements

- Separate environments for development, staging, and production.
- Feature flags for recording, transcript, and AI functions.
- Rolling deployment support.
- Health checks for each service.
- Backup and restore strategy.
- Object storage lifecycle rules.

#### 21. Project Structure

##### 21.1 Suggested folders

- `app/`
- `app/modules/meeting/`
- `app/modules/meeting/controllers/`
- `app/modules/meeting/services/`
- `app/modules/meeting/repositories/`
- `app/modules/meeting/models/`
- `app/modules/meeting/events/`
- `app/modules/meeting/policies/`
- `app/modules/meeting/views/`
- `core/`
- `config/`
- `routes/`
- `storage/`
- `docs/`
- `tests/`

#### 22. Acceptance Criteria

- All UI, database, and API names are in English.
- The interface follows Supabase-style design principles.
- Meetings can be created, scheduled, joined, moderated, recorded, and reported.
- The module supports education workflows end to end.
- Tenant isolation is enforced everywhere.
- Audit trails are complete.
- The system is ready for global deployment.

#### 23. Delivery Checklist

- DDL script.
- API contract.
- Realtime event contract.
- UI screens.
- Security checklist.
- Compliance checklist.
- Test plan.
- Deployment checklist.
- Logging and monitoring checklist.
- Documentation index.

#### 24. Appendix — Recommended Enums

##### `meeting_status`

- `draft`
- `scheduled`
- `live`
- `ended`
- `canceled`
- `archived`

##### `participant_role`

- `host`
- `co_host`
- `moderator`
- `speaker`
- `listener`
- `guest`

##### `access_policy`

- `private`
- `tenant_only`
- `invite_only`
- `token_required`
- `public_link`

##### `join_status`

- `waiting`
- `approved`
- `joined`
- `rejected`
- `left`
