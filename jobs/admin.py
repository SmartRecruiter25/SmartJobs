from django.contrib import admin
from .models import Job, Tag, JobApplication, ApplicationReview, SkillChallenge, ChallengeResult, MatchScore

admin.site.register(Job)
admin.site.register(Tag)
admin.site.register(JobApplication)
admin.site.register(ApplicationReview)
admin.site.register(SkillChallenge)
admin.site.register(ChallengeResult)
admin.site.register(MatchScore)

