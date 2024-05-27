from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from menu1 import menu1
from menu2 import menu2
from menu3 import menu3
from menu4 import menu4
from menu5 import menu5
#python3 -m PyInstaller --onefile main.py
#pyinstaller main.spec

def open_menu(menu_function_name):
    root.withdraw()
    menu = {
        'menu1': menu1,
        'menu2': menu2,
        'menu3': menu3,
        'menu4': menu4,
        'menu5': menu5
    }.get(menu_function_name)
    if menu:
        menu(root)

def main_menu():
    global root
    root = tk.Tk()
    root.title("Анализ данных климатического моделирования")
    root.geometry("800x600")
    root.resizable(False, False)
    title_font = tkfont.Font(size=20, weight="bold")
    button_font = tkfont.Font(size=14)

    title_label = tk.Label(root, text="Главное меню", font=title_font, bg='#333333', fg='white')
    title_label.pack(pady=(100, 20))

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('My.TButton', font=button_font, padding=[20, 10], background='#555555', foreground='white', borderwidth=0)
    style.map('My.TButton', background=[('active', '#666666')], relief=[('pressed', 'flat'), ('!pressed', 'flat')])

    button1 = ttk.Button(root, text="Вывод данных в определенный момент времени", style='My.TButton', command=lambda: open_menu('menu1'))
    button2 = ttk.Button(root, text="Вывод данных за промежуток времени", style='My.TButton', command=lambda: open_menu('menu2'))
    button3 = ttk.Button(root, text="Вывод распределения и анализ данных (1 месяц)", style='My.TButton', command=lambda: open_menu('menu3'))
    button4 = ttk.Button(root, text="Вывод распределения и анализ данных (несколько месяцев)", style='My.TButton', command=lambda: open_menu('menu4'))
    button5 = ttk.Button(root, text="Вывод распределения и анализ данных (год)", style='My.TButton', command=lambda: open_menu('menu5'))

    button1.pack(fill='x', padx=150, pady=10)
    button2.pack(fill='x', padx=150, pady=10)
    button3.pack(fill='x', padx=150, pady=10)
    button4.pack(fill='x', padx=150, pady=10)
    button5.pack(fill='x', padx=150, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_menu()