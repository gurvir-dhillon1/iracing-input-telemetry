import irsdk
import time

class IracingClient:
    def __init__(self):
        self.ir = irsdk.IRSDK()
        self.is_connected = False

    def start_connection(self):
        while not self.ir.is_connected:
            if not self.ir.is_initialized:
                self.ir.startup()
            time.sleep(1)
        self.is_connected = True
        return self.is_connected

    def poll_data(self):
        if self.is_connected:
            return {
                'Throttle': self.ir['Throttle'],
                'Brake': self.ir['Brake'],
                'Gear': self.ir['Gear'],
                'Speed': self.ir['Speed']
            }
        return {'Throttle': 0, 'Brake': 0, 'Gear': 0, 'Speed': 0}

    def destroy_connection(self):
        self.ir.shutdown()
        self.is_connected = False
        return not self.is_connected