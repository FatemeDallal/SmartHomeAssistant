from collections import defaultdict

import matplotlib.colors as m_colors
from home import *
import re
from rapidfuzz import process

import json
import os

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
        device, location, action, value = None, None, None, None
        command = command.lower()
        mapped = map_keywords(command)
        number, unit = extract_number_and_unit(command)

        if unit is None and "brightness" in command:
            unit = "%"
        elif unit is None and "temperature" in command:
            unit = "degrees"

        if "lights" in mapped:
            device = "lights"
        elif "set_temperature_cool" in mapped:
            device = "cooling"
        elif "set_temperature_heat" in mapped:
            device = "heating"
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
            value = number
        elif "set_temperature" in mapped or (unit and unit.lower() == "degrees"):
            if "cool" in command:
                action = "set_temperature_cool"
            elif "heat" in command:
                action = "set_temperature_heat"
            value = number
        elif "set_cooling" in mapped or (unit and unit.lower() == "degrees"):
            action = "set_temperature_cool"
            value = number
        elif "set_heating" in mapped:
            action = "set_temperature_heat"
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
            if instruction["action"] == "turn_on" and instruction["device"] is not None:
                responses.append(turn_on(instruction["device"], instruction["location"]))

            elif instruction["action"] == "turn_off" and instruction["device"] is not None:
                responses.append(turn_off(instruction["device"], instruction["location"]))

            elif instruction["action"] == "set_color_light" and instruction["device"] is not None:
                responses.append(set_color_light(instruction["device"], instruction["location"]))

            elif instruction["action"] == "set_brightness_light" and instruction["device"] is not None:
                responses.append(set_brightness_light(instruction["device"], instruction["location"]))

            elif instruction["action"] == "set_temperature_cool" and instruction["device"] is not None:
                responses.append(set_temperature_cool(instruction["device"], instruction["location"]))

            elif instruction["action"] == "set_temperature_heat" and instruction["device"] is not None:
                responses.append(set_temperature_heat(instruction["device"], instruction["location"]))

            elif instruction["action"] == "set_channel_tv" and instruction["device"] is not None:
                responses.append(set_channel_tv(instruction["device"], instruction["location"]))

            elif instruction["action"] == "get_time":
                responses.append(get_time())

            elif instruction["action"] == "get_date":
                responses.append(get_date())

            elif instruction["action"] == "get_news":
                responses.append(get_news())

            elif instruction["action"] == "get_status":
                responses.append(get_status())

            elif instruction["action"] == "get_weather":
                responses.append(get_weather())

            else:
                responses.append("Unknown command.")
        except Exception as e:
            return f"Error while executing command: {e}"

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


def get_output(instructions):
    output_lines = []
    for instruction in instructions:
        output_lines.append(instruction["value"])

    return "\n".join(output_lines)


def smart_home_agent(user_input):
    correct_input = correct_spelling(user_input)
    instructions = parse_command(correct_input)

    output = get_output(execute_command(instructions))
    return output


while True:
    inp = input("Enter command: ")
    response = smart_home_agent(inp)

    print(response)
