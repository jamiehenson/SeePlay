from SimpleCV import *
import rtmidi
import threading
import performer
import watchman

def watch(w, h, show, midiout):
    if watchman.active == True:
    	fps = watchman.fps
        os.system("screencapture -x -d -a -r -o tempout.png")

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
        performer.add_bass("G2 . . C2 . . G3 . . . C1 . . . . . ")
        performer.add_drums("Hxxxxxxxxxxxxxxxx S.x..x....x..x... Kx.xx..xx..xx....")

        if show == True:
            img.show()

        threading.Timer(1/fps,watch,[w,h,show,midiout]).start()

def start(w,h,show,midiout):
    threading.Timer(0,watch,[w,h,show,midiout]).start()