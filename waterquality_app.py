import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("water_quality_model.pkl")

def get_pollution_level(wqi):
    if wqi <= 25:
        return "Excellent"
    elif wqi <= 50:
        return "Good"
    elif wqi <= 75:
        return "Moderate"
    elif wqi <= 100:
        return "Poor"
    else:
        return "Very Poor"

st.title("Water Quality Index & Pollution Level Prediction")

st.header("Enter Water Quality Parameters")

# Numeric input fields for the 18 features
latitude = st.number_input("Latitude", value=0.0)
longitude = st.number_input("Longitude", value=0.0)
temp = st.number_input("Water Temperature (°C)", value=25.0)
ph = st.number_input("pH", value=7.0)
do = st.number_input("Dissolved Oxygen (mg/L)", value=6.0)
conductivity = st.number_input("Conductivity (µS/cm)", value=500.0)
turbidity = st.number_input("Turbidity (NTU)", value=5.0)
nitrate = st.number_input("Nitrate (mg/L)", value=2.0)
nitrite = st.number_input("Nitrite (mg/L)", value=0.05)
ammonia = st.number_input("Ammonia-N (mg/L)", value=0.1)
total_phos = st.number_input("Total Phosphorus (mg/L)", value=0.5)
total_nitrogen = st.number_input("Total Nitrogen (mg/L)", value=1.0)
cod = st.number_input("COD (mg/L)", value=30.0)
bod = st.number_input("BOD (mg/L)", value=5.0)
heavy_pb = st.number_input("Heavy Metals Pb (µg/L)", value=0.01)
heavy_cd = st.number_input("Heavy Metals Cd (µg/L)", value=0.005)
heavy_hg = st.number_input("Heavy Metals Hg (µg/L)", value=0.002)
coliform = st.number_input("Coliform Count (CFU/100mL)", value=100, step=1)

if st.button("Predict WQI & Pollution Level"):
    df_input = pd.DataFrame({
        'Latitude': [latitude],
        'Longitude': [longitude],
        'Water_Temperature_C': [temp],
        'pH': [ph],
        'Dissolved_Oxygen_mg_L': [do],
        'Conductivity_uS_cm': [conductivity],
        'Turbidity_NTU': [turbidity],
        'Nitrate_mg_L': [nitrate],
        'Nitrite_mg_L': [nitrite],
        'Ammonia_N_mg_L': [ammonia],
        'Total_Phosphorus_mg_L': [total_phos],
        'Total_Nitrogen_mg_L': [total_nitrogen],
        'COD_mg_L': [cod],
        'BOD_mg_L': [bod],
        'Heavy_Metals_Pb_ug_L': [heavy_pb],
        'Heavy_Metals_Cd_ug_L': [heavy_cd],
        'Heavy_Metals_Hg_ug_L': [heavy_hg],
        'Coliform_Count_CFU_100mL': [coliform]
    })

    wqi = model.predict(df_input)[0]
    level = get_pollution_level(wqi)

    st.metric("Predicted Water Quality Index (WQI)", round(wqi, 2))
    st.success(f"Pollution Level: *{level}*")

# Batch Prediction Section
st.header("Batch Prediction via CSV Upload")
uploaded_file = st.file_uploader("Upload a CSV file with 19 features", type=["csv"])
if uploaded_file:
    batch_df = pd.read_csv(uploaded_file)
    predictions = model.predict(batch_df)
    batch_df['Predicted_WQI'] = predictions
    batch_df['Pollution_Level'] = [get_pollution_level(wqi) for wqi in predictions]
    st.write(batch_df)
