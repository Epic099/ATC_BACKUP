from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=1000)
    icao = models.CharField(max_length=4, default="IRFD")
    def __str__(self):
      return f"{self.name}"


class Aircraft(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Callsign = models.CharField(max_length=15)
    Taxi = models.JSONField(null=True, default=["0"])
    Runway = models.CharField(max_length=10, null=True, default="0")    
    Departure = models.CharField(max_length=4, default=" ")
    Arrival = models.CharField(max_length=4, default=" ")
    Squawk = models.CharField(max_length=4, default="0000")
    Info = models.CharField(max_length=10, default=" ")
    Add_Info = models.TextField(default=" ")
    AircraftType = models.CharField(max_length=15, default=" ")
    Altitude = models.IntegerField(default=0)
    Gate = models.CharField(max_length=10, default=" ")
    lastInstruction = models.CharField(max_length=255, null=True, default=" ")
    Incoming = models.BooleanField(default=True)
    
    def __str__(self):
      return f"{self.room}  |  {self.Callsign}"