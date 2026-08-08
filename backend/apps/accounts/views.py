from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.permissions import IsAdmin
from apps.core.responses import success_response
from apps.core.viewsets import StandardModelViewSet

from .models import User
from .serializers import (
    ChangePasswordSerializer,
    LoginTokenObtainPairSerializer,
    ProfileSerializer,
    UserSerializer,
    UserWriteSerializer
)


class LoginRateThrottle(AnonRateThrottle):
    rate = '10/minute'


class LoginView(GenericAPIView):
    serializer_class = LoginTokenObtainPairSerializer
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            raise ValidationError({
                'refresh': 'توکن refresh الزامی است.'
            })

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            raise ValidationError({
                'refresh': 'توکن معتبر نیست.'
            })

        return Response(success_response({
            'detail': 'خروج انجام شد.'
        }))


class RefreshView(GenericAPIView):
    serializer_class = TokenRefreshSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(success_response(serializer.validated_data))


class MeView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProfileSerializer

        return UserSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])

        return Response(success_response({
            'detail': 'رمز عبور با موفقیت تغییر کرد.'
        }))


class UserViewSet(StandardModelViewSet):
    queryset = User.active_objects.all().order_by('-created_at')
    permission_classes = [IsAdmin]
    lookup_field = 'public_id'
    filterset_fields = {
        'role': ['exact'],
        'is_active': ['exact']
    }
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'username', 'role']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserWriteSerializer

        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance == request.user:
            raise ValidationError('نمی‌توانید حساب کاربری خود را حذف کنید.')

        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def activate(self, request, public_id=None):
        user = self.get_object()
        user.is_active = True
        user.save(update_fields=['is_active'])

        return Response(success_response(UserSerializer(user).data))

    @action(detail=True, methods=['post'])
    def deactivate(self, request, public_id=None):
        user = self.get_object()

        if user == request.user:
            raise ValidationError('نمی‌توانید حساب کاربری خود را غیرفعال کنید.')

        user.is_active = False
        user.save(update_fields=['is_active'])

        return Response(success_response(UserSerializer(user).data))
