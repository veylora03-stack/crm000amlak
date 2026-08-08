# معماری Backend — CRM تخصصی املاک

این سند معماری، پشته فناوری و اصول کلی Backend پروژه را تعریف می‌کند.

---

## 1. پشته فناوری
- Python 3.11+
- Django 5.x
- Django REST Framework (DRF)
- PostgreSQL (دیتابیس اصلی)
- Redis (Cache/Queue - اختیاری در فاز اولیه)
- Pillow (مدیریت تصاویر)
- drf-spectacular (مستندسازی OpenAPI)
- django-filter (فیلترهای پیشرفته)
- django-simple-history (تاریخچه تغییرات)
- python-decouple (متغیرهای محیطی)
- djangorestframework-simplejwt (احراز هویت JWT)
- django-cors-headers (مدیریت CORS)

## 2. اصول کلی
- همه APIها باید Prefix `/api/v1/` داشته باشند.
- احراز هویت با JWT (Simple JWT).
- Pagination استاندارد (PageNumberPagination، page_size=20، max=100).
- فرمت پاسخ‌ها JSON با ساختار استاندارد `{success, data, meta, errors}`.
- همه مدل‌های اصلی دارای `public_id` (UUID) و `Soft Delete` باشند.
- تاریخ‌ها به‌صورت timezone-aware (Asia/Tehran) ذخیره شوند.
- مبالغ به‌صورت `BigIntegerField` (عدد صحیح) ذخیره شوند.
- زبان پیش‌فرض `fa` و TimeZone `Asia/Tehran`.
- استفاده از `select_related` و `prefetch_related` برای جلوگیری از N+1.

## 3. ساختار اپلیکیشن‌ها
- `accounts`: کاربران، احراز هویت، نقش‌ها
- `clients`: مشتریان، لیدها
- `properties`: املاک، تصاویر، امکانات
- `sales`: پایپ‌لاین، Stageها، Dealها
- `activities`: تعامل‌ها، Timeline
- `tasks`: وظایف، یادآورها
- `dashboard`: KPIها، نمودارها
- `reports`: گزارش‌گیری، خروجی‌ها
- `notifications`: نوتیفیکیشن‌های داخلی
- `audit`: Audit Log
- `core`: مدل‌های پایه، تنظیمات، Utils

## 4. امنیت
- رمز عبور هش‌شده (Django default).
- JWT Expiration تنظیم‌شده.
- CORS محدود به Frontend.
- Rate limit برای Login.
- Validation کامل سمت سرور.
- محدودیت حجم و فرمت فایل‌های آپلودی.
- جلوگیری از Path Traversal.
