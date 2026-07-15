import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
from database.firebase_db import get_db_ref

def render_geospatial_monitor():
    """Merender Peta Spasial Real-time Lansia dan Relawan di Malang Raya"""
    st.subheader("🗺️ Real-Time Geospatial Monitor")
    
    users_data = get_db_ref("users").get()
    incidents_data = get_db_ref("incidents").get()
    
    # Fokus koordinat awal di Malang Raya
    m = folium.Map(location=[-7.9839, 112.6214], zoom_start=12)
    
    # Plot Posisi User Aktif
    if users_data:
        for val in users_data.values():
            if "latitude" in val and "longitude" in val:
                role = val.get("role")
                color = "blue" if role == "orang_tua" else "green"
                folium.Marker(
                    location=[val["latitude"], val["longitude"]],
                    popup=f"{val.get('fullname')} ({role})",
                    icon=folium.Icon(color=color, icon="user")
                ).add_to(m)
                
    # Plot Insiden Darurat Aktif (Red Marker)
    if incidents_data:
        for inc in incidents_data.values():
            if inc.get("status") == "OPEN":
                folium.Marker(
                    location=[inc["latitude"], inc["longitude"]],
                    popup=f"⚠️ DARURAT: {inc['parent_username']}",
                    icon=folium.Icon(color="red", icon="exclamation-sign")
                ).add_to(m)
                
    folium_static(m)

def get_closest_volunteer(p_lat, p_lon):
    """Mencari nama relawan dengan jarak terdekat dari lokasi lansia"""
    users = get_db_ref("users").get()
    closest_name = "Tidak Ada"
    min_dist = float('inf')
    
    if users:
        for val in users.values():
            if val.get("role") == "relawan" and "latitude" in val:
                dist = geodesic((p_lat, p_lon), (val["latitude"], val["longitude"])).km
                if dist < min_dist:
                    min_dist = dist
                    closest_name = val.get("fullname")
    return closest_name, min_dist