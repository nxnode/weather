from copy import deepcopy
from datetime import datetime
from unittest.mock import patch

from src.weather import main

MOCK_DATA = {
    "dt": 1673317565,
}


class Args:
    def __init__(self) -> None:
        self.zipcode = 72532


@patch("src.weather.get_weather")
def test_main(mock_get_weather):
    mock_data = deepcopy(MOCK_DATA)
    mock_data["dt"] = datetime.now().timestamp()
    mock_get_weather.return_value = mock_data
    assert main(Args()) == mock_data


@patch("src.weather.call_api")
def test_main(mock_get_weather):
    mock_data = deepcopy(MOCK_DATA)
    mock_data["dt"] = datetime.now().timestamp()
    mock_get_weather.return_value = mock_data
    assert main(Args()) == mock_data
