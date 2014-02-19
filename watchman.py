from PySide import QtGui
import sched
import time
import rtmidi
import threading
import performer
import wm_ambient

watch_loop = sched.scheduler(time.time, time.sleep)
fps = 1
scale = 0.5
active = True
    
def start_watching(show):
    geo = QtGui.QDesktopWidget().availableGeometry()
    w = geo.width()*scale
    h = geo.height()*scale

    midiout = rtmidi.MidiOut(1)
    threading.Timer(0,performer.start,[midiout]).start()

    wm_ambient.start(w,h,show,midiout)

    del midiout

if __name__ == '__main__':
    start_watching()    

