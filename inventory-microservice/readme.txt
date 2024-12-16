# Inventory Microservice README

## Overview
This project implements an inventory microservice for managing hotel rooms. It supports registering new rooms, updating room status, and synchronizing with a SOAP service for availability updates.

## Features
- Register new hotel rooms with room type and status.
- Update room status and synchronize with the SOAP service.
- Provide API endpoints for external integrations.

## Requirements
- Python 3.x
- Flask
- SQLite
- Requests

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
### 1. Register Room
- **URL:** `/register`
- **Method:** POST
- **Request Format:** Form Data

#### Example Request
```bash
POST /register HTTP/1.1
Content-Type: application/x-www-form-urlencoded

room_type=double&status=available
```

#### Example Response
- Displays a success page with the room details.

### 2. Update Room Status
- **URL:** `/update`
- **Method:** POST
- **Request Format:** Form Data

#### Example Request
```bash
POST /update HTTP/1.1
Content-Type: application/x-www-form-urlencoded

room_id=1&new_status=occupied
```

#### Example Response
- Displays a success page with the updated room details.

### 3. Register Room (API)
- **URL:** `/rooms`
- **Method:** POST
- **Request Format:** JSON

#### Example Request
```json
{
    "room_type": "double",
    "status": "available"
}
```

#### Example Response
```json
{
    "room_id": 1,
    "room_type": "double",
    "status": "available"
}
```

### 4. Update Room Status (API)
- **URL:** `/rooms/<int:room_id>`
- **Method:** PATCH
- **Request Format:** JSON

#### Example Request
```json
{
    "status": "occupied"
}
```

#### Example Response
```json
{
    "message": "Room status updated successfully",
    "room_id": 1,
    "new_status": "occupied"
}
```

## SOAP Synchronization
This service automatically synchronizes room updates with the SOAP service. The SOAP endpoint URL is configured in the `notify_soap_service` function.

## Run the Server
To start the inventory microservice:
```bash
python inventory.py
```
The server will be available at `http://127.0.0.1:8002`.

## Testing
Use Postman or any other API testing tool to send requests to the endpoints. You can also use the provided web interface for managing rooms.
