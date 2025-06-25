from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png"
    )

    skills = models.ManyToManyField('Skill', through='ProfileSkill', blank=True)

    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)

    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    preferred_job_type = models.CharField(max_length=100, blank=True, null=True)

    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)

    certified = models.BooleanField(default=False)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    years_of_training = models.IntegerField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)


class Skill(models.Model):
   
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class ProfileSkill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert')
    ])
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.profile.username} - {self.skill.name} ({self.level})"


class SkillProof(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skill_proofs')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    file = models.FileField(upload_to='skill_proofs/', null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.profile.username} - {self.skill.name}"