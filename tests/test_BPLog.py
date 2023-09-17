import csv
from pathlib import Path

import pytest

from src import BPLog as BP
from src.BPLog import Datapoint


@pytest.fixture
def bplog():
    mylog = BP.BPLog()
    return mylog


def test_add_measurement_date(bplog):
    bplog.add_measurement(Datapoint(date="230915", sys="120", dia="80"))
    assert bplog.measurements[0].date == "230915"


def test_add_measurement_sys(bplog):
    bplog.add_measurement(Datapoint(date="230915", sys="120", dia="80"))
    assert bplog.measurements[0].sys == "120"


def test_add_measurement_dia(bplog):
    bplog.add_measurement(Datapoint(date="230915", sys="120", dia="80"))
    assert bplog.measurements[0].dia == "80"


def test_get_unique_dates(bplog):
    expected = []
    assert bplog._get_unique_dates() == expected

    bplog.add_measurement(Datapoint(date="230915", sys="120", dia="80"))
    expected = ["230915"]
    assert bplog._get_unique_dates() == expected

    expected = ["230915", "230916"]
    bplog.add_measurement(Datapoint(date="230916", sys="120", dia="80"))
    assert bplog._get_unique_dates() == expected
    bplog.add_measurement(Datapoint(date="230916", sys="120", dia="80"))
    assert bplog._get_unique_dates() == expected


def test_get_daily_measurements(bplog):
    bplog.add_measurement(Datapoint(date="230915", sys="1", dia="1"))
    bplog.add_measurement(Datapoint(date="230915", sys="2", dia="2"))
    bplog.add_measurement(Datapoint(date="230916", sys="3", dia="3"))

    date = "230915"
    expected = [
        Datapoint(date="230915", sys="1", dia="1"),
        Datapoint(date="230915", sys="2", dia="2"),
    ]
    assert bplog._get_daily_measurements(date) == expected

    date = "230916"
    expected = [
        Datapoint(date="230916", sys="3", dia="3"),
    ]
    assert bplog._get_daily_measurements(date) == expected


def test_calc_averages(bplog):
    daily_measurements = [
        Datapoint(date="230915", sys="120", dia="80"),
        Datapoint(date="230915", sys="140", dia="100"),
    ]
    expected = 130, 90
    assert bplog._calc_averages(daily_measurements) == expected


def test_set_measurements_daily_avg(bplog):
    bplog.add_measurement(Datapoint(date="230901", sys="1", dia="1"))
    expected = [Datapoint("230901", 1, 1)]
    bplog.calc_daily_avg()
    assert bplog.daily_avg == expected

    bplog.add_measurement(Datapoint(date="230901", sys="2", dia="2"))
    expected = [Datapoint("230901", 1, 1)]
    bplog.calc_daily_avg()
    assert bplog.daily_avg == expected

    bplog.add_measurement(Datapoint(date="230901", sys="3", dia="3"))
    expected = [Datapoint("230901", 2, 2)]
    bplog.calc_daily_avg()
    assert bplog.daily_avg == expected


def test_set_measurements_sevenday_avg(bplog):
    bplog.add_measurement(Datapoint(date="230901", sys="1", dia="1"))
    bplog.add_measurement(Datapoint(date="230902", sys="2", dia="2"))
    bplog.add_measurement(Datapoint(date="230903", sys="3", dia="3"))
    bplog.add_measurement(Datapoint(date="230904", sys="4", dia="4"))
    bplog.add_measurement(Datapoint(date="230905", sys="5", dia="5"))
    bplog.add_measurement(Datapoint(date="230906", sys="6", dia="6"))

    expected = []
    bplog.calc_daily_avg()
    bplog.calc_seven_day_avg()
    assert bplog.seven_day_avg == expected

    bplog.add_measurement(Datapoint(date="230907", sys="7", dia="7"))
    bplog.add_measurement(Datapoint(date="230908", sys="8", dia="8"))
    bplog.add_measurement(Datapoint(date="230909", sys="9", dia="9"))

    expected = [
        Datapoint(date="230907", sys=4, dia=4),
        Datapoint(date="230908", sys=5, dia=5),
        Datapoint(date="230909", sys=6, dia=6),
    ]

    bplog.calc_daily_avg()
    bplog.calc_seven_day_avg()
    assert bplog.seven_day_avg == expected


def test_import_from_cvs(bplog):
    test_file = Path('test_file_import_csv.csv')
    with open(test_file, 'w') as file_obj:
        writer = csv.writer(file_obj, lineterminator='\n')
        writer.writerow(('1', '1', '1'))
        writer.writerow(('2', '2', '2'))

    bplog.import_from_csv(test_file)
    expected = [
        Datapoint(date='1', sys='1', dia='1'),
        Datapoint(date='2', sys='2', dia='2'),
    ]
    assert bplog.measurements == expected

    test_file.unlink()
