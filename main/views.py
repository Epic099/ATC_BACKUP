from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .import forms
from .models import Aircraft, Room
from .import models
from .database import Client
import urllib.parse
import os

def valid_room(room_name):
  rooms = Room.objects.all()
  for r in rooms:
    if str(r.name) == str(room_name):
      return True
  return False

client = Client()

def home(request):
    return render(request, 'main/home.html')

@login_required(login_url="/login")
def atc(request):
    if request.method == "POST":
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            rooms = Room.objects.all()
            r = form.cleaned_data["room"]
            print(valid_room(r))
            if valid_room(r):
              print(r)
              return redirect(f"atc/{r}")
            else:
              return redirect("atc")
        form = forms.CreateRoomForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["room_name"]
            icao = form.cleaned_data["icao"]
            if name != "" and icao != "":
              r = models.Room.objects.create(name=name, icao=icao)
            
              return redirect(f"atc/{name}")
    else:
        form = forms.RoomForm()
        createform = forms.CreateRoomForm()
        return render(request, 'main/atc.html', context={"form" : form, "form2" : createform})
@login_required(login_url="/login")
def room(request, room : str):
  rooms = Room.objects.all()
  if not valid_room(room):
    return HttpResponseNotFound("Room not found")
  room = Room.objects.filter(name=room).first()
  aircrafts = Aircraft.objects.filter(room=room)
  inair = []
  outair = []
  for aircraft in aircrafts:
    if aircraft.Incoming == True:
      inair.append(aircraft)
    else:
      outair.append(aircraft)
  return render(request, "main/room.html", context={"room" : room, "icao" : room.icao, "in_aircrafts" : inair, "out_aircrafts" : outair})

      
@login_required(login_url="/login")
def airport(request, icao : str):
    if request.method == "GET":
        chart_dirs = client.get_Charts(icao)
        callsign = request.GET.get("callsign")
        runway = request.GET.get("runway")
        if not client.runway_valid(icao, runway):
            runway = client.get_default_runway(icao)
            return redirect(f"/atc/{icao}?runway={runway}&callsign={callsign}")
        airways = []
        for chart in chart_dirs.airway:
            if str.find(os.path.basename(chart), runway) >= 0:
                airways.append(chart)
        aircrafts = Aircraft.objects.all()
        print(aircrafts)
        return render(request, 'main/airport.html', context={"ICAO" : icao, "Ground_Charts" : chart_dirs.ground, "Airway_Charts" : airways, "Callsign" : callsign, "aircrafts" : aircrafts})
    else:
        return HttpResponseBadRequest("Post request was made, which is unsupported")