import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

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
def animation_graph_bfs(G, node_col, edge_col):
    plt.clf()
    nx.draw(G, with_labels= True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
    plt.show(block=False) 

# Обход графа в ширину
def bfs(map_me, v):
    ans = []
    check_v = [0]*len(map_me)
    check_v[v-1] = 1
    dq = deque()
    dq.append(v)
    tmp = []
    while len(dq) > 0:
        new_dq = deque()
        while len(dq) > 0:
            cell = dq.popleft()
            for i in map_me[cell]:
                if check_v[i-1] == 0:
                    new_dq.append(i)
                    ans.append([cell, i])
            tmp.append(cell)
            check_v[cell-1] = 1
        dq = new_dq
    return ans, tmp

# Число компонент связности
def count_ks(G, map_me, edge_col, node_col, arr_color):
    all_v = []
    for i in map_me:
        all_v.append(i)
    ans = 0
    id_start = 0
    for i in range(id_start, len(all_v)):
        if all_v[i] != -1:
            arr_bfs, arr_bfs_user = bfs(map_me, all_v[i])
            for j in range(len(arr_bfs)):
                edge_col = set_color_edge(G, edge_col, arr_bfs[j], arr_color[i])
            for j in arr_bfs_user:
                all_v[j-1] = -1
                set_color_node(G, node_col, j, arr_color[i])
            ans += 1
    #animation_graph_bfs(G, node_col, edge_col)
    return ans
    
### Список смежности 
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

# Список смежности 
map_me = {
    1: [2, 3],
    2: [1, 3],
    3: [2, 1],
    4: [5, 6],
    5: [4, 6],
    6: [4, 5],
    7: [8, 9],
    8: [7, 9],
    9: [7, 8],
    10:[11, 12],
    11:[10, 12],
    12:[10, 11],
    13:[14, 15],
    14:[13, 15],
    15:[13, 14],
    16:[17, 18],
    17:[16, 18],
    18:[16, 17, 19],
    19:[18, 20],
    20:[19]
    }

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

#Цвета ребер графа
edge_col = new_edge_color(map_me)

#Цвета вершин графа
node_col = new_node_color(map_me)

#Граф пользователя
G = new_graph(map_me)

#Количество компонент связности
print(count_ks(G, map_me, edge_col, node_col, arr_color))

