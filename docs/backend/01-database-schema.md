# معماری داده و Schema — CRM تخصصی املاک

این سند ساختار دیتابیس و مدل‌های اصلی را تعریف می‌کند.

---

## 1. اصول دیتابیس
- استفاده از PostgreSQL
- BigAutoField برای id
- UUIDField برای public_id
- Soft Delete برای موجودیت‌های اصلی (is_deleted)
- Index برای فیلدهای پرکاربرد
- DateTimeField(timezone=True)
- BigIntegerField برای مبالغ

## 2. مدل‌های اصلی

### accounts.User
- id, public_id, username, email, password_hash, first_name, last_name
- role (Admin, Manager, Agent, Client)
- phone, avatar, is_active, is_staff, last_login
- created_at, updated_at

### clients.Client
- id, public_id, full_name, phone, email, source, status
- customer_type, budget_min, budget_max
- preferred_areas (JSON), preferred_property_types (JSON)
- notes, assigned_agent (FK), score, is_deleted
- created_by, updated_by, created_at, updated_at

### properties.Property
- id, public_id, code, title, slug
- property_type, listing_type, status, publish_status
- price, deposit_amount, rent_amount (BigInteger)
- land_area, building_area, bedrooms, bathrooms, parking_count
- floor_number, total_floors, year_built
- address, province, city, district, neighborhood
- latitude, longitude, description
- amenities (JSON), owner_client (FK), assigned_agent (FK)
- is_deleted, created_by, updated_by, created_at, updated_at

### properties.PropertyImage
- id, public_id, property (FK), image, thumbnail, alt_text
- sort_order, is_primary, created_at

### sales.Pipeline
- id, public_id, name, description, is_active, sort_order

### sales.Stage
- id, public_id, pipeline (FK), name, color, sort_order
- is_won_stage, is_lost_stage

### sales.Deal
- id, public_id, title, client (FK), property (FK)
- pipeline (FK), stage (FK), agent (FK)
- amount (BigInteger), probability, expected_close_date
- source, status, lost_reason, won_reason, notes
- is_deleted, created_by, updated_by, created_at, updated_at

### activities.Interaction
- id, public_id, interaction_type
- client (FK), deal (FK), property (FK), agent (FK)
- title, body, occurred_at, duration_minutes
- needs_followup, followup_at
- created_by, created_at, updated_at

### tasks.Task
- id, public_id, title, description
- assigned_user (FK), client (FK), deal (FK), property (FK)
- priority, status, due_date, due_time, completed_at
- created_by, created_at, updated_at

### notifications.Notification
- id, public_id, user (FK), type, title, body
- payload (JSON), is_read, read_at, created_at

### audit.AuditLog
- id, user (FK), action, entity_name, entity_id
- before_data (JSON), after_data (JSON)
- ip, user_agent, created_at

### core.MatchScore
- id, client (FK), property (FK), score
- matched_fields (JSON), created_at, updated_at

## 3. Indexهای پیشنهادی
- Client: phone, email, status, assigned_agent, created_at
- Property: code, status, property_type, city, price, created_at
- Deal: stage, pipeline, agent, status, expected_close_date
- Interaction: client, deal, occurred_at
- Task: assigned_user, status, due_date
- AuditLog: entity_name, entity_id, created_at
