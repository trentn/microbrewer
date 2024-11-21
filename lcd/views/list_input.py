import threading

from . import UI_Element, InvalidDirection
from .label_mixins import DynamicLabel

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