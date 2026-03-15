
# import streamlit as st
# import pandas as pd
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium
# from math import radians, cos, sin, sqrt, atan2

# CSV_PATH = "database/reports.csv"


# # ─────────────────────
# # Distance Function
# # ─────────────────────
# def calculate_distance(lat1, lon1, lat2, lon2):

#     R = 6373.0

#     lat1 = radians(lat1)
#     lon1 = radians(lon1)
#     lat2 = radians(lat2)
#     lon2 = radians(lon2)

#     dlon = lon2 - lon1
#     dlat = lat2 - lat1

#     a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1-a))

#     return round(R*c,2)


# # ─────────────────────
# # Admin Page
# # ─────────────────────
# def show():

#     st.title("♻ Waste Monitoring Admin")

#     # Start Location Button
#     start_tracking = st.button("📍 Start Admin Location")

#     if start_tracking:
#         st.success("Admin location tracking started")

#     # Load Data
#     try:
#         data = pd.read_csv(CSV_PATH)
#     except:
#         st.warning("No reports found")
#         return

#     if data.empty:
#         st.info("No waste reports yet")
#         return

#     # Dashboard
#     col1,col2,col3 = st.columns(3)

#     col1.metric("Total Reports",len(data))
#     col2.metric("High Waste",len(data[data["waste_percent"]>80]))
#     col3.metric("Average Waste",round(data["waste_percent"].mean(),1))


#     # ─────────────────────
#     # Google Style Map
#     # ─────────────────────

#     st.subheader("Waste Location Map")

#     m = folium.Map(
#         location=[23.2599,77.4126],
#         zoom_start=5,
#         tiles="OpenStreetMap"
#     )

#     marker_cluster = MarkerCluster().add_to(m)

#     # Waste markers
#     for i in range(len(data)):

#         lat = data.iloc[i]["lat"]
#         lon = data.iloc[i]["lon"]
#         waste = data.iloc[i]["waste_percent"]

#         if waste > 80:
#             color="red"
#         elif waste > 50:
#             color="orange"
#         else:
#             color="green"

#         folium.Marker(
#             [lat,lon],
#             popup=f"Waste Level: {waste}%",
#             icon=folium.Icon(color=color,icon="trash")
#         ).add_to(marker_cluster)

#     st_folium(m,width=1000,height=550)


#     # ─────────────────────
#     # Waste Table
#     # ─────────────────────

#     st.subheader("Waste Reports")

#     st.dataframe(data,use_container_width=True)


#     # Download
#     csv=data.to_csv(index=False).encode("utf-8")

#     st.download_button(
#         "Download CSV",
#         csv,
#         "waste_reports.csv",
#         "text/csv"
#     )
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from math import radians, cos, sin, sqrt, atan2

CSV_PATH = "database/reports.csv"

# ─────────────────────────────────────────────────────────────
# Google Maps Style CSS
# ─────────────────────────────────────────────────────────────
GOOGLE_MAPS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500&display=swap');

[data-testid="stAppViewContainer"] { background: #f1f3f4; font-family: 'Roboto', sans-serif; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.gmap-topbar {
    position: sticky; top: 0; z-index: 999;
    background: #fff;
    box-shadow: 0 2px 6px rgba(0,0,0,0.18);
    display: flex; align-items: center; gap: 16px;
    padding: 10px 20px; height: 64px;
}
.gmap-logo {
    font-family: 'Google Sans', sans-serif; font-size: 22px; font-weight: 700;
    color: #4285F4; letter-spacing: -0.5px; white-space: nowrap;
}
.gmap-logo span:nth-child(1) { color: #34A853; }
.gmap-logo span:nth-child(2) { color: #FBBC04; }
.gmap-logo span:nth-child(3) { color: #EA4335; }
.gmap-logo span:nth-child(4) { color: #4285F4; }

.gmap-searchbar {
    flex: 1; max-width: 520px; background: #f1f3f4; border-radius: 24px;
    display: flex; align-items: center; padding: 0 16px; height: 44px; gap: 10px;
    transition: box-shadow 0.2s;
}
.gmap-searchbar:hover { box-shadow: 0 1px 6px rgba(0,0,0,0.2); background: #fff; }
.gmap-searchbar input {
    border: none; background: transparent; outline: none;
    font-family: 'Roboto', sans-serif; font-size: 16px; color: #202124; width: 100%;
}
.gmap-searchbar input::placeholder { color: #9aa0a6; }
.gmap-avatar {
    width: 36px; height: 36px; background: #4285F4; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-family: 'Google Sans', sans-serif; font-weight: 500; font-size: 15px;
    margin-left: auto; cursor: pointer;
}

.gmap-sidebar-header { padding: 20px 20px 10px; border-bottom: 1px solid #e8eaed; }
.gmap-sidebar-title { font-family: 'Google Sans', sans-serif; font-size: 20px; font-weight: 700; color: #202124; margin: 0 0 4px; }
.gmap-sidebar-sub { font-size: 13px; color: #5f6368; }

.gmap-chips { display: flex; gap: 8px; padding: 14px 20px; border-bottom: 1px solid #e8eaed; flex-wrap: wrap; }
.gmap-chip {
    display: flex; align-items: center; gap: 6px;
    background: #f1f3f4; border-radius: 20px; padding: 6px 14px;
    font-size: 13px; font-weight: 500; color: #202124; white-space: nowrap;
}
.gmap-chip .dot { width: 10px; height: 10px; border-radius: 50%; }

.gmap-tabs { display: flex; padding: 0 20px; border-bottom: 1px solid #e8eaed; overflow-x: auto; }
.gmap-tab {
    padding: 12px 16px; font-size: 14px; font-weight: 500; color: #5f6368;
    cursor: pointer; border-bottom: 3px solid transparent; white-space: nowrap;
}
.gmap-tab.active { color: #1a73e8; border-bottom-color: #1a73e8; }

.gmap-list { padding: 8px 0; }
.gmap-report-item {
    display: flex; align-items: center; gap: 14px; padding: 12px 20px;
    cursor: pointer; border-bottom: 1px solid #f1f3f4; transition: background 0.15s;
}
.gmap-report-item:hover { background: #f8f9fa; }
.gmap-report-icon { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.gmap-report-info { flex: 1; min-width: 0; }
.gmap-report-name { font-size: 14px; font-weight: 500; color: #202124; margin-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.gmap-report-meta { font-size: 12px; color: #5f6368; }
.gmap-report-badge { font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 12px; white-space: nowrap; }

[data-testid="stDownloadButton"] > button {
    background: #1a73e8 !important; color: #fff !important; border: none !important;
    border-radius: 4px !important; font-family: 'Google Sans', sans-serif !important; font-size: 14px !important;
}
</style>
"""

def waste_color_hex(w):
    return "#ea4335" if w > 80 else ("#fbbc04" if w > 50 else "#34a853")

def waste_folium_color(w):
    return "red" if w > 80 else ("orange" if w > 50 else "green")

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1, lon1, lat2, lon2 = radians(lat1), radians(lon1), radians(lat2), radians(lon2)
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return round(R * 2 * atan2(sqrt(a), sqrt(1-a)), 2)


def show():
    st.set_page_config(layout="wide", page_title="Waste Maps", page_icon="♻")
    st.markdown(GOOGLE_MAPS_CSS, unsafe_allow_html=True)

    try:
        data = pd.read_csv(CSV_PATH)
    except Exception:
        data = pd.DataFrame(columns=["lat","lon","waste_percent"])

    total      = len(data)
    high_waste = len(data[data["waste_percent"] > 80])   if not data.empty else 0
    med_waste  = len(data[(data["waste_percent"] > 50) & (data["waste_percent"] <= 80)]) if not data.empty else 0
    low_waste  = total - high_waste - med_waste

    # ── Topbar ──
    st.markdown("""
    <div class="gmap-topbar">
        <div class="gmap-logo">W<span>a</span><span>s</span><span>t</span><span>e</span> Maps</div>
        <div class="gmap-searchbar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="2.2">
                <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input type="text" placeholder="Search waste reports, locations..." />
        </div>
        <div class="gmap-avatar">A</div>
    </div>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns([36, 64], gap="small")

    # ── Sidebar ──
    with left_col:
        st.markdown("""
        <div class="gmap-sidebar-header">
            <div class="gmap-sidebar-title">♻ Waste Monitor</div>
            <div class="gmap-sidebar-sub">Real-time waste level tracking across India</div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="gmap-chips">
            <div class="gmap-chip"><div class="dot" style="background:#4285f4"></div>{total} Total</div>
            <div class="gmap-chip"><div class="dot" style="background:#ea4335"></div>{high_waste} High</div>
            <div class="gmap-chip"><div class="dot" style="background:#fbbc04"></div>{med_waste} Med</div>
            <div class="gmap-chip"><div class="dot" style="background:#34a853"></div>{low_waste} Low</div>
        </div>
        <div class="gmap-tabs">
            <div class="gmap-tab active">All Reports</div>
            <div class="gmap-tab">🔴 Critical</div>
            <div class="gmap-tab">🟡 Medium</div>
            <div class="gmap-tab">🟢 Clean</div>
        </div>""", unsafe_allow_html=True)

        if data.empty:
            st.info("No waste reports yet.")
        else:
            list_html = '<div class="gmap-list">'
            for i, row in data.iterrows():
                w   = row["waste_percent"]
                clr = waste_color_hex(w)
                bg  = clr + "18"
                label = "High" if w > 80 else ("Medium" if w > 50 else "Low")
                list_html += f"""
                <div class="gmap-report-item">
                    <div class="gmap-report-icon" style="background:{bg}">🗑️</div>
                    <div class="gmap-report-info">
                        <div class="gmap-report-name">Report #{i+1}</div>
                        <div class="gmap-report-meta">{row['lat']:.4f}°N, {row['lon']:.4f}°E</div>
                    </div>
                    <span class="gmap-report-badge" style="color:{clr};background:{clr}18">{w}% {label}</span>
                </div>"""
            list_html += "</div>"
            st.markdown(list_html, unsafe_allow_html=True)

            csv_bytes = data.to_csv(index=False).encode("utf-8")
            st.download_button("⬇ Download CSV", csv_bytes, "waste_reports.csv", "text/csv", use_container_width=True)

    # ── Map ──
    with right_col:
        current_hash = hash(data.to_csv())

        if st.session_state.get("map_data_hash") != current_hash:
            m = folium.Map(
                location=[23.2599, 77.4126],
                zoom_start=11,
                tiles=None,
                prefer_canvas=True,
            )
            folium.TileLayer(
                tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                attr="Google Maps",
                name="Google Maps",
                max_zoom=20,
                overlay=False,
                control=False,
            ).add_to(m)

            if not data.empty:
                mc = MarkerCluster(options={"maxClusterRadius": 40}).add_to(m)
                for _, row in data.iterrows():
                    w   = row["waste_percent"]
                    clr = waste_folium_color(w)
                    folium.Marker(
                        [row["lat"], row["lon"]],
                        popup=folium.Popup(
                            f'<div style="font-family:Roboto,sans-serif;min-width:160px">'
                            f'<b style="font-size:15px">🗑 Waste Report</b><hr style="margin:6px 0">'
                            f'<b>Level:</b> {w}%<br><b>Lat:</b> {row["lat"]:.5f}<br><b>Lon:</b> {row["lon"]:.5f}</div>',
                            max_width=220
                        ),
                        tooltip=f"🗑 {w}% waste",
                        icon=folium.Icon(color=clr, icon="trash", prefix="fa"),
                    ).add_to(mc)

            st.session_state["folium_map"]    = m
            st.session_state["map_data_hash"] = current_hash

        st_folium(
            st.session_state["folium_map"],
            use_container_width=True,
            height=680,
            returned_objects=[],
            key="waste_map",
        )


if __name__ == "__main__":
    show()