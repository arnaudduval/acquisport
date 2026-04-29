"""
Exemple simple : cardio + affichage
"""

import asyncio
import threading
import time
from collections import deque


from bleak import BleakClient

# ----------------------------------------
# Config
# ----------------------------------------

ADDRESS = "EA:2B:E3:98:BE:A2"
HR_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
WINDOW = 60 # secondes affichées

PLOT_BACKEND = "pyqtgraph"  #"matplotlib"


# ----------------------------------------
# Buffers
# ----------------------------------------

times = deque()
hr_values = deque()
rr_values = deque()

data_lock = threading.Lock()

t0 = time.time()

# ----------------------------------------
# BLE parsing
# ----------------------------------------

def handle_hr(_, data):
    global times, hr_values, rr_values

    now = time.time() - t0
    flags = data[0]

    offset = 1

    # Heart rate format
    # # bit 0 : format (0 = uint8, 1 = uint16)
    if flags & 0x01:
        hr = int.from_bytes(data[offset:offset+3], byteorder="little")
        offset += 2
    else:
        hr = data[offset]
        offset += 1

    # Energy expended present
    if flags & 0x08:
        offset += 2

    rr = None

    # RR intervals present
    if flags & 0x10:
        rr_raw = int.from_bytes(data[offset:offset+2], "little")
        rr = rr_raw / 1024 * 1000  # ms

    with data_lock:
        times.append(now)
        hr_values.append(hr)

        if rr is not None:
            print("RR")
            rr_values.append((now, rr))

        # Purge old values
        while times and now - times[0] > WINDOW:
            times.popleft()
            hr_values.popleft()

        while rr_values and now - rr_values[0][0] > WINDOW:
            rr_values.popleft()


# ----------------------------------------
# BLE loop
# ----------------------------------------

async def ble_loop():
    async with BleakClient(ADDRESS) as client:
        print("Connecté")

        await client.start_notify(HR_CHAR_UUID, handle_hr)

        while True:
            await asyncio.sleep(1)


def run_ble():
    asyncio.run(ble_loop())

# ----------------------------------------
# MATPLOTLIB BACKEND
# ----------------------------------------

def run_matplotlib():
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    line_hr, = ax1.plot([], [])
    line_rr, = ax2.plot([], [])

    def update(frame):
        if not times:
            return line_hr, line_rr

        x = list(times)

        line_hr.set_data(x, list(hr_values))

        if rr_values:
            rr_x = [v[0] for v in rr_values]
            rr_y = [v[1] for v in rr_values]
            line_rr.set_data(rr_x, rr_y)

            ax2.set_xlim(max(0, x[-1] - WINDOW), x[-1])
            ax2.set_ylim(min(rr_y) - 50, max(rr_y) + 50)

        ax1.set_xlim(max(0, x[-1] - WINDOW), x[-1])
        ax1.set_ylim(min(hr_values) - 5, max(hr_values) + 5)

        return line_hr, line_rr

    FuncAnimation(fig, update, interval=200)
    plt.show()

# ----------------------------------------
# PyQtGraph backend
# ----------------------------------------
def run_pyqtgraph():
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtWidgets, QtCore

    app = QtWidgets.QApplication([])


    win = pg.GraphicsLayoutWidget(show=True, title="Cardio Live")
    win.resize(1200, 800)

    plot_hr = win.addPlot(title="Fréquence cardiaque")
    curve_hr = plot_hr.plot()

    win.nextRow()

    plot_rr = win.addPlot(title="RR Interval")
    curve_rr = plot_rr.plot()

    def update():
        with data_lock:
            if not times:
                return

            x = list(times)
            hr = list(hr_values)
            rr = list(rr_values)

        curve_hr.setData(x, hr)

        if rr:
            rr_x = [v[0] for v in rr]
            rr_y = [v[1] for v in rr]
            curve_rr.setData(rr_x, rr_y)

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(50)

    app.exec()

# ----------------------------------------
# Main
# ----------------------------------------

threading.Thread(target=run_ble, daemon=True).start()

if PLOT_BACKEND == "matplotlib":
    run_matplotlib()
elif PLOT_BACKEND == "pyqtgraph":
    run_pyqtgraph()
else:
    raise ValueError("Backend inconnu")
