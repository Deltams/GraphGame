import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Создание нового графа на основе словоря
def new_graph(map_me): 
    G = nx.Graph()
    for i in map_me:
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
def animation_graph_bfs(G, node_col, edge_col, arr):
    if len(arr) == 0:
        return
    if arr[0][2] % 2 == 1:
        edge_col = set_color_edge(G, edge_col, arr[0], 'red')
    else:
        edge_col = set_color_edge(G, edge_col, arr[0], 'blue')
    plt.clf()
    nx.draw(G, with_labels= True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
    plt.show(block=False)
    animation_graph_bfs(G, node_col, edge_col, arr[1:]) 

# Обход графа в ширину
def bfs(map_me, v):
    ans = []
    check_v = [0]*len(map_me)
    check_v[v-1] = 1
    dq = deque()
    dq.append(v)
    step = 1
    while len(dq) > 0:
        new_dq = deque()
        while len(dq) > 0:
            cell = dq.popleft()
            for i in map_me[cell]:
                if check_v[i-1] == 0:
                    new_dq.append(i)
                    ans.append([cell, i, step])
            check_v[cell-1] = 1
        dq = new_dq
        step += 1
    return ans

# Список смежности 
map_me = {
    1: [2, 3],
    2: [1, 4, 5],
    3: [1, 6, 7],
    4: [2, 8],
    5: [2],
    6: [3],
    7: [3],
    8: [4]
    }

# Начальная точка обхода графа в глубину
point_bfs = 8

#Цвета ребер графа
edge_col = new_edge_color(map_me)

#Цвета вершин графа
node_col = new_node_color(map_me)

#Граф пользователя
G = new_graph(map_me)

#Массив с ходами обхода в глубину
arr = bfs(map_me, point_bfs)

#Изменяем цвет точки с которой начинали обход
node_col = set_color_node(G, node_col, point_bfs, 'yellow')

#Отображает пользователю обход графа в глубину
animation_graph_bfs(G, node_col, edge_col, arr)
