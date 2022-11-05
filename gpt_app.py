import streamlit as st
from PIL import Image
import torch
from transformers import pipeline
device = "cuda:0" if torch.cuda.is_available() else "cpu"

###########################
#### CREAR Singletons
###########################

@st.experimental_singleton
def model_generator():
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M', device=0)
    return generator

@st.experimental_singleton
def model_translator_en_es():
    translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")
    return translator

@st.experimental_singleton
def model_translator_es_en():
    translator = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")
    return translator

@st.experimental_singleton
def model_sentiment():
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    return classifier

generator = model_generator()
translator_en_es = model_translator_en_es()
translator_es_en = model_translator_es_en()
sentiment = model_sentiment()

###########################
#### LAYOUT - Sidebar
###########################

logo_pypro = Image.open('assets/pypro_logo_plot.png')
with st.sidebar:
    st.image(logo_pypro)

st.title('GPT Neo y Análisis de Sentimiento')

# Input de texto traducido al español
prompt_es = st.text_area('Texto a Generar', 'Insertar texto aqui')
prompt_en = translator_es_en(prompt_es)


# Generar texto con el prompt en ingles
results = generator(prompt_en[0]['translation_text'], do_sample=True, max_length=256, temperature=0.95)
gen_text_en = results[0]['generated_text']


# Traducir el texto generado a español
gen_text_es = translator_en_es(gen_text_en)
st.write('Texto generado:', gen_text_es[0]['translation_text'])

# Aplicar Sentiment Analysis a el texto generado en ingles
sentiment_en = sentiment(gen_text_en)
st.write(sentiment_en)