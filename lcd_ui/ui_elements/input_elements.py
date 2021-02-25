from . import UI_Element

class DialInput(UI_Element):
    def __init__(self, label, init_value):
        self.label = label
        self.value = init_value
        self.set = False

    def scroll(self,dir):
        self.set = False
        if dir == 'up':
            self.value = self.value + 1
        elif dir == 'down':
            self.value = self.value - 1
        else:
            pass

    def cycle(self):
        pass

    def select(self):
        pass

    def get_display(self):
        return [self.label, str(self.value)]


class SelectTemp(DialInput):
    def select(self):
        with open('/tmp/target_temp','w') as f:
            str_val = str(self.value)
            f.write(str_val+'0'*max(0,5-len(str_val)))
        self.set = True
