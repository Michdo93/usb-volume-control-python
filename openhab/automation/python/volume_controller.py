from openhab.triggers import when
from openhab.core import items, actions

@when("Item USB_Volume_Controller_Command received command")
def volume_controller_python(event):
    cmd = event.itemCommand.toString()
    
    vol_item = items.getItem("Sonos_Volume")
    mute_item = items.getItem("Sonos_Mute")
    stop_item = items.getItem("Sonos_Stop")
    
    if cmd == "INCREASE":
        vol_item.sendCommand("INCREASE")
    elif cmd == "DECREASE":
        vol_item.sendCommand("DECREASE")
    elif cmd == "MUTE_UNMUTE":
        if mute_item.state.toString() == "ON":
            mute_item.sendCommand("OFF")
        else:
            mute_item.sendCommand("ON")
    elif cmd == "PLAY_PAUSE":
        if stop_item.state.toString() == "ON":
            stop_item.sendCommand("OFF")
        else:
            stop_item.sendCommand("ON")
    elif cmd == "NEXT":
        items.getItem("Sonos_Controller").sendCommand("NEXT")
    elif cmd == "PREVIOUS":
        items.getItem("Sonos_Controller").sendCommand("PREVIOUS")
