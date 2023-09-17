import pytest

from src import BPLog as BP
from src.BPLog import Measurement


@pytest.fixture
def bplog():
    mylog = BP.BPLog()
    return mylog


def test_add_measurement_date(bplog):
    bplog.add_measurement(Measurement(date="230915", sys="120", dia="80"))
    assert bplog.measurements[0].date == "230915"


def test_add_measurement_sys(bplog):
    bplog.add_measurement(Measurement(date="230915", sys="120", dia="80"))
    assert bplog.measurements[0].sys == "120"


def test_add_measurement_dia(bplog):
    bplog.add_measurement(Measurement(date="230915", sys="120", dia="80"))
    assert bplog.measurements[0].dia == "80"


def test_get_unique_dates(bplog):
    expected = set()
    assert bplog._get_unique_dates() == expected

    bplog.add_measurement(Measurement(date="230915", sys="120", dia="80"))
    expected = {"230915"}
    assert bplog._get_unique_dates() == expected

    expected = {"230915", "230916"}
    bplog.add_measurement(Measurement(date="230916", sys="120", dia="80"))
    assert bplog._get_unique_dates() == expected
    bplog.add_measurement(Measurement(date="230916", sys="120", dia="80"))
    assert bplog._get_unique_dates() == expected


def test_get_daily_measurements(bplog):
    bplog.add_measurement(Measurement(date="230915", sys="1", dia="1"))
    bplog.add_measurement(Measurement(date="230915", sys="2", dia="2"))
    bplog.add_measurement(Measurement(date="230916", sys="3", dia="3"))

    date = "230915"
    expected = [
        Measurement(date="230915", sys="1", dia="1"),
        Measurement(date="230915", sys="2", dia="2"),
    ]
    assert bplog._get_daily_measurements(date) == expected

    date = "230916"
    expected = [
        Measurement(date="230916", sys="3", dia="3"),
    ]
    assert bplog._get_daily_measurements(date) == expected


def test_calc_averages(bplog):
    daily_measurements = [
        Measurement(date="230915", sys="120", dia="80"),
        Measurement(date="230915", sys="140", dia="100"),
    ]
    expected = 130, 90
    assert bplog._calc_averages(daily_measurements) == expected
