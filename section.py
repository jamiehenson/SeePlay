import performer
import watchman
import random
import tools

blank = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]
rhythm = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]

def note_no():
    chosen = tools.weighted_choice(tools.rhythm_choices)
    return int(chosen)

def gen_rhythm():
    global rhythm
    tem = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]
    for i in xrange(int(performer.tsig * performer.timing) / 4):
        if random.random() < watchman.activities["section"]:
            tem[note_no()] = "x"

    rhythm = tem

def gen():
    gen_rhythm()