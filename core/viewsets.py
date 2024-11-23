from rest_framework import viewsets, permissions, status
from django.contrib.auth.models import User
from rest_framework.response import Response

from core import models, serializers, filters
import logging

logger = logging.getLogger(__name__)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    filterset_class = filters.QuestionFilter
    permission_classes = [permissions.IsAuthenticated]


class OptionViewSet(viewsets.ModelViewSet):
    queryset = models.Option.objects.all()
    serializer_class = serializers.OptionSerializer
    filterset_class = filters.OptionFilter
    permission_classes = [permissions.IsAuthenticated]



class QuestionGroupViewSet(viewsets.ModelViewSet):
    queryset = models.QuestionGroup.objects.all()
    serializer_class = serializers.QuestionGroupSerializer
    filterset_class = filters.QuestionGroupFilter
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        logger.info("Dados recebidos para criar o grupo de questões: %s", request.data)

        # Verificando se a chave 'questionsGroupQuestion' está presente nos dados da requisição
        if 'questionsGroupQuestion' not in request.data:
            logger.error("Faltando 'questionsGroupQuestion' nos dados recebidos.")
            return Response({"detail": "'questionsGroupQuestion' is required."}, status=status.HTTP_400_BAD_REQUEST)

        questions_data = request.data['questionsGroupQuestion']
        logger.info("IDs das perguntas recebidas: %s", questions_data)

        # Verificando se todos os IDs de perguntas são válidos
        invalid_questions = [q_id for q_id in questions_data if not models.Question.objects.filter(id=q_id).exists()]
        if invalid_questions:
            logger.error("IDs de perguntas inválidos: %s", invalid_questions)
            return Response({"detail": "Some question IDs are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Criando o grupo de questões
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                question_group = serializer.save()
                logger.info("Grupo de questões criado com sucesso com ID: %d", question_group.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error("Erro na validação do serializer: %s", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Erro ao criar grupo de questões: %s", str(e))
            return Response({"detail": "Erro ao criar grupo de questões."}, status=status.HTTP_400_BAD_REQUEST)

class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer
    filterset_class = filters.MatchFilter
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_class = filters.UserFilter
    permission_classes = [permissions.IsAuthenticated]


class MatchUserViewSet(viewsets.ModelViewSet):
    queryset = models.MatchUser.objects.all()
    serializer_class = serializers.MatchUserSerializer
    filterset_class = filters.MatchUserFilter
    permission_classes = [permissions.IsAuthenticated]
