from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Skill, ProfileSkill, SkillProof
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'created']


class ProfileSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        source='skill', queryset=Skill.objects.all(), write_only=True
    )

    class Meta:
        model = ProfileSkill
        fields = ['id', 'skill', 'skill_id', 'level', 'created']


class SkillProofSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        source='skill', queryset=Skill.objects.all(), write_only=True
    )

    class Meta:
        model = SkillProof
        fields = ['id', 'skill', 'skill_id', 'file', 'link', 'description', 'created']


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    skills = ProfileSkillSerializer(many=True, read_only=True)
    skill_proofs = SkillProofSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'role', 'name', 'location', 'short_intro', 'bio',
            'profile_image', 'cv', 'preferred_job_type',
            'company_name', 'company_website', 'company_description',
            'certified', 'specialization', 'years_of_training',
            'is_active', 'skills', 'skill_proofs',
            'username', 'email'
        ]


class MiniProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role')
        email = validated_data['email'].lower()
        user = User.objects.create_user(
            username=validated_data['username'],
            email=email,
            password=validated_data['password']
        )
        Profile.objects.create(user=user, role=role)
        return user
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
         raise serializers.ValidationError("This username is already taken.")
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.profile.role
        token['username'] = user.username
        return token