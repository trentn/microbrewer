class InvalidPosition(Exception):
    pass

class WillNotFitDisplay(Exception):
    pass

class LCDProxy(object):
    def __init__(self, lcd=None, chars=16, rows=2, init_char=' '):
        self.chars = chars
        self.rows = rows
        self.buffer = [bytearray(init_char*self.chars,encoding='utf-8') for row in range(self.rows)]
        self.prev_buffer = self.buffer.copy()
        self.cursor_pos = (0,0)
        self.lcd = lcd
    
    def write(self,char):
        try:
            self.buffer[self.cursor_pos[0]][self.cursor_pos[1]] = ord(char)
            self.cursor_pos = (self.cursor_pos[0],self.cursor_pos[1]+1)
        except IndexError:
            raise InvalidPosition
    
    def write_string(self,word,wrap=False):
        try:
            for char in word:
                self.write(char)
                if wrap:
                    if self.cursor_pos[1] == self.chars:
                        self.cursor_pos = (self.cursor_pos[0]+1,0)
        except InvalidPosition:
            raise WillNotFitDisplay

    def clear(self):
        self.buffer = [bytearray(' '*self.chars,encoding='utf-8') for row in range(self.rows)]

    def get_char(self,pos):
        try:
            return chr(self.buffer[pos[0]][pos[1]])
        except IndexError:
            raise InvalidPosition

    def update(self):
        if self.lcd:
            for row in range(self.rows):
                for char in range(self.chars):
                    if self.buffer[row][char] != self.prev_buffer[row][char]:
                        self.lcd.cursor_pos = (row,char)
                        self.lcd.write(self.buffer[row][char])
                        self.prev_buffer[row][char]=self.buffer[row][char]
        
        

    def __str__(self):
        string = ''
        for row in range(self.rows):
            line = ' '.join([chr(b) for b in self.buffer[row]]) + '\n'
            string = string + line
        return string[:-1]
