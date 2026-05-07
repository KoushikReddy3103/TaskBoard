from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('taskboard:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next') or reverse('taskboard:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm(request)
    
    return render(request, 'taskboard/registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    logger.info(HttpResponse("Logged out successfully", status=200))
    
    return redirect('taskboard_auth:login')