import hid
import paho.mqtt.client as mqtt
import time
import sys

# --- CONFIGURATION ---
VENDOR_ID = 0xe5b7
PRODUCT_ID = 0x0811

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "usbdevice/volume_controller/command"
MQTT_CLIENT_ID = "usb_volume_controller"

# Command mapping to MQTT Payloads
COMMAND_MAPPING = {
    1: "INCREASE",
    2: "DECREASE",
    4: "MUTE_UNMUTE",
    8: "PLAY_PAUSE",
    16: "NEXT",
    32: "PREVIOUS"
}

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker successfully!")
    else:
        print(f"Failed to connect, return code {rc}")

def main():
    # Initialize MQTT Client (using modern paho-mqtt callback API version 2)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=MQTT_CLIENT_ID)
    client.on_connect = on_connect

    try:
        print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return

    # Initialize USB HID Device
    devices = hid.enumerate(VENDOR_ID, PRODUCT_ID)
    if not devices:
        print("Device not found! Is it plugged in?")
        client.loop_stop()
        return

    h = hid.device()
    try:
        h.open_path(devices[0]['path'])
        # Non-blocking mode so Ctrl+C works instantly
        h.set_nonblocking(True)
    except Exception as e:
        print(f"Failed to open device path: {e}")
        client.loop_stop()
        return

    print("USB Volume MQTT Controller started. Listening for inputs (Press Ctrl+C to exit)...")

    try:
        while True:
            data = h.read(64)
            if not data:
                time.sleep(0.05) # Prevent high CPU usage
                continue
            
            cmd = data[0]
            if cmd == 0:
                continue

            if cmd in COMMAND_MAPPING:
                payload = COMMAND_MAPPING[cmd]
                print(f"Publishing MQTT -> Topic: {MQTT_TOPIC} | Payload: {payload}")
                client.publish(MQTT_TOPIC, payload)
            else:
                print(f"Unknown command received: {cmd}")

    except KeyboardInterrupt:
        print("\nProgram is shutting down...")
    finally:
        client.loop_stop()
        client.disconnect()
        h.close()
        print("Device closed safely. Goodbye!")

if __name__ == "__main__":
    main()
