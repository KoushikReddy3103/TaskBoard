from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TaskForm
from .models import Task


@login_required
def dashboard(request):
    qs = Task.objects.filter(owner=request.user).order_by('-priority', 'due_date')
    return render(request, 'taskboard/dashboard.html', {'tasks': qs})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            # trigger background job (same as API)
            from .tasks import send_task_created_email
            send_task_created_email.delay(task.id)
            messages.success(request, 'Task created and reminder scheduled.')
            return redirect('taskboard:dashboard')
    else:
        form = TaskForm()
    return render(request, 'taskboard/create_task.html', {'form': form})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, 'taskboard/task_detail.html', {'task': task})