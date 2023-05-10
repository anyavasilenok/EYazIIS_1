import copy
from tkinter import Tk, Canvas, Text, Button, PhotoImage, Label, ttk, Scrollbar, filedialog, Toplevel
from PIL import ImageTk, Image
import natural_language_editor
import PyPDF2
import pickle


ASSETS_PATH = "pics"
PATH_FOR_SAVINGS = "dictionaries"
DICTIONARY = []


def relative_to_assets(path: str):
    return ASSETS_PATH + "\\" + path


# Функция для преобразования текста в словарь
def show_vocabulary():
    text = input_1.get(1.0, 'end').replace('\n', '')
    global DICTIONARY
    DICTIONARY = natural_language_editor.parser(text)
    fill_vocabulary(DICTIONARY)
    print(DICTIONARY)


# Функция для заполнения treeview из словаря(из текста/файла)
def fill_vocabulary(dictionary):
    rows = 0
    for lexeme in dictionary:
        for form in lexeme[1]['form']:
            word_form = form + ' ' + str(lexeme[1]['form'][form]['count']) + '\n'
            vocabulary.insert('', 'end', values=(word_form,
                                                 lexeme[0] + " " + str(lexeme[1]['count']),
                                                 lexeme[1]['form'][form]['tags']))
        rows += 1


# Очистка словаря
def clear_vocabulary():
    global rows
    rows = 0
    vocabulary.delete(*vocabulary.get_children())


# Функция для очистки treeview и textbox
def clear_everything():
    global rows
    rows = 0
    vocabulary.delete(*vocabulary.get_children())
    global DICTIONARY
    DICTIONARY = []
    input_1.delete('1.0', 'end')


# Создание словаря
def create_vocabulary():
    clear_vocabulary()
    show_vocabulary()


# Загрузка текста из pdf файла в textbox
def load_pdf():
    filepath = filedialog.askopenfilename()
    if filepath != "":
        if filepath[-4::] != '.pdf':
            print('это не pdf')
        else:
            with open(filepath, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                text = ''
                for i in range(num_pages):
                    page = reader.pages[i]
                    text += page.extract_text()

                lines = text.splitlines()
                text = ' '.join(lines)
                input_1.insert('1.0', text)


# Созранение словаря в формате pickle
def save_dictionary():
    global save_entry
    file_name = save_entry.get(1.0, 'end').replace('\n', '')
    filepath = PATH_FOR_SAVINGS + '\\' + file_name + '.pickle'
    with open(filepath, 'wb') as file:
        pickle.dump(DICTIONARY, file)


# Загрузка pickle словаря из файла
def load_dict_from_file():
    filepath = filedialog.askopenfilename()
    if filepath != "":
        if filepath[-7::] != '.pickle':
            print('это не pickle')
        else:
            with open(filepath, 'rb') as file:
                global DICTIONARY
                clear_vocabulary()
                DICTIONARY = pickle.load(file)
                fill_vocabulary(DICTIONARY)


# Окно добавления словоформы
def add_form_window():
    global is_pressed_first_form
    is_pressed_first_form = True
    global is_pressed_first_info
    is_pressed_first_info = True
    add_form_window = Toplevel(window)
    add_form_window.lift()
    add_form_window.geometry("440x301")
    add_form_window.configure(bg="#639EED")

    add_form_canvas = Canvas(
        add_form_window,
        bg="#639EED",
        height=301,
        width=440,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    add_form_canvas.place(x=0, y=0)
    add_form_canvas.create_rectangle(
        10.0,
        11.0,
        430.0,
        289.0,
        fill="#2969BE",
        outline="")

    add_form_canvas.create_text(
        172.0,
        51.0,
        anchor="nw",
        text="Добавить",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    # Текстбокс для ввода словоформы
    global add_form_entry
    add_form_entry = Text(
        add_form_window,
        bd=0,
        wrap="word",
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )

    add_form_entry.insert('1.0', "введите словоформу")
    add_form_entry.bind("<Button-1>", add_form_on_click)

    add_form_entry.place(
        x=72.0,
        y=99.0,
        width=296.0,
        height=35.0
    )

    # Текстбокс для ввода информации для словоформы
    global add_info_entry
    add_info_entry = Text(
        add_form_window,
        bd=0,
        wrap="word",
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )

    add_info_entry.insert('1.0', "введите информацию для словоформы")
    add_info_entry.bind("<Button-1>", add_info_on_click)

    add_info_entry.place(
        x=72.0,
        y=152.0,
        width=296.0,
        height=35.0
    )

    button_image_13 = PhotoImage(
        file=relative_to_assets("button_13.png"))
    button_13 = Button(
        add_form_window,
        image=button_image_13,
        borderwidth=0,
        highlightthickness=0,
        command=add_word_form,
        relief="flat"
    )
    button_13.place(
        x=72.0,
        y=216.0,
        width=296.0,
        height=39.0
    )
    add_form_window.resizable(False, False)
    add_form_window.mainloop()


# Функция добавления словоформы и морфологической информации
def add_word_form():
    global add_form_entry
    global add_info_entry
    global DICTIONARY
    word = add_form_entry.get('1.0', 'end').replace('\n', '')
    info = add_info_entry.get('1.0', 'end').replace('\n', '')
    if word != '' and info != '':
        clear_vocabulary()
        DICTIONARY = natural_language_editor.correct_dict(word, info, DICTIONARY)
        fill_vocabulary(DICTIONARY)
    else:
        print('Что-то пошло не так в функции add_word_form')


# Функция для удаления текста при нажатии на текстбокс (текстбокс для ввода словоформы)
def add_form_on_click(event):
    global add_form_entry
    global is_pressed_first_form
    if is_pressed_first_form is True:
        add_form_entry.delete("1.0", 'end')
        is_pressed_first_form = False
    else:
        pass


# Функция для удаления текста по нажатию на текстбокс (текстбокс для ввода информации для словоформы)
def add_info_on_click(event):
    global add_info_entry
    global is_pressed_first_info
    if is_pressed_first_info is True:
        add_info_entry.delete("1.0", "end")
        is_pressed_first_info = False
    else:
        pass


# Окно сохранения словаря
def save_dictionary_window():
    save_dictionary_window = Toplevel(window)
    save_dictionary_window.lift()
    save_dictionary_window.geometry("440x301")
    save_dictionary_window.configure(bg="#639EED")

    save_canvas = Canvas(
        save_dictionary_window,
        bg="#639EED",
        height=301,
        width=440,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    save_canvas.place(x=0, y=0)
    save_canvas.create_rectangle(
        10.0,
        11.0,
        430.0,
        289.0,
        fill="#2969BE",
        outline="")

    save_canvas.create_text(
        214.0,
        104.0,
        anchor="nw",
        text="\/",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    save_canvas.create_text(
        123.0,
        59.0,
        anchor="nw",
        text="Введите название файла",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    global save_entry
    save_entry = Text(
        save_dictionary_window,
        bd=0,
        wrap="word",
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    save_entry.place(
        x=72.0,
        y=143.0,
        width=296.0,
        height=33.0
    )

    save_canvas.create_text(
        217.0,
        98.0,
        anchor="nw",
        text="|",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    button_image_10 = PhotoImage(
        file=relative_to_assets("button_10.png"))
    button_10 = Button(
        save_dictionary_window,
        image=button_image_10,
        borderwidth=0,
        highlightthickness=0,
        command=save_dictionary,
        relief="flat"
    )
    button_10.place(
        x=72.0,
        y=204.0,
        width=296.0,
        height=39.0
    )
    save_dictionary_window.resizable(False, False)
    save_dictionary_window.mainloop()


# Функция фильтрации словаря
def filter_dictionary():
    global filter_entry
    global DICTIONARY
    text = filter_entry.get()
    clear_vocabulary()
    new_dictionary = []
    rows = 0
    for lexeme in DICTIONARY:
        for form in lexeme[1]['form']:
            data = lexeme[1]['form'][form]['tags']
            if ';' in data:
                substring = data[:data.index(';')]
                if text == substring:
                    new_dictionary.append(lexeme)
                    word_form = form + ' ' + str(lexeme[1]['form'][form]['count']) + '\n'
                    vocabulary.insert('', 'end', values=(word_form,
                                                         lexeme[0] + " " + str(lexeme[1]['count']),
                                                         lexeme[1]['form'][form]['tags']))
        rows += 1
    DICTIONARY = copy.deepcopy(new_dictionary)


# Окно фильтрации словаря
def filter_dictionary_window():
    filter_dictionary_window = Toplevel(window)
    filter_dictionary_window.lift()
    filter_dictionary_window.geometry("440x301")
    filter_dictionary_window.configure(bg="#639EED")

    filter_canvas = Canvas(
        filter_dictionary_window,
        bg="#639EED",
        height=301,
        width=440,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    filter_canvas.place(x=0, y=0)
    filter_canvas.create_rectangle(
        10.0,
        11.0,
        430.0,
        289.0,
        fill="#2969BE",
        outline="")

    filter_canvas.create_text(
        214.0,
        104.0,
        anchor="nw",
        text="\/",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    filter_canvas.create_text(
        172.0,
        63.0,
        anchor="nw",
        text="Фильтрация",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    options = [x for x in natural_language_editor.POS.values()]

    global filter_entry
    filter_entry = ttk.Combobox(
        filter_dictionary_window,
        values=options
    )
    filter_entry.place(
        x=72.0,
        y=143.0,
        width=296.0,
        height=33.0
    )

    filter_canvas.create_text(
        217.0,
        98.0,
        anchor="nw",
        text="|",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    button_image_12 = PhotoImage(
        file=relative_to_assets("button_12.png"))
    button_12 = Button(
        filter_dictionary_window,
        image=button_image_12,
        borderwidth=0,
        highlightthickness=0,
        command=filter_dictionary,
        relief="flat"
    )
    button_12.place(
        x=72.0,
        y=204.0,
        width=296.0,
        height=39.0
    )
    filter_dictionary_window.resizable(False, False)
    filter_dictionary_window.mainloop()


# Окно редактирования treeview
def edit_dictionary_window(data):
    edit_dictionary_window = Toplevel(window)
    edit_dictionary_window.lift()
    edit_dictionary_window.geometry("440x301")
    edit_dictionary_window.configure(bg="#639EED")

    edit_canvas = Canvas(
        edit_dictionary_window,
        bg="#639EED",
        height=301,
        width=440,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    edit_canvas.place(x=0, y=0)
    edit_canvas.create_rectangle(
        10.0,
        11.0,
        430.0,
        289.0,
        fill="#2969BE",
        outline="")

    edit_canvas.create_text(
        214.0,
        104.0,
        anchor="nw",
        text="\/",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    edit_canvas.create_text(
        152.0,
        59.0,
        anchor="nw",
        text="Измените строку",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    global edit_entry
    edit_entry = Text(
        edit_dictionary_window,
        bd=0,
        wrap="word",
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    edit_entry.place(
        x=72.0,
        y=143.0,
        width=296.0,
        height=33.0
    )

    edit_entry.insert('1.0', data)

    edit_canvas.create_text(
        217.0,
        98.0,
        anchor="nw",
        text="|",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    button_image_11 = PhotoImage(
        file=relative_to_assets("button_11.png"))
    button_11 = Button(
        edit_dictionary_window,
        image=button_image_11,
        borderwidth=0,
        highlightthickness=0,
        command=save_editing,
        relief="flat"
    )
    button_11.place(
        x=72.0,
        y=204.0,
        width=296.0,
        height=39.0
    )
    edit_dictionary_window.resizable(False, False)
    edit_dictionary_window.mainloop()


# Окно загрузки (пдф текста/словаря)
def load_window():
    load_window = Toplevel(window)
    load_window.lift()
    load_window.geometry("440x301")
    load_window.configure(bg="#639EED")

    load_canvas = Canvas(
        load_window,
        bg="#639EED",
        height=301,
        width=440,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    load_canvas.place(x=0, y=0)
    load_canvas.create_rectangle(
        10.0,
        11.0,
        430.0,
        289.0,
        fill="#2969BE",
        outline="")

    # Загрузить словарь из файла
    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    button_8 = Button(
        load_window,
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=load_dict_from_file,
        relief="flat"
    )
    button_8.place(
        x=85.0,
        y=110.0,
        width=261.0,
        height=55.0
    )

    load_canvas.create_text(
        159.0,
        59.0,
        anchor="nw",
        text="Окно загрузки",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    # Загрузить пдф
    button_image_9 = PhotoImage(
        file=relative_to_assets("button_9.png"))
    button_9 = Button(
        load_window,
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=load_pdf,
        relief="flat"
    )
    button_9.place(
        x=85.0,
        y=197.0,
        width=261.0,
        height=56.0
    )
    load_window.resizable(False, False)
    load_window.mainloop()


# Функция редактирования treeview
def edit_item(event):
    # Получить выделенную строку в Treeview
    selected_item = vocabulary.focus()

    # # Получить значения ячеек выбранной строки
    values = vocabulary.item(selected_item)['values']
    values = [i.replace('\n', '') for i in values]
    data = f'{values[0]} {values[1]} {values[2]}'
    edit_dictionary_window(data)


# Функция сохранения изменений в treeview
def save_editing():
    selected_item = vocabulary.focus()
    global edit_entry
    data = edit_entry.get(1.0, 'end').split()
    print(data)
    third_column = ''
    if len(data) >= 5:
        for i in data[4::]:
            third_column = third_column + i + ' '
        vocabulary.set(selected_item, 0, data[0] + ' ' + data[1])
        vocabulary.set(selected_item, 1, data[2] + ' ' + data[3])
        vocabulary.set(selected_item, 2, third_column)
    else:
        print("Некорректная информация, введите информацию для трёх столбцов")


window = Tk()


window.geometry("1200x700")

img = Image.open(r"D:\pythonProjects\EYazIIS_LR_1\design\build\assets\frame0\фон.png")
width = 1200
height = 700
imag = img.resize((width, height), Image.LANCZOS)
image = ImageTk.PhotoImage(imag)
panel = Label(window, image=image)
panel.pack(side="top", fill="both")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=700,
    width=1200,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

canvas.create_rectangle(
    57.0,
    0.0,
    1371.0,
    700.0,
    fill="#FFFFFF",
    outline="")

canvas.create_image(0, 0, anchor="nw", image=image)

canvas.create_rectangle(
    0.0,
    0.0,
    1200.0,
    53.0,
    fill="#2969BE",
    outline="")

# Кнопка сохранить
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=save_dictionary_window,
    relief="flat"
)

button_1.place(
    x=805.0,
    y=6.0,
    width=123.0,
    height=41.0
)

canvas.create_text(
    39.0,
    19.0,
    anchor="nw",
    text="Spacy",
    fill="#FFFFFF",
    font=("Inter", 14 * -1)
)

# Кнопка загрузить

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=load_window,
    relief="flat"
)
button_3.place(
    x=938.0,
    y=6.0,
    width=123.0,
    height=41.0
)

# Кнопка добавить
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))

button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=add_form_window,
    relief="flat"
)
button_4.place(
    x=539.0,
    y=7.0,
    width=123.0,
    height=41.0
)

# Кнопка очистить
button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))

button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=clear_everything,
    relief="flat"
)
button_5.place(
    x=672.0,
    y=6.0,
    width=123.0,
    height=41.0
)

# Кнопка фильтрация
button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))

button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=filter_dictionary_window,
    relief="flat"
)
button_6.place(
    x=1071.0,
    y=6.0,
    width=123.0,
    height=41.0
)

# Рамки текстбоксов
canvas.create_rectangle(
    81.0,
    110.0,
    491.0,
    540.0,
    fill="#177BAF",
    outline="")

canvas.create_rectangle(
    715.0,
    110.0,
    1125.0,
    540.0,
    fill="#177BAF",
    outline="")

# Ввод текста
input_1 = Text(
    bd=0,
    wrap="word",
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)

input_1.place(
    x=99.0,
    y=158.0,
    width=374.0,
    height=303.0
)

vocabulary = ttk.Treeview(
    columns=("Token", "Word form", "Info"),
    height=11,
    selectmode="browse"
)


# Привязка обработчика двойного щелчка мышью к объекту treeview
vocabulary.bind('<Double-1>', edit_item)

scrollX = Scrollbar(vocabulary, command=vocabulary.xview, orient='horizontal')
scrollX.pack(side='bottom', fill='x')
vocabulary.config(xscrollcommand=scrollX.set)
vocabulary.pack(side='left')

vocabulary.place(
    x=733.0,
    y=158.0,
    width=374.0,
    height=360.0
)

vocabulary.heading('Token', text="Форма", anchor='w')
vocabulary.heading('Word form', text="Лексема", anchor='w')
vocabulary.heading('Info', text="Информация", anchor='w')

vocabulary.column('#0', stretch=False, width=0)
vocabulary.column('#1', stretch=False, width=124)
vocabulary.column('#2', stretch=False, width=124)
vocabulary.column('#3', stretch=False, width=600)


canvas.create_text(
    161.0,
    126.0,
    anchor="nw",
    text="Ввод текста на естественном языке",
    fill="#FFFFFF",
    font=("Inter", 14 * -1)
)

canvas.create_text(
    802.0,
    126.0,
    anchor="nw",
    text="Словарь, составленный по тексту",
    fill="#FFFFFF",
    font=("Inter", 14 * -1)
)


# Составить словарь
button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))

button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=create_vocabulary,
    relief='flat'
)
button_7.place(
    x=99.0,
    y=479.0,
    width=369.0,
    height=41.0
)

window.resizable(False, False)
window.mainloop()
