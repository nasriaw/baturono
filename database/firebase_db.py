import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import os

def initialize_firebase():
    """Menginisialisasi Firebase Admin SDK secara aman (Hybrid Lokal & Cloud)"""
    if not firebase_admin._apps:
        # Cek environment Streamlit Cloud Secrets terlebih dahulu
        if "firebase" in st.secrets and "firebase_db_url" in st.secrets:
            try:
                fb_creds = dict(st.secrets["firebase"])
                # Menangani pemformatan ulang karakter newline (\n) pada private_key di cloud secrets
                if "private_key" in fb_creds:
                    fb_creds["private_key"] = fb_creds["private_key"].replace("\\n", "\n")
                cred = credentials.Certificate(fb_creds)
                database_url = st.secrets["firebase_db_url"]
            except Exception as e:
                st.error(f"Gagal memuat secrets Firebase: {e}")
                st.stop()
        else:
            # Jalur Fallback untuk VSC Lokal
            cred_path = os.path.join("config", "serviceAccountKey.json")
            if not os.path.exists(cred_path):
                st.error("Error: Berkas config/serviceAccountKey.json tidak ditemukan untuk running lokal!")
                st.info("Jika Anda sedang melakukan konfigurasi di cloud, pastikan 'Secrets' sudah terisi.")
                st.stop()
            cred = credentials.Certificate(cred_path)
            # URL default untuk running lokal (Pastikan disesuaikan dengan milik Anda)
            database_url = " https://baturono-app-default-rtdb.asia-southeast1.firebasedatabase.app"#"https://baturono-default-rtdb.firebaseio.com/"
            
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })

def get_db_ref(path):
    """Mendapatkan referensi jalur node Firebase"""
    initialize_firebase()
    return db.reference(path)