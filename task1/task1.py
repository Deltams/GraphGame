import networkx as nx
import matplotlib.pyplot as plt   

# Проверка для dfs
def check_check(check):
    for i in check:
        if i == 0:
            return True
    return False

# Обход графа в глубину
def dfs(map_me, v): 
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
def animation_graph(G, node_col, edge_col, v, arr):
    #Размер ребер
    edge_lab = nx.get_edge_attributes(G,'weight')
    step = 1
    for i in arr:
        set_color_edge(G, edge_col, i, 'red')
        edge_lab[(i[0], i[1])] = step
        step += 1
    plt.clf()
    pos=nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_lab)
##    nx.draw(G, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
##    plt.legend(labels=[str(v)], loc='best', fontsize=12, shadow=True, framealpha=1, facecolor='#08E8DE', edgecolor='#40E0D0', title=string_legend)
    plt.show(block=False)

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
point_dfs = 1

#Цвета ребер графа
edge_col = new_edge_color(map_me)

#Цвета вершин графа
node_col = new_node_color(map_me)

#Граф пользователя
G = new_graph(map_me)

#Массив с ходами обхода в глубину
arr = dfs(map_me, point_dfs)

#Изменяем цвет точки с которой начинали обход
node_col = set_color_node(G, node_col, point_dfs, 'yellow')

#Отображает пользователю обход графа в глубину
animation_graph(G, node_col, edge_col, point_dfs, arr)

