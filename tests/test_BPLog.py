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
