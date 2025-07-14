from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 

from .models import (
    Job, Tag, JobApplication, ApplicationReview,
    SkillChallenge, ChallengeResult, MatchScore
)
from .forms import JobForm

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError

from .serializers import (
    JobSerializer, JobCreateUpdateSerializer, TagSerializer,
    JobApplicationSerializer, JobApplicationCreateUpdateSerializer,  
    ApplicationReviewSerializer,ApplicationReviewCreateUpdateSerializer,
     SkillChallengeSerializer, ChallengeResultSerializer, MatchScoreSerializer
)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-created')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'location']

    filterset_fields = ['location', 'job_type', 'tags', 'skills_required', 'status']

    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return JobCreateUpdateSerializer
        return JobSerializer

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.profile)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_jobs(self, request):
        profile = request.user.profile
        jobs = Job.objects.filter(employer=profile).order_by('-created')
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)





class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all().order_by('-created')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return JobApplicationCreateUpdateSerializer
        return JobApplicationSerializer

    def perform_create(self, serializer):
        profile = self.request.user.profile
        job = serializer.validated_data['job']

        
        if JobApplication.objects.filter(applicant=profile, job=job).exists():
            raise ValidationError("You have already applied for this job.")

        serializer.save(applicant=profile)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "Job application submitted successfully 🎉",
            "application": response.data
        }
        return response

    @action(detail=False, methods=['get'], url_path='for-job/(?P<job_id>[0-9a-f-]+)', permission_classes=[IsAuthenticated])
    def applications_for_job(self, request, job_id=None):
        user_profile = request.user.profile
        job = get_object_or_404(Job, id=job_id, employer=user_profile)

        applications = JobApplication.objects.filter(job=job).order_by('-created')
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my-applications', permission_classes=[IsAuthenticated])
    def my_applications(self, request):
        profile = request.user.profile
        applications = JobApplication.objects.filter(applicant=profile).order_by('-created')
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)



class ApplicationReviewViewSet(viewsets.ModelViewSet):
    queryset = ApplicationReview.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ApplicationReviewCreateUpdateSerializer
        return ApplicationReviewSerializer

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user.profile)




class SkillChallengeViewSet(viewsets.ModelViewSet):
    queryset = SkillChallenge.objects.all()
    serializer_class = SkillChallengeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ChallengeResultViewSet(viewsets.ModelViewSet):
    queryset = ChallengeResult.objects.all()
    serializer_class = ChallengeResultSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MatchScoreViewSet(viewsets.ModelViewSet):
    queryset = MatchScore.objects.all()
    serializer_class = MatchScoreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]