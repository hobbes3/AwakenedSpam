import keyboard
import pyautogui
import pyperclip
import toml
import time
import re
import os
from datetime import datetime
from rich import print

with open('config.toml', 'r') as f:
    config = toml.load(f)

MODE  = config["base"]["mode"]
REGEX = config["base"]["regex"]

HOTKEY       = config["advanced"]["hotkey"]
SAFETY_LIMIT = config["advanced"]["safety_limit"]
INTERVAL_MS  = config["advanced"]["interval_ms"]

ALT_FILL_PREFIX = config["alt"]["fill_prefix"]
ALT_FILL_SUFFIX = config["alt"]["fill_suffix"]

EXIT_KEY = 'esc'

def elapsed_time(start_time):
    total_seconds = time.time() - start_time
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return f"Took {minutes}m {seconds:02d}s."

def start_clicking():
    start_time = time.time()

    interval_sec = INTERVAL_MS / 1000.0
    print(f"[!] Started. To EXIT early let go of SHIFT!")

    time.sleep(0.1)

    attempt_width = len(str(SAFETY_LIMIT))
    alt_extra_info = ""

    for i in range(0, SAFETY_LIMIT + 1):
        keyboard.press_and_release('ctrl+alt+c')
        time.sleep(0.05)
        raw_text = pyperclip.paste()

        item_name = m.group(1).strip() if (m := re.search(r"Rarity:.+\n(.+)", raw_text)) else "ERROR: Item name not found!" 

        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        # Print formatted result log.
        print(f"[{timestamp}] Result {str(i).rjust(attempt_width)}: Regex: \"{REGEX}\" Item Name: {item_name} {alt_extra_info}")

        # Check for regex match.
        if re.search(REGEX, raw_text, re.IGNORECASE):
            print("[!] Match found! Exiting.")
            print(elapsed_time(start_time))
            exit()

        has_prefix = bool(re.search("Prefix", raw_text)) 
        has_suffix = bool(re.search("Suffix", raw_text)) 

        # How to click
        if MODE == "alt":
            if ALT_FILL_PREFIX and not has_prefix or ALT_FILL_SUFFIX and not has_suffix:
                # Use an orb of augmentation via alt+click.
                pyautogui.keyDown('alt')
                pyautogui.click()
                pyautogui.keyUp('alt')

                alt_extra_info = "(filled prefix)" if not has_prefix else "(filled suffix)"
            else:
                # Continue to use an orb of alteration.
                pyautogui.click()
                alt_extra_info = ""
        else:
            # For orb of alchemy, scour first via alt-click, then alch again via click.
            pyautogui.keyDown('alt')
            pyautogui.click()
            pyautogui.keyUp('alt')
            time.sleep(0.05)
            pyautogui.click()

        # Check for shift-release every 10ms during the interval.
        end_time = time.time() + interval_sec
        while time.time() < end_time:
            if not keyboard.is_pressed('shift'):
                print("[!] Shift released during wait. Exiting.")
                print(elapsed_time(start_time))
                exit()
            time.sleep(0.01)

    print("[!] Safety limit reached. Exiting.")
    print(elapsed_time(start_time))
    exit()

def pre_start_exit():
    print(f"[!] {EXIT_KEY.upper()} pressed. Exiting.")
    exit()

def exit():
    keyboard.unhook_all()
    os._exit(0)

if MODE not in ("alt", "alch"):
    print("Invalid mode in toml file. Exiting.")
    exit()

orb_name = "Orb of Alteration" if MODE == "alt" else "Orb of Alchemy"
print("======= START OF PROGRAM ========")
print(f"Mode: [blue]{MODE}[/blue]")
print(f"Regex: \"{REGEX}\"")
print(f"Safety limit: {SAFETY_LIMIT} attempts")
print(f"Interval: {INTERVAL_MS} ms")
if MODE == "alt":
    print(f"Fill prefix: {ALT_FILL_PREFIX}")
    print(f"Fill suffix: {ALT_FILL_SUFFIX}")

print(f"[!] Right click an {orb_name.upper()}, hold SHIFT, hover over the target item, then press {HOTKEY.upper()} to start.")
print(f"Keep holding down SHIFT after starting. Releasing it early will exit the program immediately.")
print(f"Waiting... Or press {EXIT_KEY.upper()} to exit.")

# Set up global hotkeys
keyboard.add_hotkey(EXIT_KEY, pre_start_exit)
keyboard.add_hotkey(f"shift+{HOTKEY}", start_clicking)

# Block main thread until EXIT_KEY is pressed.
keyboard.wait(EXIT_KEY)