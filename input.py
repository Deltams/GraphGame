import random
import tkinter as tk
import os

root = tk.Tk()
root.title('Ввод данных')
root.geometry('800x580+100+100')
root.resizable(False, False)

try:
    root.iconbitmap('icon.ico')
except:
    pass

entry_list = []

holst = tk.Canvas(width=800, height=580)
holst.pack()

zero = tk.StringVar(root, value='0')

def ptint_func():
    for entry in entry_list:
        print(entry.get())

def func():
    x = 0
    y = 0
    for i in range(10):
        x = 0
        for j in range(10):
            e1 = tk.Entry(holst, width=4, justify='center')
            e1.pack()
            entry_list.append(e1)
            holst.create_window(250+x,150+y,window=e1)
            x += 30
        y += 30

func()
root.bind('<Escape>', lambda e: ptint_func())
root.mainloop()
