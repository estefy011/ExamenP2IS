import sqlite3

def setup_database():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()

    # Crear la tabla reservations
    cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INTEGER PRIMARY KEY, -- Sin AUTOINCREMENT
    room_number INTEGER NOT NULL,
    customer_name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT NOT NULL
)
""")

    conn.commit()
    conn.close()
    print("Base de datos 'reservations.db' configurada correctamente.")

if __name__ == "__main__":
    setup_database()
