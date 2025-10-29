import unittest
from SumOfTwo import findTarget

class TestFindTarget(unittest.TestCase):
    
    def test_example1(self):
        result = findTarget([2, 7, 11, 15], 9)
        self.assertEqual(result, [0, 1])
    
    def test_example2(self):
        result = findTarget([3, 2, 4], 6)
        self.assertEqual(result, [1, 2])
    
    def test_example3(self):
        result = findTarget([3, 3], 6)
        self.assertEqual(result, [0, 1])

    def test_negative_numbers(self):
        """Тест с отрицательными числами в массиве"""
        result = findTarget([-1, 2, 5, 8], 1)
        self.assertEqual(result, [0, 1])

    def test_larger_array(self):
        """Тест с большим массивом и числами вразброс"""
        result = findTarget([1, 4, 7, 10, 13, 16, 19], 23)
        self.assertEqual(result, [1, 6])

    def test_no_solution(self):
        result = findTarget([1, 2, 3], 10)
        self.assertIsNone(result)  

if __name__ == '__main__':
    unittest.main()