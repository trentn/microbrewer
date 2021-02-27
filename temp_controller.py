from lcd_ui import *


class WifiConfig(object):
    def __init__(self):
        self.ssid = ValueReference('')
        self.passwd = ValueReference('')


target_temp = ValueReference(65)
wifi_config = WifiConfig()

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

def build_ui():    
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
        DisplayTemp("Current: ",'/sys/bus/w1/devices/28-012033966b3f/temperature'),
        DialInput("Target: ", target_temp)
    ]
    temp_main_menu = Menu(temp_main_entries,'Temperature')


    main_menu_entries = [
        temp_main_menu,
        wifi_main_menu
    ]
    return Menu(main_menu_entries, None)
