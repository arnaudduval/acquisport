import socket
import json

from core.bus import event_bus
from core.events import SampleEvent
from core.config import UDP_PORT
from core.timebase import now


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", UDP_PORT))

    print(f"UDP listening on {UDP_PORT}")

    while True:
        data, _ = sock.recvfrom(2048)

        msg = json.loads(data.decode())

        event_bus.put(
            SampleEvent(
                t=now(),
                hr=msg.get("hr"),
                power=msg.get("power"),
                cadence=msg.get("cadence"),
                speed=msg.get("speed"),
                source="udp"
            )
        )