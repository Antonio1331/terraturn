# TerraTurn — Earth Observation & Orbital Crop Rotation Decision Support

> **NASA Space Apps Challenge 2026**  
> Transforming real-time NASA Earth Observation telemetry and in-situ camera verification into field-level, climate-resilient multi-year crop rotation strategies.

---

## Overview

Static, regional crop rotation templates fail to account for sub-field soil variability, steep drainage slopes, and accelerating climate volatility. Conventional sequences (such as *Cotton → Winter Wheat → Bare Fallow*) often leave topsoil exposed for **140+ days per year**, accelerating wind and storm runoff erosion while depleting root-zone moisture.

**TerraTurn** is an interactive agronomic decision-support platform that combines **live 2026 Year-to-Date NASA satellite telemetry** with local farm constraints (soil texture, irrigation regime, tillage machinery) and farmer priorities (*Water Conservation, Soil Organic Matter, Biological Nitrogen Fixation, Net Margin*) to rank multi-year regenerative and drought-adapted crop rotations.

---

## Key Capabilities

* **Real-Time 2026 Year-to-Date NASA POWER Telemetry:** Clicking any coordinate or drawing a custom field polygon anywhere on Earth queries the NASA Langley Research Center (`power.larc.nasa.gov/api/temporal/daily/point`) REST API in real time to extract actual daily observations from January 1, 2026 up to the current active satellite pass (`Jan–Nov*`, omitting future unelapsed months).
* **Custom Field Boundary Drawing (`Leaflet.draw`):** Farmers and agronomists can outline any parcel worldwide, automatically computing geodesic area (ha) and centroid coordinates to run localized water-balance and rotation evaluations.
* **Orbital Pass HUD & Swath Overlay:** Displays live sun-synchronous satellite ground tracks (`SMAP L-Band` / `ISS ECOSTRESS`) over the active field parcel with altitude, inclination, and downlink lock status.
* **In-Situ Field Camera NDVI Scanner:** Browser-based optical scanner (`getUserMedia`) computes real-time Excess Green (`ExG`) / Pseudo-NDVI indices from live device camera frames to validate Landsat bare-soil flags (`NDVI < 0.25`) directly on the ground[cite: 2, 3].
* **Sub-Field Management Zones (30m WGS84 Grid):** Visualizes spatial variability across four sensor layers:
  * **SMAP L4** Root-Zone Soil Moisture (`% VWC`)
  * **ECOSTRESS** Canopy Surface Temperature (`°C LST`)[cite: 3]
  * **SRTM 30m DEM + GPM** Runoff & Erosion Grade (`%`)[cite: 3]
  * **Landsat 8/9 HLS** Bare-Soil Exposure Windows (`NDVI < 0.25`)[cite: 3]
* **Year-to-Date Hydrological & Bare-Soil Profile:** Interactive SVG chart overlaying monthly precipitation (`GPM`), reference evapotranspiration demand (`ET0`), root-zone moisture (`SMAP`), and bare-soil exposure intervals—dynamically recalculating whenever soil texture, irrigation regime, management zone, or climate stress scenarios change[cite: 2, 3].
* **Climate Stress-Testing:** Instant simulation of `+2.0°C Summer Heat Anomaly`, `-20% Growing Season Rainfall`, and `Early Autumn Frost (-14 Days)`[cite: 3].
* **Human-in-the-Loop Agronomist Verification:** Every recommended rotation includes transparent satellite evidence, plain-language technical references (*Bio-drilling, GDD, ET0*), an interactive ground-truth verification checklist (subsurface `ECe` salinity, soil `pH`, local buyer contracts), and one-click JSON/Print brief exports[cite: 3].

---

## NASA Earth Observation Datasets & Harmonization

TerraTurn harmonizes multi-mission NASA datasets onto a standardized **30-meter WGS84 (`EPSG:4326`)** analysis frame[cite: 3]:

| Mission / Product | Native Scale | Derived Agronomic Metric | Role in TerraTurn Scoring Engine |
| :--- | :--- | :--- | :--- |
| **NASA POWER Daily** | 0.5° Point REST | `T2M_MAX`, `PRECTOTCORR`, `GWETROOT`, Solar Radiation | Live 2026 YTD telemetry, `ET0` demand, and aridity ratio calculation[cite: 3] |
| **SMAP L4 Soil Moisture** | 9 km → 30 m | Root-zone (0–100 cm) volumetric water content (`% VWC`) | Detects late-summer moisture deficits and compaction stress[cite: 3] |
| **ECOSTRESS (ISS)** | 70 m → 30 m | Land Surface Temperature (`LST`) & thermal stress | Identifies heat-stressed sub-field benches (`>36°C`)[cite: 3] |
| **GPM IMERG Final** | 0.1° → 30 m | Cumulative precipitation (`mm`) & storm intensity | Evaluates seasonal rainfall timing and runoff erosivity[cite: 3] |
| **Landsat 8/9 OLI-TIRS** | 30 m Native | `NDVI` time series & bare-soil duration (`NDVI < 0.25`) | Flags post-harvest bare-soil exposure windows[cite: 3] |
| **SRTM Global DEM** | 30 m Native | Sub-field slope grade (`%`) & flow accumulation | Targets perennial strip buffers to steep runoff slopes (`>3%`)[cite: 3] |
| **GRACE / GRACE-FO** | Basin Mascon | Terrestrial Water Storage (`TWS`) anomaly | Contextualizes regional groundwater and canal supply limits[cite: 3] |
| **MODIS Terra/Aqua** | 250 m → 30 m | 20-year phenological green-up/senescence baselines | Calibrates planting and termination windows[cite: 3] |

---

## Repository Structure

```text
Terraturn/
├── manage.py
├── requirements.txt
├── config/                        # Django project settings & root URL configuration
├── planner/
│   ├── urls.py                    # Dashboard & REST API endpoints
│   ├── views.py                   # SSR initial state + AJAX endpoints
│   └── services/
│       ├── nasa_client.py         # Live NASA POWER Daily API client (2026 YTD)
│       └── scoring.py             # Multi-objective rotation & aridity scoring engine
└── templates/
    └── planner/
        └── index.html             # NASA Horizon UI, Leaflet.draw, Orbital HUD & Field Cam