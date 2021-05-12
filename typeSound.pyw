from pynput import keyboard
import glob
from random import randrange
import pygame
from pygame import mixer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# load sound files
sounds = glob.glob("sounds/*")
n = len(sounds)
nextSound = sounds[randrange(n)]
pygame.mixer.init()
pygame.mixer.music.load(nextSound)
pygame.mixer.music.set_volume(0.4)


# read system sound level
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# valance volume depending on system volume
def balanceVol():
    #maxVol = 0.0
    #minVol = -65.25
    curr = volume.GetMasterVolumeLevel()
    factor = (curr - 0.2)/(-50)
    pygame.mixer.music.set_volume(factor)







# listen for settings change
class KeyLoggerXD:
    def __init__(self):
        print("init")

        self.enable  =   "enable sound"
        self.disable =  "disable sound"

        self.enableLen = len(self.enable)
        self.disableLen = len(self.disable)

        self.buffers = [self.enable, self.disable]
        self.buffer = self.disable

        self.bufferLens = [self.enableLen, self.disableLen]
        self.bufferLen = self.disableLen

        self.nextIndex = 0
        self.enabled = True

    def startStop(self, key):
        if (key == self.buffer[self.nextIndex]):
            self.nextIndex = self.nextIndex + 1
            if (self.nextIndex == self.bufferLen):
                self.nextIndex = 0
                self.enabled = not self.enabled
                self.buffer = self.buffers[self.enabled]
                self.bufferLen = self.bufferLens[self.enabled]
        else:
            self.nextIndex = 0





def on_press(key):
    # if enabled, play sound
    if (kl.enabled):
        global nextSound
        balanceVol()
        pygame.mixer.music.load(nextSound) 
        pygame.mixer.music.play()
        nextSound = sounds[randrange(n)]
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
        if (k == "space"):
            k = " "
    kl.startStop(k)


# run program
print("type sound started")
kl = KeyLoggerXD()
listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keysadaaaaasda
