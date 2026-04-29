import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore

from core.buffer import snapshot
import analytics.scx as scx
from core.config import UI_REFRESH_MS

def run():
    app = QtWidgets.QApplication([])

    win = pg.GraphicsLayoutWidget(show=True, title="Acquisport")
    win.resize(1200,800)

    plot_hr = win.addPlot(title="Heart rate")
    curve_hr = plot_hr.plot()

    win.nextRow()

    plot_power = win.addPlot(title="Power")
    curve_power = plot_power.plot()

    win.nextRow()

    scx_label = pg.LabelItem(justify="right")
    win.addItem(scx_label)

    def update():
        hr_data = snapshot("hr")
        power_data = snapshot("power")

        if hr_data:
            x_hr, y_hr = zip(*hr_data)
            curve_hr.setData(x_hr, y_hr)
            plot_hr.setXRange(max(0, x_hr[-1] - 60), x_hr[-1])

        if power_data:
            x_power, y_power = zip(*power_data)
            curve_power.setData(x_power, y_power)

        if scx.scx_value is not None:
            scx_label.setText(f"SCx: {scx.scx_value:.4f}")

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(UI_REFRESH_MS)

    app.exec()