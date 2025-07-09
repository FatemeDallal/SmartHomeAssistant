from agent import smart_home_agent

if __name__ == '__main__':
    test_cases = [
        "turn on the lights in the kitchen",
        "turn off the lights in the bathroom",
        "set the color of the lights to blue",
        "set brightness to 60 in room1",
        "turn on heating in room2",
        "set the temperature to 25 degrees in the living room",
        "change the TV channel to 4",
        "get the weather",
        "what time is it",
        "get the news",
        "turn off lights and set brightness to 70 in kitchen"
    ]

    for test in test_cases:
        print("Input:", test)
        response = smart_home_agent(test)
        print("Response:", response)
        print("-" * 60)
