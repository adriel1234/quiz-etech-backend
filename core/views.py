from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError, NotFound
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
from .serializers import UserSerializer



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

@api_view(['POST'])
@permission_classes([AllowAny])
def create_match_user(request):
    data = request.data

    # Verificar se os dados essenciais foram enviados
    if not data.get('userName') and not data.get('userId'):
        raise ValidationError('Nome de usuário ou ID de usuário é obrigatório')

    if not data.get('match') or not data['match'].get('id'):
        raise ValidationError('Match ID é obrigatório')

    # Tentando obter o usrName ou userId
    user_name = data.get('userName')
    user_id = data.get('userId')

    # Criar ou recuperar o usuário baseado no nome
    if user_name:
        user, created = User.objects.get_or_create(username=user_name)
        if created:
            user.set_unusable_password()  # Define a senha como inutilizável
            user.save()
    elif user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Nome de usuário ou ID de usuário é obrigatório'}, status=400)

    # Verificar se o matchId foi fornecido
    match_id = data.get('match', {}).get('id')
    if not match_id:
        return JsonResponse({'error': 'Match ID é obrigatório'}, status=400)

    try:
        # Buscar o match a partir do ID
        match = Match.objects.get(id=match_id)

        # Criar o MatchUser
        match_user = MatchUser.objects.create(
            user=user,
            match=match,
            points=data.get('points', 0),
            right_questions=data.get('rightQuestions', 0),
            wrong_questions=data.get('wrongQuestions', 0)
        )

        # Retorna os dados no formato desejado
        response_data = {
            'id': match_user.id,
            'modified_at': match_user.modified_at.isoformat(),  # Formato ISO para 'modified_at'
            'points': match_user.points,
            'right_questions': match_user.right_questions,
            'wrong_questions': match_user.wrong_questions,
            'user': match_user.user.id,  # ID do usuário
            'match': match_user.match.id,  # ID do match
        }

        return JsonResponse(response_data, status=201)

    except Match.DoesNotExist:
        return JsonResponse({'error': 'Match não encontrado'}, status=404)

def quiz_player(request, match_id):
    # Obtém o objeto Match pelo ID
    match = get_object_or_404(MatchUser, id=match_id)

    # Define o dicionário com os dados no formato desejado
    match_data = {
        "id": match.id,
        "modified_at": match.modified_at.isoformat(),  # Data formatada no padrão ISO
        "points": match.points,  # Pontuação inicial
        "right_questions": match.right_questions,  # Perguntas corretas inicial
        "wrong_questions": match.wrong_questions,  # Perguntas erradas inicial
        "user": match.user.id,  # ID do usuário autenticado
        "match": match.id  # ID do match
    }

    # Retorna o dicionário formatado como JSON
    return JsonResponse(match_data, safe=False)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_quiz_with_match_user(request, quiz_id, match_user_id):
    # Buscar o Quiz pelo ID
    quiz = get_object_or_404(Match, id=quiz_id)

    # Buscar o MatchUser pelo ID
    match_user = get_object_or_404(MatchUser, id=match_user_id)

    # Preparar os dados para o retorno
    response = {
        'quiz': {
            'id': quiz.id,
            'title': quiz.description,
            'questions': [
                {
                    'id': question.id,
                    'description': question.description,
                    'options': [
                        {'description': option.description, 'correct': option.correct}
                        for option in question.options.all()
                    ]  # Opções associadas à pergunta
                }
                for question in quiz.question_group.questions_group_question.all()
            ]
        },
        'matchUser': {
            'id': match_user.id,
            'user': match_user.user.username,
            'points': match_user.points,
            'right_questions': match_user.right_questions,
            'wrong_questions': match_user.wrong_questions,
        }
    }

    return JsonResponse(response, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_by_id(request, user_id):
    """
    Retorna o usuário baseado no userId.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound('Usuário não encontrado.')

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)