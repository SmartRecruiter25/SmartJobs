from django.urls import path
from . import views

urlpatterns = [
    path('', views.jobs, name="jobs"),  
    path('job/<str:pk>/', views.job, name="job"),  
    path('create-job/', views.createJob, name="create-job"),  
    path('update-job/<str:pk>/', views.updateJob, name="update-job"),  
    path('delete-job/<str:pk>/', views.deleteJob, name="delete-job"), 
]