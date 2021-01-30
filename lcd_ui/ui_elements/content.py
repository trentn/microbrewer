from abc import abstractmethod
import time

class Content(object):
    def __init__(self, content):
        self.content = content
        self.menu = None

    def set_parent(self,parent_menu):
        self.menu = parent_menu

    def __str__(self):
        return self.content

class DynamicContent(Content):
    def __init__(self,content):
        super().__init__(content)
        self.init_content = content
        self.dynamic_content = ""

    def run(self,event_queue,interval=1):
        while self.menu.is_displayed:
            self.update_content(event_queue)
            time.sleep(interval)

    @abstractmethod
    def update_content(self, event_queue):
        raise NotImplementedError

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

