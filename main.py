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
from temp_controller import build_ui
import time

def input_thread(event_queue,is_daemon):
    #button setup
    def setup_buttons():
        #setup down
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(20, GPIO.RISING, callback=down_button_callback)
        
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(21, GPIO.RISING, callback=up_button_callback)

        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(18, GPIO.RISING, callback=back_button_callback)

        GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(23, GPIO.RISING, callback=select_button_callback)
    
    #input handler callbacks
    def down_button_callback(channel):
        time.sleep(0.04)
        if GPIO.input(channel):
            event_queue.put({'type':'input','val':'down'}) 
    
    def up_button_callback(channel):
        time.sleep(0.04)
        if GPIO.input(channel):
            event_queue.put({'type':'input','val':'up'})

    def back_button_callback(channel):
        time.sleep(0.04)
        if GPIO.input(channel):
            event_queue.put({'type':'input','val':'back'})

    def select_button_callback(channel):
        time.sleep(0.04)
        if GPIO.input(channel):
            event_queue.put({'type':'input','val':'select'})


    setup_buttons()
    if not is_daemon:
        while True:
            i = input()
            event_queue.put({'type':'input','val':i})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--console','-c', action='store_true')
    parser.add_argument('--daemon', '-d', action='store_true')

    args = parser.parse_args()

    if args.console or not on_rpi:
        lcd = None
        output_console = True
    else:
        lcd = CharLCD(numbering_mode=GPIO.BCM,cols=16,rows=2,pin_rs=26,pin_e=19,pins_data=[13,6,5,12])
        output_console = False
        
    display = LCDProxy(lcd=lcd)

    temp_controller_ui = build_ui()
    ui = UI(temp_controller_ui,display,output_console)

    ui_t = threading.Thread(target=ui.run)
    input_t = threading.Thread(target=input_thread, args=(ui.event_queue,args.daemon),daemon=True)

    ui_t.start()
    input_t.start()

    ui_t.join()
    GPIO.cleanup()
