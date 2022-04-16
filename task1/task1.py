import networkx as nx
import matplotlib.pyplot as plt   

# Проверка для ovg
def check_check(check):
    for i in check:
        if i == 0:
            return True
    return False

# Обход графа в глубину
def ovg(map_me, v): 
    check=[0]*len(map_me)
    check[v-1] = 1

    ans = []
    ls = [v]
    while check_check(check):
        list_me = map_me[ls[-1]]
        ch_tru = True
        for i in list_me:
            if check[i-1] == 0:
                check[i-1] = 1
                ls.append(i)
                ch_tru = False
                ans.append([ls[-2], i])
                break
        if ch_tru:
            ls.pop()
            
    return ans

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
def animation_graph_ovg(G, node_col, edge_col, arr):
    if len(arr) == 0:
        return
    edge_col = set_color_edge(G, edge_col, arr[0], 'red')
    plt.clf()
    nx.draw(G, with_labels= True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
    plt.show(block=False)
    animation_graph_ovg(G, node_col, edge_col, arr[1:])

# Список смежности   
map_me = {
    1: [2, 6],
    2: [1, 3, 4, 7],
    3: [2, 4, 5],
    4: [2, 3],
    5: [3],
    6: [1, 7],
    7: [2, 6]
    }

# Начальная точка обхода графа в глубину
point_ovg = 1

#Цвета ребер графа
edge_col = new_edge_color(map_me)

#Цвета вершин графа
node_col = new_node_color(map_me)

#Граф пользователя
G = new_graph(map_me)

#Массив с ходами обхода в глубину
arr = ovg(map_me, point_ovg)

#Изменяем цвет точки с которой начинали обход
node_col = set_color_node(G, node_col, point_ovg, 'yellow')

#Отображает пользователю обход графа в глубину
animation_graph_ovg(G, node_col, edge_col, arr)

