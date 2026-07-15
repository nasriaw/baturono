import streamlit as st
from modules.auth import render_login_page
from modules.panic_system import trigger_panic_button
from modules.dashboard_admin import render_geospatial_monitor, get_closest_volunteer
from modules.health_analytics import analyze_voice_transcript, forecast_health_metrics
from modules.mini_commerce import render_commerce_catalog, render_admin_commerce
from modules.reminders import render_reminder_manager
from streamlit_geolocation import streamlit_geolocation
import pandas as pd

st.set_page_config(page_title="BATURONO App", page_icon="🚨", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    render_login_page()
else:
    st.sidebar.title(f"👤 {st.session_state['fullname']}")
    st.sidebar.write(f"Hak Akses: **{st.session_state['role'].upper()}**")
    if st.sidebar.button("🚪 Keluar Sistem"):
        st.session_state["authenticated"] = False
        st.rerun()
        
    role = st.session_state["role"]
    
    # 1. HALAMAN ORANG TUA
    if role == "orang_tua":
        st.markdown("<h1 style='color:red;'>🚨 PUSAT DARURAT BATURONO</h1>", unsafe_allow_html=True)
        st.write("Jika Anda membutuhkan bantuan mendadak, silakan klik tombol merah besar di bawah:")
        
        # Geolocation tracker
        loc = streamlit_geolocation()
        lat = loc.get("latitude") if loc.get("latitude") else -7.9839
        lon = loc.get("longitude") if loc.get("longitude") else 112.6214
        
        if st.button("🔴 AKTIFKAN PANIC BUTTON", use_container_width=True, type="primary"):
            inc_id = trigger_panic_button(st.session_state["username"], lat, lon)
            st.error(f"⚠️ Alergi kedaruratan terkirim ke Telegram Group! (ID Insiden: {inc_id})")
            
        render_reminder_manager(st.session_state["username"])
        
        st.markdown("---")
        st.subheader("🎙️ Deteksi Kesehatan Psikologis Suara Lansia (AI NLP)")
        txt_input = st.text_area("Ketik transkrip suara di sini (Bahasa Inggris):", "I am feeling very anxious and dizzy right now.")
        if st.button("Analisis Tingkat Distress"):
            res = analyze_voice_transcript(txt_input)
            st.info(f"Kondisi Emosi: **{res['label']}** (Tingkat Keyakinan: {res['score']:.2%})")

    # 2. HALAMAN ANAK
    elif role == "anak":
        st.title("👨‍👩‍👦 Portal Pengawasan Anak")
        render_geospatial_monitor()
        render_commerce_catalog()

    # 3. HALAMAN RELAWAN
    elif role == "relawan":
        st.title("🤝 Komunitas Relawan - Grup bantuorangtua")
        render_geospatial_monitor()

    # 4. HALAMAN ADMIN
    elif role == "admin":
        st.title("🛡️ Dashboard Central Admin - M. Nasri AW")
        t1, t2, t3 = st.tabs(["Peta Monitoring Spasial", "Manajemen Mini Commerce", "AI Early Warning System"])
        
        with t1:
            render_geospatial_monitor()
        with t2:
            render_admin_commerce()
        with t3:
            st.subheader("📈 Peramalan Kesehatan Lansia (Prophet)")
            dummy_history = [
                {'ds': '2026-07-14 08:00:00', 'y': 120},
                {'ds': '2026-07-14 09:00:00', 'y': 125},
                {'ds': '2026-07-14 10:00:00', 'y': 130},
                {'ds': '2026-07-14 11:00:00', 'y': 142}
            ]
            if st.button("Hitung Prediksi Tren Tensi"):
                fc = forecast_health_metrics(dummy_history)
                if fc is not None:
                    st.dataframe(fc)
                    st.line_chart(fc.set_index('ds'))
