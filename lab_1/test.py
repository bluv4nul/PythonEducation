import unittest
from SumOfTwo import findTarget

class TestFindTarget(unittest.TestCase):
    
    def test_example1(self):
        result = findTarget([2, 7, 11, 15], 9)
        self.assertEqual(result, (0, 1))
    
    def test_example2(self):
        result = findTarget([3, 2, 4], 6)
        self.assertEqual(result, (1, 2))
    
    def test_example3(self):
        result = findTarget([3, 3], 6)
        self.assertEqual(result, (0, 1))

if __name__ == '__main__':
    unittest.main()