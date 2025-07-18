from django.urls import path
from . import views
from .views import loginUser, registerUser, userDashboard ,hello




urlpatterns = [
    
    
    path('login/', loginUser, name="login"),
    path('register/', registerUser, name="register"),
    path('dashboard/', userDashboard, name="dashboard"),
    
    
    path('hello/', hello, name='hello'),

    
    path('profiles/', views.ProfileListView.as_view(), name='api-profiles'),
    path('profiles/<uuid:id>/', views.ProfileDetailView.as_view(), name='api-profile-detail'),

    path('skills/', views.SkillListView.as_view(), name='api-skills'),
    path('skills/<uuid:pk>/', views.SkillDetailView.as_view(), name='api-skill-detail'),

    
    path('profile-skills/', views.ProfileSkillListCreateView.as_view(), name='api-profile-skills'),
    path('profile-skills/<uuid:pk>/', views.ProfileSkillDetailView.as_view(), name='api-profile-skill-detail'),

   
    path('skill-proofs/', views.SkillProofListCreateView.as_view(), name='api-skill-proofs'),
    path('skill-proofs/<uuid:pk>/', views.SkillProofDetailView.as_view(), name='api-skill-proof-detail'),

    

]