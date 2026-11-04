# 40 — Aulas Online e Reuniões ao Vivo, por Portal

> Parte do [SDD v2](00-README.md). Matriz de portais em [31](31-matriz-portais-modulos.md). Portais e domínios em [23](23-dominios-provisionamento-ciclo-de-vida.md). Presença e frequência em [17](17-regras-modulos.md). Dado de menor, consentimento e gravação em [07](07-privacidade-lgpd.md) e [26](26-sdd-juridico-regulatorio.md). Gateway de IA em [27](27-inteligencia-artificial-e-portais.md). Auditoria em [29](29-auditoria.md). Retenção em [21](21-busca-e-armazenamento.md). Pendências de acesso físico e geolocalização em [35](35-acesso-e-seguranca-fisica-por-portal.md), seção 9.
> **Status:** análise e especificação proposta, criada em 03/11/2026 a partir de `global_meeting_spec_v2_complete.md` (620 linhas, v1) e das partes de chamada e EAD de `spec_gestao_academica_completo.md` (seção 8.3 e linhas 596–612). Itens **[Decisão do autor]** e **(jurídico)** dependem de resposta ou parecer. Não é parecer.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Aula online está especificada como módulo? | **Não.** A v1 não tem módulo de aula online. O único texto é a especificação genérica de reunião ao vivo, com um caso de uso "Live class" (seção 5.2) |
| Está organizada por portal? | **Não.** A especificação de reunião não conhece os seis portais. Usa papéis genéricos (`teacher`, `student`, `parent_guardian`, `guest`) e não diz o que cada um vê |
| Trata de menores? | **Não.** Aluno é tratado como adulto. Não há consentimento de responsável, nem bloqueio de gravação, nem limite de câmera |
| Gravação e transcrição têm regra de privacidade? | **Parcial.** Diz "sob permissão explícita" e "conforme política do tenant", sem padrão nem base legal |
| Presença em aula online é regra? | **Não.** Tem registro de entrada e saída, sem regra de frequência válida nem correção pelo professor |
| Infraestrutura de mídia é definida? | **Não na v2.** A v1 cita WebRTC, SFU, serviço de gravação e armazenamento de mídia, sem decisão de construir ou contratar |
| A v2 cita o módulo como especificado? | **Corrigir.** O catálogo ([12](12-catalogo-modulos.md)) marca "Reunião global" como "Especificado", mas o arquivo é da v1 e não foi adaptado. Status correto: **especificação genérica, não aderente** |

---

## 2. O que existe na v1

| Fonte | O que diz | Limite |
|---|---|---|
| `global_meeting_spec_v2_complete.md` | Reunião, sala, chat, sala de espera, presença, gravação, transcrição, relatórios, auditoria, RBAC por tenant e unidade | Genérica. Não separa aula de reunião de pais, de reunião pedagógica e de reunião administrativa como regras diferentes |
| Mesmo arquivo, seção 5.2 | "Live class": professor abre sessão para um grupo de alunos, com controle de áudio, vídeo, chat e ordem de fala | Não diz quem pode entrar além da turma, nem o que acontece com aluno fora da turma |
| `spec_gestao_academica_completo.md`, seção 8.3 | Chamada por QR Code, por geolocalização no modo EAD e por IP e horário de acesso ao "LMS" | Cita um LMS que não tem especificação. Geolocalização já está pendente em [35](35-acesso-e-seguranca-fisica-por-portal.md) (ACC-05) |
| `spec_gestao_academica_completo.md`, Conselho de Classe | Campo `meeting_link` na reunião do conselho | Sem regra de acesso nem de gravação |
| `12-portals-navigation-sidebar-pages-spec.md` (v1) | "Calendário de Aulas" (professor), "Aulas e Conteúdos" (aluno), "Aulas de Hoje" (dashboard do professor) | Não há item de sala ao vivo na navegação. A aula é tratada como calendário e conteúdo |

**Conclusão:** a v1 tem a sala ao vivo (genérica) e o calendário de aulas, mas não liga os dois. Não há um lugar onde a aula online se encontre com a turma, a presença e o portal do aluno.

---

## 3. Problemas encontrados

1. **Aluno tratado como adulto.** A v1 não exige consentimento do responsável para aula com menor, nem para gravação ou transcrição ([26](26-sdd-juridico-regulatorio.md): consentimento específico e em destaque, LGPD art. 14).
2. **Gravação por padrão do tenant.** A política de retenção é "por tenant", sem valor padrão. Uma escola sem configuração gravaria sem prazo.
3. **Transcrição sem freio.** A v1 gera transcrição "de áudio ao vivo, se habilitado". Não diz se a transcrição de aula com menores sai para um provedor de IA. Pela regra da v2 ([27](27-inteligencia-artificial-e-portais.md)), dado de menor não sai do sistema sem finalidade e base definidas.
4. **Convidado sem regra de portal.** O papel `guest` existe na v1 (acesso por token assinado e expirável), mas não há portal para ele. Não se sabe quem é, o que vê nem por quanto tempo.
5. **Responsável sem limite.** O responsável entra em reunião 1:1 com o professor. Não há regra que impeça o acesso a sala de aula de outros alunos ou a gravação da turma.
6. **Presença por conexão.** A v1 registra tempo conectado e marca presença "manual ou automática". Tempo conectado não prova que o aluno assistiu.
7. **Câmera de aluno menor.** A v1 dá controle de vídeo ao professor, sem padrão de câmera desligada para alunos nem regra de exposição de imagem de menor a outros alunos.
8. **Dois sistemas de presença sem ponte.** A chamada presencial (QR, geolocalização) e a presença em aula online usam tabelas diferentes na v1. Não há regra de qual vale para a frequência oficial.
9. **Infraestrutura sem decisão.** SFU, serviço de gravação e armazenamento de mídia são descritos como unidades de implantação, sem dizer se a entidade contrata um provedor de vídeo ou se a plataforma opera a sua própria. Essa escolha muda o papel LGPD (operador) e o custo.
10. **Modelo de dados conflita com [03].** A v1 cria tabelas `tenants` e `users` no mesmo esquema da sala. Pela v2, cada entidade e unidade tem o seu banco, e a identidade fica no master ([03](03-dominio-tenancy.md), seção 1.1). Essas tabelas devem sair do banco da unidade.
11. **Padrão visual não adotado.** A v1 pede interface escura estilo Supabase com verde-esmeralda. A v2 não define esse padrão em [08](08-frontend-design-system.md). Decidir se a sala segue o padrão do portal ou um próprio.

---

## 4. Modelo proposto

### 4.1 Tipos de sessão

Cada sessão tem um tipo. O tipo define quem pode entrar, se pode gravar e se gera presença.

| Tipo | Quem entra | Gravação | Gera presença | Gera transcrição |
|---|---|---|---|---|
| Aula da turma | Professor e alunos da turma, com vínculo ativo | Desligada por padrão. Só com permissão da entidade e consentimento (seção 5) | Sim, pela regra da seção 6 | Desligada por padrão |
| Reunião professor e responsável | Professor e o responsável com vínculo ao aluno | Desligada por padrão. Só com consentimento do próprio responsável | Não | Desligada |
| Reunião pedagógica ou administrativa | Membros convidados da equipe | Só com permissão da gestão | Não | Só com aviso a todos |
| Convidado externo (palestra, banca) | Convidado com token de uso único, para uma só sessão | Só com aviso e permissão da gestão | Não | Não |

### 4.2 Estados da sessão

`agendada` → `aberta` (sala liberada) → `em_andamento` → `encerrada`, com `cancelada` a partir de `agendada`. Sessão `encerrada` não reabre. Uma nova sessão é criada se a aula voltar.

### 4.3 Entrada

- Entrada só com autenticação do portal, exceto o convidado externo, que entra com token.
- Sala de espera obrigatória para convidado e responsável. Aluno entra direto se estiver na lista da turma.
- Token de entrada assinado e com validade curta. Link de sessão não serve para outra sessão.
- Tentativa de entrada fora da turma ou do vínculo gera evento de segurança e é recusada.

---

### 4.4 Interface da sala

**Decidido pelo autor em 03/11/2026.** A sala usa o template do portal, com a mesma identidade visual, e layout de reunião estilo Zoom:

- Grade de vídeo no centro, com destaque para quem fala.
- Painel lateral com participantes e chat, alternável.
- Barra superior de ação: microfone, câmera, compartilhar tela, levantar a mão, gravação e sair.
- Indicador visível de gravação e de sessão em andamento.

O estilo escuro com verde-esmeralda da v1 não é obrigatório. O template e os componentes da sala estão em [08](08-frontend-design-system.md), seção 9.

---

## 5. Gravação, transcrição e consentimento

**Regra padrão:** nenhuma sessão com aluno é gravada por padrão.

| Regra | Detalhe |
|---|---|
| Permissão | A entidade habilita a gravação por unidade. O professor inicia a gravação por sessão, com aviso visível na sala |
| Consentimento | Para aluno menor, consentimento do responsável, específico e registrado, antes da gravação ([26](26-sdd-juridico-regulatorio.md)). Sem consentimento, o aluno entra na aula sem ser gravado, ou não entra, conforme a regra da entidade **(jurídico)** |
| Aviso | Todos veem o aviso de gravação ao entrar, e o aviso fica visível enquanto ela durar |
| Acesso à gravação | Só a gestão e o professor da turma. Responsável vê só a gravação da própria sessão de reunião 1:1. Aluno não vê gravação de aula dos colegas |
| Download | Bloqueado por padrão. Quando habilitado, gera evento de auditoria ([29](29-auditoria.md)) |
| Transcrição | Desligada por padrão. Pode ser enviada a provedor de IA, **decidido pelo autor em 03/11/2026**, sempre pelo gateway de IA ([27](27-inteligencia-artificial-e-portais.md)), com registro da chamada. A entidade habilita por unidade. Só existe se a sessão tiver gravação permitida, conforme o consentimento da regra acima |
| Retenção | Padrão proposto: **30 dias** para gravação e transcrição, com expurgo automático. Valor a confirmar **(jurídico)** |
| Exclusão a pedido | Gravação e transcrição apagadas a pedido do titular ou do responsável, quando a lei permitir. Registro da exclusão sem o dado |

---

## 6. Presença em aula online

A regra de presença precisa de três pontos: quem conta, quanto tempo conta e quem corrige.

| Regra | Proposta |
|---|---|
| Base | Presença conta com **40 minutos** de tempo conectado. O valor é configurável por entidade, com 40 minutos como padrão. Decidido pelo autor em 03/11/2026 |
| Interação | Além do tempo, o aluno registra presença ativa por uma das formas: resposta a pergunta de checagem, ou confirmação por código mostrado pelo professor. Sem interação, o sistema marca **presença pendente** |
| Presença pendente | Vira falta só após revisão do professor |
| Correção | O professor corrige com motivo. A correção vai para auditoria com antes e depois |
| Frequência oficial | A frequência oficial é o registro da chamada em [17](17-regras-modulos.md), com a presença online como uma das origens. Origem fica registrada no registro de frequência |
| Geolocalização | Não usada para aula online. A v1 propõe GPS para EAD. Pendente em [35](35-acesso-e-seguranca-fisica-por-portal.md), ACC-05 |
| Câmera | Aluno entra com câmera desligada por padrão. O professor não obriga câmera ligada, por ser dado de imagem de menor sem finalidade pedagógica |

---

## 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Ver saúde técnica da plataforma: uso de sala, falhas de conexão, filas de gravação, sem identidade nem conteúdo | Entrar em sala, ver gravação, ver transcrição, ver nome de participante | P |
| **Gestão** | Agendar sessões da unidade, criar e encerrar sala, ver presença consolidada, gerenciar permissão de gravação, ver relatórios e auditoria. **Diretor da unidade** entra em qualquer sessão da unidade, com passe livre. **Coordenador** entra para observar aulas da unidade. Ambos com registro em auditoria | Entrar em sala de aula sem ser moderador, convidado, diretor ou coordenador da unidade. Baixar gravação sem evento de auditoria | E |
| **Professor** | Criar e conduzir aula da própria turma, controlar microfone, câmera e chat, admitir da sala de espera, iniciar gravação com permissão, corrigir presença com motivo | Criar sessão para turma que não leciona, ver aula de outra turma, baixar gravação sem permissão | E |
| **Aluno** | Entrar na aula da própria turma no horário, ver a própria presença, ver a gravação quando liberada pela entidade | Entrar em turma sem vínculo, ver lista de participantes além do próprio nome, ver gravação de colegas, gravar, baixar | E |
| **Responsáveis** | Entrar na reunião 1:1 com o professor do próprio dependente, ver a própria gravação de reunião, receber aviso de sessão | Entrar em aula de turma, ver presença da turma, ver dado de outro aluno, entrar sem sala de espera | E, só dependentes com vínculo ativo |
| **Terceiros** | Ver integração técnica com o provedor de vídeo, se a entidade contratar um, sem conteúdo de sessão | Ver sessão, participante, gravação ou transcrição | E, pelo contrato de integração ([38](38-portal-de-terceiros-prestadores.md)) |
| **Convidado externo** | Entrar em uma sessão com token de uso único, se a entidade habilitar a opção de externos | Ver outras sessões, o portal da entidade, ou dados de participantes | Fora dos seis portais. Decidido pelo autor em 03/11/2026: a entidade pode habilitar externos |

**Regra de isolamento:** um portal nunca recebe dado de sessão de outra turma, de outra unidade ou de outra entidade. Teste de varredura de resposta por papel.

---

## 8. Infraestrutura de mídia

| Opção | Descrição | Efeito |
|---|---|---|
| A. Provedor de vídeo contratado | A entidade ou a plataforma contrata um provedor de vídeo, com contrato de operador | Menos operação. Exige contrato de operador com cláusulas de dado de menor e de localização dos dados **(jurídico)** |
| B. Própria mídia | Plataforma opera SFU e gravação próprios | Mais controle. Exige operação de mídia, monitoramento e custo de infraestrutura, que a v2 ainda não especifica ([10](10-implantacao-operacao.md)) |

**Decidido pelo autor em 03/11/2026: opção B, mídia própria, com as melhores tecnologias disponíveis.** A plataforma opera a sua própria SFU, o serviço de gravação e o armazenamento de mídia. A escolha de cada componente open source é feita em homologação, com critério de maturidade, segurança e desempenho, e registrada em [10](10-implantacao-operacao.md). Consequências:

- A plataforma passa a ser a operadora direta do dado de sessão. Cifração em trânsito e em repouso, isolamento de mídia por entidade e unidade, e registro de acesso são obrigatórios desde o primeiro lançamento ([05](05-seguranca.md)).
- Operação de mídia (SFU, gravação em fragmentos, armazenamento, capacidade e monitoramento) está especificada em [10](10-implantacao-operacao.md), seção 10.
- As integrações de mídia saem de [16](16-integracoes-externas.md) e passam a ser componentes internos. Cabe um contrato de operador só se algum componente de terceiro for usado.
- Gravação fica sob a mesma guarda de [21](21-busca-e-armazenamento.md) para arquivos. O expurgo automático da seção 5 precisa rodar no armazenamento de mídia.

---

## 9. Correções nos documentos

Correções abaixo. A de [12](12-catalogo-modulos.md) já foi aplicada. As demais são propostas e dependem da aprovação do autor.

| Onde | Correção |
|---|---|
| [12](12-catalogo-modulos.md), linha "Reunião global" | Trocar "Especificado" por "Especificação genérica da v1. Aderente só após [40](40-aulas-online-por-portal.md)" |
| [31](31-matriz-portais-modulos.md), matriz por portal | Incluir a aula online como módulo de entidade (E), ligado à turma e não ao módulo de comunicação |
| [28](28-cobertura-ia-todos-os-modulos.md) | Marcar aula online e reunião como **Não** para transcrição e resumo de sessão com menor, até parecer |
| `global_meeting_spec_v2_complete.md` (v1) | Não editar. Este documento substitui a parte de aula. A parte de reunião administrativa segue a v1 com as regras da seção 4 |

---

## 10. Pendências

| # | Pendência | Tipo |
|---|---|---|
| LIV-01 | Consentimento de responsável para gravação e para entrada de aluno menor sem gravação (seção 5). Pedido por cláusula do contrato com a instituição | (jurídico). Texto da cláusula a cargo do jurídico |
| LIV-02 | Prazo de retenção de gravação e transcrição, padrão 30 dias (seção 5) | (jurídico). Padrão de 30 dias até parecer |
| LIV-03 | Transcrição de aula com menor pode sair para provedor de IA (seção 5) | **Decidido: sim**, pelo gateway de IA. Consentimento (LIV-01) continua valendo |
| LIV-04 | Tempo conectado para presença (seção 6) | **Decidido: 40 minutos**, configurável por entidade |
| LIV-05 | Infraestrutura de mídia (seção 8) | **Decidido: mídia própria**, com as melhores tecnologias |
| LIV-11 | Operação de mídia: SFU, gravação em fragmentos, armazenamento e mapeamento | **Feito:** [10](10-implantacao-operacao.md), seção 10 |
| LIV-06 | Convidado externo (seção 7) | **Decidido:** a entidade habilita a opção. Quem entra usa token de uso único |
| LIV-07 | Coordenador entra em aula para observar (seção 7) | **Decidido:** sim, com registro em auditoria |
| LIV-08 | Padrão visual da sala (seção 4.4) | **Decidido:** template do portal, layout de reunião |
| LIV-12 | Template e componentes da sala | **Feito:** [08](08-frontend-design-system.md), seção 9 |
| LIV-13 | Valores de capacidade: fragmento de 60 segundos (**decidido** em 03/11/2026), bitrate, salas por nó e limite de perda de pacote | Medir em homologação e registrar em [10](10-implantacao-operacao.md), seção 10 |
| LIV-09 | Geolocalização em EAD (seção 6) | **Decidido** em 03/11/2026 por ACC-05 de [35](35-acesso-e-seguranca-fisica-por-portal.md): a escola configura |
| LIV-10 | Modelo de dados da sala, sem tabelas `tenants` e `users` no banco da unidade | **Escrito** em [51](51-ddl-modulos-novos.md), seção 9. Revisão do owner pendente (DDL-01) |

---

## 11. Critérios de aceite

- [ ] Aluno de turma A não entra em sessão da turma B (teste de isolamento).
- [ ] Sessão com aluno menor não grava sem consentimento registrado (teste).
- [ ] Transcrição desligada por padrão; sessão com menor não envia dado a provedor de IA sem parecer (teste).
- [ ] Câmera do aluno começa desligada (teste).
- [ ] Responsável não entra em aula de turma e não vê presença de outros alunos (teste de varredura).
- [ ] Gravação baixada gera evento de auditoria com motivo (teste).
- [ ] Presença pendente não vira falta sem revisão do professor (teste).
- [ ] Token de convidado expira e não serve para outra sessão (teste).
- [ ] Itens **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
