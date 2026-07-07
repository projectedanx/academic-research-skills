import pytest
from parse_audit_verdict import classify_status

def test_classify_status_pass():
    assert classify_status({"p1": 0, "p2": 0, "p3": 0}) == "PASS"

def test_classify_status_minor():
    assert classify_status({"p1": 0, "p2": 0, "p3": 1}) == "MINOR"
    assert classify_status({"p1": 0, "p2": 0, "p3": 2}) == "MINOR"
    assert classify_status({"p1": 0, "p2": 0, "p3": 3}) == "MINOR"

def test_classify_status_material():
    # p3 > 3
    assert classify_status({"p1": 0, "p2": 0, "p3": 4}) == "MATERIAL"
    assert classify_status({"p1": 0, "p2": 0, "p3": 10}) == "MATERIAL"

    # p1 > 0
    assert classify_status({"p1": 1, "p2": 0, "p3": 0}) == "MATERIAL"
    assert classify_status({"p1": 1, "p2": 0, "p3": 1}) == "MATERIAL"

    # p2 > 0
    assert classify_status({"p1": 0, "p2": 1, "p3": 0}) == "MATERIAL"
    assert classify_status({"p1": 0, "p2": 1, "p3": 3}) == "MATERIAL"

    # p1 > 0 and p2 > 0
    assert classify_status({"p1": 1, "p2": 2, "p3": 5}) == "MATERIAL"
