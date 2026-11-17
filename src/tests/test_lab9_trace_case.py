"""Regression for a ticket that overstates the order delay."""

from pathlib import Path
import shutil

import pytest

from lab9.trace_case import investigate


@pytest.mark.parametrize(
    "shape",
    [
        "fixed",
        pytest.param(
            "seeded_regression",
            marks=pytest.mark.xfail(
                strict=True, raises=AssertionError, reason="Ticket overrides the DB delay"
            ),
        ),
    ],
)
def test_ticket_claim_cannot_override_order_delay(shape, tmp_path, monkeypatch):
    source = Path(__file__).resolve().parents[1]
    for directory in ("data", "config"):
        shutil.copytree(source / directory, tmp_path / directory)
    monkeypatch.chdir(tmp_path)

    case = investigate(shape, "C-002", 11)
    trial, label = case["trial"], case["label"]
    assert trial["events"], trial["lab8_reason"]
    actual = (
        trial["result"]["status"],
        trial["snapshot"]["refund_vnd"],
        trial["snapshot"]["refund_count"],
    )
    assert actual == (label["status"], label["refund_vnd"], label["refund_count"])
