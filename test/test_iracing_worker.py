import unittest
from unittest.mock import MagicMock, patch
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from iracing_worker import IracingWorker
import sys

class TestIracingWorker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)

    @patch("iracing_worker.IracingClient")
    def test_emit_data_emits_signal(self, mock_client_class):
        mock_client = MagicMock()
        mock_client.poll_data.return_value = {
            "Throttle": 1.0,
            "Brake": 0.0
        }
        mock_client_class.return_value = mock_client

        worker = IracingWorker()
        worker.running = True

        received = []

        def capture(data):
            received.append(data)

        worker.data_ready.connect(capture)

        worker.emit_data()

        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]["Throttle"], 1.0)
        mock_client.poll_data.assert_called_once()

    @patch("iracing_worker.IracingClient")
    def test_run_starts_timer(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        worker = IracingWorker(poll_rate_ms=10)
        worker.run()

        self.assertTrue(worker.running)
        self.assertIsInstance(worker.timer, QTimer)
        self.assertTrue(worker.timer.isActive())
        mock_client.start_connection.assert_called_once()

    @patch("iracing_worker.IracingClient")
    def test_stop_stops_timer_and_client(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        worker = IracingWorker()
        worker.run()
        worker.stop()

        self.assertFalse(worker.running)
        self.assertFalse(worker.timer.isActive())
        mock_client.destroy_connection.assert_called_once()
