# Frotas da empresa

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Operações internas
- Domínio: plataforma (banco master), instância separada do módulo das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Status: detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)
- Fonte da v1: [spec_gestao_frotas_completo.md](../../../docs/v2/anexo-v1/spec_gestao_frotas_completo.md) (1558 linhas)

## 1. Regra de leitura
As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.

## 2. Objetivo e escopo
Gerir os veículos da própria empresa desenvolvedora: veículos, motoristas, reservas, manutenção, abastecimento, viagens, multas e documentos.

## 3. Telas
- **Veículos da empresa** (datatable): placa, documentos com validade, situação, responsável.
- **Reservas** (calendário): veículo, solicitante, aprovação pela alçada.
- **Manutenções** (kanban): solicitada, aprovada, em execução, concluída.
**Títulos da v1 (referência, não são telas):**

- Sumário
- 1. Visão Geral
  - 1.1 Objetivo
  - 1.2 Escopo Funcional
  - 1.3 Integrações
- 2. Perfis e Permissões RBAC
- 3. Dashboard de Frotas
  - 3.1 Widgets KPI — Linha 1 (Cards grandes)
  - 3.2 Widgets KPI — Linha 2 (Cards médios)
  - 3.3 Charts amCharts 5
  - 3.4 Datatable — Alertas Críticos
  - 3.5 Datatable — Reservas do Dia
  - 3.6 Painel de Mapa (opcional)
- 4. Gestão de Veículos
  - 4.1 Controles da Página
  - 4.2 Datatable — Veículos
  - 4.3 Drawer — Cadastrar / Editar Veículo
  - 4.4 Drawer — Detalhe do Veículo
- 5. Motoristas e Habilitações
  - 5.1 Controles da Página
  - 5.2 Datatable — Motoristas
  - 5.3 Drawer — Cadastrar / Editar Motorista
- 6. Agendamentos e Reservas
  - 6.1 Controles da Página
  - 6.2 Datatable — Reservas
  - 6.3 Visualização Calendário
  - 6.4 Visualização Timeline (Gantt)
  - 6.5 Drawer — Nova Reserva / Editar
  - 6.6 Drawer — Check-in / Check-out
- 7. Manutenções e Revisões
  - 7.1 Controles da Página
  - 7.2 Datatable — Ordens de Manutenção
  - 7.3 Charts — Manutenções
  - 7.4 Drawer — Nova OS de Manutenção
  - 7.5 Drawer — Plano de Manutenção Preventiva
- 8. Abastecimentos e Combustível
  - 8.1 Controles da Página
  - 8.2 Datatable — Abastecimentos
  - 8.3 Widgets — Combustível
  - 8.4 Charts — Combustível
  - 8.5 Drawer — Registrar Abastecimento
- 9. Rotas e Viagens
  - 9.1 Controles da Página
  - 9.2 Datatable — Viagens
  - 9.3 Drawer — Registrar Viagem / Rota
- 10. Multas e Ocorrências
  - 10.1 Controles da Página
  - 10.2 Datatable — Multas e Ocorrências
  - 10.3 Drawer — Registrar Multa
- 11. Documentos e Licenciamentos
  - 11.1 Controles da Página
  - 11.2 Datatable — Documentos
  - 11.3 Drawer — Cadastrar Documento
- 12. Kanban Operacional
  - 12.1 Kanban — Status de Veículos
  - 12.2 Kanban — Manutenções
  - 12.3 Kanban — Reservas
- 13. Automações e Alertas
  - 13.1 Automações Disponíveis
  - 13.2 Drawer — Configurar Automação
  - 13.3 Log de Automações
- 14. Relatórios e Exportações
  - 14.1 Relatórios Disponíveis
  - 14.2 Charts nos Relatórios
- 15. Configurações do Módulo
  - 15.1 Abas de Configuração
  - 15.2 Drawer — Regras de Aprovação de Reservas
- 16. APIs REST
  - 16.1 Veículos
  - 16.2 Motoristas
  - 16.3 Reservas e Agendamentos
  - 16.4 Manutenções
  - 16.5 Abastecimentos
  - 16.6 Rotas e Viagens
  - 16.7 Multas
  - 16.8 Dashboard e Relatórios
- 17. Schema SQL
- 18. LGPD e Auditoria
  - 18.1 Dados Pessoais Tratados
  - 18.2 Eventos Auditados
  - 18.3 Regras de Acesso e Mascaramento
  - 18.4 Direitos do Titular (LGPD)
- 19. Critérios de Aceite
  - 19.1 Funcionais
  - 19.2 Segurança e Conformidade
  - 19.3 Performance e UX
  - 19.4 Checklist de Entrega

## 4. Correções da v2 que prevalecem
- **DP-01:** Frotas entra nesta versão ([80](../../../docs/v2/80-decisoes-por-padrao.md)).
- **T-01:** as 13 tabelas recebem `tenant_id` NOT NULL e índice composto ([19](../../../docs/v2/19-regras-modulos-3.md), seção 1).
- **Regras** ([19](../../../docs/v2/19-regras-modulos-3.md), seção 9): CNH vencida bloqueia a reserva e mostra alerta; conflito de horário bloqueia a reserva; veículo em manutenção bloqueia e sugere alternativo; validade do tacógrafo obrigatória quando aplicável; consumo é calculado (litros e quilometragem) e **nunca** campo de entrada, inclusive na tela que a v1 mostra como editável; abastecimento com litros maior que zero.
- **Instância da empresa:** sem filtro de unidade, entidade ou filial; dados no banco master; o portal do desenvolvedor não vê o módulo de nenhuma entidade.
- **Perfis da v1 (seção 2 da v1):** substituídos pelos papéis da seção 6 desta ficha.
- **Mapa (v1, "Painel de Mapa", opcional):** só com provedor de mapas aprovado como integração ([16](../../../docs/v2/16-integracoes-externas.md)); sem provedor, o painel não aparece.

## 5. Decisões por padrão aplicadas
- **DP-01:** módulo incluído.
- **DP-03:** papéis de operador e aprovador separados.

## 6. Permissões e papéis
- `platform.fleet` (nível 1): cadastrar veículos e motoristas, registrar reservas, abastecimentos, viagens, multas e documentos.
- `platform.fleet.approver` (nível 2): aprovar reservas e ordens de manutenção, conforme as regras de aprovação da v1; não aprova a própria reserva (DP-03; [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 4.1).

## 7. Dados
- Modelo de dados da v1 (seção 13, "Schema SQL"), com a correção T-01 e o consumo como valor calculado.

## 8. Integrações
- Financeiro da plataforma: custo de abastecimento, manutenção e multa (contas a pagar).
- Patrimônio da empresa: veículo é também bem patrimonial.
- Suprimentos da empresa: peças e serviços de manutenção.

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md).
- CNH, multas e dados do motorista são dados pessoais: acesso só pelos papéis da seção 6, com retenção conforme [07](../../../docs/v2/07-privacidade-lgpd.md).

## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- Regras de aprovação de reservas: configuradas no módulo (v1, "Regras de Aprovação de Reservas"); sem regra configurada, toda reserva exige aprovação (critério 1 do [80](../../../docs/v2/80-decisoes-por-padrao.md)).

## 13. Conteúdo integral da v1 (absorvido)

### SPEC — Módulo Frotas
**Projeto:** TotusTuusSoftCloud SaaS Platform  
**Módulo:** Frotas / Fleet Management  
**Versão:** 1.0  
**Status:** Draft  
**Stack:** PHP 8 puro · Supabase · Tailwind CSS 4.2 · amCharts 5 · MariaDB/InnoDB · JWT · REST API  
**Arquitetura:** Multi-entity · Multi-unit · Multi-user · Banco segregado por unidade  
**Autor:** Jefferson Augusto — TotusTuusSoftCloud  
**Data:** 2026-06-07  

- Language Standard: Global English
---

#### Sumário

1. [Visão Geral](#1-visao-geral)
2. [Perfis e Permissões RBAC](#2-perfis-e-permissoes-rbac)
3. [Dashboard de Frotas](#3-dashboard-de-frotas)
4. [Gestão de Veículos](#4-gestao-de-veiculos)
5. [Motoristas e Habilitações](#5-motoristas-e-habilitacoes)
6. [Agendamentos e Reservas](#6-agendamentos-e-reservas)
7. [Manutenções e Revisões](#7-manutencoes-e-revisoes)
8. [Abastecimentos e Combustível](#8-abastecimentos-e-combustivel)
9. [Rotas e Viagens](#9-rotas-e-viagens)
10. [Multas e Ocorrências](#10-multas-e-ocorrencias)
11. [Documentos e Licenciamentos](#11-documentos-e-licenciamentos)
12. [Kanban Operacional](#12-kanban-operacional)
13. [Automações e Alertas](#13-automacoes-e-alertas)
14. [Relatórios e Exportações](#14-relatorios-e-exportacoes)
15. [Configurações do Módulo](#15-configuracoes-do-modulo)
16. [APIs REST](#16-apis-rest)
17. [Schema SQL](#17-schema-sql)
18. [LGPD e Auditoria](#18-lgpd-e-auditoria)
19. [Critérios de Aceite](#19-criterios-de-aceite)

---

#### 1. Visão Geral

##### 1.1 Objetivo
Gerenciar toda a frota de veículos da entidade: cadastro, documentação, motoristas, agendamentos, manutenções, abastecimentos, rotas, multas e custos — com rastreabilidade completa, alertas automáticos e relatórios gerenciais.

##### 1.2 Escopo Funcional
- Cadastro completo de veículos (próprios, locados, terceirizados)
- Gestão de motoristas e CNH com vencimentos
- Reserva e agendamento de veículos por setor/usuário
- Controle de manutenções preventivas e corretivas
- Controle de abastecimentos com custo por km
- Registro de rotas, viagens e quilometragem
- Gestão de multas, sinistros e ocorrências
- Controle de documentos: CRLV, seguro, IPVA, vistoria
- Kanban de status operacional da frota
- Automações de alertas por vencimento e quilometragem
- Relatórios de custo total de propriedade (TCO) por veículo

##### 1.3 Integrações
| Módulo | Tipo | Dados |
|---|---|---|
| Financeiro | Consumo | Custos de manutenção, abastecimento, multas |
| Patrimônio | Bidirecional | Veículo como ativo patrimonial |
| RH/HCM | Consulta | Dados do motorista/colaborador |
| Suprimentos | Consumo | Peças, pneus, insumos |
| Compliance | Publicação | Logs de auditoria, ocorrências |
| Notificações | Consumo | Alertas de vencimento, manutenção |

---

#### 2. Perfis e Permissões RBAC

| Funcionalidade | SA | GE | GF | MOT | MAN | AUD | VIS |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Dashboard completo | ✓ | ✓ | ✓ | — | — | ✓ | ✓ |
| Cadastrar veículo | ✓ | ✓ | — | — | — | — | — |
| Editar veículo | ✓ | ✓ | — | — | — | — | — |
| Excluir veículo | ✓ | — | — | — | — | — | — |
| Ver veículos | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Cadastrar motorista | ✓ | ✓ | — | — | — | — | — |
| Ver motoristas | ✓ | ✓ | ✓ | — | — | ✓ | ✓ |
| Criar reserva | ✓ | ✓ | ✓ | ✓ | — | — | — |
| Aprovar reserva | ✓ | ✓ | — | — | — | — | — |
| Registrar manutenção | ✓ | ✓ | — | — | ✓ | — | — |
| Aprovar manutenção | ✓ | ✓ | ✓ | — | — | — | — |
| Registrar abastecimento | ✓ | ✓ | — | ✓ | — | — | — |
| Registrar rota/viagem | ✓ | ✓ | — | ✓ | — | — | — |
| Registrar multa | ✓ | ✓ | — | — | — | — | — |
| Gerenciar documentos | ✓ | ✓ | — | — | — | — | — |
| Ver relatórios | ✓ | ✓ | ✓ | — | — | ✓ | ✓ |
| Exportar dados | ✓ | ✓ | ✓ | — | — | ✓ | — |
| Configurações | ✓ | ✓ | — | — | — | — | — |
| Kanban operacional | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Automações | ✓ | ✓ | — | — | — | — | — |

**Legenda:** SA = Super Admin · GE = Gestor de Frotas · GF = Gestor Financeiro · MOT = Motorista · MAN = Manutenção · AUD = Auditor · VIS = Visualizador

---

#### 3. Dashboard de Frotas

**Rota:** `GET /frotas/dashboard`  
**Arquivo:** `modules/frotas/dashboard.php`

##### 3.1 Widgets KPI — Linha 1 (Cards grandes)

| # | Widget | Métrica | Cor | Ícone |
|---|---|---|---|---|
| 1 | Total de Veículos | Quantidade total ativa | Azul | `ki-car` |
| 2 | Veículos Disponíveis | Prontos para uso | Verde | `ki-check-circle` |
| 3 | Veículos em Uso | Em rota agora | Amarelo | `ki-geolocation` |
| 4 | Em Manutenção | Parados para manutenção | Laranja | `ki-wrench` |
| 5 | Km Rodados (mês) | Total km no período | Roxo | `ki-route` |
| 6 | Custo Total (mês) | R$ gastos no período | Vermelho | `ki-dollar` |

##### 3.2 Widgets KPI — Linha 2 (Cards médios)

| # | Widget | Métrica |
|---|---|---|
| 1 | Abastecimentos (mês) | Quantidade de abastecimentos |
| 2 | Litros Consumidos | Total litros no período |
| 3 | Custo/km Médio | R$ por km rodado |
| 4 | Manutenções Abertas | Ordens abertas |
| 5 | CNHs a Vencer (30d) | Motoristas com CNH próxima do vencimento |
| 6 | Documentos a Vencer (30d) | CRLV, IPVA, seguro próximos |

##### 3.3 Charts amCharts 5

| # | Chart | Tipo | Dados |
|---|---|---|---|
| 1 | Frota por Status | Donut | Disponível / Em uso / Manutenção / Inativo |
| 2 | Custo Mensal por Categoria | Bar Stacked | Manutenção / Combustível / Multas / Outros |
| 3 | Km Rodados por Veículo | Bar Horizontal | Top 10 veículos por km |
| 4 | Evolução de Custos | Line | Últimos 12 meses |
| 5 | Consumo de Combustível | Area | Litros por semana |
| 6 | Custo por km por Veículo | Scatter | Eficiência por veículo |

##### 3.4 Datatable — Alertas Críticos

**Colunas:** Veículo · Tipo de Alerta · Vencimento · Dias Restantes · Responsável · Ação  
**Filtros:** Tipo · Urgência · Veículo  
**Ações:** Ver Detalhe · Resolver · Atribuir  
**Badges:** CRÍTICO (vermelho < 7d) · URGENTE (amarelo < 30d) · ATENÇÃO (azul < 60d)

##### 3.5 Datatable — Reservas do Dia

**Colunas:** Horário · Veículo · Motorista · Origem → Destino · Status · Ações  
**Filtros:** Status · Veículo · Motorista  
**Ações:** Ver · Aprovar · Rejeitar · Check-in · Check-out

##### 3.6 Painel de Mapa (opcional)
- Integração Google Maps API ou OpenStreetMap
- Pins de veículos em rota (GPS tracker)
- Status por cor: verde/amarelo/vermelho

---

#### 4. Gestão de Veículos

**Rota:** `GET /frotas/veiculos`  
**Arquivo:** `modules/frotas/veiculos/index.php`

##### 4.1 Controles da Página

| Controle | Tipo | Ação |
|---|---|---|
| Novo Veículo | Button primary | Abre Drawer de cadastro |
| Importar CSV | Button secondary | Upload em lote |
| Exportar | Dropdown | Excel / CSV / PDF |
| Filtro de Status | Select múltiplo | Disponível/Em uso/Manutenção/Inativo |
| Filtro de Tipo | Select | Carro/Moto/Caminhão/Van/Ônibus/Outro |
| Filtro de Categoria | Select | Próprio/Locado/Terceirizado |
| Busca | Input text | Placa, modelo, chassis |
| Visualização | Toggle | Tabela / Cards / Mapa |

##### 4.2 Datatable — Veículos

| Coluna | Tipo | Observação |
|---|---|---|
| # | Checkbox | Seleção múltipla |
| Foto | Avatar | Thumbnail do veículo |
| Placa | Badge | Link para detalhe |
| Modelo / Marca | Text | Marca · Modelo · Ano |
| Tipo | Badge | Carro / Moto / etc. |
| Categoria | Badge | Próprio / Locado |
| Status | Badge colorido | Disponível / Em Uso / Manutenção / Inativo |
| Km Atual | Number | Odômetro atual |
| Próx. Manutenção | Date | Km ou data |
| Motorista Atual | Text | Nome do motorista vinculado |
| Ações | Dropdown | Ver · Editar · Manutenção · Desativar |

**Paginação:** 10/25/50/100 por página  
**Ordenação:** Todas as colunas  
**Bulk Actions:** Desativar · Exportar · Transferir unidade

##### 4.3 Drawer — Cadastrar / Editar Veículo

**Título:** Novo Veículo / Editar Veículo  
**Largura:** 700px  
**Abas:** Dados Gerais · Documentação · Fotos · Histórico

###### Aba: Dados Gerais
| Campo | Tipo | Validação |
|---|---|---|
| Foto do veículo | File upload | JPG/PNG max 5MB |
| Placa | Input mask | AAA-0000 ou AAA0A00 (Mercosul), required |
| Tipo | Select | Carro/Moto/Caminhão/Van/Ônibus/Outro, required |
| Categoria | Select | Próprio/Locado/Terceirizado, required |
| Marca | Input / Select | required |
| Modelo | Input | required |
| Ano de Fabricação | Input number | 1900–2030, required |
| Ano do Modelo | Input number | 1900–2030, required |
| Cor | Input + Color picker | required |
| Chassi | Input | 17 chars, único |
| RENAVAM | Input mask | 9–11 dígitos |
| Combustível | Select | Gasolina/Etanol/Flex/Diesel/GNV/Elétrico/Híbrido |
| Capacidade do Tanque (L) | Input number | Mín 1 |
| Km/L médio | Input decimal | Consumo esperado |
| Km Atual (odômetro) | Input number | required |
| Capacidade de passageiros | Input number | |
| Capacidade de carga (kg) | Input number | Se caminhão/van |
| Unidade | Select | Multi-unit, required |
| Responsável | Select | Usuário da unidade |
| Observações | Textarea | Max 1000 chars |
| Status | Toggle | Ativo / Inativo |

###### Aba: Documentação
| Campo | Tipo | Validação |
|---|---|---|
| IPVA — Valor | Input currency | |
| IPVA — Vencimento | Date | |
| IPVA — Status | Select | Pago/Pendente/Isento |
| CRLV — Vencimento | Date | required |
| CRLV — Arquivo | File upload | PDF |
| Seguro — Seguradora | Input | |
| Seguro — Apólice | Input | |
| Seguro — Vencimento | Date | |
| Seguro — Valor | Input currency | |
| Seguro — Arquivo | File upload | PDF |
| Vistoria — Data | Date | |
| Vistoria — Vencimento | Date | |
| Vistoria — Laudo | File upload | PDF |
| Tacógrafo — Validade | Date | Se obrigatório |
| Outros Documentos | Repeater | Nome + Vencimento + Arquivo |

###### Aba: Fotos
- Upload múltiplo (frente, lateral esq/dir, traseira, interior, painel)
- Drag and drop
- Preview grid 3 colunas
- Máximo 20 fotos, 5MB cada

###### Aba: Histórico (somente leitura)
- Timeline de eventos: manutenções, trocas de motorista, abastecimentos, multas
- Filtro por período e tipo de evento

##### 4.4 Drawer — Detalhe do Veículo

**Largura:** 900px  
**Layout:** Sidebar esquerda (foto + status + dados básicos) + Área direita com abas

**Abas da área direita:**
- **Resumo:** KPIs individuais (km total, custo total, custo/km, manutenções realizadas)
- **Manutenções:** Lista histórica + próximas agendadas
- **Abastecimentos:** Histórico com gráfico consumo
- **Rotas:** Viagens realizadas com mapa e km
- **Multas:** Ocorrências vinculadas
- **Documentos:** Todos os docs com status de validade
- **Auditoria:** Log de alterações

---

#### 5. Motoristas e Habilitações

**Rota:** `GET /frotas/motoristas`  
**Arquivo:** `modules/frotas/motoristas/index.php`

##### 5.1 Controles da Página

| Controle | Tipo | Ação |
|---|---|---|
| Novo Motorista | Button primary | Abre Drawer |
| Exportar | Dropdown | Excel / CSV / PDF |
| Filtro de Status CNH | Select | Válida / A vencer / Vencida |
| Filtro de Categoria CNH | Select | A/B/C/D/E |
| Busca | Input text | Nome, CPF, matrícula |

##### 5.2 Datatable — Motoristas

| Coluna | Tipo | Observação |
|---|---|---|
| # | Checkbox | |
| Foto | Avatar | |
| Nome | Text | Link para detalhe |
| CPF | Masked | ***.***.***-** |
| Matrícula | Text | Vínculo com RH |
| CNH Nº | Text | |
| Categoria CNH | Badge | A/B/C/D/E |
| Validade CNH | Date | |
| Status CNH | Badge | Válida (verde) / A Vencer (amarelo) / Vencida (vermelho) |
| Pontuação CNH | Number | Pontos na carteira |
| Veículo Atual | Text | Veículo vinculado |
| Status | Badge | Ativo / Inativo / Suspenso |
| Ações | Dropdown | Ver · Editar · Suspender |

##### 5.3 Drawer — Cadastrar / Editar Motorista

**Abas:** Dados Pessoais · CNH e Habilitação · Treinamentos · Histórico

###### Aba: Dados Pessoais
| Campo | Tipo | Validação |
|---|---|---|
| Foto | File upload | |
| Vínculo com colaborador | Select search | Busca em RH/HCM |
| Nome completo | Input | required |
| CPF | Input mask | Validação dígito, required |
| Data de nascimento | Date | required |
| Telefone | Input mask | |
| E-mail | Input email | |
| Endereço | Input | |
| Tipo de vínculo | Select | CLT / PJ / Autônomo / Terceirizado |
| Unidade | Select | Multi-unit |
| Status | Select | Ativo / Inativo / Suspenso |

###### Aba: CNH e Habilitação
| Campo | Tipo | Validação |
|---|---|---|
| Número da CNH | Input | required |
| Categoria | Select múltiplo | A/B/C/D/E, required |
| Data de emissão | Date | required |
| Data de validade | Date | required |
| Data 1ª habilitação | Date | |
| Órgão emissor (DETRAN UF) | Select | |
| Pontuação atual | Input number | 0–40 |
| Observações infrações | Textarea | |
| Scan da CNH (frente) | File upload | JPG/PDF |
| Scan da CNH (verso) | File upload | JPG/PDF |
| EAR (Exerce Atividade Remunerada) | Toggle | |
| Cursos adicionais | Repeater | MOPP, Transporte Escolar, etc. |

###### Aba: Treinamentos
| Campo | Tipo |
|---|---|
| Nome do treinamento | Input |
| Instituição | Input |
| Data de realização | Date |
| Validade | Date |
| Certificado | File upload |

###### Aba: Histórico (somente leitura)
- Veículos conduzidos
- Rotas realizadas
- Multas recebidas
- Manutenções solicitadas

---

#### 6. Agendamentos e Reservas

**Rota:** `GET /frotas/agendamentos`  
**Arquivo:** `modules/frotas/agendamentos/index.php`

##### 6.1 Controles da Página

| Controle | Tipo | Ação |
|---|---|---|
| Nova Reserva | Button primary | Abre Drawer |
| Exportar | Dropdown | Excel / PDF |
| Visualização | Toggle | Tabela / Calendário / Timeline |
| Filtro de Status | Select | Pendente/Aprovado/Em andamento/Concluído/Cancelado |
| Filtro de Veículo | Select search | |
| Filtro de Motorista | Select search | |
| Filtro de Período | Date range | |

##### 6.2 Datatable — Reservas

| Coluna | Tipo | Observação |
|---|---|---|
| # | Checkbox | |
| ID Reserva | Text | REV-000001 |
| Solicitante | Text | |
| Veículo | Text | Placa + Modelo |
| Motorista | Text | |
| Data/Hora Saída | DateTime | |
| Data/Hora Retorno | DateTime | |
| Destino | Text | |
| Finalidade | Badge | Serviço / Entrega / Institucional / Pessoal |
| KM Estimado | Number | |
| Status | Badge | Pendente/Aprovado/Em andamento/Concluído/Cancelado |
| Ações | Dropdown | Ver · Aprovar · Rejeitar · Check-in · Check-out · Cancelar |

##### 6.3 Visualização Calendário
- FullCalendar.js integrado
- View: Mensal / Semanal / Diário
- Cor por veículo ou por status
- Clique no evento abre Drawer de detalhe
- Drag & Drop para reagendar (GE/SA)

##### 6.4 Visualização Timeline (Gantt)
- Eixo Y: Veículos
- Eixo X: Tempo
- Barras coloridas por status
- Detecta conflito de agendamento

##### 6.5 Drawer — Nova Reserva / Editar

| Campo | Tipo | Validação |
|---|---|---|
| Solicitante | Select search / auto | Usuário logado ou selecionar, required |
| Setor / Departamento | Select | required |
| Veículo | Select search | Mostra disponíveis no período, required |
| Motorista | Select search | required |
| Finalidade | Select | required |
| Destino (endereço) | Input + mapa | |
| Data/Hora de Saída | DateTime | required |
| Data/Hora de Retorno | DateTime | required |
| KM estimado | Input number | |
| Passageiros | Input number | Máx = capacidade do veículo |
| Nomes dos passageiros | Repeater | |
| Aprovador responsável | Select | Auto por unidade |
| Observações | Textarea | |
| Documentos de suporte | File upload múltiplo | |

**Validações automáticas:**
- Conflito de horário do veículo → bloqueia + exibe alerta
- CNH vencida do motorista → bloqueia + exibe alerta
- Veículo em manutenção → bloqueia + sugere alternativo

##### 6.6 Drawer — Check-in / Check-out

**Check-in:**
| Campo | Tipo |
|---|---|
| KM saída (odômetro) | Input number, required |
| Nível de combustível | Select (1/4, 1/2, 3/4, Cheio) |
| Condições do veículo | Checklist (lataria, pneus, vidros, interior) |
| Fotos no momento da saída | Upload múltiplo |
| Assinatura digital | Canvas / Pad |

**Check-out:**
| Campo | Tipo |
|---|---|
| KM chegada (odômetro) | Input number, required |
| Nível de combustível | Select |
| Ocorrências durante viagem | Textarea |
| Fotos retorno | Upload múltiplo |
| Avaliação do motorista | Stars 1–5 |
| Assinatura digital | Canvas / Pad |

---

#### 7. Manutenções e Revisões

**Rota:** `GET /frotas/manutencoes`  
**Arquivo:** `modules/frotas/manutencoes/index.php`

##### 7.1 Controles da Página

| Controle | Tipo | Ação |
|---|---|---|
| Nova OS de Manutenção | Button primary | Abre Drawer |
| Exportar | Dropdown | Excel / PDF |
| Filtro de Tipo | Select | Preventiva / Corretiva / Emergencial |
| Filtro de Status | Select | Aberta / Em execução / Aguardando peça / Concluída / Cancelada |
| Filtro de Veículo | Select search | |
| Filtro de Período | Date range | |

##### 7.2 Datatable — Ordens de Manutenção

| Coluna | Tipo | Observação |
|---|---|---|
| # | Checkbox | |
| OS Nº | Text | OS-000001 |
| Veículo | Text | Placa + Modelo |
| Tipo | Badge | Preventiva / Corretiva / Emergencial |
| Descrição resumida | Text | |
| Fornecedor / Oficina | Text | |
| Abertura | Date | |
| Previsão conclusão | Date | |
| Conclusão real | Date | |
| Custo total (R$) | Currency | |
| Status | Badge colorido | |
| Ações | Dropdown | Ver · Editar · Concluir · Cancelar |

##### 7.3 Charts — Manutenções

| Chart | Tipo | Dados |
|---|---|---|
| Custo por tipo de manutenção | Donut | Preventiva vs Corretiva vs Emergencial |
| Top 10 veículos por custo | Bar horizontal | Custo acumulado |
| Tempo médio de parada | Bar | Por tipo de manutenção |
| Frequência mensal | Line | Qtd OS por mês |

##### 7.4 Drawer — Nova OS de Manutenção

**Abas:** Dados Gerais · Serviços e Peças · Financeiro · Histórico

###### Aba: Dados Gerais
| Campo | Tipo | Validação |
|---|---|---|
| Veículo | Select search | required |
| Tipo de manutenção | Select | Preventiva/Corretiva/Emergencial, required |
| Descrição do problema | Textarea | required |
| KM no momento da abertura | Input number | required |
| Próxima manutenção em KM | Input number | |
| Fornecedor / Oficina | Select search + criar | |
| Responsável interno | Select | |
| Data de abertura | Date | Auto: hoje |
| Previsão de conclusão | Date | |
| Prioridade | Select | Baixa / Normal / Alta / Crítica |
| Defeitos observados | Checklist | Motor / Freios / Suspensão / Elétrica / Outros |
| Fotos do defeito | Upload múltiplo | |
| Observações | Textarea | |

###### Aba: Serviços e Peças
- **Tabela de serviços:** Descrição · Tempo estimado (h) · Valor mão de obra
- **Tabela de peças/insumos:** Item · Quantidade · Valor unitário · Valor total
- **Totais automáticos:** Mão de obra + Peças = Total OS
- Integração com Suprimentos para baixa de estoque

###### Aba: Financeiro
| Campo | Tipo |
|---|---|
| Centro de custo | Select |
| Conta contábil | Select |
| Forma de pagamento | Select |
| Número NF | Input |
| Arquivo NF | File upload |
| Data de pagamento | Date |
| Valor pago | Input currency |

###### Aba: Histórico
- Últimas 10 manutenções do veículo
- Gráfico custo histórico por manutenção

##### 7.5 Drawer — Plano de Manutenção Preventiva

| Campo | Tipo | Validação |
|---|---|---|
| Veículo | Select | required |
| Tipo de serviço | Select | Troca óleo / Filtros / Pneus / Revisão geral / Outro |
| Periodicidade | Select | KM / Meses |
| Intervalo (KM ou meses) | Input number | |
| Próxima execução (KM) | Input number | |
| Próxima execução (data) | Date | |
| Alertar com antecedência (KM) | Input number | Ex: 500 km antes |
| Alertar com antecedência (dias) | Input number | Ex: 15 dias antes |
| Responsável | Select | |
| Observações | Textarea | |

---

#### 8. Abastecimentos e Combustível

**Rota:** `GET /frotas/abastecimentos`  
**Arquivo:** `modules/frotas/abastecimentos/index.php`

##### 8.1 Controles da Página

| Controle | Tipo | Ação |
|---|---|---|
| Registrar Abastecimento | Button primary | Abre Drawer |
| Exportar | Dropdown | Excel / CSV / PDF |
| Filtro de Veículo | Select search | |
| Filtro de Motorista | Select search | |
| Filtro de Combustível | Select | Gasolina/Etanol/Diesel/GNV/Elétrico |
| Filtro de Período | Date range | |
| Filtro de Posto | Select / input | |

##### 8.2 Datatable — Abastecimentos

| Coluna | Tipo | Observação |
|---|---|---|
| # | Checkbox | |
| Data/Hora | DateTime | |
| Veículo | Text | Placa + Modelo |
| Motorista | Text | |
| Combustível | Badge | |
| Litros | Number | |
| Valor/L (R$) | Currency | |
| Total (R$) | Currency | |
| KM no abastecimento | Number | |
| KM percorrido | Number | Calculado: KM atual - KM anterior |
| Consumo (KM/L) | Decimal | Calculado |
| Posto | Text | |
| Cupom fiscal | Link | Download |
| Ações | Dropdown | Ver · Editar · Excluir |

##### 8.3 Widgets — Combustível

| Widget | Dados |
|---|---|
| Gasto total (mês) | R$ total abastecimentos |
| Litros consumidos | Total litros no período |
| Média KM/L da frota | Consumo médio geral |
| Custo médio/L | Preço médio pago por litro |

##### 8.4 Charts — Combustível

| Chart | Tipo | Dados |
|---|---|---|
| Gasto por combustível | Donut | Gasolina / Etanol / Diesel |
| Consumo semanal | Bar | Litros por semana |
| Custo/L ao longo do tempo | Line | Evolução do preço |
| KM/L por veículo | Bar horizontal | Eficiência por veículo |

##### 8.5 Drawer — Registrar Abastecimento

| Campo | Tipo | Validação |
|---|---|---|
| Veículo | Select search | required |
| Motorista | Select search | Auto pelo veículo, editável |
| Data/Hora | DateTime | Auto: agora, required |
| KM atual (odômetro) | Input number | required |
| Tipo de combustível | Select | required |
| Litros abastecidos | Input decimal | required |
| Valor por litro (R$) | Input currency | required |
| Valor total (R$) | Input currency | Calculado automaticamente |
| Posto / Fornecedor | Input / Select | |
| Número do cupom fiscal | Input | |
| Foto do cupom | File upload | JPG/PNG |
| Tanque cheio? | Toggle | Sim/Não |
| Observações | Textarea | |

---

#### 9. Rotas e Viagens

**Rota:** `GET /frotas/rotas`  
**Arquivo:** `modules/frotas/rotas/index.php`

##### 9.1 Controles da Página

| Controle | Tipo | Ação |
|---|---|---|
| Nova Rota | Button primary | Abre Drawer (rota pré-definida) |
| Registrar Viagem | Button secondary | Abre Drawer de viagem avulsa |
| Exportar | Dropdown | Excel / PDF |
| Filtro de Status | Select | Planejada / Em andamento / Concluída / Cancelada |
| Filtro de Veículo | Select search | |
| Filtro de Motorista | Select search | |
| Filtro de Período | Date range | |

##### 9.2 Datatable — Viagens

| Coluna | Tipo | Observação |
|---|---|---|
| # | Checkbox | |
| Código | Text | VIA-000001 |
| Veículo | Text | |
| Motorista | Text | |
| Origem | Text | |
| Destino | Text | |
| Saída | DateTime | |
| Chegada | DateTime | |
| KM Percorrido | Number | |
| Custo estimado (R$) | Currency | Combustível estimado |
| Passageiros | Number | |
| Status | Badge | |
| Ações | Dropdown | Ver · Editar · Iniciar · Finalizar · Cancelar |

##### 9.3 Drawer — Registrar Viagem / Rota

| Campo | Tipo | Validação |
|---|---|---|
| Tipo | Select | Viagem avulsa / Rota recorrente |
| Vinculada à reserva | Select search | Opcional |
| Veículo | Select search | required |
| Motorista | Select search | required |
| Origem (endereço) | Input + autocomplete | required |
| Destino (endereço) | Input + autocomplete | required |
| Paradas intermediárias | Repeater | Endereço + Tempo estimado |
| KM saída | Input number | required |
| KM chegada | Input number | Preenchido no encerramento |
| Data/Hora saída | DateTime | required |
| Data/Hora chegada estimada | DateTime | |
| Data/Hora chegada real | DateTime | Preenchido no encerramento |
| Finalidade | Select | |
| Passageiros | Repeater | Nome + CPF |
| Pedágios (R$) | Input currency | |
| Estacionamento (R$) | Input currency | |
| Outras despesas | Repeater | Descrição + Valor |
| Observações | Textarea | |
| Comprovantes | File upload múltiplo | |

---

#### 10. Multas e Ocorrências

**Rota:** `GET /frotas/multas`  
**Arquivo:** `modules/frotas/multas/index.php`

##### 10.1 Controles da Página

| Controle | Tipo | Ação |
|---|---|---|
| Registrar Multa | Button primary | Abre Drawer |
| Registrar Sinistro | Button secondary | Abre Drawer |
| Exportar | Dropdown | Excel / PDF |
| Filtro de Tipo | Select | Multa / Sinistro / Avaria |
| Filtro de Status | Select | Aberta / Em recurso / Paga / Cancelada |
| Filtro de Veículo | Select search | |
| Filtro de Período | Date range | |

##### 10.2 Datatable — Multas e Ocorrências

| Coluna | Tipo | Observação |
|---|---|---|
| # | Checkbox | |
| Tipo | Badge | Multa / Sinistro / Avaria |
| Auto de Infração / Nº | Text | |
| Veículo | Text | |
| Motorista | Text | |
| Data da Ocorrência | Date | |
| Infração / Descrição | Text | |
| Órgão autuador | Text | DETRAN / PRF / etc. |
| Valor (R$) | Currency | |
| Vencimento | Date | |
| Status | Badge | |
| Ações | Dropdown | Ver · Editar · Recurso · Pagar · Cancelar |

##### 10.3 Drawer — Registrar Multa

| Campo | Tipo | Validação |
|---|---|---|
| Tipo | Select | Multa / Sinistro / Avaria, required |
| Veículo | Select search | required |
| Motorista na época | Select search | required |
| Auto de infração Nº | Input | |
| Data/Hora da ocorrência | DateTime | required |
| Órgão autuador | Input | |
| Código da infração | Input | |
| Descrição da infração | Textarea | required |
| Valor original (R$) | Input currency | |
| Valor com desconto (R$) | Input currency | |
| Vencimento para pagamento | Date | |
| Pontos na CNH | Input number | |
| Status | Select | Aberta / Em recurso / Paga / Cancelada |
| Responsável pelo pagamento | Select | Empresa / Motorista |
| Descontar do motorista? | Toggle | |
| Arquivo da notificação | File upload | PDF |
| Observações | Textarea | |

---

#### 11. Documentos e Licenciamentos

**Rota:** `GET /frotas/documentos`  
**Arquivo:** `modules/frotas/documentos/index.php`

##### 11.1 Controles da Página

| Controle | Tipo | Ação |
|---|---|---|
| Novo Documento | Button primary | Abre Drawer |
| Filtro de Tipo | Select | CRLV / IPVA / Seguro / Vistoria / Tacógrafo / Outro |
| Filtro de Status | Select | Válido / A vencer / Vencido |
| Filtro de Veículo | Select search | |
| Busca | Input text | |

##### 11.2 Datatable — Documentos

| Coluna | Tipo | Observação |
|---|---|---|
| # | Checkbox | |
| Tipo | Badge | |
| Veículo | Text | |
| Descrição | Text | |
| Emissão | Date | |
| Vencimento | Date | |
| Dias restantes | Number | Badge colorido |
| Valor (R$) | Currency | IPVA, seguro |
| Arquivo | Link | Download |
| Status | Badge | Válido / A vencer / Vencido |
| Ações | Dropdown | Ver · Editar · Renovar · Excluir |

##### 11.3 Drawer — Cadastrar Documento

| Campo | Tipo | Validação |
|---|---|---|
| Veículo | Select search | required |
| Tipo de documento | Select | required |
| Descrição | Input | |
| Número / Código | Input | |
| Data de emissão | Date | |
| Data de vencimento | Date | required |
| Órgão emissor | Input | |
| Valor (R$) | Input currency | |
| Arquivo | File upload | PDF, required |
| Alertar antes de vencer | Input number | Dias de antecedência |
| Renovação automática? | Toggle | |
| Observações | Textarea | |

---

#### 12. Kanban Operacional

**Rota:** `GET /frotas/kanban`  
**Arquivo:** `modules/frotas/kanban/index.php`

##### 12.1 Kanban — Status de Veículos

**Colunas:**

| Coluna | Cor | Descrição |
|---|---|---|
| 🟢 Disponível | Verde | Veículo pronto para uso |
| 🟡 Reservado | Amarelo | Reserva aprovada aguardando saída |
| 🔵 Em Rota | Azul | Veículo em viagem ativa |
| 🟠 Manutenção | Laranja | Em manutenção preventiva ou corretiva |
| 🔴 Indisponível | Vermelho | Avaria, sinistro ou suspensão |
| ⚫ Inativo | Cinza | Desativado temporária ou permanentemente |

**Cards contêm:**
- Foto miniatura do veículo
- Placa + Modelo
- Motorista atual (se aplicável)
- Km atual
- Próxima manutenção (alerta se < 500 km)
- Documentos a vencer (badge)
- Menu rápido: Ver · Mover · Agendar Manutenção

**Controles:**
- Drag & Drop para mover entre colunas (com confirmação + log)
- Filtro por tipo de veículo
- Filtro por responsável
- Busca por placa/modelo
- Toggle: Visualização Compacta / Expandida

##### 12.2 Kanban — Manutenções

**Colunas:**

| Coluna | Cor |
|---|---|
| 📋 Solicitada | Cinza |
| ✅ Aprovada | Azul |
| 🔧 Em execução | Amarelo |
| ⏳ Aguardando Peça | Laranja |
| ✔️ Concluída | Verde |
| ❌ Cancelada | Vermelho |

**Cards contêm:**
- Número da OS
- Veículo (Placa + Modelo)
- Tipo (Preventiva/Corretiva/Emergencial)
- Fornecedor / Oficina
- Custo estimado
- Data prevista conclusão
- SLA (badge: no prazo / atrasado)
- Responsável

##### 12.3 Kanban — Reservas

**Colunas:**

| Coluna | Cor |
|---|---|
| 📩 Solicitada | Cinza |
| ⏳ Aguardando Aprovação | Amarelo |
| ✅ Aprovada | Verde |
| 🚗 Em andamento | Azul |
| 🏁 Concluída | Verde escuro |
| ❌ Rejeitada / Cancelada | Vermelho |

---

#### 13. Automações e Alertas

**Rota:** `GET /frotas/automacoes`  
**Arquivo:** `modules/frotas/automacoes/index.php`

##### 13.1 Automações Disponíveis

| # | Gatilho | Ação Automática | Canal |
|---|---|---|---|
| 1 | CNH do motorista vence em X dias | Alerta para gestor + motorista | E-mail / Push / Sistema |
| 2 | CRLV vence em X dias | Alerta para gestor | E-mail / Push |
| 3 | Seguro vence em X dias | Alerta para gestor + financeiro | E-mail / Push |
| 4 | IPVA vence em X dias | Alerta + cria despesa no financeiro | E-mail / Sistema |
| 5 | KM de manutenção atingido | Abre OS preventiva automaticamente | Sistema |
| 6 | Manutenção vence em X dias | Alerta para responsável | E-mail / Push |
| 7 | Veículo em manutenção há > X dias | Escalada para gestor | E-mail |
| 8 | Reserva aprovada | Notifica solicitante + motorista | E-mail / Push / SMS |
| 9 | Reserva rejeitada | Notifica solicitante com motivo | E-mail / Push |
| 10 | Check-in realizado | Notifica gestor | Sistema |
| 11 | Check-out não realizado no prazo | Alerta para gestor + motorista | E-mail / Push |
| 12 | Multa registrada | Notifica gestor + motorista | E-mail / Sistema |
| 13 | Consumo anômalo detectado | Alerta (KM/L fora do padrão > 20%) | E-mail / Sistema |
| 14 | Vistoria vence em X dias | Alerta para gestor | E-mail |
| 15 | Custo mensal > limite definido | Alerta para gestor financeiro | E-mail / Push |

##### 13.2 Drawer — Configurar Automação

| Campo | Tipo |
|---|---|
| Gatilho | Select (lista acima) |
| Veículo(s) afetado(s) | Select múltiplo / Todos |
| Antecedência (dias/km) | Input number |
| Canal de notificação | Checkbox múltiplo: E-mail / Push / SMS / Sistema |
| Destinatários | Select múltiplo (perfis/usuários) |
| Mensagem personalizada | Textarea (com variáveis: {veiculo}, {data}, {motorista}) |
| Ativa? | Toggle |
| Frequência de repetição | Select: Única / Diária / Semanal |

##### 13.3 Log de Automações

**Datatable:**
| Coluna | Tipo |
|---|---|
| Data/Hora | DateTime |
| Automação | Text |
| Veículo | Text |
| Destinatários | Text |
| Status | Badge: Enviado / Falha / Ignorado |
| Canal | Badge |
| Ações | Ver detalhe |

---

#### 14. Relatórios e Exportações

**Rota:** `GET /frotas/relatorios`  
**Arquivo:** `modules/frotas/relatorios/index.php`

##### 14.1 Relatórios Disponíveis

| # | Relatório | Filtros | Exportação |
|---|---|---|---|
| 1 | Custo Total por Veículo (TCO) | Período / Veículo / Tipo | Excel / PDF |
| 2 | Custo por Categoria | Período / Tipo (combustível, manutenção, multa) | Excel / PDF |
| 3 | KM Rodados por Veículo | Período / Veículo | Excel / PDF |
| 4 | Consumo de Combustível | Período / Veículo / Motorista | Excel / PDF |
| 5 | Histórico de Manutenções | Período / Veículo / Tipo | Excel / PDF |
| 6 | Multas e Ocorrências | Período / Veículo / Motorista | Excel / PDF |
| 7 | Utilização da Frota | Período / Veículo | Excel / PDF |
| 8 | Vencimentos Futuros | Tipo / Antecedência | Excel / PDF |
| 9 | Desempenho por Motorista | Período / Motorista | Excel / PDF |
| 10 | Relatório de Viagens | Período / Veículo / Motorista | Excel / PDF |
| 11 | Dashboard Executivo (PDF) | Período | PDF |
| 12 | Planilha de Depreciação | Período / Veículo | Excel |

##### 14.2 Charts nos Relatórios

| Relatório | Charts inclusos |
|---|---|
| TCO | Bar empilhada mês a mês + Donut por categoria de custo |
| Combustível | Line consumo + Bar custo por veículo |
| Manutenções | Bar tipo + Line frequência mensal |
| Utilização | Heat map dias × veículos |
| Motorista | Radar: km / consumo / multas / avaliação |

---

#### 15. Configurações do Módulo

**Rota:** `GET /frotas/configuracoes`  
**Arquivo:** `modules/frotas/configuracoes/index.php`

##### 15.1 Abas de Configuração

| Aba | Conteúdo |
|---|---|
| Geral | Nome do módulo, unidade, moeda, fuso horário |
| Tipos de Veículo | CRUD: Carro, Moto, Caminhão, Van, Ônibus, Outro |
| Categorias de Custo | CRUD: Combustível, Manutenção, Multa, Seguro, IPVA, Outros |
| Fornecedores/Oficinas | CRUD: Nome, CNPJ, contato, especialidade, avaliação |
| Postos de Combustível | CRUD: Nome, endereço, combustíveis disponíveis |
| Tipos de Manutenção | CRUD: Preventiva, Corretiva, Emergencial + serviços padrão |
| Regras de Aprovação | Fluxo de aprovação de reservas por valor/perfil |
| Alertas | Antecedências padrão por tipo de vencimento |
| Integrações | Financeiro, Patrimônio, RH, GPS Tracker |
| Limites de Custo | Alertas por veículo / frota / período |

##### 15.2 Drawer — Regras de Aprovação de Reservas

| Campo | Tipo |
|---|---|
| Condição | Select: Sempre / KM > X / Fora do horário comercial / Fins de semana |
| Aprovador 1 | Select (usuário/perfil) |
| Aprovador 2 (opcional) | Select |
| Prazo para aprovação (h) | Input number |
| Ação se não aprovado no prazo | Select: Aprovação automática / Rejeição automática / Escalada |

---

#### 16. APIs REST

**Base URL:** `/api/v1/frotas`  
**Auth:** Bearer JWT  
**Headers:** `Content-Type: application/json · X-Entity-ID · X-Unit-ID`

##### 16.1 Veículos

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/veiculos` | Listar veículos (paginated) | GE+ |
| GET | `/veiculos/{id}` | Detalhe do veículo | GE+ |
| POST | `/veiculos` | Cadastrar veículo | GE+ |
| PUT | `/veiculos/{id}` | Editar veículo | GE+ |
| DELETE | `/veiculos/{id}` | Desativar veículo | SA |
| GET | `/veiculos/{id}/historico` | Histórico completo | GE+ |
| GET | `/veiculos/{id}/documentos` | Documentos do veículo | GE+ |
| GET | `/veiculos/disponiveis` | Veículos disponíveis no período | GE+ |
| POST | `/veiculos/{id}/fotos` | Upload de fotos | GE+ |

##### 16.2 Motoristas

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/motoristas` | Listar motoristas | GE+ |
| GET | `/motoristas/{id}` | Detalhe do motorista | GE+ |
| POST | `/motoristas` | Cadastrar motorista | GE+ |
| PUT | `/motoristas/{id}` | Editar motorista | GE+ |
| DELETE | `/motoristas/{id}` | Desativar motorista | SA |
| GET | `/motoristas/{id}/historico` | Viagens e multas | GE+ |

##### 16.3 Reservas e Agendamentos

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/reservas` | Listar reservas | GE+ |
| GET | `/reservas/{id}` | Detalhe da reserva | GE+ |
| POST | `/reservas` | Criar reserva | MOT+ |
| PUT | `/reservas/{id}` | Editar reserva | MOT+ |
| POST | `/reservas/{id}/aprovar` | Aprovar reserva | GE+ |
| POST | `/reservas/{id}/rejeitar` | Rejeitar reserva | GE+ |
| POST | `/reservas/{id}/checkin` | Realizar check-in | MOT+ |
| POST | `/reservas/{id}/checkout` | Realizar check-out | MOT+ |
| DELETE | `/reservas/{id}` | Cancelar reserva | GE+ |

##### 16.4 Manutenções

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/manutencoes` | Listar OS | GE+ |
| GET | `/manutencoes/{id}` | Detalhe OS | GE+ |
| POST | `/manutencoes` | Criar OS | MAN+ |
| PUT | `/manutencoes/{id}` | Editar OS | MAN+ |
| POST | `/manutencoes/{id}/concluir` | Concluir OS | MAN+ |
| DELETE | `/manutencoes/{id}` | Cancelar OS | GE+ |

##### 16.5 Abastecimentos

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/abastecimentos` | Listar | GE+ |
| POST | `/abastecimentos` | Registrar | MOT+ |
| PUT | `/abastecimentos/{id}` | Editar | GE+ |
| DELETE | `/abastecimentos/{id}` | Excluir | GE+ |

##### 16.6 Rotas e Viagens

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/viagens` | Listar viagens | GE+ |
| POST | `/viagens` | Registrar viagem | MOT+ |
| PUT | `/viagens/{id}` | Atualizar viagem | MOT+ |
| POST | `/viagens/{id}/finalizar` | Finalizar viagem | MOT+ |

##### 16.7 Multas

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/multas` | Listar | GE+ |
| POST | `/multas` | Registrar | GE+ |
| PUT | `/multas/{id}` | Editar | GE+ |
| POST | `/multas/{id}/pagar` | Marcar como paga | GF+ |

##### 16.8 Dashboard e Relatórios

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/dashboard` | KPIs e dados do dashboard | GE+ |
| GET | `/relatorios/tco` | Custo total de propriedade | GE+ |
| GET | `/relatorios/combustivel` | Relatório de combustível | GE+ |
| GET | `/relatorios/manutencoes` | Relatório de manutenções | GE+ |
| GET | `/relatorios/utilizacao` | Utilização da frota | GE+ |
| GET | `/relatorios/motoristas` | Desempenho motoristas | GE+ |

---

#### 17. Schema SQL
```sql
-- ============================================================
-- MÓDULO FROTAS — Schema MariaDB/InnoDB
-- Multi-entity · Multi-unit · UUID · Soft Delete
-- ============================================================

-- Veículos
CREATE TABLE flt_vehicles (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    plate           VARCHAR(8) NOT NULL,
    type            ENUM('car','motorcycle','truck','van','bus','other') NOT NULL,
    category        ENUM('own','leased','outsourced') NOT NULL DEFAULT 'own',
    brand           VARCHAR(100) NOT NULL,
    model           VARCHAR(100) NOT NULL,
    year_manufacture YEAR NOT NULL,
    year_model      YEAR NOT NULL,
    color           VARCHAR(50),
    chassis         VARCHAR(17) UNIQUE,
    renavam         VARCHAR(11) UNIQUE,
    fuel_type       ENUM('gasoline','ethanol','flex','diesel','gnv','electric','hybrid') NOT NULL,
    tank_capacity   DECIMAL(8,2),
    avg_consumption DECIMAL(8,2) COMMENT 'km/L esperado',
    odometer_current BIGINT UNSIGNED DEFAULT 0,
    passenger_capacity TINYINT UNSIGNED,
    cargo_capacity  DECIMAL(10,2),
    responsible_user_id BIGINT UNSIGNED,
    photo_main      VARCHAR(500),
    status          ENUM('available','in_use','maintenance','unavailable','inactive') DEFAULT 'available',
    notes           TEXT,
    deleted_at      DATETIME NULL,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_entity_unit (entity_id, unit_id),
    INDEX idx_plate (plate),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Motoristas
CREATE TABLE flt_drivers (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    user_id         BIGINT UNSIGNED COMMENT 'Vínculo com users',
    name            VARCHAR(200) NOT NULL,
    cpf             CHAR(11) NOT NULL,
    birth_date      DATE,
    phone           VARCHAR(20),
    email           VARCHAR(200),
    address         TEXT,
    link_type       ENUM('clt','pj','autonomous','outsourced') DEFAULT 'clt',
    cnh_number      VARCHAR(20) NOT NULL,
    cnh_category    SET('A','B','C','D','E') NOT NULL,
    cnh_issued_at   DATE,
    cnh_expires_at  DATE NOT NULL,
    cnh_first_date  DATE,
    cnh_detran_uf   CHAR(2),
    cnh_points      TINYINT UNSIGNED DEFAULT 0,
    cnh_ear         TINYINT(1) DEFAULT 0,
    status          ENUM('active','inactive','suspended') DEFAULT 'active',
    notes           TEXT,
    deleted_at      DATETIME NULL,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_cpf_entity (cpf, entity_id),
    INDEX idx_entity_unit (entity_id, unit_id),
    INDEX idx_cnh_expires (cnh_expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reservas
CREATE TABLE flt_reservations (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(20) NOT NULL UNIQUE,
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    vehicle_id      BIGINT UNSIGNED NOT NULL,
    driver_id       BIGINT UNSIGNED NOT NULL,
    requester_id    BIGINT UNSIGNED NOT NULL,
    approver_id     BIGINT UNSIGNED,
    department      VARCHAR(100),
    purpose         ENUM('service','delivery','institutional','personal','other') NOT NULL,
    destination     TEXT,
    departure_at    DATETIME NOT NULL,
    return_at       DATETIME NOT NULL,
    km_estimated    INT UNSIGNED,
    passengers_count TINYINT UNSIGNED DEFAULT 0,
    passengers_list JSON,
    status          ENUM('pending','approved','in_progress','completed','rejected','cancelled') DEFAULT 'pending',
    rejection_reason TEXT,
    checkin_km      BIGINT UNSIGNED,
    checkin_fuel    ENUM('1/4','1/2','3/4','full'),
    checkin_at      DATETIME,
    checkout_km     BIGINT UNSIGNED,
    checkout_fuel   ENUM('1/4','1/2','3/4','full'),
    checkout_at     DATETIME,
    driver_rating   TINYINT UNSIGNED,
    notes           TEXT,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES flt_vehicles(id),
    FOREIGN KEY (driver_id) REFERENCES flt_drivers(id),
    INDEX idx_entity_unit (entity_id, unit_id),
    INDEX idx_status (status),
    INDEX idx_departure (departure_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Manutenções
CREATE TABLE flt_maintenances (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(20) NOT NULL UNIQUE,
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    vehicle_id      BIGINT UNSIGNED NOT NULL,
    type            ENUM('preventive','corrective','emergency') NOT NULL,
    description     TEXT NOT NULL,
    odometer_at_open BIGINT UNSIGNED,
    next_maintenance_km BIGINT UNSIGNED,
    supplier_id     BIGINT UNSIGNED,
    responsible_id  BIGINT UNSIGNED,
    priority        ENUM('low','normal','high','critical') DEFAULT 'normal',
    opened_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    estimated_close DATETIME,
    closed_at       DATETIME,
    labor_cost      DECIMAL(12,2) DEFAULT 0,
    parts_cost      DECIMAL(12,2) DEFAULT 0,
    total_cost      DECIMAL(12,2) GENERATED ALWAYS AS (labor_cost + parts_cost) STORED,
    cost_center     VARCHAR(50),
    invoice_number  VARCHAR(50),
    status          ENUM('open','in_progress','waiting_parts','completed','cancelled') DEFAULT 'open',
    notes           TEXT,
    deleted_at      DATETIME NULL,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES flt_vehicles(id),
    INDEX idx_entity_unit (entity_id, unit_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Itens de Manutenção (serviços e peças)
CREATE TABLE flt_maintenance_items (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    maintenance_id  BIGINT UNSIGNED NOT NULL,
    item_type       ENUM('service','part') NOT NULL,
    description     VARCHAR(300) NOT NULL,
    quantity        DECIMAL(10,3) DEFAULT 1,
    unit_price      DECIMAL(12,2) DEFAULT 0,
    total_price     DECIMAL(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (maintenance_id) REFERENCES flt_maintenances(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Abastecimentos
CREATE TABLE flt_refueling (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    vehicle_id      BIGINT UNSIGNED NOT NULL,
    driver_id       BIGINT UNSIGNED,
    fueled_at       DATETIME NOT NULL,
    odometer        BIGINT UNSIGNED NOT NULL,
    km_since_last   BIGINT UNSIGNED,
    fuel_type       ENUM('gasoline','ethanol','flex','diesel','gnv','electric') NOT NULL,
    liters          DECIMAL(10,3) NOT NULL,
    price_per_liter DECIMAL(8,3) NOT NULL,
    total_cost      DECIMAL(12,2) GENERATED ALWAYS AS (liters * price_per_liter) STORED,
    consumption     DECIMAL(8,2) COMMENT 'km/L calculado',
    full_tank       TINYINT(1) DEFAULT 1,
    supplier        VARCHAR(200),
    receipt_number  VARCHAR(100),
    notes           TEXT,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES flt_vehicles(id),
    INDEX idx_entity_unit (entity_id, unit_id),
    INDEX idx_fueled_at (fueled_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Viagens
CREATE TABLE flt_trips (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(20) NOT NULL UNIQUE,
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    vehicle_id      BIGINT UNSIGNED NOT NULL,
    driver_id       BIGINT UNSIGNED NOT NULL,
    reservation_id  BIGINT UNSIGNED,
    origin          TEXT NOT NULL,
    destination     TEXT NOT NULL,
    stops           JSON,
    departure_km    BIGINT UNSIGNED,
    arrival_km      BIGINT UNSIGNED,
    km_traveled     BIGINT UNSIGNED GENERATED ALWAYS AS (IF(arrival_km > departure_km, arrival_km - departure_km, NULL)) STORED,
    departed_at     DATETIME,
    estimated_arrival DATETIME,
    arrived_at      DATETIME,
    purpose         VARCHAR(200),
    passengers      JSON,
    tolls_cost      DECIMAL(10,2) DEFAULT 0,
    parking_cost    DECIMAL(10,2) DEFAULT 0,
    other_costs     DECIMAL(10,2) DEFAULT 0,
    status          ENUM('planned','in_progress','completed','cancelled') DEFAULT 'planned',
    notes           TEXT,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES flt_vehicles(id),
    FOREIGN KEY (driver_id) REFERENCES flt_drivers(id),
    INDEX idx_entity_unit (entity_id, unit_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Multas e Ocorrências
CREATE TABLE flt_fines (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    vehicle_id      BIGINT UNSIGNED NOT NULL,
    driver_id       BIGINT UNSIGNED,
    type            ENUM('fine','accident','damage') NOT NULL,
    auto_number     VARCHAR(50),
    occurred_at     DATETIME NOT NULL,
    authority       VARCHAR(100),
    infraction_code VARCHAR(20),
    description     TEXT NOT NULL,
    original_amount DECIMAL(12,2),
    discount_amount DECIMAL(12,2),
    due_date        DATE,
    cnh_points      TINYINT UNSIGNED DEFAULT 0,
    responsible     ENUM('company','driver') DEFAULT 'company',
    deduct_driver   TINYINT(1) DEFAULT 0,
    status          ENUM('open','appealing','paid','cancelled') DEFAULT 'open',
    paid_at         DATE,
    paid_amount     DECIMAL(12,2),
    notes           TEXT,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES flt_vehicles(id),
    INDEX idx_entity_unit (entity_id, unit_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Documentos
CREATE TABLE flt_documents (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    vehicle_id      BIGINT UNSIGNED NOT NULL,
    type            ENUM('crlv','ipva','insurance','inspection','tachograph','other') NOT NULL,
    description     VARCHAR(200),
    doc_number      VARCHAR(100),
    issuer          VARCHAR(200),
    issued_at       DATE,
    expires_at      DATE NOT NULL,
    amount          DECIMAL(12,2),
    file_path       VARCHAR(500),
    alert_days_before INT UNSIGNED DEFAULT 30,
    auto_renew      TINYINT(1) DEFAULT 0,
    status          ENUM('valid','expiring','expired','renewed') DEFAULT 'valid',
    notes           TEXT,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES flt_vehicles(id),
    INDEX idx_entity_unit (entity_id, unit_id),
    INDEX idx_expires (expires_at),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Planos de Manutenção Preventiva
CREATE TABLE flt_maintenance_plans (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    vehicle_id      BIGINT UNSIGNED NOT NULL,
    service_type    VARCHAR(200) NOT NULL,
    periodicity     ENUM('km','months','both') NOT NULL,
    interval_km     BIGINT UNSIGNED,
    interval_months TINYINT UNSIGNED,
    next_km         BIGINT UNSIGNED,
    next_date       DATE,
    alert_km_before INT UNSIGNED DEFAULT 500,
    alert_days_before INT UNSIGNED DEFAULT 15,
    responsible_id  BIGINT UNSIGNED,
    active          TINYINT(1) DEFAULT 1,
    notes           TEXT,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_vehicle (vehicle_id),
    INDEX idx_next_km (next_km),
    INDEX idx_next_date (next_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Automações
CREATE TABLE flt_automations (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED,
    trigger_type    VARCHAR(100) NOT NULL,
    vehicle_ids     JSON COMMENT 'NULL = todos',
    advance_value   INT UNSIGNED,
    channels        SET('email','push','sms','system') NOT NULL,
    recipients      JSON,
    custom_message  TEXT,
    frequency       ENUM('once','daily','weekly') DEFAULT 'once',
    active          TINYINT(1) DEFAULT 1,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_entity (entity_id),
    INDEX idx_trigger (trigger_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Log de Automações
CREATE TABLE flt_automation_logs (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    automation_id   BIGINT UNSIGNED NOT NULL,
    vehicle_id      BIGINT UNSIGNED,
    recipients      JSON,
    channel         VARCHAR(20),
    status          ENUM('sent','failed','skipped') NOT NULL,
    message         TEXT,
    error_detail    TEXT,
    fired_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (automation_id) REFERENCES flt_automations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Log de Auditoria
CREATE TABLE flt_audit_logs (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    user_id         BIGINT UNSIGNED NOT NULL,
    action          VARCHAR(100) NOT NULL,
    table_name      VARCHAR(100) NOT NULL,
    record_id       BIGINT UNSIGNED,
    old_values      JSON,
    new_values      JSON,
    ip_address      VARCHAR(45),
    user_agent      TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_entity_unit (entity_id, unit_id),
    INDEX idx_user (user_id),
    INDEX idx_table_record (table_name, record_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

#### 18. LGPD e Auditoria

##### 18.1 Dados Pessoais Tratados

| Campo | Tabela | Classificação LGPD | Retenção |
|---|---|---|---|
| CPF do motorista | flt_drivers | Dado pessoal identificável | 10 anos |
| Nome completo | flt_drivers | Dado pessoal | 10 anos |
| Data de nascimento | flt_drivers | Dado pessoal | 10 anos |
| Número CNH | flt_drivers | Dado pessoal identificável | 10 anos |
| E-mail / Telefone | flt_drivers | Dado pessoal | 10 anos |
| Localização (viagens) | flt_trips | Dado de localização | 5 anos |
| Assinatura digital | flt_reservations | Dado pessoal | 5 anos |
| Foto do motorista | flt_drivers | Biométrico/imagem | 5 anos |
| Infrações / pontos CNH | flt_fines, flt_drivers | Dado pessoal sensível | 10 anos |

##### 18.2 Eventos Auditados

| # | Evento | Tabela | Criticidade |
|---|---|---|---|
| 1 | Cadastro de veículo | flt_vehicles | Média |
| 2 | Alteração de dados do veículo | flt_vehicles | Média |
| 3 | Inativação de veículo | flt_vehicles | Alta |
| 4 | Cadastro de motorista | flt_drivers | Alta |
| 5 | Alteração de CNH | flt_drivers | Alta |
| 6 | Criação de reserva | flt_reservations | Média |
| 7 | Aprovação/Rejeição de reserva | flt_reservations | Alta |
| 8 | Check-in / Check-out | flt_reservations | Alta |
| 9 | Registro de manutenção | flt_maintenances | Média |
| 10 | Conclusão de OS | flt_maintenances | Média |
| 11 | Registro de multa | flt_fines | Alta |
| 12 | Pagamento de multa | flt_fines | Alta |
| 13 | Upload de documento | flt_documents | Alta |
| 14 | Exclusão de qualquer registro | Todas | Crítica |
| 15 | Exportação de dados | — | Alta |
| 16 | Alteração de automação | flt_automations | Média |

##### 18.3 Regras de Acesso e Mascaramento

- CPF exibido mascarado: `***.***.***.***-**` para perfis abaixo de GE
- Dados completos do motorista: apenas GE, SA e AUD
- Exportações de dados pessoais: requerem log de finalidade (LGPD Art. 7)
- Fotos de motoristas: acessíveis apenas dentro do contexto da entidade
- Logs de auditoria: imutáveis, apenas SA e AUD podem visualizar

##### 18.4 Direitos do Titular (LGPD)

| Direito | Endpoint | Observação |
|---|---|---|
| Acesso | `GET /lgpd/motorista/{id}/dados` | Exporta todos os dados |
| Retificação | Formulário de edição | Com log obrigatório |
| Eliminação | `DELETE /lgpd/motorista/{id}` | Anonimização + log |
| Portabilidade | `GET /lgpd/motorista/{id}/export` | JSON/CSV |
| Oposição | `POST /lgpd/motorista/{id}/opt-out` | Bloqueia notificações |

---

#### 19. Critérios de Aceite

##### 19.1 Funcionais

- [ ] CRUD completo de veículos com upload de fotos e documentos
- [ ] CRUD completo de motoristas com gestão de CNH
- [ ] Fluxo de reserva completo: solicitação → aprovação → check-in → check-out
- [ ] Conflito de agendamento detectado e bloqueado automaticamente
- [ ] OS de manutenção com itens de serviço e peças + custo calculado
- [ ] Registro de abastecimento com cálculo automático de km/L
- [ ] Registro de viagens com km percorrido calculado
- [ ] Registro e acompanhamento de multas e sinistros
- [ ] Gestão de documentos com alertas de vencimento
- [ ] Kanban operacional com drag & drop e log de movimentação
- [ ] 15 automações configuráveis com log de disparo
- [ ] 12 relatórios com exportação Excel/PDF
- [ ] Dashboard com 12 KPIs e 6 charts amCharts 5

##### 19.2 Segurança e Conformidade

- [ ] Autenticação JWT com expiração e refresh token
- [ ] RBAC com 7 perfis e 20 permissões granulares
- [ ] Todos os endpoints validam entity_id e unit_id do token
- [ ] CPF e dados sensíveis mascarados por perfil
- [ ] Todas as operações CUD registradas em flt_audit_logs
- [ ] Soft delete em todas as tabelas principais
- [ ] Upload de arquivos: validação de tipo, tamanho e antivírus
- [ ] Rate limiting: 100 req/min por usuário
- [ ] LGPD: anonimização disponível para motoristas desligados

##### 19.3 Performance e UX

- [ ] Dashboard carregado em < 2 segundos
- [ ] Datatables com paginação server-side
- [ ] Busca com debounce de 300ms
- [ ] Drawers abrem em < 500ms
- [ ] Responsivo: funcional em tablets (768px+)
- [ ] Kanban com drag & drop fluido
- [ ] Calendário de reservas com FullCalendar.js
- [ ] Exportações geradas assincronamente (queue) para > 1.000 registros
- [ ] Gráficos amCharts 5 com loading skeleton

##### 19.4 Checklist de Entrega

- [ ] Spec revisado e aprovado pelo PO
- [ ] Schema SQL executado e validado
- [ ] APIs documentadas e testadas (Postman/Insomnia)
- [ ] RBAC implementado e testado por perfil
- [ ] Automações configuradas e testadas
- [ ] Relatórios validados com dados reais
- [ ] Testes de segurança: SQL injection, XSS, IDOR
- [ ] Documentação de onboarding atualizada
- [ ] Integração com módulos: Financeiro, Patrimônio, RH validada

---

*Documento gerado por TotusTuusSoftCloud SaaS Platform — Módulo Frotas v1.0 — 2026-06-07*
