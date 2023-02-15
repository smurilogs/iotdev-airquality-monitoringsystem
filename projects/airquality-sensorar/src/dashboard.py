

import pandas as pd
import numpy as np
import streamlit as st
import datetime
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="SensoAr",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

hide_menu_style = "<style>#MainMenu {visibility: hidden;} </style>"
st.markdown(hide_menu_style, unsafe_allow_html=True)

leftcol, rightcol = st.columns([4, 1])

with leftcol:
    st.markdown("<h1 style='text-align: center; color: grey;'>SensorAr</h1>", unsafe_allow_html=True)

select_str = 'Último Dia'
with rightcol:
    select_str = st.selectbox('Período:', ['Último Dia', 'Última Semana', 'Último Mês', 'Útimo Ano'])

st.markdown("***")

registers = [
        {"data/hora": "2023-01-01 00:00", "IQAr": 0,"cor": "red" }, {"data/hora": "2023-01-07 00:00", "IQAr": 55,"cor": "red" }, {"data/hora": "2023-01-13 00:00", "IQAr": 43, "cor": "red" },
        {"data/hora": "2023-01-02 00:00", "IQAr": 91,"cor": "red" }, {"data/hora": "2023-01-08 00:00", "IQAr": 81,"cor": "red" }, {"data/hora": "2023-01-14 00:00", "IQAr": 53, "cor": "red" },
        {"data/hora": "2023-01-03 00:00", "IQAr": 19,"cor": "red" }, {"data/hora": "2023-01-09 00:00", "IQAr": 87,"cor": "red" }, {"data/hora": "2023-01-15 00:00", "IQAr": 52, "cor": "red" },
        {"data/hora": "2023-01-04 00:00", "IQAr": 28,"cor": "red" }, {"data/hora": "2023-01-10 00:00", "IQAr": 55,"cor": "red" }, {"data/hora": "2023-01-16 00:00", "IQAr": 43, "cor": "red" },
        {"data/hora": "2023-01-05 00:00", "IQAr": 91,"cor": "red" }, {"data/hora": "2023-01-11 00:00", "IQAr": 81,"cor": "red" }, {"data/hora": "2023-01-17 00:00", "IQAr": 53, "cor": "red" },
        {"data/hora": "2023-01-06 00:00", "IQAr": 19,"cor": "green" }, {"data/hora": "2023-01-12 00:00", "IQAr": 87,"cor": "red" }, {"data/hora": "2023-01-18 00:00", "IQAr": 52, "cor": "red" }
    ]

if(select_str != 'Último Dia'):
    registers = [
        {"data/hora": "2023-01-01 00:00", "IQAr": 28,"cor": "red" }, {"data/hora": "2023-01-07 00:00", "IQAr": 55,"cor": "red" }, {"data/hora": "2023-01-13 00:00", "IQAr": 43, "cor": "red" },
        {"data/hora": "2023-01-02 00:00", "IQAr": 91,"cor": "red" }, {"data/hora": "2023-01-08 00:00", "IQAr": 81,"cor": "red" }, {"data/hora": "2023-01-14 00:00", "IQAr": 53, "cor": "red" },
        {"data/hora": "2023-01-03 00:00", "IQAr": 19,"cor": "red" }, {"data/hora": "2023-01-09 00:00", "IQAr": 87,"cor": "red" }, {"data/hora": "2023-01-15 00:00", "IQAr": 52, "cor": "red" },
        {"data/hora": "2023-01-04 00:00", "IQAr": 28,"cor": "red" }, {"data/hora": "2023-01-10 00:00", "IQAr": 55,"cor": "red" }, {"data/hora": "2023-01-16 00:00", "IQAr": 43, "cor": "red" },
        {"data/hora": "2023-01-05 00:00", "IQAr": 91,"cor": "red" }, {"data/hora": "2023-01-11 00:00", "IQAr": 81,"cor": "red" }, {"data/hora": "2023-01-17 00:00", "IQAr": 53, "cor": "red" },
        {"data/hora": "2023-01-06 00:00", "IQAr": 19,"cor": "green" }, {"data/hora": "2023-01-12 00:00", "IQAr": 87,"cor": "red" }, {"data/hora": "2023-01-18 00:00", "IQAr": 52, "cor": "red" }
    ]
    
st.vega_lite_chart({
"$schema": "https://vega.github.io/schema/vega-lite/v5.json",
"description": "A simple bar chart with embedded data.",

    "title": "Concentração de MP2,5",
    "width": 1000,
    "height": 250,
    "data": {
        "values": date_dicts
    },
    "mark": {"type": "bar", "line": False, "point": True},
    "encoding": {
        "x": {"field": "data/hora", "type": "nominal", "axis": {"labelAngle": 60}},
        "y": {"field": "IQAr", "type": "quantitative"},
        "color": {
            "field": "cor",
            "type": "nominal",
            "scale": None
        }
    }  
})


st.vega_lite_chart({
"$schema": "https://vega.github.io/schema/vega-lite/v5.json",
"description": "A simple bar chart with embedded data.",

    "title": "Concentração de MP10",
    "width": 1000,
    "height": 250,
    "data": {
        "values": [
        {"data/hora": "2023-01-01 00:00", "IQAr": 28,"cor": "red" }, {"data/hora": "2023-01-07", "IQAr": 55,"cor": "red" }, {"data/hora": "2023-01-13", "IQAr": 43, "cor": "red" },
        {"data/hora": "2023-01-02", "IQAr": 91,"cor": "red" }, {"data/hora": "2023-01-08", "IQAr": 81,"cor": "red" }, {"data/hora": "2023-01-14", "IQAr": 53, "cor": "red" },
        {"data/hora": "2023-01-03", "IQAr": 19,"cor": "red" }, {"data/hora": "2023-01-09", "IQAr": 87,"cor": "red" }, {"data/hora": "2023-01-15", "IQAr": 52, "cor": "red" },
        {"data/hora": "2023-01-04", "IQAr": 28,"cor": "red" }, {"data/hora": "2023-01-10", "IQAr": 55,"cor": "red" }, {"data/hora": "2023-01-16", "IQAr": 43, "cor": "red" },
        {"data/hora": "2023-01-05", "IQAr": 91,"cor": "red" }, {"data/hora": "2023-01-11", "IQAr": 81,"cor": "red" }, {"data/hora": "2023-01-17", "IQAr": 53, "cor": "red" },
        {"data/hora": "2023-01-06", "IQAr": 19,"cor": "green" }, {"data/hora": "2023-01-12", "IQAr": 87,"cor": "red" }, {"data/hora": "2023-01-18", "IQAr": 52, "cor": "red" }
        ]
    },
    "mark": {"type": "line", "line": True, "point": True},
    "encoding": {
        "x": {"field": "data/hora", "type": "nominal", "axis": {"labelAngle": 60}},
        "y": {"field": "IQAr", "type": "quantitative"},
        "color": {
            "field": "cor",
            "type": "nominal",
            "scale": None
        }
    }  
})

st.vega_lite_chart({
"$schema": "https://vega.github.io/schema/vega-lite/v5.json",
"description": "A simple bar chart with embedded data.",

    "title": "Concentração de MP10",
    "width": 1000,
    "height": 250,
    "data": {
        "values": [
        {"data/hora": "2023-01-01 00:00", "IQAr": 28,"cor": "red" }, {"data/hora": "2023-01-07", "IQAr": 55,"cor": "red" }, {"data/hora": "2023-01-13", "IQAr": 43, "cor": "red" },
        {"data/hora": "2023-01-02", "IQAr": 91,"cor": "red" }, {"data/hora": "2023-01-08", "IQAr": 81,"cor": "red" }, {"data/hora": "2023-01-14", "IQAr": 53, "cor": "red" },
        {"data/hora": "2023-01-03", "IQAr": 19,"cor": "red" }, {"data/hora": "2023-01-09", "IQAr": 87,"cor": "red" }, {"data/hora": "2023-01-15", "IQAr": 52, "cor": "red" },
        {"data/hora": "2023-01-04", "IQAr": 28,"cor": "red" }, {"data/hora": "2023-01-10", "IQAr": 55,"cor": "red" }, {"data/hora": "2023-01-16", "IQAr": 43, "cor": "red" },
        {"data/hora": "2023-01-05", "IQAr": 91,"cor": "red" }, {"data/hora": "2023-01-11", "IQAr": 81,"cor": "red" }, {"data/hora": "2023-01-17", "IQAr": 53, "cor": "red" },
        {"data/hora": "2023-01-06", "IQAr": 19,"cor": "green" }, {"data/hora": "2023-01-12", "IQAr": 87,"cor": "red" }, {"data/hora": "2023-01-18", "IQAr": 52, "cor": "red" }
        ]
    },
    "mark": {"type": "line", "line": True, "point": True},
    "encoding": {
        "x": {"field": "data/hora", "type": "nominal", "axis": {"labelAngle": 60}},
        "y": {"field": "IQAr", "type": "quantitative"},
        "color": {
            "field": "cor",
            "type": "nominal",
            "scale": None
        }
    }  
})


#chart_data = pd.DataFrame(
#    np.random.randn(20, 3),
#    columns=["data/hora", "IQAr", "c"])
#st.bar_chart(chart_data)