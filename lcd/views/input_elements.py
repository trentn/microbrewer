import time
import random
import threading
import subprocess

from . import UI_Element, InvalidDirection
from .label_mixins import *
from .content_elements import ScrollingContent


class DialInput(UI_Element, DynamicLabel):
    def __init__(self, label, dest):
        super().__init__(None,label)
        self.label = 'Set ' + label
        self.value = dest.value
        self._dest = dest
        
        self.init_content = label
        self.dynamic_content = ""

        self.set = False

    def scroll(self,**kwargs):
        dir = kwargs['dir']
        self.set = False
        if dir == 'up':
            self.value = self.value + 1
        elif dir == 'down':
            self.value = self.value - 1
        else:
            pass

    def cycle(self):
        pass

    def select(self, event_queue):
        self._dest.value = self.value
        event_queue.put({'type':'input','val':'back'})

    def get_display(self):
        return [self.label, str(self.value)]

    def update_content(self, event_queue):
        line = str(self._dest.value)
        if line != self.dynamic_content:
            self.dynamic_content = line
            self.content = self.init_content + self.dynamic_content
            event_queue.put({'type':'display_update'})

class ListInput(UI_Element):
    def __init__(self, options,label,num_lines=2):
        super().__init__(options,label)
        self._options = self._children
        self._num_lines = num_lines
        self._select_line = 0
        self._display_start = 0
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

    def scroll(self,**kwargs):
        dir = kwargs['dir']
        if dir == 'up':
            if self._select_line > 0:
                self._select_line = (self._select_line - 1)
            else:
                self.scroll_display('up')
        elif dir == 'down':
            if self._select_line < self._num_lines-1 and self._select_line < len(self._options)-1:
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
        lines = [">" + str(line) if i==self._select_line else " " + str(line) for i,line in enumerate(lines)]
        return lines

    def start(self,event_queue):
        self.is_displayed = True
        for entry in self._options:
            if isinstance(entry,DynamicLabel):
                t = threading.Thread(target=entry.run,args=(event_queue,),daemon=True)
                t.start()
    
    def stop(self):
        self.is_displayed = False

class Menu(ListInput):
    def __init__(self,options,label):
        super().__init__(options,label)

    def select(self, event_queue):
        option = self._options[self._display_start+self._select_line]
        if isinstance(option, (ListInput,DialInput,TextInput)):
            return option
        else:
            return None

class SSIDList(ListInput, ScrollingLabel):
    def __init__(self,ssid_ref,num_lines=2):
        super().__init__(None,'',num_lines)
        self._ssid_ref = ssid_ref
        self.init_content = 'Set SSID: '
        self.dynamic_content = self._ssid_ref
    
    def select(self, event_queue):
       self._ssid_ref.value = str(self._options[self._display_start+self._select_line])
       event_queue.put({'type':'input','val':'back'})

    def start(self,event_queue):
        self._options = []
        try:
            result = subprocess.check_output('iwlist wlan0 scan | grep ESSID', shell=True, text=True)
            for r in result.strip().split('\n'):
                ssid = r.split('"')[1]
                option = ScrollingContent('', ssid)
                option.set_parent(self)
                self._options.append(option)
        except:
            option = ScrollingContent('', 'Unable to find nearby SSIDs')
            option.set_parent(self)
            self._options.append(option)

        super().start(event_queue)


class TextInput(UI_Element,ScrollingLabel):
    def __init__(self,dest,label):
        super().__init__(None,'')
        self._dest = dest
        self._value = ''
        self._letters = list('ABCDEFGHJIKLMNOPQRSTUVWXYZ 1234567890_!?@#$%^&*"\';:,.=+-()<>[]{}\\/|`~')
        #self._letters = list('ABCDEFGHJIKLMNOPQRSTUVWXYZ')
        self._start = 0
        self._end = 16 
        self._display_letters = bytearray(''.join(self._letters), encoding='utf-8')
        self._letter_index = 0
        self.dynamic_content = self._dest
        self.init_content = label

    def scroll(self,**kwargs):
        dir = kwargs['dir']
        length = kwargs['length']
        if dir == 'up':
            if length == 'short':
                self._letters[self._letter_index] = self._letters[self._letter_index].upper()
                self._letter_index = max(self._letter_index - 1, 0)
                if self._letter_index < self._start:
                    self._start -= 1
                    self._end -= 1
            elif length == 'long':
                self._letters[self._letter_index] = self._letters[self._letter_index].upper()
        elif dir == 'down':
            if length == 'short':
                self._letters[self._letter_index] = self._letters[self._letter_index].upper()
                self._letter_index = min(self._letter_index + 1, len(self._letters)-1)
                if self._letter_index >= self._end:
                    self._start += 1
                    self._end += 1
            elif length == 'long':
                if self._letters[self._letter_index].isalpha():
                    self._letters[self._letter_index] = self._letters[self._letter_index].lower() 
        else:
            pass

    def back(self):
        self._dest.value = self._value
        return self._parent

    def select(self, event_queue):
        self._value = self._value + self._letters[self._letter_index]
        event_queue.put({'type':'display_update'})

    def get_display(self):
        lines = [self._value, self._display_letters.decode('utf-8')[self._start:self._end]]
        return lines

    def start(self,event_queue):
        self.is_displayed = True
        def blink(self):
            while self.is_displayed:
                index = self._letter_index
                
                self._display_letters[index] = ord(' ')
                event_queue.put({'type':'display_update'})
                time.sleep(0.3)

                self._display_letters[index] = ord(self._letters[index])
                event_queue.put({'type':'display_update'})
                time.sleep(0.3)

        t = threading.Thread(target=blink, args=(self,),daemon=True)
        t.start()
    
    def stop(self):
        self.is_displayed = False


class BurnerUI(ListInput):
    def __init__(self, burner):
        super().__init__(None,'Burner Control')

        self.enable_line = ScrollingContent('','Enable Temperature Control')
        self.enable_line.set_parent(self)
        self.disable_line = ScrollingContent('','Disable Temperature Control')
        self.disable_line.set_parent(self)
        
        self._options = ['On',self.enable_line]

        self.burner = burner

    def select(self, event_queue):
        selected = self._options[self._select_line]
        if selected == 'On':
            self.burner.turn_on()
            self._options[self._select_line] = 'Off'
        elif selected == 'Off':
            self.burner.turn_off()
            self._options[self._select_line] = 'On'
        elif type(selected) == ScrollingContent:
            content = selected.init_content + selected.dynamic_content 
            if content == 'Enable Temperature Control':
                self.burner.running = True
                self.control_t = threading.Thread(target=self.burner.control_temperature)
                self.control_t.start()
                self._options = [self.disable_line]
                self._select_line = 0
                self.stop()
                self.start(event_queue)
            elif content == 'Disable Temperature Control':
                self.burner.running = False
                self.control_t.join()
                self._options = ['On',self.enable_line]
                self._select_line = 1
                self.stop()
                self.start(event_queue)
