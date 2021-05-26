
import time
import subprocess

try:
    import netifaces
except ImportError:
    print("Import netifaces failed")

from . import UI_Element
from .label_mixins import *

class DisplayTemp(UI_Element, DynamicLabel):
    def __init__(self,content,temp_source):
        super().__init__(None, content)
        self._temp_source = temp_source
        self.init_content = content
        self.dynamic_content = ""

    def update_content(self,event_queue):
        line = ''

        with open(self._temp_source, 'r') as f:
            line = f.readline()
            if line[-1] == '\n':
                line = line[:-1]
            line = line[:2]+'.'+line[2:]

        if line != self.dynamic_content:
            self.dynamic_content = line
            self.content = self.init_content + self.dynamic_content
            event_queue.put({'type':'display_update'})

class ScrollingContent(UI_Element,ScrollingLabel):
    def __init__(self, content, dynamic_content):
        super().__init__(None,'')
        self.init_content = content
        self.dynamic_content = dynamic_content


class DisplayIP(ScrollingContent):
    def __init__(self):
        super().__init__('IP: ','')
        self.get_IP()

    def get_IP(self):
        try:
            iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
            self.dynamic_content = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
        except:
            self.dynamic_content = '000.000.000.000' 

class DisplaySSID(ScrollingContent):
    def __init__(self):
        super().__init__('SSID: ','')
        self.get_SSID()

    def get_SSID(self):
        try:
            output = subprocess.check_output(['iwgetid'])
            self.dynamic_content = output.split(b'"')[1].decode('utf-8')
        except:
            self.dynamic_content = "Could not get SSID"
