import time
import math
import random

from core.bus import event_bus
from core.events import SampleEvent
from core.timebase import now

def run():
    while True:
        t = now()

        hr = 135 + 8 * math.sin(t / 6) + random.uniform(-1, 1)
        power = 240 + 35 * math.sin(t / 10) + random.uniform(-5, 5)
        speed = 11.5 + 0.6 * math.sin(t / 8) + random.uniform(-0.1, 0.1)
        cadence = 88 + 4 * math.sin(t / 7) + random.uniform(-1, 1)

        event_bus.put(
            SampleEvent(
                t=t,
                hr=hr,
                power=power,
                speed=speed,
                cadence=cadence,
                source="fake"
            )
        )

        time.sleep(0.1)