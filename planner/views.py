import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .services.nasa_client import fetch_nasa_power_telemetry
from .services.scoring import evaluate_rotation_strategies


def planner_dashboard(request):
    """
    Главная страница TerraTurn. Передаёт стартовую телеметрию NASA POWER
    и полный справочник из 10 культур.
    """
    default_parcels = {
        "sirdaryo": {
            "label": "Sirdaryo Plot 04 (42.4 ha)",
            "center": [40.4885, 68.7140],
            "defaultSoil": "clay_loam",
            "defaultWater": "deficit",
            "defaultRotation": "cotton_wheat_fallow",
        },
        "yangiyul": {
            "label": "Yangiyul North (68.0 ha)",
            "center": [41.1240, 69.0420],
            "defaultSoil": "silt_loam",
            "defaultWater": "drip_pivot",
            "defaultRotation": "wheat_monocrop",
        },
        "platte": {
            "label": "Platte Pivot 12 (54.5 ha)",
            "center": [40.9165, -98.3420],
            "defaultSoil": "silt_loam",
            "defaultWater": "rainfed",
            "defaultRotation": "corn_soy_fallow",
        },
    }

    initial_nasa = fetch_nasa_power_telemetry(40.4885, 68.7140)

    crops_catalog = [
        {
            "name": "Winter Rye (Secale cereale)",
            "role": "Cover & Soil Builder",
            "waterMm": 240,
            "rootCm": 150,
            "nFixKg": 0,
            "frostC": -25,
            "notes": "Scavenges residual soil nitrate; prevents winter wind and raindrop erosion on bare slopes.",
        },
        {
            "name": "Daikon Tillage Radish",
            "role": "Cover & Soil Builder",
            "waterMm": 210,
            "rootCm": 180,
            "nFixKg": 0,
            "frostC": -4,
            "notes": "Deep taproot bio-drills compacted clay plow pans and increases spring water infiltration.",
        },
        {
            "name": "Crimson Clover (Trifolium incarnatum)",
            "role": "N-Fixing Legume",
            "waterMm": 290,
            "rootCm": 95,
            "nFixKg": 75,
            "frostC": -10,
            "notes": "Fixes atmospheric nitrogen ahead of maize or sorghum; requires topsoil pH above 6.0.",
        },
        {
            "name": "Grain Sorghum (Sorghum bicolor)",
            "role": "Drought-Tolerant Cash",
            "waterMm": 380,
            "rootCm": 165,
            "nFixKg": 0,
            "frostC": 2,
            "notes": "C4 waxy-leaf physiology maintains yield during +36°C heatwaves with 34% less water than maize.",
        },
        {
            "name": "Kabuli Chickpea (Cicer arietinum)",
            "role": "N-Fixing Legume / Cash",
            "waterMm": 310,
            "rootCm": 110,
            "nFixKg": 60,
            "frostC": -3,
            "notes": "Low-water spring pulse that breaks cereal root-rot disease cycles and adds biological nitrogen.",
        },
        {
            "name": "Mungbean (Vigna radiata)",
            "role": "N-Fixing Legume / Catch",
            "waterMm": 260,
            "rootCm": 85,
            "nFixKg": 55,
            "frostC": 5,
            "notes": "65-day summer catch crop sown immediately after winter wheat harvest to eliminate bare summer fallow.",
        },
        {
            "name": "Alfalfa / Lucerne (Medicago sativa)",
            "role": "N-Fixing Perennial Strip",
            "waterMm": 520,
            "rootCm": 240,
            "nFixKg": 165,
            "frostC": -18,
            "notes": "Multi-year deep-rooted perennial for steep runoff benches; requires subsoil salinity ECe < 4.0 dS/m.",
        },
        {
            "name": "Early Winter Barley (Hordeum vulgare)",
            "role": "Drought-Tolerant Cash",
            "waterMm": 330,
            "rootCm": 130,
            "nFixKg": 0,
            "frostC": -14,
            "notes": "Matures 14–18 days earlier than winter wheat, avoiding peak July ECOSTRESS thermal stress.",
        },
        {
            "name": "Sorghum-Sudangrass Hybrid",
            "role": "Cover & Soil Builder",
            "waterMm": 350,
            "rootCm": 190,
            "nFixKg": 0,
            "frostC": 3,
            "notes": "High-biomass summer cover that suppresses root-knot nematodes and adds rapid organic carbon.",
        },
        {
            "name": "Spring Oats (Avena sativa)",
            "role": "Cover & Soil Builder",
            "waterMm": 270,
            "rootCm": 115,
            "nFixKg": 0,
            "frostC": -6,
            "notes": "Companion nurse crop with legumes; winter-kills cleanly to leave an easy no-till seedbed.",
        },
    ]

    field_initial_state = {
        "apiEndpoint": "/api/v1/nasa-sync/",
        "gridResolution": "30m WGS84 (EPSG:4326)",
        "parcels": default_parcels,
        "initialMonthly": initial_nasa["monthly"],
        "crops": crops_catalog,
    }

    return render(request, "planner/index.html", {
        "field_initial_state": field_initial_state
    })


def api_nasa_sync(request):
    """
    GET /api/v1/nasa-sync/?lat=...&lon=...
    Возвращает 100% реальные данные NASA POWER для указанных координат.
    """
    try:
        lat = float(request.GET.get("lat", 40.4885))
        lon = float(request.GET.get("lon", 68.7140))
    except ValueError:
        return JsonResponse({"error": "Invalid lat/lon coordinates"}, status=400)

    nasa_data = fetch_nasa_power_telemetry(lat, lon)
    return JsonResponse(nasa_data)


@csrf_exempt
@require_POST
def api_evaluate_rotations(request):
    """
    POST /api/v1/rotations/evaluate/
    Серверный скоринг стратегий севооборота.
    """
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    strategies = evaluate_rotation_strategies(body)
    return JsonResponse({"strategies": strategies})