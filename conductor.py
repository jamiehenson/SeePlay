import threading
import performer
import watchman
import tools
import bass
import chords
import drum
import melody

relativekey = "C"
relativemode = "+"
modulated = False

def init_values(parent):
    global relativekey
    global relativemode
    global modulated

    relativekey = parent.user_key
    relativemode = parent.user_mode
    modulated = False

def gen_templates(inst):
    if inst == "bass":
        bass.gen()
    elif inst == "melody":
        melody.gen()
    elif inst == "drums":
        drum.gen()
    elif inst == "chords":
        chords.gen()

def relative_keychange(parent):
    global relativekey
    global relativemode
    global modulated

    if modulated == False:
        if relativemode == "+":
            relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] - 3) % 12)
            relativemode = "-"
        else:
            relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] + 3) % 12)
            relativemode = "+"
        modulated = True
    else:
        relativekey = parent.user_key
        relativemode = parent.user_mode
        modulated = False

def conduct(parent):
    if watchman.active == True:
        chords.play()
        bass.play()
        drum.play()
        melody.play()

        if performer.bar > 0:
            case1 = True if performer.bar % (performer.timing * 2) == performer.timing - 1 else False
            case2 = True if performer.main_beat % int(parent.user_tsig) == 0 else False
            case3 = True if performer.main_beat > 0 else False

            if case1 and case2 and case3:
                relative_keychange(parent)

        threading.Timer(performer.tempo_in_time,conduct,[parent]).start()