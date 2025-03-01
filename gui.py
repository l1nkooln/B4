import sqlite3
from tkinter import *
import tkintermapview
from tkinter import ttk

# Функция для получения данных из базы
def get_artillery_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artillery")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Функция для сохранения выбора
def save_user_choice(choice_data):
    print(f"Ваш вибір збережено: {choice_data}")

# Функция обработки выбора из combo4
def on_artillery_select(event):
    selected_index = combo4.current()
    if selected_index >= 0:
        selected_artillery = artillery_data[selected_index]
        save_user_choice(selected_artillery)

# Получаем список вооружений из базы
artillery_data = get_artillery_data()
artillery_names = [row[1] for row in artillery_data]  # Извлекаем только названия

position = ['Туча', 'Сокіл', 'Заєць']
caliber = ['120 high-explosive fragmentation', '120 smoke', '120 light', '122 high-explosive fragmentation', '122 fire', '203 cumulative', '152 high-explosive fragmentation']

win = Tk()
win.title("В'їбаш по ворогу")
win.geometry('1000x600')
win.resizable(False, False)
win.config(bg="#335233")

map_widget = tkintermapview.TkinterMapView(win, width=800, height=500, corner_radius=0)
map_widget.set_position(48.59573572042534, 37.97750165860023)
map_widget.set_zoom(12)
map_widget.set_marker(48.594317, 37.914648, text='Піхота укрита')
map_widget.set_marker(48.605858, 37.917671, text='Піхота укрита')
map_widget.set_marker(48.594317, 37.914648, text='Піхота')
map_widget.set_marker(48.568261, 37.88323, text='Піхота укрита')
map_widget.set_marker(48.580133, 37.897703, text='Піхота укрита')
map_widget.set_marker(48.532218, 37.900205, text='Піхота укрита')
map_widget.set_marker(48.557198, 37.903422, text='Піхота укрита')
map_widget.set_marker(48.588623, 37.966295, text='ксп укрите')
map_widget.set_marker(48.576391, 37.909502, text='міномет укритий')
map_widget.set_marker(48.565392, 37.915432, text='міномет укритий')
map_widget.set_marker(48.570083, 37.908243, text='міномет')
map_widget.set_marker(48.573059, 37.960736, text='гаубиця укрита')
map_widget.set_marker(48.596196, 37.949817, text='гаубиця укрита')
map_widget.set_marker(48.608206, 37.949736, text='гаубиця укрита')
map_widget.set_marker(48.602496, 37.964798, text='гаубиця укрита')
map_widget.set_marker(48.597342, 37.987914, text='логістичний центр')
map_widget.set_marker(48.588868, 38.00686, text='логістичний центр')
map_widget.set_marker(48.595533, 38.035939, text='склад боєприпасів')
map_widget.set_marker(48.602527, 38.004359, text='склад боєприпасів')
map_widget.set_marker(48.571236, 38.012168, text='склад боєприпасів')
map_widget.place(x=0, y=0)

bt = Button(text="В'їбати", height=5, width=20, font=("Arial", 10, "bold"))
bt.place(x=817, y=50)

lbl1 = ttk.Label(text="Позиція")
lbl2 = ttk.Label(text="Широта")
lbl3 = ttk.Label(text="Довгота")
lbl4 = ttk.Label(text="Зброя")
lbl5 = ttk.Label(text="Снаряд")
lbl1.place(x=20, y=510)
lbl2.place(x=200, y=510)
lbl3.place(x=380, y=510)
lbl4.place(x=560, y=510)
lbl5.place(x=740, y=510)

combo1 = ttk.Combobox(win, values=position)
combo1.place(x=20, y=540)
combo2 = ttk.Combobox(win, values=["Енеїда", "Тарас Бульба", "Гайдамаки", "Собор"])
combo2.place(x=200, y=540)
combo3 = ttk.Combobox(win, values=["Енеїда", "Тарас Бульба", "Гайдамаки", "Собор"])
combo3.place(x=380, y=540)
combo4 = ttk.Combobox(win, values=artillery_names)
combo4.place(x=560, y=540)
combo4.bind("<<ComboboxSelected>>", on_artillery_select)  # Привязываем обработчик
combo5 = ttk.Combobox(win, values=caliber)
combo5.place(x=740, y=540)

win.mainloop()