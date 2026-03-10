import time
import random
import os
import sys
import threading

# Optional third-party libraries (install to unlock full effects)
try:
    from rich import print as rprint
    from rich.console import Console
    from rich.text import Text
    RICH_AVAILABLE = True
except Exception:
    RICH_AVAILABLE = False

try:
    from colorama import init as colorama_init
    from colorama import Fore, Style
    COLORAMA_AVAILABLE = True
except Exception:
    COLORAMA_AVAILABLE = False

try:
    import pyfiglet
    PYFIGLET_AVAILABLE = True
except Exception:
    PYFIGLET_AVAILABLE = False

try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except Exception:
    PLAYSOUND_AVAILABLE = False

try:
    import pyttsx3
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False

try:
    import winsound
    WINSOUND_AVAILABLE = True
except Exception:
    WINSOUND_AVAILABLE = False

if COLORAMA_AVAILABLE:
    colorama_init(autoreset=True)

console = Console() if RICH_AVAILABLE else None

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
SFX = {
    "heartbeat": os.path.join(ASSETS_DIR, "heartbeat.wav"),
    "footsteps": os.path.join(ASSETS_DIR, "footsteps.wav"),
    "wind": os.path.join(ASSETS_DIR, "wind.wav"),
    "drip": os.path.join(ASSETS_DIR, "drip.wav"),
    "scrape": os.path.join(ASSETS_DIR, "scrape.wav"),
}

ENABLE_SOUND = False  # Set True if you add audio files under assets/
ENABLE_TTS = False    # Set True for whispered narration (pyttsx3 required)
ENABLE_TYPEWRITER_SOUND = True  # Uses quiet system beeps if winsound is available
TYPEWRITER_SPEED = 0.03
GLITCH_CHANCE = 0.08


def _play_sound(name):
    if not ENABLE_SOUND or not PLAYSOUND_AVAILABLE:
        return
    path = SFX.get(name)
    if path and os.path.isfile(path):
        try:
            playsound(path, block=False)
        except Exception:
            pass


def _tts_whisper(text):
    if not ENABLE_TTS or not TTS_AVAILABLE:
        return
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 120)
        engine.setProperty("volume", 0.6)
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass


def _glitch(text):
    if random.random() > GLITCH_CHANCE:
        return text
    glitch_chars = ["#", "%", "&", "@", "*", "=", "-"]
    out = []
    for ch in text:
        if ch.isalpha() and random.random() < 0.10:
            out.append(random.choice(glitch_chars))
        else:
            out.append(ch)
    return "".join(out)


def _print_line(text, color=None):
    text = _glitch(text)
    if RICH_AVAILABLE:
        style = None
        if color == "red":
            style = "bold red"
        elif color == "dim":
            style = "dim"
        elif color == "cyan":
            style = "cyan"
        rprint(Text(text, style=style))
    elif COLORAMA_AVAILABLE and color:
        palette = {
            "red": Fore.RED + Style.BRIGHT,
            "dim": Style.DIM,
            "cyan": Fore.CYAN,
        }
        print(palette.get(color, "") + text + Style.RESET_ALL)
    else:
        print(text)


def _typewriter_tick(ch, index):
    if not ENABLE_TYPEWRITER_SOUND or not WINSOUND_AVAILABLE:
        return
    if ch.isspace():
        return
    # Short, quiet ticks every few characters to avoid being too loud
    if index % 3 == 0:
        try:
            winsound.Beep(900, 10)
        except Exception:
            pass


def typewriter(text, speed=TYPEWRITER_SPEED, color=None):
    text = _glitch(text)
    if RICH_AVAILABLE and color:
        style = "red" if color == "red" else "cyan" if color == "cyan" else "dim"
        console.print(Text("", style=style), end="")
    for i, ch in enumerate(text):
        sys.stdout.write(ch)
        sys.stdout.flush()
        _typewriter_tick(ch, i)
        time.sleep(speed)
    sys.stdout.write("\n")
    sys.stdout.flush()


def timed_input(prompt, timeout=12):
    """Return user's input or empty string if they don't respond in time."""
    user_input = {"value": ""}

    def _get_input():
        try:
            user_input["value"] = input(prompt)
        except Exception:
            user_input["value"] = ""

    thread = threading.Thread(target=_get_input, daemon=True)
    thread.start()
    thread.join(timeout)
    return user_input["value"]


def title_card():
    if PYFIGLET_AVAILABLE:
        banner = pyfiglet.figlet_format("HOLLOW DOOR", font="slant")
        _print_line(banner, color="red")
    else:
        _print_line("=== HOLLOW DOOR ===", color="red")


def scene_intro(name):
    title_card()
    _play_sound("wind")
    typewriter("The air tastes like iron.", speed=0.04, color="dim")
    time.sleep(0.6)
    typewriter("Something is standing on the other side of your door.", speed=0.035)
    time.sleep(0.6)
    typewriter(f"It already knows your name, {name}.", speed=0.05, color="red")
    _tts_whisper(f"It already knows your name, {name}.")


def scene_choice_alone():
    while True:
        _play_sound("heartbeat")
        a = timed_input("Are you alone? (Y/N) ", timeout=10).strip().upper()
        if not a:
            typewriter("Silence is also an answer.", speed=0.05, color="dim")
            a = "Y"
        if a == "Y":
            typewriter("Good. No one will hear you.", speed=0.04, color="red")
            time.sleep(1)
            typewriter("Imagine the cold breath at your neck...", speed=0.04, color="dim")
            return "alone"
        if a == "N":
            typewriter("Then I'll be patient. I'll learn every voice in the house.", speed=0.04)
            return "not_alone"
        typewriter("Please answer Y or N.", speed=0.03, color="dim")


def scene_choice_steps():
    while True:
        _play_sound("footsteps")
        b = timed_input("Do you hear the footsteps outside your door? (Y/N) ", timeout=10).strip().upper()
        if not b:
            typewriter("The steps stop. They are right behind you.", speed=0.05, color="red")
            b = "Y"
        if b == "Y":
            typewriter("Don't look at the crack beneath the door.", speed=0.04)
            time.sleep(0.6)
            typewriter("Did you see it move?", speed=0.05, color="red")
            return "steps_yes"
        if b == "N":
            typewriter("Then why is your door handle turning?", speed=0.05, color="red")
            return "steps_no"
        typewriter("Please answer Y or N.", speed=0.03, color="dim")


def scene_dark_hallway():
    _play_sound("drip")
    typewriter("You press your ear to the door.", speed=0.04)
    time.sleep(0.5)
    typewriter("The hallway smells of wet wood and old pennies.", speed=0.04, color="dim")
    time.sleep(0.5)
    typewriter("A wet hand slides beneath the gap, groping for your shadow.", speed=0.05, color="red")


def scene_phone(name):
    typewriter("Your phone lights up. No number. Just your name.", speed=0.04)
    time.sleep(0.5)
    typewriter(f"The message is a single word: 'TURN', {name}.", speed=0.05, color="red")


def scene_mirror():
    typewriter("The mirror on the wall is breathing.", speed=0.04, color="dim")
    time.sleep(0.5)
    typewriter("Its fog writes your answer before you say it.", speed=0.04)


def scene_knob():
    _play_sound("scrape")
    typewriter("The handle turns anyway, slow as a bone being twisted.", speed=0.05, color="red")
    time.sleep(0.5)
    typewriter("Your lock clicks. Then another. Then another.", speed=0.04)


def scene_whisper_loop(name):
    typewriter("A voice from the hallway uses your voice.", speed=0.05, color="red")
    time.sleep(0.5)
    typewriter(f"It says the sentence you are thinking right now, {name}.", speed=0.05)


def scene_final_choice():
    while True:
        c = timed_input("Do you open the door? (Y/N) ", timeout=8).strip().upper()
        if not c:
            typewriter("Your hand moves without permission.", speed=0.05, color="red")
            c = "Y"
        if c == "Y":
            return "open"
        if c == "N":
            return "close"
        typewriter("Please answer Y or N.", speed=0.03, color="dim")


def ending_open():
    typewriter("The door opens into your room.", speed=0.05, color="red")
    time.sleep(0.6)
    typewriter("You step back. Something steps forward.", speed=0.05)
    time.sleep(0.6)
    typewriter("It has your face, but it is wearing it wrong.", speed=0.05, color="red")


def ending_close():
    typewriter("You keep the door shut.", speed=0.05)
    time.sleep(0.6)
    typewriter("The scratching stops.", speed=0.05, color="dim")
    time.sleep(0.6)
    typewriter("Then you realize the scratching was inside the room.", speed=0.05, color="red")


def ending_random():
    endings = [
        "A whisper slides under the door: 'We are already inside.'",
        "Your phone buzzes. It's a photo of you... sitting here, right now.",
        "The room goes cold. The lock clicks. Then another lock you didn't know existed.",
        "You hear your own voice from the hallway, asking to be let in.",
        "The light flickers. In the dark, you see teeth where there should be eyes.",
        "You feel a breath on your ear that counts down from five.",
    ]
    time.sleep(0.8)
    typewriter(random.choice(endings), speed=0.05, color="red")


def play(name):
    scene_intro(name)
    state_a = scene_choice_alone()
    state_b = scene_choice_steps()

    # Build tension based on earlier answers
    if state_a == "alone":
        scene_phone(name)
    else:
        scene_mirror()

    if state_b == "steps_yes":
        scene_dark_hallway()
    else:
        scene_knob()

    scene_whisper_loop(name)
    ending_random()
    finale = scene_final_choice()
    if finale == "open":
        ending_open()
    else:
        ending_close()


def main():
    name = timed_input("What's your name? ", timeout=12).strip()
    if not name:
        name = "stranger"
    while True:
        play(name)
        time.sleep(0.8)
        again = timed_input("Play again? (Y/N) ", timeout=8).strip().upper()
        if again != "Y":
            typewriter(f"It doesn't end when you quit, {name}.", speed=0.05, color="red")
            break


if __name__ == "__main__":
    main()
