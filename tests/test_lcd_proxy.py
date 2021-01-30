import unittest
from lcd_ui import * #pylint: disable=import-error

class TestLCDProxy(unittest.TestCase):
    def test_init(self):
        p = LCDProxy() #pylint: disable=undefined-variable
        self.assertEqual(p.lcd, [bytearray(' '*16,encoding='utf-8'),bytearray(' '*16,encoding='utf-8')])

    def test_str_repr(self):
        p = LCDProxy(chars=5, rows=1, init_char='A') #pylint: disable=undefined-variable
        intended_output ='A A A A A' 
        self.assertEqual(str(p),intended_output)

    def test_write(self):
        p = LCDProxy(chars=5, rows=1) #pylint: disable=undefined-variable
        intended_output = 'A B C D E'
        p.cursor_pos = (0,0)
        p.write('A')
        p.write('B')
        p.write('C')
        p.write('D')
        p.write('E')
        self.assertEqual(str(p),intended_output)

    def test_write_error(self):
        p = LCDProxy(chars=5, rows=1) #pylint: disable=undefined-variable
        p.cursor_pos = (6,1)
        self.assertRaises(InvalidPosition,p.write,'A') #pylint: disable=undefined-variable

    def test_write_word(self):
        p = LCDProxy(chars=5,rows=1) #pylint: disable=undefined-variable
        intended_output = 'A B C D E'
        p.cursor_pos = (0,0)
        p.write_string('ABCDE')
        self.assertEqual(str(p),intended_output)

    def test_write_word_wrap(self):
        p = LCDProxy(chars=5,rows=2) #pylint: disable=undefined-variable
        intended_output = 'A B C D E\nF G H I J'
        p.cursor_pos = (0,0)
        p.write_string('ABCDEFGHIJ',wrap=True)
        self.assertEqual(str(p),intended_output)

    def test_write_word_error(self):
        p = LCDProxy(chars=5,rows=1) #pylint: disable=undefined-variable
        p.cursor_pos = (0,0)
        self.assertRaises(WillNotFitDisplay,p.write_string,'ABCDEF') #pylint: disable=undefined-variable

    def test_write_word_wrap_error(self):
        p = LCDProxy(chars=5,rows=2) #pylint: disable=undefined-variable
        p.cursor_pos = (1,0)
        self.assertRaises(WillNotFitDisplay,p.write_string,'ABCDEF',wrap=True) #pylint: disable=undefined-variable

    def test_get_char(self):
        p = LCDProxy(chars=5,rows=1,init_char='A') #pylint: disable=undefined-variable
        self.assertEqual(p.get_char([0,0]),'A')
    
    def test_get_char_error(self):
        p = LCDProxy(chars=5,rows=1,init_char='A') #pylint: disable=undefined-variable
        self.assertRaises(InvalidPosition,p.get_char,[5,0]) #pylint: disable=undefined-variable

    def test_clear(self):
        p = LCDProxy(chars=5,rows=1,init_char='A') #pylint: disable=undefined-variable
        p.clear()
        self.assertEqual(str(p),'         ')

if __name__ == '__main__':
    unittest.main()