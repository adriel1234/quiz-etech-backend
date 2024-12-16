from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from core import models, serializers, filters

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.prefetch_related('options').all().order_by('id')
    serializer_class = serializers.QuestionSerializer
    filterset_class = filters.QuestionFilter
    # permission_classes = [AllowAny]
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # Permitir acesso irrestrito (AllowAny) para métodos de leitura (GET, HEAD, OPTIONS)
        if self.action in ['retrieve', 'list']:
            permission_classes = [AllowAny]
        else:
            # Exigir autenticação para outras ações (POST, PUT, DELETE, etc.)
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class OptionViewSet(viewsets.ModelViewSet):
    queryset = models.Option.objects.all()
    serializer_class = serializers.OptionSerializer
    filterset_class = filters.OptionFilter
    permission_classes = [permissions.IsAuthenticated]



class QuestionGroupViewSet(viewsets.ModelViewSet):
    queryset = models.QuestionGroup.objects.all().order_by('id')
    serializer_class = serializers.QuestionGroupSerializer
    filterset_class = filters.QuestionGroupFilter
    permission_classes = [permissions.IsAuthenticated]


class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer
    filterset_class = filters.MatchFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]  # Allow GET requests for all users
        else:
            permission_classes = [permissions.IsAuthenticated]  # Other actions require authentication
        return [permission() for permission in permission_classes]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_class = filters.UserFilter
    permission_classes = [permissions.IsAuthenticated]




class AllowPUTPATCHOnly(BasePermission):
    def has_permission(self, request, view):
        # Permite PUT e PATCH para qualquer um
        if request.method in ['PUT', 'PATCH']:
            return True
        # Restringe outros métodos
        return False

class MatchUserViewSet(viewsets.ModelViewSet):
    queryset = models.MatchUser.objects.all()
    serializer_class = serializers.MatchUserSerializer
    filterset_class = filters.MatchUserFilter
    permission_classes = [AllowPUTPATCHOnly]