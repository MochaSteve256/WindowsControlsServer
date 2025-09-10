from __future__ import print_function
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


import threading
import os
import keyboard
import time

time.sleep(1)

# ---
# Volume
# ---

_volume_lock = threading.Lock()

def set_master_volume(level: float):
    with _volume_lock:
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level, None)  # type: ignore
            # Explicitly release COM objects
            interface = None
            devices = None
            print(f"Master volume set to {level*100:.0f}%")
        except Exception as e:
            print(f"[Volume Error] {e}")

def get_master_volume() -> float:
    with _volume_lock:
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            level = volume.GetMasterVolumeLevelScalar()  # type: ignore
            # Explicitly release COM objects
            interface = None
            devices = None
            return level
        except Exception as e:
            print(f"[Volume Error] {e}")
            return -1.0


# ---
# Music Controls
# ---

def play_pause_music():
    keyboard.send('play/pause media')

def next_track():
    keyboard.send('next track')

def previous_track():
    keyboard.send('previous track')


# ---
# General
# ---

def lock_screen():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def shutdown():
    os.system("shutdown /s /t 0")


if __name__ == "__main__":
    current_volume = get_master_volume()  # Get current volume
    set_master_volume(0.5)  # Set master volume to 50%
