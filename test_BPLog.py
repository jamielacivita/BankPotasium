import unittest

import pytest

import BPLog as BP

@pytest.fixture
def bplog():
    mylog = BP.BPLog()
    return mylog


def test_add_measurement_date(bplog):
    bplog.add_measurement(["230915","120","80"])
    assert bplog.measurements[0][0] == "230915"

def test_add_measurement_sys(bplog):
    bplog.add_measurement(["230915","120","80"])
    assert bplog.measurements[0][1] == "120"

def test_add_measurement_dia(bplog):
    bplog.add_measurement(["230915","120","80"])
    assert bplog.measurements[0][2] == "80"

