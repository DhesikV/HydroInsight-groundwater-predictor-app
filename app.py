import streamlit as st
import pandas as pd
import joblib
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import io

# Load dataset and model
df = pd.read_csv("clean_groundwater.csv")
model = joblib.load("groundwater_model.pkl")

st.set_page_config(page_title="HydroInsight – Groundwater Finder", layout="wide")
st.title("💧 HydroInsight – Tamil Nadu Groundwater Predictor")

# Features for prediction
features = [
    "Monsoon season recharge from rainfall",
    "Monsoon season recharge from other sources",
    "Non-monsoon season recharge from rainfall",
    "Non-monsoon season recharge from other sources",
    "Total annual groundwater recharge",
    "Total Annual Extraction",
]

# Add predictions (1 = Available, 0 = Over-exploited)
df["Predicted"] = model.predict(df[features])
df["Prediction_Status"] = df["Predicted"].map({1: "✅ Available", 0: "❌ Over-Exploited"})

# --- Load Tamil Nadu GeoJSON ---
gdf = gpd.read_file("TAMILNADU_SUBDISTRICTS.geojson")

# Merge predictions with map data
map_data = gdf.merge(df, left_on="dtname", right_on="Name of District", how="left")

# Create two columns in Streamlit
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Tamil Nadu Groundwater Availability Map")
    m = folium.Map(location=[11, 78], zoom_start=7)

    for _, r in map_data.iterrows():
        if pd.isna(r["Predicted"]):
            continue
        color = "green" if r["Predicted"] == 1 else "red"
        geo_json = gpd.GeoSeries(r["geometry"]).simplify(0.001).to_json()
        folium.GeoJson(
            data=geo_json,
            style_function=lambda x, col=color: {
                "fillColor": col, "color": "black", "weight": 1, "fillOpacity": 0.6
            },
            tooltip=f"{r['dtname']}: {r['Prediction_Status']}"
        ).add_to(m)

    st_folium(m, width=700, height=500)

with col2:
    st.subheader("📊 District-wise Groundwater Data")

    # --- District Selector ---
    district_list = ["All Districts"] + sorted(df["Name of District"].unique().tolist())
    selected_district = st.selectbox("🔍 Select District:", district_list)

    if selected_district != "All Districts":
        display_df = df[df["Name of District"] == selected_district]
        st.markdown(f"### 📍 Data for {selected_district}")
    else:
        display_df = df
        st.markdown("### 📍 Data for All Districts")

    st.dataframe(display_df)

    # --- Download Buttons ---
    st.markdown("### 📥 Download Data")

    # CSV
    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv,
        file_name="groundwater_predictions.csv",
        mime="text/csv"
    )

    # Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        display_df.to_excel(writer, index=False, sheet_name="Groundwater Data")
    st.download_button(
        label="⬇️ Download as Excel",
        data=buffer,
        file_name="groundwater_predictions.xlsx",
        mime="application/vnd.ms-excel"
    )
