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
