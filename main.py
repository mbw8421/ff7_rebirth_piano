import csv
import sys
from time import sleep, perf_counter
from pynput.mouse import Listener

import vgamepad as vg

KEY_DELAY = 0.1

# Fixed compensation for PS Remote Play / Chiaki input latency: every note is
# sent this many seconds *before* its scheduled time. Tune by ear/eye against
# the Great/Good/Bad/Miss counter in-game: raise it if hits are consistently
# registering late, lower it (or go negative) if they're consistently early.
LEAD_OFFSET = 0.08

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


def sleep_until(target_time):
    """Sleep until an absolute perf_counter() timestamp.

    Using an absolute target (rather than a fixed-duration sleep) means any
    jitter from the previous note's processing is corrected here instead of
    compounding into the next one.
    """
    remaining = target_time - perf_counter()
    if remaining > 0:
        sleep(remaining)


def push_button(button):
    gamepad.press_button(button=button)
    gamepad.update()
    press_time = perf_counter()
    sleep_until(press_time + KEY_DELAY)
    gamepad.release_button(button=button)
    gamepad.update()


def push_single_joystick(stick, direction):
    JOYSTICK_METHODS[stick](x_value_float=direction[0], y_value_float=direction[1])
    gamepad.update()
    press_time = perf_counter()
    sleep_until(press_time + KEY_DELAY)
    JOYSTICK_METHODS[stick](x_value_float=0, y_value_float=0)
    gamepad.update()


def push_both_joysticks(direction_left, direction_right):
    JOYSTICK_METHODS["left"](x_value_float=direction_left[0], y_value_float=direction_left[1])
    JOYSTICK_METHODS["right"](x_value_float=direction_right[0], y_value_float=direction_right[1])
    gamepad.update()
    press_time = perf_counter()
    sleep_until(press_time + KEY_DELAY)
    JOYSTICK_METHODS["left"](x_value_float=0, y_value_float=0)
    JOYSTICK_METHODS["right"](x_value_float=0, y_value_float=0)
    gamepad.update()


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

    # Every note's target time is scheduled as an offset from this single
    # anchor, rather than relative to "whenever the previous note finished" -
    # that's what stops small delays from one note carrying over and
    # compounding into every note after it.
    start_time = perf_counter()
    next_target = start_time

    for i, line in enumerate(song_data):
        if i == 0:
            continue
        if i > 1:
            elapsed = perf_counter() - start_time
            print(f"Playing note [{line[1]}] [{note_count}/{total_note_count}][{i + 1}][{elapsed:.4f}]")
            if not line[1] or not line[2]:
                print(f"Exiting due to missing data")
                exit(1)

        sleep_until(next_target - LEAD_OFFSET)
        next_target += float(line[2])

        if line[0] == "S":
            pass
        elif line[0] == "L":
            push_single_joystick("left", POSITION[line[1]])
        elif line[0] == "R":
            push_single_joystick("right", POSITION[line[1]])
        elif line[0] == "B":
            left, right = line[1].split("-")
            push_both_joysticks(POSITION[left], POSITION[right])
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
