from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken


class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)

            # Check token validity
            is_token_valid = self.check_token_validity(str(refresh.access_token), user)
            if is_token_valid:
                return Response(
                    {   
                        "user_id": user.id,
                        "message": "Login successful",
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Token is invalid or expired"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def check_token_validity(self, token, user):
        user = default_token_generator.check_token(user, token)
        if user is not None:
            # Token is valid
            return True
        else:
            # Token is invalid or expired
            return False

    @action(detail=False, methods=["post"])
    def logout(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def register(self, request):
        if User.objects.filter(username=request.data["username"]).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=request.data["username"],
            password=request.data["password"],
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            email=request.data["email"],
        )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Registration successful",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )
