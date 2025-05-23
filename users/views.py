from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomLoginForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_based_on_role(user)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_based_on_role(user)
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})



def unauthorized(request):
    return render(request, 'users/unauthorized.html')


def redirect_based_on_role(user):
    if user.user_type == 'student':
        return redirect('game_list')  # Redirect to game list for students
    elif user.user_type == 'teacher':
        return redirect('dashboard')   # Teacher dashboard
    elif user.user_type == 'admin':
        return redirect('/admin/')     # Django admin
    else:
        return redirect('unauthorized')  # Optional unauthorized page