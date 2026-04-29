from acquisition.ble.base import BLEDevice

class HeartRateSensor(BLEDevice):
    CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

    def parse(self, data):
        flags = data[0]
        offset = 1

        if flags & 0x01:
            hr = int.from_bytes(data[offset:offset+2], "little")
        else:
            hr = data[offset]

        return ("hr", hr)