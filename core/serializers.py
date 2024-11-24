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

    def update(self, instance, validated_data):
        # Atualizar os dados da questão
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Atualizar as opções
        options_data = validated_data.pop('options', [])
        existing_options = {opt.id: opt for opt in instance.options.all()}

        for option_data in options_data:
            option_id = option_data.get('id')
            if option_id and option_id in existing_options:
                # Atualizar uma opção existente
                option = existing_options.pop(option_id)
                option.description = option_data.get('description', option.description)
                option.correct = option_data.get('correct', option.correct)
                option.save()
            else:
                # Criar uma nova opção
                models.Option.objects.create(question=instance, **option_data)

        # Excluir opções que não estão na requisição
        for option in existing_options.values():
            option.delete()

        return instance


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
