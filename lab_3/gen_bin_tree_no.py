
def gen_bin_tree(h, root):

    #Создаем экзепляр дерева (оно же вершина)
    tree = {
        'root': root,
        'left': None,
        'right': None
    }

    nodes = [None, tree]

    #Обозначаем текущий уровень
    level = 0 

    #открываем цикл
    while level != h-1: 
        
        #считаем границы нужных нам вершин
        left_index = 2**(level)
        right_index = 2**(level+1);

        #октрываем цикл по вершинам, которые нужны нам на текущем уровне
        for i in range(left_index, right_index):

            #Текущий элемент
            current = nodes[i]
        
            #Создаем левую и правую ветки
            left = {
            'root': current['root']*2+1,
            'left': None,
            'right': None
            }
            right = {
            'root': current['root']*2-1,
            'left': None,   
            'right': None
            }

            
            current['left'] = left
            current['right'] = right

            #Добавляем ветки в список вершин
            nodes.append(left)
            nodes.append(right)
        level+=1
    return tree

tree = gen_bin_tree(3,1)
print(tree)

        


            
        
            
                

    

                

