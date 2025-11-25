import unittest
from gen_bin_tree_no_rec import gen_bin_tree_no_rec


class TestGenBinTree(unittest.TestCase):

    def test_height_zero(self):
        """Тест для высоты 0"""
        result = gen_bin_tree_no_rec(0, 5)
        expected = {"root": 5}
        self.assertEqual(result, expected)

    def test_height_one(self):
        """Тест для высоты 1"""
        result = gen_bin_tree_no_rec(1, 1)
        expected = {"root": 1, "left": None, "right": None}
        self.assertEqual(result, expected)

    def test_height_two(self):
        """Тест для высоты 2"""
        result = gen_bin_tree_no_rec(2, 1)
        expected = {
            "root": 1,
            "left": {"root": 3, "left": None, "right": None},  # 1*2+1 = 3
            "right": {"root": 1, "left": None, "right": None},  # 1*2-1 = 1
        }
        self.assertEqual(result, expected)

    def test_height_three(self):
        """Тест для высоты 3"""
        result = gen_bin_tree_no_rec(3, 2)
        expected = {
            "root": 2,
            "left": {
                "root": 5,
                "left": {"root": 11, "left": None, "right": None},
                "right": {"root": 9, "left": None, "right": None},
            },
            "right": {
                "root": 3,
                "left": {"root": 7, "left": None, "right": None},
                "right": {"root": 5, "left": None, "right": None},
            },
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
