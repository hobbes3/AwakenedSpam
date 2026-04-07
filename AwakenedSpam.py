import keyboard
import pyautogui
import pyperclip
import toml
import time
import regex
import sys
import mouse 
from datetime import datetime
from rich.console import Console
from rich.markup import escape

# Initialize Rich console for better formatting control
console = Console()

def pre_start_exit():
    console.print(f"[bold blue][!] {EXIT_KEY.upper()}[/] pressed.")
    safe_exit()

def safe_exit():
    global running
    keyboard.unhook_all()
    
    total_seconds = time.time() - start_time
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    console.print(f"\n[bold red]Exiting.[/] Took {minutes}m {seconds:02d}s.")
    
    running = False
    sys.exit()

def regex_string(regex, matched_array=[]):
    formatted_regex = []
    for i, r in enumerate(regex):
        if i in matched_array:
            formatted_regex.append(f"[green]{escape(r)}[/]")
        else:
            formatted_regex.append(f"[red]{escape(r)}[/]")
    return "[white] • [/]".join(formatted_regex)

def get_harvest_coords():
    """Captures item and craft positions by listening for specific user inputs."""

    console.print("[bold yellow][!][/] Place the item in the [bold]Horticrafting Station[/] and select a craft option.")
    console.print("Hold [bold blue]SHIFT[/] and [bold blue]CLICK[/] on the target item... (and keep holding [bold blue]SHIFT[/]).")
    console.print(f"Waiting... Or press [bold blue]{EXIT_KEY.upper()}[/] now to exit.")
    
    mouse_item = None
    while True:
        if keyboard.is_pressed(EXIT_KEY):
            pre_start_exit()
            return None, None

        # Captures position only when Shift and Left Click are active
        if keyboard.is_pressed('shift') and mouse.is_pressed('left'):
            mouse_item = pyautogui.position()
            break
        time.sleep(0.01)
    
    console.print(f"[green]Registered item mouse position:[/] {mouse_item}")
    time.sleep(0.1) # Prevent double-triggering

    console.print("[bold yellow][!][/] Hover over the [bold]CRAFT[/] button and press [bold blue]HOME[/] (and keep holding [bold blue]SHIFT[/]).")
    console.print(f"Waiting... Or release [bold blue]SHIFT[/] now to exit.")

    mouse_craft = None
    while not keyboard.is_pressed('home'):
        if keyboard.is_pressed(EXIT_KEY):
            pre_start_exit()
            return None, None

        if not keyboard.is_pressed('shift'):
            console.print("[bold blue][!] SHIFT[/] released.")
            safe_exit()
            return None, None

        time.sleep(0.01)
    
    mouse_craft = pyautogui.position()
    console.print(f"[green]Registered CRAFT button position:[/] {mouse_craft}")

    start_clicking(mouse_item, mouse_craft)

def start_clicking(mouse_item=None, mouse_craft=None):
    interval_sec = REROLL_INTERVAL_MS / 1000.0
    action_sec = ACTION_INTERVAL_MS / 1000.0
    
    console.print(f"\n[bold blue][!][/] Started. [red]Do not move the mouse[/]. To [bold]EXIT[/] early let go of [bold blue]SHIFT[/]!")

    attempt_width = len(str(SAFETY_LIMIT))
    previous_item_name = ""
    same_item_count = 0

    for i in range(0, SAFETY_LIMIT + 1):
        extra_info = ""
        # Move to item location if harvesting
        if MODE == "harvest":
            pyautogui.moveTo(mouse_item)
            time.sleep(action_sec)
        
        if ADVANCED_ITEM_DESCRIPTION:
            keyboard.press_and_release('ctrl+alt+c')
        else:
            keyboard.press_and_release('ctrl+c')
        time.sleep(action_sec)
        
        # Strip \r to fix the 'nonet' printing bug
        raw_text = pyperclip.paste().replace('\r', '')

        matched_regex = []
        for j, r in enumerate(REGEX):
            if regex.search(r, raw_text, flags=regex.IGNORECASE | regex.DOTALL):
                matched_regex.append(j)

        item_name = m.group(1).strip() if (m := regex.search(r"Rarity:.+\n(.+)", raw_text)) else "ERROR" 
        if item_name == previous_item_name:
            same_item_count += 1
        else:
            same_item_count = 0
        if same_item_count >= SAME_ITEM_NAME_LIMIT:
            console.print(f"[bold blue][!][/] [bold red]Detected {same_item_count} consecutive items with the same name.[/]")
            safe_exit()
            return
        previous_item_name = item_name

        has_prefix = None
        has_suffix = None
        augment = False
        if MODE == "alt":
            has_prefix = "Prefix" in raw_text
            has_suffix = "Suffix" in raw_text
            if (ALT_AUG_PREFIX and not has_prefix) or (ALT_AUG_SUFFIX and not has_suffix):
                augment = True
                extra_info = f"- [yellow]augmenting...[/]"

        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        console.print((
            f"[{timestamp}] [cyan]Result {str(i).rjust(attempt_width)}[/] - "
            f"Regex match: {len(matched_regex)}/{REGEX_MIN_COUNT} "
            f"- {regex_string(REGEX, matched_regex)} "
            f"- Item: [white]{item_name}[/] "
            f"[magenta]{extra_info}[/]"
        ),
        highlight=False)
        
        if len(matched_regex) >= REGEX_MIN_COUNT:       
            console.print(f"[bold blue][!][/] [bold green]Minimum match of {REGEX_MIN_COUNT} reached![/]")
            safe_exit()
            return

        # Execute clicking logic
        if MODE == "harvest":
            pyautogui.moveTo(mouse_craft)
            time.sleep(action_sec)
            pyautogui.click()
        elif MODE == "alt":
            if augment:
                pyautogui.keyDown('alt')
                pyautogui.click()
                pyautogui.keyUp('alt')
            else:
                pyautogui.click()
        elif MODE == "alch":
            pyautogui.keyDown('alt')
            pyautogui.click()
            pyautogui.keyUp('alt')
            time.sleep(action_sec)
            pyautogui.click()
        else: # chaos
            pyautogui.click()

        # Responsive wait loop
        end_time = time.time() + interval_sec
        while time.time() < end_time:
            if not keyboard.is_pressed('shift'):
                console.print("[bold blue][!] Shift[/] released.")
                safe_exit()
                return
            time.sleep(0.01)

    console.print("[bold blue][!][/] [bold red]Safety limit reached. Exiting.[/]")
    safe_exit()

# --- Main Listener ---
running = True
start_time = time.time()

try:
    with open('config.toml', 'r') as f:
        config = toml.load(f)
except FileNotFoundError:
    console.print("[bold red]Error:[/] 'config.toml' not found in the script directory.")
    safe_exit()
except toml.TomlDecodeError as e:
    console.print(f"[bold red]Error:[/] Invalid TOML syntax in 'config.toml':\n[yellow]{e}[/]")
    safe_exit()
except Exception as e:
    console.print(f"[bold red]An unexpected error occurred while reading config:[/] {e}")
    safe_exit()

MODE  = config["base"]["mode"]
REGEX = config["base"]["regex"]
REGEX_MIN_COUNT = config["base"]["regex_min_count"]

ALT_AUG_PREFIX = config["alt"]["aug_prefix"]
ALT_AUG_SUFFIX = config["alt"]["aug_suffix"]

HOTKEY                    = config["advanced"]["hotkey"]
SAFETY_LIMIT              = config["advanced"]["safety_limit"]
SAME_ITEM_NAME_LIMIT      = config["advanced"]["same_item_name_limit"]
REROLL_INTERVAL_MS        = config["advanced"]["reroll_interval_ms"]
ACTION_INTERVAL_MS        = config["advanced"]["action_interval_ms"]
ADVANCED_ITEM_DESCRIPTION = config["advanced"]["advanced_item_description"]

EXIT_KEY = 'esc'

if MODE not in ("alt", "alch", "chaos", "harvest"):
    console.print("[bold red]Invalid \"mode\" in config.toml.[/]")
    safe_exit()

# Main Listener Interface
console.print("[bold blue]======= START OF PROGRAM ========[/]")
console.print(f"Mode: [blue]{MODE}[/]")
console.print(f"Regex: {regex_string(REGEX)}", highlight=False)
console.print(f"Regex minimum count: {REGEX_MIN_COUNT}")
console.print(f"Safety limit: {SAFETY_LIMIT} | Same item name limit: {SAME_ITEM_NAME_LIMIT}")
console.print(f"Reroll interval: {REROLL_INTERVAL_MS} ms | Action_interval: {ACTION_INTERVAL_MS} ms")


if MODE in ("alt", "alch", "chaos"):
    orb_name = ""
    if MODE == "alt":
        orb_name = "Orb of Alteration"
        console.print(f"Augment prefix: [blue]{ALT_AUG_PREFIX}[/] | Augment suffix: [blue]{ALT_AUG_SUFFIX}[/]")
    elif MODE == "alch":
        orb_name = "Orb of Alchemy"
    else:
        orb_name = "Chaos Orb"

    console.print(f"[bold blue][!][/] Right click an [bold blue]{orb_name.upper()}[/], hold [bold blue]SHIFT[/], hover item, then press [bold blue]{HOTKEY.upper()}[/] to start (and keep holding [bold blue]SHIFT[/]).")
    console.print(f"Do not move the mouse during the process. Let go of [bold blue]SHIFT[/] to exit early.")

mouse_item, mouse_craft = None, None
if MODE in ("harvest"):
    get_harvest_coords()

console.print(f"Waiting... Or press [bold blue]{EXIT_KEY.upper()}[/] now to exit.")

keyboard.add_hotkey(f"shift+{HOTKEY}", lambda: start_clicking(mouse_item, mouse_craft))

while running:
    if keyboard.is_pressed(EXIT_KEY):
        safe_exit()
    time.sleep(0.1)