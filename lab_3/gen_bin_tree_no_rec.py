def gen_bin_tree_no_rec(h, root):
    if h <= 0:
        return {}

    # создаём корень
    tree = {'root': root, 'left': None, 'right': None}

    # список узлов текущего уровня
    current_level = [tree]

    for level in range(1, h):
        next_level = []
        for node in current_level:
            left = {'root': node['root'] * 2 + 1, 'left': None, 'right': None}
            right = {'root': node['root'] * 2 - 1, 'left': None, 'right': None}
            node['left'] = left
            node['right'] = right
            next_level.extend([left, right])
        current_level = next_level

    return tree
