from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import MatchUser,Match


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

def ranking_by_match_api(request, match_id):
    # Verifica se o match existe
    match = get_object_or_404(Match, id=match_id)

    # Recupera os dados dos usuários para o match específico
    ranking_list = MatchUser.objects.filter(match=match).order_by('-points')

    # Cria uma lista de dicionários com os dados necessários
    ranking_data = []
    for match_user in ranking_list:
        ranking_data.append({
            'username': match_user.user.username,
            'points': match_user.points,
            'right_questions': match_user.right_questions,
            'wrong_questions': match_user.wrong_questions
        })

    # Retorna os dados em formato JSON
    return JsonResponse(ranking_data, safe=False)
