import streamlit as st
from database.firebase_db import get_db_ref

def login_user(username, password):
    """Validasi password berdasarkan username di node /users"""
    ref = get_db_ref(f"users/{username}")
    user_data = ref.get()
    if user_data and str(user_data.get("password")) == str(password):
        return user_data
    return None

def render_login_page():
    """Tampilan Form Login Utama"""
    st.markdown("<h2 style='text-align: center; color: #c53030;'>🚨 Login Sistem BATURONO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4a5568;'>Sistem Kedaruratan & Pemantauan Lansia Terintegrasi</p>", unsafe_allow_html=True)
    
    with st.form("login_container"):
        username = st.text_input("Username / ID Pengguna")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Masuk Aplikasi", use_container_width=True)
        
        if submitted:
            if not username or not password:
                st.warning("Mohon isi username dan password terlebih dahulu.")
                return
            
            user_info = login_user(username, password)
            if user_info:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["role"] = user_info.get("role")
                st.session_state["fullname"] = user_info.get("fullname")
                st.success(f"Login Berhasil! Selamat datang {user_info.get('fullname')}")
                st.rerun()
            else:
                st.error("Maaf, Username atau Password salah!")