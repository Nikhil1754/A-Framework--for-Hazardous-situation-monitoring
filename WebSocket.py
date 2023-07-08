import asyncio
import json
import logging
import websockets
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Application Default credentials are automatically created.


logging.basicConfig(level=logging.INFO)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def func(altitude, pressure, smoke, sound, temperature):
    db = firestore.client()
    db.collection('sensors').document('1').update({
        'value': altitude
    })
    # db.collection('sensors').document('2').update({
    #     'value': humidity
    # })
    db.collection('sensors').document('3').update({
        'value': pressure
    })
    db.collection('sensors').document('4').update({
        'value': smoke
    })
    db.collection('sensors').document('5').update({
        'value': sound
    })
    db.collection('sensors').document('6').update({
        'value': temperature
    })


async def consumer_handler(websocket: websockets.WebSocketClientProtocol) -> None:
    async for message in websocket:
        log_message(message)


async def consume(connstring: str) -> None:
    obj = {
        "tsSubCmds": [
            {
                "entityType": "DEVICE",
                "entityId": "1b888590-2604-11ed-93a7-11fb8198d51b",
                "scope": "LATEST_TELEMETRY",
                "cmdId": 1
            }
        ],
        "historyCmds": [],
        "attrSubCmds": []
    }

    async with websockets.connect(connstring) as websocket:
        await websocket.send(json.dumps(obj))
        await websocket.recv()
        await consumer_handler(websocket)


def log_message(message: str) -> None:
    y = json.loads(message)
    data = y["data"]
    print(data)
    func(data['Altitude'][0][1], data['Pressure'][0][1], data['Smoke'][0][1],data['Sound'][0][1], data['Temperature'][0][1])


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZWFtMTBAaW5mb3N5cy5jb20iLCJ1c2VySWQiOiJlYmNmMmY0MC0yNjAxLTExZWQtOTNhNy0xMWZiODE5OGQ1MWIiLCJzY29wZXMiOlsiQ1VTVE9NRVJfVVNFUiJdLCJpc3MiOiJ0aGluZ3Nib2FyZC5pbyIsImlhdCI6MTY2MTc2MzcwNSwiZXhwIjoxNjYxNzcyNzA1LCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiMjExMGY1MzAtMjM4Ny0xMWVkLTkzYTctMTFmYjgxOThkNTFiIiwiY3VzdG9tZXJJZCI6Ijg3OGZhYTgwLTI0NGItMTFlZC05M2E3LTExZmI4MTk4ZDUxYiJ9.EN4djiMSYYVqLPV5-Y8mfk41FrFNm-q1I-NJ95oBIpIcRYQqAl9b47t5SYJA-JU66jKT9q_03kAwFs6UlEqjSg"
    # token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZWFtMTBAaW5mb3N5cy5jb20iLCJ1c2VySWQiOiJlYmNmMmY0MC0yNjAxLTExZWQtOTNhNy0xMWZiODE5OGQ1MWIiLCJzY29wZXMiOlsiQ1VTVE9NRVJfVVNFUiJdLCJpc3MiOiJ0aGluZ3Nib2FyZC5pbyIsImlhdCI6MTY2MTcwNjQ1MywiZXhwIjoxNjYxNzE1NDUzLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiMjExMGY1MzAtMjM4Ny0xMWVkLTkzYTctMTFmYjgxOThkNTFiIiwiY3VzdG9tZXJJZCI6Ijg3OGZhYTgwLTI0NGItMTFlZC05M2E3LTExZmI4MTk4ZDUxYiJ9.jPgxpbRxG5YevkDdx8-DrdGVGG5u__16GglaL85q47i9vJ4leU9O6QeAG3zVUyQ5L2hKVImoiZrcp9jBNl9DHA";
    connstring = "ws://thingsboard.surveymaster.in/api/ws/plugins/telemetry?token=" + token
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        consume(connstring)
    )
