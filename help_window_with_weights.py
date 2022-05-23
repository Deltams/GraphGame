# исправить: menu_bar.add_cascade(label='Справка', command=OPEN_CHILDROOT1) -> menu_bar.add_cascade(label='Справка', command=open_help_window)

def open_help_window():
    help_window = Toplevel(root)
    help_window.title('Справка')
    help_window.geometry('700x400+100+100')
    help_window.resizable(False, False)
    help_window.grab_set()

    ans = "\nВвод данных доступен списком смежности, матрицей смежности и матрицей инцидентности.\n"
    ans += 'Формат ввода можно выбрать в настройках.\n\n'

    ans += "В матрице смежности напишите в ячейке вес ребра.\n"
    ans += "В матрице инцидентности по горизонтали расположены ребра, по вертикали вершины.\n"
    ans += "Вес ребра в матрицах можно задать, установив число в поле ввода (работает автодополнение)\n"
    ans += "Вес ребра в списке смежности задается в формате Вершина::Вес, (Вершина, Вес), Вершина Вес\n"
    ans += "# 1: 2::3, 4 5, (5, 6), [7, 9]\n"
    ans += "Т.е. вершина 1 связана с вершиной 2 и вес ребра составляет 3;\n"
    ans += "связана с вершиной 4 и вес ребра 5;\n"
    ans += "связана с вершиной 5 и вес ребра 6;\n"
    ans += "связана с вершиной 7 и вес ребра 9.\n\n\n"

    ans += "С уважением, команда ЯРДИАР\n"
    ans += "Ярослав Верховых - github.com/vrkh\n"
    ans += "Дмитрий Шевчук - github.com/Deltams\n"
    ans += "Арсений Селицкий - vk.com/id175668822\n"
    label = Label(help_window, text=ans, font=('Times New Roman', 13, 'normal'), justify='left').pack()
