import pyqtgraph as pg
import math
from PySide6.QtCore import QTimer

class TelemetryGraph(pg.PlotWidget):
  def __init__(self, buffer_size=200):
    super().__init__()

    self.setBackground('black')
    self.getPlotItem().getAxis('bottom').setVisible(False)
    self.getPlotItem().getAxis('left').setVisible(False)
    self.getPlotItem().getViewBox().setMouseEnabled(x=False, y=False)

    #self.addLegend()

    self.throttle_line = self.plot([], [], pen=pg.mkPen('g', width=2), name='throttle')
    self.brake_line = self.plot([], [], pen=pg.mkPen('r', width=2), name='brake')

    self.data_len = buffer_size
    self.throttle_data = [0] * self.data_len
    self.brake_data = [0] * self.data_len
    self.x = list(range(self.data_len))

    self.throttle_label = pg.TextItem(color='g', anchor=(0,0.5))
    self.brake_label = pg.TextItem(color='r', anchor=(0,0.5))
    self.addItem(self.throttle_label)
    self.addItem(self.brake_label)

    self.timer = QTimer()
    self.timer.timeout.connect(self.update_data)
    self.timer.start(50)

    self.t = 0
  
  def update_data(self):
    self.t += 0.05
    new_throttle = (math.sin(self.t) + 1) / 2
    new_brake = (math.sin(self.t + math.pi/2) + 1) / 2

    self.throttle_data = self.throttle_data[1:] + [new_throttle]
    self.brake_data = self.brake_data[1:] + [new_brake]

    self.throttle_line.setData(self.x, self.throttle_data)
    self.brake_line.setData(self.x, self.brake_data)

    self.throttle_label.setText(f'{int(self.throttle_data[-1]*100)}')
    self.throttle_label.setPos(self.x[-1]-2, new_throttle)
    self.brake_label.setText(f'{int(self.brake_data[-1]*100)}')
    self.brake_label.setPos(self.x[-1]-2, new_brake)