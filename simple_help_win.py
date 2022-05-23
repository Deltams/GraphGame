# menu_bar.add_cascade(label='Справка', command=open_help_window)

def open_help_window():
    help_window = Toplevel(root)
    help_window.title('Справка')
    help_window.geometry('750x300+100+100')
    help_window.resizable(False, False)
    help_window.grab_set()

    ans = "\nВвод данных доступен списком смежности, матрицей смежности и матрицей инцидентности.\n"
    ans += 'Формат ввода можно выбрать в настройках.\n\n'

    ans += "В матрице смежности нажмите на ячейку, чтобы соединить две вершины (работает автодополнение).\n"
    ans += "Если на пересечении вершин стоит 1 - ребро есть, если ноль - вершины не соединены.\n"
    ans += "В матрице инцидентности по горизонтали расположены ребра, по вертикали вершины.\n"
    ans += "Выберите две ячейки вершин на вертикали ребра и соедините их.\n\n"

    ans += "С уважением, команда ЯРДИАР\n"
    ans += "Ярослав Верховых - github.com/vrkh\n"
    ans += "Дмитрий Шевчук - github.com/Deltams\n"
    ans += "Арсений Селицкий - vk.com/id175668822\n"
    label = Label(help_window, text=ans, font=('Times New Roman', 13, 'normal'), justify='left').pack()
