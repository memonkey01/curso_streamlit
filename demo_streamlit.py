import streamlit as st
import pandas as pd
import plotly.express as px


#Leer datos
df_origin = pd.read_csv('data/fifa_23_players.csv')

with st.sidebar:
    nationality = st.multiselect('Nacionalidad',sorted(df_origin['Nationality'].unique()))
    team = st.multiselect('Equipo', sorted(df_origin['Club Name'].unique()))
    is_national = st.checkbox('Selección Nacional')

def filter_data(df, nationality, team, is_national):
    df_copy = df.copy()

    if len(nationality) > 0:
        df_copy = df_copy[df_copy['Nationality'].isin(nationality)]
    if len(team) > 0:
        df_copy = df_copy[df_copy['Club Name'].isin(team)]

    if is_national == True:
        df_copy = df_copy[df_copy['National Team Name'] != '-']
    
    return df_copy

df_ = filter_data(df_origin, nationality, team, is_national)
st.title("Fifa 2023")
st.subheader("Análisis de Equipos")

total_jugadores = len(df_)
rating_medio = df_['Overall'].mean()
valor_medio = df_['Value(in Euro)'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("# Jugadores", f"{total_jugadores:,.0f}")
col2.metric("Rating Medio", f"{rating_medio:,.1f}")
col3.metric("Valor $ Medio", f"{valor_medio:,.0f}")



def get_team_statistics(df):
    radar_columns = ['Pace Total','Shooting Total','Passing Total',
                'Dribbling Total','Defending Total','Physicality Total']
    metrics = []
    for metric in radar_columns:
        metrics.append(df_[metric].mean())
    
    return pd.DataFrame(dict(metrics=metrics, theta=radar_columns))

radar_fig = px.line_polar(get_team_statistics(df_), r='metrics', theta='theta', line_close=True)

radar_fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 100]
    )),
  showlegend=False
)
st.plotly_chart(radar_fig)

st.dataframe(df_)
