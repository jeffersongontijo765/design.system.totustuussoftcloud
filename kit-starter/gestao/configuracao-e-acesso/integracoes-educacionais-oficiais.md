# Integrações educacionais oficiais

- Portal: Gestão (`gestao.`)
- Área: Configuração e acesso
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [74](../../../docs/v2/74-integracoes-educacionais-oficiais.md) (integral); [16](../../../docs/v2/16-integracoes-externas.md), seção 1
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Integrações com sistemas oficiais de educação (censo, diploma digital, secretarias de educação).

## 3. Telas

- **Integrações** (lista com estado e última execução).
- **Configuração** (credencial por referência ao cofre do tenant).
- **Execuções e erros** (log).

## 4. Permissões por portal (extraídas do SDD)

Do [74](../../../docs/v2/74-integracoes-educacionais-oficiais.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Aprovar envio ao órgão. Ver o histórico de envios e rejeições | Gerar arquivo sem a secretaria | E |
| **Coordenação** | Conferir frequência e turmas antes do envio | Enviar | E |
| **Secretaria** | Gerar, conferir, baixar e importar arquivos. Enviar por API, quando autorizada | Enviar sem conferência da gestão | E |

## 5. Papéis

- `entity.admin` e `unit.secretary` (operação).
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- [74](../../../docs/v2/74-integracoes-educacionais-oficiais.md); dois níveis de integração ([16](../../../docs/v2/16-integracoes-externas.md), seção 1).

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

### 13.1 [74 — Integrações Educacionais Oficiais, por Portal](../../../docs/v2/74-integracoes-educacionais-oficiais.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Trata as integrações com órgãos e programas da educação: Educacenso (INEP), SIGEP (transporte escolar), SGP / MEC Gestão Presente, sistema municipal próprio e programas federais, como o Pé-de-Meia. Integrações externas em geral em [16](../../../docs/v2/16-integracoes-externas.md). Censo escolar e conferência em [69](../../../docs/v2/69-relatorios-e-censo-por-portal.md), seção 4. Carga por arquivo, sem acesso direto ao banco de terceiro, em [70](../../../docs/v2/70-importacao-de-dados-por-portal.md). Transporte e rastro de localização em [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md), seções 3.5 e 11. Frequência em [61](../../../docs/v2/61-diario-escolar-por-portal.md). Matrícula em [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md). Logs de integração em [49](../../../docs/v2/49-logs-testes-por-portal.md), seção 2. Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Layouts, prazos e regras de programa mudam por ano e são marcados **(verificar)**. O conflito de integração com o sistema municipal foi decidido (INT-01, seção 3.4).

---

#### 1. Princípios

1. **Canal oficial, nunca banco de terceiro.** Nenhuma integração acessa o banco do órgão ou de outro sistema ([16](../../../docs/v2/16-integracoes-externas.md)).
2. **Quem envia é a entidade, pela secretaria.** O sistema gera, confere e registra. Não envia nada a órgão sem ação da secretaria, salvo integração por API autorizada (seção 3.3).
3. **Envio é versionado.** Cada envio grava o layout, a versão, o hash, a data e quem enviou. Reenvio gera nova versão ([69](../../../docs/v2/69-relatorios-e-censo-por-portal.md), seção 4).
4. **Dado mínimo.** Só vai o que o layout exige. Dado de localização e de saúde só vai se o layout exigir e se a base legal permitir ([50](../../../docs/v2/50-pacote-juridico-e-norma.md)).
5. **Erro não é corrigido em silêncio.** Rejeição do órgão volta como lista de erros, para correção no módulo de origem.

---

#### 2. Visão geral

| Integração | Função | Canal | Quem executa | Situação |
|---|---|---|---|---|
| Educacenso (INEP) | Declarar escolas, turmas, matrículas, docentes e infraestrutura | Arquivo no layout oficial, importado no sistema do INEP | Secretaria | Seção 3.1 |
| SIGEP | Controle de transporte escolar | Exportação e importação de arquivo | Secretaria, com o transportador | Seção 3.2 |
| SGP / MEC Gestão Presente | Sincronizar gestão e estudantes com a plataforma federal | API | Sistema, com credencial da entidade | Seção 3.3 |
| Sistema municipal próprio | Matrícula, enturmação, diário, frequência e histórico | A definir (INT-01) | Sistema, conforme contrato | Seção 3.4 |
| Pé-de-Meia e programas federais | Elegibilidade e frequência de estudantes | Pela plataforma de dados do SGP | Sistema, com aprovação da secretaria | Seção 3.5 |

---

#### 3. Integrações

##### 3.1 Educacenso (INEP)

- **Conteúdo:** escolas, turmas, matrículas, docentes e infraestrutura. Fontes em [69](../../../docs/v2/69-relatorios-e-censo-por-portal.md), seção 4.2.
- **Mecanismo:** o sistema gera o arquivo no layout oficial do ano. A secretaria confere (seção 4.3 de [69](../../../docs/v2/69-relatorios-e-censo-por-portal.md)), baixa o arquivo e importa no sistema do INEP. A plataforma não acessa o sistema do INEP por conta própria.
- **Registro:** cada arquivo gerado fica em `rel_envios_regulatorios`, com layout, versão, hash e quem gerou, conferiu e enviou ([51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.14).
- **Obrigação:** todo estabelecimento público e privado de educação básica e toda instituição de educação superior presta as informações ao INEP (Decreto 6.425/2008, arts. 4º e 5º). No público, a autoridade do Executivo de cada ente responde pela exatidão; no privado, o representante legal (art. 2º, §§ 1º e 2º, e art. 3º, parágrafo único). Dados pessoais do censo têm sigilo e não servem a outro fim (art. 6º). Conferido em 03/11/2026 no Planalto.
- **Prazo e layout:** o decreto não fixa data de referência, prazo nem layout. Ficam para ato do Ministro da Educação e do INEP, publicado a cada ano (art. 7º, § 1º). Por isso o sistema guarda layout e calendário como **versão por ano**, carregada pela equipe de produto a partir do ato do ano, e não fixa datas no código. Conferir o ato vigente a cada ciclo **(verificar)**.

##### 3.2 SIGEP (transporte escolar)

- **Conteúdo:** alunos usuários do transporte, rotas, veículos, monitores e dados de deslocamento. A troca é por arquivo de exportação e importação, no layout do SIGEP **(verificar)**.
- **Quem executa:** a secretaria gera e importa. O transportador recebe só o que é da sua rota ([38](../../../docs/v2/38-portal-de-terceiros-prestadores.md), seção 3.5).
- **Localização:** o rastro de localização não entra no arquivo a menos que o layout exija. Se exigir, vale a regra de guarda do TER-02 ([38](../../../docs/v2/38-portal-de-terceiros-prestadores.md), seção 11). **(jurídico)**, INT-05.
- **Monitor:** dado pessoal de terceiro. Só o necessário ao layout.

##### 3.3 SGP / MEC Gestão Presente

- **Mecanismo:** API, com credencial da entidade, guardada no cofre ([05](../../../docs/v2/05-seguranca.md)). Recomendada para redes com sistema próprio, por isso a entidade decide se usa.
- **Ciclo:** envio incremental, por registro alterado. Resposta de rejeição fica na fila de integração ([49](../../../docs/v2/49-logs-testes-por-portal.md), LOG-01). Falha de envio é reenviada com a mesma chave de idempotência.
- **Reconciliação:** diária, entre o registro interno e o que o SGP retornou. Diferença vira item para a secretaria, sem correção automática.
- **Termo:** adesão à plataforma federal exige termo da entidade **(jurídico)**, INT-04.

##### 3.4 Sistema municipal próprio

- **Função:** matrícula, enturmação, diário, frequência e histórico, conforme o contrato com a prefeitura.
- **Conflito:** a lista de integrações admite API REST, arquivos CSV ou XML, ou integração por banco. O [16](../../../docs/v2/16-integracoes-externas.md) proíbe acesso direto ao banco de terceiro. Não dá para usar as duas coisas.
- **Decidido** em 03/11/2026 (INT-01): API REST. Arquivo CSV/XML fica como alternativa se a prefeitura não tiver API. Banco não.

##### 3.5 Pé-de-Meia e programas federais

- **Conteúdo:** elegibilidade de estudantes e frequência, quando o programa exigir.
- **Mecanismo:** pela plataforma de dados do SGP (seção 3.3). Não há canal próprio.
- **Regra de envio:** só aluno com matrícula ativa ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md)), e frequência do diário ([61](../../../docs/v2/61-diario-escolar-por-portal.md)) fechada no período. Aprovação da secretaria antes do envio.
- **Regra do programa:** Conferido em 03/11/2026 na Lei 14.818/2024 (planalto.gov.br, com as Leis 14.945/2024 e 15.265/2025). A lei não usa o nome Pé-de-Meia: trata do incentivo financeiro-educacional na modalidade de poupança.
  - **Elegível:** estudante do ensino médio público, em todas as modalidades, de família no CadÚnico, com prioridade pela renda (art. 1º, § 1º). Na EJA, de 19 a 24 anos (art. 1º, § 2º).
  - **Requisitos** (art. 3º): matrícula no início do ano, **frequência mínima de 80%** das horas letivas, conclusão do ano com aprovação, participação no Saeb e em avaliação externa do ente, Enem no último ano, Encceja na EJA.
  - **Periodicidade:** aportes de matrícula e frequência pelo menos 9 vezes por ano (art. 5º, § 4º). O sistema prepara a frequência por mês fechado.
  - **Quem verifica:** a autoridade federal da educação (art. 3º, § 1º). As redes prestam as informações, nos termos do regulamento (art. 4º).
  - O sistema não decide elegibilidade: envia matrícula e frequência e mostra o aluno abaixo de 80% como alerta à secretaria. O 80% é do programa e não muda o mínimo de aprovação de 75% ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 4).
  - **Regulamento** (Decreto 11.901/2024, conferido em 03/11/2026): idade de 14 a 24 anos e família no CadÚnico (art. 3º). Matrícula registrada até dois meses após o início do ano letivo e CPF do aluno (art. 4º, § 1º). Frequência de 80% medida pela média do período transcorrido ou pela frequência mensal, conforme ato do MEC (art. 4º, § 2º). Valores anuais: R$ 200 de matrícula, R$ 1.800 de frequência, R$ 1.000 de conclusão e R$ 200 do Enem (art. 4º).
  - **Dever da rede:** termo de compromisso assinado pelo chefe do Executivo do ente (art. 7º). A rede presta as informações e responde **sozinha pela veracidade** (art. 7º, §§ 1º e 3º). Informação fora do prazo do termo pode levar ao não pagamento do período (art. 7º, § 2º). Por isso o sistema mostra o prazo do termo, cadastrado pela secretaria, e alerta antes do vencimento. O envio exige aprovação da secretaria, que fica registrada.
  - **Desligamento:** evasão, abandono, ou reprovação por duas vezes seguidas ou por dois anos, entre outros casos (art. 5º). O sistema mostra esses alunos como alerta, sem decidir.
  - Ficam com o ato do MEC: forma exata da medição da frequência, canal e calendário de envio **(verificar)**.

---

#### 4. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Manter os layouts publicados, sem dado de entidade | Enviar ou ver envio de entidade | P |
| **Gestão** | Aprovar envio ao órgão. Ver o histórico de envios e rejeições | Gerar arquivo sem a secretaria | E |
| **Coordenação** | Conferir frequência e turmas antes do envio | Enviar | E |
| **Secretaria** | Gerar, conferir, baixar e importar arquivos. Enviar por API, quando autorizada | Enviar sem conferência da gestão | E |
| **Professor** | Nada. A frequência do diário alimenta o envio | Ver envio ou arquivo | E |
| **Aluno** e **Responsáveis** | Nada | Ver arquivo ou envio | E |
| **Transportador** (terceiro) | Ver a própria rota e os alunos da rota | Ver outras rotas ou arquivo completo | Terceiros, [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md) |
| **Terceiros** (demais) | Nada | Qualquer item de integração | E |

---

#### 5. Pendências

| # | Pendência | Tipo |
|---|---|---|
| INT-01 | Sistema municipal: API REST, arquivo CSV/XML, ou banco (seção 3.4) | **Decidido** em 03/11/2026: API REST. Banco não |
| INT-02 | Layout e prazo do Educacenso, por ano e por esfera (seção 3.1) | **Conferido** em parte em 03/11/2026: obrigação e responsáveis no Decreto 6.425/2008. Layout e prazo vêm do ato anual do MEC e do INEP, guardados como versão por ano **(verificar)** a cada ciclo |
| INT-03 | Critérios e periodicidade do Pé-de-Meia (seção 3.5) | **Conferido** em 03/11/2026: Lei 14.818/2024, arts. 1º, 3º, 4º e 5º. Decreto 11.901/2024, arts. 3º a 7º, conferido. Canal e calendário de envio no ato do MEC **(verificar)** |
| INT-04 | Termo de adesão à plataforma federal (SGP), e quem assina (seção 3.3) | (jurídico) |
| INT-05 | Dado de localização no arquivo do SIGEP (seção 3.2). Mesmo ponto de TER-02 | (jurídico) |
| INT-06 | Layout do SIGEP e se o monitor é pessoa do terceiro (seção 3.2) | (verificar) |
| INT-07 | DDL: integração, envio, lote, resposta e rejeição. Reutiliza `rel_envios_regulatorios` onde couber | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.20. Revisão do owner pendente (DDL-01) |

---

#### 6. Critérios de aceite

- [ ] Nenhuma integração acessa banco de terceiro (teste de configuração).
- [ ] Envio ao Educacenso não ocorre sem conferência da gestão (teste).
- [ ] Transportador vê só a própria rota (teste de isolamento).
- [ ] Reenvio com a mesma chave não duplica registro (teste de idempotência).
- [ ] Rejeição do órgão aparece como lista de erros, sem correção automática (teste).
- [ ] Pé-de-Meia só inclui aluno com matrícula ativa (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).

### 13.2 [16](../../../docs/v2/16-integracoes-externas.md), seção 1

#### 1. Dois níveis

| Nível | Quem contrata e paga | Quem configura | Credencial fica em | Quem usa |
|---|---|---|---|---|
| **Plataforma (master)** | TotusTuus SoftCloud | Equipe da plataforma, com permissão `plataforma.integracao.*` | Cofre da plataforma | Todos os tenants, de forma transparente |
| **Tenant** | A entidade (cliente) | Administrador da entidade, com permissão `integracao.conexao.*` | Cofre, com chave de cifragem por tenant | Só o próprio tenant |

Regras:

1. Credencial de um tenant nunca é visível para outro tenant, nem para a equipe da plataforma em texto claro.
2. A equipe da plataforma vê status, erros resumidos e metadados de uma conexão de tenant. Para ver o segredo, é preciso step-up, motivo registrado e alerta ao canal de segurança (ver [06](../../../docs/v2/06-identidade-acesso.md), seção 10).
3. Uma integração de plataforma pode ser usada por um tenant só quando o plano contratado inclui o recurso. O controle é feito pela configuração do tenant, não pelo código.
4. Integração de tenant não pode substituir integração de plataforma em funções de segurança, como e-mail de verificação e MFA.
