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
import tools
import profiles
import math
from SimpleCV import *

fps = 1
scale = 0.5
active = False
processing_rate = 4

activity_boost = 0

activities = {
    "all" : 0,
    "bass" : 0,
    "chords" : 0,
    "melody" : 0,
    "drums" : 0,
    "section" : 0
}

home = os.path.join(os.path.expanduser('~'))
imgbank = []
imglimit = 3
imgscale = 0.5

def change_activity(inst, val, sen):
    global activities

    corrected_val = round(float(val + activity_boost) / float(sen), 3)
    # corrected_val = (val) / 4

    if abs(activities[inst] - corrected_val) > 0.05 or performer.bar < 4:
        activities[inst] = corrected_val
        conductor.gen_templates(inst)

def change_all_activity(val, sen):
    change_activity("bass", val, sen)
    change_activity("drums", val, sen)
    change_activity("chords", val, sen)
    change_activity("melody", val, sen)
    change_activity("section", val, sen)

def take(parent): 
    os.system("screencapture -xdaro " + home + "/sp_0.png")

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

def get_hist_brightness(hist, detail):
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

def get_brightness_grid(img, detail):
    w = img.width / detail
    h = img.height / detail

    vals = []
    for i in xrange(detail):
        vals.append([])
        for j in xrange(detail):
            cropimg = img.crop(j * w, i * h, w, h)
            vals[i].append(get_hist_brightness(cropimg.histogram(255), 20))

    return vals

def get_brightness_totals(vals):
    detail = int(len(vals))
    totals = []
    totalvals = []
    centre = int(math.floor(detail / 2))
    tiers = int(math.ceil((detail + 1) / 2))

    for i in xrange(tiers + 1):
        totals.append([])

    for i in xrange(detail):
        for j in xrange(detail):
            tier = float(max(abs(i - centre), abs(j - centre)) + 1)
            mult = 1 #float(1.0 - (0.1 * tier))
            # if vals[i][j] != 0:
            totals[0].append(vals[i][j] * mult)
            totals[int(tier)].append(vals[i][j] * mult)

    for i in xrange(len(totals)):
        if len(totals[i]) != 0:
            totalvals.append(float(sum(totals[i]) / len(totals[i])))
        else:
            totalvals.append(0)

    # print totals

    return totalvals

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

def count_colour_totals(img):
    r = g = b = 1

    w = img.width
    h = img.height
    step = 2
    
    for i in xrange(0, w, step):
        for j in xrange(0, h, step):
            (r2, g2, b2) = img.getPixel(i, j)
            r += r2
            g += g2
            b += b2
    
    return [r, g, b]

def count_colour_maxtotals(img):
    p = 1

    w = img.width
    h = img.height
    step = 2
    
    for i in xrange(0, w, step):
        for j in xrange(0, h, step):
            p += 255
    
    return p

def count_colours(img):
    [r, g, b] = count_colour_totals(img)
    pixtotal = r + g + b
    rounder = 2

    r_val = round(float(r/pixtotal), rounder)
    g_val = round(float(g/pixtotal), rounder)
    b_val = round(float(b/pixtotal), rounder)

    return [r_val, g_val, b_val]

def get_avg_brightness(img):
    [r, g, b] = count_colour_totals(img)
    total = count_colour_maxtotals(img)

    st = time.time()
    avg = (r + g + b) / 3
    total2 = (total + total + total) / 3
    # print "AVG: ", avg / total2, time.time() - st
    return avg / total2

def get_luminosity(img, lumtype):
    [r, g, b] = count_colour_totals(img)
    total = count_colour_maxtotals(img)

    #Standard
    if lumtype == "a":
        st = time.time()
        lum = (0.2126 * r) + (0.7152 * g) + (0.0722 * b)
        lum_max = (0.2126 * total) + (0.7152 * total) + (0.0722 * total)
        # print "LUMA: ", lum / lum_max, time.time() - st
        return lum / lum_max

    #Percieved A
    elif lumtype == "b":
        st = time.time()
        lum = (0.299 * r) + (0.587 * g) + (0.114 * b)
        lum_max = (0.299 * total) + (0.587 * total) + (0.114 * total)
        # print "LUMB: ", lum / lum_max, time.time() - st
        return lum / lum_max

    #Perceived B, slower to calculate
    elif lumtype == "c":
        st = time.time()
        lum = math.sqrt(math.pow(0.241 * r, 2) + math.pow(0.691 * g, 2) + math.pow(0.068 * b, 2))
        lum_max = math.sqrt(math.pow(0.241 * total, 2) + math.pow(0.691 * total, 2) + math.pow(0.068 * total, 2))
        # print "LUMC: ", lum / lum_max, time.time() - st
        return lum / lum_max

def watch(parent):
    if active == True:
        take(parent)

        img = Image(home + "/sp_0.png").scale(int(parent.screen_x * imgscale), int(parent.screen_y * imgscale))

        if parent.user_inputsrc == "manual":
            [x,y,w,h] = parent.user_inputregion
            img = img.crop(x * imgscale, y * imgscale, w * imgscale, h * imgscale)
        
        add_to_imgbank(img)

        if parent.user_type == "Standard A":
            threading.Timer(0, profiles.standard_a, [parent, img]).start()
        elif parent.user_type == "Standard B":
            threading.Timer(0, profiles.standard_b, [parent, img]).start()
        elif parent.user_type == "Sparse":
            threading.Timer(0, profiles.sparse, [parent, img]).start()

        threading.Timer(performer.tempo_in_time / processing_rate, watch, [parent]).start()

def start_watching(parent):
    threading.Timer(0,performer.start,[parent]).start()

    if parent.user_sheetmusic:
        lily.init()

    if parent.user_midioutput:
        recorder.init(parent)

    conductor.init_values(parent)

    threading.Timer(0,watch,[parent]).start()
    threading.Timer(0,conductor.conduct,[parent]).start()

    change_all_activity(0, 4)

    parent.set_user_tempo_modifier(1)

if __name__ == '__main__':
    start_watching()    

