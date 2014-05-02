import tools
import performer
import conductor
import random
import section
import watchman

current_bass = ". . . . . . . . . . . . . . . ."
rhythm = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]
b_lock = False
prev_degree = 0
degree = 0 # The tonic by default

def make_phrase(template, scale):
    bar = ""
    sequence = template.split()
    for note in sequence:
        if note != "." and note.startswith("r") == False:
            note = str(scale[int(note[:1])] + str(note[-2:]))
        bar += (note + " ")
    return bar

def gen_rhythm(template):
    newtem = template
    for i in xrange(0, len(template), 1):
        if (random.random() < float(watchman.activities["bass"])):
            if template[i] == "." and newtem.count("x") <= section.xlim:
                newtem[i] = "x"
            else:
                newtem[i] = "."

    return newtem

def gen_notes(template):
    global degree, prev_degree
    # Note lengths and pitch
    newtem = template
    edited = False
    newdeg = 0
    icount = 0

    # print "B", newtem
    for i in xrange(int(performer.tsig * performer.timing)):
        if template[i] != ".":
            newdeg, newtem = tools.place_notes(i, template, True, degree, prev_degree)
            prev_degree = degree
            degree = newdeg
            edited = True
            icount = i
    # print "A", newtem
        else:
            newtem[i] = "."

    if edited == False:
        newtem[0] = "r1"
    else:
        if abs(int(icount) - int(performer.tsig * performer.timing)) > (tools.lengths[newtem[icount][-2:]] * performer.timing):
            for j in xrange(int(icount+1), int(performer.tsig * performer.timing)):
                newtem[j] = "rse"

    # Starting rest
    if template[0] == '.':
        newdeg, newtem = tools.place_notes(0, template, False, degree, prev_degree)

    return newtem

def gen():
    global current_bass, b_lock
    if b_lock == False:
        current_bass = " ".join(gen_notes(gen_rhythm(rhythm)))
        # current_bass = " ".join(gen_notes(rhythm))
        b_lock = True

def play():
    key = conductor.relativekey
    mode = conductor.relativemode
    octave = str(1)

    scale = tools.make_scale(key, mode, octave)

    bar = make_phrase(current_bass, scale)

    while len(performer.basslines) <= performer.buff: 
        performer.add_bass(bar)
