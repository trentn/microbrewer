import time
import random
import threading
import subprocess

from . import UI_Element, InvalidDirection
from .content import Content, DynamicContent, ScrollingContent


class ValueReference(object):
    def __init__(self, init_value):
        self.value = init_value


class DialInput(UI_Element):
    def __init__(self, label, dest):
        self.label = label
        self.value = dest.value
        self._dest = dest
        self.set = False

    def scroll(self,dir):
        self.set = False
        if dir == 'up':
            self.value = self.value + 1
        elif dir == 'down':
            self.value = self.value - 1
        else:
            pass

    def cycle(self):
        pass

    def select(self):
        self._dest.value = self.value

    def get_display(self):
        return [self.label, str(self.value)]

class ListInput(UI_Element):
    def __init__(self, options, num_lines=2):
        self._options = options
        self._num_lines = num_lines
        self._select_line = 0
        self._display_start = 0
        self._display_threads = []
        self.is_displayed = False

    def scroll_display(self,dir):
        if dir == 'up':
            if self._display_start > 0:
                self._display_start = (self._display_start - 1)
        elif dir == 'down':
            if self._display_start < len(self._options)-self._num_lines:
                self._display_start = (self._display_start + 1)
        else:
            raise InvalidDirection

    def scroll(self,dir):
        if dir == 'up':
            if self._select_line > 0:
                self._select_line = (self._select_line - 1)
            else:
                self.scroll_display('up')
        elif dir == 'down':
            if self._select_line < self._num_lines-1:
                self._select_line = (self._select_line + 1)
            else:
                self.scroll_display('down')
        else:
            raise InvalidDirection

    def cycle(self):
        pass

    def select(self, event_queue):
        pass

    def get_display(self):
        lines = self._options[self._display_start:self._display_start+self._num_lines]
        lines = [">" + str(line[0]) if i==self._select_line else " " + str(line[0]) for i,line in enumerate(lines)]
        return lines

    def start(self,event_queue):
        self.is_displayed = True
        for entry in self._options:
            if isinstance(entry[0],DynamicContent):
                t = threading.Thread(target=entry[0].run,args=(event_queue,),daemon=True)
                t.start()
                self._display_threads.append(t)
    
    def stop(self):
        self.is_displayed = False


class SSIDList(ListInput):
    def __init__(self,ssid_ref,num_lines=2):
        super().__init__(None,num_lines)
        self._ssid_ref = ssid_ref
    
    def select(self, event_queue):
       self._ssid_ref.value = self._options[self._display_start+self._select_line][1]
       event_queue.put({'type':'input','val':'back'})

    def start(self,event_queue):
        self._options = []
        result = subprocess.check_output('iwlist wlan0 scan | grep ESSID', shell=True, text=True)
        for r in result.strip().split('\n'):
            ssid = r.split('"')[1]
            option = ScrollingContent('', dynamic_content=ssid)
            option.set_parent(self)
            self._options.append((option,ssid)) 
        super().start(event_queue)
