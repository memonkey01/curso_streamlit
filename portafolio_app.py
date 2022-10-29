import streamlit as st
import pandas as pd
import pandas_datareader.data as web
import datetime
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib as mpl
import mplcyberpunk
import numpy as np
from prophet import Prophet


plt.style.use("dark_background")
###########################
#### Funciones Principales
###########################

def get_data(stock, start_time, end_time):
    df = web.DataReader(stock, 'yahoo', start=start_time, end=end_time)
    return df

def plot_close_price(data):
    background = plt.imread('assets/logo_source.png')
    logo = plt.imread('assets/pypro_logo_plot.png')
    font = {'family': 'sans-serif',
        'color':  'white',
        'weight': 'normal',
        'size': 16,
        }

    font_sub = {'family': 'sans-serif',
        'color':  'white',
        'weight': 'normal',
        'size': 10,
        }


    fig = plt.figure(figsize=(10,6))
    plt.plot(data.index, data.Close, color='dodgerblue', linewidth=1)
    mplcyberpunk.add_glow_effects()
    plt.ylabel('Precio USD')
    plt.xticks(rotation=45,  ha='right')
    ax = plt.gca()
    #ax.figure.figimage(logo,  10, 1000, alpha=.99, zorder=1)
    ax.figure.figimage(background, 40, 40, alpha=.15, zorder=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.grid(True,color='gray', linestyle='-', linewidth=0.2)
    return fig

def daily_returns(df):
    df = df.sort_index(ascending=True)
    df['returns'] = np.log(df['Close']).diff()
    return df

def returns_vol(df):
    df['volatility'] = df.returns.rolling(12).std()
    return df

def plot_volatility(df_vol):
    background = plt.imread('assets/logo_source.png')
    logo = plt.imread('assets/pypro_logo_plot.png')
    font = {'family': 'sans-serif',
            'color':  'white',
            'weight': 'normal',
            'size': 16,
            }

    font_sub = {'family': 'sans-serif',
            'color':  'white',
            'weight': 'normal',
            'size': 10,
            }


    df_plot = df_vol.copy()
    fig = plt.figure(figsize=(10,6))
    plt.plot(df_plot.index, df_plot.returns, color='dodgerblue', linewidth=0.5)
    plt.plot(df_plot.index, df_plot.volatility, color='darkorange', linewidth=1)
    mplcyberpunk.add_glow_effects()
    plt.ylabel('% Porcentaje')
    plt.xticks(rotation=45,  ha='right')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.3f}'))
    #ax.figure.figimage(logo,  10, 1000, alpha=.99, zorder=1)
    ax.figure.figimage(background, 40, 40, alpha=.15, zorder=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.grid(True,color='gray', linestyle='-', linewidth=0.2)
    plt.legend(('Retornos Diarios', 'Volatilidad Móvil'), frameon=False)
    return fig


def plot_prophet(data, forecast):
    data_prophet = data.reset_index().copy()
    data_prophet.rename(columns={'Date':'ds','Close':'y'}, inplace=True)

    m = Prophet()
    m.fit(data_prophet[['ds','y']])

    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    fig1 = m.plot(forecast)
    background = plt.imread('assets/logo_source.png')
    mplcyberpunk.add_glow_effects()
    ax = plt.gca()
    ax.figure.figimage(background, 40, 40, alpha=.15, zorder=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.grid(True,color='gray', linestyle='-', linewidth=0.4)
    plt.xticks(rotation=45,  ha='right')
    plt.ylabel('Precio de Cierre')
    return fig1


###########################
#### LAYOUT - Sidebar
###########################

logo_pypro = Image.open('assets/pypro_logo_plot.png')
with st.sidebar:
    st.image(logo_pypro)
    stock = st.selectbox('Ticker', ['NVDA','TSLA','MSFT','AMZN','INTC','AMD','JNJ','BABA','GOOGL'], index=1)
    start_time = st.date_input(
                    "Fecha de Inicio",
                    datetime.date(2019, 7, 6))
    end_time = st.date_input(
                    "Fecha Final",
                    datetime.date(2022, 10, 6))


###########################
#### DATA - Funciones sobre inputs
###########################

data = get_data(stock, start_time.strftime("%Y-%m-%d"), end_time.strftime("%Y-%m-%d"))
plot_price = plot_close_price(data)

df_ret = daily_returns(data)
df_vol = returns_vol(df_ret)
plot_vol = plot_volatility(df_vol)
plot_forecast = plot_prophet(data, 1)


###########################
#### LAYOUT - Render Final
###########################

st.title("Análisis de Acciones")

st.subheader('Precio de Cierre')
st.pyplot(plot_price)

st.subheader('Forecast a un Año')
st.pyplot(plot_forecast)

st.subheader('Retornos Diarios')
st.pyplot(plot_vol)

st.dataframe(data)



