class InvalidDirection(Exception):
    pass

class Menu(object):
    def __init__(self,entries,num_lines=2):
        self._entries = entries
        self._num_lines = num_lines
        self._select_line = 0
        self._display_start = 0

    def scroll_display(self,dir):
        if dir == 'up':
            if self._display_start > 0:
                self._display_start = (self._display_start - 1)
        elif dir == 'down':
            if self._display_start < len(self._entries)-self._num_lines:
                self._display_start = (self._display_start + 1)
        else:
            raise InvalidDirection

    def scroll_select(self,dir):
        if dir == 'up':
            if self._select_line > 0:
                self._select_line = (self._select_line - 1)
        elif dir == 'down':
            if self._select_line < self._num_lines-1:
                self._select_line = (self._select_line + 1)
        else:
            raise InvalidDirection

    def get_display(self):
        lines = self._entries[self._display_start:self._display_start+self._num_lines]
        lines = [">"+line if i==self._select_line else " "+line for i,line in enumerate(lines)]
        return lines