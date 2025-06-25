from django.db import models
import uuid

class Job(models.Model):
    employer = models.ForeignKey(
        'users.Profile', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='jobs', limit_choices_to={'role': 'employer'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    tags = models.ManyToManyField('Tag', blank=True)
    
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(
        max_length=50,
        choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('remote', 'Remote')],
        null=True, blank=True
    )
    location = models.CharField(max_length=200, blank=True, null=True)
    experience_required = models.CharField(max_length=100, blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)
    skills_required = models.ManyToManyField('users.Skill', blank=True)

    JOB_STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=10, choices=JOB_STATUS_CHOICES, default='open')

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    @property
    def application_count(self):
        return self.applications.count()



class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name



class JobApplication(models.Model):
    applicant = models.ForeignKey(
        'users.Profile', on_delete=models.CASCADE, limit_choices_to={'role': 'job_seeker'}
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    cover_letter = models.TextField(null=True, blank=True)
    cv_text = models.TextField(null=True, blank=True)
    match_score = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20, default='pending', choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ]
    )
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"



class ApplicationReview(models.Model):
    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(
        'users.Profile', on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'employer'}
    )
    value = models.CharField(max_length=10, choices=[('up', 'Up Vote'), ('down', 'Down Vote')])
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.application} - {self.value}"


class SkillChallenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    related_skills = models.ManyToManyField('users.Skill', blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True, related_name='challenges')
    difficulty = models.CharField(
        max_length=50,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        null=True, blank=True
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class ChallengeResult(models.Model):
    user = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    challenge = models.ForeignKey(SkillChallenge, on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} - Score: {self.score}"



class MatchScore(models.Model):
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    score = models.FloatField()
    evaluated_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.profile.username} - {self.job.title} - {self.score}"