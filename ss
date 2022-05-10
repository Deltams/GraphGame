from tkinter import *
from tkinter import ttk


root = Tk()
root.title('Список смежности')
root.geometry('900x700+200+100')
root.resizable(False, False)


entry_list = []
def create_entries():
    body_canvas.delete('all')
    entry_list.clear()

    x = 40
    y = 20

    for i in range(1, int(node_number_button.get())+1):
        label = Label(text=f'{i}.', font=('Arial', 12, 'normal'))
        body_canvas.create_window(x, y, window=label)

        entry = Entry(width=30, font=('Arial', 12, 'normal'))
        body_canvas.create_window(x+150, y, window=entry)

        entry_list.append(entry)

        y += 30


map_me = {}
def save_entries():
    for i in range(len(entry_list)):
        map_me[i+1] = validate_string(entry_list[i].get())
    
    print(map_me)


def validate_string(map_string):
    if ',' in map_string:
        res = map_string.split(',')
        res = [int(item.replace(' ', '')) for item in res]
    else:
        res = map_string.split(' ')
        res = [x for x in res if x]
        res = [int(item) for item in res]

    return res


def save_entries_with_weight():
    for i in range(len(entry_list)):
        map_me[i+1] = validate_string_with_weight(entry_list[i].get())
    
    print(map_me)


def validate_string_with_weight(map_string):
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
            ans.append([ch1, ch2])
    return ans


header_canvas = Canvas(width=900, height=50, bg='#fad7d4')
header_canvas.pack()

label_node = Label(text='Количество вершин', font=('Arial', 12, 'normal'))
header_canvas.create_window(80, 20, window=label_node)

node_number_button = ttk.Combobox(values=[i for i in range(1, 21)], font=('Arial', 12, 'normal'), width=10)
header_canvas.create_window(280, 20, window=node_number_button)
node_number_button.current(0)

button_var_count = Button(text='Создать список смежности', font=('Arial', 12, 'normal'), command=create_entries)
header_canvas.create_window(500, 20, window=button_var_count)

save_entries_b = Button(text='print() без веса', font=('Arial', 12, 'normal'), command=save_entries)
header_canvas.create_window(700, 20, window=save_entries_b)

save_entries_b2 = Button(text='print() с весом', font=('Arial', 12, 'normal'), command=save_entries_with_weight)
header_canvas.create_window(830, 20, window=save_entries_b2)


body_canvas = Canvas(width=900, height=700, bg='#e0defa')
body_canvas.pack()


root.mainloop()
