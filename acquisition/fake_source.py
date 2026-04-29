import time
import math
import random

from core.bus import event_bus
from core.events import MetricEvent
from core.timebase import now

def emit(metric, value, source="fake"):
    event_bus.put(
        MetricEvent(
            t=now(),
            metric=metric,
            value=value,
            source=source
        )
    )


def run():
    while True:
        t = now()

        emit("hr", 135 + 8 * math.sin(t / 6) + random.uniform(-1, 1))
        emit("power", 240 + 35 * math.sin(t / 10) + random.uniform(-5, 5))
        emit("speed", 11.5 + 0.6 * math.sin(t / 8) + random.uniform(-0.1, 0.1))
        emit("cadence", 88 + 4 * math.sin(t / 7) + random.uniform(-1, 1))


        time.sleep(0.1)