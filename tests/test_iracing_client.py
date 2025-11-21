import unittest
from unittest.mock import MagicMock, patch
from iracing_client import IracingClient

class TestIracingClient(unittest.TestCase):

    @patch("iracing_client.irsdk.IRSDK")
    def test_start_connection_sets_is_connected(self, mock_irsdk_class):
        mock_irsdk = MagicMock()
        mock_irsdk.is_connected = True
        mock_irsdk.is_initialized = True
        mock_irsdk_class.return_value = mock_irsdk

        client = IracingClient()
        connected = client.start_connection()
        
        self.assertTrue(connected)
        self.assertTrue(client.is_connected)
        mock_irsdk.startup.assert_not_called()  # Already initialized/connected

    @patch("iracing_client.irsdk.IRSDK")
    def test_poll_data_returns_correct_dict(self, mock_irsdk_class):
        mock_irsdk = MagicMock()
        mock_irsdk.is_connected = True
        mock_irsdk.__getitem__.side_effect = lambda key: {"Throttle":0.5,"Brake":0.2,"Gear":3,"Speed":120}[key]
        mock_irsdk_class.return_value = mock_irsdk

        client = IracingClient()
        client.is_connected = True
        data = client.poll_data()

        self.assertEqual(data['Throttle'], 0.5)
        self.assertEqual(data['Brake'], 0.2)
        self.assertEqual(data['Gear'], 3)
        self.assertEqual(data['Speed'], 120)

    @patch("iracing_client.irsdk.IRSDK")
    def test_destroy_connection_sets_is_connected_false(self, mock_irsdk_class):
        mock_irsdk = MagicMock()
        mock_irsdk_class.return_value = mock_irsdk

        client = IracingClient()
        client.is_connected = True
        result = client.destroy_connection()

        self.assertFalse(client.is_connected)
        mock_irsdk.shutdown.assert_called_once()
        self.assertTrue(result)
