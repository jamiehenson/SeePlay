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
import profiles
from SimpleCV import *

fps = 1
scale = 0.5
active = False

activity_boost = 0

activities = {
    "all" : 0,
    "bass" : 0,
    "chords" : 0,
    "melody" : 0,
    "drums" : 0
}

home = os.path.join(os.path.expanduser('~'))
imgbank = []
imglimit = 5
imgscale = 0.5

def change_activity(inst, val):
    global activities

    corrected_val = (val + activity_boost) / 4
    # corrected_val = (val) / 4

    if abs(activities[inst] - corrected_val) > 0.1 or performer.bar < 4:
        activities[inst] = corrected_val
        activities["all"] = activities["bass"] + activities["drums"] + activities["chords"] + activities["melody"]
        conductor.gen_templates(inst)

def change_all_activity(val):
    change_activity("bass", val)
    change_activity("drums", val)
    change_activity("chords", val)
    change_activity("melody", val)

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
    return newpeak

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

def get_brightness(hist, detail):
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

def count_colours(img):
    r = g = b = 0

    w = img.width
    h = img.height
    step = 2
    rounder = 2

    for i in xrange(0, w, step):
        for j in xrange(0, h, step):
            (r2, g2, b2) = img.getPixel(i, j)
            r += r2
            g += g2
            b += b2
    
    pixtotal = r + g + b

    r_val = round(float(r/pixtotal), rounder)
    g_val = round(float(g/pixtotal), rounder)
    b_val = round(float(b/pixtotal), rounder)

    return [r_val, g_val, b_val]

def invlerp(minval, maxval, val):
    bottomgap = abs(minval - val)
    gap = abs(maxval - minval)
    return max(min(1.0, float(bottomgap / gap)), 0.0) 

def watch(parent):
    if active == True:
        take(parent)

        img = Image(home + "/sp_0.tiff").scale(int(parent.screen_x * imgscale), int(parent.screen_y * imgscale))

        if parent.user_inputsrc == "manual":
            [x,y,w,h] = parent.user_inputregion
            img = img.crop(x * imgscale, y * imgscale, w * imgscale, h * imgscale)
        
        add_to_imgbank(img)

        if parent.user_type == "Standard":
            threading.Timer(0, profiles.standard_b, [parent, img]).start()

        threading.Timer(performer.tempo_in_time, watch, [parent]).start()

def start_watching(parent):
    threading.Timer(0,performer.start,[parent]).start()

    if parent.user_sheetmusic:
        lily.init()

    if parent.user_midioutput:
        recorder.init()

    conductor.init_values(parent)

    threading.Timer(0,watch,[parent]).start()
    threading.Timer(0,conductor.conduct,[parent]).start()

    change_all_activity(0)

    parent.set_user_tempo_modifier(1)

if __name__ == '__main__':
    start_watching()    

