"""This code is sample for test ci"""
import unittest

import calc


class TestFunc(unittest.TestCase): 
    def test_func(self): 
        value1 = 1 
        value2 = 2 
        expected = 3 
        actual = calc.func(value1, value2)
        self.assertEqual(expected, actual) 

if __name__ == '__main__':
    unittest.main()
