# Weather Logger — Automated Weather Data Pipeline

A Python data pipeline deployed on an Ubuntu AWS EC2 instance. It retrieves current temperature and wind-speed data from the Open-Meteo API, stores timestamped readings in SQLite, and runs automatically every 15 minutes through cron.

## Skills Demonstrated

- Linux and Ubuntu administration on an AWS EC2 virtual machine
- Python functions, HTTP requests, JSON parsing, and exception handling
- SQLite database creation and parameterized SQL queries
- Cron scheduling and log redirection
- Git and GitHub version control
- Troubleshooting differences between interactive shells and scheduled jobs

## Architecture

```text
Open-Meteo API
      |
      v
   fetch.py
      |
      v
 Python dictionary
      |
      v
    db.py
      |
      v
 SQLite (weather.db)
      ^
      |
   main.py
      ^
      |
 cron: every 15 minutes
```

The pipeline collects weather readings, stores them locally, and makes them available for SQL analysis.

## Project Structure

```text
weather-logger-capstone/
├── README.md
├── fetch.py
├── db.py
├── main.py
├── test_insert.py
├── .gitignore
└── capstone/
    ├── original/
    └── redo-oct21/
```

The root-level Python scripts are the main project. The `capstone/` directory contains the original and rebuilt versions used for comparison and gap analysis.

## Requirements

- Python 3
- `pip`
- The `requests` library
- An internet connection for the public API

AWS EC2 and cron are required for the automated cloud deployment, but the Python pipeline can also be run manually on a compatible local machine.

## Setup

From the root of a fresh clone on Ubuntu or another compatible Linux environment:

```bash
git clone https://github.com/junnybonz-dotcom/weather-logger-capstone.git
cd weather-logger-capstone

python3 -m venv env
source env/bin/activate
python3 -m pip install requests
```

Initialize the SQLite table:

```bash
python3 -c "from db import create_table; create_table()"
```

## Run Manually

Activate the virtual environment if it is not already active, then run:

```bash
python3 main.py
```

Example output captured during a real run on September 30, 2026:

```text
Logged: {'fetched_at': '2026-09-30T14:33:07.610584', 'temperature_c': 26.1, 'wind_speed_kmh': 2.3}
```

This is a historical example. Current temperature, wind speed, and timestamps will vary.

## Database Schema

The `weather_log` table stores one row per successful reading:

```sql
CREATE TABLE weather_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at TEXT NOT NULL,
    temperature_c REAL,
    wind_speed_kmh REAL
);
```

The timestamp is stored as text, while temperature and wind speed use numeric fields.

## SQL Analysis

The collected data can be queried to summarize the readings.

### Count collected readings

```sql
SELECT COUNT(*) FROM weather_log;
```

Captured result on September 30, 2026:

```text
115
```

### Temperature statistics

```sql
SELECT
    MAX(temperature_c) AS hottest,
    MIN(temperature_c) AS coolest,
    AVG(temperature_c) AS average_temp
FROM weather_log;
```

Captured output:

```text
30.7|24.2|26.9669565217391
```

### Average temperature by hour

```sql
SELECT
    strftime('%H', fetched_at) AS hour,
    AVG(temperature_c) AS avg_temp,
    COUNT(*) AS readings
FROM weather_log
GROUP BY hour
ORDER BY hour;
```

This query groups readings by hour and calculates the average temperature and number of readings per group. The results depend on the data collected.

## Cron Automation

On the EC2 deployment, the pipeline is scheduled every 15 minutes. The following example uses the deployment path `/home/ubuntu/capstone`:

```cron
*/15 * * * * cd /home/ubuntu/capstone && /home/ubuntu/capstone/env/bin/python3 main.py >> /home/ubuntu/capstone/cron.log 2>&1
```

The job:

- Runs every 15 minutes.
- Changes into the project directory.
- Uses Python from the virtual environment.
- Appends standard output and errors to `cron.log`.

The absolute paths must match the actual deployment location. Cron does not automatically inherit the virtual environment activated in an interactive SSH session.

## Error Handling

The pipeline includes handling for several failure cases:

- API timeouts
- HTTP or API request errors
- Unexpected JSON fields
- SQLite database errors

Specific exceptions are handled instead of silently suppressing all errors with `except: pass`.

## Troubleshooting and What Broke

One development issue involved cron running differently from an interactive SSH session. The script worked manually when the virtual environment was active, but cron did not automatically inherit that environment.

The solution was to specify the virtual environment's Python interpreter directly:

```text
/home/ubuntu/capstone/env/bin/python3
```

The cron command also explicitly changes into the project directory so relative database paths resolve to the intended location.

This project helped me connect previously studied concepts—Linux, Python, APIs, JSON, SQL, SQLite, error handling, and scheduling—into one automated pipeline.

## Security and Files Not Included

The SQLite database, logs, virtual environment, and credentials should not be committed as part of the project. The repository's `.gitignore` should exclude generated files and sensitive local configuration.

No AWS access keys, private keys, account IDs, or personal IP addresses belong in this README.
