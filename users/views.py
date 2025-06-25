from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Profile, Skill, ProfileSkill, SkillProof
from .forms import ProfileForm, SkillForm
from .serializers import (
    ProfileSerializer,
    SkillSerializer,
    RegisterSerializer,
    MyTokenObtainPairSerializer,
    UserSerializer,
    ProfileSkillSerializer,
    SkillProofSerializer,
)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    data = request.data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not username or not email or not password or not role:
        return Response({'error': 'Please fill in all required fields'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, username=username, email=email, role=role)
        return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({'error': 'An error occurred during registration'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDashboard(request):
    user = request.user
    return Response({'message': f'Welcome {user.username}'})

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])
def loginUser(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({'message': 'Login successful', 'username': user.username})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

class SkillListView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

class ProfileSkillListCreateView(generics.ListCreateAPIView):
    queryset = ProfileSkill.objects.all()
    serializer_class = ProfileSkillSerializer
    permission_classes = [IsAuthenticated]

class ProfileSkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfileSkill.objects.all()
    serializer_class = ProfileSkillSerializer
    permission_classes = [IsAuthenticated]

class SkillProofListCreateView(generics.ListCreateAPIView):
    queryset = SkillProof.objects.all()
    serializer_class = SkillProofSerializer
    permission_classes = [IsAuthenticated]
class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    
class SkillProofDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SkillProof.objects.all()
    serializer_class = SkillProofSerializer
    permission_classes = [IsAuthenticated]




def logoutUser(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login')

def profiles(request):
    search_query = request.GET.get('search_query', '')
    profiles = Profile.objects.filter(name__icontains=search_query)
    return render(request, 'users/profiles.html', {'profiles': profiles})

def userProfile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    topSkills = profile.skills.exclude(description__exact="")
    otherSkills = profile.skills.filter(description="")

    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills,
    }
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    skills = profile.skills.all()

    context = {
        'profile': profile,
        'skills': skills,
    }
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('account')

    return render(request, 'users/profile_form.html', {'form': form})

@login_required(login_url='login')
def createSkill(request):
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            profile = request.user.profile
            ProfileSkill.objects.create(profile=profile, skill=skill)
            messages.success(request, 'Skill added successfully.')
            return redirect('account')

    return render(request, 'users/skill_form.html', {'form': form})

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = get_object_or_404(profile.skills, id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully.')
            return redirect('account')

    return render(request, 'users/skill_form.html', {'form': form})

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = get_object_or_404(profile.skills, id=pk)

    if request.method == 'POST':
        profile.skills.remove(skill)
        messages.success(request, 'Skill removed successfully.')
        return redirect('account')

    return render(request, 'delete_template.html', {'object': skill})