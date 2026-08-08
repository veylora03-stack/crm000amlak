# خلاصه پروژه CRM تخصصی املاک

## فازهای تکمیل شده

### فاز 1: طراحی UI/UX
- تعریف پرسوناها
- طراحی User Journeys
- طراحی Wireframes
- تعریف Design Tokens
- طراحی کامپوننت‌ها

### فاز 2: پیاده‌سازی Frontend
- Vue 3 + Vite + Tailwind
- Vue Router + Pinia
- تمام صفحات اصلی
- API Integration Layer

### فاز 3: پیاده‌سازی Backend
- Django 5.1 + DRF
- PostgreSQL Database
- JWT Authentication
- تمام مدل‌های اصلی
- تمام API Endpoints

### فاز 4: یکپارچه‌سازی
- اتصال Frontend به Backend
- Docker Configuration
- مستندات کامل

## نحوه اجرا

### Development Mode
cd backend
source .venv/bin/activate
python manage.py runserver

cd frontend
npm run dev

### Production (Docker)
docker-compose up -d

## دسترسی‌ها

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/v1/
- API Docs: http://localhost:8000/api/docs/

### حساب‌های کاربری
- Admin: admin / admin123456
- Manager: manager / manager123456
- Agent: agent / agent123456

## امکانات پیاده‌سازی شده

- احراز هویت JWT
- مدیریت کاربران و نقش‌ها
- مدیریت مشتریان (CRUD + Timeline)
- مدیریت املاک (CRUD + Images)
- Pipeline فروش (Kanban)
- مدیریت Dealها
- وظایف (Calendar View)
- نوتیفیکیشن‌ها
- داشبورد (KPI + Charts)
- گزارش‌ها (Export CSV/Excel)
- جستجوی سراسری
- Dark Mode
- Responsive Design
- RTL Support

## License

MIT License
