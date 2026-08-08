# معماری API — CRM تخصصی املاک

این سند Endpointها و ساختار پاسخ‌های API را تعریف می‌کند.

---

## 1. ساختار پاسخ‌ها

### پاسخ موفق
{
  "success": true,
  "data": {},
  "meta": { "page": 1, "page_size": 20, "total": 0 },
  "errors": []
}

### پاسخ خطا
{
  "success": false,
  "data": null,
  "meta": null,
  "errors": [
    { "code": "VALIDATION_ERROR", "field": "phone", "message": "شماره موبایل معتبر نیست." }
  ]
}

## 2. Endpointهای اصلی

### Auth
- POST /api/v1/auth/login/
- POST /api/v1/auth/logout/
- POST /api/v1/auth/refresh/
- GET /api/v1/auth/me/
- PATCH /api/v1/auth/me/
- POST /api/v1/auth/change-password/

### Users
- CRUD /api/v1/users/
- POST /api/v1/users/{id}/activate/
- POST /api/v1/users/{id}/deactivate/

### Clients
- CRUD /api/v1/clients/
- GET /api/v1/clients/{id}/timeline/
- GET /api/v1/clients/{id}/deals/
- GET /api/v1/clients/{id}/interactions/
- POST /api/v1/clients/{id}/assign/
- POST /api/v1/clients/import/
- GET /api/v1/clients/export/

### Properties
- CRUD /api/v1/properties/
- POST /api/v1/properties/{id}/images/
- PATCH /api/v1/properties/{id}/images/reorder/
- POST /api/v1/properties/{id}/publish/
- POST /api/v1/properties/{id}/archive/
- GET /api/v1/properties/{id}/similar/
- GET /api/v1/properties/{id}/matches/
- POST /api/v1/properties/import/
- GET /api/v1/properties/export/

### Pipelines / Stages / Deals
- CRUD /api/v1/pipelines/
- CRUD /api/v1/stages/
- CRUD /api/v1/deals/
- POST /api/v1/deals/{id}/move/
- GET /api/v1/deals/{id}/timeline/

### Interactions
- CRUD /api/v1/interactions/

### Tasks
- CRUD /api/v1/tasks/
- POST /api/v1/tasks/{id}/complete/

### Dashboard
- GET /api/v1/dashboard/kpis/
- GET /api/v1/dashboard/charts/
- GET /api/v1/dashboard/recent-activities/

### Reports
- GET /api/v1/reports/leads/
- GET /api/v1/reports/deals/
- GET /api/v1/reports/agents/
- GET /api/v1/reports/funnel/
- GET /api/v1/reports/properties/
- GET /api/v1/reports/export/

### Notifications
- GET /api/v1/notifications/
- POST /api/v1/notifications/{id}/read/
- POST /api/v1/notifications/read-all/

### Settings
- GET /api/v1/settings/
- PATCH /api/v1/settings/
- CRUD برای مقادیر پایه (property-types, lead-sources, etc.)

### Search
- GET /api/v1/search/?q=...

### Audit
- GET /api/v1/audit-logs/

### AI Voice Note
- POST /api/v1/ai/voice-notes/
- GET /api/v1/ai/voice-notes/{id}/
