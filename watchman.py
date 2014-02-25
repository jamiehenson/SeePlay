from PySide import QtGui
import time
import rtmidi
import threading
import gui
import performer
import wm_ambient
import os

fps = 1
scale = 0.5
active = True

def take(parent): 
    intype = parent.user_inputsrc

    if intype == "whole":
        os.system("screencapture -xdaro tempout.png")
    else:
        os.system("screencapture -xdaro tempout.png")

def start_watching(parent,show):
    geo = QtGui.QDesktopWidget().availableGeometry()
    w = geo.width()*scale
    h = geo.height()*scale

    midiout = rtmidi.MidiOut(1)
    threading.Timer(0,performer.start,[midiout,parent]).start()

    if parent.user_type == "Ambient":
        wm_ambient.start(parent)

    del midiout

if __name__ == '__main__':
    start_watching()    

