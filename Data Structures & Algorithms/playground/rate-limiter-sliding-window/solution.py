"""Reference solution — don't open this until you've attempted drill.py.

Mirrors drill.py's signatures so harness.py can run either module.
"""
from collections import defaultdict, deque
from typing import Deque, Dict, Hashable, List, Mapping


def _cleanup(window: Deque[int], timestamp: int, windowLength: int) -> None:
    cutoff = timestamp - windowLength
    while window and window[0] <= cutoff:
        window.popleft()


def rate_limiter(
    requestTimestamps: List[int],
    windowLength: int,
    maxRequests: int,
) -> List[bool]:
    accepted: Deque[int] = deque()
    decisions = []
    for timestamp in requestTimestamps:
        _cleanup(accepted, timestamp, windowLength)
        if len(accepted) < maxRequests:
            decisions.append(True)
            accepted.append(timestamp)
        else:
            decisions.append(False)
    return decisions


def per_entity_rate_limiter(
    requestTimestamps: List[int],
    userIds: List[int],
    experienceIds: List[str],
    windowLength: int,
    maxRequests: int,
) -> List[bool]:
    user_windows: Dict[int, Deque[int]] = defaultdict(deque)
    experience_windows: Dict[str, Deque[int]] = defaultdict(deque)
    decisions = []
    for timestamp, user_id, experience_id in zip(requestTimestamps, userIds, experienceIds):
        user_window = user_windows[user_id]
        experience_window = experience_windows[experience_id]
        _cleanup(user_window, timestamp, windowLength)
        _cleanup(experience_window, timestamp, windowLength)
        if len(user_window) < maxRequests and len(experience_window) < maxRequests:
            decisions.append(True)
            user_window.append(timestamp)
            experience_window.append(timestamp)
        else:
            decisions.append(False)
    return decisions


def multi_field_rate_limiter(
    requestTimestamps: List[int],
    fieldsByName: Mapping[str, List[Hashable]],
    limits: Mapping[str, "tuple[int, int]"],
) -> List[bool]:
    windows: Dict[str, Dict[Hashable, Deque[int]]] = {
        field_name: defaultdict(deque) for field_name in fieldsByName
    }
    decisions = []
    for i, timestamp in enumerate(requestTimestamps):
        current = []
        ok = True
        for field_name, values in fieldsByName.items():
            windowLength, maxRequests = limits[field_name]
            window = windows[field_name][values[i]]
            _cleanup(window, timestamp, windowLength)
            current.append(window)
            if len(window) >= maxRequests:
                ok = False
        decisions.append(ok)
        if ok:
            for window in current:
                window.append(timestamp)
    return decisions
