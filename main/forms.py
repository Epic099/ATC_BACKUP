from django import forms
from . import database
from .models import Room

cl = database.Client()

options = []
val = cl.get_airports()
ICAOS = []
for i in range(0, len(val)):
  ICAOS.append((val[i], val[i]))



for code in cl.get_airports():
    options.append((f"{code}", code))

class RoomForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), empty_label=None, label="Select a Room to join")
    
class CreateRoomForm(forms.Form):
    room_name = forms.CharField(max_length=20)
    icao = forms.ChoiceField(choices=ICAOS)