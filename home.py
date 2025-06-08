home_state = {
    "lights": {
        "kitchen": {"on": False, "color": "white", "brightness": 100},
        "living room": {"on": False, "color": "white", "brightness": 100},
        "bathroom": {"on": False, "color": "white", "brightness": 100},
        "WC": {"on": False, "color": "white", "brightness": 100},
        "room1": {"on": False, "color": "white", "brightness": 100},
        "room2": {"on": False, "color": "white", "brightness": 100},
    },
    "cooling": {
        "kitchen": {"on": False, "temperature": 24},
        "living_room": {"on": False, "temperature": 24},
        "room1": {"on": False, "temperature": 24},
        "room2": {"on": False, "temperature": 24},
    },
    "heating": {
        "kitchen": {"on": False, "temperature": 24},
        "living_room": {"on": False, "temperature": 24},
        "room1": {"on": False, "temperature": 24},
        "room2": {"on": False, "temperature": 24},
    },
    "tv": {
        "living_room": {"on": False, "channel": 1},
    }
}


def turn_on(device, location):
    home_state[device][location]["on"] = True
    return f"{device} in {location} turned ON."


def turn_off(device, location):
    home_state[device][location]["on"] = False
    return f"{device} in {location} turned OFF."


def set_color_light(device, location, color):
    if home_state[device][location]["on"]:
        home_state[device][location]["color"] = color
        return f"{device} in {location} turned ON and color changed."
    return f"{device} in {location} turned OFF."


def set_brightness_light(device, location, brightness):
    if home_state[device][location]["on"]:
        home_state[device][location]["brightness"] = brightness
        return f"{device} in {location} turned ON and brightness changed."
    return f"{device} in {location} turned OFF."


def set_temperature_cool(device, location, temperature):
    if home_state[device][location]["on"]:
        home_state[device][location]["temperature"] = temperature
        return f"{device} in {location} turned ON and temperature changed."
    return f"{device} in {location} turned OFF."


def set_temperature_heat(device, location, temperature):
    if home_state[device][location]["on"]:
        home_state[device][location]["temperature"] = temperature
        return f"{device} in {location} turned ON and temperature changed."
    return f"{device} in {location} turned OFF."


def set_channel_tv(device, location, channel):
    if home_state[device][location]["on"]:
        home_state[device][location]["channel"] = channel
        return f"{device} in {location} turned ON and channel changed."
    return f"{device} in {location} turned OFF."
