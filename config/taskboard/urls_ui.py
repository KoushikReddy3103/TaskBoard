from django.urls import path
from . import views_ui

app_name = 'taskboard'

urlpatterns = [
    path('', views_ui.dashboard, name='dashboard'),
    path('tasks/new/', views_ui.create_task, name='create_task'),
    path('tasks/<int:pk>/', views_ui.task_detail, name='task_detail'),
]