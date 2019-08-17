## Run this on ESP32 with Micropython firmware flashed

import machine as ma
import utime as ut

#     Touch0 >> GPIO4
#     Touch1 >>  Not available on Devkit 30 pin version but available on Devkit 36 pin version 
#     Touch2 >> GPIO2
#     Touch3 >> GPIO15
#     Touch4 >> GPIO13
#     Touch5 >> GPIO12
#     Touch6 >> GPIO14
#     Touch7 >> GPIO27
#     Touch8 >> GPIO33
#     Touch9 >> GPIO32

sensitivity = 600

touch_pins_ids = [4, 2, 15, 13, 12, 14, 27, 33, 32]  # TODO: change order?
touch_sensors = []

naverage = 32
fps = 12
sleepus = int(1000000 / fps / naverage)

touch_measurements = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# init {

for pi in touch_pins_ids:
    ts = ma.TouchPad(ma.Pin(pi))
    ts.config(sensitivity)
    touch_sensors.append(ts)

# } // init

# main loop {

while True:
    for k in range(naverage):
        for i, t in enumerate(touch_sensors):
            touch_measurements[i] += t.read()
        ut.sleep_us(sleepus)

    for i, t in enumerate(touch_measurements):
        touch_measurements[i] /= naverage
        # touch_measurements[i] = int(touch_measurements[i])

    print({"m": touch_measurements})  # goes trough serial to PC

    for i, t in enumerate(touch_measurements):
        touch_measurements[i] *= 0.0

# } // main loop
