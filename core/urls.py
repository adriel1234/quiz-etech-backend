from rest_framework import routers
from core import viewsets

router = routers.DefaultRouter()

router.register('question', viewsets.QuestionViewSet)
router.register('option', viewsets.OptionViewSet)
router.register('question-group', viewsets.QuestionGroupViewSet)
router.register('match', viewsets.MatchViewSet)
router.register('user', viewsets.UserViewSet)
router.register('match-user', viewsets.MatchUserViewSet)

urlpatterns = router.urls
