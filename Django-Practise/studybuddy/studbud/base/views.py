from django.shortcuts import render,redirect

from django.http import HttpResponse
from django.db.models import Q

from .models import Rooms,Topic

from .forms import RoomForm

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def home(request):
    q=request.GET.get('q','')
    rooms=Rooms.objects.filter(Q(topic__name__icontains=q)|
                               Q(name__icontains=q)|
                               Q(description__icontains=q) | 
                               Q(host__username__icontains=q))
    topic = Topic.objects.all()
    context={'rooms':rooms,'topic':topic}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Rooms.objects.get(id=pk)
    return render(request,'base/rooms.html',{'room':room})

@login_required(login_url='login')
def createroom(request):
    form = RoomForm()
    if request.method=='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context={'form':form}
    return render(request,'base/rooms_form.html',context)

@login_required(login_url='login')
def updateroom(request,pk):
    room = Rooms.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You ar enot allowed to do this....this is not your room!!!!')

    context={'form':form}
    if request.method=='POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'base/rooms_form.html',context)

@login_required(login_url='login')
def deleteroom(request,pk):
    room = Rooms.objects.get(id=pk)
    if request.user != room.host:
            return HttpResponse('You ar enot allowed to do this....this is not your room!!!!')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:

            user = User . objects .get (username=username)
        except:
            messages. error(request, 'User does not exist')
            return render(request,'base/login_register.html',{'page':'login'})


        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    context={'page':page}
    return render(request, 'base/login_register.html',context)

def registerpage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request,user)
            return redirect('home')
        else:
            print(form.errors)
    return render(request, 'base/login_register.html',{'form':form,'page':'register'})

def logoutpage(request):
    logout(request)
    return redirect('home')

