# SPEC — Módulo Object Storage & Digital Asset Management (DAM)
**Projeto:** TotusTuusSoftCloud — SaaS Multi-Entidade · Multi-Unidade · Multi-Usuário
**Módulo:** File Storage Infrastructure / Digital Asset Management
**Stack:** PHP 8 puro · MariaDB (metadados) · S3-compatible object storage (dados binários) · Supabase Storage adapter · amCharts 5
**Padrão de ID:** `id` (ordenação) · `uuid` (interno) · `code` (externo)
**Status:** Draft — gap identificado (NÃO confundir com `spec_gestao_armazenamento_completo.md`, que é WMS de estoque físico)

- Language Standard: Global English

---

## 1. Objetivo

Fornecer a infraestrutura central de armazenamento de arquivos digitais (documentos, imagens, PDFs, anexos, e-books, comprovantes, backups de export) consumida por praticamente todos os outros módulos (Documentos, Contratos, RH, SMT, Patrimônio, Biblioteca, Billing, etc.), com governança de bucket, política de retenção, controle de acesso por escopo, CDN e antivírus — em vez de cada módulo implementar upload de forma isolada.

## 2. Problema que resolve

Hoje dezenas de specs (Documentos, Contratos, RH, SMT, Frotas, Patrimônio, Suprimentos, Billing, Biblioteca) descrevem campos como `file_path VARCHAR(500)` ou `docs_json` sem nenhuma camada comum de: validação de upload, quota por tenant, CDN, versionamento, expiração, criptografia em repouso e trilha de acesso. Este módulo centraliza essa responsabilidade.

## 3. Escopo funcional

- Buckets lógicos por entidade/unidade/módulo com isolamento multi-tenant.
- Upload direto (presigned URL) e upload via backend (proxy).
- Validação de tipo MIME real, tamanho máximo e antivírus (ClamAV ou equivalente).
- Versionamento de arquivos com histórico e rollback.
- Política de retenção e expiração automática por categoria.
- Controle de acesso: público, privado, assinado por token temporário.
- CDN/cache para arquivos públicos (capas, avatares, imagens de marketing).
- Watermark dinâmico opcional (documentos sensíveis).
- Geração de thumbnails para imagens/PDFs.
- Quota de armazenamento por entidade com alertas de consumo.
- Painel de auditoria de acesso a arquivos sensíveis.
- Lixeira (soft delete) com purge programado.

## 4. Perfis de acesso

| Perfil | Permissões |
|---|---|
| Super Admin | Gestão global de buckets, quotas, políticas |
| Admin de Entidade | Gestão de buckets da própria entidade |
| Módulo consumidor (via API interna) | Upload/download escopado ao seu contexto |
| Auditor | Consulta de logs de acesso, sem download |
| Usuário final | Upload/download conforme permissão do módulo de origem |

## 5. Páginas do módulo

```
/storage-platform/dashboard
/storage-platform/buckets             — Gestão de buckets por entidade/módulo
/storage-platform/files                — Explorador de arquivos (datatable)
/storage-platform/files/:uuid          — Detalhe do arquivo + versões
/storage-platform/quotas               — Quotas por entidade
/storage-platform/retention-policies   — Políticas de retenção
/storage-platform/access-logs          — Trilha de acesso a arquivos
/storage-platform/trash                — Lixeira / itens excluídos
/storage-platform/settings             — Provedores, CDN, antivírus
```

## 6. Dashboard

### Widgets
- Armazenamento total consumido (GB) vs. quota.
- Uploads no dia/mês.
- Arquivos com falha de antivírus.
- Arquivos aguardando purge (retenção expirada).
- Top 5 módulos por consumo de storage.
- Downloads/acessos no período.

### Charts
- Área: crescimento de armazenamento por mês (12 meses).
- Donut: consumo por módulo de origem (Documentos, Contratos, RH, SMT...).
- Barras: quota utilizada por entidade (top 10).
- Linha: uploads vs. downloads por dia.

## 7. Buckets — Gestão

Cada módulo consumidor deve operar sobre um bucket lógico próprio, nunca acessar diretamente o storage físico.

### Datatable de Buckets
Colunas: nome · módulo de origem · entidade · visibilidade (público/privado) · quota (GB) · consumo atual · política de retenção vinculada · status · ações.

### Drawer CRUD — Bucket
- Nome técnico (`documents`, `contracts`, `hr-payroll`, `library-ebooks`, `billing-receipts`).
- Entidade/unidade dona.
- Visibilidade padrão dos arquivos.
- Quota máxima (GB) com alerta em 80%/95%.
- Política de retenção padrão.
- Exigir antivírus (toggle).
- Exigir criptografia em repouso (toggle — obrigatório para dados sensíveis/LGPD).

## 8. Arquivos — Explorador

### Datatable
Colunas: nome do arquivo · bucket · módulo/entidade de origem · tipo MIME · tamanho · uploader · data upload · versão atual · status (ativo/quarentena/expirado/excluído) · ações.

### Ações
Visualizar · Baixar · Ver versões · Ver trilha de acesso · Gerar link temporário · Mover para lixeira · Restaurar.

### Drawer — Detalhe do Arquivo
- Metadados completos (checksum SHA-256, MIME real detectado, dimensões se imagem).
- Histórico de versões com diff de tamanho/data.
- Resultado do antivírus (limpo/infectado/não escaneado).
- Trilha de acesso (quem visualizou/baixou, quando, IP).
- Vínculo com entidade de negócio (ex.: `contract_uuid`, `employee_uuid`).

## 9. Políticas de Retenção

- Retenção por categoria (ex.: comprovantes fiscais 5 anos, exames ocupacionais 20 anos, avatares indefinido).
- Ação ao expirar: arquivar (cold storage) / anonimizar / excluir definitivamente.
- Bloqueio de exclusão quando há hold legal (litígio) vinculado — integração com módulo de Contratos/Privacy.

## 10. Controle de Acesso e Segurança

- Links assinados com expiração configurável (padrão 15 min para downloads sensíveis).
- Upload validado por: extensão declarada + MIME real (magic bytes) + tamanho + antivírus.
- Rejeitar automaticamente: executáveis, scripts, macros ativas em documentos Office, arquivos com payload suspeito.
- Criptografia em repouso (AES-256) obrigatória para buckets marcados como sensíveis (RH, SMT, Financeiro).
- Watermark dinâmico com nome/CPF mascarado do usuário que visualiza, para documentos confidenciais (ex.: contracheque, laudo médico).

## 11. Automações

- Escanear antivírus imediatamente após upload; mover para quarentena se infectado e notificar administrador.
- Gerar thumbnail automaticamente para imagens e primeira página de PDFs.
- Executar purge diário de itens na lixeira com mais de 30 dias.
- Alertar entidade ao atingir 80% e 95% da quota.
- Expirar automaticamente arquivos conforme política de retenção vencida.
- Sincronizar exclusão lógica quando o registro de negócio de origem é excluído (ex.: contrato cancelado → anexos seguem política própria, não exclusão em cascata automática sem aprovação).

## 12. Integrações

- **Todos os módulos com upload** (Documentos, Contratos, RH, SMT, Frotas, Patrimônio, Suprimentos, Biblioteca, Billing/NFSe) consomem este módulo via SDK/API interna em vez de implementar storage próprio.
- **Auditoria**: todo upload, download e exclusão gera evento auditável.
- **Privacy/LGPD**: exportação e anonimização de arquivos vinculados a um titular de dados.
- **Notificações**: alertas de quota e de arquivo em quarentena.

## 13. Modelo de dados mínimo

```sql
CREATE TABLE storage_buckets (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  code VARCHAR(60) NOT NULL UNIQUE,
  entity_id BIGINT UNSIGNED NOT NULL,
  unit_id BIGINT UNSIGNED,
  source_module VARCHAR(60) NOT NULL,
  visibility ENUM('public','private') DEFAULT 'private',
  quota_gb INT UNSIGNED DEFAULT 10,
  used_bytes BIGINT UNSIGNED DEFAULT 0,
  retention_policy_id BIGINT UNSIGNED NULL,
  require_antivirus TINYINT(1) DEFAULT 1,
  require_encryption TINYINT(1) DEFAULT 0,
  status ENUM('active','suspended') DEFAULT 'active',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE storage_files (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  bucket_id BIGINT UNSIGNED NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  mime_type VARCHAR(100) NOT NULL,
  detected_mime VARCHAR(100),
  size_bytes BIGINT UNSIGNED NOT NULL,
  checksum_sha256 CHAR(64) NOT NULL,
  storage_key VARCHAR(500) NOT NULL COMMENT 'path no provider S3-compatible',
  origin_entity_type VARCHAR(80),
  origin_entity_uuid CHAR(36),
  antivirus_status ENUM('pending','clean','infected','skipped') DEFAULT 'pending',
  current_version INT UNSIGNED DEFAULT 1,
  uploaded_by BIGINT UNSIGNED NOT NULL,
  status ENUM('active','quarantined','expired','trashed') DEFAULT 'active',
  trashed_at DATETIME NULL,
  purge_at DATETIME NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (bucket_id) REFERENCES storage_buckets(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE storage_file_versions (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  file_id BIGINT UNSIGNED NOT NULL,
  version_number INT UNSIGNED NOT NULL,
  storage_key VARCHAR(500) NOT NULL,
  size_bytes BIGINT UNSIGNED,
  checksum_sha256 CHAR(64),
  created_by BIGINT UNSIGNED,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (file_id) REFERENCES storage_files(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE storage_access_logs (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  file_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED,
  action ENUM('view','download','upload','delete','restore') NOT NULL,
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_file (file_id),
  INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE storage_retention_policies (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  name VARCHAR(120) NOT NULL,
  retention_days INT UNSIGNED NOT NULL,
  action_on_expiry ENUM('archive','anonymize','delete') DEFAULT 'archive',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## 14. API REST (principais)

- `POST /api/v1/storage/buckets/{code}/presign-upload` — retorna URL assinada para upload direto.
- `POST /api/v1/storage/files` — registrar metadados após upload (ou proxy upload).
- `GET /api/v1/storage/files/{uuid}` · `GET /api/v1/storage/files/{uuid}/download-url`
- `GET /api/v1/storage/files/{uuid}/versions` · `POST /api/v1/storage/files/{uuid}/restore-version`
- `DELETE /api/v1/storage/files/{uuid}` (soft) · `POST /api/v1/storage/files/{uuid}/purge` (SA only)
- `GET /api/v1/storage/quota/{entity_uuid}`
- `GET /api/v1/storage/access-logs`

## 15. Requisitos não funcionais

- Upload direto ao provider via presigned URL (sem passar payload binário pelo backend PHP) para arquivos > 5MB.
- Antivírus assíncrono via fila, com bloqueio de disponibilização até resultado "clean".
- Multi-tenant: toda query de metadados filtrada por `entity_id`/`unit_id`.
- SLA de geração de thumbnail: até 10s após upload.
- Retenção mínima de logs de acesso: 5 anos (compliance).

## 16. Critérios de aceite

- Nenhum módulo grava arquivo binário fora deste serviço.
- Upload valida MIME real, tamanho e antivírus antes de disponibilizar o arquivo.
- Quota por entidade é respeitada e alerta antes de estourar.
- Versionamento permite restaurar versão anterior.
- Retenção expira e executa ação configurada automaticamente.
- Todo acesso a arquivo sensível é auditável com IP e usuário.
