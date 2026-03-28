# Awakened Spam

A lightweight, automated Python script for efficiently rolling items with alteration or alchemy orbs in **Path of Exile**. This script streamlines the tedious process of checking item affixes and rerolling until you find the desired mods. This was originally going to be a fork of [AwakenedAlterationSpam](https://github.com/VVeiVVang/AwakenedAlterationSpam), but I ended up rewriting the whole thing. Thanks to that author, _VVeiVVang_, for the original inspiration!

## Screenshot

<img width="828" height="562" alt="image" src="https://github.com/user-attachments/assets/d0e6c094-5aed-429d-b82b-c2db9273f8d9" />

_Screenshot may not be from the latest version_

## Overview

Awakened Spam automates the alteration orb rolling process by:

- Automatically capturing advanced item tooltips with `Ctrl+Alt+C`
- Extracting and parsing the item name
- Matching the item against a user-defined regex pattern
- Auto-clicking to reroll if no match is found
- Keep count of rolling attempts
- Stopping instantly when a match is found or safety limit is reached

## Features

✨ **Automatic item capture** - Reads directly from clipboard  
✨ **Regex pattern matching** - Uses the powerful (Python) regex patterns (similar to PoE's stash search using double-quotes)  
✨ **Safety limit** - Prevents accidental overspending of orbs  
✨ **Configurable** - All settings in `config.toml`  
✨ **No GUI required** - Lightweight console-based interface  
✨ **Hotkey controlled** - Start with customizable hotkeys  
✨ **Easy exiting hotkey** - Let go of `Shift` to stop the script immediately  
✨ **Adjustable interval** - Adjustable interval for server latency compensation

## Requirements

- **Python** 3.10 or higher
- **Windows** (probably; I haven't tested in other OS)
- **Path of Exile** running

## Installation

### 1. Clone or download this repository

```bash
git clone https://github.com/your-username/AwakenedSpam.git
cd AwakenedSpam
```

### 2. Install dependencies

**Using pip:**

```bash
pip install -r requirements.txt
```

**Using uv (faster alternative):**

If you have [uv](https://github.com/astral-sh/uv) installed:

```bash
uv sync
```

## Usage

### 1. Rename `config.toml.default` to `config.toml` and configure your settings in `config.toml` (see [Configuration](#configuration) section below)

### 2. Launch the script

```bash
python AwakenedSpam.py
```

### 3. In-game workflow

Once the script is running and waiting for the hotkey to start:

1. Switch to your Path of Exile window.
2. Open your crafting panel (inventory, currency tab, etc).
3. Make sure your target item is already in an appropriate state, ie magic for alteration or rare/normal for alchemy.
4. Hold down `SHIFT`.
5. `RIGHT CLICK` the appropriate crafting orb (depending on what you set in `mode`).
6. Hover over your target item.
7. Press `HOME` while keep holding down `SHIFT`. Don't move your mouse off the target item.
8. Let go of `SHIFT` to stop the script immediately.

## Configuration

Edit `config.toml` to customize behavior:

### [base] section

Controls the core rolling behavior and item matching.

```toml
[base]
mode = "alt"
regex = "life"
```

- **`mode`** - Set to either `"alt"` (alteration orb) or `"alch"` (alchemy orb).
- **`regex`** - **Case-insensitive** Python regex pattern to match item.

**Important about regex:** This uses Python regex, which _may not_ be exactly the same as PoE's regex search. Test your patterns at [regex101.com](https://regex101.com) to ensure they work as expected.

**Regex Examples:**

- `"speed"` - Match any item that says "speed" anywhere like "25% increased Movement Speed" or "19% increased Attack Speed".
- `"merciless|dictator"` - Match either the mod "Merciless" or "Dictator" (for physical damage weapons).
- `"prefix"` - Match any item that has a prefix (since the word "Prefix" will show up in the advanced item description).
- `"melee stun|per 10 str"` - Will match either the Elder mods "Socketed Gems are Supported by Level 10 Endurance Charge on Melee Stun" OR "1% increased Spell Damage per 10 Strength".
- `"\+([89][1-9]|[1-9][0-9]{2})\S+ to maximum Life"` - Match any life above 80%, such as "+123% to maximum Life".

### [alt] section

Decides when to use an Orb of Augmentation to fill either an empty prefix or suffix. This saves alteration cost when the regex can only match on a prefix or suffix (or both).

```toml
[alt]
fill_prefix = true
fill_suffix = true
```

- **`fill_prefix`** - Use augmentation orbs to fill empty prefix slots (set to `true` or `false`).
- **`fill_suffix`** - Use augmentation orbs to fill empty suffix slots (set to `true` or `false`).

### [alch] section

Reserved for future alchemy orb settings (no extra setting currently available).

```toml
[alch]
```

### [advanced] section

Fine-tune performance and hotkeys.

```toml
[advanced]
hotkey = "home"
interval_ms = 100
safety_limit = 100
```

- **`hotkey`** - Hotkey to start the automation by holding Shift and pressing this key. Some good examples include `"="`, `"end"`, `"backspace"`, `"pageup"`, `"pagedown"`. **Avoid** keys that PoE uses like `"p"`, which opens the passive skill tree and close your crafting window.
- **`interval_ms`** - Milliseconds to wait between each click. Depends on your latency to the PoE server. Setting too low may cause missed clicks or server kicks for spam. Start at 100ms and adjust as needed.
- **`safety_limit`** - Maximum number of roll attempts before automatically exiting (prevents accidental overspending).

## Questions

- Why do I have to hold `Shift` while the script is running? Why can't I afk?
  - I tried to use the `keyboard` package to continue holding down `Shift`, but I couldn't get it to work. Maybe it needs a lower level control for direct driver communication. I'll be happy to look at any pull requests.
- Will this work on the harvest horticraft station?
  - No, since the mouse will have to move to click the "Craft" button, then back to the item to copy the item. But definitely possible. I can work on this as a future update.
- Will I get banned for using this?
  - I'm not sure. This project is for educational purposes. Use at your own risk.

## Tips

- **Adjust `interval_ms`** if the script is skipping clicks or you're getting kicked for spam.
  - The interval should at least be higher than the latency to the server realm.
- **Use a visible overlay** (e.g., always-on-top PowerShell window or a 2nd monitor) to monitor progress.
- **Test regex patterns** before large rolling sessions. Remember this is Python regex, which may be different from PoE regex. I recommend [regex101.com](https://regex101.com/) to test.
- **Check [Craft of Exile](https://www.craftofexile.com/)** to understand your odds of certain mods (and adjust `safety_limit` appropriately).
- **Start with a low `safety_limit`** to test configuration.

## Legal & Ethical Use

This tool automates in-game actions. I created this for educational purposes. Use responsibly:

- Follow GGG's Terms of Service.
- Use at your own risk.
- I'm not responsible for loss of currency, items, or even accounts if banned.

## Contributing

Feel free to open issues (please read the [Questions](#questions) and [Tips](#tips) section first), submit pull requests, or suggest improvements!
