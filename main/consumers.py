import json
from . import models
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

class AtcConsumer(WebsocketConsumer):
    def connect(self):
      self.room_name = self.scope['url_route']['kwargs']['room']
      self.room_group_name = f'chat_{self.room_name}'
      async_to_sync(self.channel_layer.group_add)(
          self.room_group_name,
          self.channel_name
      )
      self.accept()
      
      self.send(text_data=json.dumps({
        'type' : "debug",
        'message' : 'Connection to Server established'
      }))
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        callsign = text_data_json["callsign"]
        changed_attribute = text_data_json["changed_attribute"]
        value = text_data_json["value"]
        if callsign != "" and changed_attribute != "":
          room = models.Room.objects.get(name=self.room_name)
          plane = models.Aircraft.objects.get(room=room, Callsign=callsign)
          if changed_attribute == "Gate":
            plane.Gate = value
          elif changed_attribute == "Departure":
            plane.Departure = value
          elif changed_attribute == "Arrival":
            plane.Arrival = value
          elif changed_attribute == "Info":
            plane.Info = value
          elif changed_attribute == "Taxi":
            if validateJSON(value):
              plane.Info = json.loads(value)
            else:
              return
          elif changed_attribute == "AircraftType":
            plane.AircraftType = value
          elif changed_attribute == "Altitude" and value.is_numeric:
            plane.Altitude = int(value)
          elif changed_attribute == "Squawk":
            plane.Squawk = value
          elif changed_attribute == "Add_Infos":
            plane.Add_Info = value
          elif changed_attribute == "Callsign":
            plane.Callsign = value
          plane.save()
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'edit_message',
                'message':message,
                'callsign':callsign,
                'changed_attribute':changed_attribute,
                'value':value
                
            }
        )

    def edit_message(self, event):
        message = event['message']
        callsign = event["callsign"]
        changed_attribute = event["changed_attribute"]
        value = event["value"]
        self.send(text_data=json.dumps({
            'type':'edit',
            'message': message,
            'callsign':callsign,
            'changed_attribute':changed_attribute,
            'value':value
        }))
      
    def disconnect(self, close_code):
      print(f'Connection closed: {close_code}')
      async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)