import hid
import pulsectl
import subprocess
import shutil
import time
import sys

VENDOR_ID = 0xe5b7
PRODUCT_ID = 0x0811

def main():
    # Initialize PulseAudio / PipeWire control
    try:
        pulse = pulsectl.Pulse('usb-volume-control')
    except Exception as e:
        print(f"Error connecting to audio server: {e}")
        return
    
    devices = hid.enumerate(VENDOR_ID, PRODUCT_ID)
    if not devices:
        print("Device not found! Is it plugged in?")
        return

    h = hid.device()
    try:
        h.open_path(devices[0]['path'])
        # Set non-blocking mode so the script can exit cleanly on Ctrl+C
        h.set_nonblocking(True)
    except Exception as e:
        print(f"Failed to open device path: {e}")
        return

    print("USB Volume Control successfully started. Listening for inputs (Press Ctrl+C to exit)...")

    has_playerctl = shutil.which("playerctl") is not None
    if not has_playerctl:
        print("Notice: 'playerctl' not found. Media keys (Play/Next/Prev) will be ignored.")

    try:
        while True:
            data = h.read(64)
            if not data:
                time.sleep(0.05) # Prevent high CPU usage
                continue
            
            cmd = data[0]
            if cmd == 0:
                continue

            print(get_command_description(cmd))

            # --- Volume Up / Down (Rotary Encoder) ---
            if cmd == 1:  # Clockwise (+2%)
                for sink in pulse.sink_list():
                    pulse.volume_change_all_chans(sink, 0.02)
            elif cmd == 2:  # Counter-clockwise (-2%)
                for sink in pulse.sink_list():
                    pulse.volume_change_all_chans(sink, -0.02)

            # --- Mute / Unmute (Knob Press) ---
            elif cmd == 4:
                for sink in pulse.sink_list():
                    new_mute_state = 0 if sink.mute else 1
                    pulse.mute(sink, new_mute_state)

            # --- Media Keys ---
            elif has_playerctl:
                if cmd == 8:   # Play/Pause
                    subprocess.run(["playerctl", "play-pause"], stderr=subprocess.DEVNULL)
                elif cmd == 16:  # Forward
                    subprocess.run(["playerctl", "next"], stderr=subprocess.DEVNULL)
                elif cmd == 32:  # Rewind
                    subprocess.run(["playerctl", "previous"], stderr=subprocess.DEVNULL)

    except KeyboardInterrupt:
        print("\nProgram is shutting down...")
    finally:
        h.close()
        print("Device closed safely. Goodbye!")

def get_command_description(cmd):
    mapping = {
        1: "Action: Volume Up (+)",
        2: "Action: Volume Down (-)",
        4: "Action: Mute / Unmute",
        8: "Action: Play / Pause",
        16: "Action: Next Track",
        32: "Action: Previous Track"
    }
    return mapping.get(cmd, f"Unknown Command: {cmd}")

if __name__ == "__main__":
    main()
