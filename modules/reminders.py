import streamlit as st
from database.firebase_db import get_db_ref

def render_reminder_manager(username):
    """Mengelola jadwal makan & minum obat lansia"""
    st.subheader("⏰ Pengingat Obat & Makan Mandiri")
    ref = get_db_ref(f"reminders/{username}")
    
    with st.expander("➕ Tambah Jadwal Pengingat Baru"):
        task = st.text_input("Nama Aktivitas (Misal: Minum Obat Tensi)")
        time_str = st.text_input("Waktu/Jam (Misal: 07:00 WIB)")
        if st.button("Simpan Pengingat"):
            if task and time_str:
                ref.push({"task": task, "time": time_str, "status": "Belum"})
                st.success("Jadwal sukses ditambahkan!")
                st.rerun()

    reminders = ref.get()
    if reminders:
        for rid, rdata in reminders.items():
            st.markdown(f"🔔 *[{rdata['time']}]* **{rdata['task']}** (Status: {rdata['status']})")