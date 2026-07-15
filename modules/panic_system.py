import streamlit as st
import requests
from datetime import datetime
from database.firebase_db import get_db_ref

def send_telegram_alert(message):
    """Mengirim pesan darurat ke Telegram Group bantuorangtua via Bot"""
    if "telegram" in st.secrets:
        bot_token = st.secrets["telegram"]["bot_token"]
        chat_id = st.secrets["telegram"]["group_chat_id"]
    else:
        # Placeholder lokal jika belum setting secrets
        bot_token = "DUMMY_TOKEN"
        chat_id = "DUMMY_CHAT_ID"
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    
    try:
        res = requests.post(url, json=payload, timeout=10)
        return res.status_code == 200
    except Exception:
        return False

def trigger_panic_button(parent_username, lat, lon):
    """Mencatat status incident darurat ke Firebase dan menembakkan alert Telegram"""
    ref = get_db_ref("incidents")
    incident_id = ref.push().key
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    incident_data = {
        "incident_id": incident_id,
        "parent_username": parent_username,
        "latitude": lat,
        "longitude": lon,
        "timestamp": timestamp,
        "status": "OPEN",
        "assigned_volunteer": ""
    }
    ref.child(incident_id).set(incident_data)
    
    # Template pesan untuk grup Telegram bantuorangtua
    msg = (
        f"🚨 *PANIC BUTTON AKTIF! KEDARURATAN LANSIA* 🚨\n\n"
        f"👤 *Nama Orang Tua:* {parent_username}\n"
        f"📅 *Waktu Kejadian:* {timestamp}\n"
        f"📍 *Koordinat GPS:* `{lat}, {lon}`\n"
        f"🗺️ *Rute Google Maps:* https://www.google.com/maps/search/?api=1&query={lat},{lon}\n\n"
        f"Mohon Rekawan terdekat segera menuju ke lokasi!"
    )
    send_telegram_alert(msg)
    return incident_id