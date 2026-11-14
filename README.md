# TerraTurn — Earth Observation Crop Rotation Decision Support System

> **NASA Space Apps Challenge 2026**  
> Transforming multi-mission NASA Earth Observation telemetry into field-level, climate-resilient multi-year crop rotation strategies.

---

## Overview

Static, regional crop rotation templates fail to account for sub-field soil variability, steep drainage slopes, and accelerating climate volatility. Conventional sequences (such as *Cotton → Winter Wheat → Bare Fallow*) often leave topsoil exposed for **140+ days per year**, accelerating wind and storm runoff erosion while depleting root-zone moisture.

**TerraTurn** is an interactive agronomic decision-support platform that combines **live NASA satellite climatology** with local farm constraints (soil texture, irrigation regime, tillage machinery) and farmer priorities (*Water Conservation, Soil Organic Matter, Biological Nitrogen Fixation, Net Margin*) to rank multi-year regenerative and drought-adapted crop rotations.

---

## Key Capabilities

* **100% Live NASA POWER Telemetry Integration:** Clicking any coordinate or drawing a custom field polygon anywhere on Earth queries the NASA Langley Research Center (`power.larc.nasa.gov`) REST API in real time to extract 10-year agroclimatology (`PRECTOTCORR`, `T2M_MAX`, `GWETROOT`, `ALLSKY_SFC_SW_DWN`).
* **Custom Field Boundary Drawing (`Leaflet.draw`):** Farmers and agronomists can outline any parcel worldwide, automatically computing geodesic area (ha) and centroid coordinates to run localized water-balance and rotation evaluations.
* **Sub-Field Management Zones (30m WGS84 Grid):** Visualizes spatial variability across four sensor layers:
  * **SMAP L4** Root-Zone Soil Moisture (`% VWC`)
  * **ECOSTRESS** Canopy Surface Temperature (`°C LST`)
  * **SRTM 30m DEM + GPM** Runoff & Erosion Grade (`%`)
  * **Landsat 8/9 HLS** Bare-Soil Exposure Windows (`NDVI < 0.25`)
* **12-Month Hydrological & Bare-Soil Vulnerability Profile:** Dynamic SVG chart overlaying monthly precipitation (`GPM`), reference evapotranspiration demand (`ET0`), root-zone moisture (`SMAP`), and bare-soil exposure intervals for the selected baseline rotation.
* **Climate Stress-Testing:** Instant simulation of `+2.0°C Summer Heat Anomaly`, `-20% Growing Season Rainfall`, and `Early Autumn Frost (-14 Days)`.
* **Human-in-the-Loop Agronomist Verification:** Every recommended rotation includes transparent satellite evidence, plain-language technical references (*Bio-drilling, GDD, ET0*), an interactive ground-truth verification checklist (subsurface `ECe` salinity, soil `pH`, local buyer contracts), and one-click JSON/Print brief exports.

---

## NASA Earth Observation Datasets & Harmonization

TerraTurn harmonizes multi-mission NASA datasets onto a standardized **30-meter WGS84 (`EPSG:4326`)** analysis frame:

| Mission / Product | Native Scale | Derived Agronomic Metric | Role in TerraTurn Scoring Engine |
| :--- | :--- | :--- | :--- |
| **NASA POWER** | 0.5° Point REST | `T2M_MAX`, `PRECTOTCORR`, `GWETROOT`, Solar Radiation | Live climatology API, `ET0` demand, and aridity ratio calculation |
| **SMAP L4 Soil Moisture** | 9 km → 30 m | Root-zone (0–100 cm) volumetric water content (`% VWC`) | Detects late-summer moisture deficits and compaction stress |
| **ECOSTRESS (ISS)** | 70 m → 30 m | Land Surface Temperature (`LST`) & thermal stress | Identifies heat-stressed sub-field benches (`>36°C`) |
| **GPM IMERG Final** | 0.1° → 30 m | Monthly precipitation (`mm`) & storm intensity | Evaluates seasonal rainfall timing and runoff erosivity |
| **Landsat 8/9 OLI-TIRS** | 30 m Native | `NDVI` time series & bare-soil duration (`NDVI < 0.25`) | Flags post-harvest bare-soil exposure windows |
| **SRTM Global DEM** | 30 m Native | Sub-field slope grade (`%`) & flow accumulation | Targets perennial strip buffers to steep runoff slopes (`>3%`) |
| **GRACE / GRACE-FO** | Basin Mascon | Terrestrial Water Storage (`TWS`) anomaly | Contextualizes regional groundwater and canal supply limits |
| **MODIS Terra/Aqua** | 250 m → 30 m | 20-year phenological green-up/senescence baselines | Calibrates planting and termination windows |

---

## System Architecture

```text
Terraturn/
├── manage.py
├── requirements.txt
├── build_deck.py                  # Automated NASA HDS pitch deck generator (.pptx)
├── terraturn_core/                # Django project settings & root URL configuration
└── planner/
    ├── urls.py                    # Dashboard & REST API endpoints
    ├── views.py                   # SSR initial state + AJAX endpoints
    ├── services/
    │   ├── nasa_client.py         # Live NASA POWER REST API client with 24h caching
    │   └── scoring.py             # Multi-objective rotation & aridity scoring engine
    └── templates/
        └── planner/
            └── index.html         # NASA Horizon Design System (HDS) UI + Leaflet.draw