from rest_framework import serializers
from django.contrib.auth.models import User
from core import models


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        exclude = ['created_at']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Option
        exclude = ['created_at']


class QuestionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionGroup
        exclude = ['created_at']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Match
        exclude = ['created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}


class MatchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MatchUser
        exclude = ['created_at']
