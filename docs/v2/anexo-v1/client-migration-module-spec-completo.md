# Client Migration Module Specification

## 1. Document Control

- Document Name: Client Migration Module Specification
- Product Context: Multi-tenant SaaS platform using Supabase-inspired admin UX patterns
- Target Stack: PHP, Fetch API, MariaDB, JSON-based migration intake
- Language Standard: Global English
- Primary Audience: Product owner, backend engineers, frontend engineers, database engineers, QA, DevOps, security reviewers
- Module Type: Admin-only operational module
- Status: Draft v1.0

## 2. Purpose

This module enables an administrator to onboard a new client that is migrating from a legacy system into the platform.

The client provides a structured JSON migration package containing source schema metadata, table definitions, field definitions, relationships when available, and optionally sample records or transformation hints. The module presents a dual-schema mapping workspace where the platform schema appears in one column and the client legacy schema appears in a second column, allowing controlled mapping of tables, columns, keys, enums, reference values, and transformation rules.

The module must support semi-automated matching so that the system proposes likely mappings first, and the administrator performs a review and final approval pass before execution.

## 3. Goals

- Standardize onboarding migrations for new clients.
- Reduce manual mapping effort by auto-suggesting table and field matches.
- Preserve data integrity during legacy-to-platform conversion.
- Provide a visual schema exploration experience similar to a schema visualizer.
- Support repeatable, auditable, and reversible migration planning.
- Minimize migration errors caused by naming mismatches, datatype mismatches, enum drift, and broken foreign-key relationships.
- Produce a clear migration execution plan before any production write occurs.

## 4. Non-Goals

- This module is not intended to replace raw DBA tooling for unrestricted database administration.
- This module is not a generic ETL studio for arbitrary third-party destinations.
- This module is not a no-code workflow engine.
- This module should not allow direct execution against production targets without validation, review, and authorization gates.

## 5. Business Context

A new client often comes from a different software vendor, internal legacy application, spreadsheets, or custom databases. Their data model rarely matches the platform model one-to-one. The migration module must bridge this gap by creating explicit mappings between:

- Source tables and target tables.
- Source columns and target columns.
- Source coded values and target normalized values.
- Source relationships and target foreign keys.
- Source identifiers and target UUID or internal ID strategy.

The module must support highly structured enterprise onboarding where traceability, reproducibility, and compliance are mandatory.

## 6. Primary Users

### 6.1 Platform Super Admin

Can create migration projects, upload JSON packages, review schema suggestions, approve execution, monitor jobs, and download audit artifacts.

### 6.2 Migration Analyst

Can inspect mappings, adjust transforms, validate referential integrity issues, run dry runs, and submit for approval.

### 6.3 Client Technical Contact

May provide the JSON package and optionally review non-sensitive mapping previews, but should not have unrestricted administrative permissions by default.

### 6.4 Compliance / Audit Reviewer

Can read migration logs, validation reports, and execution evidence.

## 7. Module Scope

The module includes:

- Migration project creation.
- JSON import and schema parsing.
- Source schema visualization.
- Target schema visualization.
- Automated mapping suggestions.
- Manual mapping review and override.
- Transformation rule management.
- Validation engine.
- Dry run engine.
- Execution orchestration.
- Logging, audit, rollback metadata, and reporting.

## 8. High-Level Workflow

1. Admin creates a new migration project.
2. Admin selects tenant/client context.
3. Admin uploads or pastes the JSON migration package.
4. System validates JSON structure and required metadata.
5. System parses source schema, tables, fields, indexes, relationships, enums, and source constraints.
6. System loads the current target platform schema from MariaDB metadata.
7. System renders a dual-column schema workspace.
8. System generates automatic table match suggestions.
9. System generates automatic column match suggestions within each mapped table pair.
10. Admin reviews unmatched, low-confidence, and conflict items.
11. Admin defines transforms, defaults, lookups, enum remaps, and key strategies.
12. System runs validation.
13. System runs dry run against staging or isolated migration schema.
14. Admin reviews reports.
15. Authorized admin approves live execution.
16. System executes migration in controlled phases.
17. System stores complete audit trail and post-migration report.

## 9. Functional Overview

The module should behave like a Supabase-style schema visualizer plus a guided migration planner.

Core UX idea:

- Left workspace: full target system schema.
- Right workspace: full client source schema.
- Connection layer: visual lines or link cards showing mapped table pairs.
- Within a selected table pair: side-by-side field mapping grid.
- Confidence badges: auto-match confidence shown as High, Medium, Low.
- Review queue: unresolved or risky items listed separately.

## 10. UI Architecture

### 10.1 Main Screens

- Migration Projects List
- Create Migration Project
- Migration Project Overview
- Schema Visualizer and Mapping Workspace
- Field Mapping Editor
- Transformation Rules Editor
- Validation Report Screen
- Dry Run Results Screen
- Execution Console
- Audit and Reports Screen

### 10.2 Migration Project Overview

Sections:

- Client identity
- Migration package metadata
- Source system name and version
- Source database type
- Import timestamp
- Mapping completion percentage
- Validation status
- Dry run status
- Execution status
- Last updated by
- Risk summary

### 10.3 Schema Visualizer Workspace

Layout recommendation:

- Left panel: target schema tree
- Center canvas: mapping graph / relationship lines
- Right panel: source schema tree
- Bottom panel: details inspector or mapping queue
- Top bar: search, filter, confidence filter, status filter, auto-match actions, save draft, validate, dry run, execute

### 10.4 Table Mapping View

Each side shows:

- Table name
- Schema/group
- Row estimate if available
- Primary key
- Foreign keys count
- Columns count
- Last import timestamp for source
- Tags such as core, financial, academic, identity, medical, lookup, audit

Actions:

- Map table
- Ignore table
- Mark table as derived
- Mark table as archival only
- Split source table into multiple target tables
- Merge multiple source tables into one target table

### 10.5 Field Mapping View

Each row in the mapping grid should support:

- Target field name
- Target datatype
- Required flag
- Unique flag
- FK target if applicable
- Source field suggestion
- Source datatype
- Transform type
- Default value
- Null handling
- Confidence score
- Validation notes
- Approval status

## 11. JSON Migration Package Specification

### 11.1 Supported Input Modes

- JSON file upload.
- JSON paste in text area.
- SQL file upload.
- XML file upload.
- CSV file upload.
- XLS or XLSX file upload.
- API submission from secure client endpoint.

### 11.2 Top-Level JSON Structure

```json
{
  "meta": {
    "source_system": "Legacy ERP",
    "source_version": "4.2.1",
    "database_type": "mysql",
    "exported_at": "2026-07-10T09:00:00Z",
    "timezone": "UTC",
    "locale": "en-US"
  },
  "client": {
    "external_client_code": "ACME-001",
    "client_name": "Acme Health Group"
  },
  "schema": {
    "tables": []
  },
  "data": {
    "tables": []
  },
  "mapping_hints": {
    "table_aliases": [],
    "field_aliases": [],
    "enum_maps": []
  }
}
```

### 11.3 Minimum Required Source Schema Elements

- Source table name
- Source column name
- Source datatype
- Nullable flag if available
- Primary key indication if available
- Foreign key reference if available
- Source row count estimate if available

### 11.4 Recommended Optional Elements

- Column description
- Friendly label
- Sample values
- Enum values
- Index metadata
- Relationship cardinality
- Legacy code meanings
- Deprecated field markers
- Source timezone metadata
- Source encoding metadata


## 11.5 Additional Accepted Source Formats

The migration module must also accept the following source formats in addition to JSON:

- SQL scripts.
- XML files.
- CSV files.
- XLS or XLSX spreadsheets.

Each format must be converted into the same internal migration package model before mapping, validation, and execution. The UI must keep the same dual-schema workspace regardless of source format.

### 11.6 Format-Specific Parsing Rules

- SQL: Parse DDL and optionally DML to extract tables, columns, constraints, indexes, and seed rows when allowed.
- XML: Parse hierarchical nodes into tabular source entities using configurable XPath or node-path rules.
- CSV: Infer headers, delimiters, quoting, encoding, and data types from uploaded files.
- XLS/XLSX: Read worksheet names, header rows, merged cells where relevant, and detect table-like ranges.

### 11.7 Normalization Pipeline

All supported file types must be normalized into:

- source tables.
- source columns.
- sample values.
- relationship hints.
- enum/value candidates.
- metadata tags.

This normalization step must happen before auto-matching.

### 11.8 Format Validation

The import layer must validate each format before parsing completes:

- SQL files must be checked for supported dialect and dangerous statements.
- XML files must be checked for well-formed structure.
- CSV files must be checked for delimiter consistency and header integrity.
- XLS/XLSX files must be checked for readable sheets and non-empty headers.


## 12.1 Upload Security and File Integrity

All uploads must be treated as untrusted input until proven otherwise.

Requirements:

- Validate file extension, MIME type, and declared format.
- Enforce size limits per file type and per migration project.
- Store uploaded files in a temporary quarantine area before parsing.
- Scan files for malware or suspicious payloads when the pipeline supports it.
- Reject executable content, embedded scripts, and active content where applicable.
- Compute and store a checksum or hash for each uploaded file.
- Log upload source, uploader identity, timestamp, and correlation ID.
- Prevent public access to raw uploaded files.

## 12.2 Parsing Error Handling

The parser must fail safely and return structured error feedback.

Error handling rules:

- Stop parsing immediately when a fatal format error is detected.
- Capture file name, format, project ID, and a stable error code.
- Include line, column, sheet, node, or statement references when available.
- Distinguish between recoverable warnings and blocking parsing errors.
- Store parsing errors in the migration audit trail.
- Keep the original upload untouched for review and reprocessing.

Recommended parser error categories:

- INVALID_JSON
- INVALID_XML
- INVALID_CSV_HEADER
- INVALID_CSV_DELIMITER
- INVALID_XLS_STRUCTURE
- UNSUPPORTED_SQL_DIALECT
- SQL_SYNTAX_ERROR
- EMPTY_FILE
- UNREADABLE_FILE
- INCONSISTENT_ENCODING

## 12.3 Corrupted File Handling

The system must detect and isolate corrupted files before they enter the mapping workflow.

Corruption signals include:

- Truncated file content.
- Hash mismatch.
- Broken archive structure.
- Unreadable workbook sheets.
- Invalid XML tree structure.
- Incomplete CSV rows due to file damage.
- Missing table or worksheet metadata expected for the declared format.

When corruption is detected:

- Mark the upload as corrupted.
- Block parsing and mapping.
- Preserve technical evidence for audit.
- Notify the admin with a clear remediation message.
- Allow the user to re-upload a corrected file.

## 12.4 Upload Threat Model

The module must protect against common upload threats:

- Path traversal.
- Content spoofing.
- Zip bombs or decompression abuse.
- Oversized payload attacks.
- Formula injection in spreadsheets.
- XML entity expansion abuse.
- SQL payloads containing destructive statements when disallowed.
- XSS through file names, sheet names, or legacy labels rendered in the UI.

## 28.4 Mapping Workspace Wireframe

Textual wireframe for the mapping screen:

```text
+----------------------------------------------------------------------------------+
| Client Migration Workspace                                                       |
| [Project Name] [Import Format] [Status] [Validate] [Dry Run] [Approve] [Execute] |
+----------------------------------------------------------------------------------+
| Search Target... | Search Source... | Auto-Match Tables | Auto-Match Fields      |
| Confidence Filter | Show Unmapped | Show Conflicts | Show Corrupted | Save Draft  |
+----------------------------------------------------------------------------------+
| TARGET SYSTEM SCHEMA                     |     LINKING / REVIEW CANVAS            |
|------------------------------------------|----------------------------------------|
| Table A                                  |  Target Table A  ===>  Source Table X  |
|  - id                                   |  Match confidence badge                 |
|  - name                                 |  Suggested fields list                  |
|  - status                               |  Conflict notes                         |
|                                          |                                        |
| Table B                                  |  Target Table B  ===>  Source Table Y  |
|  - id                                   |  Auto-match accepted / rejected         |
|  - client_id                             |  Required fields missing                |
|  - created_at                            |  Enum remap suggestions                 |
|                                          |                                        |
| Table C                                  |  Table split / merge actions            |
|  - id                                   |  Relationship warnings                  |
|  - parent_id                             |  Dry-run preview link                   |
+----------------------------------------------------------------------------------+
| SOURCE CLIENT SCHEMA                                                             |
|------------------------------------------|----------------------------------------|
| Legacy Table X                           | Mapping Details                         |
|  - legacy_id                             | Target Field: name                      |
|  - full_name                             | Source Field: fullname                  |
|  - state_code                            | Transform: trim -> normalize_case       |
|                                          | Confidence: 92%                         |
| Legacy Table Y                           | Validation Notes                        |
|  - ext_id                               | Required field resolved                  |
|  - description                          | No FK issues                             |
+----------------------------------------------------------------------------------+
| Issues Queue: Missing field | Bad type | Unmapped enum | Corrupted file | SQL risk |
+----------------------------------------------------------------------------------+
```

## 12. Metadata Extraction from Target System

The system must inspect MariaDB metadata and build an internal representation of the current platform schema, including:

- Tables
- Columns
- Types
- PKs
- FKs
- Unique constraints
- Indexes
- Default values
- Nullability
- Enum-like lookup references
- Standard audit columns
- Tenant isolation columns such as tenant_id, company_id, organization_id, school_id, unit_id when applicable

Recommended metadata sources:

- `information_schema.tables`
- `information_schema.columns`
- `information_schema.key_column_usage`
- `information_schema.referential_constraints`
- `information_schema.statistics`

## 13. Auto-Matching Strategy

The module should provide automated suggestions but never fully trust them without review.

### 13.1 Table Auto-Match Inputs

- Exact normalized name match
- Singular/plural normalization
- Prefix and suffix stripping
- Alias dictionary match
- Description similarity
- Shared key patterns
- Shared business-domain tags
- Similar column composition
- Similar foreign-key neighborhood
- Historical mappings from prior projects

### 13.2 Column Auto-Match Inputs

- Exact normalized field name
- Alias dictionary match
- Datatype compatibility
- Length compatibility
- Nullability compatibility
- Enum similarity
- Sample value similarity
- Position relevance
- Parent table confidence
- Relationship context

### 13.3 Confidence Scoring

Suggested confidence bands:

- High: 0.90 to 1.00
- Medium: 0.70 to 0.89
- Low: 0.40 to 0.69
- Reject / No Suggestion: below 0.40

### 13.4 Matching Heuristics

Normalize names before comparison:

- Lowercase all names
- Remove accents
- Replace spaces, dashes, and dots with underscore
- Convert camelCase to snake_case
- Remove common prefixes like `tb_`, `tbl_`, `cad_`, `sys_`, `legacy_`
- Remove common suffixes like `_tbl`, `_temp`, `_backup`
- Singularize/pluralize candidate names

### 13.5 Alias Dictionary

The system must support an internal dictionary for common business synonyms, for example:

| Source Term | Target Term |
|---|---|
| customer | client |
| user | person |
| class | course_class |
| doctor | professional |
| invoice | billing_document |
| branch | unit |
| company | organization |
| tenant | tenant |
| status_code | status |

This dictionary must be configurable by admins and reusable across projects.

### 13.6 Historical Learning

The module should store approved mappings as reusable suggestions for future migrations, with safeguards so that historical mappings boost confidence but never silently override current project review.

## 14. Supported Mapping Types

- One source table to one target table
- One source table to many target tables
- Many source tables to one target table
- Source field to target field
- Source computed field to target field
- Constant value to target field
- Generated UUID to target field
- Lookup remap to target foreign key
- Enum remap to normalized enum or lookup table
- Ignored source field
- Derived target field

## 15. Transformation Rules

Each field mapping may include zero or more transforms executed in order.

### 15.1 Transform Categories

- Trim whitespace
- Normalize case
- Remove formatting characters
- Date parsing and timezone conversion
- Numeric casting
- Boolean normalization
- Enum remapping
- String concatenation
- String split
- Reference lookup
- UUID generation
- Hashing when explicitly authorized for secrets or credentials
- Default fallback assignment
- Custom PHP transform hook

### 15.2 Example Transform Pipeline

```json
{
  "target_field": "document_number",
  "source_field": "cpf_raw",
  "transforms": [
    { "type": "trim" },
    { "type": "digits_only" },
    { "type": "validate_document_br" },
    { "type": "assign_if_valid" }
  ]
}
```

### 15.3 Custom Rules Governance

Custom transform hooks must be versioned, auditable, tenant-scoped where applicable, and approved before execution in production.

## 16. Data Integrity Rules

The module must validate:

- Required target fields are satisfied.
- Target unique constraints are not violated.
- Foreign keys resolve successfully.
- Datatype casts are safe.
- Date formats are valid.
- Enum and lookup values are mapped.
- Duplicate records are detected according to configurable matching rules.
- Circular dependency handling is defined.
- Parent-child load order is respected.

## 17. Referential Migration Planning

The execution engine must compute dependency order across mapped tables.

Recommended load phases:

1. Foundational lookups and reference tables
2. Core identities and organizations
3. Parent entities
4. Child entities
5. Bridge / many-to-many tables
6. Audit or historical extensions
7. Post-load reconciliation and backfilling

Where circular references exist, the engine should support staged inserts followed by deferred foreign-key resolution.

## 18. Duplicate Resolution

The module must support duplicate handling strategies per entity type:

- Strict insert only
- Upsert by external ID
- Upsert by natural key
- Fuzzy review queue
- Manual conflict resolution
- Skip duplicates and log

Example duplicate keys:

- Email
- National ID
- Legacy external ID
- Organization code
- Composite natural key

## 19. Validation Engine

### 19.1 Validation Layers

- JSON structure validation
- Source schema semantic validation
- Target compatibility validation
- Table mapping completeness validation
- Field mapping completeness validation
- Transformation validation
- Referential integrity simulation
- Duplicate detection validation
- Security validation
- Execution readiness validation

### 19.2 Validation Severity

- Error: blocks progression
- Warning: allows progression with approval
- Info: advisory only

### 19.3 Example Errors

- Required target field has no mapped source or default.
- FK target cannot be resolved.
- Target enum has unmapped legacy value.
- Transform output type does not match target column type.
- Source table marked mapped but all columns unresolved.

## 20. Dry Run Requirements

The module must support dry run execution before live migration.

Dry run outputs:

- Insert count by table
- Update count by table
- Skipped rows by rule
- Transformation failures
- Duplicate conflicts
- FK failures
- Sample before/after preview
- Execution duration estimate
- Rollback feasibility note

Dry run should execute against a safe isolated target, never directly against live tenant data.

## 21. Live Execution Controls

### 21.1 Preconditions

- Migration project status = Approved for Execution
- Validation status = Passed or Passed with approved warnings
- Dry run status = Passed
- Authorized role confirmation
- Optional second approver for high-risk clients
- Backup snapshot confirmation

### 21.2 Execution Safety Controls

- Transaction batching
- Checkpoints per phase
- Idempotency token for job execution
- Pause and resume support
- Failure isolation by table batch
- Post-batch commit logging
- Retry policy with capped attempts
- Rollback metadata generation

## 22. Audit and Compliance

Every migration action must be auditable.

Required audit records:

- Project creation
- JSON upload
- Schema parse version
- Mapping changes
- Auto-match suggestions accepted or rejected
- Validation runs
- Dry run runs
- Approval events
- Execution start and end
- Errors and exceptions
- User identity and timestamp for each action

Compliance considerations:

- Sensitive fields must be masked in previews where required.
- PII access must be role-controlled.
- Logs must avoid storing secrets in plain text.
- Audit data retention must follow platform policy.
- Exported reports must be traceable and integrity-protected.

## 23. Security Requirements

- Admin-only or explicitly permissioned access.
- CSRF protection for state-changing endpoints.
- Strict server-side authorization checks.
- File upload validation for JSON MIME and size.
- Malware scanning if file upload pipeline supports it.
- Rate limiting on import endpoints.
- Output encoding in UI to prevent XSS from legacy labels or sample values.
- Signed action logs for sensitive approvals where applicable.
- Secrets and credentials must never be migrated in raw reversible form unless a separate approved security process exists.

## 24. Suggested Status Model

### 24.1 Project Status

- Draft
- Imported
- Mapping In Progress
- Validation Failed
- Ready for Dry Run
- Dry Run Failed
- Ready for Approval
- Approved
- Executing
- Partially Completed
- Completed
- Completed With Warnings
- Cancelled

### 24.2 Mapping Status

- Unmapped
- Suggested
- Reviewed
- Approved
- Ignored
- Blocked

## 25. Recommended Database Design

Suggested core tables for the migration module:

### 25.1 `migration_projects`

- id
- tenant_id or platform scope field
- client_id
- name
- source_system
- source_version
- source_db_type
- status
- risk_level
- created_by
- approved_by
- executed_by
- created_at
- updated_at
- executed_at

### 25.2 `migration_imports`

- id
- migration_project_id
- file_name
- file_hash
- import_format
- raw_json_path or blob reference
- parsed_schema_version
- imported_by
- imported_at

### 25.3 `migration_source_tables`

- id
- migration_project_id
- source_table_name
- normalized_name
- description
- row_estimate
- primary_key_json
- metadata_json

### 25.4 `migration_source_columns`

- id
- source_table_id
- source_column_name
- normalized_name
- source_data_type
- length_value
- precision_value
- scale_value
- nullable_flag
- default_value
- sample_values_json
- metadata_json

### 25.5 `migration_target_tables_cache`

Cache snapshot of current platform schema at project creation time.

### 25.6 `migration_table_mappings`

- id
- migration_project_id
- target_table_name
- source_table_id
- mapping_type
- confidence_score
- suggestion_source
- status
- approved_by
- approved_at
- notes

### 25.7 `migration_column_mappings`

- id
- table_mapping_id
- target_column_name
- source_column_id
- transform_pipeline_json
- default_value_json
- null_strategy
- confidence_score
- status
- validation_notes

### 25.8 `migration_value_maps`

For enum and lookup remaps.

### 25.9 `migration_validation_runs`

- id
- migration_project_id
- run_type
- status
- summary_json
- started_at
- finished_at
- triggered_by

### 25.10 `migration_execution_jobs`

- id
- migration_project_id
- idempotency_key
- environment
- execution_mode
- status
- progress_json
- error_summary_json
- started_at
- finished_at

### 25.11 `migration_audit_logs`

- id
- migration_project_id
- actor_user_id
- action_type
- entity_type
- entity_id
- before_json
- after_json
- ip_address
- user_agent
- created_at

## 26. API Design Proposal

Base namespace recommendation:

`/api/admin/migrations`

### 26.1 Project Endpoints

- `POST /api/admin/migrations/projects`
- `GET /api/admin/migrations/projects`
- `GET /api/admin/migrations/projects/{id}`
- `PATCH /api/admin/migrations/projects/{id}`

### 26.2 Import Endpoints

- `POST /api/admin/migrations/projects/{id}/import-json`
- `POST /api/admin/migrations/projects/{id}/parse`
- `GET /api/admin/migrations/projects/{id}/source-schema`
- `GET /api/admin/migrations/projects/{id}/target-schema`

### 26.3 Mapping Endpoints

- `POST /api/admin/migrations/projects/{id}/auto-match-tables`
- `POST /api/admin/migrations/projects/{id}/auto-match-columns`
- `GET /api/admin/migrations/projects/{id}/table-mappings`
- `PUT /api/admin/migrations/projects/{id}/table-mappings/{mappingId}`
- `GET /api/admin/migrations/projects/{id}/column-mappings`
- `PUT /api/admin/migrations/projects/{id}/column-mappings/{mappingId}`
- `POST /api/admin/migrations/projects/{id}/value-maps`

### 26.4 Validation and Execution Endpoints

- `POST /api/admin/migrations/projects/{id}/validate`
- `POST /api/admin/migrations/projects/{id}/dry-run`
- `POST /api/admin/migrations/projects/{id}/approve`
- `POST /api/admin/migrations/projects/{id}/execute`
- `POST /api/admin/migrations/projects/{id}/pause`
- `POST /api/admin/migrations/projects/{id}/resume`
- `GET /api/admin/migrations/projects/{id}/jobs`
- `GET /api/admin/migrations/projects/{id}/reports`

## 27. Frontend Behavior Proposal

### 27.1 Technology Notes

- PHP-rendered admin shell or PHP API backend with modular frontend pages
- Fetch API for async actions
- MariaDB as operational database
- Optional canvas or SVG layer for schema relationship drawing
- Search-first UX for large schemas

### 27.2 Key Frontend Components

- Schema tree panel
- Table card
- Relationship line layer
- Mapping drawer
- Field mapping grid
- Confidence badge
- Validation issue list
- Diff viewer for before/after mapping changes
- Dry run summary widgets
- Execution log stream panel

### 27.3 UX Expectations

- Fast filter by table name, domain tag, mapped status, confidence, relationship count
- Side-by-side synchronized scrolling option
- Click a target table highlights suggested source candidates
- Click a source table highlights suggested target candidates
- Selecting a mapping opens field-level details
- Unmatched required target fields must be visually prioritized
- Warnings should be grouped by severity and entity

## 28. Schema Visualizer Requirements

The visualizer should emulate the clarity of a schema exploration tool.

### 28.1 Visual Node Contents

Each table node should show:

- Table name
- Key icon for PK fields
- Distinct style for nullable vs non-nullable fields
- Unique markers
- FK markers
- Field datatype labels
- Optional row count estimate

### 28.2 Visual Relationships

- Target schema relationships visible in one mode
- Source schema relationships visible in another mode
- Mapping lines between source and target tables visible in mapping mode
- Toggle clutter reduction for dense schemas
- Auto layout plus manual pinning

### 28.3 Filters

- Show mapped only
- Show unmapped only
- Show warnings only
- Show high-risk only
- Show core domain only
- Search by table or column

## 29. Automation Opportunities

The module should maximize automation while preserving human approval.

### 29.1 Recommended Automatic Features

- Auto-detect table names using normalization rules
- Auto-detect columns using names, types, and samples
- Auto-suggest enum remaps from observed legacy values
- Auto-detect common audit fields like created_at, updated_at, deleted_at
- Auto-classify identity fields such as email, phone, national ID, external ID
- Auto-detect lookup tables by low cardinality and repeated references
- Auto-propose migration order based on FK graph
- Auto-generate default transforms for formatting cleanup

### 29.2 Admin Fine-Tuning Layer

Automation should produce a first draft. The admin then performs a “fine comb” review focused on:

- Low confidence mappings
- Required target fields still unresolved
- Sensitive fields
- Complex relation splits and merges
- Enum and code translations
- Duplicates and ambiguous identities

## 30. Matching Engine Proposal

A lightweight scoring engine can be implemented first, with future expansion to ML-assisted ranking.

### 30.1 Initial Deterministic Scoring Example

Score components:

- 35% name similarity
- 20% alias dictionary hit
- 15% datatype compatibility
- 10% nullability compatibility
- 10% sample value pattern similarity
- 10% relationship neighborhood similarity

### 30.2 Future Enhancements

- Project-history-assisted ranking
- Embedding-based semantic label similarity
- Domain-specific model packs for education, healthcare, finance
- Explainable suggestion cards showing why a match was proposed

## 31. Error Handling

The module must provide explicit error messages and actionable next steps.

Examples:

- Invalid JSON format: show row/character hint when possible.
- Unsupported datatype: show source field and recommended custom transform.
- FK resolution failure: show missing parent mapping.
- Duplicate conflict: show matching rule and conflicting keys.
- Permission error: show missing role or approval state.

## 32. Performance Requirements

- Must support large schemas with at least hundreds of tables and thousands of columns in the workspace.
- UI rendering should use virtualization for large lists.
- Schema layout should support lazy expansion by domain or module.
- Auto-match operations should run asynchronously with job progress.
- Heavy validation and dry run operations should run in background jobs.

## 33. Observability Requirements

- Structured logs for every import, mapping update, validation run, and execution phase
- Correlation ID per migration project and per execution job
- Metrics for parse time, match time, validation error counts, execution throughput, failure rates
- Admin-visible timeline of major actions

## 34. Notifications

Recommended notification events:

- Import completed
- Validation completed
- Dry run completed
- Approval required
- Execution started
- Execution paused
- Execution completed
- Execution failed

Delivery channels may include:

- In-app notifications
- Email for high-risk approvals
- Webhook for external orchestration

## 35. Permissions Matrix

| Action | Super Admin | Migration Analyst | Client Technical Contact | Auditor |
|---|---|---|---|---|
| Create project | Yes | Yes | No | No |
| Upload JSON | Yes | Yes | Limited optional | No |
| Edit mappings | Yes | Yes | No by default | No |
| Run validation | Yes | Yes | No | No |
| Run dry run | Yes | Yes | No | No |
| Approve execution | Yes | Optional by policy | No | No |
| Execute live migration | Yes | Optional by policy | No | No |
| View audit logs | Yes | Yes | No | Yes |
| Download reports | Yes | Yes | Limited optional | Yes |

## 36. Suggested Project States and Gates

| Stage | Required Conditions | Output |
|---|---|---|
| Import | Valid JSON package | Parsed source schema |
| Mapping | Table and field pairings reviewed | Saved mapping draft |
| Validation | Required fields and relationships checked | Validation report |
| Dry Run | Validation passed | Dry run report |
| Approval | Risk and report review completed | Approval record |
| Execution | Authorized approval present | Execution log and result report |

## 37. Example Admin Review Checklist

- Are all mandatory target tables mapped or intentionally ignored?
- Are all required target fields mapped or provided by defaults/generators?
- Are all FK relationships resolvable?
- Are enum/code translations complete?
- Are duplicate rules defined for identity-bearing entities?
- Are sensitive fields handled securely?
- Has dry run completed without blocking errors?
- Has rollback and backup readiness been confirmed?

## 38. Recommended Implementation Phases

### Phase 1

- Create migration project
- Import JSON
- Parse source schema
- Snapshot target schema
- Basic table and column auto-match
- Manual review UI

### Phase 2

- Transform pipelines
- Validation engine
- Dry run engine
- Reports and audit logs

### Phase 3

- Advanced visualizer
- Historical mapping reuse
- Multi-table merge/split support
- Background job orchestration
- Approval workflow

### Phase 4

- Domain templates by industry
- Semantic matching improvements
- External orchestration hooks
- Migration playbook library

## 39. Acceptance Criteria

### 39.1 Import

- Admin can create a migration project and upload a valid JSON package.
- System parses the source schema and stores a normalized internal representation.
- System shows parse errors clearly when package structure is invalid.

### 39.2 Visualization

- Admin can view full target schema and full source schema side by side.
- Admin can search, filter, and inspect tables and fields from both sides.
- Admin can create, edit, and remove table mappings and column mappings.

### 39.3 Automation

- System proposes automatic table and field mappings with visible confidence scores.
- System clearly differentiates accepted, suggested, rejected, and unresolved mappings.
- Admin can override any automatic suggestion.

### 39.4 Validation and Execution

- System blocks execution when blocking validation errors exist.
- System supports dry run before live execution.
- System logs all critical actions and produces a migration report.

## 40. Open Technical Decisions

- Whether raw imported JSON is stored in database, object storage, or both.
- Whether transform hooks are purely configuration-driven or can execute approved PHP classes.
- Whether execution uses direct SQL batches, ORM-assisted writes, or a dedicated migration worker service.
- Whether the visualizer is built with SVG, Canvas, or DOM-based layout engine.
- Whether approval requires one or two authorized users based on risk level.

## 41. Recommended Next Deliverables

- UI wireframe spec for the schema visualizer and mapping workspace
- Database DDL spec for migration module tables
- API contract spec with request/response examples
- JSON schema definition for client migration package
- Validation rules catalog
- Execution engine technical design

## 42. Summary Statement

This module should be treated as a controlled migration orchestration system, not just an import screen. The best implementation is a guided admin workspace that combines schema visualization, automatic matching, manual review, validation, dry run simulation, and audited execution so new client onboarding becomes faster, safer, and repeatable.
