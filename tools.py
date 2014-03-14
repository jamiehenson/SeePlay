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

def make_chordscale(key, mode, octave):
    root = roots[key]
    majscale = [root, root+2, root+4, root+5, root+7, root+9, root+11, root+12]
    minscale = [root, root+2, root+3, root+5, root+7, root+8, root+10, root+12]

    majmode = ["+","-","-","-","+","+","-","-"]
    minmode = ["-","-","+","-","-","+","+","-"]

    if mode == "+":
        return midi_to_chord(majscale, majmode, octave)
    else:
        return midi_to_chord(minscale, minmode, octave)

def make_scale(key, mode, octave):
    root = roots[key]
    majscale = [root, root+2, root+4, root+5, root+7, root+9, root+11, root+12]
    minscale = [root, root+2, root+3, root+5, root+7, root+8, root+10, root+12]

    if mode == "+":
        return midi_to_letter(majscale, octave)
    else:
        return midi_to_letter(minscale, octave)

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
    chord = [pitch+octave, pitch+minoroffset+octave, pitch+7+octave, pitch+12+octave, pitch+12+minoroffset+octave, pitch+19+octave, pitch+24+octave]
    return chord

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