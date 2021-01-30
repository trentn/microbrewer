try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Unable to import RPi.GPIO")

try:
    from RPLCD import CharLCD
except ImportError:
    print("Importing RPLCD failed")

import threading
from lcd_ui import UI, LCDProxy
from temp_controller_ui import build_ui

def input_thread(event_queue):
    while True:
        i = input()
        event_queue.put({'type':'input','val':i})

if __name__ == '__main__':
    temp_controller_ui = build_ui()
    display = LCDProxy()
    lcd = CharLCD(numbering_mode=GPIO.BCM,cols=16,rows=2,pin_rs=26,pin_e=19,pins_data=[13,6,5,12])
    ui = UI(temp_controller_ui,lcd)

    ui_t = threading.Thread(target=ui.run)
    input_t = threading.Thread(target=input_thread, args=(ui.event_queue,),daemon=True)

    ui_t.start()
    input_t.start()

    ui_t.join()

