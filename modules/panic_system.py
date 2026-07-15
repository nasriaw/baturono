import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo # Modul bawaan untuk mengatur zona waktu
from database.firebase_db import get_db_ref

def send_telegram_alert(message):
    """Mengirim pesan darurat ke Telegram Group bantuorangtua via Bot"""
    if "telegram" in st.secrets:
        bot_token = st.secrets["telegram"]["TELEGRAM_BOT_TOKEN"]
        chat_id = st.secrets["telegram"]["GROUP_CHAT_ID"]
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
    """Mencatat status incident darurat ke Firebase, update lokasi user, dan kirim alert Telegram"""
    # 1. Update koordinat terbaru orang tua di node /users agar terbaca di peta anak/admin
    user_ref = get_db_ref(f"users/{parent_username}")
    user_ref.update({
        "latitude": lat,
        "longitude": lon
    })

    # 2. Catat laporan insiden baru
    ref = get_db_ref("incidents")
    incident_id = ref.push().key
    # PERBAIKAN: Memaksa server menggunakan zona waktu WIB (GMT+7)
    tz_wib = ZoneInfo("Asia/Jakarta")
    timestamp = datetime.now(tz_wib).strftime("%Y-%m-%d %H:%M:%S")
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
    
    # 3. Template kirim pesan ke Telegram Group
    msg = (
        f"🚨 *PANIC BUTTON AKTIF! KEDARURATAN LANSIA* 🚨\n\n"
        f"👤 *Nama Orang Tua:* {parent_username}\n"
        f"📅 *Waktu Kejadian:* {timestamp}\n"
        f"📍 *Koordinat GPS:* `{lat}, {lon}`\n"
        f"🗺️ *Rute Google Maps:* https://www.google.com/maps/search/?api=1&query={lat},{lon}\n\n"
        f"Mohon Relawan terdekat segera menuju ke lokasi!"
    )
    send_telegram_alert(msg)
    return incident_id
