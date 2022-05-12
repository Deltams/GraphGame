from itertools import count
from re import I
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt

FONT = ('Arial', 12, 'normal')

root = Tk()
root.title("Выбор ввода данных")
root.geometry("1100x700+150+50")

photo0 = tk.PhotoImage(file="../img/0.png")
photo1 = tk.PhotoImage(file="../img/1.png")

photo0_h = tk.PhotoImage(file="../img/0_h.png")
photo1_h = tk.PhotoImage(file="../img/1_h.png")

arr = []

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

def task1_start():
    global map_me
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
    animation_graph(G, node_col, edge_col, point_dfs, arr, 1)

# Начало mi
def check_next_mi(cord_i, cord_j):
    tmp_i = int(node_number_button.get())
    tmp_j = int(edge_number_button.get())
    if tmp_i >= cord_i and tmp_j >= cord_j and cord_i >= 0 and cord_j >= 0:
        return True
    return False

def click_mi(event):
    global arr
    cord_j = str(int((event.x-45)/30))
    cord_i = str(int((event.y-45)/30))
    string = cord_i + "_" + cord_j
    string2 = cord_j + "_" + cord_i
    if check_next_mi(int(cord_i), int(cord_j)):
        if arr[int(cord_i)][int(cord_j)] == 0:
            canvas.itemconfigure(string, image=photo1)
            arr[int(cord_i)][int(cord_j)] = 1
        else:
            canvas.itemconfigure(string, image=photo0)
            arr[int(cord_i)][int(cord_j)] = 0

def create_matrix_mi():
    global arr
    canvas.delete('all')

    x = 60
    y = 30
    for i in range(1, int(edge_number_button.get())+1):
        canvas.create_text(x, y, text=f"{i}", font=FONT)
        x += 30

    x = 30
    y = 60
    for j in range(1, int(node_number_button.get())+1):
        canvas.create_text(x, y, text=f"{j}", font=FONT)
        y += 30

    y = 60
    arr = []
    for i in range(1, int(node_number_button.get())+1):
        x = 30
        tmp = []
        for j in range(1, int(edge_number_button.get())+1):
            x += 30
            string = str(i-1) + "_" + str(j-1)
            canvas.create_image(x, y, image=photo0, tag=string)
            canvas.tag_bind(string, '<Button-1>', click_mi)
            #canvas.tag_bind(string, '<Button-1>', on_leave)
            tmp.append(0)
        arr.append(tmp)
        y += 30



def send_answer_mi():
    global map_me
    map_me = {}
    print(arr)
    
    nodes_list = []
    for edge in range(len(arr[0])):
        counter = 0
        tmp_node = []
        for node in range(len(arr)):
            if arr[node][edge]:
                counter += 1
                tmp_node.append(node+1)
                #print(f"ребро {edge+1} соединяет вершину {node+1}")
        
        if counter == 2:
            print(f"ребро {edge+1} соединяет вершины {tmp_node}")
            nodes_list.append(tmp_node)
        elif not counter:
            print(f"ребро {edge+1} не соединяет вершины")
        else:
            print(f"WARNING! Ребро {edge+1} соединяет либо больше 2 вершин, либо 1")
        
    print(nodes_list)
    for pair in nodes_list:
        print(f"{pair[0]} с вершиной {pair[1]}")
        map_me[pair[0]] = []
        map_me[pair[1]] = []
        
    for pair in nodes_list:
        map_me[pair[0]].append(pair[1])
        map_me[pair[1]].append(pair[0])

    for key in map_me.keys():
        map_me[key] = set(map_me[key])
        map_me[key] = list(map_me[key])

    for node in range(len(arr)):
        check = True
        for edge in range(len(arr[0])):
            if arr[node][edge]:
                check = False
                break
        if check:
            map_me[node+1] = []
    print(map_me)
    task1_start()
    return map_me

def open_child_root1():
    # Дописать справку(описание) к определенным заданиям
    pass

def input_ss():
    global canvas, top_canvas
    global label_v
    global label_v_win, node_number_button
    global node_number_button_win, button_var_count
    global button_var_count_win, button_send
    
    canvas.destroy()
    top_canvas.destroy()
    
    top_canvas = Canvas(width=900, height=50, bg='#fad7d4')
    top_canvas.pack()

    label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
    label_v_win = top_canvas.create_window(80, 20, window=label_v)

    node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_win = top_canvas.create_window(280, 20, window=node_number_button)
    node_number_button.current(0)

    button_var_count = Button(text='Создать список смежности', font=('Arial', 12, 'normal'), command=create_entries_ss)
    button_var_count_win = top_canvas.create_window(500, 20, window=button_var_count)

    save_entries_b = Button(text='print() без веса', font=('Arial', 12, 'normal'), command=save_entries_ss)
    top_canvas.create_window(700, 20, window=save_entries_b)

    save_entries_b2 = Button(text='print() с весом', font=('Arial', 12, 'normal'), command=save_entries_with_weight_ss)
    top_canvas.create_window(830, 20, window=save_entries_b2)

    canvas = Canvas(width=900, height=700, bg='#e0defa')
    canvas.pack()

def input_ms():
    global canvas, top_canvas
    global label_v
    global label_v_win, node_number_button
    global node_number_button_win, button_var_count
    global button_var_count_win, button_send
    
    canvas.destroy()
    top_canvas.destroy()
    
    top_canvas = Canvas(root, width=800, height=50, bg='#fad7d4')
    top_canvas.pack()

    label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
    label_v_win = top_canvas.create_window(80, 20, window=label_v)


    node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_win = top_canvas.create_window(280, 20, window=node_number_button)
    node_number_button.current(0)

    button_var_count = Button(text='Создать матрицу смежности', font=('Arial', 10, 'normal'), command=create_matrix_ms)
    button_var_count_win = top_canvas.create_window(500, 20, window=button_var_count)

    button_send = Button(text="Сохранить ответы", font=FONT, command=send_answer_ms)
    top_canvas.create_window(700, 20, window=button_send)

    canvas = Canvas(root, width=800, height=650, bg='#e0defa')
    canvas.pack()

def input_mi():
    global canvas, top_canvas
    global label_v
    global label_v_win, node_number_button
    global node_number_button_win, label_r
    global label_r_win, edge_number_button
    global edge_number_button_win, button_var_count
    global button_var_count_win, button_send
    
    canvas.destroy()
    top_canvas.destroy()
    
    top_canvas = Canvas(root, width=1100, height=50, bg='#fad7d4')
    top_canvas.pack()
    
    label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
    label_v_win = top_canvas.create_window(100, 20, window=label_v)


    node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_win = top_canvas.create_window(250, 20, window=node_number_button)
    node_number_button.current(0)


    label_r = Label(text='Количество ребер', font=('Arial', 12, 'normal'))
    label_r_win = top_canvas.create_window(400, 20, window=label_r)

    edge_number_button = ttk.Combobox(values=[i for i in range(1, 22)], font=('Arial', 12, 'normal'), width=10)
    edge_number_button_win = top_canvas.create_window(550, 20, window=edge_number_button)
    edge_number_button.current(0)


    button_var_count = Button(text='Создать матрицу инцидентности',  font=('Arial', 10, 'normal'), command=create_matrix_mi)
    button_var_count_win = top_canvas.create_window(750, 20, window=button_var_count)

    button_send = Button(text="Сохранить ответы", font=FONT, command=send_answer_mi)
    top_canvas.create_window(950, 20, window=button_send)

    canvas = Canvas(root, width=1100, height=650, bg='#e0defa')
    canvas.pack()
# Конец mi

def draw_menu():
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_cascade(label='Список смежности', command=input_ss)
    file_menu.add_command(label='Матрица смежности', command=input_ms)
    file_menu.add_cascade(label='Матрица инцидентности', command=input_mi)
##    file_menu.add_separator()
    menu_bar.add_cascade(label='Настройки', menu=file_menu)
    menu_bar.add_cascade(label='Справка', command=open_child_root1)
    root.configure(menu=menu_bar)

# Начало ms
def check_next_ms(cord_i, cord_j):
    tmp = int(node_number_button.get())
    if tmp >= cord_i and tmp >= cord_j and cord_i >= 0 and cord_j >= 0:
        return True
    return False

def click_ms(event):
    global arr
    cord_j = str(int((event.x-94)/30))
    cord_i = str(int((event.y-25)/30))
    string = cord_i + "_" + cord_j
    string2 = cord_j + "_" + cord_i
    if check_next_ms(int(cord_i), int(cord_j)):
        if string == string2:
            if arr[int(cord_i)][int(cord_j)] == 0:
                canvas.itemconfigure(string, image=photo1)
                arr[int(cord_i)][int(cord_j)] = 1
            else:
                canvas.itemconfigure(string, image=photo0)
                arr[int(cord_i)][int(cord_j)] = 0
            return
        if arr[int(cord_i)][int(cord_j)] == 0:
            canvas.itemconfigure(string, image=photo1)
            canvas.itemconfigure(string2, image=photo1)
            arr[int(cord_i)][int(cord_j)] = 1
            arr[int(cord_j)][int(cord_i)] = 1
        else:
            canvas.itemconfigure(string, image=photo0)
            canvas.itemconfigure(string2, image=photo0)
            arr[int(cord_i)][int(cord_j)] = 0
            arr[int(cord_j)][int(cord_i)] = 0
    
def create_matrix_ms():
    global arr
    canvas.delete('all')

    x = 110
    y = 10
    for i in range(1, int(node_number_button.get())+1):
        canvas.create_text(x, y, text=f"{i}", font=FONT)
        x += 30

    x = 80
    y = 40
    for j in range(1, int(node_number_button.get())+1):
        canvas.create_text(x, y, text=f"{j}", font=FONT)
        y += 30

    y = 40
    arr = []
    for i in range(1, int(node_number_button.get())+1):
        x = 80
        tmp = []
        for j in range(1, int(node_number_button.get())+1):
            x += 30
            string = str(i-1) + "_" + str(j-1)
            canvas.create_image(x, y, image=photo0, tag=string)
            canvas.tag_bind(string, '<Button-1>', click_ms)
            #canvas.tag_bind(string, '<Button-1>', on_leave)
            tmp.append(0)
        arr.append(tmp)
        y += 30

def send_answer_ms():
    global arr, map_me
    map_me = {}
    for number_line in range(len(arr)):
        map_me[number_line+1] = []

        for digit in range(len(arr[number_line])):
            if arr[number_line][digit]:
                map_me[number_line+1].append(digit+1)
    print(map_me)
    task1_start()
    return map_me
# Конец ms

# Начало ss
entry_list = []
def create_entries_ss():
    canvas.delete('all')
    entry_list.clear()

    x = 40
    y = 20

    for i in range(1, int(node_number_button.get())+1):
        label = Label(text=f'{i}.', font=('Arial', 12, 'normal'))
        canvas.create_window(x, y, window=label)

        entry = Entry(width=30, font=('Arial', 12, 'normal'))
        canvas.create_window(x+150, y, window=entry)

        entry_list.append(entry)

        y += 30

def save_entries_ss():
    global map_me
    map_me = {}
    for i in range(len(entry_list)):
        map_me[i+1] = validate_string_ss(entry_list[i].get())
    task1_start()
    print(map_me)


def validate_string_ss(map_string):
    if ',' in map_string:
        res = map_string.split(',')
        res = [int(item.replace(' ', '')) for item in res]
    else:
        res = map_string.split(' ')
        res = [x for x in res if x]
        res = [int(item) for item in res]
    return res


def save_entries_with_weight_ss():
    global map_me
    map_me = {}
    for i in range(len(entry_list)):
        map_me[i+1] = validate_string_with_weight_ss(entry_list[i].get())
    
    print(map_me)


def validate_string_with_weight_ss(map_string):
    s = map_string.split(',')
    v = -1
    # То что будет храниться в 1: ans
    ans = []
    for i in s:
        tmp = i.replace(' ', '')
        if tmp[0] == '(' or tmp[0] == '[': # Обработка скобок
            v = int(tmp[1:])
        elif tmp[-1] == ')' or tmp[-1] == ']': # Обработка скобок
            ans.append([v, int(tmp[:-1])])
            v = -1
        elif tmp.count('::') == 1: # обработка ::
            ch1 = ""
            ch2 = ""
            check = True
            for j in tmp:
                if j == ':':
                    check = False
                elif check:
                    ch1 += j
                else:
                    ch2 += j
            ans.append([int(ch1), int(ch2)])
            v = -1
        else:
            ch1 = 0
            ch2 = 0
            check = True
            for j in i:
                if j == ' ' and ch1 == 0:
                    continue
                elif j == ' ':
                    check = False
                    continue
                if check and '0' <= j and j <= '9':
                    ch1 = ch1*10 + int(j)
                else:
                    ch2 = ch2*10 + int(j)
            if ch2 <= 0:
                ch2 = 1
            ans.append([ch1, ch2])
    return ans
# Конец ss

# Начало mi
top_canvas = Canvas(root, width=1100, height=50, bg='#fad7d4')
top_canvas.pack()
    
label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
label_v_win = top_canvas.create_window(100, 20, window=label_v)


node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
node_number_button_win = top_canvas.create_window(250, 20, window=node_number_button)
node_number_button.current(0)


label_r = Label(text='Количество ребер', font=('Arial', 12, 'normal'))
label_r_win = top_canvas.create_window(400, 20, window=label_r)

edge_number_button = ttk.Combobox(values=[i for i in range(1, 22)], font=('Arial', 12, 'normal'), width=10)
edge_number_button_win = top_canvas.create_window(550, 20, window=edge_number_button)
edge_number_button.current(0)


button_var_count = Button(text='Создать матрицу инцидентности',  font=('Arial', 10, 'normal'), command=create_matrix_mi)
button_var_count_win = top_canvas.create_window(750, 20, window=button_var_count)

button_send = Button(text="Сохранить ответы", font=FONT, command=send_answer_mi)
top_canvas.create_window(950, 20, window=button_send)

canvas = Canvas(root, width=1100, height=650, bg='#e0defa')
canvas.pack()

canvas.destroy()
top_canvas.destroy()
# Конец mi

# Начало ms
top_canvas = Canvas(root, width=800, height=50, bg='#fad7d4')
top_canvas.pack()

label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
label_v_win = top_canvas.create_window(80, 20, window=label_v)


node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
node_number_button_win = top_canvas.create_window(280, 20, window=node_number_button)
node_number_button.current(0)

button_var_count = Button(text='Построить матрицу смежности', font=('Arial', 10, 'normal'), command=create_matrix_ms)
button_var_count_win = top_canvas.create_window(500, 20, window=button_var_count)

button_send = Button(text="Сохранить ответы", font=FONT, command=send_answer_ms)
top_canvas.create_window(700, 20, window=button_send)

canvas = Canvas(root, width=800, height=650, bg='#e0defa')
canvas.pack()

canvas.destroy()
top_canvas.destroy()
# Конец ms

# Начало ss
top_canvas = Canvas(width=900, height=50, bg='#fad7d4')
top_canvas.pack()

label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
label_v_win = top_canvas.create_window(80, 20, window=label_v)

node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
node_number_button_win = top_canvas.create_window(280, 20, window=node_number_button)
node_number_button.current(0)

button_var_count = Button(text='Создать список смежности', font=('Arial', 12, 'normal'), command=create_entries_ss)
button_var_count_win = top_canvas.create_window(500, 20, window=button_var_count)

save_entries_b = Button(text='print() без веса', font=('Arial', 12, 'normal'), command=save_entries_ss)
top_canvas.create_window(700, 20, window=save_entries_b)

save_entries_b2 = Button(text='print() с весом', font=('Arial', 12, 'normal'), command=save_entries_with_weight_ss)
top_canvas.create_window(830, 20, window=save_entries_b2)

canvas = Canvas(width=900, height=700, bg='#e0defa')
canvas.pack()

canvas.destroy()
top_canvas.destroy()
# Конец ss

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

pos = dict()
# Отображение пользователю графика на экран
def animation_graph(G, node_col, edge_col, v, arr, step):
    global pos
    if len(node_col) == step:
        #Размер ребер
        edge_lab = nx.get_edge_attributes(G,'weight')
        check = 1
        for i in arr:
            edge_lab[(i[0], i[1])] = check
            check += 1
        plt.clf()
        pos=pos
        nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=2)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_lab)
        plt.show(block=False)
        return
    #Размер ребер
    edge_lab = nx.get_edge_attributes(G,'weight')
    set_color_edge(G, edge_col, arr[step-1], 'red')
    edge_lab[(arr[step-1][0], arr[step-1][1])] = step
    plt.clf()
    if step == 1:
        pos=nx.spring_layout(G)
    else:
        pos=pos
    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_lab)
##    nx.draw(G, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
##    plt.legend(labels=[str(v)], loc='best', fontsize=12, shadow=True, framealpha=1, facecolor='#08E8DE', edgecolor='#40E0D0', title=string_legend)
    plt.show(block=False)
    root.after(500, lambda: animation_graph(G, node_col, edge_col, v, arr, step+1))

draw_menu()

root.mainloop()
