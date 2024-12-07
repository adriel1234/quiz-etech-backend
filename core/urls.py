from rest_framework import routers
from core import viewsets

router = routers.DefaultRouter()

router.register('questions', viewsets.QuestionViewSet, basename='question')
router.register('options', viewsets.OptionViewSet, basename='option')
router.register('question-groups', viewsets.QuestionGroupViewSet, basename='question-group')
router.register('matches', viewsets.MatchViewSet, basename='match')
router.register('users', viewsets.UserViewSet, basename='user')
router.register('match-users', viewsets.MatchUserViewSet, basename='match-user')

urlpatterns = router.urls