from SimpleCV import *
import threading
import performer
import watchman
import general_composer
import bass_composer
import chord_composer
import drum_composer

relativekey = "F"
relativemode = "+"
modulated = False

def init_values(parent):
    global relativekey
    global relativemode
    global modulated

    relativekey = parent.user_key
    relativemode = parent.user_mode
    modulated = False

def ambient(parent,thresh):
	chord_composer.ambient(parent,thresh)
	bass_composer.ambient(parent,thresh)
	drum_composer.ambient(parent,thresh)

def relative_keychange(parent):
    global relativekey
    global relativemode
    global modulated

    if modulated == False:
        if relativemode == "+":
            relativekey = general_composer.midi_to_genletter((general_composer.roots[parent.user_key] - 3) % 12)
            relativemode = "-"
        else:
            relativekey = general_composer.midi_to_genletter((general_composer.roots[parent.user_key] + 3) % 12)
            relativemode = "+"
        modulated = True
    else:
        relativekey = parent.user_key
        relativemode = parent.user_mode
        modulated = False

def watch(parent):
    global relativemode
    global relativekey

    if watchman.active == True:
    	fps = watchman.fps

    	# watchman.take(parent)
        # img = Image("tempout.png")
        # hist = img.histogram()

        # segmented = dist.stretch(200,255)
        # blobs = segmented.findBlobs()
        # if blobs:
        #     circles = blobs.filter([b.isCircle(0.5) for b in blobs])
        #     if circles:
        #         #img.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),SimpleCV.Color.BLUE,3)
        # performer.add_bass("C4 . . D4 . . E4 . . . F5 . G5 . . .")
        #performer.enqueue_bass(midiout,0.5)
        # performer.add_bass("G2 . . C2 . . G3 . . . C1 . . . . . ")
        # performer.add_drums("Hxxxxxxxxxxxxxxxx S.x..x....x..x... Kx.xx..xx..xx....")

        if parent.user_type == "Ambient":
        	ambient(parent, watchman.activity)

        if performer.bar % performer.timing == performer.timing-1 and (performer.main_beat % int(parent.user_tsig) == 0 and performer.main_beat > 0):
            relative_keychange(parent)

        threading.Timer(performer.tempo_in_time,watch,[parent]).start()

def start(parent):
    init_values(parent)
    threading.Timer(0,watch,[parent]).start()