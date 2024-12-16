import sqlite3

def sync_inventory_to_availability():
    # Conexión a las bases de datos
    inventory_conn = sqlite3.connect('inventory.db')
    hotel_conn = sqlite3.connect('hotel.db')

    inventory_cursor = inventory_conn.cursor()
    hotel_cursor = hotel_conn.cursor()

    # Obtener habitaciones del inventario
    inventory_cursor.execute("SELECT room_id, room_type, status FROM rooms")
    inventory_rooms = inventory_cursor.fetchall()

    # Borrar datos anteriores en disponibilidad (opcional, para simplificar sincronización)
    hotel_cursor.execute("DELETE FROM availability")

    # Insertar datos actualizados en la tabla availability
    for room in inventory_rooms:
        room_id, room_type, status = room
        # Suponiendo que la disponibilidad es para fechas predeterminadas
        available_date = '2024-12-20'  # Cambiar según lógica
        hotel_cursor.execute("""
            INSERT INTO availability (room_id, room_type, available_date, status)
            VALUES (?, ?, ?, ?)
        """, (room_id, room_type, available_date, status))

    # Guardar cambios y cerrar conexiones
    hotel_conn.commit()
    inventory_conn.close()
    hotel_conn.close()
    print("Sincronización completada.")

if __name__ == "__main__":
    sync_inventory_to_availability()
