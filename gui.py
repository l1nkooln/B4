
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
        
        self.artillery_data = self.db.fetch_all("SELECT * FROM artillery")
        self.position_data = self.db.fetch_all("SELECT * FROM units")
        self.targets_data = self.db.fetch_all('SELECT * FROM targets')
        
        self.artillery_names = [row[1] for row in self.artillery_data]
        self.position_names = [row[2] for row in self.position_data]
        self.targets_data = [row[1] for row in self.targets_data]
        # self.units_names = 
        
        self.create_widgets()

    def create_widgets(self):
        self.map_widget = tkintermapview.TkinterMapView(self.root, width=1920, height=580, corner_radius=0)
        self.map_widget.set_position(48.5957, 37.9775)
        self.map_widget.set_zoom(12)
        self.map_widget.set_marker(48.60273, 37.938007, text='Піхота укрита Т-101')
        self.map_widget.set_marker(48.605858, 37.917671, text='Піхота укрита Т-102')
        self.map_widget.set_marker(48.594317, 37.914648, text='Піхота Т-103')
        self.map_widget.set_marker(48.568261, 37.88323, text='Піхота укрита Т-104')
        self.map_widget.set_marker(48.580133, 37.897703, text='Піхота укрита Т-105')
        self.map_widget.set_marker(48.532218, 37.900205, text='Піхота укрита Т-106')
        self.map_widget.set_marker(48.557198, 37.903422, text='Піхота укрита Т-107')
        self.map_widget.set_marker(48.588623, 37.966295, text='ксп укрите Т-201')
        self.map_widget.set_marker(48.576391, 37.909502, text='міномет укритий Т-202')
        self.map_widget.set_marker(48.565392, 37.915432, text='міномет укритий Т-203')
        self.map_widget.set_marker(48.570083, 37.908243, text='міномет Т-204')
        self.map_widget.set_marker(48.573059, 37.960736, text='гаубиця укрита Т-301')
        self.map_widget.set_marker(48.596196, 37.949817, text='гаубиця укрита Т-302')
        self.map_widget.set_marker(48.608206, 37.949736, text='гаубиця укрита Т-303')
        self.map_widget.set_marker(48.602496, 37.964798, text='гаубиця укрита Т-304')
        self.map_widget.set_marker(48.597342, 37.987914, text='логістичний центр Т-401')
        self.map_widget.set_marker(48.588868, 38.00686, text='логістичний центр Т-402')
        self.map_widget.set_marker(48.595533, 38.035939, text='склад боєприпасів Т-403')
        self.map_widget.set_marker(48.602527, 38.004359, text='склад боєприпасів Т-404')
        self.map_widget.set_marker(48.571236, 38.012168, text='склад боєприпасів Т-405')
        self.map_widget.place(x=0, y=0)
        self.map_widget.bind("<Button-1>", self.on_map_click)

        self.lbl1 = Label(self.root, text='Підрозділ', font=("Stencil", 12, "bold"), bg="#2F4F2F", fg='white')
        self.lbl5 = Label(self.root, text ='Позиція', font=("Stencil", 12, "bold"), bg="#2F4F2F", fg='white')
        self.lbl2 = Label(self.root, text='Ціль', font=("Stencil", 12, "bold"), bg="#2F4F2F", fg='white')
        self.lbl3 = Label(self.root, text='Боєприпас', font=("Stencil", 12, "bold"), bg="#2F4F2F", fg='white')
        self.lbl4 = Label(self.root, text='Кількість', font=("Stencil", 12, "bold"), bg="#2F4F2F", fg='white')
        
        self.lbl1.place(x=20, y=620)
        self.lbl5.place(x=20, y=695)
        self.lbl2.place(x=280, y=650)
        self.lbl3.place(x=540, y=650)
        self.lbl4.place(x=800, y=650)

        
        self.combo_position = ttk.Combobox(self.root, values=self.position_names, font=("Arial", 10))
        self.combo_position.place(x=20, y=650)
        
        self.combo_pos_guns = ttk.Combobox(self.root, font=("Arial", 10))
        self.combo_pos_guns.place(x=20, y=725)

        self.entry_lat = ttk.Combobox(self.root, values=self.targets_data)
        self.entry_lat.place(x=280, y=680)
        
        self.combo_artillery = ttk.Combobox(self.root, values=self.artillery_names, font=("Arial", 10))
        self.combo_artillery.place(x=540, y=680)
        self.combo_artillery.bind("<<ComboboxSelected>>", self.update_caliber)
        
        self.combo_artillery = Entry(self.root,font=("Arial", 10))
        self.combo_artillery.place(x=800, y=680)
        
        Button(self.root, text="В'їбать", height=5, width=18, font=("Stencil", 12, "bold"), command=self.attack, bg="#556B2F", fg="white").place(x=1200, y=610)
        self.btn_list = Button(self.root, text='Виконані завдання', font=("Stencil", 12, "bold"),bg="#556B2F", fg="white", width=18).place(x=1200, y=730)
    def on_map_click(self, event):
        lat, lon = self.map_widget.get_coordinates_from_event(event)
        self.entry_lat.delete(0, END)
        self.entry_lon.delete(0, END)
        self.entry_lat.insert(0, lat)
        self.entry_lon.insert(0, lon)
    
    def update_caliber(self, event):
        selected_artillery = self.combo_artillery.get()
        calibers = self.get_calibers_for_artillery(selected_artillery)
        self.combo_caliber.set('')
        self.combo_caliber['values'] = calibers
        if calibers:
            self.combo_caliber.current(0)
    
    def get_calibers_for_artillery(self, artillery_name):
        query = "SELECT ammo FROM artillery WHERE name = ?"
        calibers = self.db.fetch_all(query, (artillery_name,))
        return self.get_field1_from_caliber(calibers[0][0]) if calibers else []
    
    def get_field1_from_caliber(self, caliber):
        if not self.db.table_exists(caliber):
            print(f"Таблиця '{caliber}' не знайдена.")
            return []
        query = f"SELECT field1 FROM '{caliber}'"
        return [row[0] for row in self.db.fetch_all(query)]
    
    def attack(self):
        lat, lon = self.entry_lat.get().strip(), self.entry_lon.get().strip()
        position = self.combo_position.get().strip()
        artillery = self.combo_artillery.get().strip()
        
        if not lat or not lon or not position or not artillery:
            print("Некоректні дані")
            return
        
        query = "SELECT COUNT(*) FROM targets WHERE field3 = ? AND field4 = ?"
        result = self.db.fetch_all(query, (lat, lon))
        
        if result[0][0] > 0:
            print("Координати знайдено, ворога знищено")
            self.db.execute_query("UPDATE targets SET destroyed = TRUE WHERE field3 = ? AND field4 = ?", (lat, lon))
        else:
            print("Координати не знайдено в базі даних.")
        
        self.entry_lat.delete(0, END)
        self.entry_lon.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    app = MilitaryApp(root)
    root.mainloop()

