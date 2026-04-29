import asyncio
import time

from bleak import BleakClient

from core.bus import event_bus
from core.events import SampleEvent
from core.config import BLE_HR_ADDRESS, HR_CHAR_UUID
from core.timebase import now


def handle_hr(_, data):
    timestamp = now()

    flags = data[0]
    offset = 1

    # Heart rate format
    # # bit 0 : format (0 = uint8, 1 = uint16)
    if flags & 0x01:
        hr = int.from_bytes(data[offset:offset+1], byteorder="little")
    else:
        hr = data[offset]

    event_bus.put(
        SampleEvent(
            t=timestamp,
            hr=hr,
            source="ble_hr"
        )
    )


async def ble_loop():
    async with BleakClient(BLE_HR_ADDRESS) as client:
        print("BLE connecté")

        await client.start_notify(HR_CHAR_UUID, handle_hr)

        while True:
            await asyncio.sleep(1)

def run():
    asyncio.run(ble_loop())