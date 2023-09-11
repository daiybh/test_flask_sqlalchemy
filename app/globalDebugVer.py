from dataclasses import dataclass

@dataclass
class GlobalVar:    
    last_update_response:str =""
    last_parkJson:str=""
    last_updateLED:str=""
    last_updateLED_time:int =0
    last_update_time=0
    current_empty_plot =0
    ledTaskThread=None