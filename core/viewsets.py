from rest_framework import viewsets, permissions
from django.contrib.auth.models import User

from core import models, serializers, filters

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.prefetch_related('options').all().order_by('id')
    serializer_class = serializers.QuestionSerializer
    filterset_class = filters.QuestionFilter
    permission_classes = [permissions.IsAuthenticated]


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


class MatchUserViewSet(viewsets.ModelViewSet):
    queryset = models.MatchUser.objects.all()
    serializer_class = serializers.MatchUserSerializer
    filterset_class = filters.MatchUserFilter
    permission_classes = [permissions.IsAuthenticated]
