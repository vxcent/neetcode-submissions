"""Rate Limiter (Sliding Window) — attempt this yourself, then check with harness.py.

Run:
    cd "Data Structures & Algorithms/playground/rate-limiter-sliding-window"
    python harness.py

Fill in the three TODOs below. Don't peek at solution.py until you've got
Part 1 and Part 2 passing on your own — the harness tells you exactly which
case broke and why.
"""
from collections import defaultdict, deque
from typing import Deque, Dict, Hashable, List, Mapping


# ---------------------------------------------------------------------------
# Part 1 — global sliding-window limiter
# ---------------------------------------------------------------------------
def rate_limiter(
    requestTimestamps: List[int],
    windowLength: int,
    maxRequests: int,
) -> List[bool]:
    """
    Return True for each accepted request and False for each denied request.
    A request at time t looks back over the half-open window (t - windowLength, t].
    Only accepted requests count against future capacity.
    """
    # TODO: maintain a deque of accepted timestamps still inside the window.
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part 2 — independent per-user and per-experience limits
# ---------------------------------------------------------------------------
def per_entity_rate_limiter(
    requestTimestamps: List[int],
    userIds: List[int],
    experienceIds: List[str],
    windowLength: int,
    maxRequests: int,
) -> List[bool]:
    """
    Return True when the request is allowed by BOTH:
      1. its user's sliding window
      2. its experience's sliding window
    A request only counts against a window if it's ultimately accepted.
    """
    # TODO: one deque per user id, one deque per experience id.
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Bonus — arbitrary dimensions, each with its own (windowLength, maxRequests)
# ---------------------------------------------------------------------------
def multi_field_rate_limiter(
    requestTimestamps: List[int],
    fieldsByName: Mapping[str, List[Hashable]],
    limits: Mapping[str, "tuple[int, int]"],
) -> List[bool]:
    """
    fieldsByName: e.g. {"user": [...], "experience": [...], "ip": [...]}
    limits: e.g. {"user": (60, 100), "experience": (60, 500), "ip": (60, 50)}
    A request is accepted only if every dimension has capacity in its own window.
    """
    # TODO: generalize part 2 to N dimensions, each with its own window/cap.
    raise NotImplementedError
