import argparse
import json
from datetime import datetime, timedelta

from src.database.models import Weather
from src.database.session import get_session

TIME_DELTA = 120


def get_weather(location):
    with get_session() as session:
        weather = (
            session.query(Weather)
            .filter(Weather.location == location)
            .order_by(Weather.data["dt"].desc())
            .first()
        )
    return weather


def add_weather(location, weather):
    weather = Weather(location=location, data=weather)
    with get_session() as session:
        session.add(weather)
        session.commit()


def call_api():
    with open("./example.json", "r", encoding="utf-8") as file:
        return json.loads(file.read())


def main(args):
    weather = get_weather(args.location).data
    print(weather["dt"])
    if not weather:
        weather = call_api()
        add_weather(args.location, weather)
    else:
        weather_date = datetime.fromtimestamp(weather["dt"])
        now = datetime.now()
        current_delta = (now - weather_date).total_seconds()
        print(current_delta)
        if current_delta > TIME_DELTA:
            weather = call_api()
            add_weather(args.location, weather)
    return weather


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ProgramName",
        description="What the program does",
        epilog="Text at the bottom of help",
    )
    parser.add_argument("-l", "--location")
    parsed_args = parser.parse_args()
    print(main(parsed_args))
