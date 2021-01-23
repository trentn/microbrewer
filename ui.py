from lcd_ui import LCDProxy, Menu

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
            ("SSID:",None),
            ("IP:",None)
        ]
        wifi_display_menu = Menu(wifi_display_entries)

        wifi_config_entries = [
            ("SSID:",None),
            ("Pwd:",None)
        ]
        wifi_config_menu = Menu(wifi_config_entries)
        

        wifi_main_entries = [
            ("Display",wifi_display_menu),
            ("Configure",wifi_config_menu)
        ]
        wifi_main_menu = Menu(wifi_main_entries)


        temp_main_entries = [
            ("Current:",None),
            ("Target:",None)
        ]
        temp_main_menu = Menu(temp_main_entries)


        main_menu_entries = [
            ("Temperature",temp_main_menu),
            ("Wifi Settings",wifi_main_menu),
            ("Poweroff",None)
        ]
        return Menu(main_menu_entries)

    def __init__(self):
        self.display = LCDProxy()
        self.prev_menus = []
        self.current_elem = self._build_ui()
        self.update_display()
    
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
            if self.prev_menus:
                self.current_elem = self.prev_menus.pop()

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


if __name__ == '__main__':
    ui = UI()

    def print_display():
        print() 
        print(ui.display)
           

    print_display()
    i = input()
    while i != 'quit':
        ui.handle_input(i)
        ui.update_display()
        print_display()
        i = input()