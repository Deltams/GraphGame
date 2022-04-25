import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

#Массив цветов
arr_color = [
    '#0000FF',
    '#000000',
    '#FFFF00',
    '#00FFFF',
    '#FF00FF',
    '#00FF00',
    '#FF0000',
    '#C0C0C0',
    '#808080',
    '#800000',
    '#808000',
    '#008000',
    '#800080',
    '#008080',
    '#000080',
    '#FFFFA4',
    '#8042DF',
    '#1B497A',
    '#DEAB6C',
    '#E8BADE'
    ]

# Создание нового графа на основе словоря
def new_graph(map_me): 
    G = nx.Graph()
    for i in map_me:
        if len(map_me[i]) == 0:
            G.add_node(i)
            continue
        for j in map_me[i]:
            G.add_edge(i, j[0], weight=j[1])
    return G

# Закраска ребер графа в стандартный цвет
def new_edge_color(map_me):
    edge_col = []
    for i in map_me:
        for j in map_me[i]:
            edge_col.append('black')
    return edge_col

# Закраска вершин графа в стандартный цвет
def new_node_color(map_me):
    node_col = []
    for i in map_me:
        node_col.append('blue')
    return node_col

# Изменение цвета определенного ребра на заданный цвет
def set_color_edge(G, edge_col, r, col):
    id_col = 0
    for i in G.edges():
        one = -1
        two = -1
        div = 0
        for j in i:
            if div % 2 == 0:
                one = j
            else:
                two = j
            div += 1
        if (one == r[0] and two == r[1]) or (two == r[0] and one == r[1]):
            edge_col[id_col] = col
            break
        id_col+=1
    return edge_col

# Изменение цвета определенной вершины на заданный цвет
def set_color_node(G, node_col, v, col):
    id_col = 0
    for i in G.nodes():
        if v == i:
            node_col[id_col] = col
            break
        id_col+=1
    return node_col

# Отображение пользователю графика на экран
def animation_graph(G, node_col, edge_col):
    plt.clf()
    pos=nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=2)
    #Размер ребер
    edge_lab = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_lab)
##    nx.draw(G, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
    plt.show(block=False)

# Алгоритм Прима
def algo_prim(G, map_me, edge_col, node_col):
    visit_v = set()
    not_visit_v = set()
    for i in map_me:
        not_visit_v.add(i)
        if len(map_me) == len(not_visit_v):
            visit_v.add(i)
            not_visit_v.remove(i)
    set_color_node(G, node_col, list(visit_v)[0], 'yellow')
    while len(not_visit_v) != 0:
        mn = -1
        r = -1
        check_mn = True
        for i in visit_v:
            for j in map_me[i]:
                if j[0] not in visit_v:
                    if check_mn:
                        check_mn = False
                        mn = j[1]
                        r = [i, j[0]]
                    elif mn > j[1]:
                        mn = j[1]
                        r = [i, j[0]]
        set_color_edge(G, edge_col, r, 'red')
        visit_v.add(r[1])
        not_visit_v.remove(r[1])
    animation_graph(G, node_col, edge_col)

### Список смежности с весом ребра
##map_me = {
##    1: [[2, 2], [5, 6], [6, 3]],
##    2: [[1, 2], [3, 4], [6, 1], [7, 7]],
##    3: [[2, 4], [4, 1], [7, 6], [8, 5]],
##    4: [[3, 1], [8, 6]],
##    5: [[1, 6], [6, 5]],
##    6: [[1, 3], [2, 1], [5, 5], [7, 7]],
##    7: [[2, 7], [3, 6], [6, 7], [8, 3]],
##    8: [[3, 5], [4, 6], [7, 3]]
##    }

# Список смежности с весом ребра 2
map_me = {
    0: [[1, 2], [2, 6], [3, 8], [6, 3]],
    1: [[0, 2], [2, 9], [3, 3], [5, 4], [6, 9]],
    2: [[0, 6], [1, 9], [3, 7]],
    3: [[0, 8], [1, 3], [2, 7], [4, 5], [5, 5]],
    4: [[3, 5], [6, 8], [7, 9]],
    5: [[1, 4], [3, 5], [7, 6], [8, 4]],
    6: [[0, 3], [1, 9], [4, 8]],
    7: [[4, 9], [5, 6], [8, 1]],
    8: [[5, 4], [7, 1]]
    }

#Цвета ребер графа
edge_col = new_edge_color(map_me)

#Цвета вершин графа
node_col = new_node_color(map_me)

#Граф пользователя
G = new_graph(map_me)

###Вывод на экран
##animation_graph(G, node_col, edge_col)

# Алгоритм Прима с выводом на экран
algo_prim(G, map_me, edge_col, node_col)
