from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
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
        # Receber o nome do usuário no corpo da requisição
        user_name = request.POST.get('name')

        if not user_name:
            return JsonResponse({"error": "Nome é obrigatório"}, status=400)

        # Obter o match associado ao match_id
        match = get_object_or_404(Match, id=match_id)

        # Criar o novo usuário no Django sem senha
        user = User.objects.create_user(username=user_name, password=None)

        # Associar o usuário ao match, se necessário. Aqui você pode adicionar um relacionamento, como um campo ManyToMany.
        # Exemplo, se o relacionamento entre Match e User for necessário:
        # match.users.add(user)  # Caso tenha um campo ManyToMany chamado 'users' no modelo 'Match'

        # Caso não seja necessário associar diretamente, apenas gravar o match_id:
        user.profile.match = match  # Supondo que 'profile' seja um modelo relacionado ao User
        user.profile.save()

        # Retornar a resposta com dados do novo usuário
        return JsonResponse({
            "user": {
                "id": user.id,
                "username": user.username,
                "match_id": match.id
            }
        })
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)