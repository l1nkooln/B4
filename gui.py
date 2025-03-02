import sqlite3
from tkinter import *
import tkintermapview
from tkinter import ttk

# витяг з бд артилерій 
def get_artillery_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artillery")
    rows = cursor.fetchall()
    conn.close()
    return rows

# витягує з бд наші позиції
def get_position_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM units")
    rows = cursor.fetchall()
    conn.close()
    return rows

# удар
def attack():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    request3 = entry1.get().strip()
    request4 = entry2.get().strip()
    selected_position = combo1.get().strip()
    selected_artillery = combo4.get().strip()
    
    if not request3 or not request4 or not selected_position or not selected_artillery:
        print("Некоректні дані")
        return
    
    query = """
    SELECT COUNT(*) FROM targets WHERE field3 = ? AND field4 = ?
    """
    cursor.execute(query, (request3, request4))
    result = cursor.fetchone()

    if result[0] > 0:
        print("Координати знайдено, ворога знищено")
        query_update = """
        UPDATE targets SET destroyed = TRUE WHERE field3 = ? AND field4 = ?
        """
        
        cursor.execute(query_update, (request3, request4))
        conn.commit()
        entry1.delete(0, END)
        entry2.delete(0, END)
        return True
    else:
        print("Координати не знайдено в базі даних.")
        entry1.delete(0, END)
        entry2.delete(0, END)
        return False
    
    print(f"\nЗ позиції: {selected_position}\nВикористана зброя: {selected_artillery}\nЗнищена позиція: {request3}, {request4}")


# кординати на мапі вибір
def on_map_click(event):
    # Отримати координати, куди було натиснуто
    lat, lon = map_widget.get_coordinates_from_event(event)
    
    # Вставити координати в поля вводу
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry1.insert(0, lat)
    entry2.insert(0, lon)


# Оновлюємо комбобокс калібрів при виборі артилерії
def update_caliber(event):
    selected_artillery = combo4.get()
    calibers = get_calibers_for_artillery(selected_artillery)
    
    # Очищаємо і оновлюємо комбобокс калібрів
    combo_caliber.set('')
    combo_caliber['values'] = calibers
    if calibers:
        combo_caliber.current(0)  # Встановлюємо перший доступний калібр як вибраний


# Функція для отримання калібрів для вибраної артилерії
def get_calibers_for_artillery(artillery_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ammo FROM artillery WHERE name = ?", (artillery_name,))
    calibers = cursor.fetchone()
    conn.close()
    
    if calibers:
        return get_field1_from_caliber(calibers[0])  # Викликаємо функцію для отримання значень з таблиці за калібром
    return []


# Функція для перевірки, чи існує таблиця в базі
def table_exists(table_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


# Функція для отримання значень поля field1 з таблиці, що називається калібром
def get_field1_from_caliber(caliber):
    if not table_exists(caliber):  # Перевіряємо, чи існує таблиця
        print(f"Таблиця для калібру '{caliber}' не знайдена в базі даних.")
        return []
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT field1 FROM '{caliber}'")  # Виконуємо запит до таблиці, ім'я якої - калібр
    field1_values = cursor.fetchall()
    conn.close()
    
    # Повертаємо список значень field1
    return [field1[0] for field1 in field1_values]


artillery_data = get_artillery_data()
artillery_names = [row[1] for row in artillery_data]

position_data = get_position_data()
position_names = [row[2] for row in position_data]

win = Tk()
win.title("Військова Операція")
# win.state('zoomed')

width= win.winfo_screenwidth() 
height= win.winfo_screenheight()
win.geometry("%dx%d" % (width, height))
win.resizable(True, True)
win.config(bg="#2F4F2F")  

map_widget = tkintermapview.TkinterMapView(win, width=1920, height=580, corner_radius=0)
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

# Додаємо обробник для кліку на карті
map_widget.bind("<Button-1>", on_map_click)

bt = Button(text="Вогонь!", height=5, width=18, font=("Stencil", 12, "bold"), command=attack, bg="#556B2F", fg="white")
bt.place(x=1300, y=630)

lbl1 = ttk.Label(text="Позиція", background="#2F4F2F", foreground="white", font=("Arial", 20, "bold"))
lbl2 = ttk.Label(text="Широта", background="#2F4F2F", foreground="white", font=("Arial", 20, "bold"))
lbl3 = ttk.Label(text="Довгота", background="#2F4F2F", foreground="white", font=("Arial", 20, "bold"))
lbl4 = ttk.Label(text="Зброя", background="#2F4F2F", foreground="white", font=("Arial", 20, "bold"))
lbl5 = ttk.Label(text="Снаряд", background="#2F4F2F", foreground="white", font=("Arial", 20, "bold"))

lbl1.place(x=20, y=640)
lbl2.place(x=280, y=640)
lbl3.place(x=540, y=640)
lbl4.place(x=800, y=640)
lbl5.place(x=1060, y=640)

combo1 = ttk.Combobox(win, values=position_names, font=("Arial", 10))
combo1.place(x=20, y=680)
entry1 = Entry(win, font=("Arial", 10))
entry1.place(x=280, y=680)
entry2 = Entry(win, font=("Arial", 10))
entry2.place(x=540, y=680)

combo4 = ttk.Combobox(win, values=artillery_names, font=("Arial", 10))
combo4.place(x=800, y=680)
combo4.bind("<<ComboboxSelected>>", update_caliber)

combo_caliber = ttk.Combobox(win, font=("Arial", 10))
combo_caliber.place(x=1060, y=680)

win.mainloop()
