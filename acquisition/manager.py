import threading

from acquisition.ble.hr import HeartRateSensor
from acquisition.ble.power import PowerSensor
from acquisition.ble.csc import CSCSensor

SENSORS = [
    HeartRateSensor("AA:BB:CC:DD:01", "polar"),
    PowerSensor("AA:BB:CC:DD:02", "assioma"),
    CSCSensor("AA:BB:CC:DD:03", "garmin_csc"),
]

SENSORS = [
    HeartRateSensor("EA:2B:E3:98:BE:A2", "Forerunner")
]

def start():
    for sensor in SENSORS:
        threading.Thread(
            target=sensor.run,
            daemon=True
        ).start()