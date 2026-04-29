from collections import deque
from core.config import BUFFER_SECONDS


buffers = {
    "hr": deque(),
    "power": deque(),
    "speed": deque(),
    "cadence": deque()
}

def push(event):
    buf = buffers[event.metric]
    buf.append((event.t, event.value))

    while buf and event.t - buf[0][0] > BUFFER_SECONDS:
        buf.popleft()

def snapshot(metric):
    return list(buffers[metric])

def get_window(metric, start_offset, end_offset):
    buf = buffers[metric]

    if not buf:
        return []

    t_now = buf[-1][0]

    t0 = t_now - start_offset
    t1 = t_now - end_offset

    return [(t, v) for t, v in buf if t0 <= t <= t1]