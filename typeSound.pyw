from __future__ import print_function
from pynput import keyboard
import glob
from random import randrange
import pygame
from pygame import mixer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import librosa
import wave
import sounddevice as sdada
import soundfile as sf
from multiprocessing import Process, Event
import time
from pynput.keyboard import Listener
import keyboard
import string
from threading import *
import random




# load sound files
sounds = glob.glob("sounds/*")
n = len(sounds)
"""
freqs = [None]*n
for i in range(n):
    freqs[i] = wave.open(sounds[i]).getframerate()
"""
r = randrange(n)
nextSound = sounds[r]
#nextFreq = freqs[r]

pygame.mixer.init()


# read system sound level
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


#y, sr = librosa.load(nextSound)
#waveform = librosa.effects.time_stretch(y, 2.0)



# valance volume depending on system volume
def balanceVol():
    #maxVol = 0.0
    #minVol = -65.25
    curr = volume.GetMasterVolumeLevel()
    factor = (curr - 0.2)/(-30*(1 + curr*(curr+30)/(-60)))
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




def listen(event):
    if event.event_type == "down": 
        key = event.name
        if (key == "space"):
            key = " "
        # if enabled, play sound
        if (kl.enabled):
            #global nextFreq

            #speed = random.uniform(0.2, 1)
            #nextFreq = round(nextFreq*speed)
            #pygame.mixer.quit()
            
            global nextSound
            balanceVol()
            pygame.mixer.music.load(nextSound)
            pygame.mixer.music.play()
            r = randrange(n)
            nextSound = sounds[r]


            
            #sd.play(y, nextFreq)
            #sound = pygame.sndarray.make_sound(waveform)
            #sound.play()



            #nextFreq = freqs[r]



            #y, sr = librosa.load(nextSound, sr=16000) # y is a numpy array of the wav file, sr = sample rate
            #y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=4) # shifted by 4 half steps
            #pygame.init()
            #wave = numpy.array([[1,1], [2,2], [3,3]], dtype="int64") # default
            #sound = pygame.sndarray.make_sound(y_shifted)
            #sound.play()

            #y, sr = sf.read(nextSound)
            #y_stretch = pyrubberband.time_stretch(y, sr, 2.0)
            #sps = nextFreq
            #sd.play(y, sps)
            #time.sleep(1)

            
            #nextFreq = freqs[r]
            #nextFreq = round(freqs[r]*0.5)
            #pygame.mixer.quit()
            #pygame.mixer.init(frequency = nextFreq)
        kl.startStop(key)



# start
kl = KeyLoggerXD()
keyboard.hook(listen) 
keyboard.wait() 