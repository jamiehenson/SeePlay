import time
import rtmidi
import threading
import gui
import performer
import conductor
import os

fps = 1
scale = 0.5
active = False
activity = 0

def change_activity(val):
    global activity

    if val == "up":
        activity += 1
    elif val == "down":
        activity -= 1
    else: 
        activity = val

def take(parent): 
    intype = parent.user_inputsrc

    if intype == "whole":
        os.system("screencapture -xdaro tempout.png")
    else:
        os.system("screencapture -xdaro tempout.png")

def start_watching(parent):
    midiout = rtmidi.MidiOut(1)
    threading.Timer(0,performer.start,[midiout,parent]).start()

    conductor.start(parent)

    del midiout

if __name__ == '__main__':
    start_watching()    

