from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permite acesso sem autenticação

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        if User.objects.filter(username=email).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({"token": str(refresh.access_token), "name": user.first_name}, status=status.HTTP_201_CREATED)