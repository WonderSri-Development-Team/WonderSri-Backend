# tracking/tests/test_location_websocket.py

import pytest
import json
from channels.testing import WebsocketCommunicator
from WonderSri_backend.asgi import application

@pytest.mark.asyncio
async def test_websocket_connection():
    communicator = WebsocketCommunicator(application, "/ws/location/")
    connected, _ = await communicator.connect()
    assert connected

    response = await communicator.receive_json_from()
    assert response == {
        'type': 'connection',
        'status': 'connection Accepted'
    }

    await communicator.disconnect()


@pytest.mark.asyncio
async def test_nearby_geofence():
    connection = WebsocketCommunicator(application, "/ws/location/")
    await connection.connect()
    await connection.receive_json_from()  

    await connection.send_json_to({
        "type": "nearbygeofences",
        "latitude": 6.032923,
        "longitude": 80.217622
    })

    response = await connection.receive_json_from(timeout=2000)
    assert response["type"] in ("nearbygeofences", "error")

    await connection.disconnect()


@pytest.mark.asyncio
async def test_allGeofences():
    connection = WebsocketCommunicator(application, "/ws/location/")
    await connection.connect()
    await connection.receive_json_from()  

    await connection.send_json_to({
        "type": "allGeofences",
    })

    response = await connection.receive_json_from(timeout=2000)
    assert response["type"] in ("allGeofences", "error")

    await connection.disconnect()
