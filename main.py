on_rpi = True
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Unable to import RPi.GPIO")
    on_rpi = False

import argparse
import threading

from lcd import LCD
from web import WebServer
from properties import SystemProperties



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--console','-c', action='store_true')

    args = parser.parse_args()

    system = SystemProperties()

    lcd_ui = LCD(system, args.console)
    ui_t = threading.Thread(target=lcd_ui.run)
    ui_t.start()

    web = WebServer(system)
    web.start()

    ui_t.join()
    web.shutdown()

    if on_rpi:
        GPIO.cleanup()

    