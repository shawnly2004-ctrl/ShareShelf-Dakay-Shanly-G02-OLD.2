from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailLoginForm

urlpatterns = [
    path('', views.dashboard_redirect, name='home'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/member/', views.member_dashboard, name='member_dashboard'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
path('profile/edit/', views.profile_edit, name='profile_edit'),
  path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=EmailLoginForm,
        redirect_authenticated_user=True), name='login'),
]