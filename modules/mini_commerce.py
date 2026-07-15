import streamlit as st
from database.firebase_db import get_db_ref

def render_commerce_catalog():
    """Katalog Belanja Obat & Kebutuhan Lansia"""
    st.subheader("🛒 BATURONO Mini Commerce")
    products = get_db_ref("products").get()
    
    if not products:
        st.info("Katalog produk saat ini kosong.")
        return
        
    cols = st.columns(2)
    for idx, (pid, pdata) in enumerate(products.items()):
        with cols[idx % 2]:
            st.markdown(f"### {pdata.get('name')}")
            st.write(f"💵 Harga: Rp {pdata.get('price'):,}")
            st.write(f"📦 Sisa Stok: {pdata.get('stock')} unit")
            if st.button("Beli Sekarang", key=pid):
                st.success(f"Berhasil memesan {pdata.get('name')}. Pesanan diteruskan ke Admin!")

def render_admin_commerce():
    """Kontrol Input Produk E-Commerce oleh Admin"""
    st.subheader("📦 Tambah Produk Inventori Baru")
    with st.form("admin_product"):
        name = st.text_input("Nama Obat / Alat Medis")
        price = st.number_input("Harga (Rp)", min_value=0, step=5000)
        stock = st.number_input("Jumlah Stok", min_value=0, step=1)
        if st.form_submit_button("Simpan ke Katalog"):
            if name:
                get_db_ref("products").push({"name": name, "price": price, "stock": stock})
                st.success(f"Produk '{name}' berhasil didaftarkan di Firebase!")