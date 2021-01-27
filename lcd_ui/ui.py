import queue
from .lcd_proxy import LCDProxy
from .ui_elements import Menu, Content, DynamicContent

'''
Menu
    Temperature
        Current Temp
        Target Temp (can be selected to set)
    Wifi Settings
        Display - shows current SSID and IP address
        Configure
            Select SSID
            Enter Password
'''

class UI(object):
    def _build_ui(self):  
        wifi_display_entries = [
            (Content("SSID:"),None),
            (Content("IP:"),None)
        ]
        wifi_display_menu = Menu(wifi_display_entries)

        wifi_config_entries = [
            (Content("SSID:"),None),
            (Content("Pwd:"),None)
        ]
        wifi_config_menu = Menu(wifi_config_entries)
        

        wifi_main_entries = [
            (Content("Display"),wifi_display_menu),
            (Content("Configure"),wifi_config_menu)
        ]
        wifi_main_menu = Menu(wifi_main_entries)


        temp_main_entries = [
            (DynamicContent("Current:"),None),
            (Content("Target:"),None)
        ]
        temp_main_menu = Menu(temp_main_entries)


        main_menu_entries = [
            (Content("Temperature"),temp_main_menu),
            (Content("Wifi Settings"),wifi_main_menu),
            (Content("Poweroff"),None)
        ]
        return Menu(main_menu_entries)

    def __init__(self):
        self.display = LCDProxy()
        self.prev_menus = []
        self.current_elem = self._build_ui()
        self.update_display()
        self.event_queue = queue.Queue()

    def run(self):
        def print_display():
            print() 
            print(self.display)

        print_display()
        
        i = None
        while i != 'quit':
            e = self.event_queue.get()
            if e['type'] == 'input':
                i = e['val']
                if e['val'] == 'quit':
                    continue
                self.handle_input(i)
                self.update_display()
            if e['type'] == 'display_update':
                self.update_display()

            print_display()
    
    def handle_input(self,input):
        if input == 'up':
            self.current_elem.scroll('up')
        
        elif input == 'down':
            self.current_elem.scroll('down')
        
        elif input == 'select':
            if isinstance(self.current_elem,Menu):
                self.goto_next_menu()
            else:
                pass

        elif input == 'cycle':
            self.current_elem.cycle()
        
        elif input == 'back':
            self.go_back_menu()

    def update_display(self):
        self.display.clear()
        lines = self.current_elem.get_display()
        for i,line in enumerate(lines):
            self.display.write_word(line,[i,0])

    def goto_next_menu(self):
        next_menu = self.current_elem.select()
        if next_menu:
            self.prev_menus.append(self.current_elem)
            self.current_elem = next_menu
            self.current_elem.start(self.event_queue)

    def go_back_menu(self):
        if self.prev_menus:
                self.current_elem.stop()
                self.current_elem = self.prev_menus.pop()