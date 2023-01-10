import argparse
import json
import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

from src.database.models import Weather
from src.database.session import get_session

TIME_DELTA = 30

load_dotenv()
API_KEY = os.getenv("API_KEY")
ZIPCODE = os.getenv("ZIP")


def get_weather(zipcode):
    with get_session() as session:
        weather = (
            session.query(Weather)
            .filter(Weather.location == zipcode)
            .order_by(Weather.data["dt"].desc())
            .first()
        )
    return weather.data if weather else weather


def add_weather(zipcode, weather):
    weather = Weather(location=zipcode, data=weather)
    with get_session() as session:
        session.add(weather)
        session.commit()


def call_api(zipcode):
    # with open("./example.json", "r", encoding="utf-8") as file:
    #     return json.loads(file.read())
    url_args = {"zip": f"{zipcode},US", "appid": API_KEY, "units": "imperial"}
    r = requests.get("https://api.openweathermap.org/data/2.5/weather", params=url_args)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        if r.status_code == 404:
            raise ValueError("No city found")
        raise
    return r.json()


def main(args):
    weather = get_weather(args.zipcode)
    if not weather:
        print("first api call")
        weather = call_api(args.zipcode)
        add_weather(args.zipcode, weather)
    else:
        weather_date = datetime.fromtimestamp(weather["dt"])
        now = datetime.now()
        current_delta = (now - weather_date).total_seconds()
        print(weather)
        print(datetime.now().timestamp())
        print(weather["dt"])
        print(current_delta)
        if current_delta > TIME_DELTA:
            weather = call_api(args.zipcode)
            add_weather(args.zipcode, weather)
    return weather


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ProgramName",
        description="What the program does",
        epilog="Text at the bottom of help",
    )
    parser.add_argument("-z", "--zipcode", default=ZIPCODE)
    parsed_args = parser.parse_args()
    print(main(parsed_args))
