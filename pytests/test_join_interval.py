from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Literal, Tuple

import bytewax.interval_join.operators.interval as iv
import bytewax.operators as op
from bytewax.dataflow import Dataflow
from bytewax.operators.windowing import ZERO_TD, EventClock
from bytewax.testing import TestingSink, TestingSource, run_main


@dataclass(frozen=True)
class _Event:
    timestamp: datetime
    value: str


def _build_dataflow(
    mode: Literal["complete", "final", "running", "product"],
    inp_left: List[_Event],
    inp_right: List[_Event],
    out_down: List[Tuple[str, str]],
) -> Dataflow:
    clock = EventClock(
        lambda e: e.timestamp, wait_for_system_duration=timedelta(seconds=10)
    )
    gap = timedelta(seconds=2)

    flow = Dataflow("test_df")
    lefts = op.input("inp_left", flow, TestingSource(inp_left))
    rights = op.input("inp_right", flow, TestingSource(inp_right))
    keyed_lefts = op.key_on("key_left", lefts, lambda e: "ALL")
    keyed_rights = op.key_on("key_right", rights, lambda e: "ALL")
    wo = iv.join_interval(
        "join_interval",
        keyed_lefts,
        clock,
        gap,
        gap,
        keyed_rights,
        mode=mode,
    )
    op.inspect("insp", wo.down)
    simplifieds = op.map(
        "simplify",
        wo.down,
        lambda v: tuple(x.value if x is not None else None for x in v[1]),
    )
    op.output("out", simplifieds, TestingSink(out_down))

    return flow


def test_join_interval_complete() -> None:
    align_to = datetime(2022, 1, 1, tzinfo=timezone.utc)
    inp_left = [
        _Event(align_to, "left"),
    ]
    inp_right = [
        _Event(align_to + timedelta(seconds=1), "right1"),
        _Event(align_to + timedelta(seconds=2), "right2"),
    ]
    out_down: List[Tuple[str, str]] = []

    flow = _build_dataflow("complete", inp_left, inp_right, out_down)

    run_main(flow)
    assert out_down == [
        ("left", "right1"),
    ]


def test_join_interval_final() -> None:
    align_to = datetime(2022, 1, 1, tzinfo=timezone.utc)
    inp_left = [
        _Event(align_to, "left"),
    ]
    inp_right = [
        _Event(align_to + timedelta(seconds=1), "right1"),
        _Event(align_to + timedelta(seconds=2), "right2"),
    ]
    out_down: List[Tuple[str, str]] = []

    flow = _build_dataflow("final", inp_left, inp_right, out_down)

    run_main(flow)
    assert out_down == [
        ("left", "right2"),
    ]


def test_join_interval_running() -> None:
    align_to = datetime(2022, 1, 1, tzinfo=timezone.utc)
    inp_left = [
        _Event(align_to, "left"),
    ]
    inp_right = [
        _Event(align_to + timedelta(seconds=1), "right1"),
        _Event(align_to + timedelta(seconds=2), "right2"),
    ]
    out_down: List[Tuple[str, str]] = []

    flow = _build_dataflow("running", inp_left, inp_right, out_down)

    run_main(flow)
    assert out_down == [
        ("left", None),
        ("left", "right1"),
        ("left", "right2"),
    ]


def test_join_interval_product() -> None:
    align_to = datetime(2022, 1, 1, tzinfo=timezone.utc)
    inp_left = [
        _Event(align_to, "left"),
    ]
    inp_right = [
        _Event(align_to + timedelta(seconds=1), "right1"),
        _Event(align_to + timedelta(seconds=2), "right2"),
    ]
    out_down: List[Tuple[str, str]] = []

    flow = _build_dataflow("product", inp_left, inp_right, out_down)

    run_main(flow)
    assert out_down == [
        ("left", "right1"),
        ("left", "right2"),
    ]
