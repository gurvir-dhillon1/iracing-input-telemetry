import pyqtgraph as pg

class TelemetryGraph(pg.PlotWidget):
  def __init__(self, buffer_size=200):
    super().__init__()
    self.graph_settings = {
      'line_width': 4,
      'throttle_color': 'g',
      'brake_color': 'r',
      'throttle_name': 'throttle',
      'brake_name': 'brake',
      'text_anchor': (0,0.5),
    }
    self.setBackground('black')
    self.getPlotItem().getAxis('bottom').setVisible(False)
    self.getPlotItem().getAxis('left').setVisible(False)
    self.getPlotItem().getViewBox().setMouseEnabled(x=False, y=False)
    self.setYRange(0, 1)

    #self.addLegend()

    self.throttle_line = self.plot([], [], pen=pg.mkPen(self.graph_settings['throttle_color'], width=self.graph_settings['line_width']), name=self.graph_settings['throttle_name'])
    self.brake_line = self.plot([], [], pen=pg.mkPen(self.graph_settings['brake_color'], width=self.graph_settings['line_width']), name=self.graph_settings['brake_name'])

    self.data_len = buffer_size
    self.throttle_data = [0] * self.data_len
    self.brake_data = [0] * self.data_len
    self.x = list(range(self.data_len))

    self.throttle_label = pg.TextItem(color=self.graph_settings['throttle_color'], anchor=self.graph_settings['text_anchor'])
    self.brake_label = pg.TextItem(color=self.graph_settings['brake_color'], anchor=self.graph_settings['text_anchor'])
    self.addItem(self.throttle_label)
    self.addItem(self.brake_label)

  def update_from_worker(self, data: dict):
    new_throttle = data['Throttle']
    new_brake = data['Brake']
    self.throttle_data = self.throttle_data[1:] + [new_throttle]
    self.brake_data = self.brake_data[1:] + [new_brake]

    self.throttle_line.setData(self.x, self.throttle_data)
    self.brake_line.setData(self.x, self.brake_data)

    self.throttle_label.setText(f'{int(self.throttle_data[-1]*100)}')
    self.throttle_label.setPos(self.x[-1]-2, new_throttle)
    self.brake_label.setText(f'{int(self.brake_data[-1]*100)}')
    self.brake_label.setPos(self.x[-1]-2, new_brake)