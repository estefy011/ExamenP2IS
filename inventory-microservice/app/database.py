import sqlite3

def setup_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Crear la tabla rooms
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_type TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    print("Base de datos 'inventory.db' configurada correctamente.")

if __name__ == "__main__":
    setup_database()
