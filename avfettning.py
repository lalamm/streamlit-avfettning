import pandas as pd
import requests
import streamlit as st
from datetime import datetime


def load_data():
    return requests.get("http://worker-rust.ludviglamm-da7.workers.dev/health_data").json()

charts = [
"Weight (kg)",
"Muscle Mass (kg)",
"Hydration (kg)",
"Fat mass Weight (kg)",
"Fat Ratio (%)",
"Fat Free Mass (kg)",
"Muscle Mass (kg)",
"Bone Mass"
]

health_data = load_data()


for chart in charts:
    #Create a series for each user then combine it..
    series = []
    for user,values in health_data.items():
        if chart in values.keys():
            chart_values= values[chart]
            serie = pd.Series([x[1] for x in chart_values],index=[pd.to_datetime(x[0],unit="s") for x in chart_values],name=user)
            #sara fix
            serie = serie.groupby(serie.index.date).min()
            serie.index = pd.to_datetime(serie.index)
            series.append(serie)
    if len(series):
        st.title(chart)
        df = pd.concat(series,axis=1)
        df= df[df.index>"20230731"].ffill()
        st.line_chart(df)
        st.title("Veckofix förändring")
        st.line_chart(df.diff(7))

