# Final Fantasy VII Rebirth Piano Minigame Script

A naive implementation of a script that leverages the pip library `vgamepad` to simulate a DS4 controller to send commands through PS Remote Play/Chiaki running on PC/Mac in order to play the stupid piano minigame for you.

Uses CSV files containing the notes and timings to send based on ordinal directions e.g. N = North, NE = North-East to denote each of the 8 possible notes per analog stick. Times are in seconds and refer to the delay to use after the given note before moving on to the next note.

I pulled Youtube videos of perfect runs and loaded the audio from them into Audacity so that I could visually identify when notes were pressed in order to get the timings between notes, this worked 9 times out of 10 without extra fiddling so wasnt too bad.

**Windows only** (`vgamepad`'s virtual controller only works on Windows).

## Prerequisites (both options below)

1. **ViGEmBus driver** — this is what lets `vgamepad` present a virtual controller to your PC at all. Download and install it from the [ViGEmBus releases page](https://github.com/ViGEm/ViGEmBus/releases) if you don't already have it (it's also a dependency of tools like DS4Windows, so you may already have it installed).
2. A working PS Remote Play or Chiaki session already running and connected to your PS5, with the song you want to play highlighted and note speed set to 3/5.

## Option A: Download and run the .exe (recommended if you don't use Python)

1. Grab the latest `ff7_piano-windows.zip` from the [Releases page](https://github.com/mbw8421/ff7_rebirth_piano/releases) and unzip it anywhere.
2. Double-click `ff7_piano.exe`.
3. Type the song name when prompted (it must match the in-game song name, e.g. `On Our Way`), then click into the PS Remote Play/Chiaki window when asked.

That's it — no Python, no pip, no terminal setup required. The `songs` folder next to the exe holds the CSVs; add your own `.csv` files there in the same [format](#file-format) to play custom songs.

If Windows SmartScreen warns about the exe being unrecognized (normal for an unsigned indie tool), choose "More info" → "Run anyway". If you'd rather not run an unsigned exe at all, use Option B below and run it from source instead.

## Option B: Run from source (for developers / if you don't want to run an exe)

1. Clone the Repository or Download the Project

    Start by cloning the repository or downloading the project to your local machine.

2. Navigate to the Project Directory

    Change into the project directory:

    ```
    cd path/to/project
    ```

3. Create a Virtual Environment

    ```
    python -m venv venv
    ```

4. Activate the Virtual Environment

    ```
    venv\Scripts\activate
    ```

    If PowerShell blocks this with a "running scripts is disabled" error, run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once (as your own user, no admin needed) and try again.

5. Install Dependencies

    ```
    python -m pip install -r requirements.txt
    ```

6. Run the Script

    ```
    python main.py
    ```

    It will ask you to type in the name of the song you want it to play, this will match what the song is called in FF7. Once you've entered the song it will prompt you to click the remote play window.

    Once you have done that it will start. It assumes you already have the song that you want to play highlighted and are at note speed 3/5.

## Deactivating the Virtual Environment
When you're done, you can deactivate the virtual environment by running:

```
deactivate
```

## Building the .exe yourself

Releases are built automatically by the `.github/workflows/release.yml` GitHub Action whenever a `v*` tag is pushed, but you can build one locally too:

```
python -m pip install -r requirements-build.txt
python -m PyInstaller --onefile --name ff7_piano --collect-data vgamepad main.py
```

The exe will be in `dist/`. Copy the `songs` folder next to it before running — the exe reads CSVs from a `songs` folder relative to itself, the same as `main.py` does when run from source. The `--collect-data vgamepad` flag is required: it bundles the `ViGEmClient.dll` that `vgamepad` loads at runtime, which PyInstaller won't pick up automatically.

## File Format

The CSV files expect 3 columns titled:

hand, note and post_delay

Valid values for hand:
|||
|---|---|
L | Left  
R | Right  
B | Both

Valid values for note:
|||
|---|---|
N | North
NE | North-East
E  | East
SE | South-East
S  | South
SW | South-West
W  | West
NW | North-West

If the value of hand for the given row is "B" denoting that 2 notes should be played together, ordinal values for note should be combined, seperated by a dash e.g.

Left plays East, Right plays South in the CSV would be:

B, E-S

## FAQS

1. __Does it work?__

    Did for me! I have included the exact csv I used. I imagine if you find it runs but does not complete the song correctly it will be down to latency between your remote play session and console. You can minimise this by ensuring that both the PS5 and computer you are running the script on are on wired connections and your remote play session is running at a low resolution to help with bandwidth.

    Heres the proof!

    [![Video](https://i.ytimg.com/vi/MHxFsa-_y4Q/maxresdefault.jpg)](https://www.youtube.com/watch?v=MHxFsa-_y4Q)

2. __Can I create my own CSV file for the other songs / custom songs and get it to play that?__

    Go for it! I've not tried it but in theory this could be extended to play any song (you'd need to handle the changing octaves / keys etc. as this is done automatically for the built in songs).

3. __Your script broke my PC!__

    No it didnt, for the sake of argument though __run at your own risk__ and I take no responisibilty for any damage the script might cause.

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Special Thanks

Special thanks to [@bad1dea](https://github.com/bad1dea) for providing most of the song CSVs!
