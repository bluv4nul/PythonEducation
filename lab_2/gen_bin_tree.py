# Root = 9; height = 6, left_leaf = root*2+1, right_leaf = 2*root-1 

def gen_bin_tree(height, root):
    #Проверяем не дошли ли мы до конца
    if height == 0:
        return {}
    
    #Создаем словарь для дерева
    tree = {
        #Указываем корень, для каждого числа корнем будет оно само
        "root" : root,
        #Создаем левую ветку через рекурсию
        "left" : gen_bin_tree(height-1, root*2+1) if height > 1 else None,
        #Создаем правую ветку через рекурсию
        "right" : gen_bin_tree(height-1, 2*root-1) if height > 1 else None

        #Каждую вложенную итерацию высота уменьшается, а корень считается по формуле 
    }
    
    return tree
