import performer
import watchman
import random
import tools
import bass
import chords
import melody

rhythm = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]
xlim = 6

def note_no():
    chosen = tools.weighted_choice(tools.rhythm_choices)
    return int(chosen)

def gen_rhythm():
    global rhythm
    tem = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]
    for i in xrange(int(performer.tsig * performer.timing)):
        if random.random() < float(watchman.activities["section"]):
            if tem.count("x") <= xlim:
                tem[note_no()] = "x"

    bass.rhythm = tem
    chords.rhythm = tem
    melody.rhythm = tem
    rhythm = tem

def gen():
    gen_rhythm()