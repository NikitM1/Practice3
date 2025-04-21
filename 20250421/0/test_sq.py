import unittest
import prog

class TestSqroot(unittest.TestCase):
    
    def test_0(self):
        self.assertEqual(prog.sqroots('5 3 2'),'')
    
    def test_1(self):
        self.assertEqual(prog.sqroots('2 -4 2'),'1.0')    
    
    def test_2(self):
        self.assertEqual(prog.sqroots('2 -3 1'),'0.5 1.0')    
    
    def test_e(self):
        with self.assertRaises(ValueError):
            prog.sqroots('oops')