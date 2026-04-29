from acquisition.ble.base import BLEDevice

class PowerSensor(BLEDevice):
    CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

    def parse(self, data):
        power = int.from_bytes(data[2:4], "little", signed=True)
        return ("power", power)
