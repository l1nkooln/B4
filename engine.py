import sqlite3

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
        print("Координати знайдено в базі даних.")
        return True
    else:
        print("Координати не знайдено в базі даних.")
        return False

    conn.close()

attack()

