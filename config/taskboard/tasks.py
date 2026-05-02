from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Task
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_task_created_email(self, task_id):
    try:
        task = Task.objects.select_related('owner').get(pk=task_id)
    except Task.DoesNotExist:
        logger.warning("send_task_created_email: Task %s not found", task_id)
        return 'task not found'
    
    recipient_email = task.owner.email
    if not recipient_email:
        logger.info("send_task_created_email: Owner has no email for task %s", task_id)
        return 'no recipient'
    
    subject = f"Task created: {task.title}"
    context = {'task': task, 'site_name': getattr(settings, 'SITE_NAME', 'TaskBoard')}
    text_body = render_to_string('taskboard/email/task_created.txt', context)
    html_body = render_to_string('taskboard/email/task_created.html', context)
    
    try:
        msg = EmailMultiAlternatives(subject=subject,
                                     body=text_body,
                                     from_email=settings.DEFAULT_FROM_EMAIL,
                                    to=[recipient_email])
        # attach HTML alternative if template exists
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
        logger.info("send_task_created_email: Sent task %s to %s", task_id, recipient_email)
        return 'sent'
    except Exception as exc:
        logger.exception("send_task_created_email: error sending email for task %s", task_id)
        try:
            # retry with exponential backoff via Celery retry
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            logger.error("send_task_created_email: max retries exceeded for task %s", task_id)
            return 'failed'