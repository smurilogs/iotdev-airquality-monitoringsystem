
from typing import List
from datetime import datetime

class Sample(object):
    
    def __init__(
        self,
        sensorar_sample_id:int,
        ttn_gateway_id:str,
        ttn_gateway_lat:float,
        ttn_gateway_lng:float,
        ttn_device_id:str,
        ttn_received_at:datetime,
        ttn_payload_frm:str,
        ttn_payload_temp:float,
        ttn_payload_rh:float,
        ttn_payload_pm1_0:float,
        ttn_payload_pm2_5:float,
        ttn_payload_pm10_0:float
    ):
        self.sensorar_sample_id = sensorar_sample_id
        self.ttn_gateway_id = ttn_gateway_id
        self.ttn_gateway_lat = ttn_gateway_lat
        self.ttn_gateway_lng = ttn_gateway_lng
        self.ttn_device_id = ttn_device_id
        self.ttn_received_at = ttn_received_at
        self.ttn_payload_frm = ttn_payload_frm
        self.ttn_payload_temp = ttn_payload_temp
        self.ttn_payload_rh = ttn_payload_rh
        self.ttn_payload_pm1_0 = ttn_payload_pm1_0
        self.ttn_payload_pm2_5 = ttn_payload_pm2_5
        self.ttn_payload_pm10_0 = ttn_payload_pm10_0
                
