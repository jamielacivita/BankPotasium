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
    expected = []
    assert bplog._get_unique_dates() == expected

    bplog.add_measurement(Measurement(date="230915", sys="120", dia="80"))
    expected = ["230915"]
    assert bplog._get_unique_dates() == expected

    expected = ["230915", "230916"]
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


def test_set_measurements_daily_avg(bplog):
    bplog.add_measurement(Measurement(date="230901", sys="1", dia="1"))
    expected = [["230901", 1, 1]]
    bplog.set_measurements_daily_avg()
    assert bplog.measurements_daily_avg == expected

    bplog.add_measurement(Measurement(date="230901", sys="2", dia="2"))
    expected = [["230901", 1, 1]]
    bplog.set_measurements_daily_avg()
    assert bplog.measurements_daily_avg == expected

    bplog.add_measurement(Measurement(date="230901", sys="3", dia="3"))
    expected = [["230901", 2, 2]]
    bplog.set_measurements_daily_avg()
    assert bplog.measurements_daily_avg == expected


def test_set_measurements_sevenday_avg(bplog):
    bplog.add_measurement(Measurement(date="230901", sys="1", dia="1"))
    bplog.add_measurement(Measurement(date="230902", sys="2", dia="2"))
    bplog.add_measurement(Measurement(date="230903", sys="3", dia="3"))
    bplog.add_measurement(Measurement(date="230904", sys="4", dia="4"))
    bplog.add_measurement(Measurement(date="230905", sys="5", dia="5"))
    bplog.add_measurement(Measurement(date="230906", sys="6", dia="6"))
    bplog.add_measurement(Measurement(date="230907", sys="7", dia="7"))
    bplog.add_measurement(Measurement(date="230908", sys="8", dia="8"))
    bplog.add_measurement(Measurement(date="230909", sys="9", dia="9"))

    expected = [
        ["230907", 4, 4],
        ["230908", 5, 5],
        ["230909", 6, 6],
    ]

    bplog.set_measurements_daily_avg()
    bplog.set_measurements_sevenday_avg()

    assert bplog.measurements_sevenday_avg == expected
