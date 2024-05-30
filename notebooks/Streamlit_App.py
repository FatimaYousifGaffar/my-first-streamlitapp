import streamlit as st
import json
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


st.title("Clean energy in Switzerland")
# Data from: https://data.open-power-system-data.org/renewable_power_plants/
clean_energy_ch = pd.read_csv(r"data\raw\renewable_power_plants_CH.csv")
clean_energy_ch.head()
clean_energy_ch.info()
with open(r"data\raw\georef-switzerland-kanton.geojson") as response:
    cantons = json.load(response)

cantons["features"][0]["properties"]
cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais', 
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich', 
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève', 
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz', 
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}

clean_energy_ch["canton_name"] = clean_energy_ch["canton"].map(cantons_dict)
clean_energy_ch.info()
sources_per_canton = clean_energy_ch.groupby("canton_name").size().reset_index(name="count")
sources_per_canton.head()
fig = px.choropleth_mapbox(
    sources_per_canton, 
    color="count",
    geojson=cantons, 
    locations="canton_name", 
    featureidkey="properties.kan_name",
    center={"lat": 46.8, "lon": 8.3},
    mapbox_style="open-street-map", 
    zoom=6.3,
    opacity=0.8,
    width=900,
    height=500,
    labels={"canton_name":"Canton",
           "count":"Number of Sources"},
    title="<b>Number of Clean Energy Sources per Canton</b>",
    color_continuous_scale="Cividis",
)
fig.update_layout(margin={"r":0,"t":35,"l":0,"b":0},
                  font={"family":"Sans",
                       "color":"maroon"},
                  hoverlabel={"bgcolor":"white", 
                              "font_size":12,
                             "font_family":"Sans"},
                  title={"font_size":20,
                        "xanchor":"left", "x":0.01,
                        "yanchor":"bottom", "y":0.95}
                 )
fig.show()
