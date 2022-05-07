from distutils.command.config import config
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk


FONT = ('Arial', 12, 'normal')

root = Tk()
root.title("Матрица смежности")
root.geometry("800x700+100+100")

arr = []

def check_next(cord_i, cord_j):
    tmp = int(node_number_button.get())
    if tmp >= cord_i and tmp >= cord_j and cord_i >= 0 and cord_j >= 0:
        return True
    return False

def click(event):
    global arr
    cord_j = str(int((event.x-94)/30))
    cord_i = str(int((event.y-25)/30))
    string = cord_i + "_" + cord_j
    string2 = cord_j + "_" + cord_i
    if check_next(int(cord_i), int(cord_j)):
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

def on_leave(event):
    print(event)
    
def create_matrix():
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
            canvas.tag_bind(string, '<Button-1>', click)
            #canvas.tag_bind(string, '<Button-1>', on_leave)
            tmp.append(0)
        arr.append(tmp)
        y += 30


top_canvas = Canvas(root, width=800, height=50, bg='red')
top_canvas.pack()

label_v = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
label_v_win = top_canvas.create_window(80, 20, window=label_v)


node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
node_number_button_win = top_canvas.create_window(280, 20, window=node_number_button)
node_number_button.current(0)

button_var_count = Button(text='Построить матрицу смежности', font=('Arial', 10, 'normal'), command=create_matrix)
button_var_count_win = top_canvas.create_window(500, 20, window=button_var_count)

canvas = Canvas(root, width=800, height=650, bg='blue')
canvas.pack()


photo0 = tk.PhotoImage(file="img/0.png")
photo1 = tk.PhotoImage(file="img/1.png")

photo0_h = tk.PhotoImage(file="img/0_h.png")
photo1_h = tk.PhotoImage(file="img/1_h.png")

root.mainloop()
