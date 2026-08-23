from django.shortcuts import render,redirect

from django.http import HttpResponse

from .models import Rooms

from .forms import RoomForm

'''rooms=[
    {'id':1,'name':"Let's learn python"},
    {'id':2,'name':"It is easy language"},
    {'id':3,'name':'Third page'}

]'''

def home(request):
    rooms=Rooms.objects.all()
    context={'rooms':rooms}
    return render(request,'base/home.html',context)

def room(request,pk):
    room=Rooms.objects.get(id=pk)
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


