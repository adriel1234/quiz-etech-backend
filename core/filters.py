from django_filters import rest_framework as filters
from core import models

# Filtro de pesquisa
LIKE = 'unaccent__icontains'
ICONTAINS = 'icontains'
EQUALS = 'exact'
STARTS_WITH = 'startswith'
GT = 'gt'
GTE = 'gte'
LT = 'lt'
LTE = 'lte'
IN = 'in'


class QuestionFilter(filters.FilterSet):
    description = filters.CharFilter(lookup_expr=LIKE)

    class Meta:
        model = models.Question
        fields = ['description']


class OptionFilter(filters.FilterSet):
    correct = filters.BooleanFilter()
    description = filters.CharFilter(lookup_expr=LIKE)
    question = filters.CharFilter(field_name='question__description', lookup_expr=LIKE)

    class Meta:
        model = models.Option
        fields = ['correct', 'description', 'question']


class QuestionGroupFilter(filters.FilterSet):
    description = filters.CharFilter(lookup_expr=LIKE)

    class Meta:
        model = models.QuestionGroup
        fields = ['description']


class MatchFilter(filters.FilterSet):
    description = filters.CharFilter(lookup_expr=LIKE)
    question_group = filters.CharFilter(field_name='question_group__description', lookup_expr=LIKE)
    time_per_question = filters.NumberFilter()

    class Meta:
        model = models.Match
        fields = ['description', 'question_group', 'time_per_question']


class UserFilter(filters.FilterSet):
    login = filters.CharFilter(lookup_expr=LIKE)
    email = filters.CharFilter(lookup_expr=LIKE)

    class Meta:
        model = models.User
        fields = ['login', 'email']


class MatchUserFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='user__login', lookup_expr=LIKE)
    match = filters.CharFilter(field_name='match__description', lookup_expr=LIKE)
    points = filters.CharFilter(field_name='points', lookup_expr=GTE)
    right_questions = filters.CharFilter(field_name='right_questions', lookup_expr=GTE)
    wrong_questions = filters.CharFilter(field_name='wrong_questions', lookup_expr=GTE)

    class Meta:
        model = models.MatchUser
        fields = ['user', 'match', 'points', 'right_questions', 'wrong_questions']
