from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TaskForm
from .models import Task, TaskRecipient
from .tasks import send_task_created_email

@login_required
def dashboard(request):
    qs = Task.objects.filter(owner=request.user).order_by('-priority', 'due_date')
    return render(request, 'taskboard/dashboard.html', {'tasks': qs})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            recipients = form.cleaned_data.pop('recipients', [])
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            # create recipient rows
            for email in recipients:
                TaskRecipient.objects.create(task=task, email=email)
            
            # trigger background job (same as API)
            from .tasks import send_task_created_email
            send_task_created_email.delay(task.id)
            messages.success(request, 'Task created and reminder scheduled.')
            return redirect('taskboard:dashboard')
    else:
        form = TaskForm()
    return render(request, 'taskboard/create_task.html', {'form': form})

@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            # Handle recipients update
            recipients_emails = form.cleaned_data.pop('recipients', [])
            
            # Save the task
            updated_task = form.save()
            
            # Update recipients
            updated_task.recipients.all().delete()  # Clear old recipients
            for email in recipients_emails:
                TaskRecipient.objects.create(task=updated_task, email=email)
            
            messages.success(request, 'Task updated successfully!')
            return redirect('taskboard:task_detail', pk=pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        # Pre-fill recipients in the form
        recipients_str = ', '.join([r.email for r in task.recipients.all()])
        form = TaskForm(instance=task, initial={'recipients': recipients_str})
    
    # GET: show full edit form
    return render(request, 'taskboard/update_task.html', {'task': task, 'form': form})


@login_required
def delete_task_if_done(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if task.status != Task.STATUS_DONE:
        messages.error(request, 'Task can only be deleted after it is marked done.')
        return redirect('taskboard:task_detail', pk=pk)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('taskboard:dashboard')

    # GET: show confirmation page
    return render(request, 'taskboard/confirm_delete.html', {'task': task})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, 'taskboard/task_detail.html', {'task': task})