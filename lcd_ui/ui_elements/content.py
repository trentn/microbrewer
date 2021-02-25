from abc import abstractmethod
import time
import subprocess

try:
    import netifaces
except ImportError:
    print("Import netifaces failed")

class Content(object):
    def __init__(self, content):
        self.content = content
        self._parent = None

    def set_parent(self,parent):
        self._parent = parent

    def __str__(self):
        return self.content

class DynamicContent(Content):
    def __init__(self,content):
        super().__init__(content)
        self.init_content = content
        self.dynamic_content = ""

    def run(self,event_queue,interval=1):
        while self._parent.is_displayed:
            self.update_content(event_queue)
            time.sleep(interval)

    @abstractmethod
    def update_content(self, event_queue):
        raise NotImplementedError

class ScrollingContent(DynamicContent):
    def __init__(self, content, dynamic_content='', line_len=16):
        super().__init__(content)
        self.dynamic_content=dynamic_content
        self.avail_chars = line_len-len(self.init_content)-1
        self.current_start = 0

    def run(self,event_queue,interval=.6):
        self.set_dynamic_content()
        super().run(event_queue,interval=interval)

    def update_content(self, event_queue):
        extra_chars = len(self.dynamic_content)-self.avail_chars
        self.content = self.init_content + self.dynamic_content[self.current_start:self.current_start+self.avail_chars]
        self.current_start = (self.current_start + 1)%(extra_chars+1)
        event_queue.put({'type':'display_update'})

    def set_dynamic_content(self):
        pass
        

class DisplayTemp(DynamicContent):
    def __init__(self,content,filename):
        super().__init__(content)
        self.filename = filename

    def update_content(self,event_queue):
        with open(self.filename, 'r') as f:
            line = f.readline()
            if line[-1] == '\n':
                line = line[:-1]
            line = line[:2]+'.'+line[2:]
            if line != self.dynamic_content:
                self.dynamic_content = line
                self.content = self.init_content + self.dynamic_content
                event_queue.put({'type':'display_update'})

class DisplayIP(ScrollingContent):
    def run(self, event_queue):
        super().run(event_queue)

    def set_dynamic_content(self):
        try:
            iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
            self.dynamic_content = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
        except NameError:
            self.dynamic_content = '000.000.000.000' 

class DisplaySSID(ScrollingContent):
    def run(self, event_queue):
        super().run(event_queue)

    def set_dynamic_content(self):
        output = subprocess.check_output(['iwgetid'])
        self.dynamic_content = output.split(b'"')[1].decode('utf-8')

