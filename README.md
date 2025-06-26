# LCA Visualizer

**LCA Visualizer** is a lightweight dashboard built with Streamlit to help analyze product life cycle impacts.

---

## Features

- Choose from sample products (Smartphone, T-shirt, Car) or upload your own CSV  
- Visualize total CO₂, energy, and water impact  
- Adjust reuse cycles to simulate circular design  
- Export your summary as CSV  

---

## Example CSV Format

```
| Phase         | Material   | Mass_kg | Emission_factor | Energy_MJ_per_kg | Water_L_per_kg |
|---------------|------------|---------|------------------|-------------------|----------------|
| Raw Material  | Steel      | 50      | 2.1              | 15                | 100            |
| Manufacturing | Plastic    | 20      | 1.8              | 12                | 60             |
| Transport     | Diesel     | 5       | 3.0              | 20                | 30             |
| Use           | Electricity| 100     | 0.5              | 5                 | 10             |
| End-of-Life   | Landfill   | 10      | 1.2              | 3                 | 5              |

```

---

## Requirements

- Python 3.8+
- pip

---

## Installation

```bash
git clone https://github.com/hanif-azhar/lca-visualizer.git
cd lca-visualizer
python -m venv venv
source venv/bin/activate     # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
```

---

## File Structure

```
lca-visualizer/
├── app.py
├── lca_data.py
├── requirements.txt
├── .gitignore
└── README.md
```

## License

This project is released under the MIT License.
```
