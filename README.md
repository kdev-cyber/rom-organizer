# ROM Organizer

A Python script that organizes ROM files from a single inbox folder into system-specific folders.

## What it does

This script scans a `00_Inbox` folder, detects ROM files by extension, cleans up filenames, and moves them into the correct system folders.

It also:

- extracts `.zip` files found in the inbox
- moves matching save files alongside ROMs
- sends duplicate or unknown files to a `99_Review` folder
- sends leftover orphan save/state files to `99_Review`

## Supported systems

- NES (`.nes`)
- SNES (`.smc`, `.sfc`)
- N64 (`.n64`, `.z64`, `.v64`)
- Game Boy (`.gb`)
- Game Boy Color (`.gbc`)
- Game Boy Advance (`.gba`)
- SEGA Genesis / Mega Drive (`.gen`, `.md`, `.smd`)
- Nintendo 3DS (`.3ds`, `.cci`, `.cxi`)

## Folder structure

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