from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CreateUserForm
from .models import Task
import calendar
from calendar import HTMLCalendar
from datetime import datetime


@login_required(login_url='todo-login')
def index(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.session.get('user_id'))
        count_tasks = tasks.filter(user=request.session.get('user_id')).count()
        completed_tasks = Task.objects.filter(completed=True).filter(user=request.session.get('user_id'))
        count_completed_tasks = completed_tasks.filter(user=request.session.get('user_id')).count()
        un_completed_tasks = Task.objects.filter(completed=False).filter(user=request.session.get('user_id'))
        count_un_completed_tasks = un_completed_tasks.filter(user=request.session.get('user_id')).count()
        context = {
            'tasks': tasks,
            'count_tasks': count_tasks,
            'count_completed_tasks': count_completed_tasks,
            'count_un_completed_tasks': count_un_completed_tasks,
        }
        return render(request, 'todo/index.html', context)
    else:
        return render(request, 'Accounts/Login.html')


def registerpage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('todo-login')
        context = {
            'form': form
        }
        return render(request, 'Accounts/Register.html', context)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            request.session["user_id"] = user.id
            if user is not None:
                login(request, user)
                return redirect('todo-index')
            else:
                messages.info(request, 'Username Or Password is Incorrect')
        return render(request, 'Accounts/Login.html',)


@login_required(login_url='todo-login')
def add_task(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.session.get('user_id'))
        count_tasks = tasks.filter(user=request.session.get('user_id')).count()
        completed_tasks = Task.objects.filter(completed=True).filter(user=request.session.get('user_id'))
        count_completed_tasks = completed_tasks.filter(user=request.session.get('user_id')).count()
        un_completed_tasks = Task.objects.filter(completed=False).filter(user=request.session.get('user_id'))
        count_un_completed_tasks = un_completed_tasks.filter(user=request.session.get('user_id')).count()
        if request.method == 'POST':
            user = User.objects.get(id=request.session.get('user_id'))
            if request.POST['content'] != '':
                Task.objects.create(content=request.POST['content'], user=user)
            tasks = Task.objects.filter(user=request.session.get('user_id'))
            count_tasks = tasks.filter(user=request.session.get('user_id')).count()
            completed_tasks = Task.objects.filter(completed=True).filter(user=request.session.get('user_id'))
            count_completed_tasks = completed_tasks.filter(user=request.session.get('user_id')).count()
            un_completed_tasks = Task.objects.filter(completed=False).filter(user=request.session.get('user_id'))
            count_un_completed_tasks = un_completed_tasks.filter(user=request.session.get('user_id')).count()
        context = {
            'count_completed_tasks': count_completed_tasks,
            'count_tasks': count_tasks,
            'count_un_completed_tasks': count_un_completed_tasks,
        }
        return render(request, 'todo/addtask.html', context)
    else:
        return render(request, 'Accounts/Login.html')


@login_required(login_url='todo-login')
def search(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            searched = request.POST['searched']
            task = Task.objects.filter(content__contains=searched)
            context = {
                'searched': searched,
                'task': task,
                }
            return render(request, 'todo/search.html', context)
    else:
        return render(request, 'Accounts/Login.html')


@login_required(login_url='todo-login')
def update(request, pk):
    if request.user.is_authenticated:
        todo = Task.objects.get(id=pk)
        if request.method == 'POST':
            Task.objects.filter(id=pk).update(content=request.POST['content'])
            if 'completed' in request.POST:
                completed = True
            elif 'completed' not in request.POST:
                completed = False
            Task.objects.filter(id=pk).update(completed=completed)
            return redirect('/')
        else:
            checked = ''
            if todo.completed == "on":
                checked = 1
            elif todo.completed == "":
                checked = 0
            context = {
                "content": todo.content,
                "completed": todo.completed,
                "checked": checked,
            }
            return render(request, 'todo/update.html', context)
    else:
        return render(request, 'Accounts/Login.html')


@login_required(login_url='todo-login')
def show_completed(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.session.get('user_id'))
        count_tasks = tasks.filter(user=request.session.get('user_id')).count()
        completed_tasks = Task.objects.filter(completed=True).filter(user=request.session.get('user_id'))
        count_completed_tasks = completed_tasks.filter(user=request.session.get('user_id')).count()
        un_completed_tasks = Task.objects.filter(completed=False).filter(user=request.session.get('user_id'))
        count_un_completed_tasks = un_completed_tasks.filter(user=request.session.get('user_id')).count()
        context = {
            'completed_tasks': completed_tasks,
            'count_completed_tasks': count_completed_tasks,
            'count_tasks': count_tasks,
            'count_un_completed_tasks': count_un_completed_tasks,
        }
        return render(request, 'todo/completed.html',  context)
    else:
        return render(request, 'Accounts/Login.html')


@login_required(login_url='todo-login')
def show_uncompleted(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.session.get('user_id'))
        count_tasks = tasks.filter(user=request.session.get('user_id')).count()
        completed_tasks = Task.objects.filter(completed=True).filter(user=request.session.get('user_id'))
        count_completed_tasks = completed_tasks.filter(user=request.session.get('user_id')).count()
        un_completed_tasks = Task.objects.filter(completed=False).filter(user=request.session.get('user_id'))
        count_un_completed_tasks = un_completed_tasks.filter(user=request.session.get('user_id')).count()

        context = {
            'count_completed_tasks': count_completed_tasks,
            'count_tasks': count_tasks,
            'count_un_completed_tasks': count_un_completed_tasks,
            'un_completed_tasks': un_completed_tasks,
        }
        return render(request, 'todo/uncompleted.html', context)
    else:
        return render(request, 'Accounts/Login.html')


@login_required(login_url='todo-login')
def delete(request, pk):
    if request.user.is_authenticated:
        todo = Task.objects.get(id=pk)
        if request.method == 'POST':
            todo.delete()
            return redirect('/')
        return render(request, 'todo/delete.html')
    else:
        return render(request, 'Accounts/Login.html')


def lougoutuser(request):
    request.session.clear()
    logout(request)
    return redirect('todo-login')


'''
@login_required(login_url='todo-login')
def calendar(request, year, month):
    if request.user.is_authenticated:
        month = month.capitalize()
        month_number = list(calendar.month_name).index(month)
        month_number = int(month_number)
        cal = HTMLCalendar().formatmonth(year, month)
        now = datetime.now()
        current_year = now.year
        print(year)
        print(month)
        context = {
            'year': year,
            'month': month,
            'month_number': month_number,
            'cal': cal,
            'current_year': current_year,
        }
        return render(request, 'partials/calendar.html', context)
    else:
        return render(request, 'Accounts/Login.html') 
'''


