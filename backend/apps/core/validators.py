import os

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^09\d{9}$',
    message='شماره موبایل معتبر نیست.'
)


def validate_phone_number(value):
    if value and not value.isdigit():
        raise ValidationError('شماره موبایل معتبر نیست.')

    if value and len(value) != 11:
        raise ValidationError('شماره موبایل معتبر نیست.')

    if value and not value.startswith('09'):
        raise ValidationError('شماره موبایل معتبر نیست.')


def validate_file_size(value, max_size_mb=10):
    max_size = max_size_mb * 1024 * 1024

    if value.size > max_size:
        raise ValidationError(f'حجم فایل بیشتر از {max_size_mb} مگابایت است.')


def validate_image_extension(value):
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    ext = os.path.splitext(value.name)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError('فرمت تصویر مجاز نیست.')
