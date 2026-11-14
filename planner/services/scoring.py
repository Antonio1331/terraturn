def evaluate_rotation_strategies(payload: dict) -> list:
    """
    Рассчитывает рейтинг стратегий севооборота на бэкенде по данным NASA POWER (GPM, ET0)
    и локальным ограничениям поля.
    """
    climate_id = payload.get("climateId", "baseline")
    rotation_id = payload.get("rotationId", "cotton_wheat_fallow")
    soil_id = payload.get("soilId", "clay_loam")
    irrigation_id = payload.get("irrigationId", "deficit")
    equipment_id = payload.get("equipmentId", "no_till")
    priorities = payload.get("priorities", {"water": 85, "som": 80, "nitrogen": 70, "margin": 65})
    monthly = payload.get("monthly", [])

    climate_offsets = {
        "baseline": {"et_mult": 1.00, "rain_mult": 1.00, "margin_delta": 0},
        "heatwave": {"et_mult": 1.15, "rain_mult": 1.00, "margin_delta": -55},
        "drought":  {"et_mult": 1.10, "rain_mult": 0.80, "margin_delta": -85},
        "frost":    {"et_mult": 0.94, "rain_mult": 1.00, "margin_delta": -45},
    }
    off = climate_offsets.get(climate_id, climate_offsets["baseline"])

    if monthly:
        annual_gpm = sum(float(m.get("gpm", 0)) for m in monthly) * off["rain_mult"]
        annual_et0 = sum(float(m.get("et0", 0)) for m in monthly) * off["et_mult"]
        aridity_ratio = annual_et0 / max(1.0, annual_gpm)
        aridity_bonus = min(8, max(-4, round((aridity_ratio - 2.2) * 2.5)))
    else:
        aridity_bonus = 0

    w_water = float(priorities.get("water", 85))
    w_som = float(priorities.get("som", 80))
    w_nitro = float(priorities.get("nitrogen", 70))
    w_margin = float(priorities.get("margin", 65))
    total_weight = max(1.0, w_water + w_som + w_nitro + w_margin)

    baseline_names = {
        "cotton_wheat_fallow": "Yr1 Cotton -> Yr2 Winter Wheat -> Yr3 Bare Fallow",
        "corn_soy_fallow": "Yr1 Grain Maize -> Yr2 Soybean -> Yr3 Bare Fallow",
        "wheat_monocrop": "Continuous Winter Wheat + Summer Bare Fallow",
    }

    candidates = [
        {
            "id": "strat_baseline",
            "name": "Current Baseline Rotation",
            "sequence": baseline_names.get(rotation_id, baseline_names["cotton_wheat_fallow"]),
            "waterDelta": round((off["et_mult"] - 1.0) * 100),
            "erosionDelta": 12 if soil_id == "silt_loam" else 5,
            "somDelta": -0.35,
            "marginUsd": max(310, 605 + off["margin_delta"]),
            "confidence": "High (10-Yr NASA POWER + Observed Baseline)",
            "weights": {"water": 20, "som": 15, "nitrogen": 10, "margin": 72},
            "climatePenalty": {"baseline": 0, "heatwave": -14, "drought": -18, "frost": -6},
            "aridityImpact": -aridity_bonus,
            "evidence": [
                "Landsat-8 NDVI time series confirms 140+ days of bare soil between autumn harvest and spring planting.",
                "ECOSTRESS & NASA POWER thermal logs show peak summer stress exceeding 37°C.",
                "SMAP L4 root-zone moisture drops below 18% VWC in late summer, increasing irrigation dependency.",
            ],
            "glossary": "NDVI < 0.25 indicates exposed soil lacking living root anchorage. Evapotranspiration (ET0) measures atmospheric water demand.",
            "checks": [
                "Measure 0–30 cm soil electrical conductivity (ECe) to verify summer salt accumulation.",
                "Inspect downslope field margins for rill erosion after spring GPM storm events.",
                "Review synthetic nitrogen carry-over before autumn disking.",
            ],
        },
        {
            "id": "strat_regenerative",
            "name": "Soil & Water Regenerator",
            "sequence": "Yr1 Maize + Crimson Clover -> Yr2 Winter Rye / Mungbean -> Yr3 Daikon Radish + Oats",
            "waterDelta": round(-23 + (off["et_mult"] - 1.0) * 35),
            "erosionDelta": -62,
            "somDelta": 1.15,
            "marginUsd": max(430, 660 + round(off["margin_delta"] * 0.45)),
            "confidence": "Moderate-High (Downscaled SMAP + SRTM)",
            "weights": {"water": 86, "som": 96, "nitrogen": 92, "margin": 70},
            "climatePenalty": {"baseline": 0, "heatwave": -2, "drought": -3, "frost": -2},
            "aridityImpact": round(aridity_bonus * 0.5),
            "evidence": [
                "SRTM slope modeling shows Winter Rye eliminates bare-soil exposure on slopes >3%, cutting sediment loss by 62%.",
                "SMAP infiltration curves indicate Daikon Radish taproots fracture plow-pan compaction, lifting spring moisture by +18%.",
                "Crimson Clover and Mungbean fix ~75 kg N/ha biologically, offsetting synthetic urea application.",
            ],
            "glossary": "Bio-drilling uses deep taproots (Daikon Radish) to create vertical macropores for water infiltration without mechanical subsoiling.",
            "checks": [
                "Verify subsurface soil pH (target 6.0–7.5) via soil core test before seeding Crimson Clover.",
                "Terminate Winter Rye 14 days prior to Yr2 cash crop planting to prevent spring moisture competition.",
                "Confirm local livestock feedlot or forage demand for Yr3 oat hay.",
            ],
        },
        {
            "id": "strat_climate_cash",
            "name": "Drought-Adapted Cash & Pulse",
            "sequence": "Yr1 Grain Sorghum -> Yr2 Kabuli Chickpea (N-Fixer) -> Yr3 Early Winter Barley",
            "waterDelta": round(-34 + (off["et_mult"] - 1.0) * 30),
            "erosionDelta": -44,
            "somDelta": 0.48,
            "marginUsd": max(500, 740 + round(off["margin_delta"] * 0.35)),
            "confidence": "High (ECOSTRESS + NASA POWER GDD Match)",
            "weights": {"water": 95, "som": 70, "nitrogen": 76, "margin": 94},
            "climatePenalty": {"baseline": 0, "heatwave": 3, "drought": 4, "frost": -1},
            "aridityImpact": aridity_bonus,
            "evidence": [
                "ECOSTRESS water-use efficiency logs show Grain Sorghum cuts July irrigation demand by 34% during heatwaves.",
                "GPM rainfall timing aligns Early Winter Barley grain-fill with spring rains, avoiding the June–August dry window.",
                "Kabuli Chickpea breaks cereal root-rot disease cycles while adding 60 kg N/ha.",
            ],
            "glossary": "Growing Degree Days (GDD) measure accumulated heat units required for a crop to reach physiological maturity before autumn frost.",
            "checks": [
                "Verify regional buyer specs and forward contracts for Kabuli Chickpea seed caliber.",
                "Check 18-month residual herbicide records for sulfonylurea carryover before chickpea seeding.",
                "Calibrate combine concave clearance to prevent pulse seed-coat splitting.",
            ],
        },
        {
            "id": "strat_forage_buffer",
            "name": "Perennial Legume & Strip Buffer",
            "sequence": "Yr1–2 Alfalfa / Lucerne Strip (High-Slope Zones) -> Yr3 Sorghum-Sudangrass + Winter Wheat",
            "waterDelta": round(-16 + (off["et_mult"] - 1.0) * 45),
            "erosionDelta": -71,
            "somDelta": 1.40,
            "marginUsd": max(460, 685 + round(off["margin_delta"] * 0.40)),
            "confidence": "Moderate (Requires Subsurface Salinity Check)",
            "weights": {"water": 72, "som": 98, "nitrogen": 96, "margin": 78},
            "climatePenalty": {"baseline": 0, "heatwave": -3, "drought": -5, "frost": 0},
            "aridityImpact": 0,
            "evidence": [
                "Targeting perennial Alfalfa to high-runoff sub-field zones stabilizes steep benches year-round.",
                "Deep 240 cm root architecture accesses capillary moisture and fixes up to 165 kg N/ha across two seasons.",
                "Eliminates tillage passes for 24 consecutive months, rebuilding soil aggregate stability.",
            ],
            "glossary": "Zone-specific strip cropping places perennial cover on steep or degraded sub-field zones while keeping prime benches in annual cash crops.",
            "checks": [
                "Test subsoil salinity (ECe < 4.0 dS/m) on elevated benches before establishing perennial alfalfa.",
                "Confirm local dairy or livestock forage baling equipment and transport access.",
                "Monitor autumn crown dormancy rating to prevent winterkill.",
            ],
        },
    ]

    results = []
    for c in candidates:
        w = c["weights"]
        weighted = (
            w["water"] * w_water +
            w["som"] * w_som +
            w["nitrogen"] * w_nitro +
            w["margin"] * w_margin
        ) / total_weight

        fit = round(weighted) + c["climatePenalty"].get(climate_id, 0) + c["aridityImpact"]
        if irrigation_id == "rainfed" and c["id"] == "strat_baseline":
            fit -= 12
        if equipment_id == "conventional" and c["id"] == "strat_regenerative":
            fit -= 6

        c_out = {k: v for k, v in c.items() if k not in ("weights", "climatePenalty", "aridityImpact")}
        c_out["fit"] = max(15, min(98, fit))
        results.append(c_out)

    results.sort(key=lambda x: x["fit"], reverse=True)
    return results