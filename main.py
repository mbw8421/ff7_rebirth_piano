import csv
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


def use_left_joystick(direction):
    gamepad.left_joystick_float(x_value_float=direction[0], y_value_float=direction[1])
    gamepad.update()
    sleep(KEY_DELAY)
    gamepad.left_joystick_float(x_value_float=0, y_value_float=0)
    gamepad.update()


def use_right_joystick(direction):
    gamepad.right_joystick_float(x_value_float=direction[0], y_value_float=direction[1])
    gamepad.update()
    sleep(KEY_DELAY)
    gamepad.right_joystick_float(x_value_float=0, y_value_float=0)
    gamepad.update()


def delay(val):
    sleep(val - KEY_DELAY)


def load_song_data_from_csv(song_name):
    """Load song data from csv file."""
    with open(f'songs/{song_name}.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def play_song(song_name):
    formatted_name = song_name.strip().replace(" ", "_").lower()
    song_data = load_song_data_from_csv(formatted_name)

    # Start the song
    push_button(vg.DS4_BUTTONS.DS4_BUTTON_CROSS)

    note_count = len(song_data) - 2

    # Play the song data
    for i, line in enumerate(song_data):
        if i > 1:
            print(f"Playing note {i - 1}/{note_count}")
        if i == 0:
            continue
        if line[0] == "S":
            delay(float(line[2]))
        elif line[0] == "L":
            use_left_joystick(POSITION[line[1]])
            delay(float(line[2]))
        elif line[0] == "R":
            use_right_joystick(POSITION[line[1]])
            delay(float(line[2]))


def setup_listener():
    global mouse_listener
    mouse_listener.start()
    print("Click onto the PS Remote Play / Chiaki window")
    mouse_listener.join()


def get_song():
    global song
    song = input("Which song would you like to play? ")


if __name__ == "__main__":
    get_song()
    setup_listener()
