import sqlite3

from db import DB_PATH, create_table, insert_weather
from fetch import WeatherFetchError, fetch_weather


def run_once(db_path=DB_PATH, weather_fetcher=fetch_weather):
    try:
        data = weather_fetcher()

        create_table(db_path)
        insert_weather(data, db_path)

    except WeatherFetchError as exc:
        print(f"Weather API error: {exc}")
        return False

    except sqlite3.Error as exc:
        print(f"Database error: {exc}")
        return False

    except (KeyError, TypeError, ValueError) as exc:
        print(f"Invalid weather data: {exc}")
        return False

    print(f"Successfully logged: {data}")
    return True


def main():
    return 0 if run_once() else 1


if __name__ == "__main__":
    raise SystemExit(main())