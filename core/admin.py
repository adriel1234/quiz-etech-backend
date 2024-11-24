from django.contrib import admin
from core import models


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'created_at', 'modified_at')
    search_fields = ('description',)
    list_filter = ('created_at',)


@admin.register(models.Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'correct', 'question', 'created_at')
    search_fields = ('description', 'question__description')
    list_filter = ('correct', 'created_at')


@admin.register(models.QuestionGroup)
class QuestionGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'created_at', 'modified_at')
    search_fields = ('description',)
    list_filter = ('created_at',)


@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'time_per_question', 'question_group', 'created_at')
    search_fields = ('description', 'question_group__description')
    list_filter = ('created_at',)


@admin.register(models.MatchUser)
class MatchUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'match', 'points', 'right_questions', 'wrong_questions', 'created_at')
    search_fields = ('user__username', 'match__description')
    list_filter = ('created_at',)
