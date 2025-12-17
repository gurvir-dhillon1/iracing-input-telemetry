import unittest
from PySide6.QtWidgets import QApplication
from telemetry_graph import TelemetryGraph
import sys

class TestTelemetryGraph(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # QApplication must exist for Qt widgets
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        self.graph = TelemetryGraph(buffer_size=5)

    def test_initial_buffers(self):
        self.assertEqual(self.graph.throttle_data, [0] * 5)
        self.assertEqual(self.graph.brake_data, [0] * 5)

    def test_update_from_worker_updates_data(self):
        data = {"Throttle": 0.6, "Brake": 0.3}

        self.graph.update_from_worker(data)

        self.assertEqual(self.graph.throttle_data[-1], 0.6)
        self.assertEqual(self.graph.brake_data[-1], 0.3)

    def test_update_shifts_buffer(self):
        for i in range(6):
            self.graph.update_from_worker({
                "Throttle": i / 10,
                "Brake": 0
            })

        self.assertEqual(self.graph.throttle_data, [0.1, 0.2, 0.3, 0.4, 0.5])

    def test_labels_update(self):
        self.graph.update_from_worker({"Throttle": 0.85, "Brake": 0.15})

        self.assertEqual(self.graph.throttle_label.toPlainText(), "85")
        self.assertEqual(self.graph.brake_label.toPlainText(), "15")
