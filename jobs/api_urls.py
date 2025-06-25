# jobs/api_urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    JobViewSet, TagViewSet, JobApplicationViewSet,
    ApplicationReviewViewSet, SkillChallengeViewSet,
    ChallengeResultViewSet, MatchScoreViewSet
)

router = DefaultRouter()
router.register('jobs', JobViewSet)
router.register('tags', TagViewSet)
router.register('applications', JobApplicationViewSet)
router.register('reviews', ApplicationReviewViewSet)
router.register('challenges', SkillChallengeViewSet)
router.register('challenge-results', ChallengeResultViewSet)
router.register('match-scores', MatchScoreViewSet)

urlpatterns = router.urls