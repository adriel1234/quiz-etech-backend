from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from core import models, serializers, filters


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    filterset_class = filters.QuestionFilter
    permission_classes = {permissions.IsAuthenticated}


class OptionViewSet(viewsets.ModelViewSet):
    queryset = models.Option.objects.all()
    serializer_class = serializers.OptionSerializer
    filterset_class = filters.OptionFilter
    permission_classes = {permissions.IsAuthenticated}


class QuestionGroupViewSet(viewsets.ModelViewSet):
    queryset = models.QuestionGroup.objects.all()
    serializer_class = serializers.QuestionGroupSerializer
    filterset_class = filters.QuestionGroupFilter
    permission_classes = {permissions.IsAuthenticated}


class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer
    filterset_class = filters.MatchFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_class = filters.UserFilter
    permission_classes = {permissions.IsAuthenticated}


class MatchUserViewSet(viewsets.ModelViewSet):
    queryset = models.MatchUser.objects.all()
    serializer_class = serializers.MatchUserSerializer
    filterset_class = filters.MatchUserFilter
    permission_classes = {permissions.IsAuthenticated}
