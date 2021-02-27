class InvalidDirection(Exception):
    pass


class UI_Element(object):
    def __init__(self,children,label):
        if not children:
            self._children = []
        else:
            self._children = children
            for child in self._children:
                child.set_parent(self)
        self._parent = None
        self.content = label
        self.is_displayed = False

    def __str__(self):
        return self.content

    def add_child(self, child):
        self._children.append(child)
        child.set_parent(self)

    def set_parent(self, parent):
        self._parent = parent

    def scroll(self,dir):
        pass

    def cycle(self):
        pass

    def select(self):
        pass

    def back(self):
        return self._parent

    def get_display(self):
        pass

    def start(self, event_queue):
        pass

    def stop(self):
        pass

from .content_elements import *
from .input_elements import *
