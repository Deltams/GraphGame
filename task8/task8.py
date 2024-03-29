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
def animation_graph(G, node_col, edge_col, v, string_legend):
    plt.clf()
    pos=nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=2)
    #Размер ребер
    edge_lab = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_lab)
##    nx.draw(G, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
    plt.legend(labels=[str(v)], loc='best', fontsize=12, shadow=True, framealpha=1, facecolor='#08E8DE', edgecolor='#40E0D0', title=string_legend)
    plt.show(block=False)
    

# Наахождения кратчайших путей от заданной вершины до остальных
# вершин графа
def min_dist_nodes(G, node_col, edge_col, map_me, point_start):
    visit_v = set()
    dq = deque()
    dq.append([point_start, 0])
    ans = dict()
    for i in map_me:
        ans[i] = 1000000
    ans[point_start] = 0
    while len(dq) > 0:
        v = dq.popleft()
        visit_v.add(v[0])
        mn = [1000000, 1000000]
        for i in visit_v:
            for j in map_me[i]:
                if j[0] not in visit_v:
                    if mn[1] > j[1]:
                        mn = j
                    ans[j[0]] = min(ans[j[0]], ans[i] + j[1])
        if mn[0] != 1000000:
            dq.append(mn)
    string_legend = ""
    for i in ans:
        string_legend += f'{i}: {ans[i]}\n'
    animation_graph(G, node_col, edge_col, point_start, string_legend)

# Список смежности с весом ребра
map_me = {
    1: [[2, 2], [5, 6], [6, 3]],
    2: [[1, 2], [3, 4], [6, 1], [7, 7]],
    3: [[2, 4], [4, 1], [7, 6], [8, 5]],
    4: [[3, 1], [8, 6]],
    5: [[1, 6], [6, 5]],
    6: [[1, 3], [2, 1], [5, 5], [7, 7]],
    7: [[2, 7], [3, 6], [6, 7], [8, 3]],
    8: [[3, 5], [4, 6], [7, 3]]
    }

### Список смежности с весом ребра
##map_me = {
##    1: [[2, 2], [3, 6], [4, 8], [7, 3]],
##    2: [[1, 2], [3, 9], [4, 3], [6, 4], [7, 9]],
##    3: [[1, 6], [2, 9], [4, 7]],
##    4: [[1, 8], [2, 3], [3, 7], [5, 5], [6, 5]],
##    5: [[4, 5], [7, 8], [8, 9]],
##    6: [[2, 4], [4, 5], [8, 6], [9, 4]],
##    7: [[1, 3], [2, 9], [5, 8]],
##    8: [[5, 9], [6, 6], [9, 1]],
##    9: [[6, 4], [8, 1]]
##    }

# Точка(вершина), с которой начинаем
point_start = 8

#Цвета ребер графа
edge_col = new_edge_color(map_me)

#Цвета вершин графа
node_col = new_node_color(map_me)

#Граф пользователя
G = new_graph(map_me)

#Вывод на экран минимального прохождения по ребрам
min_dist_nodes(G, node_col, edge_col, map_me, point_start)


