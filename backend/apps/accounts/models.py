import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from apps.core.models import SoftDeleteManager
from apps.core.validators import validate_phone_number


class RoleChoices(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    MANAGER = 'Manager', 'Manager'
    AGENT = 'Agent', 'Agent'
    CLIENT = 'Client', 'Client'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('نام کاربری الزامی است.')

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', RoleChoices.AGENT)

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', RoleChoices.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('کاربر مدیر باید is_staff=True داشته باشد.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('کاربر مدیر باید is_superuser=True داشته باشد.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(blank=True, default='', db_index=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.AGENT,
        db_index=True
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default='',
        validators=[validate_phone_number]
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    all_objects = models.Manager()
    active_objects = SoftDeleteManager()

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.username

    def delete(self, using=None, keep_parents=False):
        from django.utils import timezone

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def hard_delete(self):
        super().delete()
