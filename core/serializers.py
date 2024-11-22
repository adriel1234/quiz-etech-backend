from rest_framework import serializers
from django.contrib.auth.models import User
from core import models


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
        options_data = validated_data.pop('options')
        question = models.Question.objects.create(**validated_data)
        for option_data in options_data:
            models.Option.objects.create(question=question, **option_data)
        return question


class QuestionGroupSerializer(serializers.ModelSerializer):
    questions_group_question = serializers.PrimaryKeyRelatedField(queryset=models.Question.objects.all(), many=True)

    class Meta:
        model = models.QuestionGroup
        exclude = ['created_at']

    def create(self, validated_data):

        questions_data = validated_data.pop('questions_group_question')

        question_group = models.QuestionGroup.objects.create(**validated_data)

        question_group.questions_group_question.set(questions_data)

        return question_group

    def update(self, instance, validated_data):

        questions_data = validated_data.pop('questions_group_question', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if questions_data is not None:
            instance.questions_group_question.set(questions_data)

        return instance


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
