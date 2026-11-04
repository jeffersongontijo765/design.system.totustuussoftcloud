# SPEC v2 — Global Meeting & Live Streaming Platform

**Product:** TotusTuusSoftCloud  
**Template:** Supabase-style UI/UX  
**Language:** Global English  
**Version:** 2.0.0  
**Status:** Complete technical specification

## 1. Executive Summary

This module delivers a secure, scalable, global real-time meeting and live streaming platform for education and institutional communication. It supports teacher-parent meetings, live classes, pedagogical meetings, internal administrative sessions, one-to-one conversations, webinars, and hybrid events.

The specification assumes an enterprise SaaS environment with multi-tenant isolation, per-unit access control, strict auditability, and international naming standards. All technical artifacts must follow English naming, `snake_case` database conventions, and Supabase-inspired UI patterns.

## 2. Product Principles

- Global English first.
- Security by default.
- Privacy by design.
- Multi-tenant isolation.
- Scalable real-time architecture.
- Education-friendly UX.
- Auditability for every sensitive action.
- Open standards and vendor-neutral design.

## 3. Scope

### 3.1 Included

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

### 3.2 Excluded in this version

- Native mobile apps.
- Advanced AI meeting agent.
- External marketplace integrations.
- Full white-label domain routing.
- Hardware room system integration.

## 4. Roles and Actors

- `system_admin`
- `tenant_admin`
- `unit_admin`
- `coordinator`
- `teacher`
- `student`
- `parent_guardian`
- `moderator`
- `guest`

## 5. Business Use Cases

### 5.1 Teacher and parent meeting

A teacher schedules a one-to-one meeting with a parent or guardian, shares a secure access link, and controls entry through a waiting room. The system records attendance, duration, and optional notes.

### 5.2 Live class

A teacher opens a class session for a specific group of students. Students join with role-based permissions, and the teacher controls audio, video, chat, screen sharing, and participation order.

### 5.3 Pedagogical session

A coordinator schedules a meeting with multiple teachers to discuss planning, student performance, or institutional topics. Notes, files, and outcomes can be attached to the session record.

### 5.4 Internal meeting

An internal meeting supports administrative work, policy discussion, operational planning, and sensitive coordination inside the institution.

## 6. Functional Requirements

### 6.1 Meeting management

- Create, edit, cancel, restore, and duplicate meetings.
- Support one-time and recurring meetings.
- Support meeting templates.
- Support meeting categories and tags.
- Allow host, co-host, moderator, and participant roles.
- Support default rules by tenant and unit.

### 6.2 Access control

- Require authentication for internal users.
- Allow external access only with signed, expiring tokens.
- Support manual approval from waiting room.
- Block unauthorized reuse of join links.
- Prevent cross-tenant access.
- Apply unit-level restrictions when configured.

### 6.3 Live communication

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

### 6.4 Attendance and participation

- Track join time, leave time, and total connected time.
- Mark attendance manually or automatically.
- Distinguish viewer, speaker, and presenter participation.
- Export attendance reports.
- Record participation events for compliance.

### 6.5 Recording and transcript

- Start and stop recording under explicit permission.
- Store recordings securely.
- Generate transcript from recorded or live audio if enabled.
- Link transcript to the meeting record.
- Support retention and deletion policies.

### 6.6 Notifications

- Meeting invitation email.
- Reminder before start.
- Join confirmation.
- Meeting started notice.
- Meeting ended notice.
- Recording available notice.
- Transcript ready notice.

## 7. Non-Functional Requirements

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

## 8. UI/UX Requirements

### 8.1 Visual system

- Supabase-style dark-first interface.
- Emerald accent color.
- Minimal cards and clean tables.
- Collapsible navigation groups.
- Strong empty states.
- Compact action bars.
- Consistent status badges.

### 8.2 Screen structure

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

### 8.3 Live room layout

- Main video grid.
- Active speaker focus.
- Side panel for chat and participants.
- Top action bar.
- Status indicators.
- Responsive mobile fallback.

## 9. System Architecture

### 9.1 High-level layers

- Presentation layer.
- Application layer.
- API layer.
- Realtime signaling layer.
- Media layer.
- Recording pipeline.
- Notification pipeline.
- Storage layer.
- Audit and analytics layer.

### 9.2 Media architecture

- WebRTC for media transport.
- SFU for group sessions.
- Optional P2P for very small sessions.
- Signaling over secure WebSocket or equivalent.
- Recording as asynchronous media job.
- Separate storage for artifacts and metadata.

### 9.3 Suggested deployment units

- API service.
- Realtime signaling service.
- Media gateway service.
- Recording worker service.
- Notification worker service.
- Audit/logging service.
- Database cluster.
- Object storage for media.

## 10. Domain Model

### 10.1 Core entities

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

### 10.2 Identifier strategy

- `id`: internal technical primary key.
- `uuid`: public external identifier.
- `code`: human-readable business code.

### 10.3 Core meeting fields

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

## 11. Database Design

### 11.1 Recommended schema rules

- Use English names only.
- Use `snake_case` consistently.
- Add indexes for tenant scope, status, scheduled time, and public UUID.
- Use soft delete where operationally useful.
- Use timestamps in UTC.
- Keep audit tables append-only.

### 11.2 Example tables

#### `meetings`

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

#### `meeting_participants`

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

#### `meeting_recordings`

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

#### `meeting_audit_logs`

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

## 12. API Specification

### 12.1 Meetings

- `POST /api/v1/meetings`
- `GET /api/v1/meetings`
- `GET /api/v1/meetings/{uuid}`
- `PATCH /api/v1/meetings/{uuid}`
- `DELETE /api/v1/meetings/{uuid}`
- `POST /api/v1/meetings/{uuid}/duplicate`
- `POST /api/v1/meetings/{uuid}/start`
- `POST /api/v1/meetings/{uuid}/end`
- `POST /api/v1/meetings/{uuid}/cancel`

### 12.2 Participation

- `POST /api/v1/meetings/{uuid}/join-token`
- `POST /api/v1/meetings/{uuid}/join`
- `POST /api/v1/meetings/{uuid}/leave`
- `GET /api/v1/meetings/{uuid}/participants`
- `PATCH /api/v1/meetings/{uuid}/participants/{participant_uuid}`
- `DELETE /api/v1/meetings/{uuid}/participants/{participant_uuid}`

### 12.3 Realtime collaboration

- `POST /api/v1/meetings/{uuid}/chat/messages`
- `GET /api/v1/meetings/{uuid}/chat/messages`
- `POST /api/v1/meetings/{uuid}/screen-share/start`
- `POST /api/v1/meetings/{uuid}/screen-share/stop`
- `POST /api/v1/meetings/{uuid}/reactions`
- `POST /api/v1/meetings/{uuid}/polls`

### 12.4 Recording and transcript

- `POST /api/v1/meetings/{uuid}/recordings/start`
- `POST /api/v1/meetings/{uuid}/recordings/stop`
- `GET /api/v1/meetings/{uuid}/recordings`
- `GET /api/v1/meetings/{uuid}/transcript`
- `POST /api/v1/meetings/{uuid}/transcript/generate`

### 12.5 Reports and audit

- `GET /api/v1/meetings/{uuid}/report`
- `GET /api/v1/meetings/{uuid}/presence`
- `GET /api/v1/meetings/{uuid}/audit-logs`
- `GET /api/v1/meetings/{uuid}/exports`

## 13. Realtime Event Contract

### 13.1 Event channels

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

### 13.2 Payload standards

- Use JSON.
- Include `tenant_uuid`, `meeting_uuid`, `actor_uuid`, `event_name`, `created_at`.
- Keep payloads minimal and versioned.
- Never expose internal secrets in events.

## 14. Security Specification

### 14.1 Authentication

- Use secure token-based auth.
- Support MFA for privileged roles.
- Session hardening for internal users.
- Optional SSO integration.

### 14.2 Authorization

- Enforce RBAC and tenant scope.
- Support policy checks by role and context.
- Protect all admin and moderation actions.

### 14.3 Media security

- Encrypt media transport.
- Sign room join tokens.
- Limit token lifetime.
- Restrict access to recordings.
- Control download permissions.

### 14.4 Abuse prevention

- Rate limiting.
- Bot protection on public joins.
- Chat moderation and profanity filtering if enabled.
- Suspicious activity logs.

## 15. Privacy and Compliance

- Consent-based recording policies.
- Data retention policies by tenant.
- Right-to-access support.
- Right-to-delete support where legally allowed.
- Audit trails for sensitive actions.
- Configurable regional policy packs.

## 16. Storage and Retention

### 16.1 Storage types

- Metadata in relational database.
- Media files in object storage.
- Logs in append-only audit store.
- Transcripts in searchable text storage.

### 16.2 Retention defaults

- Meeting metadata: per tenant policy.
- Recordings: per tenant policy.
- Transcripts: per tenant policy.
- Audit logs: long-term retention.

## 17. Error Handling

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

## 18. Observability

- Application logs.
- Security logs.
- Audit logs.
- Metrics for join success, video quality, participant counts, and recording status.
- Alerting for downtime or session failures.

## 19. Testing Requirements

- Unit tests for domain rules.
- Integration tests for APIs.
- Realtime event tests.
- Authorization tests.
- Load tests for concurrent sessions.
- Browser compatibility tests.
- Recovery tests for disconnection and reconnection.
- Security validation tests.

## 20. Deployment Requirements

- Separate environments for development, staging, and production.
- Feature flags for recording, transcript, and AI functions.
- Rolling deployment support.
- Health checks for each service.
- Backup and restore strategy.
- Object storage lifecycle rules.

## 21. Project Structure

### 21.1 Suggested folders

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

## 22. Acceptance Criteria

- All UI, database, and API names are in English.
- The interface follows Supabase-style design principles.
- Meetings can be created, scheduled, joined, moderated, recorded, and reported.
- The module supports education workflows end to end.
- Tenant isolation is enforced everywhere.
- Audit trails are complete.
- The system is ready for global deployment.

## 23. Delivery Checklist

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

## 24. Appendix — Recommended Enums

### `meeting_status`

- `draft`
- `scheduled`
- `live`
- `ended`
- `canceled`
- `archived`

### `participant_role`

- `host`
- `co_host`
- `moderator`
- `speaker`
- `listener`
- `guest`

### `access_policy`

- `private`
- `tenant_only`
- `invite_only`
- `token_required`
- `public_link`

### `join_status`

- `waiting`
- `approved`
- `joined`
- `rejected`
- `left`
