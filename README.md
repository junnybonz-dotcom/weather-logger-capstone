# Weather Logger

A Python data pipeline running on an Ubuntu AWS EC2 instance.
It polls the Open-Meteo API every 15 minutes using cron and stores
timestamped temperature and wind-speed readings in a SQLite database.

## What It Does

1. Requests current weather data from Open-Meteo.
2. Parses the JSON response.
3. Extracts temperature and wind speed.
4. Stores the data in SQLite.
5. Runs automatically every 15 minutes with cron.
6. Allows the collected data to be queried with SQL.

## Architecture

Open-Meteo API
    ↓
fetch.py
    ↓
Python dictionary
    ↓
db.py
    ↓
SQLite (weather.db)
    ↓
cron automation

## Project Structure

    capstone/
    ├── fetch.py
    ├── db.py
    ├── main.py
    ├── README.md
    └── .gitignore

## Database Schema

```sql
CREATE TABLE weather_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at TEXT NOT NULL,
    temperature_c REAL,
    wind_speed_kmh REAL
);
