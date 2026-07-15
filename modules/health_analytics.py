import streamlit as st
import pandas as pd
from prophet import Prophet
from transformers import pipeline

@st.cache_resource
def load_nlp_model():
    """Load model NLP untuk analisis emosi suara secara efisien (Cache memory)"""
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_voice_transcript(text):
    """Mendeteksi indikator stress/distress dari transkrip ucapan lansia"""
    nlp = load_nlp_model()
    return nlp(text)[0]

def forecast_health_metrics(history_list):
    """Forecasting tren tensi/suhu tubuh masa depan memakai FB Prophet"""
    if len(history_list) < 4:
        return None
    df = pd.DataFrame(history_list)
    
    # Memastikan kolom 'ds' dikonversi menjadi tipe datetime pandas secara eksplisit
    df['ds'] = pd.to_datetime(df['ds'])
    
    model = Prophet(yearly_seasonality=False, daily_seasonality=True)
    model.fit(df)
    
    # Perbaikan: Mengubah 'H' menjadi 'h' (huruf kecil) agar kompatibel dengan pandas versi baru
    future = model.make_future_dataframe(periods=3, freq='h')
    
    forecast = model.predict(future)
    return forecast[['ds', 'yhat']].tail(3)
