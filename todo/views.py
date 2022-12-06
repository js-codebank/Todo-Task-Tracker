from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import TodoNote
from .forms import TodoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Username already in use.'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':UserCreationForm(), 'error':'Username and password combination does not exist'})
        else:
            login(request,user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def currenttodos(request):
    todos = TodoNote.objects.filter(user=request.user, completed__isnull=True).order_by('category')
    #Only pass a category if it is included in the users todo, elimantes extra empty headers
    cats = todos.values('category').distinct()
    c = list(list(zip(*TodoNote.TIME_CATEGORY.choices))[1])
    toPass = set()
    for i in cats:
        toPass.add(TodoNote.TIME_CATEGORY(i['category']).label)
    for i in c:
        if i not in toPass:
            c.remove(i)
    return render(request, 'todo/currenttodos.html', {'todos':todos, 'categories':tuple(c)})

@login_required
def completedtodos(request):
    todos = TodoNote.objects.filter(user=request.user, completed__isnull=False).order_by('-completed')
    #Only pass a category if it is included in the users todo, elimantes extra empty headers
    cats = todos.values('category').distinct()
    c = list(list(zip(*TodoNote.TIME_CATEGORY.choices))[1])
    toPass = set()
    for i in cats:
        toPass.add(TodoNote.TIME_CATEGORY(i['category']).label)
    for i in c:
        if i not in toPass:
            c.remove(i)
    return render(request, 'todo/completedtodos.html', {'todos':todos, 'categories':tuple(c)})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(TodoNote, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todos':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todos':todo, 'form':form, 'error':'Invalid Entry, try again.'})

@login_required
def addtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/addtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/addtodo.html', {'form':TodoForm(), 'error':'Bad data entered, try again.'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(TodoNote, pk=todo_pk, user=request.user )
    if request.method == 'POST':
        todo.completed = timezone.now()
        todo.save()
    return redirect('currenttodos')

@login_required
def uncompletetodo(request, todo_pk):
    todo = get_object_or_404(TodoNote, pk=todo_pk, user=request.user )
    if request.method == 'POST':
        todo.completed = None
        todo.save()
    return redirect('completedtodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(TodoNote, pk=todo_pk, user=request.user )
    if request.method == 'POST':
        todo.delete()
    #TODO change this redirect to return user to last page
    return redirect('currenttodos')

def home(request):
    return render(request,'todo/home.html')

