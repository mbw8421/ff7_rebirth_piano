# Final Fantasy VII Rebirth Piano Minigame Script

A naive implementation of a script that leverages the pip library `vgamepad` to simulate a DS4 controller to send commands through PS Remote Play/Chiaki running on PC/Mac in order to play the stupid piano minigame for you.

Uses CSV files containing the notes and timings to send based on ordinal directions e.g. N = North, NE = North-East to denote each of the 8 possible notes per analog stick. Times are in seconds and refer to the delay to use after the given note before moving on to the next note.

I pulled Youtube videos of perfect runs and loaded the audio from them into Audacity so that I could visually identify when notes were pressed in order to get the timings between notes, this worked 9 times out of 10 without extra fiddling so wasnt too bad.

## Prerequisites
Before proceeding, make sure you have Python 3 installed on your system. You can check this by running python --version (or python3 --version on some systems) in your terminal or command prompt.

As mentioned to use this script you will need to have a working version of PS Remote Play or Chiaki running on the computer you are running the script from.

## Setup and usage

1. Clone the Repository or Download the Project

    Start by cloning the repository or downloading the project to your local machine.

2. Navigate to the Project Directory

    Change into the project directory: 

    ```
    cd path/to/project
    ```

3. Create a Virtual Environment

    Create a new virtual environment in the project directory by running:

    On Windows:

    ```
    python -m venv venv
    ```

    On macOS and Linux: 

    ```
    python3 -m venv venv
    ```

4. Activate the Virtual Environment

    Activate the created virtual environment:

    On Windows:

    ```
    venv\Scripts\activate
    ```

    On macOS and Linux:

    ```
    source venv/bin/activate
    ```

5. Install Dependencies

    Install the required dependencies using the requirements.txt file:

    On Windows:

    ```
    python -m pip install -r requirements.txt
    ```

    On macOS and Linux

    ```
    python3 -m pip install -r requirements.txt
    ```

6. Run the Script

    Finally, run the Python script:

    On Windows:

    ```
    python main.py
    ```

    On macOS and Linux:

    ```
    python3 script_name.py
    ```

    It will ask you to type in the name of the song you want it to play, this will match what the song is called in FF7. Once you've entered the song it will prompt you to click the remote play window. 
    
    Once you have done that it will start. It assumes you already have the song that you want to play highlighted and are at note speed 3/5.

## Deactivating the Virtual Environment
When you're done, you can deactivate the virtual environment by running:

```
deactivate
```

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

   Here is proof! [https://i.ytimg.com/vi/MHxFsa-_y4Q/maxresdefault.jpg(https://www.youtube.com/watch?v=MHxFsa-_y4Q)

3. __Where are the other songs?__

    As of writing this readme I've only added the first of the songs "On Our Way". As it stands this repo functions as the scaffolding around what is required to play the songs.

    Saying that I'll add the other songs when I get around to it, likely not until I am doing trophy cleanup but I plan to use this script to complete all the songs so will add them as I do them.

    I welcome PRs containing the other songs if someone else wants to generate them in the meantime!

4. __Can I create my own CSV file for the other songs / custom songs and get it to play that?__

    Go for it! I've not tried it but in theory this could be extended to play any song (you'd need to handle the changing octaves / keys etc. as this is done automatically for the built in songs).

5. __Your script broke my PC!__

    No it didnt, for the sake of argument though __run at your own risk__ and I take no responisibilty for any damage the script might cause.

## License

This project is licensed under the MIT License - see the LICENSE file for details
