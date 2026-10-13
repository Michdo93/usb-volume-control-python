# USB Volume Control (Python)

A simple, robust Python script to control system volume and media playback using a USB multimedia knob / audio system (`Vendor ID: e5b7`, `Product ID: 0811`). Tested on Linux (Ubuntu / OpenHAB server environments using PulseAudio or PipeWire).

## Features
- **Rotary Encoder:** Adjust system volume up/down smoothly.
- **Knob Press:** Toggle Mute / Unmute.
- **Media Keys:** Play/Pause, Next Track, Previous Track (via `playerctl`).
- **Clean Exit:** Graceful shutdown on `Ctrl+C` without blocking threads.

---

## Prerequisites & Installation

### 1. System Dependencies
Make sure Python 3, pip, and necessary system audio/HID tools are installed:

```bash
sudo apt update
sudo apt install python3-pip python3-hidapi playerctl
```

### 2. Python Libraries

Install the required Python package for audio management:

```bash
pip install pulsectl hidapi
```

---

## Hardware Setup & Permissions (Udev Rules)

To allow your user account to access the USB HID device without requiring `sudo`, you need to set up a udev rule.

1. Verify your device is detected using `lsusb`:
```bash
lsusb -d e5b7:0811
```

*(Expected output: `ID e5b7:0811 ZhenHuiDesignTechnology USB-AUDIO SYSTEM`)*
2. Create a new udev rule file:
```bash
sudo nano /etc/udev/rules.d/99-usb-volume.rules
```

3. Add the following lines to the file:
```text
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="e5b7", ATTRS{idProduct}=="0811", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="e5b7", ATTRS{idProduct}=="0811", MODE="0666"
```

4. Save and reload the udev rules, then unplug and re-plug your device:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

---

## Usage

Run the script directly from your terminal:

```bash
python3 volume_control.py
```

To run it as a background service or daemon on your server, you can wrap it inside a `systemd` service or use tools like `screen` / `tmux`.

---

# USB Volume Control (MQTT Edition)

A Python script that reads inputs from a USB multimedia knob / audio system (`Vendor ID: e5b7`, `Product ID: 0811`) and publishes corresponding commands via **MQTT**. Ideal for integrating hardware volume controllers and media keys into home automation systems like OpenHAB, Home Assistant, or Node-RED. Tested on Linux (Ubuntu / Debian server environments).

---

## Features
- **Rotary Encoder:** Publish volume adjustments (`INCREASE`, `DECREASE`).
- **Knob Press:** Toggle mute/unmute (`MUTE_UNMUTE`).
- **Media Keys:** Play/Pause, Next, and Previous track controls.
- **MQTT Integration:** Sends clean string payloads to a configurable MQTT topic.
- **Daemon-Ready:** Runs smoothly as a background service via systemd.

---

## Prerequisites & Installation

### 1. Install Mosquitto MQTT Broker
If you don't have an MQTT broker running on your server yet, install Mosquitto and its client tools:

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
```

Configure Mosquitto to allow local connections (if not already set up):

1. Create or open a custom config file:
```bash
sudo nano /etc/mosquitto/conf.d/local.conf
```

2. Add the following lines:
```text
listener 1883 0.0.0.0
allow_anonymous true
```

3. Restart and enable the Mosquitto service:
```bash
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto
```

### 2. Python Dependencies

Install the required Python packages for HID access and MQTT communication:

```bash
sudo apt install python3-pip python3-hidapi
pip install paho-mqtt hidapi
```

---

## Hardware Setup & Permissions (Udev Rules)

To allow your user account to access the USB HID device without requiring `sudo`:

1. Verify your device is detected using `lsusb`:
```bash
lsusb -d e5b7:0811
```

*(Expected output: `ID e5b7:0811 ZhenHuiDesignTechnology USB-AUDIO SYSTEM`)*
2. Create a new udev rule file:
```bash
sudo nano /etc/udev/rules.d/99-usb-volume.rules
```

3. Add the following rules:
```text
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="e5b7", ATTRS{idProduct}=="0811", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="e5b7", ATTRS{idProduct}=="0811", MODE="0666"
```

4. Reload udev rules and re-plug your device:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

---

## MQTT Topic & Payloads

The script publishes all commands to a single MQTT topic (default: `usbdevice/volume_controller/command`).

### Payload Reference Table

| Action / Hardware Event | MQTT Payload | Description |
| --- | --- | --- |
| **Clockwise Rotation (Turn Right)** | `INCREASE` | Triggered when turning the knob to increase volume. |
| **Counter-Clockwise (Turn Left)** | `DECREASE` | Triggered when turning the knob to decrease volume. |
| **Knob Press (Push Down)** | `MUTE_UNMUTE` | Toggles between mute and unmute states. |
| **Play / Pause Button** | `PLAY_PAUSE` | Toggles media playback state. |
| **Forward Button** | `NEXT` | Skips to the next media track. |
| **Rewind Button** | `PREVIOUS` | Goes back to the previous media track. |

You can test if messages are publishing correctly in a separate terminal:

```bash
mosquitto_sub -h localhost -t "usbdevice/volume_controller/command"
```

---

## Running as a Systemd Service (Background Daemon)

To ensure `volume_control_mqtt.py` starts automatically on boot and keeps running in the background, set it up as a systemd service.

1. Create a new service file:
```bash
sudo nano /etc/systemd/system/usb-volume-mqtt.service
```

2. Paste the following configuration (adjust paths and usernames to match your system, e.g., user `ubuntu` and your script path `/home/ubuntu/usb-volume-control-python`):
```ini
[Unit]
Description=USB Volume Control MQTT Daemon
After=network.target mosquitto.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/usb-volume-control-python
ExecStart=/usr/bin/python3 /home/ubuntu/usb-volume-control-python/volume_control_mqtt.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Reload systemd, enable, and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable usb-volume-mqtt.service
sudo systemctl start usb-volume-mqtt.service
```

4. Check the status and logs of your service:
```bash
sudo systemctl status usb-volume-mqtt.service
journalctl -u usb-volume-mqtt.service -f
```
