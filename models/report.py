from datetime import datetime
import json
from operator import attrgetter

class Report:
    def __init__(self, report_name: str, date_start: str, date_end: str, token: str, list_images: list[str], list_mesures_power: list[dict[str, object]], list_mesures_pc: list[dict[str, object]]):
        self.name: str | None = report_name
        self.t_debut: str | None = date_start
        self.t_fin: str | None = date_end
        self.token: str | None = token
        self.images: list[str] | None = list_images
        self.measures_power: list[dict[str, object]] | None = list_mesures_power
        self.measures_pc: list[dict[str, object]] | None = list_mesures_pc


    def destructuring(self):
        '''Return the destructuring object of Report, convert to JSON'''
        
        name, t_debut, t_fin, token, images, measures_power, measures_pc = attrgetter('name', 't_debut', 't_fin', 'token', 'images', 'measures_power', 'measures_pc')(self)
                
        data = {
            "name":name, 
            "t_debut": t_debut, 
            "t_fin": t_fin, 
            "token": token,
            "images": images, 
            "measures_power": measures_power, 
            "measures_pc": measures_pc
        }
        
        json_data = json.dumps(data)
        
        return json_data