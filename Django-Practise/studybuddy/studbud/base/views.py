from django.shortcuts import render

from django.http import HttpResponse

from .models import Rooms

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
