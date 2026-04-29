import time
from core.buffer import get_window
from core.config import (
    SCX_WINDOW_START,
    SCX_WINDOW_END,
    SCX_REFRESH
)

scx_value = None

def align(power_data, speed_data, max_dt=0.2):
    aligned=[]

    for tp, p in power_data:
        nearest = min(
            speed_data,
            key=lambda s: abs(s[0] - tp),
            default=None
        )
        if nearest and abs(nearest[0] - tp) <= max_dt:
            aligned.append((p, nearest[1]))

    return aligned

def compute(aligned):
    vals = []

    for power, speed in aligned:
        if speed > 0:
            vals.append(power /(speed ** 3))

    if not vals:
        return None

    return sum(vals) / len(vals)

def worker():
    global scx_value

    while True:
        power = get_window("power", SCX_WINDOW_START, SCX_WINDOW_END)
        speed = get_window("speed", SCX_WINDOW_START, SCX_WINDOW_END)

        aligned = align(power, speed)

        scx_value = compute(aligned)

        time.sleep(SCX_REFRESH)
