import sqlite3
from tkinter import *
import tkintermapview
from tkinter import ttk

# Функція для отримання даних з бази

def get_artillery_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artillery")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_position_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM units")
    rows = cursor.fetchall()
    conn.close()
    return rows


def attack():
    request3 = entry1.get().strip()
    request4 = entry2.get().strip()
    selected_position = combo1.get().strip()
    selected_artillery = combo4.get().strip()
    
    if not request3 or not request4 or not selected_position or not selected_artillery:
        print("Некоректні дані")
        return
    
    print(f"З позиції: {selected_position}\nВикористана зброя: {selected_artillery}\nЗнищена позиція: {request3}, {request4}")

# Отримуємо дані з бази
artillery_data = get_artillery_data()
artillery_names = [row[1] for row in artillery_data]

position_data = get_position_data()
position_names = [row[2] for row in position_data]

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

bt = Button(text="В'їбати", height=5, width=20, font=("Arial", 10, "bold"), command=attack)
bt.place(x=817, y=50)

lbl1 = ttk.Label(text="Позиція")
lbl2 = ttk.Label(text="Широта")
lbl3 = ttk.Label(text="Довгота")
lbl4 = ttk.Label(text="Зброя")
lbl1.place(x=20, y=510)
lbl2.place(x=200, y=510)
lbl3.place(x=380, y=510)
lbl4.place(x=560, y=510)

combo1 = ttk.Combobox(win, values=position_names)
combo1.place(x=20, y=540)
entry1 = Entry(win)
entry1.place(x=200, y=540)
entry2 = Entry(win)
entry2.place(x=380, y=540)
combo4 = ttk.Combobox(win, values=artillery_names)
combo4.place(x=560, y=540)

win.mainloop()
