import keyboard
import pyautogui
import pyperclip
import toml
import time
import re
import os
from datetime import datetime
from rich import print
from rich.markup import escape

def pre_start_exit():
    print(f"[!] {EXIT_KEY.upper()} pressed. Exiting.")
    safe_exit()

def safe_exit():
    # Calculate and display total elapsed time
    total_seconds = time.time() - start_time
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    print(f"\n[bold red]Exiting.[/] Took {minutes}m {seconds:02d}s.")
    
    # Unhooking prevents the program from hanging on exit
    keyboard.unhook_all()
    os._exit(0)

def start_clicking():
    interval_sec = INTERVAL_MS / 1000.0
    print(f"\n[bold green][!][/] Started. To EXIT early let go of [bold]SHIFT[/]!")

    time.sleep(0.1)

    attempt_width = len(str(SAFETY_LIMIT))
    alt_extra_info = ""

    for i in range(0, SAFETY_LIMIT + 1):
        keyboard.press_and_release('ctrl+alt+c')
        time.sleep(0.05)
        
        # FIX: Strip \r to prevent the cursor from jumping to the start of the line
        raw_text = pyperclip.paste().replace('\r', '')

        # Extract Item Name with safety check
        item_name = m.group(1).strip() if (m := re.search(r"Rarity:.+\n(.+)", raw_text)) else "ERROR: Item name not found!" 

        # High-precision timestamp
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Print formatted log. Using escape(REGEX) ensures square brackets don't break Rich tags.
        print(f"[{timestamp}] [cyan]Result {str(i).rjust(attempt_width)}[/]: Regex: [yellow]\"{escape(REGEX)}\"[/] Item: [white]{item_name}[/] [magenta]{alt_extra_info}[/]")

        # Check for regex match.
        if re.search(REGEX, raw_text, re.IGNORECASE):
            print("[bold green][!] Match found! Exiting.[/]")
            safe_exit()

        has_prefix = bool(re.search("Prefix", raw_text)) 
        has_suffix = bool(re.search("Suffix", raw_text)) 

        # Click logic based on MODE
        if MODE == "alt":
            if (ALT_FILL_PREFIX and not has_prefix) or (ALT_FILL_SUFFIX and not has_suffix):
                # Use an orb of augmentation via alt+click
                with pyautogui.hold('alt'):
                    pyautogui.click()
                alt_extra_info = "(filled prefix)" if not has_prefix else "(filled suffix)"
            else:
                pyautogui.click()
                alt_extra_info = ""
        else:
            # For orb of alchemy, scour first via alt-click, then alch again
            with pyautogui.hold('alt'):
                pyautogui.click()
            time.sleep(0.05)
            pyautogui.click()

        # Responsive wait loop
        end_time = time.time() + interval_sec
        while time.time() < end_time:
            if not keyboard.is_pressed('shift'):
                print("\n[bold yellow][!] Shift released during wait. Exiting.[/]")
                safe_exit()
            time.sleep(0.01)

    print("[bold red][!] Safety limit reached. Exiting.[/]")
    safe_exit()

# Configuration Loading
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
start_time = time.time()

if MODE not in ("alt", "alch"):
    print("[bold red]Invalid mode in toml file. Exiting.[/]")
    safe_exit()

# Main Listener Interface
orb_name = "Orb of Alteration" if MODE == "alt" else "Orb of Alchemy"
print("[bold blue]======= START OF PROGRAM ========[/]")
print(f"Mode: [blue]{MODE}[/blue] | Regex: \"[yellow]{escape(REGEX)}[/yellow]\"")
print(f"Safety limit: {SAFETY_LIMIT} | Interval: {INTERVAL_MS} ms")

if MODE == "alt":
    print(f"Fill prefix: {ALT_FILL_PREFIX} | Fill suffix: {ALT_FILL_SUFFIX}")

print(f"\n[!] Right click an {orb_name.upper()}, hold [bold]SHIFT[/], hover item, then press [bold]{HOTKEY.upper()}[/].")
print(f"Waiting... Or press [bold red]{EXIT_KEY.upper()}[/] to exit.")

# Setup hotkeys
keyboard.add_hotkey(EXIT_KEY, pre_start_exit)
keyboard.add_hotkey(f"shift+{HOTKEY}", start_clicking)

keyboard.wait(EXIT_KEY)