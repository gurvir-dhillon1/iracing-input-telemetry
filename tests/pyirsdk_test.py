import time
import irsdk

ir = irsdk.IRSDK()
ir.startup()

print('waiting for iracing session...')

while True:
    if ir.is_connected:
        print(ir['Speed'])
        print(ir['Throttle'])
        print(ir['Brake'])
        print(ir['Gear'])
    else:
        print('not connected to a session yet')
        if not ir.is_initialized:
            ir.startup()
            print('attempting to startup iracing session...')
    time.sleep(1)