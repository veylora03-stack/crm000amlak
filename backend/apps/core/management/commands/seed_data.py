from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from apps.clients.models import Client
from apps.properties.models import Property, PropertyImage
from apps.sales.models import Deal, Pipeline, Stage
from apps.tasks.models import Task
from apps.notifications.models import Notification

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Starting seed...')

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                password='admin123456',
                email='admin@example.com',
                first_name='مدیر',
                last_name='سیستم',
                role='Admin'
            )
            self.stdout.write(f'Created admin user: {admin.username}')

        # Create manager user
        if not User.objects.filter(username='manager').exists():
            manager = User.objects.create_user(
                username='manager',
                password='manager123456',
                email='manager@example.com',
                first_name='مدیر',
                last_name='فروش',
                role='Manager'
            )
            self.stdout.write(f'Created manager user: {manager.username}')

        # Create agent user
        if not User.objects.filter(username='agent').exists():
            agent = User.objects.create_user(
                username='agent',
                password='agent123456',
                email='agent@example.com',
                first_name='کارشناس',
                last_name='فروش',
                role='Agent'
            )
            self.stdout.write(f'Created agent user: {agent.username}')

        admin = User.objects.get(username='admin')
        manager = User.objects.get(username='manager')
        agent = User.objects.get(username='agent')

        # Create Pipeline
        pipeline, created = Pipeline.objects.get_or_create(
            name='پایپ‌لاین فروش مسکونی',
            defaults={
                'description': 'پایپ‌لاین پیش‌فرض برای فروش املاک مسکونی',
                'is_active': True,
                'sort_order': 1
            }
        )
        if created:
            self.stdout.write(f'Created pipeline: {pipeline.name}')

        # Create Stages
        stages_data = [
            ('لید جدید', '#3b82f6', 1, False, False),
            ('تماس اولیه', '#60a5fa', 2, False, False),
            ('نیازسنجی', '#22d3ee', 3, False, False),
            ('معرفی ملک', '#fbbf24', 4, False, False),
            ('بازدید', '#f59e0b', 5, False, False),
            ('مذاکره', '#a78bfa', 6, False, False),
            ('پیشنهاد قیمت', '#8b5cf6', 7, False, False),
            ('در حال عقد قرارداد', '#fb7185', 8, False, False),
            ('برنده', '#22c55e', 9, True, False),
            ('بازنده', '#ef4444', 10, False, True),
        ]

        stages = {}
        for name, color, sort_order, is_won, is_lost in stages_data:
            stage, created = Stage.objects.get_or_create(
                pipeline=pipeline,
                name=name,
                defaults={
                    'color': color,
                    'sort_order': sort_order,
                    'is_won_stage': is_won,
                    'is_lost_stage': is_lost
                }
            )
            stages[name] = stage
            if created:
                self.stdout.write(f'Created stage: {stage.name}')

        # Create Clients
        clients_data = [
            ('علی رضایی', '09121111111', 'ali@example.com', 'اینستاگرام', 'New', 'خریدار', 5000000000, 8000000000),
            ('مریم احمدی', '09122222222', 'maryam@example.com', 'معرفی', 'Contacted', 'مستأجر', 300000000, 600000000),
            ('حسین کریمی', '09123333333', 'hossein@example.com', 'وب‌سایت', 'Qualified', 'فروشنده', 0, 0),
            ('زهرا محمدی', '09124444444', 'zahra@example.com', 'تماس ورودی', 'Negotiating', 'خریدار', 7000000000, 10000000000),
            ('رضا جعفری', '09125555555', 'reza@example.com', 'اینستاگرام', 'Won', 'خریدار', 4000000000, 6000000000),
        ]

        clients = {}
        for full_name, phone, email, source, status, customer_type, budget_min, budget_max in clients_data:
            client, created = Client.objects.get_or_create(
                phone=phone,
                defaults={
                    'full_name': full_name,
                    'email': email,
                    'source': source,
                    'status': status,
                    'customer_type': customer_type,
                    'budget_min': budget_min,
                    'budget_max': budget_max,
                    'assigned_agent': agent,
                    'created_by': admin
                }
            )
            clients[full_name] = client
            if created:
                self.stdout.write(f'Created client: {client.full_name}')

        # Create Properties
        properties_data = [
            ('AP-1001', 'آپارتمان 85 متری سعادت‌آباد', 'آپارتمان', 'فروش', 'Published', 'Published', 7500000000, 0, 0, 85, 2, 'تهران', 'سعادت‌آباد'),
            ('VL-2001', 'ویلا 250 متری لواسان', 'ویلا', 'فروش', 'Published', 'Published', 25000000000, 0, 0, 250, 3, 'لواسان', 'مرکز'),
            ('AP-1002', 'آپارتمان 120 متری ونک', 'آپارتمان', 'اجاره', 'Published', 'Published', 0, 500000000, 25000000, 120, 3, 'تهران', 'ونک'),
        ]

        properties = {}
        for code, title, property_type, listing_type, status, publish_status, price, deposit, rent, area, bedrooms, city, district in properties_data:
            property_obj, created = Property.objects.get_or_create(
                code=code,
                defaults={
                    'title': title,
                    'property_type': property_type,
                    'listing_type': listing_type,
                    'status': status,
                    'publish_status': publish_status,
                    'price': price,
                    'deposit_amount': deposit,
                    'rent_amount': rent,
                    'building_area': area,
                    'bedrooms': bedrooms,
                    'city': city,
                    'district': district,
                    'assigned_agent': agent,
                    'created_by': admin
                }
            )
            properties[code] = property_obj
            if created:
                self.stdout.write(f'Created property: {property_obj.title}')

        # Create Deals
        deals_data = [
            ('خرید آپارتمان سعادت‌آباد', 'علی رضایی', 'AP-1001', 'نیازسنجی', 'Open', 7000000000, 60),
            ('اجاره واحد اداری ونک', 'مریم احمدی', 'AP-1002', 'تماس اولیه', 'Open', 600000000, 40),
        ]

        for title, client_name, property_code, stage_name, status, amount, probability in deals_data:
            client = clients.get(client_name)
            property_obj = properties.get(property_code)
            stage = stages.get(stage_name)

            deal, created = Deal.objects.get_or_create(
                title=title,
                defaults={
                    'client': client,
                    'property': property_obj,
                    'pipeline': pipeline,
                    'stage': stage,
                    'agent': agent,
                    'amount': amount,
                    'probability': probability,
                    'status': status,
                    'created_by': admin
                }
            )
            if created:
                self.stdout.write(f'Created deal: {deal.title}')

        # Create Tasks
        tasks_data = [
            ('تماس با علی رضایی', agent, 'High', 'Todo'),
            ('ارسال فایل ویلا به حسین کریمی', agent, 'Medium', 'In Progress'),
            ('پیگیری قرارداد اجاره', manager, 'Urgent', 'Todo'),
        ]

        for title, assigned_user, priority, status in tasks_data:
            task, created = Task.objects.get_or_create(
                title=title,
                defaults={
                    'assigned_user': assigned_user,
                    'priority': priority,
                    'status': status,
                    'created_by': admin
                }
            )
            if created:
                self.stdout.write(f'Created task: {task.title}')

        # Create Notifications
        notifications_data = [
            (admin, 'task_due', 'سررسید وظیفه', 'وظیفه «تماس با علی رضایی» امروز سررسید دارد.'),
            (admin, 'stage_move', 'تغییر Stage معامله', 'معامله «خرید آپارتمان سعادت‌آباد» به مرحله نیازسنجی منتقل شد.'),
            (agent, 'client_assigned', 'تخصیص مشتری', 'مشتری «مریم احمدی» به شما تخصیص داده شد.'),
        ]

        for user, notif_type, title, body in notifications_data:
            notification, created = Notification.objects.get_or_create(
                user=user,
                title=title,
                defaults={
                    'type': notif_type,
                    'body': body
                }
            )
            if created:
                self.stdout.write(f'Created notification: {notification.title}')

        self.stdout.write(self.style.SUCCESS('Seed completed successfully!'))
