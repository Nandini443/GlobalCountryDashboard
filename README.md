# 🌍 Global Country Dashboard

A beautiful, data-rich Streamlit dashboard to explore economic, demographic, and social indicators for 80 countries worldwide.

---

## 📦 Files

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit application |
| `generate_data.py` | Script to regenerate the dataset |
| `world_countries.csv` | Dataset (80 countries × 16 indicators) |
| `requirements.txt` | Python dependencies |

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate dataset (first time only)
```bash
python generate_data.py
```
This creates `world_countries.csv`. The app also auto-generates it on first launch.

### 3. Launch the dashboard
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 📊 Dataset Columns

| Column | Description |
|--------|-------------|
| Country | Country name |
| Continent | Geographic continent |
| Population_M | Population in millions |
| GDP_Billion_USD | GDP in billion USD |
| GDP_Per_Capita_USD | GDP per capita (derived) |
| HDI | Human Development Index (0–1) |
| Life_Expectancy | Average life expectancy (years) |
| CO2_Tons_Per_Capita | CO₂ emissions per person (tons) |
| Internet_Penetration_Pct | % of population with internet access |
| Military_Spend_Billion_USD | Military spending in billion USD |
| Education_Index | UNDP Education Index (0–1) |
| Unemployment_Rate_Pct | Unemployment rate (%) |
| Capital_City | Capital city name |
| Currency | Currency code |
| Area_Km2 | Land area in km² |
| Population_Density | People per km² (derived) |

---

## 🗂️ Dashboard Pages

| Page | Description |
|------|-------------|
| 🌐 World Overview | KPIs, bubble chart, choropleth map, continent stats |
| 🔍 Country Explorer | Full country profile with radar chart and peer comparison |
| 📊 Compare Countries | Side-by-side comparison of any two nations |
| 📈 Rankings & Trends | Top-N bars, correlation heatmap, scatter explorer |
| 🗺️ Data Table | Filterable/downloadable full dataset |

---

## 🎨 Design

- **Theme**: Dark navy with gold/teal accents
- **Fonts**: Playfair Display (headings) + DM Sans (body)
- **Charts**: Plotly with custom dark theme
- **Sidebar**: Continent + population + GDP filters apply across all pages

---

*Data sources: World Bank, UN Development Programme, IMF — 2023 estimates*
