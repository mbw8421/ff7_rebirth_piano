import csv
import sys
from datetime import datetime
from time import sleep
from pynput.mouse import Listener

import vgamepad as vg

KEY_DELAY = 0.1

POSITION = {
    "N": (0, -1),
    "NE": (1, -1),
    "E": (1, 0),
    "SE": (1, 1),
    "S": (0, 1),
    "SW": (-1, 1),
    "W": (-1, 0),
    "NW": (-1, -1),
}


gamepad = vg.VDS4Gamepad()

JOYSTICK_METHODS = {
    "left": gamepad.left_joystick_float,
    "right": gamepad.right_joystick_float,
}


def on_click(x, y, button, pressed):
    mouse_listener.stop()
    play_song(song)


mouse_listener = Listener(on_click=on_click)
song = ""


def push_button(button):
    gamepad.press_button(button=button)
    gamepad.update()
    sleep(KEY_DELAY)
    gamepad.release_button(button=button)
    gamepad.update()


def push_single_joystick(stick, direction):
    JOYSTICK_METHODS[stick](x_value_float=direction[0], y_value_float=direction[1])
    gamepad.update()
    sleep(KEY_DELAY)
    JOYSTICK_METHODS[stick](x_value_float=0, y_value_float=0)
    gamepad.update()


def push_both_joysticks(direction_left, direction_right):
    JOYSTICK_METHODS["left"](x_value_float=direction_left[0], y_value_float=direction_left[1])
    JOYSTICK_METHODS["right"](x_value_float=direction_right[0], y_value_float=direction_right[1])
    gamepad.update()
    sleep(KEY_DELAY)
    JOYSTICK_METHODS["left"](x_value_float=0, y_value_float=0)
    JOYSTICK_METHODS["right"](x_value_float=0, y_value_float=0)
    gamepad.update()


def delay(val):
    if val < KEY_DELAY:
        return
    sleep(val - KEY_DELAY)


def load_song_data_from_csv(song_name):
    """Load song data from csv file."""
    try:
        with open(f'songs/{song_name}.csv', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
    except FileNotFoundError:
        print(f'Song "{song_name}" not found.')
        exit(1)
    return data


def play_song(song_name):
    formatted_name = song_name.strip().replace(" ", "_").replace("'", ".").lower()
    song_data = load_song_data_from_csv(formatted_name)

    # Start the song
    push_button(vg.DS4_BUTTONS.DS4_BUTTON_CROSS)

    note_count = 0
    total_note_count = song_data[1][1]
    start_time = datetime.now()

    # Play the song data
    for i, line in enumerate(song_data):
        if i == 0:
            continue
        if i > 1:
            timestamp = (datetime.now() - start_time).total_seconds()
            print(f"Playing note [{line[1]}] [{note_count}/{total_note_count}][{i + 1}][{timestamp}]")
            if not line[1] or not line[2]:
                print(f"Exiting due to missing data")
                exit(1)
        if line[0] == "S":
            delay(float(line[2]))
        elif line[0] == "L":
            push_single_joystick("left", POSITION[line[1]])
            delay(float(line[2]))
        elif line[0] == "R":
            push_single_joystick("right", POSITION[line[1]])
            delay(float(line[2]))
        elif line[0] == "B":
            left, right = line[1].split("-")
            push_both_joysticks(POSITION[left], POSITION[right])
            delay(float(line[2]))
            note_count += 1
        if note_count == total_note_count:
            break
        note_count += 1


def setup_listener():
    global mouse_listener
    mouse_listener.start()
    print("Click onto the PS Remote Play / Chiaki window")
    mouse_listener.join()


def get_song_from_user():
    global song
    song = input("Which song would you like to play? ")


if __name__ == "__main__":
    try:
        get_song_from_user()
        setup_listener()
    except KeyboardInterrupt:
        print("User requested to stop the script. Exiting gracefully.")
        sys.exit(0)
