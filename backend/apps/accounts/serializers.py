from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'public_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'phone',
            'avatar',
            'is_active',
            'last_login',
            'date_joined',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'public_id',
            'last_login',
            'date_joined',
            'created_at',
            'updated_at'
        ]


class UserWriteSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    password = serializers.CharField(
        write_only=True,
        required=False,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = [
            'public_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'phone',
            'is_active',
            'password'
        ]

    def validate(self, attrs):
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({
                'password': 'رمز عبور الزامی است.'
            })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)

        if password:
            user.set_password(password)

        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'public_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone',
            'avatar'
        ]
        read_only_fields = [
            'public_id',
            'username',
            'email'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError('رمز عبور فعلی اشتباه است.')

        return value

    def validate(self, attrs):
        if attrs.get('old_password') == attrs.get('new_password'):
            raise serializers.ValidationError({
                'new_password': 'رمز عبور جدید نمی‌تواند با رمز عبور فعلی یکسان باشد.'
            })

        return attrs


class LoginTokenObtainPairSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        identifier = str(attrs.get('identifier', '')).strip()
        password = attrs.get('password')

        user = None

        if identifier:
            user = User.active_objects.filter(username=identifier).first()

            if not user:
                user = User.active_objects.filter(email=identifier).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError({
                'identifier': 'نام کاربری یا رمز عبور اشتباه است.'
            })

        if not user.is_active:
            raise serializers.ValidationError({
                'identifier': 'حساب کاربری غیرفعال است.'
            })

        refresh = RefreshToken.for_user(user)

        return {
            'success': True,
            'data': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            },
            'meta': None,
            'errors': []
        }
