import glob
from random import randrange
import pygame
from pygame import mixer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import keyboard
import string
from threading import *
import math




# load sound files
sounds = glob.glob("sounds/*")
n = len(sounds)
hitsound = glob.glob("hitsound/*")[0]
tapKeys = ["z", "x"]
pygame.mixer.init()







# read system sound level
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))



# balance volume depending on system volume
def balanceVol(modifier):
    #maxVol = 0.0
    #minVol = -65.25
    db = volume.GetMasterVolumeLevel()
    # convert decibel to windows audio percentage
    percentage = math.exp(db*0.06555043 + 4.62041325) -1.56777232
    if (percentage < 12):
        factor = 1
    else:
        # normalize volume
        log = math.log(percentage)
        factor = 70/(percentage*log*log)
    pygame.mixer.music.set_volume(factor*modifier)







# listen for sequence of letters and toggle corresponding settigns
class KeyLoggerXD:
    def __init__(self, enablePhrase, disablePhrase):

        self.enable  =   enablePhrase
        self.disable =  disablePhrase

        self.enableLen = len(self.enable)
        self.disableLen = len(self.disable)

        self.buffers = [self.enable, self.disable]
        self.buffer = self.disable

        self.bufferLens = [self.enableLen, self.disableLen]
        self.bufferLen = self.disableLen

        self.nextIndex = 0
        self.enabled = True

    # match letter to sequence
    def startStop(self, key):
        # if key is the next letter in sequence...
        if (key == self.buffer[self.nextIndex]):
            # prepare for next key
            self.nextIndex = self.nextIndex + 1
            # if the entire sequence was matched, toggle "enabled"
            if (self.nextIndex == self.bufferLen):
                self.nextIndex = 0
                self.enabled = not self.enabled
                self.buffer = self.buffers[self.enabled]
                self.bufferLen = self.bufferLens[self.enabled]
        else:
            # restart if key didnt match
            self.nextIndex = 0



# listen for keypress
def listen(event):
    if event.event_type == "down": 
        key = event.name
        if (key == "space"):
            key = " "

        global nextSound
        # load hitsound
        if (osu.enabled and key in tapKeys):
            nextSound = hitsound
            tapVol = 0.5
            balanceVol(tapVol)
        # loas type sound
        elif (typing.enabled):
            r = randrange(n)
            nextSound = sounds[r]
            balanceVol(1)
        # if enabled, play sound
        if (typing.enabled):
            pygame.mixer.music.load(nextSound)
            pygame.mixer.music.play()
        typing.startStop(key)
        osu.startStop(key)



# start
osu = KeyLoggerXD("enable osu", "disable osu")
typing = KeyLoggerXD("enable sound", "disable sound")
keyboard.hook(listen) 
keyboard.wait() 