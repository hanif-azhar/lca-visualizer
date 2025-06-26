import streamlit as st
import pandas as pd
import plotly.express as px
from lca_data import load_sample_data, calculate_impacts, load_product_data

st.set_page_config(page_title="🌱 LCA Visualizer", layout="wide")

st.title("🌱 Life Cycle Assessment Visualizer")

data_source = st.radio("Choose data input:", ["Sample Data", "Upload CSV"])  #ONLY ONE TIME

if data_source == "Sample Data":
    product = st.selectbox("🛍️ Choose a Product Preset", ["Custom", "Smartphone", "T-shirt", "Car"])
    df = load_product_data(product)
else:
    uploaded = st.file_uploader("Upload your CSV", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        st.stop()

st.write("### Raw LCA Input Data")
st.dataframe(df)

impact_data = calculate_impacts(df)

st.write("### Impact Visualization (CO₂ eq.)")
fig = px.bar(impact_data, x="Phase", y="CO2_eq_kg", color="Phase", text="CO2_eq_kg")
st.plotly_chart(fig, use_container_width=True)

reuse_cycles = st.slider("Estimated Reuse Cycles", min_value=0, max_value=10, value=0)
adjusted_df = calculate_impacts(df)
adjusted_df["CO2_eq_kg"] = adjusted_df["CO2_eq_kg"] / (reuse_cycles + 1)
adjusted_df["Energy_MJ"] = adjusted_df["Energy_MJ"] / (reuse_cycles + 1)
adjusted_df["Water_L"] = adjusted_df["Water_L"] / (reuse_cycles + 1)

reuse_range = list(range(1, 11))
co2_values = [
    impact_data["CO2_eq_kg"].sum() / reuse for reuse in reuse_range
]

reuse_df = pd.DataFrame({
    "Reuse_Cycles": reuse_range,
    "CO2_per_Cycle": co2_values
})

st.write("### CO₂ Trend vs. Reuse Cycles")
fig_line = px.line(reuse_df, x="Reuse_Cycles", y="CO2_per_Cycle", markers=True)
st.plotly_chart(fig_line, use_container_width=True)


st.write("### Total Environmental Impact Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total CO₂ (kg)", round(adjusted_df["CO2_eq_kg"].sum(), 2))
col2.metric("Total Energy (MJ)", round(adjusted_df["Energy_MJ"].sum(), 2))
col3.metric("Total Water (L)", round(adjusted_df["Water_L"].sum(), 2))

st.info(f"Impacts shown below are adjusted for reuse (÷{reuse_cycles + 1})")

st.write("### CO₂ Contribution by Phase (Pie Chart)")
fig_pie = px.pie(
    adjusted_df,
    names="Phase",
    values="CO2_eq_kg",
    title="Phase Contribution to Total CO₂"
)
st.plotly_chart(fig_pie, use_container_width=True)

if st.button("Export Summary CSV"):
    st.download_button(
        label="Download CSV",
        data=adjusted_df.to_csv(index=False),
        file_name="lca_summary.csv",
        mime="text/csv"
    )

