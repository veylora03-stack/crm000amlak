# راهنمای Deployment

## Development Environment

### Backend
cd backend
source .venv/bin/activate
python manage.py runserver

### Frontend
cd frontend
npm run dev

## Production Deployment

### گزینه 1: Docker Compose (توصیه شده)

docker-compose up -d --build

سرویس‌ها:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### گزینه 2: Manual Deployment

#### Backend

1. نصب وابستگی‌ها:
pip install -r requirements.txt

2. تنظیم متغیرهای محیطی:
export DEBUG=False
export SECRET_KEY=your-production-secret-key
export DB_NAME=crm_amlak
export DB_USER=postgres
export DB_PASSWORD=your-db-password
export DB_HOST=your-db-host
export DB_PORT=5432

3. جمع‌آوری static files:
python manage.py collectstatic --noinput

4. اجرای migrations:
python manage.py migrate

5. اجرا با Gunicorn:
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

#### Frontend

1. نصب وابستگی‌ها:
npm install

2. Build:
npm run build

3. سرو کردن dist/ با Nginx:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

## Environment Variables

### Backend (.env)

DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

DB_NAME=crm_amlak
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0

CORS_ALLOWED_ORIGINS=https://your-domain.com

JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

OPENAI_API_KEY=your-openai-api-key

### Frontend (.env.production)

VITE_API_BASE_URL=https://your-domain.com/api/v1

## Nginx Configuration

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    sendfile on;
    keepalive_timeout 65;
    client_max_body_size 20M;

    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json application/javascript;

    server {
        listen 80;
        server_name your-domain.com www.your-domain.com;

        location / {
            root /var/www/crm-amlak/frontend/dist;
            try_files $uri $uri/ /index.html;
        }

        location /api {
            proxy_pass http://127.0.0.1:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }

        location /media {
            alias /var/www/crm-amlak/backend/media;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        location /static {
            alias /var/www/crm-amlak/backend/staticfiles;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
    }
}

## SSL with Let's Encrypt

1. نصب certbot:
sudo apt install certbot python3-certbot-nginx

2. دریافت certificate:
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

3. تمدید خودکار:
sudo certbot renew --dry-run

## Backup

### Database Backup
pg_dump -U postgres -d crm_amlak > backup_$(date +%Y%m%d).sql

### Restore
psql -U postgres -d crm_amlak < backup_20240101.sql

### Media Backup
tar -czf media_backup_$(date +%Y%m%d).tar.gz backend/media/

## Monitoring

### Logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
journalctl -u gunicorn -f

### Health Check
curl http://localhost:8000/api/v1/health/

## Troubleshooting

### Backend اجرا نمی‌شود
- بررسی logs: python manage.py runserver
- بررسی database connection: psql -U postgres -h localhost
- بررسی متغیرهای محیطی

### Frontend اجرا نمی‌شود
- بررسی console browser
- بررسی network tab
- بررسی CORS settings

### API خطا می‌دهد
- بررسی authentication token
- بررسی permissions
- بررسی validation errors در response

### Performance Issues
- بررسی database queries (N+1 problem)
- بررسی cache
- بررسی static files serving
