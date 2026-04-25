from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Task
from .serializers import TaskSerializer
from .tasks import send_task_created_email

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class SmallPagination(PageNumberPagination):
    page_size = 10

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = SmallPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['status', 'description' ,'title']
    ordering_fields = ['priority', 'due_date', 'created_at']
    
    
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        task = serializer.save(owner=self.request.user)
        # fire background email reminder
        send_task_created_email.delay(task.id)

