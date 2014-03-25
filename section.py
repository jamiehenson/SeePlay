import performer
import watchman
import random
import tools

blank = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]
rhythm = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]

def place_note(template):
    newtem = template
    chosen = int(tools.weighted_choice(tools.rhythm_choices))
    newtem[chosen] = "x"
    return newtem

def gen_rhythm():
    global rhythm
    template = blank
    for i in xrange(int(performer.tsig * performer.timing)):
        if random.random() < watchman.activities["section"]:
            place_note(template)

    rhythm = template

def gen():
    gen_rhythm()