from PySide6.QtCore import QObject, Signal, Slot, QTimer
from iracing_client import IracingClient

class IracingWorker(QObject):
  data_ready = Signal(dict)
  def __init__(self, poll_rate_ms=50):
    super().__init__()
    self.client = IracingClient()
    self.timer = QTimer()
    self.timer.setInterval(poll_rate_ms)
    self.timer.timeout.connect(self.client.poll_data)
    self.running = False

  @Slot()
  def run(self):
    self.client.start_connection()
    self.running = True
    self.timer.start()

  @Slot()
  def stop(self):
    self.running = False
    self.client.destroy_connection()