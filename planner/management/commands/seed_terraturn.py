# planner/management/commands/seed_terraturn.py
from django.core.management.base import BaseCommand
from planner.models import FieldParcel, ManagementZone, MonthlyClimate, CropTrait


class Command(BaseCommand):
    help = "Populates the database with initial NASA telemetry, field parcels, and crop traits."

    def handle(self, *args, **options):
        ManagementZone.objects.all().delete()
        MonthlyClimate.objects.all().delete()
        FieldParcel.objects.all().delete()
        CropTrait.objects.all().delete()

        parcels_data = [
            {
                "slug": "sirdaryo",
                "label": "Sirdaryo Plot 04 — 42.4 ha (Clay Loam, Canal Irrigation)",
                "center_lat": 40.4885,
                "center_lon": 68.7140,
                "default_soil": "clay_loam",
                "default_water": "deficit",
                "default_rotation": "cotton_wheat_fallow",
                "zones": [
                    {
                        "zone_code": "MZ-01",
                        "name": "MZ-01 Northwest Headgate Bench (10.8 ha)",
                        "coords": [[40.4910, 68.7095], [40.4910, 68.7140], [40.4885, 68.7140], [40.4885, 68.7095]],
                        "smap": 26.2,
                        "ecostress": 32.6,
                        "srtm": 1.4,
                        "bare_days": 102,
                    },
                    {
                        "zone_code": "MZ-02",
                        "name": "MZ-02 Northeast Saline Bench (11.2 ha)",
                        "coords": [[40.4910, 68.7140], [40.4910, 68.7185], [40.4885, 68.7185], [40.4885, 68.7140]],
                        "smap": 16.4,
                        "ecostress": 37.8,
                        "srtm": 3.4,
                        "bare_days": 148,
                    },
                    {
                        "zone_code": "MZ-03",
                        "name": "MZ-03 Southwest Alluvial Flat (10.1 ha)",
                        "coords": [[40.4885, 68.7095], [40.4885, 68.7140], [40.4860, 68.7140], [40.4860, 68.7095]],
                        "smap": 23.8,
                        "ecostress": 34.1,
                        "srtm": 2.1,
                        "bare_days": 118,
                    },
                    {
                        "zone_code": "MZ-04",
                        "name": "MZ-04 Southeast Tailwater Slope (10.3 ha)",
                        "coords": [[40.4885, 68.7140], [40.4885, 68.7185], [40.4860, 68.7185], [40.4860, 68.7140]],
                        "smap": 17.5,
                        "ecostress": 36.9,
                        "srtm": 4.9,
                        "bare_days": 152,
                    },
                ],
                "monthly": [
                    ("Jan", 38, 20, 27.5, 0.17),
                    ("Feb", 42, 30, 28.4, 0.20),
                    ("Mar", 54, 58, 29.1, 0.34),
                    ("Apr", 44, 96, 26.2, 0.56),
                    ("May", 22, 142, 21.8, 0.72),
                    ("Jun", 6,  184, 17.4, 0.78),
                    ("Jul", 2,  198, 15.6, 0.74),
                    ("Aug", 3,  182, 16.1, 0.62),
                    ("Sep", 7,  130, 18.0, 0.36),
                    ("Oct", 21, 78,  20.4, 0.21),
                    ("Nov", 32, 38,  23.8, 0.18),
                    ("Dec", 36, 22,  26.1, 0.16),
                ],
            },
            {
                "slug": "yangiyul",
                "label": "Yangiyul North — 68.0 ha (Silt Loam, Deficit Drip)",
                "center_lat": 41.1240,
                "center_lon": 69.0420,
                "default_soil": "silt_loam",
                "default_water": "drip_pivot",
                "default_rotation": "wheat_monocrop",
                "zones": [
                    {
                        "zone_code": "MZ-01",
                        "name": "MZ-01 Upper Loess Terrace (18.0 ha)",
                        "coords": [[41.1270, 69.0365], [41.1270, 69.0420], [41.1240, 69.0420], [41.1240, 69.0365]],
                        "smap": 21.0,
                        "ecostress": 35.4,
                        "srtm": 4.8,
                        "bare_days": 146,
                    },
                    {
                        "zone_code": "MZ-02",
                        "name": "MZ-02 Central Drip Sector (17.5 ha)",
                        "coords": [[41.1270, 69.0420], [41.1270, 69.0475], [41.1240, 69.0475], [41.1240, 69.0420]],
                        "smap": 25.6,
                        "ecostress": 32.9,
                        "srtm": 2.2,
                        "bare_days": 112,
                    },
                    {
                        "zone_code": "MZ-03",
                        "name": "MZ-03 South Canal Margin (16.5 ha)",
                        "coords": [[41.1240, 69.0365], [41.1240, 69.0420], [41.1210, 69.0420], [41.1210, 69.0365]],
                        "smap": 24.4,
                        "ecostress": 33.2,
                        "srtm": 1.9,
                        "bare_days": 108,
                    },
                    {
                        "zone_code": "MZ-04",
                        "name": "MZ-04 East Wind-Exposed Ridge (16.0 ha)",
                        "coords": [[41.1240, 69.0420], [41.1240, 69.0475], [41.1210, 69.0475], [41.1210, 69.0420]],
                        "smap": 17.1,
                        "ecostress": 36.7,
                        "srtm": 5.2,
                        "bare_days": 158,
                    },
                ],
                "monthly": [
                    ("Jan", 48, 18, 29.0, 0.22),
                    ("Feb", 52, 28, 30.1, 0.28),
                    ("Mar", 68, 54, 31.2, 0.48),
                    ("Apr", 58, 92, 28.4, 0.71),
                    ("May", 32, 136, 23.5, 0.68),
                    ("Jun", 10, 176, 18.2, 0.24),
                    ("Jul", 4,  192, 15.8, 0.19),
                    ("Aug", 4,  175, 16.0, 0.18),
                    ("Sep", 10, 124, 17.5, 0.20),
                    ("Oct", 28, 72,  21.2, 0.23),
                    ("Nov", 42, 34,  25.4, 0.26),
                    ("Dec", 46, 20,  27.8, 0.22),
                ],
            },
            {
                "slug": "platte",
                "label": "Platte Pivot 12 — 54.5 ha (Silt Loam, Rainfed Dryland)",
                "center_lat": 40.9165,
                "center_lon": -98.3420,
                "default_soil": "silt_loam",
                "default_water": "rainfed",
                "default_rotation": "corn_soy_fallow",
                "zones": [
                    {
                        "zone_code": "MZ-01",
                        "name": "MZ-01 North Upland Loam (14.0 ha)",
                        "coords": [[40.9195, -98.3470], [40.9195, -98.3420], [40.9165, -98.3420], [40.9165, -98.3470]],
                        "smap": 22.8,
                        "ecostress": 31.4,
                        "srtm": 2.8,
                        "bare_days": 134,
                    },
                    {
                        "zone_code": "MZ-02",
                        "name": "MZ-02 Northeast Eroded Crest (13.2 ha)",
                        "coords": [[40.9195, -98.3420], [40.9195, -98.3370], [40.9165, -98.3370], [40.9165, -98.3420]],
                        "smap": 17.2,
                        "ecostress": 35.8,
                        "srtm": 5.1,
                        "bare_days": 154,
                    },
                    {
                        "zone_code": "MZ-03",
                        "name": "MZ-03 Southwest Bottomland (13.8 ha)",
                        "coords": [[40.9165, -98.3470], [40.9165, -98.3420], [40.9135, -98.3420], [40.9135, -98.3470]],
                        "smap": 27.4,
                        "ecostress": 29.8,
                        "srtm": 1.2,
                        "bare_days": 116,
                    },
                    {
                        "zone_code": "MZ-04",
                        "name": "MZ-04 Southeast Drainage Swale (13.5 ha)",
                        "coords": [[40.9165, -98.3420], [40.9165, -98.3370], [40.9135, -98.3370], [40.9135, -98.3420]],
                        "smap": 24.1,
                        "ecostress": 31.9,
                        "srtm": 3.6,
                        "bare_days": 128,
                    },
                ],
                "monthly": [
                    ("Jan", 16, 15, 24.5, 0.16),
                    ("Feb", 20, 24, 25.2, 0.17),
                    ("Mar", 44, 52, 26.8, 0.21),
                    ("Apr", 68, 88, 27.4, 0.32),
                    ("May", 112, 126, 28.2, 0.54),
                    ("Jun", 104, 162, 24.6, 0.79),
                    ("Jul", 82, 178, 19.4, 0.84),
                    ("Aug", 76, 158, 18.2, 0.78),
                    ("Sep", 56, 114, 19.8, 0.46),
                    ("Oct", 42, 66,  21.5, 0.22),
                    ("Nov", 26, 30,  23.0, 0.18),
                    ("Dec", 18, 16,  24.0, 0.16),
                ],
            },
        ]

        for p_item in parcels_data:
            parcel = FieldParcel.objects.create(
                slug=p_item["slug"],
                label=p_item["label"],
                center_lat=p_item["center_lat"],
                center_lon=p_item["center_lon"],
                default_soil=p_item["default_soil"],
                default_water=p_item["default_water"],
                default_rotation=p_item["default_rotation"],
            )
            for z in p_item["zones"]:
                ManagementZone.objects.create(parcel=parcel, **z)
            for idx, (m_label, gpm, et0, smap, ndvi) in enumerate(p_item["monthly"], start=1):
                MonthlyClimate.objects.create(
                    parcel=parcel,
                    month_order=idx,
                    month_label=m_label,
                    gpm=gpm,
                    et0=et0,
                    smap=smap,
                    ndvi=ndvi,
                )

        crops_data = [
            ("Winter Rye (Secale cereale)", "Cover & Soil Builder", 240, 150, 0, -25,
             "Scavenges residual soil nitrate; prevents winter wind and raindrop erosion on bare slopes."),
            ("Daikon Tillage Radish", "Cover & Soil Builder", 210, 180, 0, -4,
             "Deep taproot bio-drills compacted clay plow pans and increases spring water infiltration."),
            ("Crimson Clover (Trifolium incarnatum)", "N-Fixing Legume", 290, 95, 75, -10,
             "Fixes atmospheric nitrogen ahead of maize or sorghum; requires topsoil pH above 6.0."),
            ("Grain Sorghum (Sorghum bicolor)", "Drought-Tolerant Cash", 380, 165, 0, 2,
             "C4 waxy-leaf physiology maintains yield during +36°C heatwaves with 34% less water than maize."),
            ("Kabuli Chickpea (Cicer arietinum)", "N-Fixing Legume / Cash", 310, 110, 60, -3,
             "Low-water spring pulse that breaks cereal root-rot disease cycles and adds biological nitrogen."),
            ("Alfalfa / Lucerne (Medicago sativa)", "N-Fixing Perennial Strip", 560, 240, 165, -20,
             "Multi-year deep-rooted perennial ideal for stabilizing steep erosion-prone sub-field benches."),
            ("Mungbean (Vigna radiata)", "N-Fixing Short Catch Crop", 270, 85, 55, 4,
             "65-day summer catch crop sown after winter wheat harvest to eliminate summer bare fallow."),
            ("Early Winter Barley", "Drought-Tolerant Cash", 330, 130, 0, -14,
             "Matures 14–18 days earlier than winter wheat, escaping peak June–July evaporative stress."),
            ("Sorghum-Sudangrass Hybrid", "Cover & Forage Builder", 390, 190, 0, 1,
             "High-biomass summer cover that suppresses nematodes and rapidly builds soil organic carbon."),
            ("Spring Oats (Avena sativa)", "Cover & Nurse Crop", 280, 105, 0, -6,
             "Winter-kills naturally in continental frosts, leaving a clean no-till mulch mat for spring planting."),
        ]

        for name, role, water_mm, root_cm, n_fix_kg, frost_c, notes in crops_data:
            CropTrait.objects.create(
                name=name,
                role=role,
                water_mm=water_mm,
                root_cm=root_cm,
                n_fix_kg=n_fix_kg,
                frost_c=frost_c,
                notes=notes,
            )

        self.stdout.write(self.style.SUCCESS("TerraTurn database seeded: 3 parcels, 12 zones, 36 climate records, 10 crops."))