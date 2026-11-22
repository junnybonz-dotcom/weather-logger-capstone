import unittest
from unittest.mock import Mock, patch

import requests

from fetch import (
    API_URL,
    REQUEST_TIMEOUT,
    WeatherFetchError,
    fetch_weather,
)


class FetchWeatherTests(unittest.TestCase):

    @patch("fetch.requests.get")
    def test_successful_weather_fetch(self, mock_get):
        response = Mock()

        response.json.return_value = {
            "current": {
                "temperature_2m": 29.5,
                "wind_speed_10m": 12.4,
            }
        }

        mock_get.return_value = response

        data = fetch_weather()

        mock_get.assert_called_once_with(
            API_URL,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(data["temperature_c"], 29.5)
        self.assertEqual(data["wind_speed_kmh"], 12.4)
        self.assertTrue(data["fetched_at"].endswith("+00:00"))

    @patch("fetch.requests.get")
    def test_timeout_is_handled(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout

        with self.assertRaisesRegex(
            WeatherFetchError,
            "timed out"
        ):
            fetch_weather()

    @patch("fetch.requests.get")
    def test_connection_error_is_handled(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError(
            "Connection failed"
        )

        with self.assertRaisesRegex(
            WeatherFetchError,
            "request failed"
        ):
            fetch_weather()

    @patch("fetch.requests.get")
    def test_invalid_json_is_handled(self, mock_get):
        response = Mock()
        response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = response

        with self.assertRaisesRegex(
            WeatherFetchError,
            "invalid JSON"
        ):
            fetch_weather()

    @patch("fetch.requests.get")
    def test_missing_weather_field_is_handled(self, mock_get):
        response = Mock()

        response.json.return_value = {
            "current": {
                "temperature_2m": 28.0
            }
        }

        mock_get.return_value = response

        with self.assertRaisesRegex(
            WeatherFetchError,
            "missing or invalid"
        ):
            fetch_weather()

    @patch("fetch.requests.get")
    def test_non_finite_measurement_is_rejected(self, mock_get):
        response = Mock()

        response.json.return_value = {
            "current": {
                "temperature_2m": "nan",
                "wind_speed_10m": 12.0,
            }
        }

        mock_get.return_value = response

        with self.assertRaisesRegex(
            WeatherFetchError,
            "non-finite"
        ):
            fetch_weather()


if __name__ == "__main__":
    unittest.main()