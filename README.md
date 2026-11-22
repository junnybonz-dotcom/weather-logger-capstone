
# Weather Logger — Automated Weather Data Pipeline

[![Weather Logger CI](https://github.com/junnybonz-dotcom/weather-logger-capstone/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/junnybonz-dotcom/weather-logger-capstone/actions/workflows/tests.yml)

A Python data pipeline deployed on an Ubuntu AWS EC2 instance. It retrieves current temperature and wind-speed data from the Open-Meteo API, stores timestamped readings in SQLite, and runs automatically every 15 minutes through cron.

## Features

- Retrieves current weather data from Open-Meteo.
- Validates API responses and measurements.
- Handles request timeouts and HTTP failures.
- Records UTC timestamps.
- Stores weather readings in SQLite.
- Uses parameterized SQL queries.
- Supports automated scheduling through Linux cron.
- Includes automated tests and GitHub Actions CI.

## Architecture

```text
Open-Meteo API
      |
      v
   fetch.py
      |
      v
 Validate data
      |
      v
    main.py
      |
      v
     db.py
      |
      v
 SQLite (weather.db)
      ^
      |
cron: every 15 minutes
```

The application collects weather data, stores it locally, and makes it available for SQL analysis.

## Requirements

- Python 3.12 or newer
- pip
- requests
- Internet access for Open-Meteo API requests

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Setup

Clone the repository:

```bash
git clone https://github.com/junnybonz-dotcom/weather-logger-capstone.git
cd weather-logger-capstone
```

Create and activate a virtual environment.

**Linux / Ubuntu:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Initialize the SQLite table:

```bash
python -c "from db import create_table; create_table()"
```

## Run Manually

Run the pipeline:

```bash
python main.py
```

The application fetches current weather data and inserts a record into `weather.db`.

The database file is stored beside `db.py` by default.

## Database Schema

The `weather_log` table stores one row per successful reading:

```sql
CREATE TABLE IF NOT EXISTS weather_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at TEXT NOT NULL,
    temperature_c REAL NOT NULL,
    wind_speed_kmh REAL NOT NULL
);
```

## SQL Analysis

Count collected readings:

```sql
SELECT COUNT(*) FROM weather_log;
```

Temperature statistics:

```sql
SELECT
    MAX(temperature_c) AS hottest,
    MIN(temperature_c) AS coolest,
    AVG(temperature_c) AS average_temp
FROM weather_log;
```

Average temperature by hour:

```sql
SELECT
    strftime('%H', fetched_at) AS hour,
    AVG(temperature_c) AS avg_temp,
    COUNT(*) AS readings
FROM weather_log
GROUP BY hour
ORDER BY hour;
```

Results depend on the readings collected in the database.

## Cron Automation

The EC2 deployment runs the pipeline every 15 minutes.

Example cron entry from the deployment:

```cron
*/15 * * * * cd /home/ubuntu/capstone && /home/ubuntu/capstone/env/bin/python3 main.py >> /home/ubuntu/capstone/cron.log 2>&1
```

The paths above are deployment-specific. Adjust them to match the actual location of the project and its virtual environment.

The job:

- Runs every 15 minutes.
- Changes to the project directory.
- Uses the virtual environment's Python interpreter.
- Appends standard output and errors to a log file.

Cron does not automatically inherit the virtual environment activated in an interactive SSH session.

## Automated Tests

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

The test suite is organized into:

- `test_fetch.py`
- `test_db.py`
- `test_main.py`

It covers API response handling, SQLite operations, and application behavior.

Tests use mocked API responses and temporary databases. They do not require a live AWS instance or real API requests.

## Continuous Integration

GitHub Actions runs the tests on:

- Python 3.12
- Python 3.13
- Python 3.14

The workflow also performs Python syntax checks.

## Project Structure

```text
weather-logger-capstone/
├── .github/
│   └── workflows/
│       └── tests.yml
├── tests/
│   ├── test_fetch.py
│   ├── test_db.py
│   └── test_main.py
├── capstone/
├── README.md
├── requirements.txt
├── fetch.py
├── db.py
├── main.py
└── .gitignore
```

The `capstone/` directory preserves earlier implementations and rebuild records.

## Error Handling

The pipeline handles:

- API timeouts
- HTTP and connection errors
- Invalid JSON
- Missing or invalid measurements
- SQLite database errors
- Invalid weather data

## Security and Files Not Included

The SQLite database, generated logs, virtual environments, and credentials should not be committed.

Never commit AWS access keys, secret keys, private keys, or sensitive local configuration.

## What I Learned

This project helped me connect Linux, Python, APIs, JSON, SQL, SQLite, error handling, and scheduling into an automated data pipeline.

It also taught me that scheduled processes have a different environment from interactive terminal sessions, so absolute paths and explicit interpreter paths matter.
