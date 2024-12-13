from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from .models import MatchUser, Match, QuestionGroup,Question


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


def quiz_player(request, match_id):
    # Obtém o objeto Match pelo ID
    match = get_object_or_404(Match, id=match_id)

    # Obtém o grupo de perguntas (GroupQuestion) associado ao match
    group_question = match.question_group

    # Obtém as perguntas associadas a esse grupo
    questions = group_question.questions_group_question.all()

    # Formata as perguntas em um formato de lista de dicionários
    questions_data = []
    for question in questions:
        questions_data.append({
            'id': question.id,
            'description': question.description,  # Exemplo de campo, você pode adicionar mais conforme necessário
        })

    # Cria um dicionário com os dados do match e as perguntas associadas
    match_data = {
        'id': match.id,
        'modified_at': match.modified_at.isoformat(),  # A data é convertida para string no formato ISO
        'time_per_question': match.time_per_question,
        'description': match.description,
        'question_group': match.question_group.id,  # Retorna o ID do grupo de perguntas
        'questions': questions_data  # Inclui as perguntas associadas ao match
    }

    # Retorna o dicionário formatado como JSON
    return JsonResponse(match_data, safe=False)

def quiz_result(request, match_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_name = data.get('name')
            code = data.get('code')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        if not user_name:
            return JsonResponse({"error": "Nome é obrigatório"}, status=400)

        # Get the match associated with the code (assuming 'code' corresponds to 'id')
        match = get_object_or_404(Match, id=code)

        # Create the user
        user = User.objects.create_user(username=user_name, password=None)

        # Save the user's match
        user.profile.match = match
        user.profile.save()

        return JsonResponse({
            "user": {
                "id": user.id,
                "username": user.username,
                "match_id": match.id
            }
        })
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)