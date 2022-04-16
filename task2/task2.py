import networkx as nx
import matplotlib.pyplot as plt
import random
import tkinter as tk
root = tk.Tk()

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

# Проверка введеных данных пользователя для выданого графа
def check_user_input(map_me, arr_user):
    st = []
    st2 = set()
    for r in arr_user:
        check = True
        for v in map_me[r[0]]:
            if v == r[1]:
                check = False
                break
        if check:
            return False
        if r[1] in st2:
            return False
        st2.add(r[1])
    for v in map_me:
        if v not in st2:
            st.append(v)    
    if len(st) != 1:
        return False
    return True

# Создание нового случайного графа (Возвращается в виде матрицы смежности)
# Забавная фича из бага, можно использовать где-то
def new_random_map_me_bag():
    all_v = int(random.random()*100)%20 + 1
    new_map_me = dict()
    for i in range(1, all_v+1):
        new_map_me[i] = set()
    tmp = 1
    while tmp < all_v+1:
        r = int(random.random()*100)%all_v + 1
        while i == r:
            r = int(random.random()*100)%all_v + 1
        new_map_me[r].add(i)
        new_map_me[i].add(r)
        if int(random.random()*100) % 7 != 0:
            tmp -= 1
        tmp += 1
    for i in range(1, all_v+1):
        new_map_me[i] = list(new_map_me[i])
    return new_map_me

# Создание нового случайного графа (Возвращается в виде матрицы смежности)
def new_random_map_me():
    all_v = int(random.random()*100)%19 + 2
    new_map_me = dict()
    for i in range(1, all_v+1):
        new_map_me[i] = set()
    tmp = 1
    while tmp < all_v+1:
        r = int(random.random()*100)%all_v + 1
        while tmp == r:
            r = int(random.random()*100)%all_v + 1
        new_map_me[r].add(tmp)
        new_map_me[tmp].add(r)
        if int(random.random()*100) % 3 != 0:
            tmp -= 1
        tmp += 1
    for i in range(1, all_v+1):
        new_map_me[i] = list(new_map_me[i])
    return new_map_me
    
# Массив, который пользователь будет вводить (Bro)
arr_user = [[1, 6], [6, 7], [1, 2], [2, 3], [3, 5], [2, 4]]

# Массив, который пользователь будет вводить (Ne Bro)
bad_arr_user_1 = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]

# Массив, который пользователь будет вводить (Ne Bro)
bad_arr_user_2 = [[1, 2], [2, 3], [3, 1]]

# Массив, который пользователь будет вводить (Ne Bro)
bad_arr_user_3 = [[1, 2], [2, 3], [3, 1], [3, 4], [4, 5], [5, 6], [6, 7]]

# Массив, который пользователь будет вводить (Ne Bro)
bad_arr_user_4 = [[1, 6], [6, 7], [1, 2], [2, 3], [3, 5]]

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
# Создание случайного списка смежности
map_me = new_random_map_me()

# Начальная точка обхода графа в глубину
point_ovg = 1

#Цвета ребер графа
edge_col = new_edge_color(map_me)

#Цвета вершин графа
node_col = new_node_color(map_me)

#Граф пользователя
G = new_graph(map_me)
nx.draw(G, with_labels= True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
plt.show(block=False)

#Массив с ходами обхода в глубину
arr = ovg(map_me, point_ovg)

#Изменяем цвет точки с которой начинали обход
node_col = set_color_node(G, node_col, point_ovg, 'yellow')

#Отображает пользователю обход графа в глубину
animation_graph_ovg(G, node_col, edge_col, arr)

#Пример ввода данных (работает через консоль и в этот момент все окна не активны(сломаны))
#1, 2, 2, 3, 3, 4
#[1, 2], [2, 3], [3, 4]
def inp(map_me):
    arr_user = input('Введите данные: ').replace('[', ''). replace(']', '').split(', ')
    ans = []
    for i in range(0, len(arr_user), 2):
        ans.append([int(arr_user[i]), int(arr_user[i+1])])
    print(check_user_input(map_me, ans))

root.after(2000, lambda: inp(map_me))


