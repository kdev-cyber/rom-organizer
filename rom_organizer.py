import os
import re
import zipfile
from helpers import get_input

print("\n=== ROM Organizer v2 ===\n")

# ===== SETTINGS =====

rom_root = get_input(
    "Enter ROM root folder",
    r"C:\Users\K\Documents\Retro\ROMs"
)

source_folder = os.path.join(rom_root, "00_Inbox")
review_folder = os.path.join(rom_root, "99_Review")

dry_run = get_input(
    "Dry run mode? Preview only, no files moved. (y/n)",
    "y"
).lower() == "y"

planned_save_moves = set()

if dry_run:
    print("\n[MODE] Dry run enabled. No files will be moved, extracted, deleted, or renamed.\n")
else:
    print("\n[MODE] Live run enabled. Files may be moved, extracted, deleted, or renamed.\n")

if not os.path.exists(rom_root):
    print("[ERROR] ROM root folder does not exist.")
    exit()

if not dry_run:
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(review_folder, exist_ok=True)


# ===== HELPERS =====

def detect_system(filename):
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".nes":
        return "NES"
    elif ext in [".smc", ".sfc"]:
        return "SNES"
    elif ext in [".n64", ".z64", ".v64"]:
        return "N64"
    elif ext == ".gba":
        return "GameBoyAdvance"
    elif ext == ".gb":
        return "GameBoy"
    elif ext == ".gbc":
        return "GameBoyColor"
    elif ext in [".gen", ".md", ".smd"]:
        return "SEGA Genesis"
    elif ext in [".3ds", ".cci", ".cxi"]:
        return "3DS"
    else:
        return "Unknown"


def clean_filename(filename):
    name, ext = os.path.splitext(filename)

    name = re.sub(r"\[.*?\]", "", name)
    name = re.sub(r"\(.*?\)", "", name)
    name = re.sub(r"\s+", " ", name).strip()

    return name + ext


def get_unique_path(folder, filename):
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(folder, filename)

    if not os.path.exists(candidate):
        return candidate

    counter = 1
    while True:
        candidate = os.path.join(folder, f"{base}_DUPLICATE_{counter}{ext}")
        if not os.path.exists(candidate):
            return candidate
        counter += 1


def move_file(src, destination):
    if dry_run:
        print(f"[DRY RUN] {src} -> {destination}")
    else:
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        os.rename(src, destination)
        print(f"[MOVE] {src} -> {destination}")


# ===== ZIP EXTRACTION =====

def extract_zip_files():
    print("[INFO] Checking ZIP files...")

    if not os.path.exists(source_folder):
        print("[INFO] 00_Inbox folder does not exist yet.")
        return

    for file in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file)

        if os.path.isdir(file_path):
            continue

        if file.lower().endswith(".zip"):
            try:
                if dry_run:
                    print(f"[DRY RUN] Would extract ZIP: {file}")
                    print(f"[DRY RUN] Would delete ZIP after extraction: {file}")
                else:
                    with zipfile.ZipFile(file_path, "r") as zip_ref:
                        zip_ref.extractall(source_folder)

                    os.remove(file_path)
                    print(f"[ZIP] Extracted and deleted ZIP: {file}")

            except zipfile.BadZipFile:
                bad_zip_path = get_unique_path(review_folder, file)
                move_file(file_path, bad_zip_path)
                print(f"[WARN] Bad ZIP file sent to Review: {file}")


# ===== SAVE FILE HANDLING =====

def move_matching_save(file, destination_folder, clean_name):
    original_base, _ = os.path.splitext(file)
    clean_base, _ = os.path.splitext(clean_name)

    save_extensions = [".sav", ".state", ".srm"]

    for ext in save_extensions:
        original_save = os.path.join(source_folder, original_base + ext)

        if os.path.exists(original_save):
            planned_save_moves.add(os.path.abspath(original_save))

            desired_save_name = clean_base + ext
            save_destination = os.path.join(destination_folder, desired_save_name)

            if os.path.exists(save_destination):
                review_save_path = get_unique_path(review_folder, desired_save_name)
                move_file(original_save, review_save_path)
                print(f"[SAVE] Duplicate save detected: {original_base + ext} -> Review")
            else:
                move_file(original_save, save_destination)
                print(f"[SAVE] Moved save: {original_base + ext} -> {desired_save_name}")


# ===== ROM SORTING =====

def sort_rom_files():
    print("[INFO] Sorting ROM files...")

    if not os.path.exists(source_folder):
        print("[INFO] 00_Inbox folder does not exist yet.")
        return

    for file in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file)

        if os.path.isdir(file_path):
            continue

        if file.lower().endswith((".sav", ".state", ".srm")):
            continue

        system = detect_system(file)

        if system == "Unknown":
            destination_folder = review_folder
        else:
            destination_folder = os.path.join(rom_root, system)

        clean_name = clean_filename(file)
        destination_path = os.path.join(destination_folder, clean_name)

        if os.path.exists(destination_path):
            review_path = get_unique_path(review_folder, clean_name)
            move_file(file_path, review_path)
            print(f"[DUPLICATE] {file} -> Review")
            continue

        move_file(file_path, destination_path)
        move_matching_save(file, destination_folder, clean_name)
        print(f"[ROM] {file} -> {clean_name} [{system}]")


def move_leftover_saves():
    print("[INFO] Checking leftover save/state files...")

    if not os.path.exists(source_folder):
        print("[INFO] 00_Inbox folder does not exist yet.")
        return

    for file in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file)
        absolute_file_path = os.path.abspath(file_path)

        if os.path.isdir(file_path):
            continue

        if absolute_file_path in planned_save_moves:
            continue

        if file.lower().endswith((".sav", ".state", ".srm")):
            review_path = get_unique_path(review_folder, file)
            move_file(file_path, review_path)
            print(f"[SAVE] Leftover save/state file sent to Review: {file}")


# ===== RUN SCRIPT =====

extract_zip_files()
sort_rom_files()
move_leftover_saves()

print("\n=== Done ===\n")