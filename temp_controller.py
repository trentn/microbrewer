from lcd_ui import *

import RPi.GPIO as GPIO

def get_temp_probe():
    with open('/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves', 'r') as w1_slave_f:
        probe_id = ''
        while not probe_id.startswith('28-'):
            probe_id = w1_slave_f.readline().strip()
    
    return '/sys/bus/w1/devices/%s/temperature' % probe_id


class WifiConfig(object):
    def __init__(self):
        self.ssid = ValueReference('')
        self.passwd = ValueReference('')

class Burner(ListInput):
    def __init__(self, target_temp=None, temperature_filename=''):
        super().__init__(None,'Burner Control')
        self.logging = False
        self.running = False
        self.burner_on = False
        self.burner_pin = 21
        self.target_temp = target_temp
        self.tempurature_filename = temperature_filename

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.burner_pin,GPIO.OUT)
        GPIO.output(self.burner_pin,GPIO.LOW)
        self.running = True

        self._options = ['On']

    def turn_on(self):
        #print('turning on the burner')
        GPIO.output(self.burner_pin,GPIO.HIGH)
        self.burner_on = True

    def turn_off(self):
        #print('turning off the burner')
        GPIO.output(self.burner_pin,GPIO.LOW)
        self.burner_on = False

    def control_temperature(self):

        logf_name = 'temp_log_%s.csv' % str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        logf = open(logf_name, 'w')
        logf_writer = csv.writer(logf, delimiter=',')
    
        print('logging temp to %s' % logf_name)
   
        system.logging = True
        while system.running:
            with open(self.temperature_filename, 'r') as tempf:
                temp = tempf.readline()
                temp = temp.strip()
                temp = float(temp)/1000
        
            if system.target_temp:
                if temp >= system.target_temp and system.burner_on:
                    self.turn_off_burner(system)

                if temp < system.target_temp and not system.burner_on:
                    self.turn_on_burner(system)

        logf_writer.writerow([time.time(),temp,system.burner_on])
        time.sleep(0.25)

        logf.close()

    def select(self, event_queue):
        selected = self._options[self._select_line]
        if selected == 'On':
            self.turn_on()
            self._options[self._select_line] = 'Off'
        elif selected == 'Off':
            self.turn_off()
            self._options[self._select_line] = 'On'

temperature_filename = get_temp_probe()
target_temp = ValueReference(65)
wifi_config = WifiConfig()
burner = Burner(target_temp,temperature_filename)


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
        burner,
        temp_main_menu,
        wifi_main_menu
    ]
    return Menu(main_menu_entries, None)
