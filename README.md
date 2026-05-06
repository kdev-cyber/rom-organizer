# ROM Organizer

⚠️ Always run in dry mode first to preview changes before moving files.

A Python script that organizes ROM files from a single inbox folder into clean, system-specific folders.

---

## 🚀 Features

- Automatically sorts ROMs by system
- Cleans up messy filenames
- Extracts `.zip` files automatically
- Moves matching save files alongside ROMs
- Sends duplicates to a `99_Review` folder
- Handles leftover/orphan save files
- Simple and fast batch processing

---

## 🧠 How It Works

The script scans a `00_Inbox` folder and:

- Detects ROMs by file extension
- Cleans filenames
- Moves them into the correct system folders

### It also:

- Extracts `.zip` files found in the inbox
- Moves matching save files with their ROMs
- Sends duplicates or unknown files to `99_Review`
- Sends leftover save/state files to `99_Review`

---

## 🎮 Supported Systems

- NES (`.nes`)
- SNES (`.smc`, `.sfc`)
- N64 (`.n64`, `.z64`, `.v64`)
- Game Boy (`.gb`)
- Game Boy Color (`.gbc`)
- Game Boy Advance (`.gba`)
- SEGA Genesis / Mega Drive (`.gen`, `.md`, `.smd`)
- Nintendo 3DS (`.3ds`, `.cci`, `.cxi`)

---

## 📁 Folder Structure

Expected ROM root layout:

```text
ROMs/
00_Inbox/
99_Review/
NES/
SNES/
N64/
GameBoy/
GameBoyColor/
GameBoyAdvance/
SEGA Genesis/
3DS/
```