import threading
import performer
import watchman
import general_composer
import bass_composer
import chord_composer
import drum_composer
import melody_composer

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
    melody_composer.ambient(parent,thresh)

def gen_templates(level):
    bass_composer.gen(level)
    melody_composer.gen(level)
    drum_composer.gen(level)

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

def conduct(parent):
    if watchman.active == True:
        if parent.user_type == "Ambient":
            ambient(parent, watchman.activity)

        if performer.bar % performer.timing == performer.timing-1 and (performer.main_beat % int(parent.user_tsig) == 0 and performer.main_beat > 0):
            relative_keychange(parent)

        threading.Timer(performer.tempo_in_time,conduct,[parent]).start()