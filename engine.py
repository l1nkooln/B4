import sqlite3

#постріл
def attack():
    request1 = input('Введіть чим вєбати (номер):')
    request2 = input('Введіть снаряд яким вєбати:')
    request3 = input('Введіть широта куди потрібно вєбати:')
    request4 = input('Введіть довготу куди потрібно вєбати:')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

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
        return True
    else:
        print("Координати не знайдено в базі даних.")
        return False

    conn.close()


#вибір артилерії
def get_artillery_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Запитуємо дані з таблиці artillery
    cursor.execute("SELECT * FROM artillery") 
    rows = cursor.fetchall()

    # Виводимо отримані дані
    print("Виберіть опцію з наведеного списку:")
    for index, row in enumerate(rows):
        print(f"{index + 1}. {row[1]}")  # Виводимо дані, заміни row на потрібний формат

    # Запитуємо в користувача вибір
    try:
        choice = int(input("Введіть номер вибору: ")) - 1
        if 0 <= choice < len(rows):
            selected_data = rows[choice]
            print(f"Ви вибрали: {selected_data[1]}")
            save_user_choice(selected_data)
        else:
            print("Невірний вибір.")
    except ValueError:
        print("Будь ласка, введіть коректний номер.")
    
    conn.close()


#збереження вибору арт обстановки
def save_user_choice(choice_data):
    print("Ваш вибір збережено.")


get_artillery_data()
