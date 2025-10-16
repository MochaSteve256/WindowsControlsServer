import subprocess
import os
import re

# Path to your compiled C# helper
path = r"C:\Users\Adrian\Desktop\Code\WindowsControlsServer\MediaControlHelper\bin\Release\net8.0-windows10.0.19041.0\MediaControlHelper.exe"

def run_hidden_command(*args):
    """Run the MediaControlHelper command silently and capture its output."""
    result = subprocess.run(
        [path, *args],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW  # <-- hides the console window

    )
    # Combine stdout + stderr, strip trailing newlines
    output = (result.stdout or "") + (result.stderr or "")
    return output.strip()

# ---
# Volume
# ---

def set_master_volume(level: float):
    # level is between 0 and 100
    print(level)
    run_hidden_command("setvolume", str(int(level * 100)))


def get_master_volume() -> float:
    output = run_hidden_command("getvolume")

    # try to extract digits like "42" from "Current volume: 42%"
    match = re.search(r"(\d+(?:\.\d+)?)\s*%", output)
    if match:
        return float(match.group(1)) / 100
    else:
        print(f"[WARN] Could not parse volume from output: {repr(output)}")
        return 0.0

# ---
# Music Controls
# ---

def play_pause_music():
    run_hidden_command("playpause")

def next_track():
    run_hidden_command("next")

def previous_track():
    run_hidden_command("prev")

# ---
# General
# ---

def lock_screen():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def shutdown():
    os.system("shutdown /s /t 0")

# ---
# Demo
# ---

if __name__ == "__main__":
    vol = get_master_volume()
    print(f"Detected system volume: {vol}%")
    set_master_volume(50)
    print("Volume set to 50%.")
