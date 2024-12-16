from flask import Flask, request, render_template, jsonify
import sqlite3
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# Función para notificar al Servicio SOAP
def notify_soap_service(room_id, room_type, status):
    url = "http://127.0.0.1:8000/availability/update"  # Endpoint del servicio SOAP
    headers = {"Content-Type": "application/json"}
    data = {
        "room_id": room_id,
        "room_type": room_type,
        "status": status
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Error al notificar al servicio SOAP: {response.text}")
    else:
        print(f"Sincronización con Servicio SOAP exitosa para Room ID {room_id}.")

# Página principal con formularios


# Registrar nueva habitación desde la interfaz gráfica
@app.route("/register", methods=["POST"])
def register_room_ui():
    room_type = request.form.get("room_type")
    status = request.form.get("status", "available")

    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        query = """
        INSERT INTO rooms (room_type, status)
        VALUES (?, ?)
        """
        cursor.execute(query, (room_type, status))
        conn.commit()
        room_id = cursor.lastrowid
    finally:
        conn.close()

    # Notificar al servicio SOAP
    notify_soap_service(room_id, room_type, status)

    return render_template("room.html", room={"room_id": room_id, "room_type": room_type, "status": status})

# Actualizar estado de habitación desde la interfaz gráfica
@app.route("/update", methods=["POST"])
def update_room_ui():
    room_id = request.form.get("room_id")
    new_status = request.form.get("new_status")

    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        # Verifica si la habitación existe
        cursor.execute("SELECT room_type FROM rooms WHERE room_id = ?", (room_id,))
        room = cursor.fetchone()

        if not room:
            return render_template("room.html", room=None)

        # Actualiza el estado de la habitación
        query = """
        UPDATE rooms
        SET status = ?
        WHERE room_id = ?
        """
        cursor.execute(query, (new_status, room_id))
        conn.commit()
    finally:
        conn.close()

    # Notificar al servicio SOAP
    notify_soap_service(room_id, room[0], new_status)

    return render_template("room.html", room={"room_id": room_id, "status": new_status})

# API JSON para registrar habitación
@app.route('/rooms', methods=['POST'])
def register_room():
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be 'application/json'"}), 415

    data = request.get_json()
    room_type = data.get('room_type')
    status = data.get('status', 'available')

    if not room_type:
        return jsonify({"error": "Field 'room_type' is required"}), 400

    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        query = """
        INSERT INTO rooms (room_type, status)
        VALUES (?, ?)
        """
        cursor.execute(query, (room_type, status))
        conn.commit()
        room_id = cursor.lastrowid
    finally:
        conn.close()

    # Notificar al servicio SOAP
    notify_soap_service(room_id, room_type, status)

    return jsonify({"room_id": room_id, "room_type": room_type, "status": status}), 201

# API JSON para actualizar estado
@app.route('/rooms/<int:room_id>', methods=['PATCH'])
def update_room_status(room_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status:
        return jsonify({"error": "Field 'status' is required"}), 400

    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        cursor.execute("SELECT room_type FROM rooms WHERE room_id = ?", (room_id,))
        room_type = cursor.fetchone()

        if not room_type:
            return jsonify({"error": "Room not found"}), 404

        query = """
        UPDATE rooms
        SET status = ?
        WHERE room_id = ?
        """
        cursor.execute(query, (new_status, room_id))
        conn.commit()
    finally:
        conn.close()

    # Notificar al servicio SOAP
    notify_soap_service(room_id, room_type[0], new_status)

    return jsonify({"message": "Room status updated successfully", "room_id": room_id, "new_status": new_status}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8002)
