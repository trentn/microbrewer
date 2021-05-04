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
        GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(27, GPIO.RISING, callback=down_button_callback)
        
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(17, GPIO.RISING, callback=up_button_callback)

        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(4, GPIO.RISING, callback=back_button_callback)

        GPIO.setup(22,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(22, GPIO.RISING, callback=select_button_callback)
    
    #input handler callbacks
    def down_button_callback(channel):
        time.sleep(0.04)
        if GPIO.input(channel):
            t0 = time.perf_counter()
            while GPIO.input(channel):
                t1 =time.perf_counter()
                if t1-t0 > 0.5:
                    event_queue.put({'type':'input','val':'down','length':'short'}) 
                    time.sleep(0.1)
                       
            t = t1-t0
            if t < 0.5:
                if t > 0.25:
                    event_queue.put({'type':'input','val':'down','length':'long'})
                else:
                    event_queue.put({'type':'input','val':'down','length':'short'}) 
    
    def up_button_callback(channel):
        time.sleep(0.04)
        if GPIO.input(channel):
            t0 = time.perf_counter()
            while GPIO.input(channel):
                t1 =time.perf_counter()
                if t1-t0 > 0.5:
                    event_queue.put({'type':'input','val':'up','length':'short'}) 
                    time.sleep(0.1)
                       
            t = t1-t0
            if t < 0.5:
                if t > 0.25:
                    event_queue.put({'type':'input','val':'up','length':'long'})
                else:
                    event_queue.put({'type':'input','val':'up','length':'short'}) 
    
    def back_button_callback(channel):
        time.sleep(0.04)
        if GPIO.input(channel):
            event_queue.put({'type':'input','val':'back'})

    def select_button_callback(channel):
        time.sleep(0.04)
        if GPIO.input(channel):
            event_queue.put({'type':'input','val':'select'})

    if on_rpi:
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
        lcd = CharLCD(numbering_mode=GPIO.BCM,cols=16,rows=2,pin_rs=18,pin_e=23,pins_data=[24,25,12,16])
        output_console = False
        
    display = LCDProxy(lcd=lcd)

    temp_controller_ui = build_ui()
    ui = UI(temp_controller_ui,display,output_console)

    ui_t = threading.Thread(target=ui.run)
    input_t = threading.Thread(target=input_thread, args=(ui.event_queue,args.daemon),daemon=True)

    ui_t.start()
    input_t.start()

    ui_t.join()
    if on_rpi:
        GPIO.cleanup()
