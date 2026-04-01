import keyboard
import pyautogui
import pyperclip
import toml
import time
import re
import os
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
    """Unhooks keys and calculates total session time."""
    
    keyboard.unhook_all()
    
    total_seconds = time.time() - start_time
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    console.print(f"\n[bold red]Exiting.[/] Took {minutes}m {seconds:02d}s.")
    
    os._exit(0)

def get_harvest_coords():
    """Captures item and craft positions by listening for specific user inputs."""

    console.print("[bold yellow][!][/] Place the item in the [bold]Horticrafting Station[/] and select a craft option.")
    console.print("Hold [bold blue]SHIFT[/] and [bold blue]CLICK[/] on the target item... (and keep holding [bold blue]SHIFT[/]).")
    console.print(f"Waiting... Or press [bold blue]{EXIT_KEY.upper()}[/] now to exit.")
    
    mouse_item = None
    while True:
        if keyboard.is_pressed(EXIT_KEY):
            pre_start_exit()

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

        if not keyboard.is_pressed('shift'):
            console.print("[bold blue][!] SHIFT[/] released.")
            safe_exit()
        time.sleep(0.01)
    
    mouse_craft = pyautogui.position()
    console.print(f"[green]Registered CRAFT button position:[/] {mouse_craft}")

    start_clicking(mouse_item, mouse_craft)

def start_clicking(mouse_item=None, mouse_craft=None):
    interval_sec = REROLL_INTERVAL_MS / 1000.0
    action_sec = ACTION_INTERVAL_MS / 1000.0
    
    console.print(f"\n[bold blue][!][/] Started. [red]Do not move the mouse[/]. To [bold]EXIT[/] early let go of [bold blue]SHIFT[/]!")

    attempt_width = len(str(SAFETY_LIMIT))
    alt_extra_info = ""

    for i in range(0, SAFETY_LIMIT + 1):
        # Move to item location if harvesting
        if MODE == "harvest":
            pyautogui.moveTo(mouse_item)
            time.sleep(action_sec)

        keyboard.press_and_release('ctrl+alt+c')
        time.sleep(action_sec)
        
        # Strip \r to fix the 'nonet' printing bug
        raw_text = pyperclip.paste().replace('\r', '')

        item_name = m.group(1).strip() if (m := re.search(r"Rarity:.+\n(.+)", raw_text)) else "ERROR" 
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Use escape() so regex characters don't break rich formatting
        console.print(f"[{timestamp}] [cyan]Result {str(i).rjust(attempt_width)}[/]: Regex: [yellow]\"{escape(REGEX)}\"[/] Item: [white]{item_name}[/] [magenta]{alt_extra_info}[/]")

        if re.search(REGEX, raw_text, re.IGNORECASE | re.S):
            console.print("[bold blue][!][/] [bold green]Match found![/]")
            safe_exit()

        alt_extra_info = ""
        # Execute clicking logic
        if MODE == "harvest":
            pyautogui.moveTo(mouse_craft)
            time.sleep(action_sec)
            pyautogui.click()
        elif MODE == "alt":
            has_prefix = "Prefix" in raw_text
            has_suffix = "Suffix" in raw_text
            if (ALT_AUG_PREFIX and not has_prefix) or (ALT_AUG_SUFFIX and not has_suffix):
                pyautogui.keyDown('alt')
                pyautogui.click()
                pyautogui.keyUp('alt')
                alt_extra_info = "(augmented prefix)" if not has_prefix else "(augmented suffix)"
            else:
                pyautogui.click()
        elif MODE == "alch":
            #with pyautogui.hold('alt'):
            #    pyautogui.click()
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
            time.sleep(0.01)

    console.print("[bold blue][!][/] [bold red]Safety limit reached. Exiting.[/]")
    safe_exit()

# --- Main Listener ---

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

ALT_AUG_PREFIX = config["alt"]["aug_prefix"]
ALT_AUG_SUFFIX = config["alt"]["aug_suffix"]

HOTKEY              = config["advanced"]["hotkey"]
REROLL_INTERVAL_MS  = config["advanced"]["reroll_interval_ms"]
ACTION_INTERVAL_MS  = config["advanced"]["action_interval_ms"]
SAFETY_LIMIT        = config["advanced"]["safety_limit"]

EXIT_KEY = 'esc'

if MODE not in ("alt", "alch", "chaos", "harvest"):
    console.print("[bold red]Invalid mode in toml file. Exiting.[/]")
    safe_exit()

# Main Listener Interface
console.print("[bold blue]======= START OF PROGRAM ========[/]")
console.print(f"Mode: [blue]{MODE}[/] | Regex: \"{escape(REGEX)}\"")
console.print(f"Safety limit: {SAFETY_LIMIT} | Reroll interval: {REROLL_INTERVAL_MS} ms | Action_interval: {ACTION_INTERVAL_MS} ms")

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
if MODE == "harvest":
    get_harvest_coords()

console.print(f"Waiting... Or press [bold blue]{EXIT_KEY.upper()}[/] now to exit.")

keyboard.add_hotkey(EXIT_KEY, pre_start_exit)
keyboard.add_hotkey(f"shift+{HOTKEY}", lambda: start_clicking(mouse_item, mouse_craft))

keyboard.wait(EXIT_KEY)