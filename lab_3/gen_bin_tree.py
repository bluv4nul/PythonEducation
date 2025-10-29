# Root = 9; height = 6, left_leaf = root*2+1, right_leaf = 2*root-1 

def gen_bin_tree(height, root, left_func=None, right_func=None):

    #Базовые случаи
    if height < 0:
        return {}
    elif height == 0:
        return {root}
    
    #Устанавливаем функции по умолчанию
    if left_func is None:
        left_func = lambda x: x * 2 + 1
    if right_func is None:
        right_func = lambda x: 2 * x - 1
    

    #Создаем словарь для дерева
    tree = {
        #Указываем корень, для каждого числа корнем будет оно само
        "root" : root,
        #Создаем левую ветку через рекурсию
        "left" : gen_bin_tree(height-1, left_func(root), left_func, right_func),
        #Создаем правую ветку через рекурсию
        "right" : gen_bin_tree(height-1, right_func(root), left_func, right_func)
    }
    
    return tree
