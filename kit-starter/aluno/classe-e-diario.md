# Classe e diário

- Portal: Aluno (`portal-do-aluno.`)
- Área: Classe e diário
- Domínio: entidade: banco da unidade; o aluno vê **só os próprios dados** (escopo `proprio`, [78](../../docs/v2/78-permissoes-e-papeis.md), seção 4.4). Aluno menor: o responsável com vínculo ativo atua por ele ([07](../../docs/v2/07-privacidade-lgpd.md))
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [62](../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md), seção 2; [62](../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md), seção 7; [61](../../docs/v2/61-diario-escolar-por-portal.md), seção 4; [61](../../docs/v2/61-diario-escolar-por-portal.md), seção 7; [80](../../docs/v2/80-decisoes-por-padrao.md) (integral)
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Disciplinas, materiais, entregas de tarefas, boletim e presença do próprio aluno.

## 3. Telas

- **Início do aluno** (dashboard: horário do dia, próximas entregas, últimas notas, avisos).
- **Minhas disciplinas** (cards).
- **Disciplina** (abas: mural, materiais, tarefas, notas, faltas).
- **Entregar tarefa** (upload ou texto; confirmação com data e hora; atraso marcado, DP-06).
- **Boletim** (por período, com média e situação).
- **Presença** (faltas por disciplina; pedido de justificativa).

## 4. Permissões por portal (extraídas do SDD)

Do [62](../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Aluno** | Ver o próprio boletim, parcial e oficial, e a situação. Baixar boletim oficial | Ver ata. Ver boletim de colega | E |

Do [61](../../docs/v2/61-diario-escolar-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Aluno** | Ver as próprias notas, faltas e justificativas. Enviar justificativa com anexo | Ver nota ou falta de colega | E |

## 5. Papéis

- `student` (nível 0, escopo próprio) ([78](../../docs/v2/78-permissoes-e-papeis.md), seção 4.4).
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- DP-06 ([80](../../docs/v2/80-decisoes-por-padrao.md)); boletim conforme [62](../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md), seção 2.

## 7. Dados

- Tabelas e campos conforme a seção 13 e o DDL do [51](../../docs/v2/51-ddl-modulos-novos.md), quando o módulo estiver lá. Toda tabela tem `entidade_id`, `unidade_id`, `created_at`, `updated_at`, `created_by` e exclusão lógica com `deleted_at` e `deleted_by` ([03](../../docs/v2/03-dominio-tenancy.md), seção 6; [15](../../docs/v2/15-validacoes.md); [19](../../docs/v2/19-regras-modulos-3.md), seção 14).

## 8. Integrações

- Ver a seção de integrações do documento de origem, na seção 13.

## 9. Exportação, auditoria e privacidade

- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../docs/v2/08-frontend-design-system.md), seção 3).
- Toda criação, alteração, aprovação, exclusão lógica, exportação e leitura de dado sensível gera evento de auditoria no banco da unidade ([29](../../docs/v2/29-auditoria.md)).
- Dados pessoais conforme [07](../../docs/v2/07-privacidade-lgpd.md): mínimo necessário, mascaramento em listas, base legal registrada.

## 10. Estados de interface

- Carregando (skeleton), vazio com chamada para ação, sem resultado de filtro, erro com nova tentativa, acesso negado, registro bloqueado, fechado ou baixado (somente leitura), conflito de edição (versão).

## 11. Requisitos de frontend

- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`): página de lista com DataTable, KPIs, drawer de detalhe, formulário em página ou modal, kanban quando houver fluxo de estados.
- Seletor de unidade no topo quando o usuário tiver mais de uma; a troca reemite o token com o novo contexto ([06](../../docs/v2/06-identidade-acesso.md), seção 12).

## 12. Critérios de aceite e pendências

- Critérios de aceite: os do documento de origem (seção 13) e os de [31](../../docs/v2/31-matriz-portais-modulos.md), seção 6.
- Testes de isolamento: usuário de outra unidade ou entidade recebe 404 em toda rota do módulo ([03](../../docs/v2/03-dominio-tenancy.md)).
- As pendências do documento de origem estão na seção 13 e consolidadas no [45](../../docs/v2/45-pendencias-consolidadas.md).

## 13. Regras da v2 (texto integral das fontes, sem corte)

### 13.1 [62](../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md), seção 2

#### 2. Boletim

##### 2.1 Conteúdo

O boletim reúne, por aluno e por período:

- Identificação do aluno, da turma, do curso, da versão da grade e do período letivo.
- Por disciplina: avaliações com nota, peso e data, média do período, total de aulas, faltas e percentual de frequência.
- Situação da disciplina: `aprovado`, `recuperacao`, `reprovado_nota`, `reprovado_frequencia`, `aprovado_conselho`, `em_andamento`.
- Versão do sistema avaliativo aplicada. Mudança posterior do sistema não altera o boletim já emitido.
- Resultado final do período, quando o período estiver fechado.

##### 2.2 Tipos de emissão

| Tipo | Quando | Valor |
|---|---|---|
| Parcial | Durante o período, a qualquer momento | Informativo. Traz a marca "parcial, sem valor oficial". Não é documento de [48](../../docs/v2/48-gerador-de-documentos-por-portal.md) |
| Oficial | Depois do fechamento do período e da ata do conselho, se houver | Documento oficial, com código de validação e QR. Vai para o contexto C de [54](../../docs/v2/54-gestao-de-documentos-tres-contextos.md) |
| Segunda via | A pedido, depois da emissão oficial | Indica que é reemissão e mantém a data de origem, como em DC-14 ([53](../../docs/v2/53-pacote-documentos-e-contratos.md)) |

**Regras:**

- Boletim oficial só é emitido com período `fechado` ([59](../../docs/v2/59-estrutura-academica-por-portal.md), seção 3.6).
- Boletim oficial traz código de validação pública. Pela regra DC-13, a validação mostra tipo, data, situação e entidade. Não mostra nota.
- Alteração de nota depois do boletim oficial gera nova versão do boletim, com aviso ao aluno e ao responsável ([57](../../docs/v2/57-notificacoes-por-portal.md)). A versão anterior fica no histórico.

### 13.2 [62](../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md), seção 7

#### 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelo de ata e de boletim, sem dado | Ver boletim, resultado ou ata de entidade | P |
| **Gestão** | Ver indicadores de aprovação e reprovação, ver atas da unidade | Alterar resultado. Decidir conselho de aluno | E |
| **Coordenação** | Convocar conselho, montar pauta, presidir, decidir resultado fora da regra, autorizar reabertura | Lançar nota pelo professor | E |
| **Secretaria** | Emitir boletim oficial, registrar ata, executar reabertura autorizada, emitir segunda via | Decidir resultado de aluno | E |
| **Professor** | Ver boletim parcial das próprias turmas. Opinar no conselho. Lançar recuperação | Decidir resultado. Ver boletim de turma de que não é professor | E |
| **Aluno** | Ver o próprio boletim, parcial e oficial, e a situação. Baixar boletim oficial | Ver ata. Ver boletim de colega | E |
| **Responsáveis** | Ver boletim do dependente, parcial e oficial. Ver a situação | Ver ata ou parecer. Ver boletim de outro aluno | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item do boletim ou do conselho | E |

### 13.3 [61](../../docs/v2/61-diario-escolar-por-portal.md), seção 4

#### 4. Faltas e justificativas

##### 4.1 Falta

- Falta é registrada por aluno, por aula. Não por dia.
- Falta é contada por disciplina, e por período no total de frequência.

##### 4.2 Justificativa

| Regra | Detalhe |
|---|---|
| Tipos | Lista padrão da plataforma, ajustável pela escola. Decidido em 03/11/2026 |
| Prazo | 5 dias úteis após a falta, ajustável pela escola. Decidido em 03/11/2026 |
| Documento | Anexo quando o tipo exigir. Armazenado como documento recebido ([54](../../docs/v2/54-gestao-de-documentos-tres-contextos.md), contexto A) |
| Quem aprova | Coordenação. Professor não aprova justificativa de própria aula |
| Efeito | A LDB não prevê abono geral de falta: a falta justificada continua contando para o mínimo de 75% (art. 24, VI). A exceção da LDB é a falta por motivo religioso com atividade alternativa, que regulariza a frequência (art. 7º-A, § 2º). Regimes especiais de lei própria, como exercícios domiciliares, entram como exceção configurada **(verificar)** |
| Negativa | Sempre com motivo. Aluno ou responsável recebe o aviso ([57](../../docs/v2/57-notificacoes-por-portal.md)) |

##### 4.3 Aviso de falta

- Falta acima do limite de alerta da escola gera aviso ao responsável ([57](../../docs/v2/57-notificacoes-por-portal.md)).
- O aviso informa a disciplina e a quantidade de faltas. Não informa motivo clínico.
- Falta de saúde justificada por atestado não aparece com diagnóstico no aviso ([57](../../docs/v2/57-notificacoes-por-portal.md), seção 3.5).
- **Conselho Tutelar:** a escola notifica ao Conselho Tutelar do município a relação dos alunos com faltas acima de 30% do percentual permitido em lei (LDB, art. 12, VIII). O sistema gera a lista por período para a secretaria enviar. A forma de cálculo e a periodicidade ficam em DIA-09 **(verificar)**.

### 13.4 [61](../../docs/v2/61-diario-escolar-por-portal.md), seção 7

#### 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Nada sobre diário de entidade | Ver diário, nota, falta ou conteúdo | P |
| **Gestão** | Ver relatórios do diário e indicadores de frequência | Lançar nota ou chamada. Autorizar reabertura, que é da coordenação | E |
| **Coordenação** | Aprovar justificativa. Autorizar lançamento fora do prazo e reabertura. Ver diário de todas as turmas da unidade | Lançar nota pelo professor | E |
| **Secretaria** | Consultar diário. Emitir relatórios. Cadastrar tipos de justificativa | Lançar nota ou aprovar justificativa | E |
| **Professor** | Fazer chamada, lançar nota e conteúdo das próprias turmas. Ver o diário das próprias turmas | Lançar em turma em que não leciona. Aprovar justificativa da própria aula | E |
| **Aluno** | Ver as próprias notas, faltas e justificativas. Enviar justificativa com anexo | Ver nota ou falta de colega | E |
| **Responsáveis** | Ver as notas e faltas do dependente. Enviar justificativa | Ver diário de outra turma | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item do diário | E |

### 13.5 [80 — Decisões tomadas por padrão (delegadas pelo autor)](../../docs/v2/80-decisoes-por-padrao.md) (documento integral)

> Parte do [SDD v2](../../docs/v2/00-README.md). Em 04/11/2026 o autor delegou as decisões em aberto: "sempre a melhor prática, mais segura, completa", sem bloquear o trabalho para perguntar.
> **Regra:** antes de decidir, o assunto é buscado em todo o SDD (v2 e [anexo-v1/](../../docs/v2/anexo-v1/)). Só entra aqui o que não está decidido em nenhum documento. Cada decisão tem motivo, alternativa descartada e onde se aplica. O autor pode revisar qualquer item; revisão vira nova linha, sem apagar a anterior.

#### 1. Critérios usados

1. **Segurança e conformidade primeiro:** na dúvida, a opção que expõe menos dado, exige aprovação ou bloqueia o erro.
2. **Completude:** na dúvida entre incluir e excluir um recurso previsto na v1, incluir.
3. **Não inventar valor legal ou contábil:** prazo, alíquota, taxa e texto jurídico não são inventados. Ficam como parâmetro obrigatório, configurado pelo responsável, e o sistema bloqueia o uso enquanto não forem configurados.
4. **Separação de funções:** quem opera não aprova a própria operação ([78](../../docs/v2/78-permissoes-e-papeis.md), seção 2.2).

#### 2. Decisões

| # | Assunto | Decisão | Motivo | Alternativa descartada | Onde se aplica |
|---|---|---|---|---|---|
| DP-01 | Frotas nesta versão (pendência do autor em [45](../../docs/v2/45-pendencias-consolidadas.md), seção 2) | **Entra nesta versão**, para a empresa e para as entidades | Completude; a especificação da v1 é completa e o transporte escolar é uso real | Deixar para versão futura | Portal do desenvolvedor (operações internas) e portal de gestão |
| DP-02 | Regra de depreciação por categoria (lacuna L-18 do [19](../../docs/v2/19-regras-modulos-3.md)) | Cada categoria de ativo tem método e taxa **aprovados pelo contábil**. Categoria sem regra aprovada **não deprecia** e aparece como pendência no painel | Critério 3: não inventar taxa contábil; não deixar ativo sem controle | Taxa padrão do sistema para todas as categorias | Patrimônio (empresa e entidade) |
| DP-03 | Papéis de patrimônio e frotas (não definidos no [22](../../docs/v2/22-crm-canais-e-papeis.md), seção 5) | Operador (nível 1) e aprovador (nível 2) separados, para patrimônio e para frotas. Compras, almoxarifado e aprovador de compras seguem o [22](../../docs/v2/22-crm-canais-e-papeis.md), seção 5 | Critério 4; mesmo padrão dos papéis departamentais já aprovados | Um único papel por módulo | [78](../../docs/v2/78-permissoes-e-papeis.md), seção 4.1 (plataforma) |
| DP-04 | Conteúdo das configurações do sistema da plataforma (não definido em nenhum documento) | Configurações agrupadas pelo documento do SDD que define cada regra (idiomas [09](../../docs/v2/09-internacionalizacao.md); senha, sessão e MFA [06](../../docs/v2/06-identidade-acesso.md); limites de API [04](../../docs/v2/04-api.md); e-mail e integrações [16](../../docs/v2/16-integracoes-externas.md); cache [30](../../docs/v2/30-cache.md); manutenção [24](../../docs/v2/24-operacao-continuidade-qualidade.md)). Toda mudança exige step-up, motivo, auditoria e gera versão com rollback. Valor fora do limite do documento de origem é recusado | Critérios 1 e 4; o sistema não aceita configuração que contrarie o SDD | Tela livre de chave e valor | Portal do desenvolvedor (segurança e operação) |
| DP-05 | Códigos dos papéis da entidade no portal de gestão (o [22](../../docs/v2/22-crm-canais-e-papeis.md), seção 5, e os documentos por portal nomeiam os papéis, mas o [78](../../docs/v2/78-permissoes-e-papeis.md), seção 4.2, só listava nove) | Um código `unit.*` ou `entity.*` para cada papel já nomeado no SDD (contábil, fiscal, comercial, compras, almoxarifado, aprovador de compras, folha, aprovador da folha, médico do trabalho, SESMT, jurídico, encarregado, segurança, TI, preceptoria, pastoral, portaria). Patrimônio e frotas da entidade seguem o DP-03 (operador e aprovador separados). Aprovador financeiro da unidade separado de quem lança ([17](../../docs/v2/17-regras-modulos.md), seção 2.4) | Critério 4; nenhum papel novo de negócio, só o código do que já existe | Reaproveitar os nove papéis genéricos | [78](../../docs/v2/78-permissoes-e-papeis.md), seção 4.2 |
| DP-06 | Mural, materiais e tarefas da classe (portal do professor, do aluno e dos responsáveis): a v1 só os cita na navegação ([12-portals-navigation-sidebar-pages-spec.md](../../docs/v2/anexo-v1/12-portals-navigation-sidebar-pages-spec.md)) e a v2 não tem regra | **Mural:** aviso por turma, publicado pelo professor da turma ou pela coordenação; comentários desligados por padrão (o professor liga por aviso); sem foto de aluno sem termo de imagem ([32](../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 3.2). **Materiais:** arquivos pelo armazenamento ([21](../../docs/v2/21-busca-e-armazenamento.md)), com antivírus e limite de tamanho; visíveis só à turma; download registrado. **Tarefas:** título, instruções, prazo, anexos, forma de entrega; entrega do aluno com data e hora, atraso marcado; nota da tarefa só pelo professor da turma e só entra no diário se a tarefa for uma avaliação do sistema avaliativo ([59](../../docs/v2/59-estrutura-academica-por-portal.md), seção 4); IA só sugere correção ([27](../../docs/v2/27-inteligencia-artificial-e-portais.md)). **Responsáveis:** veem tarefas, prazos e entregas dos dependentes com vínculo ativo, sem poder entregar. Retenção: até o fim do período letivo mais o prazo da matriz de retenção ([26](../../docs/v2/26-sdd-juridico-regulatorio.md), seção 3) | Critérios 1 e 2; mesmo escopo "só turmas vinculadas" da [31](../../docs/v2/31-matriz-portais-modulos.md), seção 2.3 | Mural aberto com comentários livres | Portais do professor, do aluno e dos responsáveis |
