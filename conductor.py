import threading
import performer
import watchman
import tools
import bass
import chords
import drum
import melody
import section
import random

relativekey = "C"
relativemode = "major"
circleno = 0
cycle = 4

def init_values(parent):
    global relativekey
    global relativemode

    relativekey = parent.user_key
    relativemode = parent.user_mode

    if parent.user_prog_type == "random":
        temp_progs = parent.prog_types
        del temp_progs["Random"]
        random_type = temp_progs[random.choice(list(temp_progs.keys()))]
        revprogs = dict((v,k) for k,v in temp_progs.iteritems())
        parent.set_user_prog_type(revprogs[random_type])

def gen_templates(inst):
    if inst == "bass":
        bass.gen()
    elif inst == "melody":
        melody.gen()
    elif inst == "drums":
        drum.gen()
    elif inst == "chords":
        chords.gen()
    elif inst == "section":
        section.gen()

def prog_relative(parent):
    global relativekey
    global relativemode

    modbar = performer.bar % cycle

    if modbar == 0:
        if relativemode == "major":
            relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] - 3) % 12)
            relativemode = "minor"
        elif relativemode == "minor":
            relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] + 3) % 12)
            relativemode = "major"
    elif modbar == cycle:
        relativekey = parent.user_key
        relativemode = parent.user_mode

def prog_none(parent):
    return 0

def prog_random(parent):
    return 0

def prog_blues(parent):
    global relativekey
    modbar = performer.bar % (3 * cycle)

    if modbar == 0 or modbar == cycle + (cycle / 2) or modbar == ((2 * cycle) + (cycle / 2)):
        relativekey = tools.midi_to_genletter((tools.roots[parent.user_key]) % 12)
    elif modbar == cycle or modbar == (2 * cycle) + (cycle / 4):
        relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] + 5) % 12)
    elif modbar == (2 * cycle):
        relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] + 7) % 12)

def prog_fifth(parent):
    global relativekey

    modbar = performer.bar % (2 * cycle)

    if modbar == 0:
        relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] + 7) % 12)
    elif modbar == cycle:
        relativekey = parent.user_key

def prog_50s(parent):
    global relativekey
    modbar = performer.bar % (4 * cycle)

    if modbar == 0:
        relativekey = tools.midi_to_genletter((tools.roots[parent.user_key]) % 12)
    elif modbar == cycle:
        relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] + 9) % 12)
    elif modbar == (2 * cycle):
        relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] + 5) % 12)
    elif modbar == (3 * cycle):
        relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] + 7) % 12)

def prog_circ5(parent):
    global circleno, relativekey
    modbar = performer.bar % cycle

    if modbar == 0:
        relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] + (7 * circleno)) % 12)
        circleno += 1

def prog_circ4(parent):
    global circleno, relativekey
    modbar = performer.bar % cycle

    if modbar == 0:
        relativekey = tools.midi_to_genletter((tools.roots[parent.user_key] + (5 * circleno)) % 12)
        circleno += 1

def progression(parent, prog_type):
    if prog_type == "none":
        prog_none(parent)
    elif prog_type == "random":
        prog_random(parent)
    elif prog_type == "blues":
        prog_blues(parent)
    elif prog_type == "relative":
        prog_relative(parent)
    elif prog_type == "fifth":
        prog_fifth(parent)
    elif prog_type == "50s":
        prog_50s(parent)
    elif prog_type == "circ4":
        prog_circ4(parent)
    elif prog_type == "circ5":
        prog_circ5(parent)
    else:
        print "Incorrect progression call."

def conduct(parent):
    global relativemode
    global relativekey

    if watchman.active == True:
        chords.play()
        bass.play()
        drum.play()
        melody.play()

        if performer.bar > 0:
            relativemode = parent.user_mode
            relativekey = parent.user_key
            progression(parent, parent.user_prog_type)

        threading.Timer(performer.tempo_in_time,conduct,[parent]).start()