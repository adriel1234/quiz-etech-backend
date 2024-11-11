from django.db import models


class ModelBase(models.Model):
    id = models.BigIntegerField(db_column='id', primary_key=True)
    created_at = models.DateTimeField(db_column='dt_created_at', auto_now_add=True)
    modified_at = models.DateTimeField(db_column='dt_modified_at', auto_now=True)

    class Meta:
        abstract = True
        managed = True


class Question(ModelBase):
    description = models.CharField(db_column='tx_question', null=False, max_length=264)

    class Meta:
        db_table = 'question'
        managed = True


class Option(ModelBase):
    correct = models.BooleanField(db_column='tx_option_correct', null=False, default=False)
    description = models.CharField(db_column='tx_option_description', null=False, max_length=264)
    question = models.ForeignKey(Question, db_column='nb_id_question', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'option'
        managed = True


class QuestionGroup(ModelBase):
    description = models.CharField(db_column='tx_question_group', null=False, max_length=264)
    questions_group_question = models.ManyToManyField(Question, db_table='question_group_question')

    class Meta:
        db_table = 'question_group'
        managed = True


class Match(ModelBase):
    time_per_question = models.IntegerField(db_column='nb_time_per_question', null=False)  # TIME
    description = models.CharField(db_column='tx_description', null=False, max_length=264)
    question_group = models.ForeignKey(QuestionGroup, db_column='nb_id_question_group', null=False,
                                       on_delete=models.CASCADE)

    class Meta:
        db_table = 'match'
        managed = True


class User(ModelBase):
    login = models.CharField(db_column='tx_login', max_length=264, unique=True)
    password = models.CharField(db_column='nb_password', max_length=128)
    email = models.EmailField(db_column='tx_email', max_length=264, unique=True)

    class Meta:
        db_table = 'user'
        managed = True


class MatchUser(ModelBase):
    user = models.ForeignKey(User, db_column='nb_id_user', null=False, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, db_column='nb_id_match', null=False, on_delete=models.CASCADE)
    points = models.IntegerField(db_column='nb_points', default=0)
    right_questions = models.IntegerField(db_column='nb_right_questions', default=0)
    wrong_questions = models.IntegerField(db_column='nb_wrong_questions', default=0)

    class Meta:
        db_table = 'match_user'
        managed = True
