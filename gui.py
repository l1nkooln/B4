import sqlite3
from tkinter import *
import tkintermapview
from tkinter import ttk


class DatabaseManager:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    def execute_query(self, query, params=()):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def fetch_all(self, query, params=()):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def table_exists(self, table_name):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        return bool(self.fetch_all(query, (table_name,)))


class MilitaryApp:
    def __init__(self, root):
        self.db = DatabaseManager()
        self.root = root
        self.root.title("Військова Операція")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.config(bg="#2F4F2F")
        
        self.targets_data = self.db.fetch_all('SELECT * FROM targets')
        self.target_markers = {}  # Збереження міток для оновлення
        self.artillery_data = self.db.fetch_all("SELECT * FROM artillery")
        self.position_data = self.db.fetch_all("SELECT * FROM units")
        self.targets_data = self.db.fetch_all('SELECT * FROM targets')
        self.artillery_names = [row[1] for row in self.artillery_data]
        self.position_names = [row[2] for row in self.position_data]
        self.target_names = [row[1] for row in self.targets_data]  # Цілі
        
        self.create_widgets()
        self.load_position_units()

    def create_widgets(self):
        self.map_widget = tkintermapview.TkinterMapView(self.root, width=1920, height=580, corner_radius=0)
        self.map_widget.set_position(48.5957, 37.9775)
        self.map_widget.set_zoom(12)
        self.map_widget.place(x=0, y=0)
        
        self.load_targets()
        
        self.lbl1 = Label(self.root, text='Підрозділ', font=("Stencil", 12, "bold"), bg="#2F4F2F", fg='white')
        self.lbl5 = Label(self.root, text='Позиція', font=("Stencil", 12, "bold"), bg="#2F4F2F", fg='white')
        self.lbl2 = Label(self.root, text='Ціль', font=("Stencil", 12, "bold"), bg="#2F4F2F", fg='white')
        self.lbl3 = Label(self.root, text='Боєприпас', font=("Stencil", 12, "bold"), bg="#2F4F2F", fg='white')
        self.lbl4 = Label(self.root, text='Кількість', font=("Stencil", 12, "bold"), bg="#2F4F2F", fg='white')
        
        self.lbl1.place(x=20, y=620)
        self.lbl5.place(x=20, y=695)
        self.lbl2.place(x=280, y=650)
        self.lbl3.place(x=540, y=650)
        self.lbl4.place(x=800, y=650)

        # Комбобокси для вибору
        self.combo_position_unit = ttk.Combobox(self.root, font=("Arial", 10))
        self.combo_position_unit.place(x=20, y=650)
        self.combo_position_unit.bind("<<ComboboxSelected>>", self.update_position_options)

        self.combo_position = ttk.Combobox(self.root, font=("Arial", 10))
        self.combo_position.place(x=20, y=720)
        
        # self.combo_pos_guns = ttk.Combobox(self.root, font=("Arial", 10))
        # self.combo_pos_guns.place(x=20, y=725)

        self.entry_lat = ttk.Combobox(self.root, values=self.target_names)
        self.entry_lat.place(x=280, y=680)
        
        self.combo_artillery = ttk.Combobox(self.root, values=self.artillery_names, font=("Arial", 10))
        self.combo_artillery.place(x=540, y=680)
        self.combo_artillery.bind("<<ComboboxSelected>>", self.update_caliber)
        
        self.quantity = Entry(self.root)
        self.quantity.place(x=800, y=680)

        Button(self.root, text="Вогонь", height=5, width=18, font=("Stencil", 12, "bold"), command=self.attack, bg="#556B2F", fg="white").place(x=1200, y=590)
        self.btn_list = Button(self.root, text='Виконані завдання', font=("Stencil", 12, "bold"), bg="#556B2F", fg="white", width=18).place(x=1200, y=705)
        Button(self.root, text="Відновити цілі", font=("Stencil", 12, "bold"), width=18, command=self.restore_targets, bg="#556B2F", fg="white").place(x=1200, y=745)

    def load_position_units(self):
        # Завантажуємо унікальні підрозділи
        position_units = self.db.fetch_all("SELECT DISTINCT position_unit FROM position")
        self.position_units = [row[0] for row in position_units]
        self.combo_position_unit['values'] = self.position_units

    def update_position_options(self, event):
        selected_unit = self.combo_position_unit.get()
        positions_for_unit = self.db.fetch_all("SELECT name FROM position WHERE position_unit=?", (selected_unit,))
        position_names = [row[0] for row in positions_for_unit]
        self.combo_position['values'] = position_names
        if position_names:
            self.combo_position.current(0)

    def restore_targets(self):
        # Оновлення всіх цілей у базі даних
        self.db.execute_query("UPDATE targets SET destroyed = 0")
        
        # Видаляємо всі мітки з карти
        for _, marker in self.target_markers.values():
            self.map_widget.delete(marker)

        # Завантажуємо цілі заново
        self.targets_data = self.db.fetch_all('SELECT * FROM targets')
        self.load_targets()

        print("Усі цілі відновлено!")

    def load_targets(self):
        for row in self.targets_data:
            target_id, name, _, lat, lon, destroyed = row
            lat, lon = float(lat), float(lon)
            
            if destroyed:
                marker = self.map_widget.set_marker(lat, lon, text=f"{name} (destroyed)")
            else:
                marker = self.map_widget.set_marker(lat, lon, text=name)
            
            self.target_markers[name] = (target_id, marker)

    def update_caliber(self, event):
        selected_artillery = self.combo_artillery.get()
        calibers = self.get_calibers_for_artillery(selected_artillery)
        self.combo_caliber.set('')
        self.combo_caliber['values'] = calibers
        if calibers:
            self.combo_caliber.current(0)

    def attack(self):
        target_name = self.entry_lat.get().strip()

        if not target_name:
            print("Некоректні дані")
            return
        
        if target_name in self.target_markers:
            target_id, marker = self.target_markers[target_name]
            self.db.execute_query("UPDATE targets SET destroyed = 1 WHERE number = ?", (target_id,))
            
            lat, lon = marker.position
            self.map_widget.delete(marker)
            new_marker = self.map_widget.set_marker(lat, lon, text=f"{target_name} (destroyed)")
            self.target_markers[target_name] = (target_id, new_marker)
            print(f"Ціль {target_name} знищена.")
        else:
            print(f"Ціль {target_name} не знайдена в базі даних.")


if __name__ == "__main__":
    root = Tk()
    app = MilitaryApp(root)
    root.mainloop()
