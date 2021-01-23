import unittest
from lcd_ui import Menu #pylint: disable=import-error

class TestMenu(unittest.TestCase):
    def test_get_display(self):  
        entries = ["A","B","C"]
        m = Menu(entries)  
        lines = m.get_display()
        self.assertEqual(len(lines),2)
        self.assertEqual(lines[0],">A")
        self.assertEqual(lines[1]," B")

    def test_scroll_display_down(self):
        entries = ["A","B","C"]
        m = Menu(entries)
        m.scroll_display('down')
        lines = m.get_display()
        self.assertEqual(lines[0],">B")
        self.assertEqual(lines[1]," C")

    def test_scroll_display_double_down(self):
        entries = ["A","B","C"]
        m = Menu(entries)
        m.scroll_display('down')
        m.scroll_display('down')
        lines = m.get_display()
        self.assertEqual(lines[0],">B")
        self.assertEqual(lines[1]," C")

    def test_scroll_display_up(self):
        entries = ["A","B","C"]
        m = Menu(entries)
        m._display_start = 1
        m.scroll_display('up')
        lines = m.get_display()
        self.assertEqual(lines[0],">A")
        self.assertEqual(lines[1]," B")

    def test_scroll_display_double_up(self):
        entries = ["A","B","C"]
        m = Menu(entries)
        m._display_start = 1
        m.scroll_display('up')
        m.scroll_display('up')
        lines = m.get_display()
        self.assertEqual(lines[0],">A")
        self.assertEqual(lines[1]," B")

    def test_scroll_select_down(self):
        entries = ["A","B","C"]
        m = Menu(entries)
        m.scroll_select('down')
        lines = m.get_display()
        self.assertEqual(lines[0]," A")
        self.assertEqual(lines[1],">B")

    def test_scroll_select_double_down(self):
        entries = ["A","B","C"]
        m = Menu(entries)
        m.scroll_select('down')
        m.scroll_select('down')
        lines = m.get_display()
        self.assertEqual(lines[0]," A")
        self.assertEqual(lines[1],">B")

    def test_scroll_select_up(self):
        entries = ["A","B","C"]
        m = Menu(entries)
        m._select_line = 1
        m.scroll_select('up')
        lines = m.get_display()
        self.assertEqual(lines[0],">A")
        self.assertEqual(lines[1]," B")

    def test_scroll_select_double_up(self):
        entries = ["A","B","C"]
        m = Menu(entries)
        m._select_line = 1
        m.scroll_select('up')
        m.scroll_select('up')
        lines = m.get_display()
        self.assertEqual(lines[0],">A")
        self.assertEqual(lines[1]," B")


