# Classe

- Portal: Professor (`portal-do-professor.`)
- Área: Classe
- Domínio: entidade: banco da unidade; o professor vê **só as turmas e disciplinas em que tem vínculo ativo** ([17](../../docs/v2/17-regras-modulos.md), seção 4.4; [06](../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [80](../../docs/v2/80-decisoes-por-padrao.md) (integral); [21](../../docs/v2/21-busca-e-armazenamento.md), seção 3.3; [21](../../docs/v2/21-busca-e-armazenamento.md), seção 3.9; [59](../../docs/v2/59-estrutura-academica-por-portal.md), seção 4
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Espaço da turma para o professor: lista de turmas e disciplinas vinculadas, mural de avisos, materiais de apoio e tarefas com entrega (DP-06).

## 3. Telas

- **Minhas turmas** (cards por turma e disciplina): horário, nº de alunos, pendências do diário, próximas tarefas.
- **Turma — visão** (página com abas): *Alunos* (lista com foto só com termo de imagem), *Mural*, *Materiais*, *Tarefas*, *Diário* (atalho).
- **Mural** (lista de avisos; criar aviso com anexos; comentários desligados por padrão, DP-06).
- **Materiais** (lista e upload pelo armazenamento, com antivírus e limite).
- **Tarefas** (DataTable): título, prazo, entregas, corrigidas; **Nova tarefa** (instruções, prazo, anexos, forma de entrega, se é avaliação).
- **Entregas da tarefa** (DataTable por aluno: entregue, atrasada, não entregue; correção com nota e comentário; sugestão de IA opcional).

## 4. Permissões por portal (extraídas do SDD)

Do [59](../../docs/v2/59-estrutura-academica-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Professor** | Ver grade e sistema das próprias disciplinas | Alterar grade ou sistema | E |

## 5. Papéis

- `teacher` (nível 1, escopo turma): ações das próprias turmas.
- `teacher.coordinator` (nível 2, unidade): aprova planos e lançamentos de nível 1 da unidade ([78](../../docs/v2/78-permissoes-e-papeis.md), seção 4.3).
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- DP-06 do [80](../../docs/v2/80-decisoes-por-padrao.md) rege mural, materiais e tarefas.
- Nota da tarefa só entra no diário se a tarefa for uma avaliação do sistema avaliativo ([59](../../docs/v2/59-estrutura-academica-por-portal.md), seção 4).
- Arquivos pelo armazenamento ([21](../../docs/v2/21-busca-e-armazenamento.md), seção 3).

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

### 13.1 [80 — Decisões tomadas por padrão (delegadas pelo autor)](../../docs/v2/80-decisoes-por-padrao.md) (documento integral)

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

### 13.2 [21](../../docs/v2/21-busca-e-armazenamento.md), seção 3.3

##### 3.3 Upload

1. Cliente pede `POST /api/v1/storage/buckets/{code}/uploads` com nome, tamanho declarado, checksum SHA-256 e tipo declarado. Serviço valida permissão, cota e tipo declarado contra a lista do bucket ([15](../../docs/v2/15-validacoes.md), seção 4.3).
2. Serviço cria registro com estado `pendente_upload` e devolve URL assinada de PUT, com validade de 15 min, `content-length` fixo e checksum esperado no cabeçalho.
3. Cliente envia direto ao provedor. Arquivos acima de 5 MB vão direto; arquivos menores podem passar pelo backend, com a mesma validação.
4. Provedor confirma o checksum. Se não bater, recusa o envio.
5. Evento `storage.file.uploaded` vai para a fila ([14](../../docs/v2/14-integracao-modulos.md), seção 5).
6. Verificador confere magic bytes, tipo real, tamanho e antivírus. Estado vai para `disponivel` ou `quarentena`.
7. Derivados são gerados só depois de `disponivel`.

Regras:

- Executável, script, macro ativa em Office e PDF com JavaScript são recusados e vão para quarentena.
- Nome original é guardado como metadado, sanitizado (sem caminho, sem caractere de controle, máximo 255).
- Limite de cota por bucket, reservado no início do upload e liberado se falhar.

### 13.3 [21](../../docs/v2/21-busca-e-armazenamento.md), seção 3.9

##### 3.9 Limites padrão

| Item | Valor inicial |
|---|---|
| Tamanho máximo por arquivo | 50 MB (documento), 10 MB (imagem), ajustável por bucket |
| Arquivos por lote de upload | 20 |
| Validade da URL de upload | 15 min |
| Validade da URL de download | 300 s padrão, 900 s máximo |
| Tempo máximo de estado `pendente_upload` | 24 h, depois descartado |

### 13.4 [59](../../docs/v2/59-estrutura-academica-por-portal.md), seção 4

#### 4. Sistemas avaliativos

Cada curso usa um sistema avaliativo. Um sistema define:

| Elemento | Opções | Regra |
|---|---|---|
| Escala | Numérica (ex.: 0 a 10), conceitual (ex.: A a E), percentual | Uma escala por sistema |
| Tipos de avaliação | Prova, trabalho, seminário, atividade prática, autoavaliação | Cada tipo tem peso |
| Método de média | Aritmética ou ponderada | Pesos somam 100% por período |
| Recuperação | Paralela, final, ou ambas | Nota de recuperação substitui ou compõe a média, conforme o sistema |
| Nota mínima de aprovação | Valor da escala | Por sistema |
| Frequência mínima | Percentual de presença | 75% do total de horas letivas no fundamental e no médio (LDB, art. 24, VI). 60% na pré-escola (art. 31, IV). No superior, a frequência de alunos e professores é obrigatória, salvo nos programas de educação a distância (art. 47, § 3º, texto literal conferido). A LDB não fixa percentual para o superior: o valor vem do regimento da instituição e é configurado por curso. O valor fica no sistema avaliativo, com esses mínimos como piso |
| Aprovação por conselho | Sim ou não | Casos fora da regra passam por conselho de classe ([55](../../docs/v2/55-academico-verificacao-e-lacunas.md), item 5) |

**Regras:**

- Nota fora da escala é recusada.
- Sistema avaliativo em uso não muda. Mudança gera nova versão, aplicada ao próximo período.
- Arredondamento padrão: uma casa decimal, arredondando para cima a partir de 0,05. A entidade pode definir outra regra, registrada no próprio sistema avaliativo.
