# CRM تخصصی املاک

سیستم مدیریت ارتباط با مشتری (CRM) تخصصی برای آژانس‌های املاک و مشاوران املاک.

## پشته فناوری

### Backend
- Python 3.11+
- Django 5.1 + Django REST Framework
- PostgreSQL (دیتابیس)
- Simple JWT (احراز هویت)
- Redis (Cache و Queue - اختیاری)

### Frontend
- Vue 3 (Composition API)
- Vite (Build Tool)
- Pinia (State Management)
- Vue Router (Routing)
- TailwindCSS (Styling)
- ApexCharts (Charts)
- Leaflet (Maps)

## راه‌اندازی سریع

### پیش‌نیازها
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### 1. Backend Setup

cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_data
python manage.py runserver

Backend API: http://127.0.0.1:8000/api/v1/
API Docs: http://127.0.0.1:8000/api/docs/

### 2. Frontend Setup

cd frontend
npm install
npm run dev

Frontend: http://localhost:3000

## حساب‌های کاربری پیش‌فرض

| نقش | نام کاربری | رمز عبور |
|-----|-----------|----------|
| Admin | admin | admin123456 |
| Manager | manager | manager123456 |
| Agent | agent | agent123456 |

## Docker (Production)

docker-compose up -d --build

## امکانات اصلی

- مدیریت مشتریان و لیدها
- مدیریت املاک با گالری و نقشه
- Pipeline فروش (Kanban)
- مدیریت Dealها
- وظایف و یادآورها
- گزارش‌ها و خروجی Excel
- داشبورد با KPIها
- نوتیفیکیشن‌ها
- AI Voice Notes
- Smart Match

## License

MIT License
