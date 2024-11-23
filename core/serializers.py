from rest_framework import serializers, request
from django.contrib.auth.models import User
from core import models
import logging

logger = logging.getLogger(__name__)


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Option
        fields = ['description', 'correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, write_only=True)

    class Meta:
        model = models.Question
        fields = ['id', 'description', 'options']

    def create(self, validated_data):
        # Registra os dados validados
        logger.info("Dados validados para criar o QuestionGroup: %s", validated_data)

        # Extrai os IDs das questões do campo 'questions_group_question'
        questions_data = validated_data.pop('questions_group_question')
        logger.info("IDs das perguntas a serem associadas ao grupo de questões: %s", questions_data)

        # Criando o grupo de questões (QuestionGroup)
        question_group = models.QuestionGroup.objects.create(**validated_data)

        # Associando as questões ao grupo
        question_group.questions_group_question.set(questions_data)  # Associação de várias questões

        # Log para confirmar a criação
        logger.info("Grupo de questões criado com sucesso com ID: %d", question_group.id)

        return question_group


class QuestionGroupSerializer(serializers.ModelSerializer):
    questions_group_question = serializers.PrimaryKeyRelatedField(queryset=models.Question.objects.all(), many=True)

    class Meta:
        model = models.QuestionGroup
        fields = ['id', 'description', 'questions_group_question']

    def create(self, validated_data):
        logger.info("Dados validados para criar o QuestionGroup: %s", validated_data)

        questions_data = validated_data.pop('questions_group_question')
        logger.info("IDs das perguntas a serem associadas: %s", questions_data)

        # Criando o grupo de perguntas
        question_group = models.QuestionGroup.objects.create(**validated_data)
        question_group.questions_group_question.set(questions_data)  # Associando as questões ao grupo

        logger.info("Grupo de questões criado com sucesso com ID: %d", question_group.id)
        return question_group

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
