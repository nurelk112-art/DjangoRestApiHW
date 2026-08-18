from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import random
from .redis_client import redis_client
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenObtainPairSerializer

# request — принимаем;
# responses — возвращаем;
# summary — название;
# description — описание;
# tags — группировка.

from .models import ConfirmationCode
from .serializer import (
    UserRegisterSerializer,
    LoginSerializer,
)
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .google import get_google_tokens, get_google_user

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


User = get_user_model()


class ConfirmAPIView(APIView):

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "code": {"type": "string"},
                },
                "required": ["email", "code"],
            }
        },
        responses={200: dict},
    )
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        redis_key = f"confirmation:{user.email}"

        saved_code = redis_client.get(redis_key)

        if saved_code is None:
            return Response(
                {"error": "Code expired or not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if saved_code == code:
            user.is_active = True
            user.save()

            redis_client.delete(redis_key)

            return Response({"message": "User confirmed"})

        return Response(
            {"error": "Wrong code"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AuthorizationAPIView(APIView):

    @extend_schema(
        request=LoginSerializer,
        responses={200: dict},
    )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"key": token.key})


class RegistrationAPIView(APIView):

    @extend_schema(
        request=UserRegisterSerializer,
        responses={201: dict},
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        code = str(random.randint(100000, 999999))

        redis_client.set(
            f"confirmation:{user.email}",
            code,
            ex=300,
        )

        return Response(
            {
                "user_id": user.id,
                "email": user.email,
                "code": code,
            },
            status=status.HTTP_201_CREATED,
        )


class GoogleLoginAPIView(APIView):

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {"code": {"type": "string"}},
                "required": ["code"],
            }
        },
        responses={200: dict},
    )
    def post(self, request):
        code = request.data.get("code")

        if not code:
            return Response(
                {"error": "Google code is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        google_tokens = get_google_tokens(code)

        access_token = google_tokens.get("access_token")

        if not access_token:
            return Response(
                {"error": "Invalid Google code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        google_user = get_google_user(access_token)

        email = google_user.get("email")
        first_name = google_user.get("given_name", "")
        last_name = google_user.get("family_name", "")

        if not email:
            return Response(
                {"error": "Email not provided by Google"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "is_active": True,
                "registration_source": "google",
            },
        )

        user.is_active = True
        user.last_login = timezone.now()
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
