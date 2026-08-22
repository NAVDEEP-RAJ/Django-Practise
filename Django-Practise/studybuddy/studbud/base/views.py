from django.shortcuts import render

from django.http import HttpResponse

rooms=[
    {'id':1,'name':"Let's learn python"},
    {'id':2,'name':"It is easy language"},
    {'id':3,'name':'Third page'}

]

def home(request):
    return render(request,'base/home.html',{'rooms':rooms})

def room(request,pk):
    room = None
    for i in rooms:
        if i['id']==int(pk):
            room=i
    return render(request,'base/rooms.html',{'room':room})
