# SOAP Service README

## Overview
This project implements a SOAP-based service for managing hotel room availability. It includes endpoints for checking room availability and updating availability information.

## Features
- Check room availability for specific dates and room types using SOAP.
- Update room availability for specific room IDs.
- Simple web interface for checking availability.

## Requirements
- Python 3.x
- Flask
- SQLite
- Requests
- XML handling libraries (default in Python)

## Setup
1. Clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install flask requests
   ```
4. Initialize the SQLite database:
   ```bash
   python setup_database.py
   ```

## Endpoints
### 1. Check Room Availability (SOAP)
- **URL:** `/soap/check_availability`
- **Method:** POST
- **Request Format:** XML
- **Response Format:** XML

#### Example Request
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header/>
    <soapenv:Body>
        <check_availability>
            <start_date>2024-12-20</start_date>
            <end_date>2024-12-22</end_date>
            <room_type>double</room_type>
        </check_availability>
    </soapenv:Body>
</soapenv:Envelope>
```

#### Example Response
```xml
<rooms>
    <room>1</room>
    <room>2</room>
</rooms>
```

### 2. Update Availability
- **URL:** `/availability/update`
- **Method:** POST
- **Request Format:** JSON

#### Example Request
```json
{
    "room_id": 1,
    "room_type": "double",
    "status": "available"
}
```

#### Example Response
```json
{
    "message": "Availability updated successfully"
}
```

## Run the Server
To start the SOAP service:
```bash
python service.py
```
The server will be available at `http://127.0.0.1:8000`.

## Testing
Use Postman or any other API testing tool to send requests to the endpoints. You can also test the functionality by using the provided web interface for checking availability.
