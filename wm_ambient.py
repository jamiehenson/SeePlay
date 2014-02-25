from SimpleCV import *
import threading
import performer
import watchman
import bass_composer
import chord_composer

def watch(parent):
    if watchman.active == True:
    	drumtacet = "H................ S................ K................"
    	tacet = ". . . . . . . . . . . . . . . ."
    	fps = watchman.fps

    	watchman.take(parent)

        img = Image("tempout.png")
        hist = img.histogram()

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

        chord_composer.ambient_chords(parent,0)
        bass_composer.ambient_bass(parent,0)
        performer.add_drums(drumtacet)

        threading.Timer((60.0/float(parent.user_tempo)) * float(parent.user_tsig),watch,[parent]).start()

def start(parent):
    threading.Timer(0,watch,[parent]).start()