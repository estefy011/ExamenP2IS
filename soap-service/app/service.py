from flask import Flask, request, render_template, jsonify
import sqlite3
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Ruta para la página principal
@app.route("/")
def home():
    return render_template("index.html")

# Ruta para manejar la consulta de disponibilidad desde la interfaz gráfica
@app.route("/check_availability", methods=["POST"])
def check_availability_ui():
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    room_type = request.form.get("room_type")

    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    query = """
    SELECT room_id FROM availability
    WHERE room_type = ? AND available_date BETWEEN ? AND ? AND status = 'available'
    """
    cursor.execute(query, (room_type, start_date, end_date))
    results = cursor.fetchall()
    conn.close()

    # Extraer los IDs de habitación
    rooms = [room[0] for room in results]
    return render_template("results.html", rooms=rooms)

# Ruta SOAP para manejar solicitudes directas (sin cambios)
@app.route('/soap/check_availability', methods=['POST'])
def check_availability_soap():
    try:
        xml_data = request.data
        tree = ET.fromstring(xml_data)
        start_date = tree.find('.//start_date').text
        end_date = tree.find('.//end_date').text
        room_type = tree.find('.//room_type').text
    except Exception as e:
        return f"Error al procesar el XML: {e}", 400

    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    query = """
    SELECT room_id FROM availability
    WHERE room_type = ? AND available_date BETWEEN ? AND ? AND status = 'available'
    """
    cursor.execute(query, (room_type, start_date, end_date))
    results = cursor.fetchall()
    conn.close()

    response = ET.Element("rooms")
    for room_id in results:
        room = ET.SubElement(response, "room")
        room.text = str(room_id[0])
    return ET.tostring(response), 200

@app.route('/availability/update', methods=['POST'])
def update_availability():
    data = request.get_json()
    room_id = data.get('room_id')
    room_type = data.get('room_type')
    status = data.get('status')

    if not all([room_id, room_type, status]):
        return jsonify({"error": "Missing fields"}), 400

    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    cursor.execute("SELECT room_id FROM availability WHERE room_id = ?", (room_id,))
    exists = cursor.fetchone()

    if exists:
        query = """
        UPDATE availability
        SET room_type = ?, status = ?
        WHERE room_id = ?
        """
        cursor.execute(query, (room_type, status, room_id))
    else:
        return jsonify({"error": "Room does not exist in availability"}), 404

    conn.commit()
    conn.close()
    return jsonify({"message": "Availability updated successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
