from lcd_ui import Menu, Content, DisplayTemp, ScrollingContent

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
        (Content("SSID:"),None),
        (ScrollingContent("Test:"),None)
    ]
    wifi_display_menu = Menu(wifi_display_entries)

    wifi_config_entries = [
        (Content("Set SSID"),None),
        (Content("Set Pwd"),None)
    ]
    wifi_config_menu = Menu(wifi_config_entries)
    

    wifi_main_entries = [
        (Content("Display"),wifi_display_menu),
        (Content("Configure"),wifi_config_menu)
    ]
    wifi_main_menu = Menu(wifi_main_entries)


    temp_main_entries = [
        (DisplayTemp("Current:",'./dummyfile'),None),
        (Content("Target:"),None)
    ]
    temp_main_menu = Menu(temp_main_entries)


    main_menu_entries = [
        (Content("Temperature"),temp_main_menu),
        (Content("Wifi Settings"),wifi_main_menu),
        (Content("Poweroff"),None)
    ]
    return Menu(main_menu_entries)