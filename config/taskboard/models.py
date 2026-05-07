from django.db import models
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class Task(models.Model):
    STATUS_TODO = 'ToDo'
    STATUS_DOING = 'Doing'
    STATUS_DONE = 'Done'
    STATUS_CHOICES = [
        (STATUS_TODO, 'ToDo'),
        (STATUS_DOING, 'Doing'),
        (STATUS_DONE, 'Done')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_TODO)
    priority = models.PositiveSmallIntegerField(default=3)
    due_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ['-priority', 'due_date', '-created_at']
    
    
    
    def __str__(self): return self.title

class TaskRecipient(models.Model):
    task = models.ForeignKey(Task, related_name='recipients', on_delete=models.CASCADE)
    email = models.EmailField()

    def clean(self):
        try:
            validate_email(self.email)
        except ValidationError:
            raise ValidationError({'email': 'Invalid email address'})
    
    def __str__(self):
        return f"{self.email} for {self.task_id}"