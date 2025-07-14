
from django.shortcuts import get_object_or_404
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

from django.conf import settings
from .models import Profile





@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            return Response({
                'message': 'Registration successful',
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("🔥 Registration error:", str(e))
            return Response({'error': str(e)}, status=500)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDashboard(request):
    user = request.user
    return Response({'message': f'Welcome {user.username}'})



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

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def hello(request):
    return Response({"message": "Hello from Smart Recruiter!"})


