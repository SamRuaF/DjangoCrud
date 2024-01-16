from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm 
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):

    return render(request, 'home.html', {

        'form' :  UserCreationForm
    })
def handler404(request, exception):
   return render(request, '404.html', status=404)


def signup(request):
    if request.method == 'GET':
        print("Enviando formulario")
        
        return render(request, 'signup.html', {


        'form' :  UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                
                #Register User
                user = User.objects.create_user(username=request.POST.get('username'),password= request.POST.get("password1"))
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                 return render(request, 'signup.html', {


        'form' :  UserCreationForm,
        "error": "User already exist"
        })

                
        return render(request, 'signup.html', {


        'form' :  UserCreationForm,
        "error": "password don't match"
        })

        print(request.POST)
        print('Obteniendo datos')

@login_required
def tasks(request):

    tasks = Task.objects.filter(user= request.user, datecompleted__isnull = True) #Esto devuelve las tareas que hay en bd
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):

    tasks = Task.objects.filter(user= request.user, datecompleted__isnull = False).order_by('-datecompleted')#Obtenemos las mismas tareas
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_tasks(request):

    if request.method =='GET':
        return render(request, 'create_task.html', {
        'form': TaskForm
    })
    else: 
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit = False)
            new_task.user = request.user
            print(new_task)
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm, 'error': 'Porfavor poner datos validos'})

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task,pk=task_id, user = request.user) #Buscamos solo nuetras tareas
        form = TaskForm(instance=task) #Obtenemos el formulario
        return render(request, 'task_detail.html', {'task':task, 'form':form})
    else:
       try:
            task = get_object_or_404(Task, pk=task_id, user = request.user) #Buscamos solo nuetras tareas
            form = TaskForm(request.POST, instance=task) #Genera un nuevo formulario
            form.save()
            return redirect('tasks')
       except ValueError:
           return render(request, 'task_detail.html', {'task':task, 'form':form, 'error':'error al actualizar task'})

@login_required
def completed_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now() #Cuando tenemos una fecha es porque ya es completado
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {

        'form': AuthenticationForm
    })
    else:
        user = authenticate(request, username=request.POST['username'], password= request.POST['password'],
                     )
        if user is None:
             return render(request, 'signin.html', {

        'form': AuthenticationForm,
        'error': 'Username or password is incorrect'
        })
        else: 
            login(request, user)
            return redirect('tasks')

        