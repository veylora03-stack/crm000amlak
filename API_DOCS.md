# مستندات API

## Base URL
http://localhost:8000/api/v1/

## Authentication

### Login
POST /auth/login/

Request:
{
  "identifier": "admin",
  "password": "admin123456"
}

Response:
{
  "success": true,
  "data": {
    "access": "eyJ...",
    "refresh": "eyJ...",
    "user": {
      "public_id": "uuid",
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "مدیر سیستم",
      "role": "Admin"
    }
  },
  "meta": null,
  "errors": []
}

### Refresh Token
POST /auth/refresh/

Request:
{
  "refresh": "eyJ..."
}

Response:
{
  "success": true,
  "data": {
    "access": "eyJ...",
    "refresh": "eyJ..."
  },
  "meta": null,
  "errors": []
}

### Get Current User
GET /auth/me/

Headers:
Authorization: Bearer <access_token>

Response:
{
  "success": true,
  "data": {
    "public_id": "uuid",
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "مدیر سیستم",
    "role": "Admin",
    "phone": "",
    "avatar": null
  },
  "meta": null,
  "errors": []
}

## Clients

### List Clients
GET /clients/

Query Parameters:
- page: شماره صفحه (default: 1)
- page_size: تعداد آیتم در صفحه (default: 20, max: 100)
- search: جستجو در نام، موبایل، ایمیل
- status: فیلتر وضعیت
- customer_type: فیلتر نوع مشتری
- source: فیلتر منبع
- assigned_agent: فیلتر Agent مسئول

Response:
{
  "success": true,
  "data": [
    {
      "public_id": "uuid",
      "full_name": "علی رضایی",
      "phone": "09121111111",
      "email": "ali@example.com",
      "status": "New",
      "customer_type": "خریدار",
      "source": "اینستاگرام",
      "budget_min": 5000000000,
      "budget_max": 8000000000,
      "assigned_agent_name": "کارشناس فروش",
      "created_at": "2024-01-01T10:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 100
  },
  "errors": []
}

### Create Client
POST /clients/

Request:
{
  "full_name": "علی رضایی",
  "phone": "09121111111",
  "email": "ali@example.com",
  "source": "اینستاگرام",
  "status": "New",
  "customer_type": "خریدار",
  "budget_min": 5000000000,
  "budget_max": 8000000000,
  "preferred_areas": ["تهران - سعادت‌آباد"],
  "preferred_property_types": ["آپارتمان"],
  "notes": "توضیحات",
  "assigned_agent": "uuid"
}

### Get Client
GET /clients/{public_id}/

### Update Client
PATCH /clients/{public_id}/

### Delete Client
DELETE /clients/{public_id}/

### Get Client Timeline
GET /clients/{public_id}/timeline/

### Get Client Deals
GET /clients/{public_id}/deals/

### Assign Client
POST /clients/{public_id}/assign/

Request:
{
  "assigned_agent": "uuid"
}

## Properties

### List Properties
GET /properties/

Query Parameters:
- page, page_size
- search
- property_type
- listing_type
- status
- publish_status
- city
- district
- price_min, price_max
- assigned_agent

### Create Property
POST /properties/

Request:
{
  "code": "AP-1001",
  "title": "آپارتمان 85 متری سعادت‌آباد",
  "property_type": "آپارتمان",
  "listing_type": "فروش",
  "status": "Draft",
  "publish_status": "Draft",
  "price": 7500000000,
  "deposit_amount": 0,
  "rent_amount": 0,
  "building_area": 85,
  "bedrooms": 2,
  "bathrooms": 1,
  "city": "تهران",
  "district": "سعادت‌آباد",
  "description": "توضیحات"
}

### Upload Property Image
POST /properties/{public_id}/images/

Content-Type: multipart/form-data

Form Data:
- image: فایل تصویر
- alt_text: متن جایگزین
- is_primary: true/false

## Deals

### List Deals
GET /deals/

Query Parameters:
- page, page_size
- search
- pipeline
- stage
- agent
- status
- amount_min, amount_max
- expected_close_date_from, expected_close_date_to

### Create Deal
POST /deals/

Request:
{
  "title": "خرید آپارتمان سعادت‌آباد",
  "client": "uuid",
  "property": "uuid",
  "pipeline": "uuid",
  "stage": "uuid",
  "agent": "uuid",
  "amount": 7000000000,
  "probability": 60,
  "expected_close_date": "2024-03-15",
  "status": "Open"
}

### Move Deal
POST /deals/{public_id}/move/

Request:
{
  "stage": "uuid"
}

## Tasks

### List Tasks
GET /tasks/

Query Parameters:
- page, page_size
- assigned_user
- priority
- status
- due_date_from, due_date_to

### Create Task
POST /tasks/

Request:
{
  "title": "تماس با علی رضایی",
  "description": "پیگیری بازدید دوم",
  "priority": "High",
  "status": "Todo",
  "due_date": "2024-01-15",
  "due_time": "14:00",
  "client": "uuid",
  "deal": "uuid"
}

### Complete Task
POST /tasks/{public_id}/complete/

## Dashboard

### Get KPIs
GET /dashboard/kpis/

Response:
{
  "success": true,
  "data": {
    "leads_today": 3,
    "leads_week": 18,
    "active_deals": 24,
    "active_deals_value": 185000000000,
    "won_month": 6,
    "lost_month": 4,
    "conversion_rate": 18.5,
    "tasks_today": 5,
    "overdue_tasks": 2,
    "active_properties": 42
  }
}

### Get Charts
GET /dashboard/charts/

### Get Recent Activities
GET /dashboard/recent-activities/

## Reports

### Leads Report
GET /reports/leads/

Query Parameters:
- date_from, date_to
- status
- source

### Deals Report
GET /reports/deals/

Query Parameters:
- date_from, date_to
- status
- agent

### Agents Report
GET /reports/agents/

### Funnel Report
GET /reports/funnel/

Query Parameters:
- pipeline

### Export Report
GET /reports/export/

Query Parameters:
- report_type: leads|deals|properties
- format: csv|xlsx

Response: فایل CSV یا Excel

## Notifications

### List Notifications
GET /notifications/

Query Parameters:
- page, page_size
- type
- is_read

### Mark as Read
POST /notifications/{public_id}/read/

### Mark All as Read
POST /notifications/read-all/

## Error Response Format

{
  "success": false,
  "data": null,
  "meta": null,
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "field": "phone",
      "message": "شماره موبایل معتبر نیست."
    }
  ]
}

## Status Codes

- 200: موفق
- 201: ایجاد شد
- 400: خطای validation
- 401: احراز هویت نشده
- 403: دسترسی غیرمجاز
- 404: یافت نشد
- 500: خطای سرور
