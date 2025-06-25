from rest_framework import serializers
from .models import (
    Job, Tag, JobApplication, ApplicationReview,
    SkillChallenge, ChallengeResult, MatchScore
)
from users.models import Skill, Profile
from users.serializers import SkillSerializer, ProfileSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created']


class JobSerializer(serializers.ModelSerializer):
    employer = ProfileSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    skills_required = SkillSerializer(many=True, read_only=True)
    application_count = serializers.ReadOnlyField()
    class Meta:
        model = Job
        fields = ['id', 'employer', 'title', 'description', 'featured_image', 'tags',
            'salary_range', 'job_type', 'location', 'experience_required',
            'deadline', 'skills_required', 'status', 'created', 'application_count']


class JobCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    skills_required = serializers.PrimaryKeyRelatedField(many=True, queryset=SkillSerializer.Meta.model.objects.all(), required=False)
    class Meta:
        model = Job
        fields = [
            'id', 'employer', 'title', 'description', 'featured_image', 'tags',
            'salary_range', 'job_type', 'location', 'experience_required',
            'deadline', 'skills_required', 'status'
        ]


class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = ProfileSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    class Meta:
        model = JobApplication
        fields = [
            'id', 'applicant', 'job', 'resume', 'cover_letter',
            'cv_text', 'match_score', 'status', 'created'
        ]


class JobApplicationCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            'id', 'applicant', 'job', 'resume', 'cover_letter',
            'cv_text', 'match_score', 'status'
        ]


class ApplicationReviewSerializer(serializers.ModelSerializer):
    reviewer = ProfileSerializer(read_only=True)
    application = JobApplicationSerializer(read_only=True)
    class Meta:
        model = ApplicationReview
        fields = ['id', 'application', 'reviewer', 'value', 'comment', 'created']


class ApplicationReviewCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationReview
        fields = ['id', 'application', 'reviewer', 'value', 'comment']


class SkillChallengeSerializer(serializers.ModelSerializer):
    related_skills = SkillSerializer(many=True, read_only=True)
    job = JobSerializer(read_only=True)
    class Meta:
        model = SkillChallenge
        fields = ['id', 'title', 'description', 'related_skills', 'job', 'difficulty', 'created']


class SkillChallengeCreateUpdateSerializer(serializers.ModelSerializer):
    related_skills = serializers.PrimaryKeyRelatedField(many=True, queryset=SkillSerializer.Meta.model.objects.all(), required=False)
    class Meta:
        model = SkillChallenge
        fields = ['id', 'title', 'description', 'related_skills', 'job', 'difficulty']


class ChallengeResultSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    challenge = SkillChallengeSerializer(read_only=True)
    class Meta:
        model = ChallengeResult
        fields = ['id', 'user', 'challenge', 'score', 'completed_at']


class ChallengeResultCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeResult
        fields = ['id', 'user', 'challenge', 'score']


class MatchScoreSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    class Meta:
        model = MatchScore
        fields = ['id', 'profile', 'job', 'score', 'evaluated_at']

class MatchScoreCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchScore
        fields = ['id', 'profile', 'job', 'score']