# Awakened Spam

A lightweight, automated Python script for **Path of Exile** for efficiently rolling items with

- <img width="22" height="22" alt="Orb_of_Alteration_inventory_icon" src="https://github.com/user-attachments/assets/ffa8af68-1394-4ae7-b0d1-c99ef8be211c" /> alteration orbs
- <img width="22" height="22" alt="Orb_of_Alchemy_inventory_icon" src="https://github.com/user-attachments/assets/fefeb38c-9071-4397-8849-be4e53a81242" /> alchemy orbs
- <img width="22" height="22" alt="Chaos_Orb_inventory_icon" src="https://github.com/user-attachments/assets/f05d174b-159b-4107-abc0-66ec801fa2e5" /> chaos orbs (or "chaos-like" currencies like screaming essences or eldritch embers)
- <img width="22" height="22" alt="Primal_Crystallised_Lifeforce_inventory_icon" src="https://github.com/user-attachments/assets/1292a8a4-28c0-4f6a-86ad-ee7d542a9d4e" /> harvest (horticrafting station)

This script streamlines the tedious process of checking item affixes and rerolling until you find the desired mods. It also prevents the oh-so-common accidental rerolls and physical/mental fatigue. Lastly, this script can leverage multiple Python regex against the advanced item description, aka <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>C</kbd>.

## Legal & Ethical Use

This tool automates _mutiple in-game actions per input_. I created this for educational purposes, ie mostly using AI coding. Use responsibly:

- Follow GGG's Terms of Service.
- Use at your own risk.
- I'm not responsible for loss of currency, items, or even accounts if banned.

## Screenshot

<img width="796" height="431" alt="AwakenedSpamSS" src="https://github.com/user-attachments/assets/3b03f1ec-d5be-441a-bc20-b6e23513df7e" />

_Screenshot may not be from the latest version_

## Overview

Awakened Spam automates the orb rolling process by:

- Automatically capturing advanced item tooltips with <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>C</kbd>
- Matching the item against a set of user-defined regex pattern
- Auto-clicking to reroll if no match is found
- Keep count of rolling attempts
- Stopping instantly on user input, when match is found, or safety limit is reached

## Features

✨ **Lightweight** - No installation required (aside from Python), doesn't modify any settings or create files outside of its directory  
✨ **No GUI required** - Console-based interface  
✨ **Automatic item capture** - Reads directly from clipboard (not your screen)  
✨ **Regex pattern matching** - Uses the powerful (Python) regex patterns (similar to PoE's stash search using double-quotes)  
✨ **Multiple regex** - Allows a set of regex and a minimum count to match multiple mods   
✨ **Configurable** - All settings in `config.toml`  
✨ **Hotkey controlled** - Start with customizable hotkeys  
✨ **Safety limit** - Prevents accidental overspending of orbs  
✨ **Easy exiting hotkey** - Let go of <kbd>Shift</kbd> to stop the script immediately  
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

### 1. Configure the script

Rename `config.toml.default` to `config.toml` and configure your settings (see [Configuration](#configuration) section below).

### 2. Launch the script

```bash
python AwakenedSpam.py
```

### 3. In-game workflow

Once the script is running and waiting for the hotkey to start (for `alt`, `alch`, and `chaos`):

1. Switch to your Path of Exile window.
2. Open your crafting panel (inventory, currency tab, etc).
3. Make sure your target item is already in an appropriate state, ie magic for alteration or rare/normal for alchemy.
4. _Follow the console instruction:_ Hold down <kbd>Shift</kbd> and <kbd>Right click</kbd> the appropriate crafting orb (depending on what you set in `mode`).
5. _Follow the console instruction:_ Hover over your target item and press <kbd>Home</kbd> while still holding <kbd>Shift</kbd>. Don't move your mouse off the target item.
6. Let go of <kbd>Shift</kbd> to stop the script immediately.

For `harvest`:

1. Switch to your Path of Exile window.
2. Open the horticrafting station, place your item in the station, and select a crafting option.
3. Make sure your target item is already in an appropriate state, ie rare for reforge.
4. _Follow the script instruction:_ Hold down <kbd>Shift</kbd> and <kbd>Click</kbd> the target item.
5. _Follow the script instruction:_ Hover over the `CRAFT` button and press <kbd>Home</kbd> while still holding <kbd>Shift</kbd>. Don't move your mouse when the script is running. 
6. Let go of <kbd>Shift</kbd> to stop the script immediately.

## Configuration

Edit `config.toml` to customize behavior:

### [base] section

Controls the core rolling behavior and item matching.

```toml
[base]
mode = "alt"
regex = ["life", "speed"]
regex_min_count = 1
```

- **`mode`** - Set to either `"alt"` (alteration orb), `"alch"` (alchemy orb), `"chaos"` (chaos orb), or `"harvest"` (horticrafting station).
- **`regex`** - A list of regex strings. The regex already has the **case-insensitive** and **single-line** flag.
- **`regex_min_count`** - The minimum number of regex that the item must match. For example, `regex_min_count = 3` means at least 3 of the supplied regex must match.

⚠️ **Important about regex:**

This uses Python regex, which _may not_ be exactly the same as PoE's regex search. Test your patterns at [regex101.com](https://regex101.com) to ensure they work as expected (see [Tips](#tips)).

Also, remember that the regex matches on the _advanced_ item description. For example, the raw text doesn't say `11% increased Strength`, it actually says `11(9-12)% increased Strength`.

**Regex Examples:**

```toml
regex = ["speed"]
regex_min_count = 1
```

Match any item that says "speed" anywhere like `25% increased Movement Speed` or `19% increased Attack Speed`.

```toml
regex = ["merciless", "dictator"]
regex_min_count = 1
```

Match either the mod `Merciless` or `Dictator` (for physical damage weapons).

```toml
regex = ["merciless|dictator"]
regex_min_count = 1
```

Same as above, but using regex's OR expression `|` instead.

```toml
regex = ["prefix"]
regex_min_count = 1
```

Match any item that has a prefix (since the word `Prefix` will show up in the advanced item description).

```toml
regex = ["\\(9-12\\)% increased str"]
regex_min_count = 1
```

Match only on tier 1 Warlord amulet mod `% increased Strength`, which is from 9% to 12%. Note how the backslash has to be escaped inside the double quotes.

```toml
regex = ["equal to", "conquest.+conquest", "warlord's"]
regex_min_count = 2
```

Match a Warlord helmet that has `Gain Accuracy Rating equal to your Strength` _and_ any other Warlord mod (either prefix or suffix). Note that `conquest` in the regex is repeated twice since the `Gain Accuracy...` mod is already `of the Conquest` suffix. This is useful for elevating a mod using an orb of dominance.

### [alt] section

Decides if to use an augmentaton orb to fill either an empty prefix or suffix. This saves alteration cost when the regex can only match on a particular affix.

```toml
[alt]
aug_prefix = true
aug_suffix = true
```

- **`aug_prefix`** - Use augmentation orbs to fill empty prefix slots (set to `true` or `false`).
- **`aug_suffix`** - Use augmentation orbs to fill empty suffix slots (set to `true` or `false`).

### [advanced] section

Fine-tune performance and hotkeys.

```toml
hotkey = "home"
same_item_name_limit = 5
reroll_interval_ms = 100
action_interval_ms = 50
safety_limit = 10
```

- **`hotkey`** - Hotkey to start the automation by holding Shift and pressing this key. Some good examples include `"="`, `"end"`, `"backspace"`, `"pageup"`, `"pagedown"`. **Avoid** keys that PoE uses like `"p"`, which opens the passive skill tree and close your crafting window.
- **`same_item_name_limit`** - If the same item name is detected 5 times in a row, then the program will exit. This usually means the currency is invalid for the target item, ie trying to alch a magic/blue item. This could also happen when alt spamming influenced bases, but it's highly unlikely to happen that many times in a row, ie `Shaper's Lathi of Shaping`.
- **`reroll_interval_ms`** - Milliseconds to wait between each reroll. Depends on your latency to the PoE server. Setting too low may cause missed clicks or server kicks for spam.
- **`action_interval_ms`** - Milliseconds to wait between each action. Each reroll has several actions, such as pressing <kbd>Ctrl</kbd>-<kbd>Alt</kbd>-<kbd>C</kbd>, holding <kbd>Alt</kbd>, and <kbd>Clicking</kbd>. Setting this too low also may cause missed clicks or server kicks.
- **`safety_limit`** - Maximum number of roll attempts before automatically exiting (prevents accidental overspending).

## Tips

- **Adjust `interval_ms`** if the script is skipping clicks or you're getting kicked for spam.
  - The interval should at least be higher than the latency to the server realm.
- **Use a visible overlay** (ie, always-on-top PowerShell window or a 2nd monitor) to monitor progress.
- **Test regex patterns** before large rolling sessions. One way to double check is to find a similar item on trade, go to their hideout, <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>C</kbd>, and paste it in [regex101.com](https://regex.101]). Don't forget to enable the `i` (insensitive) and `s` (single line) flag.
- **Check [Craft of Exile](https://www.craftofexile.com/)** to understand your odds of certain mods (and adjust `safety_limit` appropriately). And start with a low `safety_limit` to test configuration.

## Questions

- Why do I have to hold <kbd>Shift</kbd> while the script is running? Why can't I afk?
  - Originally, I tried to use the `keyboard` package to continue holding down <kbd>Shift</kbd>, but I couldn't get it to work (maybe it needs a lower level control for direct driver communication). Eventually, I realized this is a feature since it keeps the user still semi-engaged (kind of having your hands on the steering wheel during autopilot).
- Will I get banned for using this?
  - Maybe? I'm not sure. This project is for educational purposes. Use at your own risk.
- My regex didn't work and I wasted 5000 alts since nothing ever matched!!!
  - Remember, you're **NOT** searching against normal <kbd>Ctrl</kbd>-<kbd>C</kbd>. The (Python) regex is being applied to the _advanced_ item description <kbd>Ctrl</kbd>-<kbd>Alt</kbd>-<kbd>C</kbd>. For example, you may see the mod in-game as `+125 to maximum Life`, but the actual text is `+125(115-129) to maximum Life`. See [Tips](#tips) for testing your regex.

## Thanks

- This was originally going to be a fork of [AwakenedAlterationSpam](https://github.com/VVeiVVang/AwakenedAlterationSpam), but I ended up rewriting the whole thing. Thanks to that author, _VVeiVVang_, for the original inspiration!

## Contributing

Feel free to open issues (please read the [Questions](#questions) and [Tips](#tips) section first), submit pull requests, or suggest improvements!
