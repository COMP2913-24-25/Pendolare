import pytest
from app.cron_checker import checkTimeValid

def test_check_time_valid():
    cron = "0 12 * * *"
    time = "2023-01-01 12:00:00"
    result = checkTimeValid(cron, time)
    assert result is True

def test_check_time_invalid():
    cron = "0 12 * * *"
    time = "2023-01-01 13:00:00"
    result = checkTimeValid(cron, time)
    assert result is False

def test_check_time_invalid_cron_expression():
    cron = "invalid cron"
    time = "2023-01-01 12:00:00"
    result = checkTimeValid(cron, time)
    print(result)
    assert isinstance(result, str)