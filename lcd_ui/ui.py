from lcd_ui.lcd_proxy import LCDProxy
import queue
from .ui_elements import Menu

class UI(object):
    def __init__(self, root_elem, display, output_console=False):
        self.display = display
        self.prev_menus = []
        self.current_elem = root_elem
        self.update_display()
        self.event_queue = queue.Queue()
        self.output_console = output_console

    def run(self):
        self.current_elem.start(self.event_queue)

        if(self.output_console):
            def print_display():
                print() 
                print(self.display)
            print_display()
        
        i = None
        while i != 'quit':
            e = self.event_queue.get()
            if e['type'] == 'input':
                if e['val'] == 'quit':
                    continue
                self.handle_input(e)
                self.update_display()
            if e['type'] == 'display_update':
                self.update_display()
            if(self.output_console):
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

    def update_display(self):
        self.display.clear()
        lines = self.current_elem.get_display()
        for i,line in enumerate(lines):
            self.display.cursor_pos = (i,0)
            self.display.write_string(line)
        self.display.update()
