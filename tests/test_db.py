import sqlite3
import tempfile
import unittest

from pathlib import Path

from db import create_table, insert_weather


class WeatherDatabaseTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_weather.db"

        self.data = {
            "fetched_at": "2026-11-22T10:00:00+00:00",
            "temperature_c": 29.5,
            "wind_speed_kmh": 12.4,
        }

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_table(self):
        create_table(self.db_path)

        connection = sqlite3.connect(self.db_path)

        try:
            result = connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='weather_log'"
            ).fetchone()

        finally:
            connection.close()

        self.assertIsNotNone(result)

    def test_table_creation_is_idempotent(self):
        create_table(self.db_path)
        create_table(self.db_path)

        self.assertTrue(self.db_path.exists())

    def test_insert_weather(self):
        create_table(self.db_path)
        insert_weather(self.data, self.db_path)

        connection = sqlite3.connect(self.db_path)

        try:
            result = connection.execute("""
                SELECT fetched_at, temperature_c, wind_speed_kmh
                FROM weather_log
            """).fetchone()

        finally:
            connection.close()

        self.assertEqual(result, (
            "2026-11-22T10:00:00+00:00",
            29.5,
            12.4,
        ))


if __name__ == "__main__":
    unittest.main()