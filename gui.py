import sqlite3
from tkinter import *
import tkintermapview
from tkinter import ttk

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
    
    print(f"\nЗ позиції: {selected_position}\nВикористана зброя: {selected_artillery}\nЗнищена позиція: {request3}, {request4}")

artillery_data = get_artillery_data()
artillery_names = [row[1] for row in artillery_data]

position_data = get_position_data()
position_names = [row[2] for row in position_data]

win = Tk()
win.title("Військова Операція")
win.geometry('1000x600')
win.resizable(False, False)
win.config(bg="#2F4F2F")  

map_widget = tkintermapview.TkinterMapView(win, width=800, height=500, corner_radius=0)
map_widget.set_position(48.59573572042534, 37.97750165860023)
map_widget.set_zoom(12)
map_widget.place(x=0, y=0)

bt = Button(text="Вогонь!", height=5, width=18, font=("Stencil", 12, "bold"), command=attack, bg="#556B2F", fg="white")
bt.place(x=805, y=50)

lbl1 = ttk.Label(text="Позиція", background="#2F4F2F", foreground="white", font=("Arial", 10, "bold"))
lbl2 = ttk.Label(text="Широта", background="#2F4F2F", foreground="white", font=("Arial", 10, "bold"))
lbl3 = ttk.Label(text="Довгота", background="#2F4F2F", foreground="white", font=("Arial", 10, "bold"))
lbl4 = ttk.Label(text="Зброя", background="#2F4F2F", foreground="white", font=("Arial", 10, "bold"))

lbl1.place(x=20, y=510)
lbl2.place(x=200, y=510)
lbl3.place(x=380, y=510)
lbl4.place(x=560, y=510)

combo1 = ttk.Combobox(win, values=position_names, font=("Arial", 10))
combo1.place(x=20, y=540)
entry1 = Entry(win, font=("Arial", 10))
entry1.place(x=200, y=540)
entry2 = Entry(win, font=("Arial", 10))
entry2.place(x=380, y=540)
combo4 = ttk.Combobox(win, values=artillery_names, font=("Arial", 10))
combo4.place(x=560, y=540)

win.mainloop()
