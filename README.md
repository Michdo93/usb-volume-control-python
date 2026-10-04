# usb-volume-control-python

A Python script that reads input from USB volume controls and outputs the command to be executed to the command line. This code can be used later to map this control to other functions.

USB volume controls like these almost always register with the operating system as a standard USB keyboard or HID media device. When you turn or press the knob, the hardware simply sends standard key codes to the kernel (such as `KEY_VOLUMEUP`, `KEY_VOLUMEDOWN`, and `KEY_MUTE`).

To prevent Ubuntu or the Raspberry Pi OS from changing the system volume by default, you must intercept the input event using **`evdev`** in what’s known as **exclusive mode (`grab()`)**. As a result, Python receives the event and hides it from the rest of the operating system.

## Preparation / Installation

Install the `evdev` library for Python:

```bash
pip install evdev
```

*Note for Linux:* To allow your script to access the event devices (`/dev/input/event*`) without using `sudo`, your user must be a member of the `input` group:

```bash
sudo usermod -aG input $USER
```

*(Then log in again).*

---

## Python-Skript

Edit and save the `volume_control.py` file. Adjust the device name in the script if the system refers to it by a different name.

```
nano volume_control.py
```

After making important changes you can run it with:

```
python3 volume_control.py
```

---

## What the Code Does

1. **`device.grab()`**: This is the core element. It takes exclusive control of the USB button's event interface. Neither Pulseaudio/Pipewire nor the desktop manager (GNOME/KDE/Raspberry Pi Desktop) receives the event. The system volume remains unaffected.
2. **`device.read_loop()`**: Reads from the stream continuously.
3. **`ecodes.EV_KEY`**: Turning clockwise typically triggers `KEY_VOLUMEUP` in bursts, turning counterclockwise triggers `KEY_VOLUMEDOWN`, and pressing the button triggers `KEY_MUTE` (or, on some models, `KEY_MEDIA` / `KEY_PLAYPAUSE`).
