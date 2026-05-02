from django.urls import path
from . import views_auth

app_name = 'taskboard_auth'

urlpatterns = [
    path('login/', views_auth.login_view, name='login'),
    path('logout/', views_auth.logout_view, name='logout'),
]