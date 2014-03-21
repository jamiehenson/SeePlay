import performer
import math
import random

# UTILITIES

roots = {
   "C" : 0,
   "C#" : 1,
   "D" : 2,
   "Eb" : 3,
   "E" : 4,
   "F" : 5,
   "F#" : 6,
   "G" : 7,
   "Ab" : 8,
   "A" : 9,
   "Bb" : 10,
   "B" : 11
}

lengths = {
    "se" : 0.25,
    "qu" : 0.5,
    "dq" : 0.75,
    "cr" : 1.0,
    "dc" : 1.5,
    "mi" : 2.0,
    "dm" : 3.0,
    "S1" : 4.0,
    "S2" : 8.0,
    "S3" : 12.0,
    "S4" : 16.0,
    "S6" : 24.0,
    "S8" : 32.0
}

intervals = {
    "major" : [0,2,4,5,7,9,11,12],
    "minor" : [0,2,3,5,7,8,10,12],
    "ionian" : [0,2,4,5,7,9,11,12],
    "dorian" : [0,2,3,5,7,9,10,12],
    "phrygian" : [0,1,3,5,7,8,10,12],
    "lydian" : [0,2,4,6,7,9,11,12],
    "mixolydian" : [0,2,4,5,7,9,10,12],
    "aeolian" : [0,2,3,5,7,8,10,12],
    "locrian" : [0,1,3,5,6,8,10,12],
    "arabic" : [0,1,4,5,7,8,11,12]
}

note_modes = {
    "major" : ["+", "-", "-", "+", "+", "-", "-", "+"],

    "minor" : ["-", "-", "+", "+", "+", "-", "-", "-"],

    "ionian" : ["+", "-", "-", "+", "+", "-", "-", "+"],

    "dorian" : ["-", "-", "+", "+", "-", "-", "+", "+"],

    "phrygian" : ["-", "+", "+", "-", "-", "+", "+", "+"],

    "lydian" : ["+", "+", "-", "-", "+", "-", "-", "+"],

    "mixolydian" : ["+", "-", "-", "-", "+", "-", "-", "+"],

    "aeolian" : ["-", "-", "+", "-", "-", "+", "+", "+"],

    "locrian" : ["-", "+", "-", "-", "+", "+", "-", "+"],

    "arabic" : ["-", "-", "-", "-", "-", "-", "-", "-"]
}

note_choices = [(0,0.3), (1,0.05), (2,0.1), (3,0.2), (4,0.2), (5,0.05), (6,0.05), (7,0.05)]

def length_key_check(num):
    revlength = dict((v,k) for k,v in lengths.iteritems())
    return True if num in revlength else False

def length_num_to_code(num):
    revlength = dict((v,k) for k,v in lengths.iteritems())
    return revlength[num]

def letter_to_midi(note, octave):
    return roots[note] + (octave * 12) + 24

def midi_to_genletter(note):
    revroots = dict((v,k) for k,v in roots.iteritems())
    return revroots[note % 12]

def midi_to_chord(scale, mode, octave):
    newscale = []
    revroots = dict((v,k) for k,v in roots.iteritems())

    for i in xrange(len(scale)):
        newscale.append(revroots[scale[i] % 12] + str(octave) + mode[i])

    return newscale

def midi_to_letter(scale, octave):
    newscale = []
    revroots = dict((v,k) for k,v in roots.iteritems())

    for note in scale:
        newscale.append(revroots[note % 12] + str(octave))

    return newscale

def scale_intervals(root, mode):
    intvals = intervals[mode]
    newints = []
    for i in xrange(len(intvals)):
        newints.append(root + intvals[i])

    return newints

def make_chordscale(key, mode, octave):
    root = roots[key]
    intervals = scale_intervals(root, mode)
    notemodes = note_modes[mode]

    return midi_to_chord(intervals, notemodes, octave)

def make_scale(key, mode, octave):
    root = roots[key]
    intervals = scale_intervals(root, mode)

    return midi_to_letter(intervals, octave)

def make_chord(key, mode, octave):
    chordname = key + str(octave) + mode

    return chordname

def get_chord(chord):
    if len(chord) == 6:
        pitch = chord[:2]
    else:
        pitch = chord[:1]

    octave = int(chord[-4:-3]) * 12
    mode = str(chord[-3:-2])

    pitch = letter_to_midi(pitch, 0)
    minoroffset = 3 if mode == "-" else 4
    newchord = [pitch+octave, pitch+minoroffset+octave, pitch+7+octave, pitch+12+octave, pitch+12+minoroffset+octave, pitch+19+octave, pitch+24+octave]
    return newchord

def find_next_note(i, template):
    next_note = float(performer.tsig * performer.timing)
    for j in xrange(i+1, int(performer.tsig * performer.timing)):
        if template[j] != ".":
            next_note = float(j)
            break
    
    return float((next_note - i) / performer.timing)

def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w > r:
            return str(c)
        upto += w

def place_notes(i, template, notes):
    code = find_next_note(i, template)
    
    if notes:
        chosen_scaleno = weighted_choice(note_choices)
    else:
        chosen_scaleno = "r"

    if length_key_check(code):
        chosen_length = str(length_num_to_code(code))
        template[i] = chosen_scaleno + chosen_length
    else:
        rounded = float(pow(2, math.floor(math.log(code, 2))))
        diff = code - rounded
        long_length = str(length_num_to_code(rounded))
        template[i] = chosen_scaleno + long_length

    # Might not be enough
        if length_key_check(diff):
            short_length = str(length_num_to_code(diff))
            template[i + int(rounded * 4)] = chosen_scaleno + short_length
        else:
            roundtwo = float(pow(2, math.floor(math.log(diff, 2))))
            difftwo = diff - roundtwo
            long_lengthtwo = str(length_num_to_code(roundtwo))
            template[i + int(rounded * 4)] = chosen_scaleno + long_lengthtwo
            shorter_length = str(length_num_to_code(difftwo))
            template[i + int(rounded * 4) + int(roundtwo * 4)] = chosen_scaleno + shorter_length

    return template

def clamp(minval, maxval, val):
    return max(min(maxval, minval + val), minval)

def invlerp(minval, maxval, val):
    bottomgap = abs(minval - val)
    gap = abs(maxval - minval)
    return clamp(0.0, 1.0, float(bottomgap / gap))