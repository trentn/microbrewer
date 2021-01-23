class LCDProxy(object):
    def __init__(self, chars=16, rows=2, init_char=' '):
        self.chars = chars
        self.rows = rows
        self.lcd = [bytearray(init_char*self.chars,encoding='utf-8') for row in range(self.rows)]

    def write(self,char,pos):
        self.lcd[pos[0]][pos[1]] = ord(char)
    
    def write_word(self,word,start_pos):
        for char in word:
            self.write(char,start_pos)
            start_pos[1] = start_pos[1]+1

    def update(self):
        #TODO: write to lcd
        pass

    def __str__(self):
        string = ''
        for row in range(self.rows):
            line = ' '.join([chr(b) for b in self.lcd[row]]) + '\n'
            string = string + line
        return string[:-1]