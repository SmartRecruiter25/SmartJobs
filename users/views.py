
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
import google.generativeai as genai
from django.conf import settings
from .models import Profile





@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
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


genai.configure(api_key="AIzaSyCOpqFafFAR0FLT8OuFjuGgbpFoK1conZk")

class GenerateCVGeminiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # ← مهم لحفظ الـ CV

        data = request.data
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone", "")
        skills = data.get("skills", [])
        experience = data.get("experience", "")

        prompt = f"""
Generate a professional CV based on:
Name: {name}
Email: {email}          
Phone: {phone}
Skills: {', '.join(skills)}
Experience: {experience}

Make it clean, professional and formatted in sections.
        """

        try:
            model = genai.GenerativeModel(model_name="gemini-pro")
            response = model.generate_content(prompt)
            cv_text = response.text

            # تخزين الـ CV في ملف المستخدم
            profile = Profile.objects.get(user=user)
            profile.cv_text = cv_text
            profile.save()

            return Response({"cv_text": cv_text}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetMyCV(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return Response({"cv_text": profile.cv_text}, status=status.HTTP_200_OK)