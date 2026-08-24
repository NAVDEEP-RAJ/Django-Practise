from django.shortcuts import render,redirect

from django.http import HttpResponse
from django.db.models import Q

from .models import Rooms,Topic

from .forms import RoomForm

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login


'''rooms=[
    {'id':1,'name':"Let's learn python"},
    {'id':2,'name':"It is easy language"},
    {'id':3,'name':'Third page'}

]'''

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

def createroom(request):
    form = RoomForm()
    if request.method=='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context={'form':form}
    return render(request,'base/rooms_form.html',context)

def updateroom(request,pk):
    room = Rooms.objects.get(id=pk)
    form = RoomForm(instance=room)
    context={'form':form}
    if request.method=='POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'base/rooms_form.html',context)

def deleteroom(request,pk):
    room = Rooms.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
    try: 
        user = User.objects.get(username=username)
    except:
        messages.error(request, "User doesn't exist")
    return render(request,'base/login_register.html',{})


