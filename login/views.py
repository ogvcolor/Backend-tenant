# from django.contrib.auth import get_user_model, login, logout
# from rest_framework.authentication import SessionAuthentication
# from rest_framework.views import APIView
from django.contrib.auth import login
from django.utils import timezone
from knox import views as knox_views
from knox.models import AuthToken
from knox.settings import knox_settings
from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# from .validations import custom_validation, validate_email, validate_password
# from rest_framework.decorators import api_view
from .models import CustomUser
from .serializers import CreateUserSerializer, LoginSerializer, UpdateUserSerializer

# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from django.utils.translation import gettext as __
# from knox.auth import AuthToken
# from django.contrib.auth.models import User


def serialize_user_data(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_superuser": user.is_superuser,
    }


class CreateUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)


class UpdateUserAPI(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer
    authentication_classes = (TokenAuthentication,)


class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    authentication_classes = (TokenAuthentication,)

    def get_token_limit_per_user(self):
        return knox_settings.TOKEN_LIMIT_PER_USER

    def post(self, request, format=None):
        token_limit_per_user = self.get_token_limit_per_user()
        print("")
        print("")
        print("")
        print("request", request)
        print("request", request.data)
        print("")
        print("")
        print("")
        print("")

        if token_limit_per_user is not None:
            now = timezone.now()

            # Obtenha o usuário do banco de dados usando o e-mail
            user = CustomUser.objects.filter(email=request.data["email"]).first()

            if not user:
                return Response(
                    {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
                )

            active_tokens = AuthToken.objects.filter(user=user, expiry__gt=now)
            if active_tokens.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        print("respons.data", response.data)
        return Response(
            {"data": response.data, "user_data": serialize_user_data(user)},
            status=status.HTTP_200_OK,
        )
