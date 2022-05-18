from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from collections import deque

FONT = ('Arial', 12, 'normal')

root = Tk()
root.title("Построение минимального остовного дерева")
root.geometry("1100x700+150+50")

arr = []
map_me = {}
copy_map_me = {
    1: [[2, 2], [3, 6], [4, 8], [7, 3]],
    2: [[1, 2], [3, 9], [4, 3], [6, 4], [7, 9]],
    3: [[1, 6], [2, 9], [4, 7]],
    4: [[1, 8], [2, 3], [3, 7], [5, 5], [6, 5]],
    5: [[4, 5], [7, 8], [8, 9]],
    6: [[2, 4], [4, 5], [8, 6], [9, 4]],
    7: [[1, 3], [2, 9], [5, 8]],
    8: [[5, 9], [6, 6], [9, 1]],
    9: [[6, 4], [8, 1]]
    }
clear_ss_ms_mi = 0 # 1 - ss; 2 - ms; 3 - mi;

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

### Список смежности с весом ребра 2
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

def push_map_me():
    global clear_ss_ms_mi, copy_map_me, map_me, arr, entry_matrix, entry_list
    if len(copy_map_me) == 0 or (len(arr) == 0 and (clear_ss_ms_mi == 2 or clear_ss_ms_mi == 3)) or (len(entry_list) == 0 and clear_ss_ms_mi == 1):
        return
    map_me = copy_map_me
    if clear_ss_ms_mi == 1:
        for i in range(len(entry_list)):
            string = ""
            if i+1 > len(map_me):
                break
            for j in map_me[i+1]:
                string += str(j[0]) + '::' + str(j[1]) + ', '
            entry_list[i].delete(0, 'end')
            entry_list[i].insert(0, string[:-2])
        valid_entry_weight()
    elif clear_ss_ms_mi == 2:
        for i in range(len(entry_matrix)):
            if i+1 > len(map_me):
                break
            for j in map_me[i+1]:
                if j[0] >= len(arr[0]):
                    continue
                arr[i][j[0]-1] = j[1]
                arr[j[0]-1][i] = j[1]
                entry_matrix[i][j[0]-1].delete(0, 'end')
                entry_matrix[i][j[0]-1].insert(0, str(j[1]))
                entry_matrix[j[0]-1][i].delete(0, 'end')
                entry_matrix[j[0]-1][i].insert(0, str(j[1]))
        validate_matrix_entry()
    elif clear_ss_ms_mi == 3:
        now_r = 0
        tmp = set()
        print(copy_map_me)
        for i in range(len(entry_matrix)):
            if i+1 > len(map_me) or now_r == len(entry_matrix[0]):
                break
            tmp.add(i+1)
            for j in map_me[i+1]:
                if now_r == len(entry_matrix[0]):
                    break
                if j[0] >= len(arr[0]):
                    continue
                if j[0] in tmp:
                    continue
                arr[i][now_r] = j[1]
                arr[j[0]-1][now_r] = j[1]
                entry_matrix[i][now_r].delete(0, 'end')
                entry_matrix[i][now_r].insert(0, str(j[1]))
                entry_matrix[j[0]-1][now_r].delete(0, 'end')
                entry_matrix[j[0]-1][now_r].insert(0, str(j[1]))
                now_r += 1
        validate_matrix_entry_mi()

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
            if check[i[0]-1] == 0:
                check[i[0]-1] = 1
                ls.append(i[0])
                ch_tru = False
                ans.append([ls[-2], i[0]])
                break
        if ch_tru:
            ls.pop()
    return ans

# Проверка данных в map_me
def valid_map_me(map_me, point_dfs):
    global clear_ss_ms_mi
    
    # Если не создан СС или МС или МИ
    if len(map_me) == 0:
        if clear_ss_ms_mi == 1:
            tk.messagebox.showwarning(title='Оййй, не знал)', message='Создайте список смежности!')
        elif clear_ss_ms_mi == 2:
            tk.messagebox.showwarning(title='Оййй, не знал)', message='Создайте матрицу смежности!')
        elif clear_ss_ms_mi == 3:
            tk.messagebox.showwarning(title='Оййй, не знал)', message='Создайте матрицу инцидентности!')
        else:
            tk.messagebox.showwarning(title='Оййй, не знал)', message='Ошибка, где проблема?')
        return False

    # Если есть пустые строки
    for i in map_me:
        if len(map_me[i]) == 0:
            tk.messagebox.showwarning(title='Оййй, не знал)', message=f'Вершина {i} должна иметь хотябы одну смежную вершину!')
            return False
        
    try:
        #Массив с ходами обхода в глубину
        array = dfs(map_me, point_dfs)
    except:
        tk.messagebox.showwarning(title='Оййй, не знал)', message=f'В графе больше чем одна компонента связности!')
        return False
    
    # Если больше одной компоненты связности
    if len(array)+1 != len(map_me):
        tk.messagebox.showwarning(title='Оййй, не знал)', message=f'В графе больше чем одна компонента связности!')
        return False
    return True

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

pos = None
# Отображение пользователю графика на экран
def animation_graph(G, node_col, edge_col, anim_arr, step):
    global pos
    if len(anim_arr)+1 == step:
        return
    set_color_node(G, node_col, anim_arr[step-1][1], 'yellow')
    set_color_edge(G, edge_col, anim_arr[step-1], 'red')
    plt.clf()
    if step == 1:
        pos=nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=2)
    #Размер ребер
    edge_lab = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_lab)
    plt.show(block=False)
    root.after(500, lambda: animation_graph(G, node_col, edge_col, anim_arr, step+1))

# Алгоритм Прима
def algo_prim(G, map_me, edge_col, node_col):
    anim_arr = []
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
        anim_arr.append(r)
##        set_color_edge(G, edge_col, r, 'red')
        visit_v.add(r[1])
        not_visit_v.remove(r[1])
    animation_graph(G, node_col, edge_col, anim_arr, 1)

def task1_start():
    #Цвета ребер графа
    edge_col = new_edge_color(map_me)

    #Цвета вершин графа
    node_col = new_node_color(map_me)

    #Граф пользователя
    G = new_graph(map_me)

    # Алгоритм Прима с выводом на экран
    algo_prim(G, map_me, edge_col, node_col)

def clear_all():
    global clear_ss_ms_mi
    global entry_list, entry_matrix
    global arr
    
    if clear_ss_ms_mi == 1:
        for i in range(len(entry_list)):
            entry_list[i].config({"background": 'White'})
            entry_list[i].delete(0, 'end')
    elif (clear_ss_ms_mi == 2 or clear_ss_ms_mi == 3) and len(arr) != 0:
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                entry_matrix[i][j].delete(0, 'end')
                arr[i][j] = 0
        if clear_ss_ms_mi == 2:
            validate_matrix_entry()
        else:
            validate_matrix_entry_mi()

# Начало mi    
def validate_matrix_entry_mi():
    global arr, entry_matrix
    # #FAD7D4 Нежно красный
    # #CCFCCC Нежно зеленый
    nd = len(entry_matrix)
    ed = len(entry_matrix[0])
    if int(nd*(nd-1)/2) < ed:
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                entry_matrix[i][j].config({"background": '#FAD7D4'})
        return False

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if not entry_matrix[i][j].get():
                arr[i][j] = 0
                continue
            try:
                arr[i][j] = int(entry_matrix[i][j].get())
                
            except ValueError:
                arr[i][j] = 0
                if root.focus_get() == None:
                    continue
                title = "Ошибка!"
                for ii in range(len(entry_matrix)):
                    entry_matrix[ii][j].config({"background": '#FAD7D4'})
                message = f"В качестве веса вы хотите передать \"{entry_matrix[i][j].get()}\" в ячейке ({i+1},{j+1})"
                messagebox.showwarning(title, message)
    
    for j in range(len(arr[0])):
        one = 0
        for i in range(len(arr)):
            if arr[i][j] != 0:
                one += 1
        
        if one == 2:
            check = True
            ch1 = 0
            ch2 = 0
            for ii in range(len(arr)):
                if arr[ii][j] != 0 and check:
                    ch1 = arr[ii][j]
                    check = False
                elif arr[ii][j] != 0 and not check:
                    ch2 = arr[ii][j]
            if ch1 != ch2:
                for ii in range(len(arr)):
                    entry_matrix[ii][j].config({"background": '#FAD7D4'})
            else:
                for ii in range(len(arr)):
                    entry_matrix[ii][j].config({"background": '#CCFCCC'})
        elif one == 0:
            for ii in range(len(arr)):
                entry_matrix[ii][j].config({"background": 'White'})
        else:
            for ii in range(len(arr)):
                entry_matrix[ii][j].config({"background": '#FAD7D4'})
                
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if not entry_matrix[i][j].get():
                continue
            try:
                int(entry_matrix[i][j].get())
            except ValueError:
                entry_matrix[i][j].config({"background": '#FAD7D4'})
            if entry_matrix[i][j].config("background")[-1] == '#FAD7D4':
                continue
            if arr[i][j] != 0:
                for ii in range(i+1, len(arr)):
                    if arr[ii][j] != 0:
                        for jj in range(j+1, len(arr[i])):
                            if arr[ii][jj] != 0:
                                for iii in range(ii-1, -1, -1):
                                    if i == iii and arr[iii][jj] != 0:
                                        for q in range(len(arr)):
                                            entry_matrix[q][j].config({"background": '#FAD7D4'})
                                            entry_matrix[q][jj].config({"background": '#FAD7D4'})
    return True


def create_matrix_mi():
    global arr, entry_matrix
    canvas.delete('all')
    if int(edge_number_button.get()) > 35:
        edges_number = 35
        messagebox.showwarning(title="Ошибка!", message="Слишком много ребер! Максимум - 35")
    else: 
        edges_number = int(edge_number_button.get())
    if int(node_number_button.get()) > 20:
        nodes_number = 20
        messagebox.showwarning(title="Ошибка!", message="Слишком много вершин! Максимум - 20")
    else: 
        nodes_number = int(node_number_button.get())

    x = 60
    y = 30
    for i in range(1, edges_number+1):
        canvas.create_text(x, y, text=f"{i}", font=FONT)
        x += 30

    x = 30
    y = 60
    for j in range(1, nodes_number+1):
        canvas.create_text(x, y, text=f"{j}", font=FONT)
        y += 30

    y = 60
    last_arr = arr
    arr = []
    entry_matrix = []
    for i in range(1, nodes_number+1):
        x = 30
        tmp = []
        tmp_entry = []
        for j in range(1, edges_number+1):
            x += 30

            entry = Entry(font=FONT, width=2, validate="focusout", validatecommand=validate_matrix_entry_mi)
            entry.bind('<KeyPress>', key_entry)
            canvas.create_window(x, y, window=entry)
            tmp_entry.append(entry)
            
            tmp.append(0)
        arr.append(tmp)
        entry_matrix.append(tmp_entry)
        y += 30

    for i in range(len(arr)):
        if len(last_arr) <= i:
            break
        for j in range(len(arr[i])):
            if len(last_arr[i]) <= j:
                break
            arr[i][j] = last_arr[i][j]
            if arr[i][j] == 0:
                continue
            entry_matrix[i][j].insert(0, str(arr[i][j]))
                
    validate_matrix_entry_mi()


def send_answer_mi():
    global arr, map_me, entry_matrix, copy_map_me
    map_me = {}
    for i in range(len(entry_matrix)):
        map_me[i+1] = []
        for j in range(len(entry_matrix[i])):
            if entry_matrix[i][j].config("background")[-1] == '#FAD7D4':
                messagebox.showwarning(title="Ошибка!", message=f"Проверьте {j+1} столбец!")
                return
    for j in range(len(arr[0])):
        check = True
        ch1 = 0
        for i in range(len(arr)):
            if arr[i][j] != 0 and check:
                ch1 = i
                check = False
            elif arr[i][j] != 0 and not check:
                map_me[ch1+1].append([i+1, arr[ch1][j]])
                map_me[i+1].append([ch1+1, arr[i][j]])
                break
    print(map_me)
    copy_map_me = map_me
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
    global clear_ss_ms_mi

    clear_ss_ms_mi = 1
    canvas.destroy()
    top_canvas.destroy()
    
    top_canvas = Canvas(width=900, height=40, bg='#fad7d4')
    top_canvas.pack()

    label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
    label_v_win = top_canvas.create_window(80, 20, window=label_v)

    node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_win = top_canvas.create_window(310, 20, window=node_number_button)
    node_number_button.current(0)

    button_var_count = Button(text='Создать список смежности', font=('Arial', 12, 'normal'), command=create_entries_ss)
    button_var_count_win = top_canvas.create_window(545, 20, window=button_var_count)

##    save_entries_b = Button(text='print() без веса', font=('Arial', 12, 'normal'), command=save_entries_ss)
##    top_canvas.create_window(700, 20, window=save_entries_b)

    save_entries_b2 = Button(text='Показать дерево', font=('Arial', 12, 'normal'), command=save_entries_with_weight_ss)
    top_canvas.create_window(830, 20, window=save_entries_b2)

    canvas = Canvas(width=900, height=700, bg='#e0defa')
    canvas.pack()
    clear_all()

def input_ms():
    global canvas, top_canvas
    global label_v
    global label_v_win, node_number_button
    global node_number_button_win, button_var_count
    global button_var_count_win, button_send
    global clear_ss_ms_mi
    global arr

    clear_ss_ms_mi = 2
    canvas.destroy()
    top_canvas.destroy()
    arr = []
    
    top_canvas = Canvas(root, width=800, height=40, bg='#fad7d4')
    top_canvas.pack()

    label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
    label_v_win = top_canvas.create_window(80, 20, window=label_v)


    node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_win = top_canvas.create_window(280, 20, window=node_number_button)
    node_number_button.current(0)

    button_var_count = Button(text='Создать матрицу смежности', font=('Arial', 12, 'normal'), command=create_matrix_ms)
    button_var_count_win = top_canvas.create_window(500, 20, window=button_var_count)

    button_send = Button(text="Показать дерево", font=FONT, command=send_answer_ms)
    top_canvas.create_window(730, 20, window=button_send)

    canvas = Canvas(root, width=800, height=650, bg='#e0defa')
    canvas.pack()
    clear_all()

def input_mi():
    global canvas, top_canvas
    global label_v
    global label_v_win, node_number_button
    global node_number_button_win, label_r
    global label_r_win, edge_number_button
    global edge_number_button_win, button_var_count
    global button_var_count_win, button_send
    global clear_ss_ms_mi
    global arr

    clear_ss_ms_mi = 3
    canvas.destroy()
    top_canvas.destroy()
    arr = []
    
    top_canvas = Canvas(root, width=1100, height=40, bg='#fad7d4')
    top_canvas.pack()
    
    label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
    label_v_win = top_canvas.create_window(80, 20, window=label_v)


    node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_win = top_canvas.create_window(250, 20, window=node_number_button)
    node_number_button.current(0)


    label_r = Label(text='Количество ребер', font=('Arial', 12, 'normal'))
    label_r_win = top_canvas.create_window(415, 20, window=label_r)

    edge_number_button = ttk.Combobox(values=[i for i in range(1, 36)], font=('Arial', 12, 'normal'), width=10)
    edge_number_button_win = top_canvas.create_window(577, 20, window=edge_number_button)
    edge_number_button.current(0)


    button_var_count = Button(text='Создать матрицу инцидентности',  font=('Arial', 12, 'normal'), command=create_matrix_mi)
    button_var_count_win = top_canvas.create_window(795, 20, window=button_var_count)

    button_send = Button(text="Показать дерево", font=FONT, command=send_answer_mi)
    top_canvas.create_window(1025, 20, window=button_send)

    canvas = Canvas(root, width=1100, height=650, bg='#e0defa')
    canvas.pack()
    clear_all()
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
    menu_bar.add_cascade(label='Очистить данные', command=clear_all)
    menu_bar.add_cascade(label='Вставить данные', command=push_map_me)
    root.configure(menu=menu_bar)

# Начало ms
def validate_matrix_entry():
    global arr, entry_matrix
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            # #FAD7D4 Нежно красный
            # #CCFCCC Нежно зеленый
            if len(entry_matrix[i][j].get().replace(' ', '')) == 0:
                arr[i][j] = 0
                continue
            if focus_entry == entry_matrix[j][i] and entry_matrix[j][i] != entry_matrix[i][j]:
                continue
            try:
                arr[i][j] = int(entry_matrix[i][j].get())
                if arr[j][i] == None or arr[j][i] == 0:
                    arr[j][i] = int(entry_matrix[i][j].get())
                    entry_matrix[j][i].insert(0, arr[j][i])
            except ValueError:
                arr[i][j] = 0
                if root.focus_get() == None:
                    continue
                title = "Ошибка!"
                message = f"В качестве веса вы хотите передать \"{entry_matrix[i][j].get()}\" в ячейке ({i+1},{j+1})"
                messagebox.showwarning(title, message)
                return False
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] != arr[j][i]:
                entry_matrix[i][j].config({"background": '#FAD7D4'})
            elif arr[i][j] == 0:
                entry_matrix[i][j].config({"background": 'White'})
            else:
                entry_matrix[i][j].config({"background": '#CCFCCC'})
            
    return True


entry_matrix = []
def create_matrix_ms():
    global arr, entry_matrix
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
    last_arr = arr
    arr = []
    entry_matrix = []
    for i in range(1, int(node_number_button.get())+1):
        x = 80
        tmp = []
        tmp_entry = []
        for j in range(1, int(node_number_button.get())+1):
            x += 30

            entry = Entry(font=FONT, width=2, validate="focusout", validatecommand=validate_matrix_entry)
            entry.bind('<KeyPress>', key_entry)
            canvas.create_window(x, y, window=entry)
            tmp_entry.append(entry)

            tmp.append(0)

        entry_matrix.append(tmp_entry)
        arr.append(tmp)
        y += 30

    for i in range(len(arr)):
        if len(last_arr) <= i:
            break
        for j in range(len(arr[i])):
            if len(last_arr[i]) <= j:
                break
            arr[i][j] = last_arr[i][j]
            if arr[i][j] == 0:
                continue

            entry_matrix[i][j].insert(0, str(arr[i][j]))
    validate_matrix_entry()

def send_answer_ms():
    global arr, map_me, copy_map_me
    if not validate_matrix_entry():
        return
    map_me = {}
    for i in range(len(arr)):
        map_me[i+1] = []
        for j in range(len(arr[i])):
            if arr[i][j] == 0:
                continue
            map_me[i+1].append([j+1, arr[i][j]])

            # if arr[number_line][digit]:
            #     map_me[number_line+1].append(digit+1)
    print(map_me)
    print(arr)
    copy_map_me = map_me
    task1_start()
    return map_me
# Конец ms

# Начало ss

def valid_string_not_weight_ss(text):
    tmp_string = text.replace(' ', '').split(',')
    num = int(node_number_button.get())
    vizit = set()
    for i in tmp_string:
        if not len(i):
            return False
        for j in i:
            if not ('0' <= j and j <= '9'):
                return False
        if int(i) > num or int(i) < 0:
            return False
        if int(i) in vizit:
            return False
        vizit.add(int(i))
    return True

def valid_string_weight_ss(text):
    for i in text:
        if not (('0' <= i and i <= '9') or i == ':' or \
           i == ',' or i == ' ' or i == '(' or \
           i == ')' or i == '[' or i == ']' or ' '):
            return False
    tmp_string = text + ' '
    tmp_text = "" 
    for i in range(len(tmp_string)-1):
        if '0' <= tmp_string[i] and tmp_string[i] <= '9' and not ('0' <= tmp_string[i+1] and tmp_string[i+1] <= '9'):
            tmp_text += tmp_string[i] + '_'
        else:
            tmp_text += tmp_string[i]
    stack_check = []
    for i in tmp_text:
        if i == '(' or i == '[':
            if len(stack_check) != 0:
                return False
            stack_check.append(i)
        elif i == ']' or i == ')':
            if len(stack_check) == 0:
                return False
            elem = stack_check[-1]
            stack_check.pop(-1)
            if elem == '(' and i == ')':
                continue
            if elem == '[' and i == ']':
                continue
            return False
    if len(stack_check) != 0:
        return False
    in_skob = ''
    tmp_text2 = ''
    for i in tmp_text:
        if i == '(' or i == '[':
            in_skob = ''
            stack_check.append(i)
        elif i == ')' or i == ']':
            if in_skob.count(',') > 1:
                return False
            if in_skob.count('_') != 2:
                return False
            stack_check.pop(-1)
        elif len(stack_check) == 1:
            in_skob += i
        if len(stack_check) != 1:
            tmp_text2 += i
        else:
            if i != ',':
                tmp_text2 += i
    tmp_text = tmp_text2.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(' ', '').replace('::', '').split(',')
    for i in tmp_text:
        if i.count('_') > 2 or i.count('_') < 1:
            return False
        
    tmp_text = tmp_text2.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(' ', '').split(',')
    for i in tmp_text:
        if i.count('::') > 1:
            return False
        elif i.count('::') == 1:
            if (len(i.split('::')) == 2 and i.split('::')[0] == '') or (len(i.split('::')) == 2 and i.split('::')[1] == ''):
                return False
    return True

focus_entry = None
def key_entry(event):
    global focus_entry
    focus_entry = root.focus_get()

def valid_replace_and_split(text):
    text = text + ' '
    tmp_text = "" 
    for j in range(len(text)-1):
        if '0' <= text[j] and text[j] <= '9' and not ('0' <= text[j+1] and text[j+1] <= '9'):
            tmp_text += text[j] + '_'
        else:
            tmp_text += text[j]
    text = tmp_text
    text = text.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('::', '').replace(' ', '').split(',')
    return text
    

def valid_entry_weight():
    global entry_list
    global focus_entry
    for i in range(len(entry_list)):
        text = entry_list[i].get()
        # #FAD7D4 Нежно красный
        # #CCFCCC Нежно зеленый
        check = valid_string_weight_ss(text)
        if len(text) == text.count(' '):
            entry_list[i].config({"background": 'White'})
        elif check: 
            entry_list[i].config({"background": '#CCFCCC'})
            
            text = valid_replace_and_split(text)
            
            for j in text:
                tmp_text = j.split('_')
                if not (0 < int(tmp_text[0]) and int(tmp_text[0]) <= len(entry_list)):
                    entry_list[i].config({"background": '#FAD7D4'})
                    continue
                if entry_list[int(tmp_text[0])-1] == focus_entry:
                    continue
                tmp = entry_list[int(tmp_text[0])-1].get()
                text2 = entry_list[int(tmp_text[0])-1].get()
                text2 = valid_replace_and_split(text2)
                check = True
                for q in text2:
                    tmp_text2 = q.split('_')
                    if tmp_text2[0] == str(i+1):
                        check = False
                        break
                if check and len(tmp_text) == 2:
                    if len(tmp.replace(' ', '')) == 0:
                        tmp = str(i+1) + '::' + '1'
                    else:
                        tmp = str(i+1) + '::' + '1, ' + tmp
                elif check and len(tmp_text) == 3:
                    if check:
                        if len(tmp.replace(' ', '')) == 0:
                            tmp = str(i+1) + '::' + tmp_text[1]
                        else:
                            tmp = str(i+1) + '::' + tmp_text[1] + ', ' + tmp
                entry_list[int(tmp_text[0])-1].delete(0, 'end')
                entry_list[int(tmp_text[0])-1].insert(0, tmp)
        else:
            entry_list[i].config({"background": '#FAD7D4'})

    for i in range(len(entry_list)):
        text = entry_list[i].get()
        # #FAD7D4 Нежно красный
        # #CCFCCC Нежно зеленый
        if entry_list[i].config("background")[-1] == '#FAD7D4':
            continue
        check = valid_string_weight_ss(text)
        if len(text) == text.count(' '):
            entry_list[i].config({"background": 'White'})
        elif check: 
            entry_list[i].config({"background": '#CCFCCC'})
            
            text = valid_replace_and_split(text)
            vizit = set()
            for j in text:
                tmp_text = j.split('_')
                if not (0 < int(tmp_text[0]) and int(tmp_text[0]) <= len(entry_list)):
                    entry_list[i].config({"background": '#FAD7D4'})
                    continue
                if tmp_text[0] in vizit:
                    entry_list[i].config({"background": '#FAD7D4'})
                    continue
                vizit.add(tmp_text[0])
                text2 = entry_list[int(tmp_text[0])-1].get()
                text2 = valid_replace_and_split(text2)
                check = True
                for q in text2:
                    tmp_text2 = q.split('_')
                    if tmp_text2[0] == str(i+1):
                        check = False
                    if tmp_text2[0] == str(i+1) and tmp_text2[1] != tmp_text[1]:
                        if len(tmp_text2) == 2 and len(tmp_text) == 2:
                            continue
                        if len(tmp_text2) == 2 and tmp_text[1] == '1':
                            continue
                        if len(tmp_text) == 2 and tmp_text2[1] == '1':
                            continue
                        entry_list[i].config({"background": '#FAD7D4'})
                        entry_list[int(tmp_text[0])-1].config({"background": '#FAD7D4'})
                if check:
                    entry_list[i].config({"background": '#FAD7D4'})
                    entry_list[int(tmp_text[0])-1].config({"background": '#FAD7D4'})
        else:
            entry_list[i].config({"background": '#FAD7D4'})
        
    return True

def valid_entry():
    global entry_list
    global focus_entry
    for i in range(len(entry_list)):
        text = entry_list[i].get()
        # #FAD7D4 Нежно красный
        # #CCFCCC Нежно зеленый
        if len(text) == text.count(' '):
            entry_list[i].config({"background": 'White'})
        elif valid_string_not_weight_ss(text): # В данной строке в зависимости от задачи нужно будет менять функцию валидации valid_string_not_weight_ss и valid_string_weight_ss
            entry_list[i].config({"background": '#CCFCCC'})
            text = text.replace(' ', '').split(',')
            for j in text:
                if entry_list[int(j)-1] == focus_entry:
                    continue
                tmp = entry_list[int(j)-1].get()
                entry_list[int(j)-1].delete(0, 'end')
                t = tmp.replace(' ', '').split(',')
                if not str(i+1) in t:
                    if len(tmp.replace(' ', '')) == 0:
                        tmp = str(i+1)
                    else:
                        tmp = str(i+1) + ', ' + tmp
                
                entry_list[int(j)-1].insert(0, tmp)
        else:
            entry_list[i].config({"background": '#FAD7D4'})
    for i in range(len(entry_list)):
        text = entry_list[i].get()
        # #FAD7D4 Нежно красный
        # #CCFCCC Нежно зеленый
        if entry_list[i].config("background")[-1] == '#FAD7D4':
            continue
        if len(text) == text.count(' '):
            entry_list[i].config({"background": 'White'})
            for j in range(len(entry_list)):
                if i == j:
                    continue
                text_j = entry_list[j].get().replace(' ', '').split(',')
                if str(i+1) in text_j:
                    entry_list[i].config({"background": '#FAD7D4'})
                    entry_list[j].config({"background": '#FAD7D4'})
        elif valid_string_not_weight_ss(text): # В данной строке в зависимости от задачи нужно будет менять функцию валидации valid_string_not_weight_ss и valid_string_weight_ss
            entry_list[i].config({"background": '#CCFCCC'})
            
            entry_list[i].delete(0, 'end')
            text = text.replace(' ', '').split(',')
            text2 = []
            for j in range(len(text)):
                text2.append(int(text[j]))
            text2 = sorted(text2)
            for j in range(len(text)):
                text[j] = str(text2[j])
            text2 = text[0]
            for j in range(1, len(text)):
                text2 = text2 + ', ' + text[j]
            entry_list[i].insert(0, text2)
            text = entry_list[i].get()
            
            text = text.replace(' ', '').split(',')
            for j in text:
                tmp = entry_list[int(j)-1].get().replace(' ', '').split(',')
                if not str(i+1) in tmp:
                    entry_list[i].config({"background": '#FAD7D4'})
                    entry_list[int(j)-1].config({"background": '#FAD7D4'})
        else:
            entry_list[i].config({"background": '#FAD7D4'})
    
    return True

entry_list = []
def create_entries_ss():
    global entry_list
    last_entry_list = []
    for i in range(len(entry_list)):
        last_entry_list.append(entry_list[i].get())
    canvas.delete('all')
    entry_list.clear()

    x = 40
    y = 20

    for i in range(1, int(node_number_button.get())+1):
        label = Label(text=f'{i}.', font=('Arial', 12, 'normal'))
        canvas.create_window(x, y, window=label)

        # В данной строке в зависимости от задачи нужно будет менять функцию валидации valid_entry и valid_entry_weight
        entry = Entry(width=60, font=('Arial', 12, 'normal'), validate="focusout", validatecommand=valid_entry_weight)
        entry.bind('<KeyPress>', key_entry)
        canvas.create_window(x+300, y, window=entry)

        entry_list.append(entry)

        y += 30
    for i in range(len(entry_list)):
        if len(last_entry_list) <= i:
            break
        entry_list[i].insert(0, last_entry_list[i])
    # В данной строке в зависимости от задачи нужно будет менять функцию валидации valid_entry и valid_entry_weight
    valid_entry_weight()

def save_entries_ss():
    global map_me
    map_me = {}
    for i in range(len(entry_list)):
        map_me[i+1] = validate_string_ss(entry_list[i].get())
    
    print(map_me)


def validate_string_ss(map_string):
    res = []
    map_string = map_string.split(',')
    for i in map_string:
        ch = 0
        check = True
        for j in i:
            if '0' <= j and j <= '9':
                ch = ch * 10 + int(j)
            elif ch != 0:
                break
        if ch != 0:
            res.append(ch)
    return res


def save_entries_with_weight_ss():
    global map_me, copy_map_me
    map_me = {}
    for i in range(len(entry_list)):
        if len(entry_list[i].get()) == 0:
            map_me[i+1] = []
        else:
            map_me[i+1] = validate_string_with_weight_ss(entry_list[i].get())
    task1_start()
    copy_map_me = map_me
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


button_var_count = Button(text='Создать матрицу инцидентности',  font=('Arial', 12, 'normal'), command=create_matrix_mi)
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

draw_menu()

root.mainloop()
