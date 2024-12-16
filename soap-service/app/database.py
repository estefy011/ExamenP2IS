import sqlite3

def setup_database():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # Crear la tabla availability
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS availability (
        room_id INTEGER PRIMARY KEY,
        room_type TEXT NOT NULL,
        available_date DATE NOT NULL,
        status TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def populate_database():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # Insertar datos de prueba
    data = [
        (1, 'single', '2024-12-20', 'available'),
        (2, 'double', '2024-12-20', 'available'),
        (3, 'suite', '2024-12-21', 'available'),
        (4, 'single', '2024-12-21', 'maintenance')
    ]
    cursor.executemany("""
    INSERT INTO availability (room_id, room_type, available_date, status)
    VALUES (?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    populate_database()
    print("Base de datos configurada y llena con datos de prueba.")
