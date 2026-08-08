# راهنمای بهینه‌سازی Performance

## Frontend Optimization

### 1. Code Splitting
Vite به صورت خودکار code splitting انجام می‌دهد.
برای route-based splitting:
const DashboardPage = () => import('@/pages/dashboard/DashboardPage.vue')

### 2. Lazy Loading Components
کامپوننت‌های سنگین را lazy load کنید:
const ChartCard = defineAsyncComponent(() =>
  import('@/components/dashboard/ChartCard.vue')
)

### 3. Image Optimization
- از فرمت WebP استفاده کنید
- lazy loading برای تصاویر:
<img loading="lazy" src="..." />
- responsive images با srcset

### 4. Bundle Analysis
npm install -D rollup-plugin-visualizer
اضافه کردن به vite.config.js:
import { visualizer } from 'rollup-plugin-visualizer'
plugins: [visualizer({ open: true })]

### 5. Caching
- Cache API responses در Pinia stores
- localStorage برای داده‌های کم‌تغییر
- Service Worker برای offline support

## Backend Optimization

### 1. Database Query Optimization

#### استفاده از select_related و prefetch_related
# Bad
clients = Client.objects.all()
for client in clients:
    print(client.assigned_agent.full_name)

# Good
clients = Client.objects.select_related('assigned_agent').all()

#### استفاده از values() برای داده‌های ساده
# Bad
clients = Client.objects.all()
names = [c.full_name for c in clients]

# Good
names = Client.objects.values_list('full_name', flat=True)

### 2. Pagination
همیشه از pagination استفاده کنید:
class StandardPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100

### 3. Caching

#### Redis Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

#### Cache View Response
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def dashboard_kpis(request):
    ...

#### Cache QuerySet
from django.core.cache import cache

def get_active_properties():
    cache_key = 'active_properties'
    properties = cache.get(cache_key)
    
    if properties is None:
        properties = list(Property.objects.filter(publish_status='Published'))
        cache.set(cache_key, properties, timeout=300)
    
    return properties

### 4. Async Processing با Celery

#### نصب Celery
pip install celery redis

#### celery.py در config/
from celery import Celery

app = Celery('crm_amlak')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#### Task تعریف کنید
from celery import shared_task

@shared_task
def send_email_task(subject, message, recipient_list):
    send_mail(subject, message, 'noreply@example.com', recipient_list)

#### اجرا در view
send_email_task.delay('Subject', 'Message', ['user@example.com'])

### 5. Database Indexes

#### اضافه کردن index برای فیلدهای پرکاربرد
class Meta:
    indexes = [
        models.Index(fields=['status', 'created_at']),
        models.Index(fields=['assigned_agent', 'status']),
    ]

### 6. Connection Pooling

#### PostgreSQL Connection Pool
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crm_amlak',
        'CONN_MAX_AGE': 600,  # 10 minutes
    }
}

## Monitoring

### 1. Django Debug Toolbar (Development)
pip install django-debug-toolbar

INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

### 2. Sentry (Production)
pip install sentry-sdk

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)

### 3. Prometheus + Grafana
pip install django-prometheus

INSTALLED_APPS += ['django_prometheus']
MIDDLEWARE = ['django_prometheus.middleware.PrometheusBeforeMiddleware'] + MIDDLEWARE

## Checklist بهینه‌سازی

- [ ] استفاده از select_related/prefetch_related
- [ ] Pagination برای همه list endpoints
- [ ] Cache برای داده‌های کم‌تغییر
- [ ] Lazy loading برای کامپوننت‌های سنگین
- [ ] Image optimization
- [ ] Database indexes
- [ ] Async processing برای taskهای سنگین
- [ ] Monitoring و error tracking
- [ ] CDN برای static files
- [ ] Gzip compression
