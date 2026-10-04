import sys
from evdev import InputDevice, list_devices, ecodes

# Search term for the USB controller (name may vary, e.g., "USB Audio", "HID Control", "Acouto")
DEVICE_KEYWORD = "USB"

def find_knob_device():
    """Search for the appropriate HID input device."""
    devices = [InputDevice(path) for path in list_devices()]
    for dev in devices:
        # Search by input device name
        if DEVICE_KEYWORD.lower() in dev.name.lower():
            print(f"Device found: {dev.name} at {dev.path}")
            return dev
    return None

def main():
    device = find_knob_device()
    
    if not device:
        print("No matching device found. Available devices:")
        for path in list_devices():
            d = InputDevice(path)
            print(f" - {d.path}: {d.name}")
        sys.exit(1)

    # EXCLUSIVE MODE (GRAB):
    # Prevents the operating system from processing the event (no mute or volume drop in the system)
    try:
        device.grab()
        print(f"Successfully grabbed {device.name}. Mute/Volume events will be intercepted.\n")
    except IOError:
        print("Error occurred while grabbing the device. Do you have root/input permissions? (Use sudo)")
        sys.exit(1)

    try:
        for event in device.read_loop():
            # Evaluate only key events (EV_KEY) and only the initial press/rotation (value == 1 or 2 for Repeat)
            if event.type == ecodes.EV_KEY and event.value in (1, 2):
                
                if event.code == ecodes.KEY_VOLUMEUP:
                    handle_volume_up()
                elif event.code == ecodes.KEY_VOLUMEDOWN:
                    handle_volume_down()
                elif event.code in (ecodes.KEY_MUTE, ecodes.KEY_MIN_INTERESTING):
                    handle_mute()
                else:
                    print(f"Unexpected Keycode: {event.code}")

    except KeyboardInterrupt:
        print("\nEnding script...")
    finally:
        # Release the exclusive lock when exiting
        device.ungrab()

# -------------------------------------------------------------------
# Your Mapping Logic / Callbacks (as example openHAB REST commands)
# -------------------------------------------------------------------

def handle_volume_up():
    print("[Action] Volume turned up -> Send command to openHAB item")
    # to do: For example, requests.post(“http://openhab:8080/rest/items/MyVolumeItem”, data="INCREASE")

def handle_volume_down():
    print("[Action] Volume turned down -> Send command to openHAB item")
    # to do: For example, requests.post(“http://openhab:8080/rest/items/MyVolumeItem”, data="DECREASE")

def handle_mute():
    print("[Action] Mute/Play-Pause pressed -> Send command to openHAB item")
    # to do: For example, requests.post(“http://openhab:8080/rest/items/MyMuteItem”, data="TOGGLE")


if __name__ == "__main__":
    main()
