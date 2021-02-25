from .input_elements import ListInput

class Menu(ListInput):
    def __init__(self,entries,num_lines=2):
        super().__init__(entries,num_lines)
        for entry in self._options:
            entry[0].set_parent(self)

    def select(self):
        return self._options[self._display_start+self._select_line][1]
