import streamlit as st
from PIL import Image
import pandas as pd
from pytube import YouTube
import os


def download_audio(url):
    """
    Flow para descargar audio y mostrar proceso
    """
    # url input from user
    yt = YouTube(url)
    st.write(f'Leyendo URL {url}')
    st.write(yt.title)
    # extract only audio
    audio = yt.streams.filter(only_audio=True).first()
    st.write('Extrayendo Audio')
    # download the file
    out_file = audio.download(output_path='./downloads/')
    st.write('Descarga Completa')
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    try:
        os.rename(out_file, new_file)
        st.write(f'Arhivo Descargado en {new_file}')
        st.write('-----------------')
    except:
        st.write('Archivo ya existe')
        st.write('-----------------')
    return None

def download_video(url):
    """
    Flow para descargar video y mostrar proceso
    """
    # url input from user
    yt = YouTube(url)
    st.write(f'Leyendo URL {url}')
    st.write(yt.title)
 
    video = yt.streams.filter(file_extension='mp4').get_highest_resolution() 
    st.write('Extrayendo Video')

    # download the file
    out_file = video.download(output_path = './downloads/') 
    st.write('Descarga Completa')
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp4'
    try:
        os.rename(out_file, new_file)
        st.write(f'Arhivo Descargado en {new_file}')
        st.write('-----------------')
    except:
        st.write('Archivo ya existe')
        st.write('-----------------')
    return None


###########################
#### LAYOUT - Sidebar
###########################

logo_pypro = Image.open('assets/pypro_logo_plot.png')
with st.sidebar:
    st.image(logo_pypro)
    type = st.selectbox('Tipo de Descarga',['-','audio','video'])
    file_path = st.file_uploader("Archivo con URLs")


st.title('Descarga de Youtube')


if file_path:
    df = pd.read_excel(file_path)
else:
    st.warning('Selecciona un archivo con URLs válidas.', icon="⚠️")

if 'df' in locals():
    st.header('Arhivo a Descargar')
    st.dataframe(df)

if type == 'audio' and 'df' in locals():
    st.header('Status Descarga')
    with st.expander("Detalle de Descarga"):
        for idx, row in df.iterrows():
            download_audio(row['url'])

elif type == 'video' and 'df' in locals():
    st.header('Status Descarga')
    with st.expander("Detalle de Descarga"):
        for idx, row in df.iterrows():
            download_video(row['url'])

else:
    st.warning('Selecciona el tipo de descarga.', icon="⚠️")