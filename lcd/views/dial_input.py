from . import UI_Element
from .label_mixins import DynamicLabel

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