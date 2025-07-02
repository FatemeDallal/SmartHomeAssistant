from collections import defaultdict

import matplotlib.colors as m_colors
from home import *
import re
from rapidfuzz import process

import json
import os

import whisper
import pyaudio
import wave
import tempfile
import os

model = whisper.load_model("base")

KEYWORDS_PATH = os.path.join(os.path.dirname(__file__), "keywords.json")

with open(KEYWORDS_PATH, "r", encoding="utf-8") as f:
    KEYWORDS = json.load(f)

places = ["kitchen", "bathroom", "room1", "room2", "living_room", "WC"]


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


def extract_number_and_unit(text):
    patterns = [
        r'\bto\s+(\d+)\s*(percent|degrees|%)?',
        r'\bby\s+(\d+)\s*(percent|degrees|%)?',
        r'\b(\d+)\s*(percent|degrees|%)?',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            number = int(match.group(1))
            unit = match.group(2) if match.group(2) else None
            return number, unit
    return None, None


def parse_command(correct_input):
    commands = re.split(r"\s+و\s+| and ", correct_input)
    instructions = list()
    for command in commands:
        device, location, action, value = None, "living_room", None, None
        command = command.lower()
        mapped = map_keywords(command)
        number, unit = extract_number_and_unit(command)

        if unit is None and "brightness" in command:
            unit = "%"
        elif unit is None and "temperature" in command:
            unit = "degrees"

        if "lights" in mapped:
            device = "lights"
        elif "set_temperature" in mapped:
            device = "temperature"
        elif "tv" in mapped or "set_channel" in mapped:
            device = "tv"
            if not location:
                location = "living_room"
        elif "get_time" in mapped:
            action = "get_time"
        elif "get_date" in mapped:
            action = "get_date"
        elif "get_weather" in mapped:
            action = "get_weather"
        elif "get_news" in mapped:
            action = "get_news"
        elif "get_status" in mapped:
            action = "get_status"

        for place in places:
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
        elif "set_brightness_light" in mapped or (unit and unit.lower() in ["percent", "%"]):
            action = "set_brightness_light"
            value = number
            if device is None:
                device = "lights"
        elif "set_temperature" in mapped or (unit and unit.lower() == "degrees"):
            action = "set_temperature"
            value = number
        elif "set_channel" in mapped:
            action = "set_channel_tv"
            value = number

        instructions.append({"device": device, "location": location, "action": action, "value": value})

    return instructions


def execute_command(instructions):
    responses = []
    for instruction in instructions:
        try:
            device = instruction["device"]
            location = instruction["location"]
            action = instruction["action"]
            value = instruction["value"]

            if action == "turn_on" and device is not None:
                responses.append(turn_on(device, location))

            elif action == "turn_off" and device is not None:
                responses.append(turn_off(device, location))

            elif action == "set_color_light" and device is not None and value:
                responses.append(str(turn_on(device, location) + " and " + set_color_light(device, location, value)))

            elif action == "set_brightness_light" and device is not None and value is not None:
                responses.append(str(turn_on(device, location) + " and " + set_brightness_light(device, location, value)))

            elif action == "set_temperature" and device == "temperature" and value is not None:
                responses.append(str(turn_on(device, location) + " and " + set_temperature(location, value)))

            elif action == "set_channel_tv" and device is not None and value is not None:
                responses.append(str(turn_on(device, location) + " and " + set_channel_tv(device, location, value)))

            elif action == "get_time":
                responses.append(get_time())

            elif action == "get_date":
                responses.append(get_date())

            elif action == "get_news":
                responses.append(get_news())

            elif action == "get_status":
                responses.append(get_status())

            elif action == "get_weather":
                responses.append(get_weather())

            else:
                responses.append("Unknown command.")

        except Exception as e:
            responses.append(f"Error while executing command: {e}")

    return responses



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


def get_output(responses):
    return "\n".join(responses)


def smart_home_agent(user_input):
    # correct_input = correct_spelling(user_input)
    instructions = parse_command(user_input)
    responses = execute_command(instructions)
    return get_output(responses)


if __name__ == '__main__':
    while True:
        inp = input("Enter command: ")
        response = smart_home_agent(inp)

        print(response)

