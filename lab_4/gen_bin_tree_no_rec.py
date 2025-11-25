from collections import deque


def gen_bin_tree_no_rec(h, root):
    """

    Генерирует полное бинарное дерево заданной высоты без использования рекурсии.

    Использует обход в ширину (BFS) с помощью очереди deque для построения дерева.
    Каждый родительский узел имеет двух потомков: left = root * 2 + 1, right = root * 2 - 1.

    Параметры:
    h (int): Высота дерева. Если h <= 0, возвращается только корень.
    root (int): Значение корневого узла.

    Возвращает:
    dict: Словарь, представляющий бинарное дерево в виде:
          {"root": value, "left": left_subtree, "right": right_subtree}
          где left_subtree и right_subtree имеют такую же структуру.

    Примеры:
    >>> gen_bin_tree_no_rec(2, 1)
    {'root': 1, 'left': {'root': 3, 'left': None, 'right': None},
     'right': {'root': 1, 'left': None, 'right': None}}

    >>> gen_bin_tree_no_rec(0, 5)
    {'root': 5}

    """
    if h <= 0:
        return {"root": root}

    # создаём корень
    tree = {"root": root, "left": None, "right": None}

    # список узлов текущего уровня
    current_level = deque([tree])

    for level in range(1, h):
        next_level = deque()
        while current_level:
            node = current_level.popleft()
            left = {"root": node["root"] * 2 + 1, "left": None, "right": None}
            right = {"root": node["root"] * 2 - 1, "left": None, "right": None}
            node["left"] = left
            node["right"] = right
            next_level.append(left)
            next_level.append(right)
        current_level = next_level

    return tree
