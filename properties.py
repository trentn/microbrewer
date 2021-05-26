on_rpi = True
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Unable to import RPi.GPIO")
    on_rpi = False

import datetime
import csv
import time

class ValueReference(object):
    def __init__(self, init_value):
        self.value = init_value

class WifiConfig(object):
    def __init__(self):
        self.ssid = ValueReference('')
        self.passwd = ValueReference('')

class Burner(object):
    def __init__(self, target_temp=None, temperature_filename=''):
        # super().__init__(None,'Burner Control')
        self.logging = False
        self.running = False
        self.burner_on = False
        self.burner_pin = 21
        self.target_temp = target_temp
        self.temperature_filename = temperature_filename

        if on_rpi:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.burner_pin,GPIO.OUT)
            GPIO.output(self.burner_pin,GPIO.LOW)
        

    def turn_on(self):
        #print('turning on the burner')
        if on_rpi:
            GPIO.output(self.burner_pin,GPIO.HIGH)
        self.burner_on = True

    def turn_off(self):
        #print('turning off the burner')
        if on_rpi:
            GPIO.output(self.burner_pin,GPIO.LOW)
        self.burner_on = False

    def control_temperature(self):

        logf_name = '/var/log/temp_log_%s.csv' % str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        logf = open(logf_name, 'w')
        logf_writer = csv.writer(logf, delimiter=',')
    
        #print('logging temp to %s' % logf_name)
   
        self.logging = True
        while self.running:
            with open(self.temperature_filename, 'r') as tempf:
                temp = tempf.readline()
                temp = temp.strip()
                temp = float(temp)/1000
        
            if self.target_temp:
                if temp >= self.target_temp.value and self.burner_on:
                    self.turn_off()

                if temp < self.target_temp.value and not self.burner_on:
                    self.turn_on()

            logf_writer.writerow([time.time(),temp,self.burner_on])
            time.sleep(0.25)

        self.turn_off()
        logf.close()

class TempProperties(object):
    def __init__(self):
        self.probe = self.get_temp_probe()
        self.target = ValueReference(65)

    def get_temp_probe(self):
        if not on_rpi:
            return "dummyfile"
        with open('/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves', 'r') as w1_slave_f:
            probe_id = ''
            while not probe_id.startswith('28-'):
                probe_id = w1_slave_f.readline().strip()
        
        return '/sys/bus/w1/devices/%s/temperature' % probe_id

class SystemProperties(object):
    def __init__(self):
        self.temp = TempProperties()
        self.wifi_config = WifiConfig()
        self.burner = Burner(self.temp.target,self.temp.probe)