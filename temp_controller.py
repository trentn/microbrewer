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

def get_temp_probe():
    with open('/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves', 'r') as w1_slave_f:
        probe_id = ''
        while not probe_id.startswith('28-'):
            probe_id = w1_slave_f.readline().strip()
    
    return '/sys/bus/w1/devices/%s/temperature' % probe_id

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
        DisplayTemp("Current: ",get_temp_probe()),
        DialInput("Target: ", target_temp)
    ]
    temp_main_menu = Menu(temp_main_entries,'Temperature')


    main_menu_entries = [
        temp_main_menu,
        wifi_main_menu
    ]
    return Menu(main_menu_entries, None)
