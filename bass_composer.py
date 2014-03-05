import general_composer
import performer
import conductor
import random
import math

current_bass = ". . . . . . . . . . . . . . . ."

def make_phrase(template, scale):
    bar = ""
    sequence = template.split()
    for note in sequence:
        if note != "." and note.startswith("r") == False:
            note = str(scale[int(note[:1])] + str(note[-2:]))
        bar += (note + " ")

    return bar

def find_next_note(i, template):
    next_note = float(performer.tsig * performer.timing)
    for j in xrange(i+1, int(performer.tsig * performer.timing)):
        if template[j] != ".":
            next_note = float(j)
            break
    
    return float((next_note - i) / performer.timing)

def place_notes(i, template, notes):
    code = find_next_note(i, template)
    
    if notes:
        chosen_scaleno = str(random.randrange(0,5))
    else:
        chosen_scaleno = "r"
        print "Resto",code

    if general_composer.length_key_check(code):
        chosen_length = str(general_composer.length_num_to_code(code))
        template[i] = chosen_scaleno + chosen_length
    else:
        rounded = float(pow(2, math.floor(math.log(code, 2))))
        diff = code - rounded
        long_length = str(general_composer.length_num_to_code(rounded))
        short_length = str(general_composer.length_num_to_code(diff))
        template[i] = chosen_scaleno + long_length
        template[i + int(rounded * 4)] = chosen_scaleno + short_length

    return template

def gen(threshold):
    global current_bass

    template = []

    # Rhythm
    for i in xrange(int(performer.tsig * performer.timing)):
        if random.random() < 0.3:
            template.append("x")
        else:
            template.append(".")

    # Note lengths and pitch
    if "x" in template:
        for i in xrange(int(performer.tsig * performer.timing)):
            if template[i] != ".":
                template = place_notes(i, template, True)
    #else:
        #template[0] = "r1"

    # Starting rest
    if template[0] == '.':
        template = place_notes(0, template, False)

    current_bass = " ".join(template)

# Ambient
def ambient(parent, threshold):
    key = conductor.relativekey
    mode = conductor.relativemode
    octave = str(1)

    scale = general_composer.make_scale(key, mode, octave)

    template1 = "0S1 . . . . . . . . . . . . . . ."
    template1a = "0qu . 1qu . 2qu . 3qu . 4qu . 3qu . 2qu . 1qu ."
    template2 = "0cr . . . . . . . 1mi . . . . . ."
    template3 = "0cr . . 1cr . . 4cr . . . 0cr . 0cr . . ."

    bar = make_phrase(current_bass, scale)

    while len(performer.basslines) <= performer.buff: 
        performer.add_bass(bar)
