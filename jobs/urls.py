from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobViewSet, TagViewSet, JobApplicationViewSet,
    ApplicationReviewViewSet, SkillChallengeViewSet,
    ChallengeResultViewSet, MatchScoreViewSet
)

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='jobs')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'applications', JobApplicationViewSet, basename='applications')
router.register(r'application-reviews', ApplicationReviewViewSet, basename='application-reviews')
router.register(r'skill-challenges', SkillChallengeViewSet, basename='skill-challenges')
router.register(r'challenge-results', ChallengeResultViewSet, basename='challenge-results')
router.register(r'match-scores', MatchScoreViewSet, basename='match-scores')

urlpatterns = [
    path('', include(router.urls)),
]