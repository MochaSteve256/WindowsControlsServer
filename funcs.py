from __future__ import print_function
from ctypes import cast, POINTER
# from ctypes import windll
from comtypes import CLSCTX_ALL
import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import subprocess

import os
# import keyboard as kb

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
    
    # Explicitly release COM objects
    interface.Release()
    comtypes.CoUninitialize()

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
    
    # Explicitly release COM objects
    interface.Release()
    comtypes.CoUninitialize()

    return level

# ---
# Music Controls
# ---

path = "MediaControlHelper\\bin\\Release\\net8.0-windows10.0.19041.0\\win-x64\\publish\\MediaControlHelper.exe"

def play_pause_music():
    subprocess.run([path, "playpause"], check=True)

def next_track():
    subprocess.run([path, "next"], check=True)

def previous_track():
    subprocess.run([path, "prev"], check=True)

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
