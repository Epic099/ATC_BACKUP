import json, os
from django.conf import settings
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

class Charts():
    def __init__(self, ground, airway) -> None:
        self.ground = ground
        self.airway = airway

class Server():
    Airport_Data = None
    def init():
        global Airport_Data
        path = os.path.join(BASE_DIR, "static", "json", "airport_Data.json")
        with open(path, "r") as file:
            Airport_Data = json.loads(file.read())
    def get_airports():
        return Airport_Data["Airports"]
    
    def get_charts(icao):
        ground_charts = Airport_Data["Charts_Data"][icao]["Ground_Images"]
        appr_charts = Airport_Data["Charts_Data"][icao]["Approach_Images"]
        image_dir = os.path.join(settings.STATIC_ROOT, "images", "Charts", icao, "Ground")
        ground_files = []
        for chart in ground_charts:
            if os.path.isfile(os.path.join(image_dir, chart)):
                ground_files.append(f"images\\Charts\\{icao}\\Ground\\{chart}")
        image_dir = os.path.join(settings.STATIC_ROOT, "images", "Charts", icao, "Airway")
        appr_files = []
        for key in appr_charts:
            chart = appr_charts[key]
            if os.path.isfile(os.path.join(image_dir, chart)):
                appr_files.append(f"images\\Charts\\{icao}\\Airway\\{chart}")
        arrival_files = []
        
        airway_charts = appr_files + arrival_files
        
        
        #Implement Other Charts types later
        return Charts(ground_files, airway_charts)
    def runway_valid(icao : str, runway : str):        
        runways = Airport_Data["Charts_Data"][icao]["Runways"]
        return runway in runways
    
    def get_default_runway(icao : str):
        return Airport_Data["Charts_Data"][icao]["Default_Runway"]
Server.init()


class Client():
    def __init__(self):
        pass
    
    def get_airports(self):
        return Server.get_airports()
    
    def get_Charts(self, icao : str):
        return Server.get_charts(icao)
    
    def runway_valid(self, icao : str, runway : str):
        return Server.runway_valid(icao, runway)
    
    def get_default_runway(self, icao : str):
        return Server.get_default_runway(icao)
