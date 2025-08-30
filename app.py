import streamlit as st
import pandas as pd
import plotly.express as px
import io
import plotly.io as pio
from lca_data import load_sample_data, calculate_impacts, load_product_data

st.set_page_config(page_title="LCA Visualizer", layout="wide")

st.title("Life Cycle Assessment Visualizer")

data_source = st.radio("Choose data input:", ["Sample Data", "Upload CSV"])  #ONLY ONE TIME

if data_source == "Sample Data":
    selected_products = st.multiselect(
        "🛍️ Select products to compare",
        ["Smartphone", "T-shirt", "Car"],
        default=["Smartphone"]
    )

    if not selected_products:
        st.warning("Please select at least one product.")
        st.stop()

    # Load and merge selected products
    df_list = []
    for product in selected_products:
        product_df = load_product_data(product)
        product_df["Product"] = product
        df_list.append(product_df)

    df = pd.concat(df_list, ignore_index=True)

else:
    uploaded = st.file_uploader("Upload your CSV", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        st.stop()


st.write("### Raw LCA Input Data")
st.dataframe(df)

impact_data = calculate_impacts(df)

st.write("### Impact Comparison (CO₂ eq.) by Product & Phase")
fig = px.bar(
    impact_data,
    x="Phase",
    y="CO2_eq_kg",
    color="Product",
    barmode="group",
    text="CO2_eq_kg"
)
st.plotly_chart(fig, use_container_width=True)

# Export Bar Chart as PNG
buf_bar = io.BytesIO()
pio.write_image(fig, buf_bar, format='png')
st.download_button(
    label="📥 Download Impact Comparison Chart (PNG)",
    data=buf_bar.getvalue(),
    file_name="impact_comparison.png",
    mime="image/png"
)

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

# ----- CO₂ vs. Reuse Cycles Chart (Per Product) -----
st.write("### 📊 CO₂ Emissions vs. Reuse Cycles (per Product)")

reuse_range = list(range(1, 11))
reuse_chart_data = []

for product in impact_data["Product"].unique():
    product_df = impact_data[impact_data["Product"] == product]
    for reuse in reuse_range:
        reuse_co2 = product_df["CO2_eq_kg"].sum() / reuse
        reuse_chart_data.append({
            "Product": product,
            "Reuse_Cycle": reuse,
            "CO2_per_Cycle": reuse_co2
        })

reuse_df = pd.DataFrame(reuse_chart_data)

fig_line = px.line(
    reuse_df,
    x="Reuse_Cycle",
    y="CO2_per_Cycle",
    color="Product",
    markers=True,
    labels={"CO2_per_Cycle": "CO₂ (kg)"}
)
st.plotly_chart(fig_line, use_container_width=True)

# Export Line Chart as PNG
buf_line = io.BytesIO()
pio.write_image(fig_line, buf_line, format='png')
st.download_button(
    label="📥 Download CO₂ vs Reuse Cycles Chart (PNG)",
    data=buf_line.getvalue(),
    file_name="reuse_co2_trend.png",
    mime="image/png"
)

st.write("### Total Impact by Product")
summary = impact_data.groupby("Product")[["CO2_eq_kg", "Energy_MJ", "Water_L"]].sum().reset_index()
st.dataframe(summary.style.format({
    "CO2_eq_kg": "{:.2f}",
    "Energy_MJ": "{:.2f}",
    "Water_L": "{:.2f}"
}))

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

