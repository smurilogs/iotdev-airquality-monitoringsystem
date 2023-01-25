import json
import pandas as pd
import requests
import datetime
from dotenv import load_dotenv

from domain.entities import *
from repository.sqlalchemy import *
from utility.changecapture import *
from utility.filehandler import *

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

def _assemply_response_uplink_messages(uplink_messages_response):
    
    content_str = '[' + uplink_messages_response.content.decode("utf-8") + ']'
    content_str = content_str.replace('\n', '')
    content_str = content_str.replace('{"result":', ',{"result":')
    content_str = content_str.replace('[,{"result":', '[{"result":')

    response_uplink_messages = json.loads(content_str)
    return response_uplink_messages    

# catches curr
uplink_messages_response = _request_uplink_messages_response()
response_uplink_messages = _assemply_response_uplink_messages(uplink_messages_response)
FileHandler.save_json_file(response_uplink_messages, './data/cached_curr_uplink_messages.json')

curr_df = pd.read_json('./data/cached_curr_uplink_messages.json', orient='records')
curr_df = curr_df.astype(str)  


#
last_df = None
try:
    last_df = pd.read_json('./data/cached_last_uplink_messages.json', orient='records')
except:
    last_df = pd.DataFrame(columns=curr_df.columns.tolist(), dtype=str,)
    
last_df = last_df.astype(str)  

inserts_df = ChangeCapture.get_wide_inserts_df(curr_df.copy(), last_df.copy(), CC_KEYS, CC_SOURCE)

# turn curr into last
FileHandler.save_json_file(response_uplink_messages, './data/cached_last_uplink_messages.json')

repo = SqlAlchemyRepository()
repo.init()

samples = []
for i in range(len(inserts_df)):

    insert_str = str(inserts_df.loc[i, 'result']).replace('\'', '\"')
    temp_insert_dic = json.loads(insert_str)

    sample = Sample(
        sensorar_sample_id = None,
        ttn_gateway_id = temp_insert_dic['uplink_message']['rx_metadata'][0]['gateway_ids']['gateway_id'],
        ttn_gateway_lat = temp_insert_dic['uplink_message']['rx_metadata'][0]['location']['latitude'],
        ttn_gateway_lng = temp_insert_dic['uplink_message']['rx_metadata'][0]['location']['longitude'],
        ttn_device_id = temp_insert_dic['end_device_ids']['device_id'],
        ttn_received_at = datetime.fromisoformat(str(temp_insert_dic['received_at'])),
        ttn_payload_frm = temp_insert_dic['uplink_message']['frm_payload'],
        ttn_payload_temp = temp_insert_dic['uplink_message']['decoded_payload']['temp'],
        ttn_payload_rh = temp_insert_dic['uplink_message']['decoded_payload']['rh'],
        ttn_payload_pm1_0 = temp_insert_dic['uplink_message']['decoded_payload']['pm1_0'],
        ttn_payload_pm2_5 = temp_insert_dic['uplink_message']['decoded_payload']['pm2_5'],
        ttn_payload_pm10_0 = temp_insert_dic['uplink_message']['decoded_payload']['pm10_0']
    )
    
    samples.append(sample)

for sample in samples:
    repo.create_register(sample)

#wide_inserts_df['result'].to_list()
#wide_inserts_df['result'].astype(dic).to_dict('records')