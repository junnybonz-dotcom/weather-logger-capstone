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

## Setup

```bash
python3 -m venv env
source env/bin/activate
pip install requests

Initialize the database:
python3 -c "from db import create_table; create_table()"

## Run Manually 
source env/bin/activate
python3 main.py
Example Output:
Logged: {'fetched_at': '2026-09-30T14:33:07.610584', 'temperature_c': 26.1, 'wind_speed_kmh': 2.3}

## Cron Automation
The pipeline runs automatically every 15 minutes.
*/15 * * * * cd /home/ubuntu/capstone && /home/ubuntu/capstone/env/bin/python3 main.py >> /home/ubuntu/capstone/cron.log 2>&1
The command:

* runs from the project directory
* uses the virtual environment's Python interpreter
* runs every 15 minutes
* writes output and errors to cron.log

## Sample SQL Queries
Count collected readings
SELECT COUNT(*) FROM weather_log;
Output: (This is TODAY all Output would be different tomorrow because it constantly changing)
115

## Temperature statistics
SELECT
    MAX(temperature_c) AS hottest,
    MIN(temperature_c) AS coolest,
    AVG(temperature_c) AS average_temp
FROM weather_log;
Output:
30.7|24.2|26.9669565217391

## Average temperature by hour
SELECT
    strftime('%H', fetched_at) AS hour,
    AVG(temperature_c) AS avg_temp,
    COUNT(*) AS readings
FROM weather_log
GROUP BY hour
ORDER BY hour;
Output:
00|28.3666666666667|3
01|29.45|4
02|30.025|4
03|30.32|5
04|30.475|4
05|30.6333333333333|3
06|30.55|4
07|30.45|4
08|29.975|4
09|28.65|2
10|27.6|4
11|26.67|10
12|25.3533333333333|15
13|25.7625|8
14|25.6625|8
15|24.8333333333333|3
16|24.75|4
17|24.7|4
18|24.7|4
19|24.7|3
20|24.625|4
21|24.35|4
22|24.8333333333333|3
23|26.8|4

## Error Handling
The pipeline handles several failure cases:

* API timeouts
* HTTP/API errors
* Unexpected JSON fields
* SQLite/database errors

Specific exceptions are handled instead of using a silent except: pass.

## Troubleshooting
One issue during development involved cron running in a different
environment from an interactive SSH session.

The script worked manually because the virtual environment was active,
but cron does not automatically activate it.

The solution was to call the virtual environment's Python directly:

/home/ubuntu/capstone/env/bin/python3

The cron command also explicitly changes to the project directory so
the relative SQLite path points to the intended database.

## What I Learned
This project combined several skills I had previously studied separately:

* AWS EC2
* Ubuntu/Linux
* Python
* Virtual environments
* HTTP APIs
* JSON
* SQLite
* SQL
* Exception handling
* cron automation
* Logging
* Git/GitHub

The main goal was to connect these technologies into one automated
cloud-hosted system rather than practice them in isolation.

## Finally Save it!
Ctrl + O
Enter
Ctrl + X
