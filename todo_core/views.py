from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        my_task, count = reload(request)
        creator_model = Creator()
        if request.method == "POST":
            title = request.POST['title']
            if not title:
                return redirect("/")

            if len(title) > 200:
                overweight = True
                return render(request, "index.html", {"task": my_task, "count": count, "overweight": overweight})

            user = User.objects.get(id = request.user.id)
            human = Human.objects.get(user = user)
            task = Task.objects.create(title = title)
            creator_model.human = human
            creator_model.task = task
            creator_model.save()
            my_task, count = reload(request)
            return render(request, "index.html", {"task": my_task, 'count': count})
        
        return render(request, "index.html", {"task": my_task, 'count': count})
    else:
        tasks = Task.objects.order_by("-date")
        all_tasks = []
        count = 0
        for i in tasks:
            creator = Creator.objects.get(task_id = i.id)
            t = (creator.task.title, creator.task.date, creator.human.user.get_full_name)
            all_tasks.append(t)
            count += 1
        
        return render(request, "index.html", {"tasks": all_tasks, 'count': count})
    


@login_required
def reload(request):
    my_task = []
    count = 0
    try:
        human = Human.objects.get(user_id = request.user.id)
    except:
        return my_task, my_task
    creators = Creator.objects.filter(human = human)
    
    for i in creators:
        t = (i.task.id, i.task.title, i.task.date, i.human.user.get_full_name)
        my_task.append(t)
        count += 1

    return my_task, count


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username  = username, password = password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            alert = True
            return render(request, 'login.html', {'alert': alert})
    
    return render(request, 'login.html')

def user_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            passnotmatch = True
            return render(request, 'registration.html', {'passnotmatch': passnotmatch})
        check_user = User.objects.filter(username = username)
        if check_user.exists():
            existing = True
            return render(request, "registration.html", {"exsiting": existing})

        user = User.objects.create_user(username = username, email = email,
            first_name = first_name, last_name = last_name, password = password)
        human = Human.objects.create(user = user)
        user.save()
        human.save()
        alert = True
        return render(request, 'registration.html', {'alert': alert})
    
    return render(request, 'registration.html')

@login_required
def edit_task(request, myid):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
        task = Task.objects.get(id = myid)
    except:
        return redirect("/")

    if request.method == "POST":
        title = request.POST['title']
        task.title = title
        task.save()
        alert = True
        return render(request, "edit.html", {"alert": alert})
    
    return render(request, "edit.html", {"task": task})

@login_required
def delete_task(request, myid):
    if request.user.is_authenticated:
        check_task = Task.objects.filter(id = myid)
        print(check_task)
        if not check_task.exists():
            return redirect("/")
        task = Task.objects.get(id = myid)
        task.delete()
        return redirect("/")

    return redirect("/")

def Logout(request):
    logout(request)
    return redirect("/")
