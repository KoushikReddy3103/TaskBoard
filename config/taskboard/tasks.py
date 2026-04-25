from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Task
from django.template.loader import render_to_string

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_task_created_email(self, task_id):
    try:
        task = Task.objects.select_related('owner').get(pk=task_id)
    except Task.DoesNotExist:
        return 'task not found'
    

    subject = f"Task created: {task.title}"
    message = render_to_string('taskboard/email/task_created.txt', {'task': task})
    recipient = [task.owner.email] if task.owner.email else []
    if not recipient:
        return 'no recipient'


    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient)
    return 'sent'