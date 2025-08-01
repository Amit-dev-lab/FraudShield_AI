from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('manual-check/', views.manual_check, name='manual_check'),
    path('api-key/', views.api_key_view, name='api_key'),
    path('history/', views.transaction_history, name='history'),
]
