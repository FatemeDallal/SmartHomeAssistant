from collections import defaultdict

import matplotlib.colors as m_colors
from home import *
import re
from rapidfuzz import process

KEYWORDS = {
    "turn_on": [
        "turn on", "switch on", "power on", "activate", "start", "enable", "turn the .* on"
    ],
    "turn_off": [
        "turn off", "switch off", "off", "deactivate", "stop", "disable", "turn the .* off"
    ],
    "set_color": [
        "set color", "change color", "make it", "color to", "light color", "turn .* to .* color"
    ],
    "set_brightness": [
        "set brightness", "adjust brightness", "brightness to", "make it brighter", "make it dimmer",
        "increase brightness", "decrease brightness", "lower brightness", "raise brightness"
    ],
    "set_temperature": [
        "set temperature", "adjust temperature", "temperature to", "cool to", "heat to", "change temperature",
        "increase temperature", "decrease temperature"
    ],
    "set_channel": [
        "set channel", "change channel", "channel to", "switch to channel", "on channel", "go to channel"
    ],

    "lights": [
        "light", "lights", "lamp", "bulb", "ceiling light", "led"
    ],
    "cooling": [
        "cooling", "ac", "air conditioner", "air conditioning", "cooler"
    ],
    "heating": [
        "heating", "heater", "radiator", "warmer", "boiler"
    ],
    "tv": [
        "tv", "television", "smart tv", "screen", "the tv", "flat screen"
    ],

    "kitchen": ["kitchen"],
    "room1": ["room 1", "first room", "bedroom 1", "main bedroom"],
    "room2": ["room 2", "second room", "bedroom 2", "guest room"],
    "bathroom": ["bathroom", "restroom", "washroom", "toilet", "wc"],
    "living_room": ["living room", "hall", "main room", "lounge", "salon"],

    "get_time": [
        "what time", "current time", "tell me the time", "time is it", "what is the time", "do you know the time"
    ],
    "get_date": [
        "what date", "today's date", "current date", "tell me the date", "date is it", "which day is it"
    ],
    "get_weather": [
        "weather", "what's the weather", "how is the weather", "weather like", "forecast", "temperature outside"
    ],
    "get_news": [
        "news", "latest news", "what's in the news", "tell me the news", "headlines", "update me"
    ],
    "get_device_status": [
        "device status", "what is running", "what is on", "status of devices", "check devices", "check status",
        "is the .* on"
    ]
}


def map_keywords(text):
    mapped = defaultdict(list)
    for key, words in KEYWORDS.items():
        for w in words:
            if w in text:
                mapped[key].append(w)
    return mapped


def is_color(word):
    if word.lower() in m_colors.CSS4_COLORS:
        return True
    return False


def parse_command(correct_input):
    commands = re.split(r"\s+و\s+| and ", correct_input)
    instructions = list()
    for command in commands:
        device, location, action, value = None, None, None, None
        command = command.lower()
        mapped = map_keywords(command)

        if "lights" in mapped:
            device = "lights"
        elif "cooling" in mapped:
            device = "cooling"
        elif "heating" in mapped:
            device = "heating"
        elif "tv" in mapped or "set_channel" in mapped:
            device = "tv"
            location = "living_room"
        elif "time" in mapped:
            pass
        elif "date" in mapped:
            pass
        elif "weather" in mapped:
            pass
        elif "news" in mapped:
            pass
        elif "status" in mapped:
            pass

        for place in ["kitchen", "bathroom", "room1", "room2", "living_room", "WC"]:
            if place in mapped:
                location = place.replace(" ", "_")
                break

        if "turn_on" in mapped:
            action = "turn_on"
        elif "turn_off" in mapped:
            action = "turn_off"
        elif "set_color" in mapped:
            action = "set_color_light"
            words = command.split()
            for word in words:
                if is_color(word):
                    value = word
                    break
        elif "set_brightness" in mapped:
            action = "set_brightness_light"
            words = command.split()
            for word in words:
                if word.isdigit():
                    value = int(word)
                    break
        elif "set_cooling" in mapped:
            action = "set_temperature_cool"
            words = command.split()
            for word in words:
                if word.isdigit():
                    value = int(word)
                    break
        elif "set_heating" in mapped:
            action = "set_temperature_heat"
            words = command.split()
            for word in words:
                if word.isdigit():
                    value = int(word)
                    break
        elif "set_channel" in mapped:
            action = "set_channel_tv"
            value = command.split()[-1]

        instructions.append({"device": device, "location": location, "action": action, "value": value})

    return instructions


def execute_command(instructions):
    for instruction in instructions:
        try:
            if instruction["action"] == "turn_on" and instruction["device"] is not None:
                return turn_on(instruction["device"], instruction["location"])

            elif instruction["action"] == "turn_off" and instruction["device"] is not None:
                return turn_off(instruction["device"], instruction["location"])

            elif instruction["action"] == "set_color_light" and instruction["device"] is not None:
                return set_color_light(instruction["device"], instruction["location"], instruction["value"])

            elif instruction["action"] == "set_brightness_light" and instruction["device"] is not None:
                return set_brightness_light(instruction["device"], instruction["location"], instruction["value"])

            elif instruction["action"] == "set_temperature_cool" and instruction["device"] is not None:
                return set_temperature_cool(instruction["device"], instruction["location"], instruction["value"])

            elif instruction["action"] == "set_temperature_heat" and instruction["device"] is not None:
                return set_temperature_heat(instruction["device"], instruction["location"], instruction["value"])

            elif instruction["action"] == "set_channel_tv" and instruction["device"] is not None:
                return set_channel_tv(instruction["device"], instruction["location"], instruction["value"])

            elif instruction["action"] == "get_time" and instruction["device"] is not None:
                pass

            elif instruction["action"] == "get_date" and instruction["device"] is not None:
                pass

            elif instruction["action"] == "get_news" and instruction["device"] is not None:
                pass

            elif instruction["action"] == "get_status" and instruction["device"] is not None:
                pass

            elif instruction["action"] == "get_weather" and instruction["device"] is not None:
                pass

            return "Unknown command."
        except Exception as e:
            return f"Error while executing command: {e}"


def correct_spelling(sentences):
    all_keywords = set(word for words in KEYWORDS.values() for word in words)
    split_parts = re.split(r"\s+and\s+|\s+و\s+", sentences)

    corrected_sentences = []
    for part in split_parts:
        corrected_words = []
        for word in part.split():
            match, score, _ = process.extractOne(word, all_keywords)
            if score > 80:
                corrected_words.append(match)
            else:
                corrected_words.append(word)
        corrected_sentences.append(" ".join(corrected_words))

    return " and ".join(corrected_sentences)


def smart_home_agent(user_input):
    correct_input = correct_spelling(user_input)
    instructions = parse_command(correct_input)

    return execute_command(instructions)


while True:
    inp = input("Enter command: ")
    response = smart_home_agent(inp)

    print(response)
