from __future__ import print_function
from ctypes import cast, POINTER, windll
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import os
#import keyboard as kb

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

# Windows API function
SendInput = windll.user32.keybd_event

# Virtual key codes for media keys
VK_MEDIA_PLAY_PAUSE = 0xB3
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1


def play_pause_music():
    #kb.send("play/pause media")
    SendInput(VK_MEDIA_PLAY_PAUSE, 0, 0, 0)

def next_track():
    # kb.send("next track")
    SendInput(VK_MEDIA_NEXT_TRACK, 0, 0, 0)

def previous_track():
    # kb.send("previous track")
    SendInput(VK_MEDIA_PREV_TRACK, 0, 0, 0)


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
