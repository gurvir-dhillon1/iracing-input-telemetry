from PySide6.QtCore import QObject, Signal, Slot, QTimer
from iracing_client import IracingClient

class IracingWorker(QObject):
  data_ready = Signal(dict)
  def __init__(self, poll_rate_ms=50):
    super().__init__()
    self.client = IracingClient()
    self.running = False
    self.poll_rate_ms = poll_rate_ms
    self.timer = None

  def run(self):
    self.client.start_connection()
    self.timer = QTimer()
    self.timer.setInterval(self.poll_rate_ms)
    self.timer.timeout.connect(self.emit_data)
    self.running = True
    self.timer.start()

  @Slot()
  def emit_data(self):
    if self.running:
      self.data_ready.emit(self.client.poll_data())

  @Slot()
  def stop(self):
    self.running = False
    if self.timer:
      self.timer.stop()
      self.timer.deleteLater()
      self.timer = None
    try:
      self.data_ready.disconnect()
    except:
      pass
    if self.client:
      self.client.destroy_connection()