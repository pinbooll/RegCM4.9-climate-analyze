import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter import filedialog, Text
import sys
import export_mean_month
import time

def menu3(root):
    win = tk.Toplevel(root)
    win.title("Анализ данных климатического моделирования")
    win.geometry("800x600")
    win.resizable(False, False)
    title_font = tkfont.Font(size=20, weight="bold")
    button_font = tkfont.Font(size=14)
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('My.TButton', font=button_font, padding=[20, 10], background='#555555', foreground='white', borderwidth=0)
    style.map('My.TButton', background=[('active', '#666666')], relief=[('pressed', 'flat'), ('!pressed', 'flat')])
    bg_color = win.cget('bg')
    style.configure('My.TFrame', background=bg_color)

    # Кнопки управления
    top_frame = ttk.Frame(win, style='My.TFrame')
    top_frame.pack(side='top', fill='x')
    button1 = ttk.Button(top_frame, text="Назад", style='My.TButton', command=lambda: back_to_main(win, root))
    button1.pack(side='left', padx=5, pady=5)

    # Название метода
    title_label = tk.Label(win, text="Вывод распределения и анализ данных (1 месяц)", font=title_font, bg='#333333', fg='white')
    title_label.pack(pady=(10, 5))

    # Выбор файлов
    file_frame = ttk.Frame(win, style='My.TFrame')
    file_frame.pack(pady=(5, 5))
    file_entry = tk.Entry(file_frame, width=50)
    file_entry.insert(0, "Введите путь к файлу данных модели или выберите файл...")
    file_entry.bind("<FocusIn>", lambda args: file_entry.delete(0, 'end'))
    file_entry.pack(side='left', padx=5)
    file_button = ttk.Button(file_frame, text="Выбрать файл", style='My.TButton', command=lambda: select_file_netcdf(file_entry))
    file_button.pack(side='right', padx=5)

    folder_frame = ttk.Frame(win, style='My.TFrame')
    folder_frame.pack(pady=(5, 5))
    folder_entry = tk.Entry(folder_frame, width=50)
    folder_entry.insert(0, "Введите путь к папке для экспорта данных или выберите папку...")
    folder_entry.bind("<FocusIn>", lambda args: folder_entry.delete(0, 'end'))
    folder_entry.pack(side='left', padx=5)
    folder_button = ttk.Button(folder_frame, text="Выбрать папку", style='My.TButton', command=lambda: select_folder(folder_entry))
    folder_button.pack(side='right', padx=5)

    compare_file_frame = ttk.Frame(win, style='My.TFrame')
    compare_file_frame.pack(pady=(5, 5))
    compare_file_entry = tk.Entry(compare_file_frame, width=50)
    compare_file_entry.insert(0, "Введите путь к файлу для сравнения или выберите файл...")
    compare_file_entry.bind("<FocusIn>", lambda args: compare_file_entry.delete(0, 'end'))
    compare_file_entry.pack(side='left', padx=5)
    compare_file_button = ttk.Button(compare_file_frame, text="Выбрать файл", style='My.TButton', command=lambda: select_file_csv(compare_file_entry))
    compare_file_button.pack(side='right', padx=5)

    # Поля для параметров анализа
    param_frame = ttk.Frame(win, style='My.TFrame')
    param_frame.pack(side='left', anchor='n', fill='both', expand=True, padx=20, pady=5)

    # Радиус
    radius_label = tk.Label(param_frame, text="Радиус (1 = 10км)")
    radius_label.pack()
    radius_entry = tk.Entry(param_frame, width=20)
    radius_entry.pack()

    # Широта
    latitude_label = tk.Label(param_frame, text="Широта")
    latitude_label.pack()
    latitude_entry = tk.Entry(param_frame, width=20)
    latitude_entry.pack()

    # Долгота
    longitude_label = tk.Label(param_frame, text="Долгота")
    longitude_label.pack()
    longitude_entry = tk.Entry(param_frame, width=20)
    longitude_entry.pack()

    # Выбор переменных
    param_label = tk.Label(param_frame, text="Выберите параметры:")
    param_label.pack()
    param_listbox = tk.Listbox(param_frame, selectmode='multiple', width=25, height=5, exportselection=0)
    param_listbox.pack()

    parameters = {
        "Температура": "t",
        "Относительная влажность воздуха": "rh",
        "Давление": "ps"
    }

    for param in parameters:
        param_listbox.insert(tk.END, param)

    # Функция для получения выбранных элементов
    def get_selected_params():
        selected_indices = param_listbox.curselection()  # Получаем индексы выбранных элементов
        selected_params = [param_listbox.get(i) for i in selected_indices]  # Получаем значения по этим индексам
        # Преобразование выбранных параметров в метки
        selected_labels = [parameters[param] for param in selected_params if param in parameters]
        return selected_labels

    result_frame = ttk.Frame(win, style='My.TFrame')
    result_frame.pack(side='right', fill='both', expand=True, padx=20, pady=5)

    # Выбор методов анализа
    methods_label = tk.Label(result_frame, text="Выберите методы анализа:")
    methods_label.pack()
    methods_listbox = tk.Listbox(result_frame, selectmode='multiple', width=25, height=5, exportselection=0)
    methods_listbox.pack()

    methods = [
        "Корреляция",
        "Индекс согласия",
        "Среднеквадратическая ошибка"
    ]

    for method in methods:
        methods_listbox.insert(tk.END, method)

    # Функция для получения выбранных методов
    def get_selected_methods():
        selected_indices = methods_listbox.curselection()  # Получаем индексы выбранных элементов
        selected_params = [methods_listbox.get(i) for i in selected_indices]  # Получаем значения по этим индексам
        return selected_params
    
    # Текстовое поле для вывода результатов
    output_label = tk.Label(result_frame, text="Результат")
    output_label.pack()
    output_text = Text(result_frame, height=10, width=50)
    output_text.config(state='disabled')
    output_text.pack()
    
    # Перенаправить вывод из консоли в поле с результатом
    text_handler = TextHandler(output_text)
    sys.stdout = text_handler
    sys.stderr = text_handler

    # Разрешить копирование
    def copy_selection(event):
        selected_text = event.widget.selection_get()
        win.clipboard_clear()
        win.clipboard_append(selected_text)

    output_text.bind("<Control-c>", copy_selection)

    button2 = ttk.Button(top_frame, text="Выполнить", style='My.TButton', 
                         command=lambda: run_method(file_entry.get(), int(radius_entry.get()), get_selected_params(), 
                                                    float(latitude_entry.get()), float(longitude_entry.get()), folder_entry.get(),
                                                    get_selected_methods(), compare_file_entry.get()))
    button2.pack(side='right', padx=5, pady=5)

    win.mainloop()

def select_file_netcdf(entry_widget):
    filename = filedialog.askopenfilename(initialdir="/", title="Select file", 
                                          filetypes=(("NetCDF files", "*.nc"), ("All files", "*.*")))
    entry_widget.delete(0, tk.END)
    entry_widget.insert(tk.END, filename)

def select_file_csv(entry_widget):
    filename = filedialog.askopenfilename(initialdir="/", title="Select file", 
                                          filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    entry_widget.delete(0, tk.END)
    entry_widget.insert(tk.END, filename)

def select_folder(entry_widget):
    foldername = filedialog.askdirectory(initialdir="/", title="Select folder")
    entry_widget.delete(0, tk.END)
    entry_widget.insert(tk.END, foldername)

def back_to_main(win, root):
    win.destroy()
    root.deiconify()

class TextHandler(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state='normal')
        self.text_widget.insert('end', message)
        self.text_widget.yview('end')  # Автопрокрутка до последнего сообщения
        self.text_widget.config(state='disabled')

    def flush(self):
        pass

def run_method(dir_input, radius, var_list, lat, lon, dir_output, methods, dir_opendata):
    start_time = time.time()
    export_mean_month.output_main(var_list, methods, dir_input, dir_output, radius, lat, lon, dir_opendata)
    print("\nДействие выполнено успешно")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения: {execution_time} секунд")