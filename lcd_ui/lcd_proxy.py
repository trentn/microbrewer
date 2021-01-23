class InvalidPosition(Exception):
    pass

class WillNotFitDisplay(Exception):
    pass

class LCDProxy(object):
    def __init__(self, chars=16, rows=2, init_char=' '):
        self.chars = chars
        self.rows = rows
        self.lcd = [bytearray(init_char*self.chars,encoding='utf-8') for row in range(self.rows)]

    def write(self,char,pos):
        try:
            self.lcd[pos[0]][pos[1]] = ord(char)
        except IndexError:
            raise InvalidPosition
    
    def write_word(self,word,start_pos,wrap=False):
        try:
            for char in word:
                self.write(char,start_pos)
                start_pos[1] = start_pos[1]+1
                if wrap:
                    if start_pos[1] == self.chars:
                        start_pos[1] = 0
                        start_pos[0] = start_pos[0]+1
        except InvalidPosition:
            raise WillNotFitDisplay

    def get_char(self,pos):
        try:
            return chr(self.lcd[pos[0]][pos[1]])
        except IndexError:
            raise InvalidPosition

    def update(self):
        #TODO: write to lcd
        pass

    def __str__(self):
        string = ''
        for row in range(self.rows):
            line = ' '.join([chr(b) for b in self.lcd[row]]) + '\n'
            string = string + line
        return string[:-1]