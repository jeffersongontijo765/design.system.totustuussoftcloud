# SPEC — Módulo Biblioteca Acadêmica (Acervo e Empréstimos)
**Projeto:** TotusTuusSoftCloud — SaaS Multi-Entidade · Multi-Unidade · Multi-Usuário
**Módulo:** Academic Library / Circulation Management
**Stack:** PHP 8 puro · MariaDB · Tailwind CSS 4.2 · Supabase · amCharts 5
**Padrão de ID:** `id` (ordenação) · `uuid` (interno) · `code` (externo)
**Status:** Draft — gap identificado (não confundir com `spec_gestao_biblioteca_completo.md`, que é um design system de componentes UI)

- Language Standard: Global English

---

## 1. Objetivo

Gerenciar o acervo físico e digital das unidades educacionais: catalogação, aquisição, empréstimo, devolução, reserva, multas, inventário e leitura digital, integrado ao módulo Acadêmico (alunos, professores, turmas) e ao módulo Financeiro (multas).

## 2. Access Levels & Portal Boundaries

Este módulo é consumido por múltiplos portais da plataforma. Cada nível acessa **apenas seu recorte**, nunca a administração completa do acervo.

| Nível | Portal | Acesso neste módulo |
|---|---|---|
| Desenvolvedor (SaaS) | `/dev` | Nenhum acesso a dados de acervo/empréstimo. Apenas métricas agregadas de uso (ex.: nº de bibliotecas ativas por entidade) para suporte/billing da plataforma. |
| Entidade/Unidade (Bibliotecário/Admin) | `/admin/library` | Acesso total: catalogação, empréstimos, multas, inventário, relatórios. Escopo travado à própria entidade/unidade. |
| Site público (venda do SaaS) | — | Nenhum acesso. Não relacionado à venda da plataforma. |
| Professor | `/teacher/library` | Consulta ao catálogo, empréstimo próprio (prazo estendido), reserva de sala. **Não vê** empréstimos de outros usuários nem multas de terceiros. |
| Aluno | `/student/library` | Consulta ao catálogo, empréstimo/reserva/renovação **do próprio usuário**, biblioteca digital, próprias multas. |
| Terceiros | `/partner` | Sem acesso por padrão. Pode ser habilitado pontualmente (ex.: biblioteca comunitária) via permissão explícita da entidade. |
| Pais/Responsáveis (pedagógico) | `/guardian/library` | **Somente leitura**: empréstimos ativos e multas do(s) filho(s) vinculado(s). Não pode consultar catálogo geral fora do contexto do filho nem editar/pagar multa aqui. |
| Responsável Financeiro | `/payer/library` (ou aba financeira dedicada) | **Somente leitura financeira**: valor e status de multas vinculadas ao aluno sob sua responsabilidade de pagamento, com link direto para quitação no módulo Billing. **Não vê** título do livro, categoria ou histórico de leitura — apenas o valor e a referência da multa, para preservar privacidade pedagógica. |

**Regra de segregação:** a API deve expor endpoints diferentes por portal (`/api/v1/library/*` para admin vs. `/api/v1/me/library/*` para aluno/professor vs. `/api/v1/guardian/library/*` vs. `/api/v1/payer/library/fines` — este último retorna apenas `{fine_uuid, amount, status, due_date}`, sem join com `lib_items`).

## 3. Escopo funcional

- Catalogação de itens (livros, periódicos, mídias, e-books, TCCs).
- Empréstimo e devolução com regras por perfil (aluno, professor, servidor).
- Reserva de itens indisponíveis com fila de espera.
- Renovação automática e manual.
- Multas por atraso e bloqueio de novo empréstimo.
- Inventário de acervo (contagem física, divergências).
- Doações e descarte de itens.
- Empréstimo entre unidades (malote/interbibliotecas).
- Sala de leitura / reserva de espaço físico.
- Biblioteca digital: e-books, PDFs protegidos, streaming de leitura.
- Indicadores de uso do acervo por curso/disciplina.

## 3. Perfis de acesso

| Perfil | Permissões |
|---|---|
| Bibliotecário | CRUD completo, empréstimos, multas, inventário |
| Auxiliar de Biblioteca | Empréstimo/devolução, sem gestão de acervo |
| Professor | Empréstimo com prazo estendido, reserva de sala |
| Aluno | Consulta, empréstimo próprio, reserva, renovação self-service |
| Coordenador | Relatórios de uso por curso/disciplina |
| Financeiro | Consulta de multas vinculadas ao aluno |

## 4. Páginas do módulo

```
/library/dashboard
/library/catalog                  — Catálogo de itens (datatable)
/library/catalog/:uuid             — Ficha catalográfica
/library/loans                     — Empréstimos ativos e histórico
/library/reservations              — Reservas e fila de espera
/library/fines                     — Multas
/library/inventory                 — Inventário do acervo
/library/rooms                     — Reserva de salas de leitura/estudo
/library/digital                   — Biblioteca digital (e-books)
/library/reports                   — Relatórios de circulação
/library/settings                  — Regras de empréstimo, categorias, editoras
```

## 5. Dashboard

### Widgets
- Total de itens no acervo.
- Empréstimos ativos.
- Empréstimos em atraso.
- Reservas pendentes.
- Multas em aberto (R$).
- Itens mais emprestados (top 5).
- Taxa de devolução no prazo.
- Novos itens catalogados no mês.

### Charts
- Linha: empréstimos por mês.
- Donut: acervo por categoria (Literatura, Didático, Periódico, Mídia, E-book).
- Barras: circulação por curso/disciplina.
- Heatmap: horários de maior movimento no balcão.

## 6. Catálogo — Datatable

Colunas: código de tombamento · título · autor · ISBN/ISSN · categoria · editora · exemplares totais · exemplares disponíveis · localização física (estante/prateleira) · status · ações.

### Drawer — Ficha Catalográfica (CRUD)
Abas:
- **Dados Gerais**: título, subtítulo, autor(es), ISBN/ISSN, editora, edição, ano, idioma, categoria (CDD/CDU opcional), sinopse, capa (upload).
- **Exemplares**: lista de exemplares físicos com código de barras individual, estado de conservação, localização, status (disponível/emprestado/reservado/em manutenção/baixado).
- **Digital**: arquivo e-book/PDF protegido, licença de uso, número de licenças simultâneas, DRM opcional.
- **Aquisição**: fornecedor, nota fiscal, valor de aquisição, data de entrada, forma (compra/doação).
- **Histórico**: timeline de empréstimos do item.

## 7. Empréstimos

### Regras de negócio
- Prazo de empréstimo configurável por perfil (ex.: aluno 7 dias, professor 30 dias).
- Limite de itens simultâneos por perfil.
- Bloqueio automático de novo empréstimo se houver multa em aberto ou item atrasado.
- Renovação permitida até N vezes, exceto se houver reserva de outro usuário para o item.
- Devolução gera baixa automática de multa quando dentro do prazo de tolerância.

### Datatable de Empréstimos
Colunas: código do empréstimo · usuário · item · data empréstimo · data prevista devolução · data devolução real · status (ativo/atrasado/devolvido/perdido) · multa gerada · ações.

### Drawer — Novo Empréstimo
- Buscar usuário (aluno/professor/servidor) por matrícula/nome.
- Buscar item por código de barras (scanner) ou título.
- Data de devolução calculada automaticamente pela regra do perfil.
- Confirmação de retirada (assinatura digital opcional).

## 8. Reservas

- Fila de espera por item indisponível.
- Notificação automática quando item é devolvido e liberado para o próximo da fila.
- Prazo de retirada da reserva (ex.: 48h), expirando automaticamente.

## 9. Multas

### Regras
- Valor por dia de atraso configurável por categoria de item.
- Teto máximo de multa por item.
- Geração automática de fatura no módulo Financeiro/Billing quando multa é confirmada.
- Isenção de multa mediante justificativa aprovada pelo bibliotecário.

### Datatable de Multas
Colunas: usuário · item · dias de atraso · valor · status (pendente/pago/isento) · data geração · ações.

## 10. Inventário do Acervo

- Criação de inventário por estante/setor ou geral.
- Contagem via leitor de código de barras/QR.
- Relatório de divergências (item não encontrado, item fora de lugar).
- Aprovação de baixa por extravio.

## 11. Salas de Leitura / Estudo

- Cadastro de salas/cabines com capacidade.
- Reserva por aluno/professor com horário e duração máxima.
- Calendário de ocupação (dia/semana).
- Check-in obrigatório para validar reserva.

## 12. Biblioteca Digital

- Upload de e-books com DRM/watermark dinâmico por usuário.
- Controle de licenças simultâneas (empréstimo digital com expiração automática).
- Leitor embutido (visualização sem download quando exigido por licença).
- Histórico de leitura e progresso.

## 13. Automações

- Notificar usuário 2 dias antes do vencimento do empréstimo.
- Notificar usuário no dia do vencimento e em D+1, D+3 de atraso.
- Bloquear renovação automática se item tiver reserva pendente.
- Liberar reserva expirada e notificar o próximo da fila.
- Gerar relatório mensal de circulação por curso.
- Sincronizar baixa de multa com módulo Financeiro/Billing.

## 14. Integrações

- **Acadêmico**: validação de matrícula ativa do aluno antes de permitir empréstimo.
- **RH/Pessoas**: validação de vínculo ativo do professor/servidor.
- **Financeiro/Billing**: geração e baixa de fatura de multa.
- **Notificações**: envio de lembretes por e-mail/push/WhatsApp.
- **Auditoria**: toda ação de empréstimo, devolução, baixa e isenção deve ser auditada.

## 15. Modelo de dados mínimo

```sql
CREATE TABLE lib_items (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  code VARCHAR(30) NOT NULL UNIQUE,
  entity_id BIGINT UNSIGNED NOT NULL,
  unit_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR(300) NOT NULL,
  authors JSON,
  isbn VARCHAR(20),
  category VARCHAR(80),
  publisher VARCHAR(150),
  edition VARCHAR(50),
  publish_year YEAR,
  language VARCHAR(30),
  synopsis TEXT,
  cover_path VARCHAR(500),
  total_copies INT UNSIGNED DEFAULT 1,
  available_copies INT UNSIGNED DEFAULT 1,
  is_digital TINYINT(1) DEFAULT 0,
  digital_file_path VARCHAR(500),
  digital_license_count INT UNSIGNED,
  status ENUM('active','archived','lost') DEFAULT 'active',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  deleted_at DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_copies (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  item_id BIGINT UNSIGNED NOT NULL,
  barcode VARCHAR(50) NOT NULL UNIQUE,
  location VARCHAR(100),
  condition_status ENUM('new','good','damaged','lost') DEFAULT 'good',
  status ENUM('available','loaned','reserved','maintenance','disposed') DEFAULT 'available',
  FOREIGN KEY (item_id) REFERENCES lib_items(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_loans (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  code VARCHAR(30) NOT NULL UNIQUE,
  copy_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  user_type ENUM('student','teacher','staff') NOT NULL,
  loaned_at DATETIME NOT NULL,
  due_at DATE NOT NULL,
  returned_at DATETIME NULL,
  renewals_count TINYINT UNSIGNED DEFAULT 0,
  status ENUM('active','overdue','returned','lost') DEFAULT 'active',
  fine_id BIGINT UNSIGNED NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_reservations (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  item_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  queue_position SMALLINT UNSIGNED,
  status ENUM('waiting','ready','expired','fulfilled','cancelled') DEFAULT 'waiting',
  notified_at DATETIME NULL,
  expires_at DATETIME NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_fines (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  loan_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  days_late INT UNSIGNED,
  amount DECIMAL(10,2),
  status ENUM('pending','paid','waived') DEFAULT 'pending',
  billing_invoice_uuid CHAR(36) NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## 16. API REST (principais)

- `GET/POST /api/v1/library/items`
- `GET /api/v1/library/items/{uuid}/copies`
- `POST /api/v1/library/loans` · `POST /api/v1/library/loans/{uuid}/return` · `POST /api/v1/library/loans/{uuid}/renew`
- `POST /api/v1/library/reservations` · `POST /api/v1/library/reservations/{uuid}/cancel`
- `GET /api/v1/library/fines` · `POST /api/v1/library/fines/{uuid}/waive`
- `POST /api/v1/library/inventory` · `POST /api/v1/library/inventory/{uuid}/count`
- `GET /api/v1/library/rooms/availability` · `POST /api/v1/library/rooms/bookings`

## 17. Critérios de aceite

- Empréstimo, devolução e renovação funcionam com regras por perfil.
- Reserva libera automaticamente para o próximo da fila.
- Multa é gerada e sincronizada com o módulo Financeiro/Billing.
- Inventário identifica divergências corretamente.
- Biblioteca digital respeita limite de licenças simultâneas.
- Todas as ações críticas são auditadas.
