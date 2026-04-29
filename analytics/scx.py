import time
from core.buffer import get_window
from core.config import (
    SCX_WINDOW_START,
    SCX_WINDOW_END,
    SCX_REFRESH
)

scx_value = None

def compute(samples):
    vals = []

    for s in samples:
        if s.power is None or s.speed is None:
            continue

        if s.speed <= 0:
            continue

        vals.append(s.power /(s.speed ** 3))

    if not vals:
        return None

    return sum(vals) / len(vals)

def worker():
    global scx_value

    while True:
        samples = get_window(
            SCX_WINDOW_START,
            SCX_WINDOW_END
        )

        scx_value = compute(samples)

        time.sleep(SCX_REFRESH)
