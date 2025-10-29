import unittest
from gen_bin_tree import gen_bin_tree  

class TestGenBinTree(unittest.TestCase):
    
    def test_height_zero(self):
        """Тест для высоты 0 (только корень как множество)"""
        result = gen_bin_tree(0, 9)
        self.assertEqual(result, {9})  # Должно быть {9}, а не {0}
    
    def test_height_one(self):
        """Тест для высоты 1 (корень с потомками-множествами)"""
        result = gen_bin_tree(1, 9)
        expected = {
            "root": 9,
            "left": {19},  # 9*2+1 = 19
            "right": {17}  # 2*9-1 = 17
        }
        self.assertEqual(result, expected)
    
    def test_height_two(self):
        """Тест для высоты 2"""
        result = gen_bin_tree(2, 9)
        expected = {
            "root": 9,
            "left": {
                "root": 19,  # 9*2+1 = 19
                "left": {39},  # 19*2+1 = 39
                "right": {37}  # 2*19-1 = 37
            },
            "right": {
                "root": 17,  # 2*9-1 = 17
                "left": {35},  # 17*2+1 = 35
                "right": {33}  # 2*17-1 = 33
            }
        }
        self.assertEqual(result, expected)
    
    def test_height_three(self):
        """Тест для высоты 3"""
        result = gen_bin_tree(3, 9)
        
        # Проверяем структуру
        self.assertEqual(result["root"], 9)
        self.assertEqual(result["left"]["root"], 19)
        self.assertEqual(result["right"]["root"], 17)
        
        # Проверяем листья (они должны быть множествами)
        self.assertEqual(result["left"]["left"]["left"], {79})  # 39*2+1 = 79
        self.assertEqual(result["left"]["left"]["right"], {77})  # 2*39-1 = 77
    
    def test_calculation_correctness(self):
        """Тест на правильность вычислений"""
        result = gen_bin_tree(2, 10)
        
        # Проверяем правильность вычислений
        self.assertEqual(result["left"]["root"], 21)  # 10*2+1 = 21
        self.assertEqual(result["right"]["root"], 19)  # 2*10-1 = 19
        self.assertEqual(result["left"]["left"], {43})  # 21*2+1 = 43
        self.assertEqual(result["left"]["right"], {41})  # 2*21-1 = 41
    
    def test_leaf_nodes_are_sets(self):
        """Тест что листовые узлы являются множествами"""
        result = gen_bin_tree(2, 9)
        
        # Узлы высоты 2 должны иметь листовые узлы как множества
        self.assertIsInstance(result["left"]["left"], set)
        self.assertIsInstance(result["left"]["right"], set)
        self.assertIsInstance(result["right"]["left"], set)
        self.assertIsInstance(result["right"]["right"], set)
        
        # Проверяем значения в множествах
        self.assertEqual(result["left"]["left"], {39})
        self.assertEqual(result["left"]["right"], {37})
    
    def test_negative_height(self):
        """Тест для отрицательной высоты"""
        result = gen_bin_tree(-1, 9)
        self.assertEqual(result, {})
    
    def test_custom_functions(self):
        """Тест с кастомными функциями для потомков"""
        result = gen_bin_tree(
            height=2, 
            root=5,
            left_func=lambda x: x + 1,
            right_func=lambda x: x * 2
        )
        
        expected = {
            "root": 5,
            "left": {
                "root": 6,  # 5+1 = 6
                "left": {7},  # 6+1 = 7
                "right": {12}  # 6*2 = 12
            },
            "right": {
                "root": 10,  # 5*2 = 10
                "left": {11},  # 10+1 = 11
                "right": {20}  # 10*2 = 20
            }
        }
        self.assertEqual(result, expected)
    
    def test_default_functions_used(self):
        """Тест что используются функции по умолчанию"""
        result = gen_bin_tree(1, 3)
        
        # С функциями по умолчанию: left = root*2+1, right = 2*root-1
        self.assertEqual(result["left"], {7})  # 3*2+1 = 7
        self.assertEqual(result["right"], {5})  # 2*3-1 = 5

if __name__ == '__main__':
    unittest.main()