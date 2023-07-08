import serial
import time
import paho.mqtt.client as mqtt
import json

ACCESS_TOKEN = 'agjEHICsMbeG8PQRpC6U'
broker = 'thingsboard.cloud'  # Replace with your broker name
port = 1883  # Replace with your broker port
device_id = '732c3f80-ff11-11ed-b80e-4fb87ffd85da'  # Replace with your device ID

def on_connect(client, userdata, flags, rc):
    print("Connected to ThingsBoard with result code: " + str(rc))

def on_publish(client, userdata, mid):
    print("Data published to ThingsBoard with message id: " + str(mid))

# Serial Communication Configuration
z1baudrate = 9600
z1port = 'COM10'  # Set the correct port before running the code

z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2  # Set read timeout

# Main Loop - Read Serial Data and Publish to ThingsBoard
if z1serial.is_open:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.connect(broker, port, 60)

    while True:
        size = z1serial.in_waiting
        if size:
            data = z1serial.read(size)
            arr = data.splitlines()
            for i in range(len(arr)):
                telemetry_data = {
                    "data": arr[i].decode()  # Assuming the serial data is in ASCII format
                }
                payload = json.dumps(telemetry_data)
                topic = "v1/devices/{device_id}/telemetry".format(device_id=device_id)
                client.publish(topic, payload)

        time.sleep(1)

    client.disconnect()
    z1serial.close()
else:
    print('z1serial not open')
