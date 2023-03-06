import os
import json
import pandas as pd
import requests
from datetime import datetime
import pytz
import sqlite3
import schedule
import time
from dotenv import load_dotenv

from entities import *
from repository import *

load_dotenv()

CC_SOURCE = os.environ.get('TTN_APP_NAME')
CC_KEYS = ['result']

TTN_CLUSTER_REGION = os.environ.get('TTN_CLUSTER_REGION')
TTN_APP_NAME = os.environ.get('TTN_APP_NAME')
TTN_API_KEY = os.environ.get('TTN_API_KEY')


def _request_uplink_messages_response():
    headers = {
        'Authorization': f'Bearer { TTN_API_KEY }',
        'Accept': 'text/event-stream'
    }
    params ={
        'after': '2023-01-22T00:00:00Z',
        'field_mask': 'up.uplink_message'
    }
    response = requests.get(
        (
            f'https://{ str(TTN_CLUSTER_REGION).lower() }.cloud.thethings.network/api/v3/as'
            f'/applications/{ TTN_APP_NAME }/packages/storage/uplink_message'
        ),
        headers=headers,
        params=params
    )
    return response

def _assemply_response_uplink_dicts(uplink_messages_response):
    content_str = '[' + uplink_messages_response.content.decode("utf-8") + ']'
    content_str = content_str.replace('\n', '')
    content_str = content_str.replace('{"result":', ',{"result":')
    content_str = content_str.replace('[,{"result":', '[{"result":')
    response_uplink_dicts = json.loads(content_str)
    return response_uplink_dicts    

def _assembly_uplink_dicts(response_uplink_dicts):
    uplink_dicts = []
    for response_uplink_dict in response_uplink_dicts:
        uplink_dict = {
            'ttn_gateway_id': response_uplink_dict['result']['uplink_message']['rx_metadata'][0]['gateway_ids']['gateway_id'],
            'ttn_gateway_lat': response_uplink_dict['result']['uplink_message']['rx_metadata'][0]['location']['latitude'],
            'ttn_gateway_lng': response_uplink_dict['result']['uplink_message']['rx_metadata'][0]['location']['longitude'],
            'ttn_device_id': response_uplink_dict['result']['end_device_ids']['device_id'],
            'ttn_received_at': datetime.fromisoformat(str(response_uplink_dict['result']['received_at'])).astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S'),
            'ttn_payload_frm': response_uplink_dict['result']['uplink_message']['frm_payload'],
            'ttn_payload_temp': response_uplink_dict['result']['uplink_message']['decoded_payload']['temp'],
            'ttn_payload_rh': response_uplink_dict['result']['uplink_message']['decoded_payload']['rh'],
            'ttn_payload_pm1_0': response_uplink_dict['result']['uplink_message']['decoded_payload']['pm1_0'],
            'ttn_payload_pm2_5': response_uplink_dict['result']['uplink_message']['decoded_payload']['pm2_5'],
            'ttn_payload_pm10_0': response_uplink_dict['result']['uplink_message']['decoded_payload']['pm10_0']      
        }
        uplink_dicts.append(uplink_dict)
    return uplink_dicts

def get_last_timestamp_str():
    con = sqlite3.connect('././data/db.sqlite3')
    select_df = pd.read_sql_query('SELECT MAX(ttn_received_at) as ttn_received_at FROM sample_tb', con)
    con.close()
    if(select_df.loc[0, 'ttn_received_at'] is not None):  
        last_timestamp_str = str(select_df.loc[0, 'ttn_received_at'])    
        return last_timestamp_str
    return '2000-01-01 00:00:00.000000000'

def main():
    
    repo = SqlAlchemyRepository()
    repo.init()

    uplink_messages_response = _request_uplink_messages_response()
    response_uplink_dicts = _assemply_response_uplink_dicts(uplink_messages_response)
    uplink_dicts = _assembly_uplink_dicts(response_uplink_dicts)

    uplink_df = pd.DataFrame.from_dict(uplink_dicts)
    uplink_df = uplink_df.astype(str)  

    last_timestamp_str = get_last_timestamp_str()
    print(last_timestamp_str)

    if(len(uplink_df) > 0):

        inserts_df = uplink_df[uplink_df['ttn_received_at'] > last_timestamp_str].reset_index(drop=True)
        inserts_df = inserts_df.astype(str)

        samples = []
        for i in range(len(inserts_df)):
            sample = Sample(
                sensorar_sample_id = None,
                ttn_gateway_id = inserts_df.loc[i, 'ttn_gateway_id'],
                ttn_gateway_lat = float(inserts_df.loc[i, 'ttn_gateway_lat']),
                ttn_gateway_lng = float(inserts_df.loc[i, 'ttn_gateway_lng']),
                ttn_device_id = inserts_df.loc[i, 'ttn_device_id'],
                ttn_received_at = datetime.strptime(str(inserts_df.loc[i, 'ttn_received_at']), '%Y-%m-%d %H:%M:%S'),
                ttn_payload_frm = inserts_df.loc[i, 'ttn_payload_frm'],
                ttn_payload_temp = float(inserts_df.loc[i, 'ttn_payload_temp']),
                ttn_payload_rh = float(inserts_df.loc[i, 'ttn_payload_rh']),
                ttn_payload_pm1_0 = float(inserts_df.loc[i, 'ttn_payload_pm1_0']),
                ttn_payload_pm2_5 = float(inserts_df.loc[i, 'ttn_payload_pm2_5']),
                ttn_payload_pm10_0 = float(inserts_df.loc[i, 'ttn_payload_pm10_0'])
            )
            samples.append(sample)

        for sample in samples:
            repo.create_register(sample)

if __name__ == '__main__':
    
    schedule.every().day.at('00:00').do(main)
    schedule.every().day.at('12:00').do(main)
    schedule.every().minute.at(':00').do(main)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
