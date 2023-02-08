from django.urls import path

from core import views

urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup-view'),
    path('login', views.LoginView.as_view(), name='login-view'),
    path('profile', views.ProfileView.as_view(), name='profile-view'),
]
