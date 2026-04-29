import asyncio
from bleak import BleakClient

from core.bus import event_bus
from core.timebase import now
from core.events import MetricEvent


class BLEDevice:
    CHAR_UUID = None

    def __init__(self, address, source):
        self.address = address
        self.source = source

    def handle(self, _, data):
        parsed = self.parse(data)

        if parsed is None:
            return

        if isinstance(parsed, tuple):
            parsed = [parsed]

        for metric, value in parsed:
            event_bus.put(
                MetricEvent(
                    t=now(),
                    metric=metric,
                    value=value,
                    source=self.source
                )
            )

    def parse(self, data):
        raise NotImplementedError

    async def loop(self):
        while True:
            try:
                print(f"{self.source}: connexion")

                async with BleakClient(self.address) as client:
                    print(f"{self.source}: connecté")

                    await client.start_notify(
                        self.CHAR_UUID,
                        self.handle
                    )

                    try:
                        while client.is_connected:
                            await asyncio.sleep(1)
                    finally:
                        await client.stop_notify(self.CHAR_UUID)

            except Exception as e:
                print(f"{self.source}: {e}")

            await asyncio.sleep(5)

    def run(self):
        asyncio.run(self.loop())