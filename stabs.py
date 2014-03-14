import tools
import performer
import conductor
import random
import mixer
import time
import math

def multifire(motion):
    divider = 10
    intensity = int(pow(2, math.floor(math.log(motion, 2)))) / 4

    for i in xrange(int(motion / divider)):
        fire()
        time.sleep(performer.tempo_in_time / intensity)

def fire():
    key = conductor.relativekey
    mode = conductor.relativemode
    octave = str(3)

    scale = tools.make_scale(key, mode, octave)

    scalenote = scale[random.randrange(len(scale))]
    scalenote = scalenote[:-1]
    stabnote = tools.letter_to_midi(scalenote, 3)

    performer.play_note(int(mixer.get_channel("stabs")), stabnote, 0.01)
