from rest_framework import serializers
from django.contrib.auth.models import User
from core import models


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Option
        fields = ['description', 'correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ['id', 'description', 'options']

    def create(self, validated_data):
        # Remover as opções de validated_data para criar a questão
        options_data = validated_data.pop('options')
        # Criar a instância de Question
        question = models.Question.objects.create(**validated_data)

        # Criar as opções associadas à questão
        for option_data in options_data:
            models.Option.objects.create(question=question, **option_data)

        return question


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
