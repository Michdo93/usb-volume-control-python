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
