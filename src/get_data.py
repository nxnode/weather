from src.database.models import Weather
from src.database.session import get_session


def get_all_weather():
    with get_session() as session:
        all_weather = session.query(Weather).all()
    return [weather.data for weather in all_weather]


if __name__ == "__main__":
    print(get_all_weather())
