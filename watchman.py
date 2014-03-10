import time
import rtmidi
import threading
import gui
import performer
import conductor
import os
import lily
import recorder
import mixer
from SimpleCV import *

fps = 1
scale = 0.5
active = False
activity = 0

home = os.path.join(os.path.expanduser('~'))
imgbank = []
imglimit = 5
imgscale = 0.5

def change_activity(val):
    global activity

    if val == "up":
        activity += 1
    elif val == "down":
        activity -= 1
    else: 
        activity = val

    conductor.gen_templates(activity)

def take(parent): 
    intype = parent.user_inputsrc
    os.system("screencapture -xdaro " + home + "/sp_0.tiff")

def get_dominant_colour():
    current = imgbank[0]
    
    if len(imgbank) > 1:
        older = imgbank[1]
    else:
        older = current

    newpeak = current.huePeaks()[0]
    oldpeak = older.huePeaks()[0]
    #print newpeak, oldpeak

    #avgpeak = (newpeak + oldpeak) / 2
    #print avgpeak

def get_motion():
    current = imgbank[0]
    
    if len(imgbank) > 1:
        older = imgbank[1]
    else:
        older = current

    diff = current - older

    matrix = diff.getNumpy()
    mean = matrix.mean()

    return mean

def get_histograms():
    for img in imgbank:
        histo = img.histogram()

def compare_colour_channels(img, val):
    (r, g, b) = img.channels()
    rhist = r.histogram(val)
    ghist = g.histogram(val)
    bhist = b.histogram(val)

    return imgbank[0].histogram(val)

def get_brightness(img, val, detail):
    hist = img.histogram(val)
    vals = []
    for i in xrange(detail):
        vals.append(0)

    for j in xrange(detail):
        lower_bound = j * (len(hist) / detail)
        upper_bound = (j+1) * (len(hist) / detail)
        for k in xrange(lower_bound, upper_bound):
            vals[j] += hist[k]

    maxval = max(vals)
    maxbin = [i for i, j in enumerate(vals) if j == maxval]

    return float(maxbin[0]) / float(detail)

def add_to_imgbank(img):
    global imgbank
    while len(imgbank) >= imglimit:
        imgbank.pop()
    imgbank.insert(0,img)

def get_facecount(img):
    faces = img.findHaarFeatures("face.xml")
    f = 0
    if faces:
        for face in faces:
            f += 1
    return f

def watch(parent):
    if active == True:
        take(parent)

        img = Image(home + "/sp_0.tiff").scale(int(parent.screen_x * imgscale), int(parent.screen_y * imgscale))

        if parent.user_inputsrc == "manual":
            [x,y,w,h] = parent.user_inputregion
            img = img.crop(x * imgscale, y * imgscale, w * imgscale, h * imgscale)
        
        add_to_imgbank(img)

        facecount = get_facecount(img)
        parent.set_user_tempo_modifier(1)

        motion = get_motion()
        # if motion > 20: change_activity(1)

        brightness = get_brightness(img, 100, 10)
        mixer.set_volume(parent, "bass", 127 * (1 - brightness))
        mixer.set_volume(parent, "drums", 127 * (1 - brightness))
        mixer.set_volume(parent, "chords", 127 * brightness)

        threading.Timer(performer.tempo_in_time, watch, [parent]).start()

def start_watching(parent):
    midiout = rtmidi.MidiOut(1)
    threading.Timer(0,performer.start,[midiout,parent]).start()

    if parent.user_sheetmusic:
        lily.init()

    if parent.user_midioutput:
        recorder.init()

    conductor.init_values(parent)
    change_activity(0)

    threading.Timer(0,watch,[parent]).start()
    threading.Timer(0,conductor.conduct,[parent]).start()

    #del midiout

if __name__ == '__main__':
    start_watching()    

