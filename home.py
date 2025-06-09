import json
import os
import requests
from datetime import datetime

STATE_FILE = "home_state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w") as f:
            json.dump(default_state(), f, indent=4)
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def default_state():
    return {
        "lights": {
            "kitchen": {"on": False, "color": "white", "brightness": 100},
            "living_room": {"on": False, "color": "white", "brightness": 100},
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
    state = load_state()
    if device in state and location in state[device]:
        state[device][location]["on"] = True
        save_state(state)
        return f"{device} in {location} turned ON."
    return "Invalid device or location."


def turn_off(device, location):
    state = load_state()
    if device in state and location in state[device]:
        state[device][location]["on"] = False
        save_state(state)
        return f"{device} in {location} turned OFF."
    return "Invalid device or location."


def set_color_light(device, location, color):
    state = load_state()
    if device in state and location in state[device]:
        if state[device][location]["on"]:
            state[device][location]["color"] = color
            save_state(state)
            return f"{device} in {location} set to color {color}"
        return f"{device} in {location} turned OFF."
    return "Invalid device or location."


def set_brightness_light(device, location, brightness):
    state = load_state()
    if device in state and location in state[device]:
        if state[device][location]["on"]:
            state[device][location]["brightness"] = brightness
            save_state(state)
            return f"{device} in {location} set to {brightness}% brightness"
        return f"{device} in {location} turned OFF."
    return "Invalid device or location."


def set_temperature(device_type, location, temperature):
    if 0 <= temperature <= 100:
        state = load_state()
        if device_type in state and location in state[device_type]:
            if state[device_type][location]["on"]:
                state[device_type][location]["temperature"] = temperature
                save_state(state)
                return f"{device_type} in {location} turned ON and temperature changed."
            return f"{device_type} in {location} turned OFF."
        return "Invalid device or location."
    return "Invalid temperature."


def set_channel_tv(device, location, channel):
    if 1 <= channel <= 9:
        state = load_state()
        if device in state and location in state[device]:
            if state[device][location]["on"]:
                state[device][location]["channel"] = channel
                save_state(state)
                return f"{device} in {location} turned ON and channel changed."
            return f"{device} in {location} turned OFF."
        return "Invalid device or location."
    return "Invalid channel number."


def get_status():
    state = load_state()
    status_lines = []

    status_lines.append("Lights:")
    for room, s in state["lights"].items():
        line = f"  - {room.capitalize()}: {'ON' if s['on'] else 'OFF'}, Color: {s['color']}, Brightness: {s['brightness']}%"
        status_lines.append(line)

    status_lines.append("\nCooling Systems:")
    for room, s in state["cooling"].items():
        line = f"  - {room.replace('_', ' ').capitalize()}: {'ON' if s['on'] else 'OFF'}, Temperature: {s['temperature']}°C"
        status_lines.append(line)

    status_lines.append("\nHeating Systems:")
    for room, s in state["heating"].items():
        line = f"  - {room.replace('_', ' ').capitalize()}: {'ON' if s['on'] else 'OFF'}, Temperature: {s['temperature']}°C"
        status_lines.append(line)

    status_lines.append("\nTVs:")
    for room, s in state["tv"].items():
        line = f"  - {room.replace('_', ' ').capitalize()}: {'ON' if s['on'] else 'OFF'}, Channel: {s['channel']}"
        status_lines.append(line)

    return "\n".join(status_lines)


def get_time():
    return datetime.now().strftime("%H:%M")


def get_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_weather():
    city_name = "Tehran"
    api_key = "0cd1d47284dc6ddbe045dde4908bae28"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=en"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"Weather in {city_name}: {data['weather'][0]['description']}, Temperature: {data['main']['temp']}°C"
    return "Error retrieving weather data"


def get_news():
    api_key = "eef5ed61874640ff8caa9a0bb4adf9eb"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == "ok":
            headlines = [article["title"] for article in data["articles"][:5]]
            return "\n".join([f"{i + 1}. {headline}" for i, headline in enumerate(headlines)])
        return "Error: Failed to fetch news."
    except Exception as e:
        return f"An error occurred: {e}"
