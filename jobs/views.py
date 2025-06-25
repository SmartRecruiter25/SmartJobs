from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import (
    Job, Tag, JobApplication, ApplicationReview,
    SkillChallenge, ChallengeResult, MatchScore
)
from .forms import JobForm

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import (
    JobSerializer, JobCreateUpdateSerializer, TagSerializer,
    JobApplicationSerializer, ApplicationReviewSerializer,
    SkillChallengeSerializer, ChallengeResultSerializer,
    MatchScoreSerializer
)


def jobs(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/jobs.html', {'jobs': jobs})


def job(request, pk):
    job = get_object_or_404(Job, id=pk)
    return render(request, 'jobs/single-job.html', {'job': job})


@login_required(login_url="login")
def createJob(request):
    profile = request.user.profile
    if profile.role != 'employer':
        return redirect('jobs')

    form = JobForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        job = form.save(commit=False)
        job.employer = profile
        job.save()
        form.save_m2m()
        return redirect('account')

    return render(request, "jobs/job_form.html", {'form': form})


@login_required(login_url="login")
def updateJob(request, pk):
    profile = request.user.profile
    if profile.role != 'employer':
        return redirect('jobs')

    job = get_object_or_404(Job, id=pk, employer=profile)
    form = JobForm(request.POST or None, request.FILES or None, instance=job)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('account')

    return render(request, "jobs/job_form.html", {'form': form})


@login_required(login_url="login")
def deleteJob(request, pk):
    profile = request.user.profile
    if profile.role != 'employer':
        return redirect('jobs')

    job = get_object_or_404(Job, id=pk, employer=profile)
    if request.method == 'POST':
        job.delete()
        return redirect('jobs')

    return render(request, 'jobs/delete_template.html', {'object': job})


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-created')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return JobCreateUpdateSerializer
        return JobSerializer

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.profile)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all().order_by('-created')
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ApplicationReviewViewSet(viewsets.ModelViewSet):
    queryset = ApplicationReview.objects.all()
    serializer_class = ApplicationReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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