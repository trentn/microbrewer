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

    def start(self, event_queue):
        pass

    def stop(self):
        pass


from .menu import *
from .content import *
from .input_elements import *
