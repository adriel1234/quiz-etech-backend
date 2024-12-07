from rest_framework import viewsets, permissions
from django.contrib.auth.models import User

from core import models, serializers, filters


class QuestionViewSet(viewsets.ModelViewSet):
    """Gerencia operações CRUD para perguntas."""
    queryset = models.Question.objects.prefetch_related('options').all().order_by('id')
    serializer_class = serializers.QuestionSerializer
    filterset_class = filters.QuestionFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Permite leitura pública


class OptionViewSet(viewsets.ModelViewSet):
    """Gerencia opções de respostas."""
    queryset = models.Option.objects.all()
    serializer_class = serializers.OptionSerializer
    filterset_class = filters.OptionFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Permite leitura pública


class QuestionGroupViewSet(viewsets.ModelViewSet):
    """Gerencia grupos de perguntas."""
    queryset = models.QuestionGroup.objects.prefetch_related('questions_group_question').all().order_by('id')
    serializer_class = serializers.QuestionGroupSerializer
    filterset_class = filters.QuestionGroupFilter
    permission_classes = [permissions.IsAuthenticated]


class MatchViewSet(viewsets.ModelViewSet):
    """Gerencia partidas."""
    queryset = models.Match.objects.select_related('question_group').all()
    serializer_class = serializers.MatchSerializer
    filterset_class = filters.MatchFilter
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Personaliza a criação de partidas."""
        serializer.save(created_at=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Fornece somente leitura para usuários."""
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_class = filters.UserFilter
    permission_classes = [permissions.IsAdminUser]  # Apenas administradores podem acessar


class MatchUserViewSet(viewsets.ModelViewSet):
    """Gerencia os jogadores em partidas."""
    queryset = models.MatchUser.objects.select_related('user', 'match').all()
    serializer_class = serializers.MatchUserSerializer
    filterset_class = filters.MatchUserFilter
    permission_classes = [permissions.IsAuthenticated]