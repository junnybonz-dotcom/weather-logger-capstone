import math
from datetime import datetime, timezone

import requests


API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=10.3157"
    "&longitude=123.8854"
    "&current=temperature_2m,wind_speed_10m"
)

REQUEST_TIMEOUT = 10


class WeatherFetchError(Exception):
    """Raised when weather data cannot be retrieved or validated."""


def fetch_weather():
    try:
        response = requests.get(
            API_URL,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

    except requests.exceptions.Timeout as exc:
        raise WeatherFetchError(
            f"Weather API request timed out after {REQUEST_TIMEOUT}s."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise WeatherFetchError(
            f"Weather API request failed: {exc}"
        ) from exc

    try:
        payload = response.json()

    except ValueError as exc:
        raise WeatherFetchError(
            "Weather API returned invalid JSON."
        ) from exc

    if not isinstance(payload, dict):
        raise WeatherFetchError(
            "Weather API returned an unexpected response."
        )

    current = payload.get("current")

    if not isinstance(current, dict):
        raise WeatherFetchError(
            "Weather API response is missing current weather data."
        )

    try:
        temperature = float(current["temperature_2m"])
        wind_speed = float(current["wind_speed_10m"])

    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherFetchError(
            "Weather API response contains missing or invalid measurements."
        ) from exc

    if not math.isfinite(temperature) or not math.isfinite(wind_speed):
        raise WeatherFetchError(
            "Weather API returned non-finite measurements."
        )

    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        ),
        "temperature_c": temperature,
        "wind_speed_kmh": wind_speed,
    }


if __name__ == "__main__":
    try:
        print(fetch_weather())

    except WeatherFetchError as exc:
        print(f"Weather fetch failed: {exc}")