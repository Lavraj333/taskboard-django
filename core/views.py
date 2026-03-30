from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home(request):
    visits = int(request.COOKIES.get('visits', 0)) + 1
    response = render(request, 'home.html', {'visits': visits})
    response.set_cookie('visits', visits)
    return response


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)

    request.session['last_page'] = 'tasks'

    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'form': form})


@login_required
def edit_task(request, id):
    task = Task.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form})


@login_required
def delete_task(request, id):
    task = Task.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

    return render(request, 'delete_task.html', {'task': task})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('tasks')
        else:
            return HttpResponse("Invalid credentials")

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')

def error_view(request):
    raise Exception("Test error")