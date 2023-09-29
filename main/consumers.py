import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class AtcConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
        self.send(text_data=json.dumps({
            'type' : 'connection_established',
            'message' : 'connected'
        }))
    
    