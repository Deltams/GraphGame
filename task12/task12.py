import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

#Массив цветов
arr_color = [
    '#FFFF00',
    '#0000FF',
    '#40E0D0',
    '#008080',
    '#FF00FF',
    '#00FF00',
    '#FF0000',
    '#C0C0C0',
    '#808080',
    '#800000',
    '#808000',
    '#008000',
    '#800080',
    '#00FFFF',
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
            G.add_edge(i, j)
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
def animation_graph_bfs(G, node_col, edge_col, count_col):
    plt.clf()
    nx.draw(G, with_labels= True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
    plt.legend(labels=[str(count_col)], loc='best', fontsize=12, shadow=True, framealpha=1, facecolor='#08E8DE', edgecolor='#40E0D0', title='Всего цветов использовано')
    plt.show(block=False)

#Раскраска графа
def paint_graph(G, node_col, edge_col, map_me, arr_color):
    arr_v = []
    for i in map_me:
        arr_v.append([len(map_me[i]), i])
    arr_v.sort()
    tmp_arr_v = deque()
    s = 0
    for i in range(1, len(arr_v)):
        if arr_v[i][0] != arr_v[i-1][0]:
            for j in range(i-1, s-1, -1):
                tmp_arr_v.appendleft(arr_v[j])
            s = i
    if s <= len(arr_v)-1:
        for j in range(len(arr_v)-1, s-1, -1):
            tmp_arr_v.appendleft(arr_v[j])

    arr_v = list(tmp_arr_v)
    check_arr_v = [0]*(len(arr_v))
    check_col_v = [0]*(len(arr_v)+1)
    col = 0
    step = 1
    while True:
        v = -1
        for i in range(len(check_arr_v)):
            if check_arr_v[i] == 0:
                v = arr_v[i][1]
                check_col_v[arr_v[i][1]] = step
                check_arr_v[i] = step
                break
        if v == -1:
            break
        set_color_node(G, node_col, v, arr_color[col])
        for i in range(len(arr_v)):
            if check_arr_v[i] == 0:
                check_for = False
                for j in map_me[arr_v[i][1]]:
                    if check_col_v[j] == step:
                        check_for = True
                        break
                if check_for:
                    continue
                set_color_node(G, node_col, arr_v[i][1], arr_color[col])
                check_col_v[arr_v[i][1]] = step
                check_arr_v[i] = step
        col += 1
        step += 1
    animation_graph_bfs(G, node_col, edge_col, col)
        
### Список смежности ans = 2
##map_me = {
##    1: [2, 3],
##    2: [1, 4, 5],
##    3: [1, 6, 7],
##    4: [2, 8],
##    5: [2],
##    6: [3],
##    7: [3],
##    8: [4]
##    }

### Список смежности 2 ans = 3
##map_me = {
##    1: [2, 3],
##    2: [1, 4, 5],
##    3: [1, 4, 6],
##    4: [2, 3, 5, 6],
##    5: [2, 4, 7],
##    6: [3, 4, 8, 9],
##    7: [5, 8, 10],
##    8: [6, 7, 9],
##    9: [6, 8],
##    10: [7]
##    }

# Список смежности 3 ans = 4 what?
map_me = {
    1: [2, 4, 5, 8],
    2: [1, 3, 5, 6],
    3: [2, 4, 6, 7],
    4: [1, 3, 7, 8],
    5: [1, 2, 6, 7, 8],
    6: [2, 3, 5, 7, 8],
    7: [3, 4, 5, 6, 8],
    8: [1, 4, 5, 6, 7]
    }

### Список смежности 4 ans = 3
##map_me = {
##    1: [2, 5, 6],
##    2: [1, 3, 7],
##    3: [2, 4, 8],
##    4: [3, 5, 9],
##    5: [1, 4, 10],
##    6: [1, 8, 9],
##    7: [2, 9, 10],
##    8: [3, 6, 10],
##    9: [4, 6, 8],
##    10:[5, 7, 8]
##    }

### Список смежности 5 ans = 4
##map_me = {
##    1: [2, 3, 4],
##    2: [1, 3, 4],
##    3: [1, 2, 4],
##    4: [1, 2, 3]
##    }

### Список смежности 6 ans = 3
##map_me = {
##    1: [2, 4, 5],
##    2: [1, 3, 5],
##    3: [2, 4, 5],
##    4: [1, 3, 5],
##    5: [1, 2, 3, 4]
##    }

### Список смежности 7 ans = 3 what
##map_me = {
##    1: [2, 5, 6],
##    2: [1, 3, 4, 8],
##    3: [2, 4, 8],
##    4: [2, 3, 5, 7],
##    5: [1, 4, 6, 7],
##    6: [1, 5, 7],
##    7: [4, 5, 6, 8],
##    8: [2, 3, 7]
##    }

### Список смежности 8 ans = 3
##map_me = {
##    1: [3, 8],
##    2: [3, 5],
##    3: [1, 2, 4],
##    4: [3, 6, 7],
##    5: [2, 7],
##    6: [4, 8],
##    7: [4, 5],
##    8: [1, 6]
##    }

#Цвета ребер графа
edge_col = new_edge_color(map_me)

#Цвета вершин графа
node_col = new_node_color(map_me)

#Граф пользователя
G = new_graph(map_me)

# Вывод на экран раскраски графа
paint_graph(G, node_col, edge_col, map_me, arr_color)
