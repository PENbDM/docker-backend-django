from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from .serialziers import RegisterSerializer, UserSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response(
            {
                "user": UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )

        response.set_cookie(
            key="access",
            value=str(access),
            httponly=True,
            secure=False,      # True in production
            samesite="Lax",
        )

        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=False,      # True in production
            samesite="Lax",
        )

        return response

class LoginView(APIView):
    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(
            email=email,
            password=password
        )

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response(
            {
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access",
            value=str(access),
            httponly=True,
            secure=False,       # True in production (HTTPS)
            samesite="Lax",
        )

        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=False,       # True in production
            samesite="Lax",
        )

        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            UserSerializer(request.user).data
        )


class LogoutView(APIView):

    def post(self, request):

        response = Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )

        response.delete_cookie("access")
        response.delete_cookie("refresh")

        return response