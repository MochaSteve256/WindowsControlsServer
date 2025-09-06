from __future__ import print_function
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import os
import keyboard

# ---
# Volume
# ---

def set_master_volume(level):
    """Sets the system speaker master volume.
    
    Args:
        level (float): Volume level (0.0 to 1.0).
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    )
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Set master volume
    volume.SetMasterVolumeLevelScalar(level, None) # type: ignore
    print(f"Master volume set to {level * 100:.0f}%")

def get_master_volume():
    """Gets the current system speaker master volume.
    
    Returns:
        float: Volume level (0.0 to 1.0).
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    )
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Get master volume
    level = volume.GetMasterVolumeLevelScalar() # type: ignore
    print(f"Current master volume: {level * 100:.0f}%")
    return level

# ---
# Music Controls
# ---

def play_pause_music():
    keyboard.send("play/pause media")

def next_track():
    keyboard.send("next track")

def previous_track():
    keyboard.send("previous track")


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
