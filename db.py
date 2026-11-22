from pathlib import Path
import sqlite3


DB_PATH = Path(__file__).resolve().with_name("weather.db")


def create_table(db_path=DB_PATH):
    connection = sqlite3.connect(db_path)

    try:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS weather_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fetched_at TEXT NOT NULL,
                    temperature_c REAL NOT NULL,
                    wind_speed_kmh REAL NOT NULL
                )
            """)

    finally:
        connection.close()


def insert_weather(data, db_path=DB_PATH):
    connection = sqlite3.connect(db_path)

    try:
        with connection:
            connection.execute("""
                INSERT INTO weather_log (
                    fetched_at,
                    temperature_c,
                    wind_speed_kmh
                )
                VALUES (?, ?, ?)
            """, (
                data["fetched_at"],
                data["temperature_c"],
                data["wind_speed_kmh"]
            ))

    finally:
        connection.close()