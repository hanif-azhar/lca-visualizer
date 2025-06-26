import pandas as pd

def load_sample_data():
    return pd.DataFrame({
        "Phase": ["Raw Material", "Manufacturing", "Transport", "Use", "End-of-Life"],
        "Material": ["Steel", "Plastic", "Diesel", "Electricity", "Landfill"],
        "Mass_kg": [50, 20, 5, 100, 10],
        "Emission_factor": [2.1, 1.8, 3.0, 0.5, 1.2],   # CO₂ per kg
        "Energy_MJ_per_kg": [15, 12, 20, 5, 3],         # MJ per kg
        "Water_L_per_kg": [100, 60, 30, 10, 5]          # L per kg
    })

def load_product_data(product_name):
    if product_name == "Smartphone":
        return pd.DataFrame({
            "Phase": ["Raw Material", "Manufacturing", "Transport", "Use", "End-of-Life"],
            "Material": ["Aluminum", "Circuit Board", "Air Freight", "Charging", "E-waste"],
            "Mass_kg": [0.2, 0.1, 0.05, 0.1, 0.1],
            "Emission_factor": [9.0, 12.0, 6.0, 2.0, 3.0],
            "Energy_MJ_per_kg": [80, 120, 60, 20, 40],
            "Water_L_per_kg": [200, 150, 90, 30, 50]
        })
    elif product_name == "T-shirt":
        return pd.DataFrame({
            "Phase": ["Raw Material", "Manufacturing", "Transport", "Use", "End-of-Life"],
            "Material": ["Cotton", "Dyeing", "Shipping", "Washing", "Landfill"],
            "Mass_kg": [0.3, 0.2, 0.1, 0.3, 0.2],
            "Emission_factor": [2.0, 3.5, 2.0, 0.6, 1.5],
            "Energy_MJ_per_kg": [30, 40, 20, 10, 5],
            "Water_L_per_kg": [500, 400, 100, 50, 30]
        })
    elif product_name == "Car":
        return pd.DataFrame({
            "Phase": ["Raw Material", "Manufacturing", "Transport", "Use", "End-of-Life"],
            "Material": ["Steel", "Assembly", "Shipping", "Fuel", "Scrap"],
            "Mass_kg": [1000, 500, 200, 1000, 300],
            "Emission_factor": [2.1, 1.8, 3.0, 2.4, 1.2],
            "Energy_MJ_per_kg": [15, 12, 20, 30, 8],
            "Water_L_per_kg": [100, 60, 30, 10, 5]
        })
    else:
        return load_sample_data()

def calculate_impacts(df):
    df["CO2_eq_kg"] = df["Mass_kg"] * df["Emission_factor"]
    df["Energy_MJ"] = df["Mass_kg"] * df["Energy_MJ_per_kg"]
    df["Water_L"] = df["Mass_kg"] * df["Water_L_per_kg"]
    return df[["Phase", "Material", "CO2_eq_kg", "Energy_MJ", "Water_L"]]
