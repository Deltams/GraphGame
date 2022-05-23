from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.backend_tools import ToolBase
plt.rcParams["toolbar"] = "toolmanager"

FONT = ('Arial', 12, 'normal')

root = Tk()
root.title("Обход графа в ширину")
root.geometry("1100x700+150+50")

photo0 = tk.PhotoImage(file="../img/0.png")
photo1 = tk.PhotoImage(file="../img/1.png")

photo0_h = tk.PhotoImage(file="../img/0_h.png")
photo1_h = tk.PhotoImage(file="../img/1_h.png")

photo0_d = tk.PhotoImage(file="../img/0_d.png")
photo1_d = tk.PhotoImage(file="../img/1_d.png")

photo0_g = tk.PhotoImage(file="../img/0_g.png")
photo1_g = tk.PhotoImage(file="../img/1_g.png")

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

clear_ss_ms_mi = 0 # 1 - ss; 2 - ms; 3 - mi;

class PlayTool(ToolBase):
    global stop_animation, step_pos, map_me, check_leftArrow
    global point_bfs_anim, edge_col_anim, node_col_anim, G_anim, arr_anim
    
    description = "Проиграть анимацию"
    #image = r'C:\Users\user\Documents\dev\dm-graph\img\play.png'

    def trigger(self, *args, **kwargs):
        global stop_animation, step_pos, map_me, check_leftArrow
        global point_bfs_anim, edge_col_anim, node_col_anim, G_anim, arr_anim
        if not stop_animation:
            return
        if len(arr_anim) == step_pos:
            step_pos = 1
        stop_animation = False
        check_leftArrow = False
        #Цвета ребер графа
        edge_col_anim = new_edge_color(map_me)

        #Цвета вершин графа
        node_col_anim = new_node_color(map_me)
        node_col_anim = set_color_node(G_anim, node_col_anim, point_bfs_anim, 'yellow')
        for i in range(step_pos):
            if arr_anim[i][2] % 2 == 1:
                edge_col_anim = set_color_edge(G_anim, edge_col_anim, arr_anim[i], 'red')
            else:
                edge_col_anim = set_color_edge(G_anim, edge_col_anim, arr_anim[i], 'blue')
        animation_graph(G_anim, node_col_anim, edge_col_anim, point_bfs_anim, arr_anim, step_pos)


class PauseTool(ToolBase):
    global stop_animation, step_pos, map_me, check_leftArrow
    global point_bfs_anim, edge_col_anim, node_col_anim, G_anim, arr_anim

    description = "Остановить анимацию"
    #image = r'C:\Users\user\Documents\dev\dm-graph\img\pause.png'

    def trigger(self, *args, **kwargs):
        global stop_animation, step_pos, map_me, check_leftArrow
        global point_bfs_anim, edge_col_anim, node_col_anim, G_anim, arr_anim
        if stop_animation:
            return
        stop_animation = True
        step_pos = -1
        if step_pos < 1:
            setp_pos = 1
        check_leftArrow = True
        #print("Pause")

check_leftArrow = True
class LeftArrowTool(ToolBase):
    global stop_animation, step_pos, map_me, pos, check_leftArrow
    global point_bfs_anim, edge_col_anim, node_col_anim, G_anim, arr_anim
    
    default_keymap = 'left'
    description = "Перейти на шаг назад"
    #image = r'C:\Users\user\Documents\dev\dm-graph\img\left.png'

    def trigger(self, *args, **kwargs):
        global stop_animation, step_pos, map_me, pos, check_leftArrow
        global point_bfs_anim, edge_col_anim, node_col_anim, G_anim, arr_anim
        
        if not stop_animation:
            return
        if step_pos <= 1:
            step_pos = 1
            return
        step_pos -= 1
        #Цвета ребер графа
        edge_col_anim = new_edge_color(map_me)

        #Цвета вершин графа
        node_col_anim = new_node_color(map_me)
        node_col_anim = set_color_node(G_anim, node_col_anim, point_bfs_anim, 'yellow')
        for i in range(step_pos):
            if arr_anim[i][2] % 2 == 1:
                edge_col_anim = set_color_edge(G_anim, edge_col_anim, arr_anim[i], 'red')
            else:
                edge_col_anim = set_color_edge(G_anim, edge_col_anim, arr_anim[i], 'blue')
        edge_lab = nx.get_edge_attributes(G_anim,'weight')
        edge_lab[(arr_anim[step_pos-1][0], arr_anim[step_pos-1][1])] = arr_anim[step_pos-1][2]
        plt.clf()
        nx.draw_networkx(G_anim, pos, with_labels=True, font_weight='bold', node_color=node_col_anim, edge_color=edge_col_anim, width=2)
        nx.draw_networkx_edge_labels(G_anim, pos, edge_labels=edge_lab)
    ##    nx.draw(G, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
    ##    plt.legend(labels=[str(v)], loc='best', fontsize=12, shadow=True, framealpha=1, facecolor='#08E8DE', edgecolor='#40E0D0', title=string_legend)

        plt.show(block=False)
        check_leftArrow = False
        #print("Left")


class RightArrowTool(ToolBase):
    global stop_animation, step_pos, map_me, pos, check_leftArrow
    global point_bfs_anim, edge_col_anim, node_col_anim, G_anim, arr_anim
    
    default_keymap = 'right'
    description = "Перейти на шаг вперёд"
    #image = r'C:\Users\user\Documents\dev\dm-graph\img\right.png'

    def trigger(self, *args, **kwargs):
        global stop_animation, step_pos, map_me, pos, check_leftArrow
        global point_bfs_anim, edge_col_anim, node_col_anim, G_anim, arr_anim

        if not stop_animation:
            return
        if len(arr_anim) <= step_pos:
            step_pos = len(arr_anim)
            #Размер ребер
            edge_lab = nx.get_edge_attributes(G_anim,'weight')
            check = 1
            for i in arr_anim:
                edge_lab[(i[0], i[1])] = i[2]
            plt.clf()
            nx.draw_networkx(G_anim, pos, with_labels=True, font_weight='bold', node_color=node_col_anim, edge_color=edge_col_anim, width=2)
            nx.draw_networkx_edge_labels(G_anim, pos, edge_labels=edge_lab)
            plt.show(block=False)
            return
        step_pos += 1
        #Цвета ребер графа
        edge_col_anim = new_edge_color(map_me)

        #Цвета вершин графа
        node_col_anim = new_node_color(map_me)
        node_col_anim = set_color_node(G_anim, node_col_anim, point_bfs_anim, 'yellow')
        for i in range(step_pos):
            if arr_anim[i][2] % 2 == 1:
                edge_col_anim = set_color_edge(G_anim, edge_col_anim, arr_anim[i], 'red')
            else:
                edge_col_anim = set_color_edge(G_anim, edge_col_anim, arr_anim[i], 'blue')
        edge_lab = nx.get_edge_attributes(G_anim,'weight')
        edge_lab[(arr_anim[step_pos-1][0], arr_anim[step_pos-1][1])] = arr_anim[step_pos-1][2]
        plt.clf()
        nx.draw_networkx(G_anim, pos, with_labels=True, font_weight='bold', node_color=node_col_anim, edge_color=edge_col_anim, width=2)
        nx.draw_networkx_edge_labels(G_anim, pos, edge_labels=edge_lab)
    ##    nx.draw(G, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
    ##    plt.legend(labels=[str(v)], loc='best', fontsize=12, shadow=True, framealpha=1, facecolor='#08E8DE', edgecolor='#40E0D0', title=string_legend)

        plt.show(block=False)
        check_leftArrow = False
        #print("Right")

# Проверка данных в map_me
def valid_map_me(map_me, point_bfs):
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
    
    # Если больше всех данных вершин или меньше
    if point_bfs > len(map_me) or point_bfs < 1:
        if point_bfs == 2:
            tk.messagebox.showwarning(title='Оййй, не знал)', message=f'Обход со {point_bfs} вершины невозможен!')
        else:
            tk.messagebox.showwarning(title='Оййй, не знал)', message=f'Обход с {point_bfs} вершины невозможен!')
        return False

    # Если есть пустые строки
    for i in map_me:
        if len(map_me[i]) == 0:
            tk.messagebox.showwarning(title='Оййй, не знал)', message=f'Вершина {i} должна иметь хотябы одну смежную вершину!')
            return False
    try:
        #Массив с ходами обхода в ширину
        array = bfs(map_me, point_bfs)
    except:
        tk.messagebox.showwarning(title='Оййй, не знал)', message=f'В графе больше чем одна компонента связности!')
        return False

    # Если больше одной компоненты связности
    if len(array)+1 != len(map_me):
        tk.messagebox.showwarning(title='Оййй, не знал)', message=f'В графе больше чем одна компонента связности!')
        return False
    return True

# Запуск первого задания
def task1_start():
    global map_me, point_bfs_anim, edge_col_anim, node_col_anim, G_anim, arr_anim, stop_animation, check_leftArrow
    
    # Начальная точка обхода графа в ширину
    point_bfs = int(node_number_button_bfs.get())
    point_bfs_anim = point_bfs

    stop_animation = False
    check_leftArrow = False

    # Проверка списка смежности на верные данные
    if not valid_map_me(map_me, point_bfs):
        return

    #Цвета ребер графа
    edge_col = new_edge_color(map_me)
    edge_col_anim = edge_col

    #Цвета вершин графа
    node_col = new_node_color(map_me)
    node_col_anim = node_col

    #Граф пользователя
    G = new_graph(map_me)
    G_anim = G

    #Массив с ходами обхода в ширину
    arr = bfs(map_me, point_bfs)
    arr_anim = arr

    #Изменяем цвет точки с которой начинали обход
    node_col = set_color_node(G, node_col, point_bfs, 'yellow')
    node_col_anim = node_col

    #Отображает пользователю обход графа в ширину
    animation_graph(G, node_col, edge_col, point_bfs, arr, 0)
    add_tool()
    

def clear_all():
    global clear_ss_ms_mi
    global entry_list
    global arr
    
    if clear_ss_ms_mi == 1:
        for i in range(len(entry_list)):
            entry_list[i].config({"background": 'White'})
            entry_list[i].delete(0, 'end')
    elif clear_ss_ms_mi == 2 and len(arr) != 0:
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                string = str(i) + '_' + str(j)
                canvas.itemconfigure(string, image=photo0)
                arr[i][j] = 0
    elif clear_ss_ms_mi == 3 and len(arr) != 0:
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                string = str(i) + '_' + str(j)
                canvas.itemconfigure(string, image=photo0)
                arr[i][j] = 0

# Начало mi
def valid_check_mi():
    global arr
    nd = int(node_number_button.get())
    ed = int(edge_number_button.get())
    if int(nd*(nd-1)/2) < ed:
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                string = str(i) + '_' + str(j)
                if arr[i][j] == 1:
                    canvas.itemconfigure(string, image=photo1_d)
                else:
                    canvas.itemconfigure(string, image=photo0_d)
        return
    for j in range(len(arr[0])):
        one = 0
        for i in range(len(arr)):
            if arr[i][j] == 1:
                one += 1
        if one == 2:
            for i in range(len(arr)):
                string = str(i) + '_' + str(j)
                if arr[i][j] == 1:
                    canvas.itemconfigure(string, image=photo1_g)
                else:
                    canvas.itemconfigure(string, image=photo0_g)
        elif one == 0:
            for i in range(len(arr)):
                string = str(i) + '_' + str(j)
                if arr[i][j] == 1:
                    canvas.itemconfigure(string, image=photo1)
                else:
                    canvas.itemconfigure(string, image=photo0)
        else:
            for i in range(len(arr)):
                string = str(i) + '_' + str(j)
                if arr[i][j] == 1:
                    canvas.itemconfigure(string, image=photo1_d)
                else:
                    canvas.itemconfigure(string, image=photo0_d)
        
def check_next_mi(cord_i, cord_j):
    global arr

    tmp_i = int(node_number_button.get())
    tmp_j = int(edge_number_button.get())
    if int(tmp_i*(tmp_i-1)/2) < tmp_j:
        return False
    if tmp_i >= cord_i and tmp_j >= cord_j and cord_i >= 0 and cord_j >= 0:
        if arr[cord_i][cord_j] == 1:
            return True
        for j in range(len(arr[cord_i])):
            if arr[cord_i][j] == 1:
                for i in range(len(arr)):
                    if arr[i][j] == 1 and arr[i][cord_j] == 1:
                        return False
        return True
    return False

def click_mi(event):
    global arr
    cord_j = str(int((event.x-45)/30))
    cord_i = str(int((event.y-45)/30))
    string = cord_i + "_" + cord_j
    if check_next_mi(int(cord_i), int(cord_j)):
        if arr[int(cord_i)][int(cord_j)] == 0:
            canvas.itemconfigure(string, image=photo1)
            arr[int(cord_i)][int(cord_j)] = 1
        else:
            canvas.itemconfigure(string, image=photo0)
            arr[int(cord_i)][int(cord_j)] = 0
    valid_check_mi()

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
    last_arr = arr
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
    for i in range(len(arr)):
        if len(last_arr) <= i:
            break
        for j in range(len(arr[i])):
            if len(last_arr[i]) <= j:
                break
            arr[i][j] = last_arr[i][j]
            string = str(i) + '_' + str(j)
            if arr[i][j] == 1:
                canvas.itemconfigure(string, image=photo1)
            else:
                canvas.itemconfigure(string, image=photo0)
    valid_check_mi()

def send_answer_mi():
    global map_me
    map_me = {}

    if len(arr) == 0:
        tk.messagebox.showwarning(title='Оййй, не знал)', message='Создайте матрицу инцидентности!')
        return map_me
    ## print(arr)
    
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
            ## print(f"ребро {edge+1} соединяет вершины {tmp_node}")
            nodes_list.append(tmp_node)
        elif not counter:
            pass
            ## print(f"ребро {edge+1} не соединяет вершины")
        else:
            pass
            ## print(f"WARNING! Ребро {edge+1} соединяет либо больше 2 вершин, либо 1")
        
    ## print(nodes_list)
    for pair in nodes_list:
        ## print(f"{pair[0]} с вершиной {pair[1]}")
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
    ## print(map_me)
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
    global label_v_bfs, label_v_bfs_win
    global node_number_button_bfs, node_number_button_bfs_win
    global entry_answer, label_v_bfs2, label_v_bfs2_win
    global clear_ss_ms_mi

    clear_ss_ms_mi = 1
    canvas.destroy()
    top_canvas.destroy()
    
    top_canvas = Canvas(width=900, height=70, bg='#fad7d4')
    top_canvas.pack()

    label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
    label_v_win = top_canvas.create_window(80, 20, window=label_v)

    label_v_bfs = Label(text='Начать обход с вершины', font=('Arial', 12, 'normal'))
    label_v_bfs_win = top_canvas.create_window(100, 55, window=label_v_bfs)

    node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_win = top_canvas.create_window(280, 20, window=node_number_button)
    node_number_button.current(0)

    entry_answer = Entry(width=30, font=('Arial', 12, 'normal'), justify='center')
    top_canvas.create_window(755, 55, window=entry_answer)

    node_number_button_bfs = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_bfs_win = top_canvas.create_window(280, 55, window=node_number_button_bfs)
    node_number_button_bfs.current(0)

    button_var_count = Button(text='Создать список смежности', font=('Arial', 12, 'normal'), command=create_entries_ss)
    button_var_count_win = top_canvas.create_window(500, 20, window=button_var_count)

    label_v_bfs2 = Label(text='Результат обхода в ширину', font=('Arial', 12, 'normal'))
    label_v_bfs2_win = top_canvas.create_window(498, 55, window=label_v_bfs2)

    save_entries_b = Button(text='Посмотреть обход графа', font=('Arial', 12, 'normal'), command=save_entries_ss)
    top_canvas.create_window(792, 20, window=save_entries_b)

##    save_entries_b2 = Button(text='print() с весом', font=('Arial', 12, 'normal'), command=save_entries_with_weight_ss)
##    top_canvas.create_window(830, 20, window=save_entries_b2)

    canvas = Canvas(width=900, height=700, bg='#e0defa')
    canvas.pack()
    clear_all()

def input_ms():
    global canvas, top_canvas
    global label_v
    global label_v_win, node_number_button
    global node_number_button_win, button_var_count
    global button_var_count_win, button_send
    global label_v_bfs, label_v_bfs_win
    global node_number_button_bfs, node_number_button_bfs_win
    global entry_answer, label_v_bfs2, label_v_bfs2_win
    global clear_ss_ms_mi

    clear_ss_ms_mi = 2
    canvas.destroy()
    top_canvas.destroy()
    
    top_canvas = Canvas(width=900, height=70, bg='#fad7d4')
    top_canvas.pack()

    label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
    label_v_win = top_canvas.create_window(80, 20, window=label_v)

    label_v_bfs = Label(text='Начать обход с вершины', font=('Arial', 12, 'normal'))
    label_v_bfs_win = top_canvas.create_window(100, 55, window=label_v_bfs)

    node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_win = top_canvas.create_window(280, 20, window=node_number_button)
    node_number_button.current(0)

    entry_answer = Entry(width=30, font=('Arial', 12, 'normal'), justify='center')
    top_canvas.create_window(755, 55, window=entry_answer)

    node_number_button_bfs = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_bfs_win = top_canvas.create_window(280, 55, window=node_number_button_bfs)
    node_number_button_bfs.current(0)

    button_var_count = Button(text='Создать матрицу смежности', font=('Arial', 12, 'normal'), command=create_matrix_ms)
    button_var_count_win = top_canvas.create_window(500, 20, window=button_var_count)

    label_v_bfs2 = Label(text='Результат обхода в ширину', font=('Arial', 12, 'normal'))
    label_v_bfs2_win = top_canvas.create_window(492, 55, window=label_v_bfs2)

    save_entries_b = Button(text='Посмотреть обход графа', font=('Arial', 12, 'normal'), command=send_answer_ms)
    top_canvas.create_window(792, 20, window=save_entries_b)

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
    global label_v_bfs, label_v_bfs_win
    global node_number_button_bfs, node_number_button_bfs_win
    global entry_answer, label_v_bfs2, label_v_bfs2_win
    global clear_ss_ms_mi

    clear_ss_ms_mi = 3
    canvas.destroy()
    top_canvas.destroy()
    
    top_canvas = Canvas(root, width=1100, height=70, bg='#fad7d4')
    top_canvas.pack()
    
    label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
    label_v_win = top_canvas.create_window(90, 20, window=label_v)

    label_v_bfs = Label(text='Начать с вершины', font=('Arial', 12, 'normal'))
    label_v_bfs_win = top_canvas.create_window(86, 55, window=label_v_bfs)

    node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_win = top_canvas.create_window(240, 20, window=node_number_button)
    node_number_button.current(0)

    entry_answer = Entry(width=59, font=('Arial', 12, 'normal'), justify='center')
    top_canvas.create_window(821, 55, window=entry_answer)

    node_number_button_bfs = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
    node_number_button_bfs_win = top_canvas.create_window(240, 55, window=node_number_button_bfs)
    node_number_button_bfs.current(0)

    label_v_bfs2 = Label(text='Результат обхода в ширину', font=('Arial', 12, 'normal'))
    label_v_bfs2_win = top_canvas.create_window(423, 55, window=label_v_bfs2)

    label_r = Label(text='Количество ребер', font=('Arial', 12, 'normal'))
    label_r_win = top_canvas.create_window(390, 20, window=label_r)

    edge_number_button = ttk.Combobox(values=[i for i in range(1, 36)], font=('Arial', 12, 'normal'), width=10)
    edge_number_button_win = top_canvas.create_window(540, 20, window=edge_number_button)
    edge_number_button.current(0)


    button_var_count = Button(text='Создать матрицу инцидентности',  font=('Arial', 12, 'normal'), command=create_matrix_mi)
    button_var_count_win = top_canvas.create_window(745, 20, window=button_var_count)

    button_send = Button(text="Посмотреть обход графа", font=FONT, command=send_answer_mi)
    top_canvas.create_window(990, 20, window=button_send)

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
    last_arr = arr
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
    for i in range(len(arr)):
        if len(last_arr) <= i:
            break
        for j in range(len(arr[i])):
            if len(last_arr[i]) <= j:
                break
            arr[i][j] = last_arr[i][j]
            string = str(i) + '_' + str(j)
            if arr[i][j] == 1:
                canvas.itemconfigure(string, image=photo1)
            else:
                canvas.itemconfigure(string, image=photo0) 

def send_answer_ms():
    global arr, map_me
    map_me = {}
    for number_line in range(len(arr)):
        map_me[number_line+1] = []

        for digit in range(len(arr[number_line])):
            if arr[number_line][digit]:
                map_me[number_line+1].append(digit+1)
    ## print(map_me)
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
        entry = Entry(width=60, font=('Arial', 12, 'normal'), validate="focusout", validatecommand=valid_entry)
        entry.bind('<KeyPress>', key_entry)
        canvas.create_window(x+300, y, window=entry)

        entry_list.append(entry)

        y += 30
    for i in range(len(entry_list)):
        if len(last_entry_list) <= i:
            break
        entry_list[i].insert(0, last_entry_list[i])
    # В данной строке в зависимости от задачи нужно будет менять функцию валидации valid_entry и valid_entry_weight
    valid_entry()

def save_entries_ss():
    global map_me
    map_me = {}
    for i in range(len(entry_list)):
        map_me[i+1] = validate_string_ss(entry_list[i].get())
    
    ## print(map_me)
    task1_start()


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
    global map_me
    map_me = {}
    for i in range(len(entry_list)):
        if len(entry_list[i].get()) == 0:
            map_me[i+1] = []
        else:
            map_me[i+1] = validate_string_with_weight_ss(entry_list[i].get())
    
    ## print(map_me)


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
top_canvas = Canvas(root, width=800, height=70, bg='#fad7d4')
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
top_canvas = Canvas(width=900, height=70, bg='#fad7d4')
top_canvas.pack()

label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
label_v_win = top_canvas.create_window(80, 20, window=label_v)

label_v_bfs = Label(text='Начать обход с вершины', font=('Arial', 12, 'normal'))
label_v_bfs_win = top_canvas.create_window(100, 55, window=label_v_bfs)

node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
node_number_button_win = top_canvas.create_window(280, 20, window=node_number_button)
node_number_button.current(0)

entry_answer = Entry(width=30, font=('Arial', 12, 'normal'))
top_canvas.create_window(755, 55, window=entry_answer)

node_number_button_bfs = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
node_number_button_bfs_win = top_canvas.create_window(280, 55, window=node_number_button_bfs)
node_number_button_bfs.current(0)

button_var_count = Button(text='Создать список смежности', font=('Arial', 12, 'normal'), command=create_entries_ss)
button_var_count_win = top_canvas.create_window(500, 20, window=button_var_count)

label_v_bfs2 = Label(text='Результат обхода в ширину', font=('Arial', 12, 'normal'))
label_v_bfs2_win = top_canvas.create_window(500, 55, window=label_v_bfs2)

save_entries_b = Button(text='print() без веса', font=('Arial', 12, 'normal'), command=save_entries_ss)
top_canvas.create_window(830, 20, window=save_entries_b)



##save_entries_b2 = Button(text='print() с весом', font=('Arial', 12, 'normal'), command=save_entries_with_weight_ss)
##top_canvas.create_window(830, 20, window=save_entries_b2)

canvas = Canvas(width=900, height=700, bg='#e0defa')
canvas.pack()

canvas.destroy()
top_canvas.destroy()
# Конец ss

# Проверка для bfs
def check_check(check):
    for i in check:
        if i == 0:
            return True
    return False

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
                    check_v[i-1] = 1
            check_v[cell-1] = 1
        dq = new_dq
        step += 1
    set_ans = []
    for i in range(len(map_me)):
        tmp = []
        for j in range(len(map_me)):
            tmp.append(0)
        set_ans.append(tmp)
    ans2 = []
    for i in ans:
        if set_ans[i[0]-1][i[1]-1] == 0:
            ans2.append([i[0], i[1], i[2]])
            set_ans[i[0]-1][i[1]-1] = 1
            set_ans[i[1]-1][i[0]-1] = 1
    
    return ans2

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

def add_tool():
    fig = plt.gcf()
    fig.canvas.set_window_title('Graph')
    fig.set_size_inches(10, 6)
    tm = fig.canvas.manager.toolmanager
    try:
        tm.remove_tool('Play')
        tm.remove_tool('Pause')
        tm.remove_tool('Left')
        tm.remove_tool('Right')
    except:
        pass
    tm.add_tool("Play", PlayTool)
    tm.add_tool("Pause", PauseTool)
    tm.add_tool("Left", LeftArrowTool)
    tm.add_tool("Right", RightArrowTool)
    fig.canvas.manager.toolbar.add_tool(tm.get_tool("Play"), "toolgroup")
    fig.canvas.manager.toolbar.add_tool(tm.get_tool("Pause"), "toolgroup")
    fig.canvas.manager.toolbar.add_tool(tm.get_tool("Left"), "toolgroup")
    fig.canvas.manager.toolbar.add_tool(tm.get_tool("Right"), "toolgroup")

pos = dict()
stop_animation = False
step_pos = 1
# Отображение пользователю графика на экран
def animation_graph(G, node_col, edge_col, v, arr, step):
    global pos, stop_animation, step_pos, check_leftArrow
    if step == 0:
        step = 1
        pos=nx.spring_layout(G)
    if stop_animation:
        step_pos = step - 1
        if step_pos < 1:
            step_pos = 1
        return
    if len(arr)+1 == step:
        #Размер ребер
        edge_lab = nx.get_edge_attributes(G,'weight')
        check = 1
        for i in arr:
            edge_lab[(i[0], i[1])] = i[2]
        plt.clf()
        nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=2)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_lab)
        plt.show(block=False)
        string_ans = str(arr[0][0])
        for i in arr:
            string_ans += ', ' + str(i[1])
        entry_answer.delete(0, 'end')
        entry_answer.insert(0, string_ans)
        check_leftArrow = True
        stop_animation = True
        return
    #Размер ребер
    edge_lab = nx.get_edge_attributes(G,'weight')
    if arr[step-1][2] % 2 == 1:
        edge_col = set_color_edge(G, edge_col, arr[step-1], 'red')
    else:
        edge_col = set_color_edge(G, edge_col, arr[step-1], 'blue')
    edge_lab[(arr[step-1][0], arr[step-1][1])] = arr[step-1][2]
    plt.clf()
    step_pos = step
    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_lab)
##    nx.draw(G, with_labels=True, font_weight='bold', node_color=node_col, edge_color=edge_col, width=3)
##    plt.legend(labels=[str(v)], loc='best', fontsize=12, shadow=True, framealpha=1, facecolor='#08E8DE', edgecolor='#40E0D0', title=string_legend)
    plt.show(block=False)
    root.after(500, lambda: animation_graph(G, node_col, edge_col, v, arr, step+1))

draw_menu()

edge_col_anim = new_edge_color(map_me)
point_bfs_anim = 1
#Цвета вершин графа
node_col_anim = new_node_color(map_me)
#Граф пользователя
G_anim = new_graph(map_me)
#Массив с ходами обхода в глубину
arr_anim = bfs(map_me, point_bfs_anim)
#Изменяем цвет точки с которой начинали обход
node_col_anim = set_color_node(G_anim, node_col_anim, point_bfs_anim, 'yellow')

root.mainloop()
