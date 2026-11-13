"""Optional rainfall-based planting signal using the free Open-Meteo forecast API.

Needs internet. If the request fails the caller gets None and the advisor keeps
working offline. The thresholds are ILLUSTRATIVE and must be calibrated by an
agronomist for each region before real use.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.open-meteo.com/v1/forecast"

# Illustrative thresholds (mm of rain over the forecast window).
WAIT_BELOW_MM = 10.0
GO_AT_OR_ABOVE_MM = 25.0


def fetch_daily_rain(lat: float, lon: float, days: int = 7, timeout: float = 6.0) -> list[float] | None:
    qs = urllib.parse.urlencode(
        {"latitude": lat, "longitude": lon, "daily": "precipitation_sum", "forecast_days": days, "timezone": "auto"}
    )
    try:
        with urllib.request.urlopen(f"{API}?{qs}", timeout=timeout) as r:
            data = json.load(r)
        return [float(x or 0.0) for x in data["daily"]["precipitation_sum"]]
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError, OSError):
        return None


def planting_signal(daily_rain_mm: list[float]) -> dict:
    total = round(sum(daily_rain_mm), 1)
    wet_days = sum(1 for x in daily_rain_mm if x >= 1.0)
    if total < WAIT_BELOW_MM:
        level, msg = "wait", "Little rain is forecast. Prepare the field but hold off planting until the soil is moist."
    elif total >= GO_AT_OR_ABOVE_MM and wet_days >= 3:
        level, msg = "go", "Good rain is forecast. If the soil is already moist to planting depth, this is a reasonable time to plant."
    else:
        level, msg = "watch", "Some rain is forecast but it may not be reliable yet. Check soil moisture before planting."
    return {
        "level": level,
        "total_mm": total,
        "wet_days": wet_days,
        "message": msg + " Confirm local planting dates with your extension officer.",
    }
