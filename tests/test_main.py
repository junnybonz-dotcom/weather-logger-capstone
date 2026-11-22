import sqlite3
import tempfile
import unittest

from pathlib import Path

from fetch import WeatherFetchError
from main import run_once


class MainApplicationTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "weather.db"

        self.data = {
            "fetched_at": "2026-11-22T10:00:00+00:00",
            "temperature_c": 29.5,
            "wind_speed_kmh": 12.4,
        }

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_successful_pipeline(self):
        result = run_once(
            db_path=self.db_path,
            weather_fetcher=lambda: self.data
        )

        self.assertTrue(result)

        connection = sqlite3.connect(self.db_path)

        try:
            count = connection.execute(
                "SELECT COUNT(*) FROM weather_log"
            ).fetchone()[0]

        finally:
            connection.close()

        self.assertEqual(count, 1)

    def test_api_error_does_not_create_database(self):

        def failing_fetch():
            raise WeatherFetchError("Simulated API failure")

        result = run_once(
            db_path=self.db_path,
            weather_fetcher=failing_fetch
        )

        self.assertFalse(result)
        self.assertFalse(self.db_path.exists())

    def test_database_error_is_handled(self):
        invalid_path = (
            Path(self.temp_dir.name)
            / "missing_folder"
            / "weather.db"
        )

        result = run_once(
            db_path=invalid_path,
            weather_fetcher=lambda: self.data
        )

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()