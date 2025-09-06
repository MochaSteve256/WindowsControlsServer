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
    comtypes.CoInitialize()
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level, None)  # type: ignore
        print(f"Master volume set to {level * 100:.0f}%")
        interface.Release()
    except Exception as e:
        print(f"Error setting master volume: {e}")
    finally:
        comtypes.CoUninitialize()

def get_master_volume():
    comtypes.CoInitialize()  # Initialize COM in this thread
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return volume.GetMasterVolumeLevelScalar()  # type: ignore
        interface.Release()
    finally:
        comtypes.CoUninitialize()  # Cleanup COM

# ---
# Music Controls
# ---

path = r"C:\Users\Adrian\Desktop\Code\WindowsControlsServer\MediaControlHelper\bin\Release\net8.0-windows10.0.19041.0\win-x64\publish\MediaControlHelper.exe"
def run_hidden_command(cmd: str):
    subprocess.run(
        [path, cmd],
        check=True,
        creationflags=subprocess.CREATE_NO_WINDOW  # <-- hides the console window
    )


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




if __name__ == "__main__":
    current_volume = get_master_volume()  # Get current volume
    set_master_volume(0.5)  # Set master volume to 50%
