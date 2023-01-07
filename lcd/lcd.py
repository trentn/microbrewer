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

import queue
import time
import threading

from .lcd_proxy import LCDProxy
from .views import build_menu


class LCD(object):
    def __init__(self, system, console=False):
        self.console = console
        if not on_rpi:
            self.console = True
        
        if self.console:
            lcd = None
        else:
            lcd = CharLCD(numbering_mode=GPIO.BCM,cols=16,rows=2,pin_rs=18,pin_e=23,pins_data=[24,25,12,16])
            
        self.display = LCDProxy(lcd=lcd)
        
        self.current_elem = build_menu(system.burner, system.temp, system.wifi_config)
        
        self.prev_menus = []
        
        self.update_display()
        self.event_queue = queue.Queue()

    def run(self):
        threading.Thread(target=self.input_thread, args=(self.event_queue,),daemon=True).start()

        self.current_elem.start(self.event_queue)

        if(self.console):
            def print_display(): 
                print(f"\033[;H{self.display}", end="", flush=True)
            print_display()
        
        while True:
            e = self.event_queue.get()
            if e['type'] == 'input':
                if e['val'] == 'quit':
                    break
                self.handle_input(e)
                self.update_display()
            if e['type'] == 'display_update':
                self.update_display()
            if(self.console):
                print_display()
    
    def handle_input(self,event):
        if event['val'] == 'up':
            self.current_elem.scroll(dir='up',length=event['length'])
        
        elif event['val'] == 'down':
            self.current_elem.scroll(dir='down',length=event['length'])
        
        elif event['val'] == 'select':
            select = self.current_elem.select(self.event_queue)
            if select:
                self.current_elem.stop()
                self.current_elem = select
                self.current_elem.start(self.event_queue)

        elif event['val'] == 'cycle':
            self.current_elem.cycle()
        
        elif event['val'] == 'back':
            back = self.current_elem.back()
            if back:
                self.current_elem.stop()
                self.current_elem = back
                self.current_elem.start(self.event_queue)

        elif event['val'] == 'back_space':
            self.current_elem.back_space(self.event_queue)

    def update_display(self):
        self.display.clear()
        lines = self.current_elem.get_display()
        for i,line in enumerate(lines):
            self.display.cursor_pos = (i,0)
            self.display.write_string(line)
        self.display.update()


    def input_thread(self, event_queue):
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
                t0 = time.perf_counter()
                while GPIO.input(channel):
                    t1 = time.perf_counter()
                
                t = t1-t0
                if t > 0.5:
                    event_queue.put({'type':'input','val':'back'})
                else:
                    event_queue.put({'type':'input','val':'back_space'})

        def select_button_callback(channel):
            time.sleep(0.04)
            if GPIO.input(channel):
                event_queue.put({'type':'input','val':'select'})

        if on_rpi:
            setup_buttons()
        if self.console:
            while True:
                i = input()
                if i == 'w':
                    event_queue.put({'type':'input','val':'up','length':'short'})
                elif i == 'ww':
                    event_queue.put({'type':'input','val':'up','length': 'long'})
                elif i == 's':
                    event_queue.put({'type':'input','val':'down','length': 'short'})
                elif i == 'ss':
                    event_queue.put({'type':'input','val':'down','length': 'long'})
                elif i == 'a':
                    event_queue.put({'type':'input','val':'back'})
                elif i == 'aa':
                    event_queue.put({'type':'input','val':'back_space'})
                elif i == 'd':
                    event_queue.put({'type':'input','val':'select'})
                elif i == 'q':
                    event_queue.put({'type':'input','val':'quit'})
                else:
                    print(f"{i} is not valid input")