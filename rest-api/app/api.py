from flask import Flask, request, render_template, redirect, jsonify
import sqlite3
import requests

app = Flask(__name__)

def parse_soap_response(soap_response):
    """Procesa la respuesta SOAP para extraer habitaciones disponibles."""
    import xml.etree.ElementTree as ET
    try:
        tree = ET.fromstring(soap_response)
        rooms = [room.text for room in tree.findall(".//room")]
        return rooms
    except Exception as e:
        print(f"Error parsing SOAP Response: {e}")
        return []

@app.route("/")
def home():
    """Renderiza la página de inicio."""
    return render_template("index.html")

@app.route("/create", methods=["POST"])
def create_reservation_ui():
    reservation_id = request.form.get("reservation_id")
    customer_name = request.form.get("customer_name")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    room_type = request.form.get("room_type")

    # Validar que los datos estén completos
    if not all([reservation_id, customer_name, start_date, end_date, room_type]):
        return render_template("index.html", error="Todos los campos son obligatorios.")

    # Verificar si el ID ya existe
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations WHERE reservation_id = ?", (reservation_id,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return render_template("index.html", error="El ID de la reserva ya existe.")

    # Verificar disponibilidad llamando al Servicio SOAP
    soap_request = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Header/>
        <soapenv:Body>
            <check_availability>
                <start_date>{start_date}</start_date>
                <end_date>{end_date}</end_date>
                <room_type>{room_type}</room_type>
            </check_availability>
        </soapenv:Body>
    </soapenv:Envelope>
    """
    headers = {"Content-Type": "text/xml"}
    soap_response = requests.post("http://127.0.0.1:8000/soap/check_availability", data=soap_request, headers=headers)

    if soap_response.status_code != 200:
        return f"Error al verificar disponibilidad: {soap_response.text}", 500

    # Procesar la respuesta SOAP
    available_rooms = parse_soap_response(soap_response.text)
    if not available_rooms:
        conn.close()
        return render_template("index.html", error="No hay habitaciones disponibles para las fechas seleccionadas.")

    room_number = available_rooms[0]  # Selecciona la primera habitación disponible

    # Registrar la reserva en la base de datos
    query = """
    INSERT INTO reservations (reservation_id, room_number, customer_name, start_date, end_date, status)
    VALUES (?, ?, ?, ?, ?, 'confirmed')
    """
    cursor.execute(query, (reservation_id, room_number, customer_name, start_date, end_date))
    conn.commit()
    conn.close()

    # Mostrar mensaje de éxito
    return render_template("confirm.html", 
                           success="¡Reserva creada exitosamente!", 
                           reservation_id=reservation_id,
                           room_number=room_number, 
                           customer_name=customer_name, 
                           start_date=start_date, 
                           end_date=end_date)

@app.route("/reservations", methods=["GET"])
def get_reservation_ui():
    reservation_id = request.args.get("reservation_id")
    if not reservation_id:
        return render_template("index.html", error="Debe proporcionar un ID de reserva.")

    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    query = "SELECT * FROM reservations WHERE reservation_id = ?"
    cursor.execute(query, (reservation_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return render_template("reservation_details.html", reservation={
            "reservation_id": result[0],
            "room_number": result[1],
            "customer_name": result[2],
            "start_date": result[3],
            "end_date": result[4],
            "status": result[5]
        })
    else:
        return render_template("index.html", error="Reserva no encontrada.")
    
@app.route("/reservations/cancel", methods=["POST"])
def cancel_reservation_ui():
    """Cancela una reserva específica desde la interfaz."""
    reservation_id = request.form.get("reservation_id")
    if not reservation_id:
        return render_template("index.html", error="Debe proporcionar un ID de reserva para cancelar.")

    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    query = "DELETE FROM reservations WHERE reservation_id = ?"
    cursor.execute(query, (reservation_id,))
    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()

    if rows_deleted > 0:
        return render_template("index.html", success="Reserva cancelada exitosamente.")
    else:
        return render_template("index.html", error="Reserva no encontrada.")  

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8001)
