class InvalidPosition(Exception):
    pass

class WillNotFitDisplay(Exception):
    pass

class LCDProxy(object):
    def __init__(self, chars=16, rows=2, init_char=' '):
        self.chars = chars
        self.rows = rows
        self.lcd = [bytearray(init_char*self.chars,encoding='utf-8') for row in range(self.rows)]
        self.current_pos = [0,0]

    def cursor_pos(self,row,char):
        self.current_pos = [row,char]
    
    def write(self,char):
        try:
            self.lcd[self.current_pos[0]][self.current_pos[1]] = ord(char)
            self.current_pos = [self.current_pos[0],self.current_pos[1]+1]
        except IndexError:
            raise InvalidPosition
    
    def write_word(self,word,wrap=False):
        try:
            for char in word:
                self.write(char)
                if wrap:
                    if self.current_pos[1] == self.chars:
                        self.current_pos[1] = 0
                        self.current_pos[0] = self.current_pos[0]+1
        except InvalidPosition:
            raise WillNotFitDisplay

    def clear(self):
        self.lcd = [bytearray(' '*self.chars,encoding='utf-8') for row in range(self.rows)]

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