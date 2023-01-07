class InvalidDirection(Exception):
    pass

class UI_Element(object):
    def __init__(self,children,label):
        if not children:
            self._children = []
        else:
            self._children = children
            for child in self._children:
                child.set_parent(self)
        self._parent = None
        self.content = label
        self.is_displayed = False

    def __str__(self):
        return self.content

    def add_child(self, child):
        self._children.append(child)
        child.set_parent(self)

    def set_parent(self, parent):
        self._parent = parent

    def scroll(self,**kwargs):
        pass

    def cycle(self):
        pass

    def select(self):
        pass

    def back(self):
        return self._parent

    def back_space(self, event_queue):
        pass

    def get_display(self):
        pass

    def start(self, event_queue):
        pass

    def stop(self):
        pass

from .content_elements import *
from .input_elements import *


'''
Menu
    Burner Control
        On
        Off
    Temperature
        Current Temp
        Target Temp (can be selected to set)
    Wifi Settings
        Display - shows current SSID and IP address
        Configure
            Select SSID
            Enter Password
'''

def build_menu(burner, temp, wifi_config):    
    wifi_display_entries = [
        DisplaySSID(),
        DisplayIP()
    ]
    
    wifi_display_menu = Menu(wifi_display_entries,'Display')


    wifi_config_entries = [
        SSIDList(wifi_config.ssid),
        TextInput(wifi_config.passwd,'Set Pwd: ')
    ]
    
    wifi_config_menu = Menu(wifi_config_entries,'Configure')
    

    wifi_main_entries = [
        wifi_display_menu,
        wifi_config_menu
    ]
    wifi_main_menu = Menu(wifi_main_entries,'Wifi Settings')


    temp_main_entries = [
        DisplayTemp("Current: ",temp.probe),
        DialInput("Target: ", temp.target)
    ]
    temp_main_menu = Menu(temp_main_entries,'Temperature')

    main_menu_entries = [
        BurnerUI(burner),
        temp_main_menu,
        wifi_main_menu
    ]
    return Menu(main_menu_entries, None)
