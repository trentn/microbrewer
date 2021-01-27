import time
import random
import threading

class InvalidDirection(Exception):
    pass


class UI_Element(object):
    def scroll(self,dir):
        raise NotImplementedError

    def cycle(self):
        raise NotImplementedError

    def select(self):
        raise NotImplementedError

    def get_display(self):
        raise NotImplementedError


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

    def run(self,event_queue,interval=1):
        while self.menu.is_displayed:
            self.update_content()
            event_queue.put({'type':'display_update'})
            time.sleep(interval)

    def update_content(self):
        self.content = "%s %d" % (self.init_content, random.randrange(10))

class Menu(UI_Element):
    def __init__(self,entries,num_lines=2):
        self._entries = entries
        for entry in self._entries:
            entry[0].set_parent(self)

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
            if self._display_start < len(self._entries)-self._num_lines:
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

    def select(self):
        return self._entries[self._display_start+self._select_line][1]

    def get_display(self):
        lines = self._entries[self._display_start:self._display_start+self._num_lines]
        lines = [">" + str(line[0]) if i==self._select_line else " " + str(line[0]) for i,line in enumerate(lines)]
        return lines

    def start(self,event_queue):
        self.is_displayed = True
        for entry in self._entries:
            if isinstance(entry[0],DynamicContent):
                t = threading.Thread(target=entry[0].run,args=(event_queue,),daemon=True)
                t.start()
                self._display_threads.append(t)
    
    def stop(self):
        self.is_displayed = False

# class TextInput(UI_Element):
#     def __init__(self,max_chars=16):
#         self._current_input = []
#         self._current_selected = 'A'
#         self._input_options = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
#         self._input_elem_start = 0
#         self._select_item = 0
        
#     def select(self):
#         self._current_input.append(self._input_options)

#     def get_display(self):
#         return [''.join(self._current_input)+,''.join(self._input_options[self._input_elem_start:self._input_elem_start+16]])]

