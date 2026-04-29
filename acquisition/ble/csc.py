"""
CSC = Cycling Speed and Cadence
"""

from acquisition.ble.base import BLEDevice


class CSCSensor(BLEDevice):
    CHAR_UUID = "00002a5b-0000-1000-8000-00805f9b34fb"

def parse(self, data):
        speed = ...
        cadence = ...

        return [
            ("speed", speed),
            ("cadence", cadence)
        ]