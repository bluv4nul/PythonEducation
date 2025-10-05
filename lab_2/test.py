import unittest
from gen_bin_tree import gen_bin_tree  

class TestGenBinTree(unittest.TestCase):
    
    def test_height_zero(self):
        """Тест для высоты 0"""
        result = gen_bin_tree(0, 9)
        self.assertEqual(result, {})
    
    def test_height_one(self):
        """Тест для высоты 1 (только корень)"""
        result = gen_bin_tree(1, 9)
        expected = {
            "root": 9,
            "left": None,
            "right": None
        }
        self.assertEqual(result, expected)
    
    def test_height_two(self):
        """Тест для высоты 2"""
        result = gen_bin_tree(2, 9)
        expected = {
            "root": 9,
            "left": {
                "root": 19,  # 9*2+1 = 19
                "left": None,
                "right": None
            },
            "right": {
                "root": 17,  # 2*9-1 = 17
                "left": None,
                "right": None
            }
        }
        self.assertEqual(result, expected)
    
    
    def test_calculation_correctness(self):
        """Тест на правильность вычислений"""
        result = gen_bin_tree(2, 10)
        
        # Проверяем правильность вычислений для левых ветвей
        self.assertEqual(result["left"]["root"], 21)  # 10*2+1 = 21
        
        # Проверяем правильность вычислений для правых ветвей
        self.assertEqual(result["right"]["root"], 19)  # 2*10-1 = 19
    
    def test_leaf_nodes_none(self):
        """Тест что листовые узлы равны None"""
        result = gen_bin_tree(2, 9)
        
        # Узлы высоты 2 должны иметь листовые узлы как None
        self.assertIsNone(result["left"]["left"])
        self.assertIsNone(result["left"]["right"])
        self.assertIsNone(result["right"]["left"])
        self.assertIsNone(result["right"]["right"])

if __name__ == '__main__':
    unittest.main()