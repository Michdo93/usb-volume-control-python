rules.JSR223Rule({
    name: "USB Controller Sonos Control JS",
    description: "Handles USB knob events for Sonos items with received command",
    triggers: [
        triggers.ItemCommandTrigger("USB_Volume_Controller_Command")
    ],
    execute: (event) => {
        const cmd = event.itemCommand.toString();

        if (cmd === "INCREASE") {
            items.getItem("Sonos_Volume").sendCommand("INCREASE");
        } else if (cmd === "DECREASE") {
            items.getItem("Sonos_Volume").sendCommand("DECREASE");
        } else if (cmd === "MUTE_UNMUTE") {
            const muteItem = items.getItem("Sonos_Mute");
            muteItem.sendCommand(muteItem.state.toString() === "ON" ? "OFF" : "ON");
        } else if (cmd === "PLAY_PAUSE") {
            const stopItem = items.getItem("Sonos_Stop");
            stopItem.sendCommand(stopItem.state.toString() === "ON" ? "OFF" : "ON");
        } else if (cmd === "NEXT") {
            items.getItem("Sonos_Controller").sendCommand("NEXT");
        } else if (cmd === "PREVIOUS") {
            items.getItem("Sonos_Controller").sendCommand("PREVIOUS");
        }
    }
});
