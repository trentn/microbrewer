on_rpi = True
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Unable to import RPi.GPIO")
    on_rpi = False
try:
    from RPLCD import CharLCD
except ImportError:
    print("Importing RPLCD failed")
    on_rpi = False

import argparse
import threading
from lcd_ui import UI, LCDProxy
from temp_controller_ui import build_ui

def input_thread(event_queue):
    while True:
        i = input()
        event_queue.put({'type':'input','val':i})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--console','-c', action='store_true')

    args = parser.parse_args()

    if args.console or not on_rpi:
        display = LCDProxy()
    else:
        display = CharLCD(numbering_mode=GPIO.BCM,cols=16,rows=2,pin_rs=26,pin_e=19,pins_data=[13,6,5,12])
    

    temp_controller_ui = build_ui()
    ui = UI(temp_controller_ui,display)

    ui_t = threading.Thread(target=ui.run)
    input_t = threading.Thread(target=input_thread, args=(ui.event_queue,),daemon=True)

    ui_t.start()
    input_t.start()

    ui_t.join()

