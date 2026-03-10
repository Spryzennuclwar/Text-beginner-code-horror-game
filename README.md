# Text-beginner-code-horror-game
Designed as beginner with VS Code and integration of Codex by OpenAI.

## Overview
This is a beginner-friendly, text-based horror game written in Python. It runs in the terminal and focuses on atmosphere, pacing, and interactive choices. The story adapts to user input, uses randomized endings, and supports optional audio and visual effects when extra libraries are installed.

## Features
- Typewriter-style text output for suspense
- Timed input (silence becomes part of the horror)
- Randomized endings for replayability
- Branching scenes based on choices
- Optional color styling and ASCII title banner
- Optional audio effects and whisper-style narration
- Optional typewriter �tick� sound on Windows

## Requirements
- Python 3.8+ recommended

### Optional Libraries
Install these to unlock the full experience:
```
pip install rich colorama pyfiglet playsound pyttsx3
```

## How to Run
```
python Program.py
```

## Optional Audio Setup
To enable ambient audio effects:
1. Create a folder named `assets` next to `Program.py`.
2. Add any of these files (WAV format recommended):
   - `heartbeat.wav`
   - `footsteps.wav`
   - `wind.wav`
   - `drip.wav`
   - `scrape.wav`
3. Open `Program.py` and set:
```
ENABLE_SOUND = True
```

## Optional Whisper Narration
If you want whispered narration through your speakers:
1. Install `pyttsx3`.
2. Set in `Program.py`:
```
ENABLE_TTS = True
```

## Typewriter Sound
On Windows, the game can play soft �typewriter ticks� using `winsound`.
Control it in `Program.py`:
```
ENABLE_TYPEWRITER_SOUND = True
```

## Game Flow
1. The game asks your name.
2. It presents a series of unsettling prompts.
3. Your choices change which scenes you see.
4. A final decision leads to one of two endings.
5. You can replay for different outcomes.

## Project Structure
```
.
+-- Program.py
+-- README.md
```

## Notes for Beginners
- The game uses standard Python only; all enhancements are optional.
- If you don�t install extra libraries, the story still works.
- You can expand the story by adding more scenes and endings in `Program.py`.

## Credits
Created as a beginner project in VS Code with assistance from Codex by OpenAI.
