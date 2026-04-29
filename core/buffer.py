from collections import deque
from core.config import BUFFER_SECONDS


buffer = deque()

def push(event):
    buffer.append(event)

    while buffer and event.t - buffer[0].t > BUFFER_SECONDS:
        buffer.popleft()

def snapshot():
    return list(buffer)

def get_window(start_offset, end_offset):
    if not buffer:
        return []

    t_now = buffer[-1].t

    t0 = t_now - start_offset
    t1 = t_now - end_offset

    return [s for s in buffer if t0 <= s.t <= t1]