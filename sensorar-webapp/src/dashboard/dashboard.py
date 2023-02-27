

import pandas as pd
import numpy as np
import streamlit as st
import datetime
import sqlite3
from datetime import datetime, timedelta

def get_iqar_df(select_df):

    if(len(select_df) != 0):
        #
        select_df = select_df[['ttn_device_id', 'ttn_received_at', 'ttn_payload_temp', 'ttn_payload_rh', 'ttn_payload_pm1_0', 'ttn_payload_pm2_5', 'ttn_payload_pm10_0']]
        def apply_func(ttn_received_at):
            date = datetime.fromisoformat(str(ttn_received_at))	
            date = date.replace(microsecond=0).replace(second=0).replace(minute=0).replace(hour=0)
            date = date.strftime('%Y-%m-%d')
            return date
        select_df['ttn_received_at'] = select_df.apply(lambda x: apply_func(x['ttn_received_at']), axis=1)

        #
        select_df = select_df.groupby(['ttn_device_id', 'ttn_received_at']).agg(
            ttn_payload_temp = ('ttn_payload_temp', 'mean'),
            ttn_payload_rh = ('ttn_payload_rh', 'mean'),
            ttn_payload_pm1_0 = ('ttn_payload_pm1_0', 'mean'),
            ttn_payload_pm2_5 = ('ttn_payload_pm2_5', 'mean'),
            ttn_payload_pm10_0 = ('ttn_payload_pm10_0', 'mean')
        ).reset_index()
        select_df= select_df.round(decimals=2)

        #
        select_df = select_df.rename(columns={
                'ttn_device_id': 'device_id',
                'ttn_received_at': 'received_at',
                'ttn_payload_temp': 'temp',
                'ttn_payload_rh': 'rh',
                'ttn_payload_pm1_0': 'pm1_0',
                'ttn_payload_pm2_5': 'pm2_5',
                'ttn_payload_pm10_0': 'pm10_0',
        })

        #
        select_df['iqar_pm10_0_color'] = None
        select_df['iqar_pm10_0_value'] = None
        for i in range(len(select_df)):
            if(select_df.loc[i, 'pm10_0'] <= 50):
                iqar_color = 'green'
                iqar_value = 0 + ((40 - 0)/(50 - 0)) * (select_df.loc[i, 'pm10_0'] - 0)

            elif(50 < select_df.loc[i, 'pm10_0'] <= 100):
                iqar_color = 'yellow'
                iqar_value = 41 + ((80 - 41)/(100 - 51)) * (select_df.loc[i, 'pm10_0'] - 51)
                
            elif(100 < select_df.loc[i, 'pm10_0'] <= 150):
                iqar_color = 'orange'
                iqar_value = 81 + ((120 - 81)/(150 - 101)) * (select_df.loc[i, 'pm10_0'] - 101)
                    
            elif(150 < select_df.loc[i, 'pm10_0'] <= 250):
                iqar_color = 'red'
                iqar_value = 121 + ((200 - 121)/(250 - 151)) * (select_df.loc[i, 'pm10_0'] - 151)
            
            elif(250 < select_df.loc[i, 'pm10_0']):
                iqar_color = 'purple'
                iqar_value = 201 + ((400 - 201)/(600 - 251)) * (select_df.loc[i, 'pm10_0'] - 251)

            select_df.loc[i, 'iqar_pm10_0_color'] = iqar_color
            select_df.loc[i, 'iqar_pm10_0_value'] = iqar_value

        #
        select_df['iqar_pm2_5_color'] = None
        select_df['iqar_pm2_5_value'] = None
        for i in range(len(select_df)):
            
            if(select_df.loc[i, 'pm2_5'] <= 50):
                iqar_color = 'green'
                iqar_value = 0 + ((40 - 0)/(25 - 0)) * (select_df.loc[i, 'pm2_5'] - 0)
                    
            elif(50 < select_df.loc[i, 'pm2_5'] <= 100):
                iqar_color = 'yellow'
                iqar_value = 41 + ((80 - 41)/(50 - 26)) * (select_df.loc[i, 'pm2_5'] - 26)
                
            elif(100 < select_df.loc[i, 'pm2_5'] <= 150):
                iqar_color = 'orange'
                iqar_value = 81 + ((120 - 81)/(75 - 51)) * (select_df.loc[i, 'pm2_5'] - 51)
                    
            elif(150 < select_df.loc[i, 'pm2_5'] <= 250):
                iqar_color = 'red'
                iqar_value = 121 + ((200 - 121)/(125 - 76)) * (select_df.loc[i, 'pm2_5'] - 76)
            
            elif(250 < select_df.loc[i, 'pm2_5']):
                iqar_color = 'purple'
                iqar_value = 201 + ((400 - 201)/(300 - 126)) * (select_df.loc[i, 'pm2_5'] - 126)

            select_df.loc[i, 'iqar_pm2_5_color'] = iqar_color
            select_df.loc[i, 'iqar_pm2_5_value'] = iqar_value

        return select_df

    else:
        select_df = pd.DataFrame()
        return select_df




def show_pm2_5_plot(iqar_dicts):
    
    st.vega_lite_chart({
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "A simple bar chart with embedded data.",

        "title": "IQAr para MP2,5 (valor adimensional):",
        "width": 900,
        "height": 210,
        "data": {
            "values": iqar_dicts
        },
        "mark": {"type": "bar", "line": False, "point": True},
        "encoding": {
            "x": {
                "field": "received_at",
                "type": "nominal",
                "axis": {
                    "labelAngle": 90,
                    "title": "Data"
                    }
                },
            "y": {
                "field": "iqar_pm2_5_value",
                "type": "quantitative",
                "axis": {
                    "title": "IQAr"
                    },
                "scale": {
                    "domain": [0, 100]
                }
            },
            "color": {
                "field": "iqar_pm2_5_color",
                "type": "nominal",
                "scale": None
            }
        },
        "layer": [
            {"mark": "bar"},
            {
                "mark": {
                    "type": "text",
                    "align": "center",
                    "yOffset": -10,
                    "fontSize": 10
                },
                "encoding": {
                    "text": {
                        "field": "iqar_pm2_5_value",
                        "type": "quantitative",
                        "formatType": "number"
                    }
                }
            }
        ],  
    })

def show_pm10_0_plot(iqar_dicts):
    
    st.vega_lite_chart({
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "A simple bar chart with embedded data.",

        "title": "IQAr para MP10 (valor adimensional):",
        "width": 900,
        "height": 210,
        "data": {
            "values": iqar_dicts
        },
        "mark": {"type": "bar", "line": False, "point": True},
        "encoding": {
            "x": {
                "field": "received_at",
                "type": "nominal",
                "axis": {
                    "labelAngle": 90,
                    "title": "Data"
                    }
                },
            "y": {
                "field": "iqar_pm10_0_value",
                "type": "quantitative",
                "axis": {
                    "title": "IQAr"
                    },
                "scale": {
                    "domain": [0, 100]
                }
            },
            "color": {
                "field": "iqar_pm10_0_color",
                "type": "nominal",
                "scale": None
            }
        },
        "layer": [
            {"mark": "bar"},
            {
                "mark": {
                    "type": "text",
                    "align": "center",
                    "yOffset": -10,
                    "fontSize": 10
                },
                "encoding": {
                    "text": {
                        "field": "iqar_pm10_0_value",
                        "type": "quantitative",
                        "formatType": "number"
                    }
                }
            }
        ],
    })

def show_temp_rh_plots(iqar_dicts):
    
    st.vega_lite_chart({
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "A simple bar chart with embedded data.",

        "title": "Temperatura Ambiente (°C)",
        "width": 900,
        "height": 250,
        "data": {
            "values": iqar_dicts
        },
        "mark": {"type": "line", "line": False, "point": True},
        "encoding": {
            "x": {
                "field": "received_at",
                "type": "nominal",
                "axis": {
                    "labelAngle": 90,
                    "title": "Data"
                    }
                },
            "y": {
                "field": "temp",
                "type": "quantitative",
                "axis": {
                    "title": "°C"
                    },
                "scale": {
                    "domain": [0, 50]
                }
            },
            "color": {"value": "blue"}
        },
        "layer": [
            {"mark": "line"},
            {
                "mark": {
                    "type": "text",
                    "align": "center",
                    "yOffset": -10,
                    "fontSize": 10
                },
                "encoding": {
                    "text": {
                        "field": "temp",
                        "type": "quantitative",
                        "formatType": "number"
                    }
                }
            }
        ],
    })

    st.vega_lite_chart({
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "A simple bar chart with embedded data.",

        "title": "Humidade Relativa Ambiente (%)",
        "width": 900,
        "height": 250,
        "data": {
            "values": iqar_dicts
        },
        "mark": {"type": "line", "line": False, "point": True},
        "encoding": {
            "x": {
                "field": "received_at",
                "type": "nominal",
                "axis": {
                    "labelAngle": 90,
                    "title": "Data"
                    }
                },
            "y": {
                "field": "rh",
                "type": "quantitative",
                "axis": {
                    "title": "%"
                    },
                "scale": {
                    "domain": [0, 100]
                }
            },
            "color": {"value": "blue"}
        },
        "layer": [
            {"mark": "line"},
            {
                "mark": {
                    "type": "text",
                    "align": "center",
                    "yOffset": -10,
                    "fontSize": 10
                },
                "encoding": {
                    "text": {
                        "field": "rh",
                        "type": "quantitative",
                        "formatType": "number"
                    }
                }
            }
        ],
    })

def get_select_df(start_date, stop_date):
    date_start_str = start_date.strftime("%Y-%m-%d")#datetime(2023, 1, 23).strftime("%Y-%m-%d")
    date_stop_str = stop_date.strftime("%Y-%m-%d")#datetime(2023, 1, 30).strftime("%Y-%m-%d")
    con = sqlite3.connect('././data/db.sqlite3')
    select_df = pd.read_sql_query('SELECT * from sample_tb WHERE \''+ date_start_str + ' 00:00\' < ttn_received_at AND ttn_received_at < \'' + date_stop_str + ' 23:59\'', con)
    con.close()    
    return select_df


def show_device_selector():
    return st.selectbox(
        'Dispositivo:',
        (
            'eui-70b3d57ed0059066',
            ''
        )
    )

def show_dates_range_selector():
    return st.date_input(
        "Período:",
        [
            datetime.today() - timedelta(days=7),
            datetime.today()
        ]
    )

def show_presenting_selector():
    return st.selectbox(
        'Apresentação',
        (
            'MP2,5 + MP10 + Ambiente',
            'MP2,5 + Ambiente',
            'MP10 + Ambiente',
            'MP2,5',
            'MP10',
            'Ambiente'
        )
    )



st.set_page_config(
    page_title="SensoAr",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def hide_sandwich_menu():
    st.markdown("""
            <style>
                .block-container {
                        padding-top: 0rem;
                        padding-bottom: 0rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
            </style>
            """, unsafe_allow_html=True)
    hide_menu_style = "<style>#MainMenu {visibility: hidden;} </style>"
    st.markdown(hide_menu_style, unsafe_allow_html=True)

def show_title():
    st.markdown("<h1 style='text-align: center; color: grey; font-size: 2.2em;'>SensorAr</h1>", unsafe_allow_html=True)








hide_sandwich_menu()

show_title()

leftcol, middlecol, rightcol = st.columns([3, 3, 5])

with leftcol:
    device = show_device_selector()

with middlecol:
    dates_range = show_dates_range_selector()

with rightcol:
    presenting = show_presenting_selector()

    
st.markdown('')
st.markdown('')

select_df = pd.DataFrame()

if(len(dates_range) == 2):
    start_date = dates_range[0]
    stop_date = dates_range[1]
    select_df = get_select_df(start_date, stop_date)

iqar_df = get_iqar_df(select_df)
iqar_dicts = iqar_df.to_dict('records')

if('MP2,5' in presenting):
    show_pm2_5_plot(iqar_dicts)

if('MP10' in presenting):
    show_pm10_0_plot(iqar_dicts)

if('Ambiente' in presenting):
    show_temp_rh_plots(iqar_dicts)

#hide_table_row_index = """
#            <style>
#            thead tr th:first-child {display:none}
#            tbody th {display:none}
#            </style>
#            """
#st.markdown(hide_table_row_index, unsafe_allow_html=True)
#st.table(iqar_dicts[['received_at', 'temp', 'rh', 'pm2_5', 'pm10_0']])









